from opinions import Opinion


class UsePEP517BuildOpinion(Opinion):
    def apply_changes(self):
        tool_poe_tasks = self.project.pyproject.get_or_create_table("tool", "poe", "tasks", is_super=True)
        tool_poe_tasks["build"] = "python -m build"
