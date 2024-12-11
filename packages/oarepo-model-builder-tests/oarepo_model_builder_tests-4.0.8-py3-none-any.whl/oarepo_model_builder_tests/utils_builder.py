from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class TestUtilsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "test_utils"
    template = "test_utils"

    def _get_output_module(self):
        return f'{self.current_model.definition["tests"]["module"]}.utils'
