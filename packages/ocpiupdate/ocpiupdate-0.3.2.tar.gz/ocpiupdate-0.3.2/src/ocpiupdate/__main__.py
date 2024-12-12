#!/usr/bin/env python3

"""Script that automatically updates OpenCPI Projects."""

from __future__ import annotations

import argparse
import importlib.metadata
import logging
import pathlib
import sys
import xml.etree.ElementTree as ET
from typing import Iterable

from . import makefile, treesitter
from .config import Config
from .version import V2_4_7, Version

MODELS = ["hdl", "rcc"]

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("ocpiupdate")


def yield_owd_from_project(
    project_directory: pathlib.Path,
) -> Iterable[pathlib.Path]:
    """Yield a generator of worker directory paths from a project path."""
    for path in (f for model in MODELS for f in project_directory.rglob(f"*.{model}")):
        if not path.is_dir():
            continue
        model = path.suffix[1:]
        owd = path / f"{path.stem}-{model}.xml"
        if not owd.exists():
            owd = path / f"{path.stem}.xml"
            if not owd.exists():
                continue
        yield owd


def yield_workers_from_library(
    library_directory: pathlib.Path,
) -> Iterable[pathlib.Path]:
    """Yield a generator of worker directory paths from a library path."""
    for path in library_directory.iterdir():
        if not path.is_dir():
            continue
        if len(path.suffixes) == 0:
            continue
        model = path.suffix[1:]
        if model not in MODELS:
            continue
        yield path


def yield_specs_from_library(
    library_directory: pathlib.Path,
) -> Iterable[pathlib.Path]:
    """Yield a generator of spec file paths from a library path."""
    if not (library_directory / "specs").exists():
        return
    for path in (library_directory / "specs").iterdir():
        if path.suffix != ".xml":
            continue
        if not path.stem.endswith("spec"):
            continue
        yield path


def yield_recursive_findall(
    element: ET.Element,
    tag: str,
) -> Iterable[ET.Element]:
    """Yield all occurrences of a given XML tag at any depth in an XML tree."""
    if element.tag == tag:
        yield element
    for child in element:
        yield from yield_recursive_findall(child, tag)


class Arguments:
    """Class containing all globally relevant command line arguments."""

    dry_run: bool
    to_version: Version
    verbose: bool

    def __init__(self, namespace: argparse.Namespace) -> None:
        """Construct."""
        self.dry_run = namespace.dry_run
        self.to_version = namespace.to_version
        self.verbose = namespace.verbose


def v2_4_7_owd_rename(worker_directory: pathlib.Path, arguments: Arguments) -> bool:
    """
    Rename all OWD files to their v2.4.7 names.

    - Move all *.hdl/*.xml to *.hdl/*-hdl.xml
    - Move all *.rcc/*.xml to *.rcc/*-rcc.xml
        - This isn't done for RCC Workers that proxy one or more HDL Workers
          when moving to v2.4.7 or earlier.
        - See https://opencpi.dev/t/broken-hdl-worker-search-path-on-slave-attributes/105

    This function ignores OWDs that have already been migrated.
    """
    if arguments.to_version < V2_4_7:
        return False
    name = worker_directory.stem
    model = worker_directory.suffix[1:]
    old_owd_file = worker_directory / f"{name}.xml"
    # Ignore already converted workers
    if not old_owd_file.exists():
        logger.debug(
            "File '%s' not found, assuming conversion already completed",
            old_owd_file,
        )
        return False
    # Ignore RCC Workers that proxy HDL Workers in v2.4.7 and earlier
    if arguments.to_version <= V2_4_7 and model == "rcc":
        slaves = ET.parse(old_owd_file).getroot().find("slaves")
        if slaves is not None:
            for instance in yield_recursive_findall(slaves, "instance"):
                worker = instance.attrib.get("worker")
                if worker is None:
                    logger.debug(
                        "File '%s' is malformed: instance without worker",
                        old_owd_file,
                    )
                    return False
                if worker.endswith("hdl"):
                    logger.debug(
                        "File '%s' is an RCC Worker with a HDL Slave, "
                        "can't convert in v2.4.7 or earlier",
                        old_owd_file,
                    )
                    return False
    # Rename the file
    new_owd_file = worker_directory / f"{name}-{model}.xml"
    if not arguments.dry_run:
        old_owd_file.rename(new_owd_file)
    logger.info("Moved '%s' to '%s'", old_owd_file, new_owd_file)
    return True


def v2_4_7_move_spec_to_comp(spec_file: pathlib.Path, arguments: Arguments) -> bool:
    """Move all specs/*-spec.xml to *.comp/*-comp.xml."""
    if arguments.to_version < V2_4_7:
        return False
    # Make comp dir
    spec_file_name = spec_file.stem[:-5]
    comp_dir = spec_file.parent.parent / f"{spec_file_name}.comp"
    if not arguments.dry_run:
        comp_dir.mkdir(exist_ok=True)
    logger.info("Created '%s'", comp_dir)
    # Move file to new location
    new_comp_file = comp_dir / f"{spec_file_name}-comp.xml"
    if not arguments.dry_run:
        spec_file.rename(new_comp_file)
    logger.info("Moved '%s' to '%s'", spec_file, new_comp_file)
    return True


def v2_4_7_replace_renamed_specs(
    worker_xml: pathlib.Path,
    spec_files: list[pathlib.Path],
    arguments: Arguments,
) -> bool:
    """Replace the `spec` attribute where required due to a file move."""
    if arguments.to_version < V2_4_7:
        return False
    logger.debug("Scanning '%s' ... ", worker_xml)
    with worker_xml.open("r") as file:
        lines = file.readlines()
    changed_something = False
    for i, line in enumerate(lines):
        for spec_file in spec_files:
            # Case where spec="<spec>[-_]spec.xml"
            # Case where spec="<spec>[-_]spec"
            name = spec_file.stem[:-5]
            for case in [spec_file.name, spec_file.stem]:
                if case in line:
                    lines[i] = line.replace(case, name)
                    logger.info(
                        "Replaced '%s' with '%s' on line %d of '%s'",
                        case,
                        name,
                        i,
                        worker_xml,
                    )
                    changed_something = True
                    break
    if changed_something and not arguments.dry_run:
        with worker_xml.open("w") as file:
            file.writelines(lines)
    return changed_something


def parse_variables_from_makefiles(
    file_paths: list[pathlib.Path],
    file_identifier: str,
    config: Config,
) -> tuple[bool, dict[str, str]]:
    """Try to parse makefiles, returning a dictionary of their top level variables."""
    variables: dict[str, str] = {}
    node_fragments_to_ignore = config.get_list_setting_for_parse(
        "makefile",
        file_identifier,
        "node-fragments-to-ignore",
    )
    nodes_to_ignore = [
        treesitter.MAKE_PARSER.parse(fragment.encode("utf-8")).root_node.children[0]
        for fragment in node_fragments_to_ignore
    ]
    node_types_to_ignore = config.get_list_setting_for_parse(
        "makefile",
        file_identifier,
        "node-types-to-ignore",
    )
    for file_path in file_paths:
        if not file_path.exists():
            logger.debug(
                "File '%s' not found, assuming conversion already completed",
                file_path,
            )
            continue
        tree = treesitter.MAKE_PARSER.parse(file_path.read_bytes())
        for child in tree.root_node.children:
            # If node can be ignored, ignore it
            if child.type in node_types_to_ignore:
                logger.debug(
                    "Node ('%s') of type '%s' on line %d of '%s' is ignored "
                    "due to config",
                    child.text.decode("utf-8"),
                    child.type,
                    child.start_point[0],
                    file_path,
                )
                continue
            match_found = False
            for node in nodes_to_ignore:
                if treesitter.structural_equality(child, node):
                    logger.debug(
                        "Node ('%s') matches an ignored node",
                        treesitter.to_string(child),
                    )
                    match_found = True
                    break
            if match_found:
                continue
            # If variable is parsable, parse it. If not, fail
            if child.type == "variable_assignment":
                try:
                    makefile.update_variables_with_variable_assignment(child, variables)
                    continue
                except RuntimeError as err:
                    logger.warning("%s of '%s'", str(err), file_path)
                    logger.warning(
                        "File '%s' not parsed due to unrecognised operator",
                        file_path,
                    )
                    return False, variables
            # Node hasn't been recognised or ignored, so fail
            logger.debug(
                "Node ('%s') of type '%s' not supported when parsing %s to %s in '%s'",
                child.text.decode("utf-8"),
                child.type,
                child.start_point,
                child.end_point,
                file_path,
            )
            logger.warning(
                "File '%s' not parsed due to unrecognised node at position %s",
                file_path,
                child.start_point,
            )
            return False, variables
    return True, variables


def check_variables_for_xml(
    variables: dict[str, str],
    file_paths: list[pathlib.Path],
    file_identifier: str,
    config: Config,
) -> bool:
    """Check a collection of variables for validity in a given XML document."""
    accepted_variables = config.get_list_setting_for_parse(
        "xml",
        file_identifier,
        "accepted-variables",
    )
    not_recommended_variables = config.get_dict_setting_for_parse(
        "xml",
        file_identifier,
        "not-recommended-variables",
    )
    recommended_variables = config.get_dict_setting_for_parse(
        "xml",
        file_identifier,
        "recommended-variables",
    )
    for k in variables:
        if k in accepted_variables:
            continue
        if k in not_recommended_variables:
            logger.warning(
                "Variable '%s' not recommended when converting '%s' (%s)",
                k,
                [str(file_path) for file_path in file_paths],
                not_recommended_variables[k],
            )
            continue
        # Variable not recognised
        logger.warning(
            "Files '%s' not converted due to unrecognised variable: %s",
            [str(file_path) for file_path in file_paths],
            k,
        )
        return False
    for k in recommended_variables:
        if k not in variables:
            logger.warning(
                "Variable '%s' recommended for inclusion when converting '%s' (%s)",
                k,
                [str(file_path) for file_path in file_paths],
                recommended_variables[k],
            )
            continue
    return True


def translate_makefile_to_xml_in_project(
    project_directory: pathlib.Path,
    from_file_identifier: str,
    to_file_identifier: str,
    arguments: Arguments,
    config: Config,
) -> bool:
    """Migrate a makefile to an xml file in a project."""
    if arguments.to_version < V2_4_7:
        return False
    logger.debug(
        "translate_makefile_to_xml_in_project(%s, %s, %s, ..., ...)",
        project_directory,
        from_file_identifier,
        to_file_identifier,
    )
    project_relative_old_file_paths = config.get_list_setting_for_parse(
        "makefile",
        from_file_identifier,
        "paths",
    )
    if len(project_relative_old_file_paths) == 0:
        logger.warning(
            "Setting 'ocpiupdate.makefile.%s.paths' not found or empty",
            from_file_identifier,
        )
        return False
    old_file_paths = [
        project_directory / project_relative_old_file_path
        for project_relative_old_file_path in project_relative_old_file_paths
    ]
    # Check that all the variables are acceptable, terminate if they aren't
    parsable, variables = parse_variables_from_makefiles(
        old_file_paths,
        from_file_identifier,
        config,
    )
    if not parsable:
        return False
    translated_from_makefile_variables = config.get_dict_setting_for_parse(
        "xml",
        to_file_identifier,
        "translated-from-makefile-variables",
    )
    xml_variables = {
        translated_from_makefile_variables.get(k, k): v for k, v in variables.items()
    }
    valid = check_variables_for_xml(
        xml_variables,
        old_file_paths,
        to_file_identifier,
        config,
    )
    if not valid:
        return False
    # Build the XML file
    root_tag = config.get_setting_for_parse(
        "xml",
        to_file_identifier,
        "tag",
    )
    if root_tag is None:
        logger.warning(
            "Setting 'ocpiupdate.xml.%s.tag' not found",
            to_file_identifier,
        )
        return False
    project_relative_new_file_path = config.get_setting_for_parse(
        "xml",
        to_file_identifier,
        "path",
    )
    if project_relative_new_file_path is None:
        logger.warning(
            "Setting 'ocpiupdate.xml.%s.path' not found",
            to_file_identifier,
        )
        return False
    new_file_path = project_directory / project_relative_new_file_path
    if new_file_path.exists() and len(xml_variables) != 0:
        logger.warning(
            "File '%s' already exists. Partial migration is not supported, "
            "aborting migration",
            new_file_path,
        )
        return False
    old_file_paths = [
        old_file_path for old_file_path in old_file_paths if old_file_path.exists()
    ]
    if not arguments.dry_run:
        if not new_file_path.exists():
            root = ET.Element(root_tag, attrib=xml_variables)
            tree = ET.ElementTree(root)
            tree.write(new_file_path, encoding="utf-8", xml_declaration=True)
        for old_file_path in old_file_paths:
            old_file_path.unlink()
    if not new_file_path.exists():
        logger.info(
            "Created '%s' from '%s' ('%s', %s)",
            new_file_path,
            [str(old_file_path) for old_file_path in old_file_paths],
            root_tag,
            xml_variables,
        )
    logger.info(
        "Deleted '%s'",
        [str(old_file_path) for old_file_path in old_file_paths],
    )
    return True


def delete_file_in_project(
    project_directory: pathlib.Path,
    file_type: str,
    file_identifier: str,
    arguments: Arguments,
    config: Config,
) -> bool:
    """Delete a file in a project."""
    if arguments.to_version < V2_4_7:
        return False
    logger.debug(
        "delete_file_in_project(%s, %s, %s, ..., ...)",
        project_directory,
        file_type,
        file_identifier,
    )
    project_relative_file_paths = config.get_list_setting_for_parse(
        file_type,
        file_identifier,
        "paths",
    )
    if len(project_relative_file_paths) == 0:
        logger.warning(
            "Setting 'ocpiupdate.%s.%s.paths' not found or empty",
            file_type,
            file_identifier,
        )
        return False
    file_paths = [
        project_directory / project_relative_file_path
        for project_relative_file_path in project_relative_file_paths
    ]
    # Delete file if it is redundant
    at_least_one_file_deleted = False
    for file_path in file_paths:
        if file_type == "makefile":
            parsable, variables = parse_variables_from_makefiles(
                [file_path],
                file_identifier,
                config,
            )
            if not parsable:
                continue
        else:
            logger.error("File type '%s' not recognised", file_type)
            return False
        if len(variables) != 0:
            logger.warning(
                "File '%s' not deleted due to presence of variables: %s",
                file_path,
                variables,
            )
            continue
        if not arguments.dry_run:
            file_path.unlink(missing_ok=True)
        logger.info("Deleted '%s'", file_path)
        at_least_one_file_deleted = True
    return at_least_one_file_deleted


class MissingArgumentError(Exception):
    """Error when script is not given a required argument."""

    def __init__(self, argument: str) -> None:
        """Construct."""
        super().__init__(f"{argument} must be provided at least once")


def main() -> None:
    """Run the script."""
    # Argument parsing
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--config",
        type=pathlib.Path,
        default=pathlib.Path(__file__).parent / "ocpiupdate.toml",
        help="Use a given config file",
    )
    argparser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what the program would do, but don't write anything to disk",
    )
    argparser.add_argument(
        "--library",
        action="append",
        type=pathlib.Path,
        help="The libraries to search when moving `[-_]spec` files",
    )
    argparser.add_argument(
        "--project",
        action="append",
        type=pathlib.Path,
        help="The projects to search when modifying `spec` attributes",
    )
    argparser.add_argument(
        "--to-version",
        type=Version,
        help="The OpenCPI version to migrate to (2.4.7 [default] or newer)",
        default=V2_4_7,
    )
    argparser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable printing debug messages to stdout",
    )
    argparser.add_argument(
        "--version",
        action="store_true",
        help="Print the version of the program and exit",
    )
    args, unknown_args = argparser.parse_known_args()
    if len(unknown_args) != 0:
        logger.error("Extra arguments not recognised: %s", unknown_args)
        sys.exit(1)

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    if args.version:
        print(importlib.metadata.version(__package__ or __name__))  # noqa: T201
        sys.exit(0)

    try:
        # Load configuration
        config = Config.from_file(args.config)
        logger.debug("Parsed config file '%s' as: %s", args.config, str(config))

        # Validate arguments
        if args.project is None:
            argument = "--project"
            raise MissingArgumentError(argument)  # noqa: TRY301
        if args.library is None:
            argument = "--library"
            raise MissingArgumentError(argument)  # noqa: TRY301

        # Start of processing
        projects = args.project
        libraries = args.library
        arguments = Arguments(args)
        logger.debug(
            "Running over projects '%s' and libraries '%s ...",
            projects,
            libraries,
        )
        files_moved = []
        for library in libraries:
            for worker in yield_workers_from_library(library):
                v2_4_7_owd_rename(worker, arguments)
            for spec_file in yield_specs_from_library(library):
                v2_4_7_move_spec_to_comp(spec_file, arguments)
                files_moved.append(spec_file)
        migration_strategies = config.get_migration_strategies()
        for project in projects:
            for migration_strategy in migration_strategies:
                # Try to delete any file marked for deletion
                for file_identifier in migration_strategy.file_identifiers_to_delete:
                    delete_file_in_project(
                        project,
                        migration_strategy.file_type,
                        file_identifier,
                        arguments,
                        config,
                    )
                # Try to translate any file marked for deletion
                for (
                    from_file_identifier,
                    (to_file_type, to_file_identifier),
                ) in migration_strategy.file_identifiers_to_translate:
                    if (
                        migration_strategy.file_type == "makefile"
                        and to_file_type == "xml"
                    ):
                        translate_makefile_to_xml_in_project(
                            project,
                            from_file_identifier,
                            to_file_identifier,
                            arguments,
                            config,
                        )
                    else:
                        logger.warning(
                            "Migrating file type '%s' to '%s' by 'translate-to' "
                            "isn't supported",
                            migration_strategy.file_type,
                            to_file_type,
                        )
            for owd in yield_owd_from_project(project):
                # Edit any worker that referenced a moved spec
                v2_4_7_replace_renamed_specs(owd, files_moved, arguments)
    except Exception as err:
        logger.error(str(err))  # noqa: TRY400
        if args.verbose:
            raise
        sys.exit(1)


if __name__ == "__main__":
    main()
