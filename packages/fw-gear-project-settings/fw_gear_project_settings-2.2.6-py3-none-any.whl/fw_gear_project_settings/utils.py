import json
import logging
import os
import shutil
import tempfile
import zipfile
from datetime import date, datetime
from pathlib import Path
from pprint import pprint as pp

import flywheel
import glob2
from flywheel import Client, Project, RolesRoleAssignment, Rule

log = logging.getLogger(__name__)


def create_archive(content_dir: str, arcname: str, zipfilepath: str = None) -> str:
    """Generate an archive from a given directory.

    Args:
        content_dir: Full path to directory containing archive content.
        arcname: Name for top-level folder in archive.
        zipfilepath: Desired path of output archive. If not provided the
                           content_dir basename will be used. Defaults to None.

    Returns:
        str: Full path to created zip archive.
    """

    import zipfile

    if not zipfilepath:
        zipfilepath = content_dir + ".zip"
    with zipfile.ZipFile(zipfilepath, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
        zf.write(content_dir, arcname)
        for fn in os.listdir(content_dir):
            zf.write(
                os.path.join(content_dir, fn),
                os.path.join(os.path.basename(arcname), fn),
            )
    return zipfilepath


def extract_archive(zip_file_path: str, extract_location: str) -> str:
    """Extract zipfile to <zip_file_path> and return the path to the directory containing the files,
    which should be the zipfile name without the zip extension.

    Args:
        zip_file_path: Full path to existing archive.
        extract_location: Full path of top-level destination for extraction.

    Returns:
        str: Path to extracted archive
    """

    if not zipfile.is_zipfile(zip_file_path):
        log.warning("{} is not a Zip File!".format(zip_file_path))
        return None

    with zipfile.ZipFile(zip_file_path) as ZF:
        if "/" in ZF.namelist()[0]:
            extract_dest = os.path.join(
                extract_location, ZF.namelist()[0].split("/")[0]
            )
            ZF.extractall(extract_location)
            return extract_dest
        else:
            extract_dest = os.path.join(
                extract_location, os.path.basename(zip_file_path).split(".zip")[0]
            )
            if not os.path.isdir(extract_dest):
                log.debug("Creating extract directory: {}".format(extract_dest))
                os.mkdir(extract_dest)
            log.debug(
                "Extracting {} archive to: {}".format(zip_file_path, extract_dest)
            )
            ZF.extractall(extract_dest)

            return extract_dest


def generate_project_template(
    fw: Client,
    output_dir: Path,
    source: Project,
    permissions: bool,
    data_views: bool,
    outname: str = None,
) -> dict:
    """For a given project generate a dict with permissions and gear rules.

    Args:
        fw: Flywheel Client
        output_dir: Output directory
        source: Flywheel Project which has the existing permissions and gear rules.
        permissions: Option to export permissions
        data_views: Option to export data views
        outname: Full path to output the json file contianing the template.
            If not provided we default to `/flywheel/v0/output/project_template.json`

    Returns:
        dict: Project template containing 'permissions', 'rules', and 'views':
            {
              "permissions": [
                {
                  "id": "<user_id>",
                  "role_ids": "[ <access_rights> ]"
                }
              ],
              "rules": [
                {
                  "project_id": "<project_id>",
                  "gear_id": "<gear_id>",
                  "name": "<gear_name>",
                  "config": {},
                  "fixed_inputs": [
                    {
                      "type": "project",
                      "id": "<container_id>",
                      "name": "<file_name>",
                      "input": "<input_name>"
                    }
                  ],
                  "auto_update": false,
                  "any": [],
                  "all": [
                    {
                      "type": "file.type",
                      "value": "dicom",
                      "regex": false
                    }
                  ],
                  "_not": [],
                  "disabled": true,
                  "compute_provider_id": null,
                  "id": null
                }
              ],
              "views" [
                {
                    "columns": [],
                    "description": null,
                    "error_column": true,
                    "file_spec": null,
                    "id": <view_id>,
                    "include_ids": false,
                    "include_labels": false,
                    "label": <view_label>,
                    "missing_data_strategy": "none",
                    "origin": {
                        "id": <user_id>,
                        "type": "user"
                    },
                    "sort": null
                }
            ]
            }
    """

    if not outname:
        outname = os.path.join(
            output_dir, "project-settings_template_{}.json".format(source.id)
        )

    template = dict()
    template["rules"] = list()

    log.info(
        f"Generating template from source project: {source.group}/{source.label} [id={source.id}]"
    )

    rules = [r.to_dict() for r in fw.get_project_rules(source.id)]

    if permissions:
        template["permissions"] = [p.to_dict() for p in source.permissions]
    else:
        template["permissions"] = list()

    if data_views:
        template["views"] = [v.to_dict() for v in fw.get_views(source.id)]
    else:
        template["views"] = list()

    for rule in rules:
        # Here we grab the gear info for easy lookup later on. Note that it will
        # be removed.
        rule["gear"] = fw.get_gear(rule["gear_id"]).gear.to_dict()
        template["rules"].append(rule)

    save_template(template, outname)

    return template


def save_template(template: dict, outfilename: str) -> str:
    """Write project template to JSON file.

    Args:
        template: Template dictionary, created by generate_project_template
        outfilename: Full path for output file.

    Returns:
        str: Full path to generated template json.
    """

    def json_serial(obj):
        """JSON serializer for datetime"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError("Type %s not serializable" % type(obj))

    with open(outfilename, "w") as of:
        json.dump(
            template,
            of,
            sort_keys=True,
            indent=4,
            separators=(",", ": "),
            default=json_serial,
        )

    return outfilename


def download_fixed_inputs(
    fw: Client, output_dir: str, template: dict, project_id: str
) -> str | None:
    """For each fixed input found in the templates gear rules, download the file
       and create an archive from those files within the outdir specified by the
       gear_context. The resulting archive can then be loaded to a new project.

    Args:
        fw: Flywheel Client
        output_dir: Output directory
        template: Project template dictionary, containing a list of project
            "permissions" and a list of project "rules".
        project_id: Source project ID (used for naming the output archive.)

    Returns:
        str: Full path to generated fixed input archive.
    """

    tdirpath = tempfile.mkdtemp()

    # Create the archive directory, which will be zipped
    content_dir = os.path.join(
        tdirpath, "project-settings_fixed-inputs_{}".format(project_id)
    )
    os.mkdir(content_dir)

    downloaded = list()  # List of files that are to be downloaded

    log.info("Checking template for fixed inputs...")
    for rule in template["rules"]:
        if rule.get("fixed_inputs"):
            for fixed_input in rule.get("fixed_inputs"):
                container = fw.get(fixed_input.get("id"))
                fname = fixed_input.get("name")
                container.download_file(fname, os.path.join(content_dir, fname))
                downloaded.append(fname)

    if downloaded:
        archive_name = os.path.join(output_dir, os.path.basename(content_dir) + ".zip")
        log.info(
            f"Saved {len(downloaded)} fixed input files. Creating archive {archive_name}"
        )
        create_archive(content_dir, os.path.basename(content_dir), archive_name)
    else:
        log.info(f"Found {len(downloaded)} fixed input files.")
        archive_name = None

    shutil.rmtree(tdirpath)

    return archive_name


def create_project(
    fw: Client, clone_project_path: str, apply_to_existing_project: bool
) -> Project:
    """Create project specified in config.clone_project_path. If an existing
        project is found (and config.apply_to_existing_project flag is set to
        True) it will be returned.

    Args:
        fw: Flywheel Client
        clone_project_path: Path to new project, format <group_id>/<project_name>
        apply_to_existing_project: Whether to apply settings and rules to existing project

    Returns:
        Project: Flywheel Project to which the template permissions and rules will be applied.
    """

    clone_project_path_split = clone_project_path.split("/")
    # clone_project_path should have exactly one "/" and therefore should split into 2,
    # else raise an error.
    if len(clone_project_path_split) != 2:
        log.error(
            f"{clone_project_path} is not a correctly formatted path to a Flywheel "
            "project. Please check that `clone_project_path` is in the format "
            "<group_id>/<project_name> and rerun the gear. Exiting."
        )
        os.sys.exit(1)

    group_id = clone_project_path_split[0]
    project_label = clone_project_path_split[1]

    # Check for existing project
    try:
        project = fw.lookup(f"{group_id}/{project_label}")
        if apply_to_existing_project and project:
            log.info(
                f"Existing project {group_id}/{project_label} (id={project.id}) found! "
                "apply_to_existing_project flag is set... the template will be applied to this project!"
            )
            return fw.get_project(project.id)
        else:
            log.exception(
                f"Project {group_id}/{project_label} (id={project.id}) found! "
                "apply_to_existing_project flag is False, bailing out!"
            )
            os.sys.exit(1)
    except SystemExit:
        # SystemExit within try, plus generic except, is handled
        # poorly in testing. This is here to make *sure* we exit.
        os.sys.exit(1)

    except:  # noqa: E722
        pass

    log.info(f"Creating new project: group={group_id}, label={project_label}")
    try:
        project_id = fw.add_project({"group": group_id, "label": project_label})
        project = fw.get_project(project_id)
        log.info(
            f"Done. Created new project: group={group_id}, label={project_label}, id={project.id}"
        )

    except flywheel.ApiException as err:
        log.exception(
            f"API error during project creation: {err.status} -- {err.reason} -- {err.detail}"
        )
        os.sys.exit(1)

    return project


def upload_fixed_inputs(fixed_input_archive: str, project: Project) -> bool:
    """Unpack the fixed inputs archive and upload to the clone project.

    Args:
        fixed_input_archive: Full path to `fixed_input_archive`.
        project: Flywheel Project to which the fixed_inputs will be uploaded.

    Returns:
        bool: True for success, False otherwise.
    """

    # If a single unzipped JSON file was passed in, upload the file and return
    if fixed_input_archive.lower().endswith("json"):
        log.info(f"Uploading fixed input file: {os.path.basename(fixed_input_archive)}")
        project.upload_file(fixed_input_archive)
        return True

    tdirpath = tempfile.mkdtemp()

    fixed_input_dir = extract_archive(fixed_input_archive, tdirpath)

    # If archive was created via MACOS compression, it may have a "__MACOSX" dir
    if os.path.exists(fixed_input_dir + "/__MACOSX/"):
        log.debug("Deleting __MACOSX directory created by MACOS compression")
        shutil.rmtree(fixed_input_dir + "/__MACOSX/")

    # Get file paths from the input dir
    fixed_inputs = glob2.glob(fixed_input_dir + "/*", recursive=True)

    # Upload each of the fixed inputs to the clone project.
    for fixed_input in fixed_inputs:
        log.info(f"Uploading fixed input file: {os.path.basename(fixed_input)}")
        project.upload_file(fixed_input)

    log.debug(f"Deleting {fixed_input_dir}")

    shutil.rmtree(tdirpath)

    return True


def apply_template_to_project(
    fw: Client,
    permissions: bool,
    default_group_permissions: bool,
    gear_rules_config: bool,
    existing_rules: str,
    data_views: bool,
    project: Project,
    template: dict,
    fixed_input_archive: str = None,
) -> int:
    """Apply default group (default) or template permissions, and gear rules to <project>.

    Args:
        fw: Flywheel Client
        permissions: Whether to export/import permissions
        default_group_permissions: Whether to use default group permissions to clone project
        gear_rules_config: Whether to export/import gear rules and related fixed inputs
        existing_rules: Set behavior when project already has a rule with the same name as a template rule
        data_views: Option to export/import data views
        project: Flywheel Project to which the rules and permissions will be applied.
        template: Project template dictionary, containing a list of project "permissions" and a list of project "rules".
        fixed_input_archive (optional): Path to archive containing gear rule fixed inputs. Defaults to None.

    Returns:
        int: 0 for success, 1 otherwise.
    """

    exit_status = 0

    # Permissions
    if (permissions and template.get("permissions")) or default_group_permissions:
        log.info("APPLYING PERMISSIONS TO PROJECT...")
        all_users = [x.id for x in fw.get_all_users()]
        users = [x.id for x in project.permissions]
        if default_group_permissions:
            log.info("Applying default group permissions...")
            permissions = fw.get_group(project.group).permissions_template
        else:
            permissions = template["permissions"]

        for permission in permissions:
            log.debug(pp(permission))
            if not isinstance(permission, RolesRoleAssignment):
                permission = RolesRoleAssignment(
                    permission["id"], permission["role_ids"]
                )
            if (permission.id not in users) and (permission.id in all_users):
                log.info(" Adding {} to {}".format(permission.id, project.label))
                project.add_permission(permission)
            else:
                log.warning(
                    " {} will not be added to {}. The user is either already in the project or not a valid user.".format(
                        permission.id, project.label
                    )
                )
        log.info("...PERMISSIONS APPLIED")
    else:
        log.info("NOT APPLYING PERMISSIONS TO PROJECT!")

    # Handle Fixed Inputs
    if gear_rules_config and template.get("rules"):
        log.info("APPLYING GEAR RULES TO PROJECT...")
        if fixed_input_archive:
            log.info("Unpacking and uploading fixed gear inputs...")
            upload_fixed_inputs(fixed_input_archive, project)
            log.info("...Done.")

        # Gear Rules
        gear_rules = list()
        for rule in template["rules"]:
            log.info(" Generating new rule from template: {}".format(rule["name"]))
            try:
                # If the gear does not exist, we are probably on another instance and
                # need to look it up.
                log.info("Locating gear {}...".format(rule["gear_id"]))
                gear = fw.get_gear(rule["gear_id"])
                log.info(
                    "Found {},{}:{}".format(
                        rule["gear_id"], rule["gear"]["name"], rule["gear"]["version"]
                    )
                )
            except:  # noqa: E722
                log.warning(
                    "Gear ID {} cannot be found on this system!".format(rule["gear_id"])
                )
                try:
                    log.info("Checking for the gear locally...")
                    gear = fw.lookup(
                        "gears/{}/{}".format(
                            rule["gear"]["name"], rule["gear"]["version"]
                        )
                    )
                    rule["gear_id"] = gear.id
                except:  # noqa: E722
                    log.error(
                        "{}:{} was not found on this system! Please install it!".format(
                            rule["gear"]["name"], rule["gear"]["version"]
                        )
                    )
                    log.warning("Skipping this rule! {}".format(rule["name"]))
                    exit_status = 1
                    continue

            # For each fixed input, fix the project id
            if rule["fixed_inputs"]:
                for fi in range(0, len(rule["fixed_inputs"])):
                    rule["fixed_inputs"][fi]["id"] = project.id
                    rule["fixed_inputs"][fi]["type"] = "project"
                    if "base" in rule["fixed_inputs"][fi].keys() and not rule[
                        "fixed_inputs"
                    ][fi].get("base"):
                        # If key exists and value is None/empty, delete key
                        del rule["fixed_inputs"][fi]["base"]
                    if "found" in rule["fixed_inputs"][fi].keys() and not rule[
                        "fixed_inputs"
                    ][fi].get("found"):
                        del rule["fixed_inputs"][fi]["found"]

            # Fix all and any fields
            if rule["all"]:
                for ar in range(0, len(rule["all"])):
                    if not rule["all"][ar]["regex"]:
                        rule["all"][ar]["regex"] = False
            if rule["any"]:
                for ar in range(0, len(rule["any"])):
                    if not rule["any"][ar]["regex"]:
                        rule["any"][ar]["regex"] = False
            if rule["_not"]:
                log.debug("RULE NOT")
                for ar in range(0, len(rule["_not"])):
                    if not rule["_not"][ar]["regex"]:
                        log.debug("setting to false...")
                        rule["_not"][ar]["regex"] = False

            new_rule = Rule(
                project_id=project.id,
                gear_id=rule["gear_id"],
                name=rule["name"],
                config=rule["config"],
                fixed_inputs=rule["fixed_inputs"],
                auto_update=rule["auto_update"],
                any=rule["any"],
                all=rule["all"],
                _not=rule["_not"],
                disabled=True,
            )

            # role_id, priority, and triggering input are not currently able to be set
            # on Rule init, but can be appended post-init.
            # For R/W compatibility, the API demands role_id be non-null,
            # else it won't allow the rule to save.
            try:
                modifiers = {"role_id": rule["role_id"], "disabled": rule["disabled"]}
            except KeyError:
                log.warning(
                    "Role_ID not found in gear rule %s, rule will be added as disabled.",
                    rule["name"],
                )
                modifiers = {"disabled": True}

            try:
                modifiers["priority"] = rule["priority"]
            except KeyError:
                log.warning(
                    "Priority not found in gear rule %s, priority defaulting to medium.",
                    rule["name"],
                )

            try:
                modifiers["triggering_input"] = rule["triggering_input"]
            except KeyError:
                log.warning(
                    "Triggering input not found in gear rule %s, no triggering input will be set.",
                    rule["name"],
                )

            gear_rules.append((new_rule, modifiers))

        RULE_ACTION = existing_rules

        if RULE_ACTION == "REPLACE ALL":
            log.info("REPLACE ALL action was configured. Deleting existing rules.")
            for rule in fw.get_project_rules(project.id):
                fw.remove_project_rule(project.id, rule.id)

        # project_rules = [x for x in fw.get_project_rules(project.id)]
        project_rule_names = [x.name for x in fw.get_project_rules(project.id)]
        log.debug(project_rule_names)

        for gear_rule, modifier in gear_rules:
            if gear_rule.get("name") in project_rule_names:
                log.warning(
                    "A matching rule for '{}' was already found on this project.".format(
                        gear_rule.get("name")
                    )
                )
                matching_rule = [
                    x
                    for x in fw.get_project_rules(project.id)
                    if x.name == gear_rule.get("name")
                ]
                if RULE_ACTION == "MATCH":
                    for mr in matching_rule:
                        log.info(
                            "MATCH action was configured. Deleting the matching rule."
                        )
                        fw.remove_project_rule(project.id, mr.id)
                elif RULE_ACTION == "SKIP":
                    log.info(
                        "SKIP action was configured. Not adding rule from template."
                    )
                    continue
                elif RULE_ACTION == "APPEND":
                    log.warning(
                        "APPEND action was configured. Template rule will be added - duplicates will exist."
                    )
            try:
                log.info(
                    'Adding "{}" rule to "{} (id={})" project'.format(
                        gear_rule["name"], project.label, project.id
                    )
                )
                created_rule = fw.add_project_rule(project.id, gear_rule)
                fw.modify_project_rule(project.id, created_rule.id, modifier)
            except flywheel.ApiException as err:
                log.error(
                    f"API error during gear rule creation: {err.status} -- {err.reason} -- {err.detail}. \nBailing out!"
                )
                log.debug(gear_rule)
                os.sys.exit(1)
        log.info("...GEAR RULES APPLIED TO PROJECT!")
    else:
        log.info("NOT APPLYING GEAR RULES TO PROJECT! (config.gear_rules=False)")

    # Data Views
    if data_views and template.get("views"):
        log.info("APPLYING DATA VIEWS TO PROJECT...")
        # We don't want to add any views that are already on the project.
        already_existing_views = [v.to_dict() for v in fw.get_views(project.id)]
        already_existing_view_ids = [d.get("id") for d in already_existing_views]
        for view in template.get("views"):
            if view.get("id") not in already_existing_view_ids:
                log.info(f"Adding Data View with label {view.get('label')}")
                created_view = fw.View(
                    label=view.get("label"),
                    include_ids=view.get("include_ids", True),
                    include_labels=view.get("include_labels", True),
                    error_column=view.get("error_column"),
                    sort=view.get("sort", True),
                )
                created_view.file_spec = view.get("file_spec")
                created_view.description = view.get("description")
                created_view.columns = view.get("columns")
                created_view.missing_data_strategy = view.get("missing_data_strategy")
                created_view.group_by = view.get("group_by")
                created_view.filter = view.get("filter")

                fw.add_view(project.id, created_view)
        log.info("...DATA VIEWS APPLIED TO PROJECT!")
    else:
        log.info("NOT APPLYING DATA VIEWS TO PROJECT! (config.data_views=False)")

    return exit_status


def get_valid_project(destination: dict, fw: Client) -> Project:
    """Use the <gear_context> to parse the destination and use it to determine
        a vaild project. The destination should be an analysis, and the parent of
        that analysis container must be a project. That project is returned here.

    Args:
        destination: gear_context.destination dictionary
        fw: Flywheel Client
    Returns:
        Project: Flywheel Project which has the existing permissions and gear rules.
    """

    if destination["type"] != "analysis":
        msg = "Destination must be an analysis!"
        log.error(msg)
        os.sys.exit(1)

    analysis = fw.get_analysis(destination["id"])

    try:
        project = fw.get_project(analysis.parent["id"])
    except flywheel.ApiException as err:
        log.error(
            f"Could not retrieve source project. This Gear must be run at the project level!: {err.status} -- {err.reason} -- {err.detail}. \nBailing out!"
        )
        os.sys.exit(1)

    return project


def load_template_from_input(template_file: str) -> dict:
    """Load json template from file.

    Args:
        template_file: Full path to JSON template file.

    Returns:
        dict: Project template containing 'permissions', and 'rules':
            {
              "permissions": [],
              "rules": []
            }
    """

    log.info(f"Loading existing template file: {template_file}")
    with open(template_file, "r") as tf:
        template = json.load(tf)

    return template
