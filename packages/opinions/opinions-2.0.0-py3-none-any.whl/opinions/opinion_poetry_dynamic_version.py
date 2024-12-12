from opinions import Opinion


class PoetryDynamicVersionOpinion(Opinion):
    def apply_changes(self):
        if not self.is_poetry_project:
            return

        build_system = self.project.pyproject.get_or_create_table("build-system", is_super=True)
        build_system["requires"] = ["poetry-core>=1.0.0", "poetry-dynamic-versioning>=1.0.0,<2.0.0"]
        build_system["build-backend"] = "poetry_dynamic_versioning.backend"

        tool_dynamic_version = self.project.pyproject.get_or_create_table(
            "tool", "poetry-dynamic-versioning", is_super=True
        )
        tool_dynamic_version["enable"] = True

        tool_poetry = self.project.pyproject.get_or_create_table("tool", "poetry", is_super=True)
        tool_poetry["version"] = "0.0.0"
