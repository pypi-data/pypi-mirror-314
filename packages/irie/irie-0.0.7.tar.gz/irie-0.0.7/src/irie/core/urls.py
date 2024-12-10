#===----------------------------------------------------------------------===#
#
#         STAIRLab -- STructural Artificial Intelligence Laboratory
#
#===----------------------------------------------------------------------===#
#
#   Fall 2022
#
#----------------------------------------------------------------------------#
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "IRiE"
admin.site.index_title = "IRiE"
admin.site.site_title  = "IRiE"

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication routes
    path("", include("irie.apps.authentication.urls")),

    # Application routes
    path("", include("irie.apps.events.urls")),

    path("", include("irie.apps.evaluation.urls")),

    path("", include("irie.apps.prediction.urls")),

    path("", include("irie.apps.inventory.urls")),

#   path("", include("irie.apps.recovery.urls")),

    path("", include("irie.apps.documents.urls")),

    # Leave `site.urls` as last the last line
    path("", include("irie.apps.site.urls"))


# Ensure we can serve files stored with models (eg, bridge renderings)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

