from . import Opinion


class RuffVSCodeOpinion(Opinion):
    def apply_changes(self) -> None:
        vscode_settings = self.project.get_json_file(".vscode/settings.json")

        vscode_settings.content["mypy-type-checker.importStrategy"] = "fromEnvironment"

        for setting in list(vscode_settings.content.keys()):
            if setting.startswith("python.linting") or setting == "python.formatting.provider":
                del vscode_settings.content[setting]

        if "[python]" not in vscode_settings.content:
            vscode_settings.content["[python]"] = {}
        python_settings = vscode_settings.content["[python]"]

        python_settings["editor.defaultFormatter"] = "charliermarsh.ruff"
        python_settings["editor.formatOnSave"] = True

        if "editor.codeActionsOnSave" not in python_settings:
            python_settings["editor.codeActionsOnSave"] = {}
        on_save_settings = python_settings["editor.codeActionsOnSave"]
        on_save_settings["source.organizeImports.ruff"] = "explicit"

        extensions_config = self.project.get_json_file(".vscode/extensions.json")
        if "recommendations" not in extensions_config.content:
            extensions_config.content["recommendations"] = []
        recommendations: list[str] = extensions_config.content["recommendations"]

        for ext in [
            "ms-python.python",
            "charliermarsh.ruff",
            "ms-python.mypy-type-checker",
        ]:
            if ext not in recommendations:
                recommendations.append(ext)
