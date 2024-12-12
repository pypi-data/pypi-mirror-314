from . import Opinion

TEST_FILES = "tests/**/*.py"


class RuffOpinion(Opinion):
    def apply_changes(self):
        ruff_tool = self.project.pyproject.get_or_create_table("tool", "ruff", is_super=True)
        ruff_tool["line-length"] = 120

        if "select" not in ruff_tool:
            ruff_tool["select"] = []

        for lint_rule in [
            "E4",
            "E7",
            "E9",
            "F",
            "UP",
            "S",
            "A",
            "I",
        ]:
            if lint_rule not in ruff_tool["select"]:
                ruff_tool["select"].append(lint_rule)

        self.project.pyproject.add_pytest_opt("--ruff")
        self.project.pyproject.add_pytest_opt("--ruff-format")

        ruff_per_file = self.project.pyproject.get_or_create_table("tool", "ruff", "per-file-ignores", is_super=True)
        if TEST_FILES not in ruff_per_file:
            ruff_per_file[TEST_FILES] = []

        for test_exclude_lint_rule in [
            "S101",
        ]:
            if test_exclude_lint_rule not in ruff_per_file[TEST_FILES]:
                ruff_per_file[TEST_FILES].append(test_exclude_lint_rule)
