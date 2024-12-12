import os
import tempfile
from pathlib import Path

from .zipped_model import unzip_model


def decide_aimet_subtype(path: str) -> str:
    """
    Validate path (a directory) against .aimet format spec and decide whether
    it's ONNX or PT.

    Returns:
    - str: "onnx", "pt"
    """
    onnx_pt_files = [
        f for f in os.listdir(path) if f.endswith(".pt") or f.endswith(".onnx")
    ]
    if len(onnx_pt_files) != 1:
        raise ValueError(
            f".aimet path must contain exactly one .pt or .onnx file: {path}"
        )
    sub_suffix = Path(onnx_pt_files[0]).suffix
    return sub_suffix[1:]


def filepath_to_aimet_model_type(path: str) -> str:
    zip_path = None

    # Check inside to determine ONNX or PT AIMET.
    # cannot call _assert_is_valid_zipped_model which depends on this function
    if not os.path.isdir(path):
        # might come from .aimet.zip
        zip_path = path + ".zip"
        if not os.path.exists(zip_path):
            raise ValueError(f".aimet path must be a directory: {path}")
    if not zip_path:
        return decide_aimet_subtype(path)
    # need to unzip first
    with tempfile.TemporaryDirectory() as tempdir:
        unzip_model(zip_path, tempdir)
        # unzip_model confirms that there's only one directory under 'tempdir'
        subdir = next(os.scandir(tempdir)).name
        subdir_path = os.path.join(tempdir, subdir)
        return decide_aimet_subtype(subdir_path)
