from pathlib import Path
import json
import io 
import base64
import numpy as np
# Ensure Agg backend is set for non-interactive plotting
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt, ticker, cm
import quakeio
from mdof import transform
from scipy.signal import find_peaks
from mdof.utilities import Config, extract_channels
from matplotlib import colormaps
# try:
#     import scienceplots
#     plt.style.use(["science"])
# except ImportError:
#     pass

N_PEAKS = 5 # number of "significant" peaks per record
MISSING_CHANNEL_LIMIT = 3 # number of missing output channels allowed before skipping event
MAX_ACCEL = 3.0

from irie.apps.events.models import EventRecord



def ssid_stats(events, key):
    """
    mode_results is a list (station level) of lists (event level) of dictionaries (mode level).
    mode_results = [
        [
            {
                "period": ..., 
                "frequency": ...,
                "damping": ...,
                "emac": ...,
                "mpc": ...,
            },
            ...
        ],
        ...
    ]

    [
       # "Event"
       {"S1": {"period": [0.1]},
        "R1": {"period": [1.2]}}
    ]
    """
    mode_results = [_find_ssid(event.id) for event in events]
    import numpy as np

    filtered_results = [
            {
              method: [
                  result for result in event_results[method]
                        if key in result and result.get("emac", 1.0) > 0.5 and result.get("mpc", 1.0) > 0.5
              ] for method in event_results
            } for event_results in mode_results
    ]

    from collections import defaultdict
    values = defaultdict(list)
    for event in filtered_results:
        for method in event:
            for result in event[method]:
                values[method].append(result[key])

    mean = {method: np.mean(values[method]) for method in values}
    std =  {method: np.std(values[method]) for method in values}

    def _first(method_results):
        if method_results and len(method_results) > 0:
            results = np.array([result[key] for result in method_results])
            try:
                idx = np.argmax([result["amplitude"] for result in method_results])
                return results[idx]
            except KeyError:
                return np.max(results)
        else: 
            return {}

    return [
        {method: {
#           "distance": (closest_item[key]-mean)/std),
            "nearest_mean": event_results[method][np.argmin(np.abs(mean[method] \
                            - [result[key] for result in event_results[method]]))] \
                if event_results[method] and len(event_results[method]) > 0 else {} ,
            "maximum": _first(event_results[method])
            }
            for method in event_results
        }
        for event_results in filtered_results
    ]


def _find_ssid(event_id=None, evaluation=None):
    """
    Given an event ID, finds the results of the first configured
    system ID run. This generally looks like a list of dicts,
    each with fields "frequency", "damping", etc.
    """
    from irie.apps.evaluation.models import Evaluation

    if evaluation is None:
        evaluation = Evaluation.objects.filter(event_id=int(event_id))

    elif not isinstance(evaluation, list):
        evaluation = [evaluation]


    if len(evaluation) != 1:
        return []

    else:
        evaluation_data = evaluation[0].evaluation_data

    if "SPECTRAL_SHIFT_IDENTIFICATION" in evaluation_data:
        return {
                key: val.get("data", val.get("error", [])) 
                    for key,val in evaluation_data["SPECTRAL_SHIFT_IDENTIFICATION"]["summary"].items()
        }

    else:
        return []


def ssid_event_plot(evaluation):
    import numpy as np
    from mdof.macro import FrequencyContent

    plot = FrequencyContent(scale=True, period=True, xlabel="Period (s)", ylabel="Normalized Amplitude")

    for name, mdata in evaluation["summary"].items():
        periods = []
        amplitudes = []
        for i in mdata.get("data", []):
            if "period" in i:
                periods.append(i["period"])
                if "amplitude" in i:
                    amplitudes.append(i["amplitude"])

        if len(amplitudes) and (len(amplitudes) == len(periods)):
            plot.add(np.array(periods), np.array(amplitudes), label=name)
        else:
            plot.add(np.array(periods), label=name)

    fig = plot.get_figure()
    return fig.to_json()
 

def _load_events(asset, output_channels):
    """
    Parse event file and restructure the relevant data
    (filename, date, peak acceleration, acceleration response history, and timestep).
    
    Return a dictionary:
    {
      filename:
      {
        'date': date,
        'peak_accel': peak_accel,
        'outputs': outputs,
        'dt': dt
      }
    }
    """
    events = {}
    for evt in EventRecord.objects.filter(asset=asset):

        try:
            event = quakeio.read(evt.event_file.path, format="csmip.zip", exclusions=["*filter*"])
            outputs, dt = extract_channels(event, output_channels)
        except Exception as e:
            print(f"Error loading event: {e}")
            continue

        filename = event['file_name']
        date = event['event_date']
        peak_accel = np.abs(event['peak_accel'])/980.665
        events[filename] = {'date': date, 'peak_accel': peak_accel, 'outputs': outputs, 'dt': dt}

    events = sorted(events.items(), key=lambda k: np.abs(k[1]["peak_accel"]))
    return {k:v for k,v in events}


def get_spectra(event, period_band, cmap):
    """
    Get coordinates (periods, amplitudes) of spectra for an event, and return them along
    with the maximum period of the N_PEAKS tallest peaks, as well as plotting options
    such as color and alpha.
    """
    n_outputs = event['outputs'].shape[0]
    frequencies,_,S = transform.fdd(outputs=event['outputs'], step=event['dt']) # Full frequency spectrum
    periods = 1/frequencies
    period_mask = (periods>=period_band[0]) & (periods<=period_band[1])
    periods = periods[period_mask]
    n_periods = len(periods)   # Number of periods, x axis of spectrum.  Varies per record.    
    spec_coords = np.empty((n_outputs, 3, n_periods))  # Initialize empty array for coordinates.
    xvalue = event['peak_accel']
    for j in range(n_outputs):
        amplitudes = S[j,:]
        amplitudes = amplitudes/max(amplitudes)
        amplitudes = amplitudes[period_mask]
        spec_coords[j] = [[xvalue]*n_periods, periods, amplitudes]  # All spectra from FDD.  One spectrum for each n_outputs outputs
        peak_indices, _ = find_peaks(amplitudes, prominence=max(amplitudes)*0.01)
        peaks = sorted(peak_indices, key=lambda peak: amplitudes[peak], reverse=True)
        max_peak_period = np.max(periods[peaks[:N_PEAKS]])
    plot_conf = Config()
    plot_conf.color = cmap(event['peak_accel']/MAX_ACCEL)
    plot_conf.alpha = 1

    return {
        'spec_coords': spec_coords, 
        'max_peak_period': max_peak_period, 
        'plot_conf': plot_conf
    }


def _plot_3d_spectrum(ax, date, trace, num_spectra=1, label='date', line=True, plotter='matplotlib', **options):
    color = options.get('color', None)
    alpha = options.get('alpha', 0.5)
    if label=='date':
        label = date
    if plotter == 'matplotlib':
        for i in range(num_spectra):
            if line:
                ax.plot(trace[i,0,:],trace[i,1,:],trace[i,2,:], label=label,
                        linestyle='-', color=color, alpha=alpha)
            else:
                ax.scatter(trace[i,0,:],trace[i,1,:],trace[i,2,:], label=label,
                        marker=options.get('marker','o'), color=color, s=30, alpha=alpha)


def _linear_interpolate(x, y, target_x):
    sorted_indices = sorted(range(len(x)), key = lambda i: x[i])
    x = x[sorted_indices]
    y = y[sorted_indices]
    i1 = max(np.where(x<=target_x)[0])
    i2 = min(np.where(x>=target_x)[0])
    x1 = x[i1]
    x2 = x[i2]
    y1 = y[i1]
    y2 = y[i2]
    target_y = y1 + (target_x - x1)*(y2 - y1)/(x2 - x1)    
    return target_y


def plot_spectral_surface(ax, traces, **options):
    alpha = options.get('alpha',0.5)
    colors = options.get('colors',None)
    cmap = options.get('cmap',None)
    n_points_per_trace = 2000
    period_lower_bound = np.max([trace[0,1,-1] for trace in traces])
    period_upper_bound = np.min([trace[0,1,0] for trace in traces])
    standard_periods = np.linspace(period_lower_bound+0.01, period_upper_bound-0.01, n_points_per_trace)
    X = []
    Y = []
    Z = []
    for trace in traces:
        X.append(np.full(n_points_per_trace,trace[0,0,0]))
        Y.append(standard_periods)
        current_periods = trace[0,1,:]
        current_amplitudes = trace[0,2,:]
        z = []
        for period in standard_periods:
            z.append(_linear_interpolate(current_periods,current_amplitudes,period))
        Z.append(z)
    X = np.array(X)
    Y = np.array(Y)
    Z = np.array(Z)
    if colors is None:
        if cmap is None:
            cmap = cm.plasma
        ax.plot_surface(X,Y,Z, cmap=cmap, alpha=alpha)
    else:
        ax.plot_surface(X,Y,X, facecolors=colors)


def _plot_mountains(spectra, accellim=None):
    fig = plt.figure(figsize=(13,13))
    ax = fig.add_subplot(projection='3d')

    max_period = 1.1*np.max([event['max_peak_period'] for event in spectra.values()])

    for event in spectra:
        periods = spectra[event]['spec_coords'][0,1,:]
        spec_coords = spectra[event]['spec_coords'][:,:,(periods<=max_period)]
        _plot_3d_spectrum(ax=ax, date="", # TODO events[event]['date'], 
                          trace=spec_coords, 
                          label=None, **(spectra[event]['plot_conf']))


    ax.tick_params(axis='x', which='major', pad=15)
    ax.tick_params(axis='y', which='major', pad=15)
    for tick in ax.xaxis.get_majorticklabels():
        tick.set_verticalalignment("bottom")
    ax.xaxis.set_minor_locator(ticker.NullLocator())
    if accellim is not None: 
        ax.set_xlim((0,accellim))
    ax.view_init(elev=30, azim=-20, roll=2)
    ax.set_box_aspect((5,5,1), zoom=0.75)
    ax.set_xlabel("Peak Station Acceleration (g)", labelpad=30)
    ax.set_ylabel("Period (s)", labelpad=40)
    ax.set_zlabel("Normalized spectral amplitude", labelpad=10)
    # ax.legend(frameon=True, framealpha=0.9, bbox_to_anchor=(0.5,0,0.5,0.7), loc='upper left')
    return fig


def make_mountains(asset, output_channels=None):

    cmap = colormaps['plasma']
    conf = Config()
    conf.period_band = (0.1,3)
    conf.damping = 0.02
    conf.ss_decimation = 8
    conf.order = 40

    if output_channels is None:
        if not asset.bridge_sensors:
            raise ValueError("Failed to determine output sensors for Asset")
        output_channels = json.loads(asset.bridge_sensors[2:-1])

    n_expected_outputs = len(output_channels)
    events = _load_events(asset, output_channels)

    spectra = {} # dictionary to store the spectra at each event
    for filename,event in events.items():
        n_parsed_channels = event['outputs'].shape[0]
        if n_parsed_channels < n_expected_outputs-MISSING_CHANNEL_LIMIT:
            print(f"Missing {n_expected_outputs-n_parsed_channels} output channels; skipping event") # Missing too many channels
            continue

        spectra[filename] = get_spectra(event, conf.period_band, cmap) # {'spec_coords':spec_coords, 'max_peak_period':max_peak_period, 'plot_conf':plot_conf}


    # if station == 'CE89494':
    #     max_period = 2.5
    # if station == 'CE89973':
    #     accellim = 2.5
    if len(spectra) == 0:
        return None 

    fig = _plot_mountains(spectra)

    # Save the plot to a BytesIO buffer
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    # plt.show()

    # Encode the image as Base64
    return base64.b64encode(buffer.read()).decode("utf-8")

def parse_args(args):
    procedure = {
        'STATION_TYPE': None,
        'station': None,
        'indir':   None,
        'outdir':  "./out",
        'accellim': None
    }
    argi = iter(args[1:])
    for arg in argi:
        if arg in ['--help', '-h']:
            print(HELP)
            sys.exit()
        elif arg == '--station':
            procedure['station'] = next(argi)
        elif arg == '--indir':
            procedure['indir'] = next(argi)
        elif arg == '--outdir':
            procedure['outdir'] = next(argi)
        elif arg == '--accellim':
            procedure['accellim'] = float(next(argi))
        else:
            procedure['STATION_TYPE'] = arg
    if procedure['STATION_TYPE'] is None:
        print("Station type ('bridges' or 'buildings') is a required argument.")
        sys.exit()
    return procedure


if __name__ == '__main__':

    import sys
    procedure = parse_args(sys.argv)
    STATION_TYPE = procedure['STATION_TYPE']
    outdir = Path(procedure['outdir'])
    if not outdir.exists():
        outdir.mkdir()

    conf = Config()
    conf.period_band = (0.1,3) if STATION_TYPE=="bridges" else (0.1,8)
    if procedure['accellim'] is None:
        accellim = 1.5 if STATION_TYPE=="bridges" else 1.2
    else:
        accellim = procedure['accellim']
    conf.damping = 0.02
    conf.ss_decimation = 8
    conf.order = 40
    # cmap = colormaps['seismic']
    cmap = colormaps['plasma']
    path_to_channels = f"../channels_{STATION_TYPE}/channels_summary.json"
    with open(path_to_channels, 'r') as readfile:
        CHANNELS = json.load(readfile)

    if procedure['station'] is not None:
        CHANNELS = {k:v for k,v in CHANNELS.items() if k==procedure['station']}

    for station in CHANNELS:
        make_mountains(station)
