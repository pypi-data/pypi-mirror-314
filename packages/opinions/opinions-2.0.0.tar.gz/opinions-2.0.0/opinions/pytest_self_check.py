import pytest

from .cli import prep_project


def pytest_collect_file(parent, file_path):
    if file_path.name == "pyproject.toml":
        return PyprojectFile.from_parent(parent, path=file_path)


class PyprojectFile(pytest.File):
    def collect(self):
        yield PyprojectItem.from_parent(self, name="opinions-check")


class PyprojectItem(pytest.Item):
    def runtest(self):
        project = prep_project()
        if project.is_dirty:
            raise ValueError("Project needs to be reconfigured")

    def repr_failure(self, excinfo):
        if isinstance(excinfo.value, ValueError):
            return "\n".join(
                [
                    "Project needs to be reconfigured",
                    "Run 'opinions apply' to fix",
                ]
            )
