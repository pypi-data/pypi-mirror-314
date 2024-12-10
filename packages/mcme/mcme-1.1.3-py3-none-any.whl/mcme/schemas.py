from dataclasses import dataclass
from typing import Optional


@dataclass
class ExportParameters:
    """Class for defining export parameters."""
    download_format: str
    pose: str
    animation: str
    compatibility_mode: str
    out_file: str
