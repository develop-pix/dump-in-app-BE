from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    # Admin
    path("app/admin/", admin.site.urls),
    # API
    path("app/api/auth/", include(("dump_in.authentication.urls", "api-auth"))),
    path("app/api/users/", include(("dump_in.users.urls", "api-users"))),
    path("app/api/images/", include(("dump_in.images.urls", "api-images"))),
]

from config.settings.debug_toolbar.setup import DebugToolbarSetup  # noqa
from config.settings.swagger.setup import SwaggerSetup  # noqa

urlpatterns = DebugToolbarSetup.do_urls(urlpatterns)
urlpatterns = SwaggerSetup.do_urls(urlpatterns)

# Static/Media File Root (CSS, JavaScript, Images)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
