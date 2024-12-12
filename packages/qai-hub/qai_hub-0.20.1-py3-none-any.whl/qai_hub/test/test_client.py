import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

import qai_hub.public_api_pb2 as api_pb
from qai_hub import SourceModelType
from qai_hub.client import (
    Client,
    Device,
    UserError,
    _assert_is_valid_zipped_model,
    _make_zipped_model_compatible,
    _profile_pb_to_python_dict,
)


def create_sample_mlmodelc(modelDir: Path, include_assemble_json: bool = False):
    Path(modelDir).mkdir(parents=True)
    Path(modelDir / "model.espresso.net").touch()
    Path(modelDir / "model.espresso.shape").touch()
    Path(modelDir / "model.espresso.weights").touch()
    if include_assemble_json:
        Path(modelDir / "assemble.json").touch()


def test_valid_zipped_mlmodelc():
    #  1. <filepath>/foo.mlmodelc/assemble.json in case of pipeline model
    #  2. <filepath>/foo.mlmodelc/model.espresso.net or
    #  3. <filepath>/foo.mlmodelc/model0/model.espresso.net in case of pipeline model

    mlmodelc_name = "myModel.mlmodelc"
    # Case 1:
    with tempfile.TemporaryDirectory(suffix="baseDir") as baseDir:
        modelDir = Path(baseDir) / mlmodelc_name
        create_sample_mlmodelc(modelDir, include_assemble_json=True)

        zipPath = Path(baseDir) / "my_model_archive"
        shutil.make_archive(
            str(zipPath), "zip", root_dir=baseDir, base_dir=mlmodelc_name
        )
        _assert_is_valid_zipped_model(f"{zipPath}.zip")

    # Case 2
    with tempfile.TemporaryDirectory(suffix="baseDir") as baseDir:
        modelDir = Path(baseDir) / mlmodelc_name
        create_sample_mlmodelc(modelDir)

        zipPath = Path(baseDir) / "my_model_archive"
        shutil.make_archive(
            str(zipPath), "zip", root_dir=baseDir, base_dir=mlmodelc_name
        )
        _assert_is_valid_zipped_model(f"{zipPath}.zip")

    # Case 3
    with tempfile.TemporaryDirectory(suffix="baseDir") as baseDir:
        modelDir = Path(baseDir) / "myModel.mlmodelc"
        pipelinePath = Path(modelDir) / "model0"
        create_sample_mlmodelc(pipelinePath)

        zipPath = Path(baseDir) / "my_model_archive"
        shutil.make_archive(
            str(zipPath), "zip", root_dir=baseDir, base_dir=mlmodelc_name
        )
        _assert_is_valid_zipped_model(f"{zipPath}.zip")

    # Unsupported: model.espresso.net / assemble.json present
    # with flat directory structure i.e. model.zip -> model.espresso.net
    with tempfile.TemporaryDirectory(suffix="baseDir") as baseDir:
        modelDir = Path(baseDir) / mlmodelc_name
        create_sample_mlmodelc(modelDir, include_assemble_json=True)

        zipPath = Path(baseDir) / "my_model_archive"
        shutil.make_archive(str(zipPath), "zip", root_dir=modelDir, base_dir="./")
        with pytest.raises(UserError):
            _assert_is_valid_zipped_model(f"{zipPath}.zip")

    # Valid .mlmodelc within zip with no model.espresso.net/assemble.json
    with tempfile.TemporaryDirectory(suffix="baseDir") as baseDir:
        # Make an invalid model
        modelDir = Path(baseDir) / mlmodelc_name
        Path(modelDir).mkdir()
        Path(modelDir / "bad_file").touch()

        # Check that this fails
        zipPath = Path(baseDir) / "my_model_archive"
        shutil.make_archive(
            str(zipPath), "zip", root_dir=baseDir, base_dir=mlmodelc_name
        )
        with pytest.raises(UserError):
            _assert_is_valid_zipped_model(f"{zipPath}.zip")


def test_valid_zipped_mlpackage():
    # <dirpath>/foo.mlpackage/ in case of zipped mlpackage

    mlpackage_name = "myModel.mlpackage"
    with tempfile.TemporaryDirectory(suffix="baseDir") as baseDir:
        modelDir = Path(baseDir) / mlpackage_name
        os.makedirs(modelDir)

        zipPath = Path(baseDir) / "my_model_archive"
        shutil.make_archive(
            str(zipPath), "zip", root_dir=baseDir, base_dir=mlpackage_name
        )
        _assert_is_valid_zipped_model(f"{zipPath}.zip")


def test_make_mlmodelc_compatible_zip_does_not_zip_zip():
    model_name = "myModel.mlmodelc"
    with tempfile.TemporaryDirectory(suffix="baseDir") as base_dir:
        model_dir = Path(base_dir) / model_name
        create_sample_mlmodelc(model_dir)

        zip_base_path = Path(base_dir) / "my_model_archive"
        zip_path = shutil.make_archive(
            str(zip_base_path), "zip", root_dir=base_dir, base_dir=model_name
        )

        with tempfile.NamedTemporaryFile(suffix=".mlmodelc.zip") as model_zip_tempfile:
            mlmodelc_zip_path = _make_zipped_model_compatible(
                zip_path, model_zip_tempfile.name, ".mlmodelc"
            )
            assert mlmodelc_zip_path == zip_path


def test_make_mlmodelc_compatible_zip_zips_dir():
    with tempfile.TemporaryDirectory(suffix="baseDir") as base_dir:
        model_dir = Path(base_dir) / "myModel.mlmodelc"
        create_sample_mlmodelc(model_dir)

        model_output_path = str(Path(base_dir, "output_model_dir"))
        os.makedirs(model_output_path)
        zipfile_path = _make_zipped_model_compatible(
            str(model_dir), model_output_path, ".mlmodelc"
        )
        assert zipfile_path == os.path.join(model_output_path, "myModel.mlmodelc.zip")
        _assert_is_valid_zipped_model(zipfile_path)


def test_make_mlmodelc_compatible_zip_zips_dir_removing_additional_dirs():
    with tempfile.TemporaryDirectory(suffix="baseDir") as base_dir:
        model_dir = Path(base_dir) / "myModel.mlmodelc"
        create_sample_mlmodelc(model_dir)
        Path(os.path.join(base_dir, "__MACOS__")).mkdir(parents=True)
        Path(os.path.join(base_dir, "some_random_file")).touch()

        zipped_file_path = shutil.make_archive(
            os.path.join(base_dir, "test_model.mlmodelc"), "zip", root_dir=base_dir
        )
        with tempfile.TemporaryDirectory() as tmp_dir:
            zipfile_path = _make_zipped_model_compatible(
                zipped_file_path, tmp_dir, ".mlmodelc"
            )
            assert zipfile_path == str(os.path.join(tmp_dir, "myModel.mlmodelc.zip"))
            _assert_is_valid_zipped_model(zipfile_path)


@pytest.mark.parametrize(
    "framework, os_type, os_version, model_type, supported",
    [
        # .pt supported on all devices
        ("framework:coreml", "os:macos", "12.1", SourceModelType.TORCHSCRIPT, True),
        ("framework:tflite", "os:macos", "12.1", SourceModelType.TORCHSCRIPT, True),
        ("framework:onnx", "os:macos", "12.1", SourceModelType.TORCHSCRIPT, True),
        ("framework:coreml", "os:ios", "15.1", SourceModelType.TORCHSCRIPT, True),
        ("framework:tflite", "os:ios", "15.1", SourceModelType.TORCHSCRIPT, True),
        ("framework:onnx", "os:ios", "15.1", SourceModelType.TORCHSCRIPT, True),
        ("framework:tflite", "os:android", "10.", SourceModelType.TORCHSCRIPT, True),
        ("framework:onnx", "os:android", "10.1", SourceModelType.TORCHSCRIPT, True),
        # .mlpackage is supported only on iOS15+ and macOS12+
        ("framework:coreml", "os:macos", "12.1", SourceModelType.MLPACKAGE, True),
        ("framework:coreml", "os:macos", "11.1", SourceModelType.MLPACKAGE, False),
        ("framework:coreml", "os:ios", "15.1", SourceModelType.MLPACKAGE, True),
        ("framework:coreml", "os:ios", "13.1", SourceModelType.MLPACKAGE, False),
        ("framework:tflite", "os:android", "10.", SourceModelType.MLPACKAGE, False),
        ("framework:onnx", "os:android", "10.1", SourceModelType.MLPACKAGE, False),
        # .mlmodel is supported only on iOS and macOS
        ("framework:coreml", "os:macos", "12.1", SourceModelType.MLMODEL, True),
        ("framework:coreml", "os:ios", "15.1", SourceModelType.MLMODEL, True),
        ("framework:onnx", "os:macos", "12.1", SourceModelType.MLMODEL, False),
        ("framework:tflite", "os:ios", "15.1", SourceModelType.MLMODEL, False),
        ("framework:tflite", "os:android", "10.", SourceModelType.MLMODEL, False),
        ("framework:onnx", "os:android", "10.1", SourceModelType.MLMODEL, False),
        # .mlmodelc is supported only on iOS and macOS
        ("framework:coreml", "os:macos", "12.1", SourceModelType.MLMODELC, True),
        ("framework:coreml", "os:ios", "15.1", SourceModelType.MLMODELC, True),
        ("framework:tflite", "os:android", "10.", SourceModelType.MLMODELC, False),
        ("framework:onnx", "os:android", "10.1", SourceModelType.MLMODELC, False),
        # .onnx is supported with ONNX runtime on Android
        ("framework:coreml", "os:macos", "12.1", SourceModelType.ONNX, False),
        ("framework:coreml", "os:ios", "15.1", SourceModelType.ONNX, False),
        ("framework:tflite", "os:macos", "12.1", SourceModelType.ONNX, False),
        ("framework:tflite", "os:ios", "15.1", SourceModelType.ONNX, False),
        # supported only for compile jobs with tflite
        ("framework:tflite", "os:android", "10.", SourceModelType.ONNX, False),
        ("framework:onnx", "os:android", "10.1", SourceModelType.ONNX, True),
        ("framework:onnx", "os:windows", "11", SourceModelType.ONNX, True),
        # .ort is supported with ONNX runtime
        ("framework:coreml", "os:macos", "12.1", SourceModelType.ORT, False),
        ("framework:coreml", "os:ios", "15.1", SourceModelType.ORT, False),
        ("framework:tflite", "os:macos", "12.1", SourceModelType.ORT, False),
        ("framework:tflite", "os:ios", "15.1", SourceModelType.ORT, False),
        ("framework:tflite", "os:android", "10.", SourceModelType.ORT, False),
        ("framework:onnx", "os:android", "10.1", SourceModelType.ORT, True),
        ("framework:onnx", "os:windows", "11", SourceModelType.ORT, True),
        # .tflite is supported with tflite framework
        ("framework:coreml", "os:macos", "12.1", SourceModelType.TFLITE, False),
        ("framework:coreml", "os:ios", "15.1", SourceModelType.TFLITE, False),
        ("framework:tflite", "os:macos", "12.1", SourceModelType.TFLITE, True),
        ("framework:tflite", "os:ios", "15.1", SourceModelType.TFLITE, True),
        ("framework:tflite", "os:android", "10.", SourceModelType.TFLITE, True),
        ("framework:onnx", "os:android", "10.1", SourceModelType.TFLITE, False),
        ("framework:onnx", "os:windows", "11", SourceModelType.TFLITE, False),
        (
            "framework:qnn",
            "os:windows",
            "11",
            SourceModelType.QNN_LIB_AARCH64_ANDROID,
            False,
        ),
    ],
)
def test_model_type_device_check(
    framework, os_type, os_version, model_type, supported, monkeypatch
):
    device = Device(attributes=[framework, os_type], os=os_version)
    monkeypatch.setattr(
        Client,
        "_get_device",
        MagicMock(return_value=device),
    )

    client = Client()
    if supported:
        client._check_devices(device, model_type)
    else:
        with pytest.raises(UserError, match=".*does not support.*"):
            client._check_devices(device, model_type)


def test_profile_pb_to_python_dict():
    profile_pb = api_pb.ProfileDetail()

    profile_pb.major_version = 1
    profile_pb.minor_version = 8

    profile_pb.execution_time = 3652
    profile_pb.after_execution_peak_memory = 166711296
    profile_pb.cold_load_time = 1374293
    profile_pb.after_cold_load_peak_memory = 166711296
    profile_pb.warm_load_time = 277823
    profile_pb.after_warm_load_peak_memory = 163520512
    profile_pb.compile_time = 0
    profile_pb.after_compile_peak_memory = 0

    profile_pb.compile_memory.increase.lower = 0
    profile_pb.compile_memory.increase.upper = 0
    profile_pb.compile_memory.peak.lower = 0
    profile_pb.compile_memory.peak.upper = 0

    profile_pb.cold_load_memory.increase.lower = 72258864
    profile_pb.cold_load_memory.increase.upper = 82031840
    profile_pb.cold_load_memory.peak.lower = 98230272
    profile_pb.cold_load_memory.peak.upper = 108003248

    profile_pb.warm_load_memory.increase.lower = 0
    profile_pb.warm_load_memory.increase.upper = 0
    profile_pb.warm_load_memory.peak.lower = 118784
    profile_pb.warm_load_memory.peak.upper = 43225712

    profile_pb.execution_memory.increase.lower = 0
    profile_pb.execution_memory.increase.upper = 2658496
    profile_pb.execution_memory.peak.lower = 2654208
    profile_pb.execution_memory.peak.upper = 39406752

    profile_pb.all_compile_times.append(1)
    profile_pb.all_cold_load_times.append(1374293)
    profile_pb.all_warm_load_times.append(277823)
    profile_pb.all_execution_times.append(10003)
    profile_pb.all_execution_times.append(4205)

    profile_pb.segment_details.append(
        api_pb.SegmentDetail(
            id=":0:75",
            compute_unit=api_pb.COMPUTE_UNIT_CPU,
            delegate_name="XNNPACK",
            execution_time=109,
        )
    )
    profile_pb.segment_details.append(
        api_pb.SegmentDetail(
            id=":0:73",
            compute_unit=api_pb.COMPUTE_UNIT_NPU,
            delegate_name="QNN",
            delegate_extra_info="HTP",
            execution_time=473,
        )
    )

    profile_pb.layer_details.append(
        api_pb.LayerDetail(
            name="model/tf.math.divide/truediv",
            compute_unit=api_pb.COMPUTE_UNIT_CPU,
            layer_type_name="MUL",
            id=":0:1",
            delegate_name="XNNPACK",
            execution_time=23,
            segment_id=":0:75",
            delegate_reported_ops="Multiply (ND, F32)",
        )
    )
    profile_pb.layer_details.append(
        api_pb.LayerDetail(
            name="model/tf.compat.v1.transpose/transpose",
            compute_unit=api_pb.COMPUTE_UNIT_NPU,
            layer_type_name="TRANSPOSE",
            id=":0:2",
            delegate_name="QNN",
            delegate_extra_info="HTP",
            execution_time=127,
            segment_id=":0:73",
            delegate_reported_ops="Transpose",
            execution_cycles=180315,
        )
    )

    expected = {
        "execution_summary": {
            "estimated_inference_time": 3652,
            "estimated_inference_peak_memory": 166711296,
            "first_load_time": 1374293,
            "first_load_peak_memory": 166711296,
            "warm_load_time": 277823,
            "warm_load_peak_memory": 163520512,
            "compile_time": 0,
            "compile_peak_memory": 0,
            "compile_memory_increase_range": (0, 0),
            "compile_memory_peak_range": (0, 0),
            "first_load_memory_increase_range": (72258864, 82031840),
            "first_load_memory_peak_range": (98230272, 108003248),
            "warm_load_memory_increase_range": (0, 0),
            "warm_load_memory_peak_range": (118784, 43225712),
            "inference_memory_increase_range": (0, 2658496),
            "inference_memory_peak_range": (2654208, 39406752),
            "all_compile_times": [1],
            "all_first_load_times": [1374293],
            "all_inference_times": [10003, 4205],
            "all_warm_load_times": [277823],
        },
        "execution_detail": [
            {
                "compute_unit": "CPU",
                "execution_time": 23,
                "name": "model/tf.math.divide/truediv",
                "type": "MUL",
            },
            {
                "compute_unit": "NPU",
                "execution_cycles": 180315,
                "execution_time": 127,
                "name": "model/tf.compat.v1.transpose/transpose",
                "type": "TRANSPOSE",
            },
        ],
    }

    actual = _profile_pb_to_python_dict(profile_pb)

    assert expected == actual
