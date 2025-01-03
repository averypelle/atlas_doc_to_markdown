# -*- coding: utf-8 -*-

import typing as T
from rich import print as rprint

from ..paths import dir_project_root, dir_htmlcov
from ..vendor.pytest_cov_helper import (
    run_unit_test as _run_unit_test,
    run_cov_test as _run_cov_test,
)
from ..base import T_BASE


def run_unit_test(
    script: str,
):
    _run_unit_test(
        script=script,
        root_dir=f"{dir_project_root}",
    )


def run_cov_test(
    script: str,
    module: str,
    preview: bool = False,
    is_folder: bool = False,
):
    _run_cov_test(
        script=script,
        module=module,
        root_dir=f"{dir_project_root}",
        htmlcov_dir=f"{dir_htmlcov}",
        preview=preview,
        is_folder=is_folder,
    )


def check_seder(inst: T.Optional[T_BASE]):
    print("========== Check seder ==========")
    if inst is None:
        return
    print(f"---------- inst ----------")
    rprint(inst)
    data = inst.to_dict()
    print(f"---------- data ----------")
    rprint(data)
    inst1 = inst.from_dict(data)
    print(f"---------- inst1 ----------")
    rprint(inst1)
    assert inst1 == inst
    data1 = inst1.to_dict()
    print(f"---------- data1 ----------")
    rprint(data1)
    assert inst1.to_dict() == data1
