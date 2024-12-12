import argparse
import os
from pathlib import Path

from opinions import OpinionatedProject


def main():
    arg_parser = argparse.ArgumentParser()
    subparsers = arg_parser.add_subparsers(required=True)

    check_parser = subparsers.add_parser("check")
    check_parser.set_defaults(func=check)

    apply_parser = subparsers.add_parser("apply")
    apply_parser.set_defaults(func=apply)

    args = arg_parser.parse_args()
    args.func(args)


def check(args):
    project = prep_project()
    if project.is_dirty:
        print("Changes needed - run 'opinions apply' to fix")
        exit(1)
    else:
        print("No changes needed")


def apply(args):
    project = prep_project()
    result = project.finalize()
    if result:
        print("Project configured!")
    else:
        print("Nothing to do")


def prep_project() -> OpinionatedProject:
    project = OpinionatedProject(Path(os.getcwd()))
    for opinion in project.opinions:
        opinion.apply_changes()

    return project
