from opinions import Opinion


class PoetryExplicitSourcesOpinion(Opinion):
    def apply_changes(self):
        if not self.is_poetry_project:
            return

        sources = self.project.pyproject.content.get("tool", {}).get("poetry", {}).get("source", [])

        for source in sources:
            if "secondary" in source:
                if source["secondary"]:
                    source["priority"] = "supplemental"
                del source["secondary"]

        for source in sources:
            if source["priority"] == "default":
                source["priority"] = "primary"

        if not any([x["name"].lower() == "pypi" for x in sources]) and not any(
            [x.get("priority", "primary") == "primary" for x in sources]
        ):
            sources.append({"name": "pypi", "priority": "primary"})
