from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class TestResourceBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_tests_resource"
    template = "test_resource"

    def finish(self, **extra_kwargs):
        tests = getattr(self.current_model, "section_tests")
        super().finish(
            fixtures=tests.fixtures, test_constants=tests.constants, **extra_kwargs
        )

    def _get_output_module(self):
        return f'{self.current_model.definition["tests"]["module"]}.test_resource'
