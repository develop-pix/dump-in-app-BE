import logging

from django.urls import path

logger = logging.getLogger("configuration")


def show_swagger(*args, **kwargs) -> bool:
    from config.settings.swagger.settings import SWAGGER_ENABLED

    if not SWAGGER_ENABLED:
        return False

    try:
        import drf_yasg  # noqa
    except ImportError:
        logger.info("No installation found for: drf_yasg")
        return False

    return True


class SwaggerSetup:
    @staticmethod
    def do_settings(INSTALLED_APPS):
        _show_swagger: bool = show_swagger()
        logger.info(f"Django Swagger in use: {show_swagger}")

        if not _show_swagger:
            return INSTALLED_APPS

        INSTALLED_APPS += ["drf_yasg"]

        return INSTALLED_APPS

    @staticmethod
    def do_urls(urlpatterns):
        if not show_swagger():
            return urlpatterns

        from drf_yasg import openapi
        from drf_yasg.views import get_schema_view
        from rest_framework.permissions import AllowAny

        # from config.settings.swagger.generators import WebAPISchemeGenerator, AdminAPISchemeGenerator

        web_chema_view = get_schema_view(
            openapi.Info(
                title="Web API",
                default_version="v1",
                description="",
                terms_of_service="",
                contact=openapi.Contact(email=""),
                license=openapi.License(name=""),
            ),
            public=True,
            permission_classes=(AllowAny,),
            # urlconf="apps.api.v1.urls",
            # generator_class=WebAPISchemeGenerator,
        )

        admin_schema_view = get_schema_view(
            openapi.Info(
                title="Admin API",
                default_version="v1",
                description="",
                terms_of_service="",
                contact=openapi.Contact(email=""),
                license=openapi.License(name=""),
            ),
            public=True,
            permission_classes=(AllowAny,),
            # urlconf="apps.api.admin.urls",
            # generator_class=AdminAPISchemeGenerator,
        )

        return urlpatterns + [
            path("swagger/web/docs", web_chema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
            path("swagger/web/redoc", web_chema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
            path(
                "swagger/admin/docs",
                admin_schema_view.with_ui("swagger", cache_timeout=0),
                name="schema-swagger-admin-ui",
            ),
            path("swagger/admin/redoc", admin_schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc-admin"),
        ]
