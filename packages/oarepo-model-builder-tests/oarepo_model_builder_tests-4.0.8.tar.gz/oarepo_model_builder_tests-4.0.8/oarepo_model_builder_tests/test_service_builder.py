from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class TestServiceBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_tests_service"
    template = "test_service"

    def finish(self, **extra_kwargs):
        tests = getattr(self.current_model, "section_tests")
        super().finish(
            fixtures=tests.fixtures, test_constants=tests.constants, **extra_kwargs
        )

    def _get_output_module(self):
        return f'{self.current_model.definition["tests"]["module"]}.test_service'
