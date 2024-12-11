from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class ConftestBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_tests_conftest"
    template = "conftest"

    def _get_output_module(self):
        return f'{self.current_model.definition["tests"]["module"]}.conftest'
