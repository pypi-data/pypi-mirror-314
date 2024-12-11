"""Parser module to parse gear config.json."""

import logging
from pathlib import Path
from typing import Tuple

from flywheel_gear_toolkit import GearToolkitContext

from fw_gear_project_settings.utils import get_valid_project

log = logging.getLogger(__name__)


# This function mainly parses gear_context's config.json file and returns relevant
# inputs and options.
def parse_config(
    gear_context: GearToolkitContext,
) -> Tuple[str, dict]:
    """Parses context's config.json for gear use

    Returns:
        debug: Debug configuration, default False
        gear_args: Arguments needed for the gear to run as configured, including
            * template: Path to inputted template json file, else None
            * fixed_inputs: Path to inputted fixed input archive file, else None
            * output_dir: /flywheel/v0/output/, where created files will be placed
            * source: Flywheel Project which has the existing permissions and gear rules
            * clone_project_path: Path to new project, format <group_id/project_name>
            * default_group_permissions: Whether to use default group permissions to clone project
            * permissions: Whether to export/import permissions
            * gear_rules: Whether to export/import gear rules and related fixed inputs
            * apply_to_existing_project: Whether to apply settings and rules to existing project
            * existing_rules: Set behavior when project already has a rule with the same name as a template rule
            * data_views: Option to export/import DataViews
            * fw: Flywheel Client
    """

    debug = gear_context.config.get("debug")
    gear_args = {
        "template": gear_context.get_input_path("template"),
        "fixed_inputs": gear_context.get_input_path("fixed_inputs"),
        "output_dir": Path(gear_context.output_dir),
        "source": get_valid_project(gear_context.destination, gear_context.client),
        "clone_project_path": gear_context.config.get("clone_project_path"),
        "default_group_permissions": gear_context.config.get(
            "default_group_permissions"
        ),
        "permissions": gear_context.config.get("permissions"),
        "gear_rules": gear_context.config.get("gear_rules"),
        "apply_to_existing_project": gear_context.config.get(
            "apply_to_existing_project"
        ),
        "existing_rules": gear_context.config.get("existing_rules"),
        "data_views": gear_context.config.get("data_views"),
        "fw": gear_context.client,
    }

    log.info("Destination: {}".format(gear_context.destination))
    log.info("Config: {}".format(gear_context.config))

    return debug, gear_args
