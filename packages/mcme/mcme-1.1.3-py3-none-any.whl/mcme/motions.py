
import os
import tempfile

import click
from .helpers import Uploader
from .avatars import from_smpl
import requests
import openapi_client as client
from .logger import log
from openapi_client import PostgresqlBuildState as BuildState
from smplcodec import SMPLCodec
import dataclasses

motion_parameters = ["body_translation",
                    "body_pose",
                    "head_pose",
                    "left_hand_pose",
                    "right_hand_pose"]

class TMRMotion():
    """
    Temporary motion retrieved by text prompt using the /motions/search API endpoint.
    The motion can be found by text prompt and trimmed to the relevant frames, creating a temporary .smpl file.
    """

    def __init__(self,  prompt: str) -> None:
        """Initializing motion"""
        self.prompt = prompt


    def find_motion(self, api_instance: client.SearchMotionsApi) -> None:
        """Finding motion and downloading motion .smpl file as a temporary file"""
        motion_options = client.ServicesSearchMotionsOptions(
        num_motions=1,
        text=self.prompt)
        try:
            # Search for motion using prompt
            api_response = api_instance.submit_search_motions(motion_options)
        except Exception as e:
            raise click.ClickException("Exception when calling SearchMotionsApi->submit_search_motions: %s\n" % e) from e
        if api_response.data is None or api_response.data.attributes is None:
            raise click.ClickException("Searching for motion response came back empty")
        log.info(f"Creating motion from text finished with state {BuildState(api_response.data.attributes.state).name}")
        if api_response.included is None or \
            len(api_response.included) == 0 or \
            api_response.included[0] is None or \
            api_response.included[0].attributes is None or \
            api_response.data is None or \
            api_response.data.attributes is None or \
            api_response.data.attributes.result is None or \
            api_response.data.attributes.result.motions is None or \
            len(api_response.data.attributes.result.motions) == 0 or \
            api_response.data.attributes.result.motions[0] is None or \
            api_response.data.attributes.result.motions[0].start_time is None or \
            api_response.data.attributes.result.motions[0].end_time is None:
                raise click.ClickException("No motion found.")
        
        # Temporarily downloading motion .smpl file
        motion_download_url = api_response.included[0].attributes.url.path
        log.debug(f"Motion found: {api_response.data.attributes.result.motions[0].path_key}")
        with tempfile.NamedTemporaryFile(delete=False, suffix='.smpl') as file:
            self.file = file.name
            try:
                stream = requests.get(motion_download_url, stream=True, timeout=60)
                stream.raise_for_status()
            except requests.exceptions.HTTPError as err:
                raise click.ClickException(str(err)) from err
            for chunk in stream.iter_content(chunk_size=1024 * 1024):
                file.write(chunk)

        # Save start and end times of motion for later trimming
        self.start = api_response.data.attributes.result.motions[0].start_time
        self.end = api_response.data.attributes.result.motions[0].end_time


    def trim(self, start=None, end=None) -> str:
        """Trimming motion to relevant part as indicated in search motions response"""
        if start == None:
            start = self.start
        if end == None:
            end = self.end
        motion = SMPLCodec.from_file(self.file)

        # set original file as trimmed file if trimming is unnecessary
        if end == motion.frame_count/motion.frame_rate:
            log.debug("Motion trimming not necessary.")
            self.trimmed_file = self.file
            return self.trimmed_file
        
        # else, write trimmed temp file
        first_frame = int(start * motion.frame_rate)
        last_frame = int(end * motion.frame_rate)
        # update frame count to prevent smplcodec validation from failing
        setattr(motion, "frame_count", last_frame-first_frame)
        for attr in motion_parameters:
            if hasattr(motion, attr):
                frames = getattr(motion, attr)
                trimmed_frames = frames[first_frame:last_frame]
                setattr(motion,attr,trimmed_frames)
                
        
        temp = tempfile.NamedTemporaryFile(delete=False, suffix='_trimmed.smpl')
        try:
            self.trimmed_file = temp.name
            # remove codec_version since it is not compatible with the API (yet)
            del motion.__dataclass_fields__["codec_version"]
            motion.write(temp.name)
        finally:
            temp.close()
        return self.trimmed_file


    def cleanup(self):
        """"Deleting temporary .smpl file containing the downloaded motion"""
        os.remove(self.file)
        if os.path.isfile(self.trimmed_file):
            os.remove(self.trimmed_file)
