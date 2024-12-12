import json
import time
from pathlib import Path

import pytest

from cathodic_report import compress


@pytest.fixture
def tmp_folder():
    return Path("./tmp")


def test_report_compress(tmp_dir):
    with open(tmp_dir / "output.json", "r", encoding="utf-8") as f:
        output = json.load(f)

    filename = f"report-{int(time.time())}.spz"
    compress.compress_output(
        compress.forms.ReportOutput.model_validate(output),
        tmp_dir / filename,
    )

    assert (tmp_dir / filename).exists()

    compress.decompress_file(tmp_dir / filename, tmp_dir / "decompress")

    # remove the compressed file
    (tmp_dir / filename).unlink()


def test_compress(base_dir: Path, tmp_folder: Path):
    output_path = tmp_folder / "test.tar.xz"
    if not tmp_folder.exists():
        tmp_folder.mkdir(parents=True)

    try:
        compress.compress_folder(base_dir, str(output_path))
        assert output_path.exists()

    finally:
        # clean up
        if output_path.exists():
            output_path.unlink()
