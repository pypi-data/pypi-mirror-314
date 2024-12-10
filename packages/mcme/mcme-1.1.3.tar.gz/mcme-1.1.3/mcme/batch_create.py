import os
import click

from .logger import log
import openapi_client as client
from openapi_client.models.postgresql_build_method import PostgresqlBuildMethod

from .avatars import from_video, from_images, from_scans, export
from .helpers import LocalUploader, download_avatar, get_timestamp

def validate_batch_input_dir(ctx, param, value) -> bool:
    """
    Validate the input directory for batch create.
    - Check if the directory has more than one file
    """
    if not os.path.isdir(value):
        raise click.BadParameter("Input directory does not exist")
    
    if len(os.listdir(value)) < 1:
        raise click.BadParameter("Input directory does not have enough files")

    return value

def handle_batch_processing(api_client, batch_options_js, input_dir: str, output_dir: str):
    """
    Create batch of avatars from files.
    """
    log.info(f"Creating batch of avatars from files in {input_dir}")
    input_file_path = os.path.join(input_dir, "input.mp4")

    missing_files_handle = open(os.path.join(output_dir, "missing_files.txt"), "a")
    errored_processes = []

    # Iterate through batch_options_js["data"]["input_files"]
    # Read out "filename" and look for the file in the input directory
    # If the file is found, create the avatar
    for file in batch_options_js["data"]["input_files"]:
        file_name = file["filename"]
        input_file_path = os.path.join(input_dir, file_name)

        # Check if the file exists
        if not os.path.exists(input_file_path):
            log.warn(f"File {input_file_path} does not exist")
            missing_files_handle.write(f"{input_file_path}\n")
            continue

        # Create avatar
        avatar_id = get_processor(batch_options_js["mode"], input_file_path, file["parameters"], api_client, batch_options_js["timeout"])

        # TODO(dheid)
        # Make download and export configurable to be also running in parallel
        avatar_client = client.AvatarsApi(api_client)
        if file.get("export_parameters"):
            format = file["export_parameters"]["format"]
            pose = file["export_parameters"].get("pose")
            download_url = export(avatar_id, format, file["export_parameters"]["pose"], file["export_parameters"]["animation"], "default", avatar_client, batch_options_js["timeout"])
            out_filename = os.path.join(output_dir, f"{get_timestamp()}_{file_name}.{format.lower()}")
            download_avatar(out_filename, download_url)


    if errored_processes:
        log.info(f"Writing list of errored processes to {output_dir}")
        with open(os.path.join(output_dir, "errored_processes.txt"), "w") as f:
            f.write("\n".join(errored_processes))

    missing_files_handle.close()


def get_processor(mode, input_file_path: str, params: dict, api_client, timeout) -> str:
    """
    Get the function to create avatar based on mode.
    """
    avatar_client = client.AvatarsApi(api_client)
    uploader = LocalUploader()
    mode = mode.lower()

    params["avatarname"] = os.path.basename(input_file_path).split(".")[0]

    log.info(f"Creating avatar with mode {mode}")
    if mode.upper() == PostgresqlBuildMethod.FROM_VIDEO.value:
        from_video_client = client.CreateAvatarFromVideoApi(api_client)
        return from_video(params["gender"], params["avatarname"], input_file_path, from_video_client, avatar_client, uploader, timeout)
    else:
        raise NotImplementedError(f"Mode {mode} is not implemented")




