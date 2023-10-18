# class WebAPISchemeGenerator(OpenAPISchemaGenerator):
#     def get_schema(self, request=None, public=False):
#         schema = super().get_schema(request, public)
#         schema.base_path = "/api/v1/"
#         return schema


# class AdminAPISchemeGenerator(OpenAPISchemaGenerator):
#     def get_schema(self, request=None, public=False):
#         schema = super().get_schema(request, public)
#         schema.base_path = "/admin-api/"
#         return schema
