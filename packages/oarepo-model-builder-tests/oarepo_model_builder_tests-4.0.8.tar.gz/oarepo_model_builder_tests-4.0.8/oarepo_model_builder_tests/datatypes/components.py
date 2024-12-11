import marshmallow as ma
from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.datatypes.components.model.utils import set_default

# todo
"""
tests running in separate profile *after* generation
ask about links
hardcoding profile names for identifying services?
ui and entrypoints for draft files
"""


class TestSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    extra_fixtures = ma.fields.List(
        ma.fields.String(),
        data_key="extra-fixtures",
        attribute="extra-fixtures",
        required=False,
        load_default=[],
    )

    extra_code = ma.fields.String(
        data_key="extra-code", attribute="extra-code", load_default=""
    )

    module = ma.fields.String(load_default="tests")

    disabled = ma.fields.List(ma.fields.String())


class ModelTestComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]

    class ModelSchema(ma.Schema):
        tests = ma.fields.Nested(TestSchema, load_default=lambda: TestSchema().load({}))

    def before_model_prepare(self, datatype, *, context, **kwargs):
        tests = set_default(datatype, "tests", {})
        tests.setdefault(
            "module",
            "tests",
        )

    def process_tests(self, datatype, section, **extra_kwargs):
        section.fixtures = {
            "record_service": "record_service",
            "sample_record": "sample_record",
        }

        section.constants = {
            "read_url": "",
            "update_url": "",
            "delete_url": "",
            "deleted_http_code": 410,
            "skip_search_test": False,
            "service_read_method": "read",
            "service_create_method": "create",
            "service_delete_method": "delete",
            "service_update_method": "update",
            "deleted_record_pid_error": "PIDDeletedError",
            "links": {
                "self": "https://{site_hostname}/api{base_urls['base_url']}{pid_value}",
            },
        }


components = [ModelTestComponent]
