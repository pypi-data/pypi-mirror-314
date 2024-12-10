"""
compress folder to an xz file
"""

import lzma
import os
import tarfile
from pathlib import Path

from .output import forms


def decompress_file(filename: Path, output_dir: Path):
    """
    将压缩文件解压到指定目录

    Args:
        filename (Path): 压缩文件路径
        output_dir (Path): 解压目标目录

    Returns:
        None
    """
    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)

    # 解压文件
    with tarfile.open(filename, mode="r:xz") as tar:
        tar.extractall(path=output_dir)


def compress_folder(folder_path: str, output_path: str):
    """
    将指定文件夹压缩为 xz 格式的文件

    Args:
        folder_path (str): 要压缩的文件夹路径
        output_path (str): 输出的 xz 文件路径

    Returns:
        None
    """
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"文件夹不存在: {folder_path}")

    # # 确保输出路径以 .tar.xz 结尾
    # if not output_path.endswith(".tar.xz"):
    #     output_path += ".tar.xz"

    # 创建 tar.xz 文件
    with tarfile.open(output_path, mode="w:xz", preset=9) as tar:
        # 添加文件夹中的所有内容
        tar.add(folder_path, arcname=os.path.basename(folder_path))


def compress_output(report: forms.ReportOutput, output_path: Path | str):
    import os
    import tarfile

    with tarfile.open(output_path, mode="w:xz", preset=9) as tar:

        def add_to_tar(name):
            tar.add(
                name,
                arcname=os.path.basename(name),
            )

        add_to_tar(report.header.beginning)
        add_to_tar(report.header.summary_table)
        add_to_tar(report.header.graph)
        for device in report.devices:
            add_to_tar(device.header)
            for table in device.tables:
                add_to_tar(table)
            add_to_tar(device.graph)
