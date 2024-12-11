from oarepo_model_builder.builders import OutputBuilder
from oarepo_model_builder.outputs.cfg import CFGOutput


class OarepoModelBuilderSetupCfgBuilder(OutputBuilder):
    TYPE = "oarepo_model_builder_setup_cfg"

    TEST_DEPENDENCIES = [
        ("pytest-invenio", ">=1.4.11"),
    ]

    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")

        for package, version in self.TEST_DEPENDENCIES:
            output.add_dependency(
                package, version, group="options.extras_require", section="tests"
            )
