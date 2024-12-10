
import os
import json
from typing import Any, Optional

from keycloak import KeycloakOpenID
import openapi_client as client
import click
from openapi_client.models.postgresql_build_method import PostgresqlBuildMethod
from os import path, walk
from datetime import datetime
from .logger import log
from .auth import authenticate
from .helpers import (load_config, 
                      parse_betas, 
                      validate_export_parameter, 
                      get_export_parameters, 
                      download_avatar,
                      select_asset_id,
                      get_timestamp,
                      get_measurements_dict,
                      Uploader, State)
from .motions import TMRMotion
from .avatars import from_betas, export, from_images, from_measurements, from_scans, from_video, from_smpl
from .batch_create import validate_batch_input_dir, handle_batch_processing
from .user import User, request_user_info
from .constants import CREDIT_COSTS


CURRENT_DIR = path.dirname(path.abspath(__file__))
DEFAULT_CONFIG = path.join(CURRENT_DIR, "../configs/prod.toml")

@click.group()
@click.pass_context
@click.option('--config',
              type=click.Path(exists=True), default=os.environ.get("MCME_CONFIG_PATH", DEFAULT_CONFIG), help="Path to config file")
@click.option(
    "--username",
    default=lambda: os.environ.get("MCME_USERNAME")
)
@click.option(
    "--password",
    default=lambda: os.environ.get("MCME_PASSWORD")
)
def cli(ctx: click.Context, 
        username: str,
        password: str,
        config: str) -> None:
    """
    Command-line interface for the Meshcapade.me API.
    """
    ctx.ensure_object(dict)
    ctx.obj["config"] = load_config(config)
    ctx.obj["keycloak_tokens"] = os.path.expanduser(ctx.obj["config"]["cli_state"]["keycloak_tokens"])
    auth_config = ctx.obj["config"]["auth"]
    keycloak_openid: KeycloakOpenID = KeycloakOpenID(server_url=auth_config["server_url"],
                                    client_id=auth_config["client_id"],
                                    realm_name=auth_config["realm_name"])
    state = State(ctx.obj["keycloak_tokens"])
    ctx.obj["token"] = authenticate(keycloak_openid, state, username, password)
    # construct api client
    configuration = client.Configuration(
        host = ctx.obj["config"]["api"]["host"]
    )
    configuration.access_token =  ctx.obj["token"]
    # Enter a context with an instance of the API client
    ctx.obj["api_client"] = client.ApiClient(configuration)
    

@cli.result_callback()
@click.pass_context
def close_api_client(
    ctx: click.Context,
    result: Any,
    **kwargs):
    ctx.obj["api_client"].close()

@cli.group()
@click.pass_context
@click.option(
    "--download-format",
    type=click.Choice(["OBJ", "FBX"], case_sensitive=False),
    is_eager=True,
    help="Format for downloading avatar"
)
@click.option(
    "--pose",
    type=click.Choice(["T", "A", "I", "SCAN"], case_sensitive=False),
    callback=validate_export_parameter,
    help="Pose the downloaded avatar should be in. SCAN is only applicable for avatars created from images, as it corresponds to the pose of the person captured in the image."
)
@click.option(
    "--animation",
    type=click.Choice(["a-salsa"], case_sensitive=False),
    callback=validate_export_parameter,
    help="Animation for the downloaded avatar"
)
@click.option(
    "--compatibility-mode",
    type=click.Choice(["DEFAULT", "OPTITEX", "UNREAL"], case_sensitive=False),
    callback=validate_export_parameter,
    help="Adjust output for compatibility with selected software."
)
@click.option(
    "--out-file",
    type=click.Path(dir_okay=False),
    callback=validate_export_parameter,
    help="File to save created avatar mesh to"
)
def create(
    ctx: click.Context, 
    download_format: str, 
    pose: str, 
    animation: str, 
    compatibility_mode: str, 
    out_file: click.Path
    ) -> None:
    """
    Create avatars. Please be aware that these commands cost credits.
    """
    # all create avatar operations need keycloak authentication
    ctx.obj["download"] = True if download_format is not None else False


@create.command(name="from-betas")
@click.pass_context
@click.option('--gender',
              type=click.Choice(client.EnumsGender.enum_values(), case_sensitive=False),
              help="Gender of created avatar")
@click.option('--betas',
              type=click.UNPROCESSED, callback=parse_betas, 
              help="Beta values. Supply like 0.1,0.2 or \"[0.1,0.2]\"")
@click.option('--name',
              type=str, 
              default="avatar_from_betas",
              help="Name of created avatar")
@click.option('--model-version',
              type=click.Choice(client.EnumsModelVersion.enum_values(), case_sensitive=False), 
              help="Model version")
def create_from_betas(
    ctx: click.Context,
    gender: Optional[client.EnumsGender], 
    betas: list[float], 
    name: str, 
    model_version: Optional[client.EnumsModelVersion]
    ) -> None:
    """Create avatar from betas."""
    # Create avatar from betas
    api_instance = client.CreateAvatarsFromBetasApi(ctx.obj["api_client"])
    asset_id = from_betas(gender, betas, name, model_version, api_instance)
    log.info(f"AssetID: {asset_id}")

    # Exit here if avatar should not be downloaded
    if ctx.obj["download"]:
        # Get download parameters from parent context
        params = get_export_parameters(ctx)
        # Export avatar
        ctx.invoke(export_and_download_avatar, 
                   format=params.download_format,
                   pose=params.pose,
                   animation=params.animation,
                   compatibility_mode=params.compatibility_mode,
                   out_file=params.out_file,
                   asset_id=asset_id)


@create.command(name="from-measurements")
@click.pass_context
@click.option('--gender',
              type=click.Choice(client.EnumsGender.enum_values(), case_sensitive=False),
              required=True,
              help="Gender of created avatar")
@click.option('--name',
              type=str, 
              default="avatar_from_measurements",
              help="Name of created avatar")
@click.option('--height',
              type=float,
              help="Height")
@click.option('--weight',
              type=float,
              help="Weight")
@click.option('--bust-girth',
              type=float,
              help="Bust girth")
@click.option('--ankle-girth',
              type=float,
              help="Ankle girth")
@click.option('--thigh-girth',
              type=float,
              help="Thigh girth")
@click.option('--waist-girth',
              type=float,
              help="Waist girth")
@click.option('--armscye-girth',
              type=float,
              help="Armscye girth")
@click.option('--top-hip-girth',
              type=float,
              help="Top hip girth")
@click.option('--neck-base-girth',
              type=float,
              help="Neck base girth")
@click.option('--shoulder-length',
              type=float,
              help="Shoulder length")
@click.option('--lower-arm-length',
              type=float,
              help="Lower arm length")
@click.option('--upper-arm-length',
              type=float,
              help="Upper arm length")
@click.option('--inside-leg-height',
              type=float,
              help="Inside leg height")
@click.option('--model-version',
              type=click.Choice(client.EnumsModelVersion.enum_values(), case_sensitive=False), 
              help="Model version")
def create_from_measurements(
    ctx: click.Context,
    gender: Optional[client.EnumsGender],
    name: str,
    height,
    weight,
    bust_girth,
    ankle_girth,
    thigh_girth,
    waist_girth,
    armscye_girth,
    top_hip_girth,
    neck_base_girth,
    shoulder_length,
    lower_arm_length,
    upper_arm_length,
    inside_leg_height,
    model_version: Optional[client.EnumsModelVersion]
    ) -> None:
    """Create avatar from measurements."""
    # Create avatar from measurements
    measurements = get_measurements_dict(
    height,
    weight,
    bust_girth,
    ankle_girth,
    thigh_girth,
    waist_girth,
    armscye_girth,
    top_hip_girth,
    neck_base_girth,
    shoulder_length,
    lower_arm_length,
    upper_arm_length,
    inside_leg_height
    )
    api_instance_from_measurements = client.CreateAvatarFromMeasurementsApi(ctx.obj["api_client"])
    api_instance_avatars = client.AvatarsApi(ctx.obj["api_client"])
    timeout = ctx.obj["config"]["cli"]["timeout"]
    asset_id = from_measurements(gender, name, measurements, model_version, api_instance_from_measurements, api_instance_avatars, timeout)

    # Exit here if avatar should not be downloaded
    if ctx.obj["download"]:
        # Get download parameters from parent context
        params = get_export_parameters(ctx)
        # Export avatar
        ctx.invoke(export_and_download_avatar, 
                   format=params.download_format,
                   pose=params.pose,
                   animation=params.animation,
                   compatibility_mode=params.compatibility_mode,
                   out_file=params.out_file,
                   asset_id=asset_id)

@create.command(name="from-images")
@click.pass_context
@click.option('--gender',
              type=click.Choice(client.EnumsGender.enum_values(), case_sensitive=False),
              help="Gender of created avatar")
@click.option('--name',
              type=str, 
              default="avatar_from_images",
              help="Name of created avatar")
@click.option('--input',
              type=click.Path(dir_okay=False, exists=True),
              help="Path to input image")
@click.option('--height',
              type=int,
              help="Height of the person in the image")
@click.option('--weight',
              type=int,
              help="Weight of the person in the image")
@click.option('--image-mode',
              type=click.Choice(["AFI", "BEDLAM_CLIFF"], case_sensitive=False),
              default="AFI",
              help="Mode for avatar creation")
def create_from_images(
    ctx: click.Context,
    gender: Optional[client.EnumsGender],
    name: str,
    input: str,
    height: int,
    weight: int,
    image_mode: str
    ) -> None:
    """Create avatar from images."""
    api_instance_images = client.CreateAvatarFromImagesApi(ctx.obj["api_client"])
    api_instance_avatars = client.AvatarsApi(ctx.obj["api_client"])
    uploader = Uploader()
    timeout = ctx.obj["config"]["cli"]["timeout"]
    asset_id = from_images(gender, name, input, height, weight, image_mode, api_instance_images, api_instance_avatars, uploader, timeout)

    # Exit here if avatar should not be downloaded
    if ctx.obj["download"]:
        # Get download parameters from parent context
        params = get_export_parameters(ctx)
        # Export avatar
        ctx.invoke(export_and_download_avatar, 
                   format=params.download_format,
                   pose=params.pose,
                   animation=params.animation,
                   compatibility_mode=params.compatibility_mode,
                   out_file=params.out_file,
                   asset_id=asset_id)


@create.command(name="from-scans")
@click.pass_context
@click.option('--gender',
              type=click.Choice(client.EnumsGender.enum_values(), case_sensitive=False),
              help="Gender of created avatar")
@click.option('--name',
              type=str, 
              default="avatar_from_scans",
              help="Name of created avatar")
@click.option('--input',
              type=click.Path(dir_okay=False, exists=True),
              help="Path to input image")
@click.option('--init-pose',
              type=str,
              help="Pose for initialization")
@click.option('--up-axis',
              type=str,
              help="Up axis")
@click.option('--look-axis',
              type=str,
              help="Look axis")
@click.option('--input-units',
              type=str, 
              help="Input units of scan")
def create_from_scans(
    ctx: click.Context,
    gender: Optional[client.EnumsGender],
    name: str,
    input: str,
    init_pose: str,
    up_axis: str,
    look_axis: str,
    input_units: str
    ) -> None:
    """Create avatar from images."""
    api_instance_scan = client.CreateAvatarFromScansApi(ctx.obj["api_client"])
    api_instance_avatars = client.AvatarsApi(ctx.obj["api_client"])
    uploader = Uploader()
    timeout = ctx.obj["config"]["cli"]["timeout"]
    asset_id = from_scans(gender, name, input, init_pose, up_axis, look_axis, input_units, api_instance_scan, api_instance_avatars, uploader, timeout)

    # Exit here if avatar should not be downloaded
    if ctx.obj["download"]:
        # Get download parameters from parent context
        params = get_export_parameters(ctx)
        # Export avatar
        ctx.invoke(export_and_download_avatar, 
                   format=params.download_format,
                   pose=params.pose,
                   animation=params.animation,
                   compatibility_mode=params.compatibility_mode,
                   out_file=params.out_file,
                   asset_id=asset_id)


@create.command(name="from-video")
@click.pass_context
@click.option('--gender',
              type=click.Choice(client.EnumsGender.enum_values(), case_sensitive=False),
              help="Gender of created avatar")
@click.option('--name',
              type=str, 
              default="avatar_from_images",
              help="Name of created avatar")
@click.option('--input',
              type=click.Path(dir_okay=False, exists=True),
              help="Path to input video")
def create_from_video(
    ctx: click.Context,
    gender: Optional[client.EnumsGender],
    name: str,
    input: str
    ) -> None:
    """Create avatar from a single video."""
    api_instance_images = client.CreateAvatarFromVideoApi(ctx.obj["api_client"])
    api_instance_avatars = client.AvatarsApi(ctx.obj["api_client"])
    uploader = Uploader()
    timeout = ctx.obj["config"]["cli"]["timeout"]
    asset_id = from_video(gender, name, input, api_instance_images, api_instance_avatars, uploader, timeout)

    # Exit here if avatar should not be downloaded
    if ctx.obj["download"]:
        # Get download parameters from parent context
        params = get_export_parameters(ctx)
        # Export avatar
        ctx.invoke(export_and_download_avatar, 
                   format=params.download_format,
                   pose=params.pose,
                   animation=params.animation,
                   compatibility_mode=params.compatibility_mode,
                   out_file=params.out_file,
                   asset_id=asset_id)


@create.command(name="from-text")
@click.pass_context
@click.option('--prompt',
              type=str, 
              required=True,
              help="Text prompt describing desired motion")
def create_from_text(
    ctx: click.Context,
    prompt: str
    ) -> None:
    """Create avatar with motion from text prompt."""
    api_instance_motions = client.SearchMotionsApi(ctx.obj["api_client"])
    api_instance_avatars = client.AvatarsApi(ctx.obj["api_client"])
    timeout = ctx.obj["config"]["cli"]["timeout"]

    motion = TMRMotion(prompt)

    # Search for motion by prompt and save temporary smpl file
    motion.find_motion(api_instance_motions)

    trimmed_motion = motion.trim()

    # Use found and trimmed motion .smpl file to create avatar
    uploader = Uploader()
    asset_id = from_smpl(trimmed_motion, api_instance_avatars, uploader, timeout)

    # Delete temporary motion .smpl file
    motion.cleanup()

    # Exit here if avatar should not be downloaded
    if ctx.obj["download"]:
        # Get download parameters from parent context
        params = get_export_parameters(ctx)
        # Export avatar
        ctx.invoke(export_and_download_avatar, 
                   format=params.download_format,
                   pose=params.pose,
                   animation=params.animation,
                   compatibility_mode=params.compatibility_mode,
                   out_file=params.out_file,
                   asset_id=asset_id)


@cli.command(name="batch-create")
@click.pass_context
@click.option('--options',
              type=click.Path(dir_okay=False),
              required=True,
              help="Path to options file. This file should contain a list of dictionaries, each containing the parameters for creating the avatars.")
@click.option('--input-dir',
              type=click.Path(dir_okay=True),
              required=True,
              callback=validate_batch_input_dir,
              help="Path to directory containing input files.")
@click.option('--output-dir',
              type=click.Path(dir_okay=True),
              required=True,
              help="Path to directory where to save the results to.")
def batch_create(
    ctx: click.Context,
    options: click.Path,
    input_dir: click.Path,
    output_dir: click.Path,
    ) -> None:
    """
    Create multiple avatars in batch mode. Please be aware that these commands cost credits.
    """
    # Read out batch options file
    batch_options = {}
    with open(options, "r") as f:
        batch_options = json.load(f)

    # Match batch mode to the correct function
    if batch_options.get("mode") is None:
        raise click.ClickException("Batch mode not specified")

    # Validate the process mode
    if PostgresqlBuildMethod(batch_options.get("mode").upper()) is None:
        raise click.ClickException("Invalid process mode")

    batch_options["timeout"] = ctx.obj["config"]["cli"]["timeout"]

    
    api_instance_user = client.UserApi(ctx.obj["api_client"])

    user = request_user_info(api_instance_user)

    # Read from constants the price of the batch creation for each file
    # TODO(dheid): Get the actual price for one alignment from the API and use that when that endpoint is available
    if user.credits < len(batch_options["data"]["input_files"]) * CREDIT_COSTS[batch_options.get("mode").upper()]:
        log.info(f"Insufficient credits for batch creation. Credits: {user.credits}. Still want to proceed?")
        if not click.confirm("Do you want to proceed?"):
            raise click.ClickException("Insufficient credits for batch creation")

    handle_batch_processing(ctx.obj["api_client"], batch_options, input_dir, output_dir)
    

@cli.command(name="download")
@click.pass_context
@click.option(
    "--format",
    type=click.Choice(["OBJ", "FBX"], case_sensitive=False),
    default="OBJ",
    help="Format for downloading avatar"
)
@click.option(
    "--pose",
    type=click.Choice(["T", "A", "SCAN", "U", "I", "W"], case_sensitive=False),
    default = "A",
    help="Pose the downloaded avatar should be in"
)
@click.option(
    "--animation",
    type=click.Choice(["a-salsa"], case_sensitive=False),
    help="Animation for the downloaded avatar"
)
@click.option(
    "--compatibility-mode",
    type=click.Choice(["DEFAULT", "OPTITEX", "UNREAL"], case_sensitive=False),
    help="Compatibility mode"
)
@click.option(
    "--out-file",
    type=click.Path(dir_okay=False),
    help="File to save created avatar mesh to"
)
@click.option(
    "--asset-id",
    type=str,
    help="Asset id of avatar to be downloaded"
)
@click.option(
    "--show-max-avatars",
    type=int,
    default=10,
    help="Maximum number of created avatars to show (most recent ones are shown first)"
)
def export_and_download_avatar(
    ctx: click.Context,
    format: str, 
    pose: str, 
    animation: str, 
    compatibility_mode: str, 
    out_file: click.Path,
    asset_id: str,
    show_max_avatars: int
    ) -> None:
    """
    Export avatar using asset id.
    """
    api_instance = client.AvatarsApi(ctx.obj["api_client"])
    name = None
    if asset_id is None:
        asset_id, name = select_asset_id(api_instance, show_max_avatars)

    # Export avatar
    timeout = ctx.obj["config"]["cli"]["timeout"]
    download_url = export(asset_id, format, pose, animation, compatibility_mode, api_instance, timeout)
    out_filename = str(out_file) if out_file is not None else \
        f"{get_timestamp()}_{name}.{format.lower()}" if (name is not None and name != "") else \
        f"{get_timestamp()}_{asset_id}.{format.lower()}"
    download_avatar(out_filename, download_url)
    log.info(f"Downloaded avatar to {out_filename}")

@cli.command()
@click.pass_context
def info(ctx: click.Context) -> None:
    """Show API info."""
    # Create an instance of the API class
    api_instance = client.InfoApi(ctx.obj["api_client"])

    try:
        # Show API info
        api_response: str = api_instance.info()
        log.info(api_response)
    except Exception as e:
        log.info("Exception when calling InfoApi->info: %s\n" % e)

@cli.command(name="user-info")
@click.pass_context
def user_info(ctx: click.Context) -> None:
    """Show username and available credits."""
    api_instance_user = client.UserApi(ctx.obj["api_client"])

    user = request_user_info(api_instance_user)

    log.info(f"Username: {user.email}")
    log.info(f"Credits: {user.credits}")
