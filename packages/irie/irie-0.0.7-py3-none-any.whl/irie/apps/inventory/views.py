#===----------------------------------------------------------------------===#
#
#         STAIRLab -- STructural Artificial Intelligence Laboratory
#
#===----------------------------------------------------------------------===#
#
#   Summer 2023, BRACE2 Team
#   Berkeley, CA
#
#----------------------------------------------------------------------------#
import os
import re
import json
import base64
import numpy as np
from django.core.paginator import Paginator
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from irie.apps.events.models import EventRecord
from irie.apps.site.view_utils import raise404
from irie.apps.inventory.models import Asset
from .filters import AssetFilter
# Predictors
from irie.apps.prediction.runners.hazus import hazus_fragility
from irie.apps.prediction.runners.ssid import make_mountains, ssid_stats, ssid_event_plot


@login_required(login_url="/login/")
def fetch_rendering(request):
    asset_id = request.GET.get('asset')
    asset = Asset.objects.get(id=asset_id)

    if asset.cesmd == "CE58658":
        template = loader.get_template(f"bridges/InteractiveTwin-{asset.cesmd}.html")
        return HttpResponse(template.render({}, request))


    from irie.apps.prediction.models import PredictorModel
    for p in PredictorModel.objects.filter(asset=asset):
        if p.protocol == "IRIE_PREDICTOR_T4":
            return HttpResponse("html")

    return HttpResponse("No rendering available for this asset.")



@login_required(login_url="/login/")
def asset_event_summary(request, cesmd, event):
    from irie.apps.evaluation.models import Evaluation

    context = {}
    context["segment"] = "events"
    html_template = loader.get_template("inventory/asset-event-summary.html")

    try:
        segments = request.path.split("/")
        _, _, is_nce = segments[-3:]

        try:
            evaluation = Evaluation.objects.filter(event_id=int(event))[0]
            evaluation_data = evaluation.evaluation_data

        except Exception as e:
            # TODO: Handle case where evaluation cant be found
            evaluation_data = {}
            evaluation = None

        for metric in evaluation_data.values():
            metric["completion"] = (
                100 * len(metric["summary"])/len(metric["predictors"])
            )

        if "SPECTRAL_SHIFT_IDENTIFICATION" in evaluation_data:
            context["freq_plot_json"] = \
                    ssid_event_plot(evaluation_data["SPECTRAL_SHIFT_IDENTIFICATION"])

        context["all_evaluations"] = evaluation_data

        context["evaluation_details"] = { 
                 metric.replace("_", " ").title(): {
                    key:  [list(map(lambda i: f"{i:.3}" if isinstance(i,float) else str(i), row)) for row in table]
                    for key, table in predictors["details"].items()
                 } 
            for metric, predictors in sorted(evaluation_data.items(), key=lambda i: i[0])
        }
        context["asset"]       = evaluation and evaluation.event.asset or None
        context["nce_version"] = is_nce
        context["event_data"]  = EventRecord.objects.get(pk=int(event)).motion_data


        resp = html_template.render(context, request)

        return HttpResponse(resp)

    except Exception as e:
        if "DEBUG" in os.environ and os.environ["DEBUG"]:
            raise e
        html_template = loader.get_template("site/page-500.html")
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def dashboard(request):
    from irie.apps.inventory.models import Asset
    from irie.apps.evaluation.models import Evaluation

    context = {}
    context["segment"] = "dashboard"
    try:
        if "demo" in request.path:
            context["demo_version"] = True

        context["recent_evaluations"] = [
            (evaluation, EventRecord.objects.get(pk=evaluation.event_id))
            for evaluation in reversed(list(Evaluation.objects.all())[-6:])
        ]
        assets = list(set(
            Asset.objects.get(cesmd=event[1].cesmd) for event in context["recent_evaluations"]
        ))
        colors = {
            asset.id: max(event[1].pga for event in context["recent_evaluations"] if event[1].cesmd == asset.cesmd)
            for asset in assets
        }
        
        context["asset_map"] = AssetMap(assets, colors=colors, color_name="Peak Station Accel.").get_html()
        context["calid"] = {b.cesmd: b.calid for b in assets}

        html_template = loader.get_template("inventory/dashboard.html")
        return HttpResponse(html_template.render(context, request))

    except Exception as e:
        if "DEBUG" in os.environ and os.environ["DEBUG"]:
            raise e
        html_template = loader.get_template("site/page-500.html")
        return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/")
def asset_event_report(request):
    from irie.apps.evaluation.models import Evaluation

    context = {}
    context["segment"] = "events"
    html_template = loader.get_template("inventory/report.tex")

    events = [
        EventRecord.objects.get(pk=evaluation.event_id)
        for evaluation in reversed(list(Evaluation.objects.all())[-6:])
    ]
    assets = list(set(
        Asset.objects.get(cesmd=event.cesmd) for event in events
    ))
    context["events"] = events
    context["assets"] = assets 

    context["mountains"] = []

    if request.method == 'POST' and request.FILES.get('map_image'):
        context["map"] = base64.b64encode(request.FILES['map_image'].read()).decode("utf-8")

    for event in events:
        context["mountains"].append(make_mountains(event.asset))

    resp = html_template.render(context, request)

    return HttpResponse(resp)



@login_required(login_url="/login/")
def asset_profile(request, calid):

    context = {}
    html_template = loader.get_template("inventory/asset-profile.html")
    context["segment"] = "assets"

    context["nce_version"] = True

    try:
        asset = Asset.objects.get(calid=calid)

    except Asset.DoesNotExist:
        return raise404(request, context)

    context["asset"] = asset

    # Compute Hazus fragility probabilities and curve
    try:
        hazus_results = hazus_fragility(asset.nbi_data, generate_plot=False, return_data=True)

        # Add fragility probabilities and plot to the context
        context["hazus"] = {
            "probabilities": {
                "Slight": hazus_results.get("Slight"),
                "Moderate": hazus_results.get("Moderate"),
                "Extensive": hazus_results.get("Extensive"),
                "Complete": hazus_results.get("Complete"),
            },
            "sa_range": json.dumps(hazus_results["sa_range"]),
            "curves":   json.dumps(hazus_results["curves"])
            # "plot_base64": hazus_results.get("plot_base64"),
        }
    except: 
        pass 

    try:
        context["mountains"] = make_mountains(asset)
    except:
        pass

    context["tables"] = _make_tables(asset)

    if asset.cesmd:
        cesmd = asset.cesmd

        events = list(reversed(sorted(EventRecord.objects.filter(cesmd=cesmd),
                                      key=lambda x: x.motion_data["event_date"])))

        evals = [
            {"event": event,
             "pga": event.pga, #abs(event.motion_data["peak_accel"])/980., 
             "evaluation": ssid,
            }
            for i, (event, ssid) in enumerate(zip(events, ssid_stats(events, "period")))
        ]
        context["evaluations"] = Paginator(evals, 5).get_page(1)

    try:
        return HttpResponse(html_template.render(context, request))

    except Exception as e:
        if "DEBUG" in os.environ and os.environ["DEBUG"]:
            raise e
        html_template = loader.get_template("site/page-500.html")
        return HttpResponse(html_template.render(context, request))

def _make_tables(asset):
    if asset.cesmd and isinstance(asset.cgs_data, list):
        tables = [
            {k: v for k,v in group.items()
                if k not in {
                    "Remarks",
                    "Instrumentation",
                    "Remarks/Notes",
                    "Construction Date"
                }
            } for group in asset.cgs_data[1:]
        ]
    else:
        tables = []

    # Filter out un-interesting information
    nbi_data = [
      {k: v for k,v in group.items() 
           if k not in {
               "Owner Agency",
               "Year Reconstructed",
               "Bridge Posting Code",
               "Latitude",
               "Longitude",
               "NBIS Minimum Bridge Length",
               "Record Type",
               "State Name",
               "U.S. Congressional District",
               "Inventory Route NHS Code"
           }
       } for group in asset.nbi_data.values()
    ]
    tables.extend(nbi_data)
    tables = [tables[2], *tables[:2], *tables[3:]]
    condition = {}
    for table in tables:
        keys = set()
        for k in table:
            key = k.lower()
            if "condition" in key \
            or "rating" in key \
            or (re.search("^ *[0-9] - [A-Z]", table[k]) is not None and "code" not in key):
                condition[k] = table[k]
                keys.add(k)

        for k in keys:
            del table[k]

    tables.insert(3,condition)

    # for some tables, all values are empty. Filter these out
    tables = [
        table for table in tables if sum(map(lambda i: len(i),table.values()))
    ]
    return tables



@login_required(login_url="/login/")
def asset_table(request):
    """
    Returns a table of all assets in the database, paginated
    """

    context = {}
    context["segment"] = "assets"

    page = request.GET.get("page", 1)
    try:
        page = int(page)
    except:
        page = 1

    filter_set = AssetFilter(request.GET, queryset=Asset.objects.all())
    assets = filter_set.qs
    context["bridges"]   = Paginator(assets, 10).get_page(page)
    context["asset_map"] = AssetMap(assets=assets).get_html()
    context["filter"] = filter_set


    # Copy the GET parameters and remove the 'page' parameter
    query_params = request.GET.copy()
    query_params.pop('page', None)  # Remove 'page' parameter if it exists
    context["query_string"] = query_params.urlencode()


    html_template = loader.get_template("inventory/asset-table.html")
    try:
        return HttpResponse(html_template.render(context, request))

    except Exception as e:
        if "DEBUG" in os.environ and os.environ["DEBUG"]:
            raise e
        html_template = loader.get_template("site/page-500.html")
        return HttpResponse(html_template.render(context, request))



import folium

class AssetMap:
    def __init__(self, assets, name=None, colors=None, color_name=None):
        if name is None:
            name = "Assets"

        if colors is not None:
            cm = folium.branca.colormap.LinearColormap(colors=["green", "yellow", "orange", "red"], 
                                                       vmin=0, vmax=max(colors.values()),
                                                       caption=color_name)
            colors = {
                k: cm.rgb_hex_str(v) for k,v in colors.items()
            }
        else:
            cm = None 

        markers = self.add_bridges(assets, colors=colors)

        if len(markers) > 0:
            location = sum(np.array(m.location) for m in markers) / len(markers)
        else:
            location = [37.7735, -122.0993] # (self._preferences.latitude, self._preferences.longitude)

        # self._figure = figure = folium.Figure()
        self._map    = m      = folium.Map(
            location=location, 
            zoom_start=6, 
            tiles='cartodbpositron'
        )

        if cm is not None:
            cm.add_to(m)

        for marker in markers:
            marker.add_to(m)


        # CESMD
        # Partial
        # Full


    def get_html(self, **kwargs):
        return self._map._repr_html_()

    def add_bridges(self, assets, colors=None):
        if colors is None:
            colors = {}

        markers = []
        for b in assets:
            lat, lon = b.coordinates
            popup = folium.Popup(
                        folium.Html(
                            '<a style="display: inline;" target="_blank" href="/inventory/{calid}/">{label}</a>'.format(
                                calid=b.calid,
                                label=b.calid
                            ), 
                            script=True
                        ),
                        min_width= 50,
                        max_width=100
            )
            if b.is_complete:
                markers.append(folium.Marker(
                    location=[lat, lon],
                    popup=popup,
                    icon=folium.Icon(icon="cloud", color="blue" if not b.is_complete else "beige"),
                    z_index_offset=1000
                ))
            else:
                markers.append(folium.CircleMarker(
                    location=[lat, lon],
                    popup=popup,
                    color="black",
                    fill_color=colors.get(b.id, "gray"),
                    fill=True,
                    opacity=1,
                    fill_opacity=1,
                    radius=4,
                    weight=1,
                    z_index_offset=800
                ))
        return markers
