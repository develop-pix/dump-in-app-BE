from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    # Admin
    path("app/admin/", admin.site.urls),
    # API
    path("app/api/auth", include(("dump_in.authentication.urls", "api-auth"))),
    path("app/api/users", include(("dump_in.users.urls", "api-users"))),
    path("app/api/reviews", include(("dump_in.reviews.urls", "api-reviews"))),
    path("app/api/photo-booths", include(("dump_in.photo_booths.urls", "api-photo-booths"))),
    path("app/api/events", include(("dump_in.events.urls", "api-events"))),
]

from config.settings.debug_toolbar.setup import DebugToolbarSetup  # noqa
from config.settings.swagger.setup import SwaggerSetup  # noqa

urlpatterns = DebugToolbarSetup.do_urls(urlpatterns)
urlpatterns = SwaggerSetup.do_urls(urlpatterns)

# Static/Media File Root (CSS, JavaScript, Images)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
