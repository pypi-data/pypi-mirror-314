import json
from pathlib import Path
from typing import Any, Optional

import tomlkit
from tomlkit.container import Container
from tomlkit.items import Item


class TOMLFile:
    def __init__(self, path: Path):
        self.path = Path(path)
        self._content: Optional[tomlkit.TOMLDocument] = None
        self._dirty = False
        self._initial_content: Optional[str] = None

    @property
    def is_dirty(self) -> bool:
        return self._dirty or (
            self._content is not None
            and self._initial_content is not None
            and tomlkit.dumps(self._content) != self._initial_content
        )

    @property
    def content(self) -> tomlkit.TOMLDocument:
        if self._content is None:
            if self.path.exists():
                with open(self.path) as f:
                    self._content = tomlkit.load(f)
                    self._initial_content = tomlkit.dumps(self._content)
            else:
                self._content = tomlkit.document()
                self._initial_content = ""
        return self._content

    def finalize(self) -> bool:
        wrote_out = False
        if self.is_dirty:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.path, "w") as f:
                tomlkit.dump(self.content, f)
            wrote_out = True
        return wrote_out

    def mark_dirty(self):
        self._dirty = True

    def get_or_create_table(self, *path: str, is_super=False) -> tomlkit.TOMLDocument | Item | Container | Any:
        table: Any = self.content
        for path_fragment in path:
            if path_fragment not in table:
                table[path_fragment] = tomlkit.table(is_super_table=is_super)
            table = table[path_fragment]
        return table


class PyProjectTOMLFile(TOMLFile):
    def add_pytest_opt(self, option):
        pytest_iniopts = self.get_or_create_table("tool", "pytest", "ini_options", is_super=True)
        if "addopts" not in pytest_iniopts:
            pytest_iniopts["addopts"] = ""

        if option not in pytest_iniopts["addopts"].split(" "):
            pytest_iniopts["addopts"] += " " + option
            pytest_iniopts["addopts"] = pytest_iniopts["addopts"].strip()


class JsonFile:
    def __init__(self, path: Path):
        self.path = Path(path)
        self._content: Optional[Any] = None
        self._dirty = False
        self._initial_content: Optional[str] = None

    @property
    def is_dirty(self) -> bool:
        return self._dirty or (
            self._content is not None
            and self._initial_content is not None
            and json.dumps(self._content) != self._initial_content
        )

    @property
    def content(self) -> Any:
        if self._content is None:
            if self.path.exists():
                with open(self.path) as f:
                    self._content = json.load(f)
                    self._initial_content = json.dumps(self._content)
            else:
                self._content = {}
                self._initial_content = ""
        return self._content

    def finalize(self) -> bool:
        wrote_out = False
        if self.is_dirty:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.path, "w") as f:
                json.dump(self.content, f, indent=4)
            wrote_out = True
        return wrote_out

    def mark_dirty(self):
        self._dirty = True


class OpinionatedProject:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self._toml_files: dict[str, TOMLFile] = {}
        self._json_files: dict[str, JsonFile] = {}

        from opinions.opinion_mypy import MypyOpinion
        from opinions.opinion_pep517 import UsePEP517BuildOpinion
        from opinions.opinion_poetry_dynamic_version import PoetryDynamicVersionOpinion
        from opinions.opinion_poetry_sources import PoetryExplicitSourcesOpinion
        from opinions.opinion_ruff import RuffOpinion
        from opinions.opinion_ruff_vscode import RuffVSCodeOpinion

        self.opinions = [
            RuffOpinion(self),
            MypyOpinion(self),
            RuffVSCodeOpinion(self),
            PoetryExplicitSourcesOpinion(self),
            PoetryDynamicVersionOpinion(self),
            UsePEP517BuildOpinion(self),
        ]

    def get_toml_file(self, path: str) -> TOMLFile:
        if path not in self._toml_files:
            self._toml_files[path] = TOMLFile(self.base_path / path)
        return self._toml_files[path]

    def get_json_file(self, path: str) -> JsonFile:
        if path not in self._json_files:
            self._json_files[path] = JsonFile(self.base_path / path)
        return self._json_files[path]

    @property
    def pyproject(self) -> PyProjectTOMLFile:
        if "pyproject.toml" not in self._toml_files:
            self._toml_files["pyproject.toml"] = PyProjectTOMLFile(self.base_path / "pyproject.toml")
        return self._toml_files["pyproject.toml"]  # type: ignore

    def can_manage_project(self) -> bool:
        return (self.base_path / "pyproject.toml").exists()

    def finalize(self) -> bool:
        dirty = False
        for _, toml_file in self._toml_files.items():
            f_dirty = toml_file.finalize()
            dirty = dirty or f_dirty
        for _, json_file in self._json_files.items():
            f_dirty = json_file.finalize()
            dirty = dirty or f_dirty
        return dirty

    @property
    def is_dirty(self):
        return any([x.is_dirty for x in self._toml_files.values()]) or any(
            [x.is_dirty for x in self._json_files.values()]
        )


class Opinion:
    def __init__(self, project: OpinionatedProject):
        self.project = project

    def apply_changes(self):
        raise NotImplementedError()

    def is_poetry_project(self) -> bool:
        tools = self.project.pyproject.content.get("tool", {})
        return "poetry" in tools.keys()
