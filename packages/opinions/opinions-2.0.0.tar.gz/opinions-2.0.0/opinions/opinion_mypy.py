from . import Opinion


class MypyOpinion(Opinion):
    def apply_changes(self):
        self.project.pyproject.add_pytest_opt("--mypy")
