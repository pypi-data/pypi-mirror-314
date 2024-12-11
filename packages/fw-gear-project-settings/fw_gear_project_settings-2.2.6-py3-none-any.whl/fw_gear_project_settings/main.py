import logging
from pathlib import Path

from flywheel import Client, Project

from fw_gear_project_settings.utils import (
    apply_template_to_project,
    create_project,
    download_fixed_inputs,
    generate_project_template,
    load_template_from_input,
)

log = logging.getLogger(__name__)


def run(
    template: str | None,
    fixed_inputs: str | None,
    output_dir: Path,
    source: Project,
    clone_project_path: str,
    default_group_permissions: bool,
    permissions: bool,
    gear_rules: bool,
    apply_to_existing_project: bool,
    existing_rules: str,
    data_views: bool,
    fw: Client,
) -> int:
    """Runs the gear as configured.

    Args:
        template: Path to inputted template json file, else None
        fixed_inputs: Path to inputted fixed input archive file, else None
        output_dir: /flywheel/v0/output, where created files will be placed
        source: Flywheel Project which has the existing permissions and gear rules
        clone_project_path: Path to new project, format <group_id/project_name>
        default_group_permissions: Whether to use default group permissions to clone project
        permissions: Whether to export/import permissions
        gear_rules: Whether to export/import gear rules and related fixed inputs
        apply_to_existing_project: Whether to apply settings and rules to existing project
        existing_rules: Set behavior when project already has a rule with the same name as a template rule
        data_views: Option to export/import DataViews
        fw: Flywheel Client
    """

    apply_template = True
    # This variable controls the application of the template.
    # When this is not true - because there is no clone
    # project or input provided - only the template
    # and fixed input archive will be generated.

    exit_status = 0

    if template:
        template = load_template_from_input(template)
        apply_from_input = True
    else:
        template = generate_project_template(
            fw,
            output_dir,
            source,
            permissions,
            data_views,
        )
        apply_from_input = False

    fixed_input_archive = None
    if gear_rules:
        fixed_input_archive = fixed_inputs or download_fixed_inputs(
            fw, output_dir, template, source.id
        )

    if clone_project_path:
        # If a clone_project_path was provided, attempt to create the project,
        # or find an existing project and return it.
        clone_project = create_project(
            fw,
            clone_project_path,
            apply_to_existing_project,
        )
    elif apply_from_input:
        # If the input template was already provided then the clone_projet
        # is the source_project
        log.info("Applying template from input. Setting clone project to source.")
        clone_project = source
    else:
        # We're just exporting a template.
        log.info("Exporting template... Done!")
        apply_template = False

    if apply_template:
        exit_status = apply_template_to_project(
            fw,
            permissions,
            default_group_permissions,
            gear_rules,
            existing_rules,
            data_views,
            clone_project,
            template,
            fixed_input_archive,
        )

    return exit_status
