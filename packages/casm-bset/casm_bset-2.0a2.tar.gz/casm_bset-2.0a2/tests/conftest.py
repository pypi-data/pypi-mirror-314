import os
import pathlib
import shutil
import sys

import numpy as np
import pytest

import libcasm.xtal as xtal

# Pytest will rewrite assertions in test modules, but not elsewhere.
# This tells pytest to also rewrite assertions in utils/helpers.py.
#
pytest.register_assert_rewrite("utils.helpers")


def _win32_longpath(path):
    """
    Helper function to add the long path prefix for Windows, so that shutil.copytree
     won't fail while working with paths with 255+ chars.
    """
    if sys.platform == "win32":
        # The use of os.path.normpath here is necessary since "the "\\?\" prefix
        # to a path string tells the Windows APIs to disable all string parsing
        # and to send the string that follows it straight to the file system".
        # (See https://docs.microsoft.com/pt-br/windows/desktop/FileIO/naming-a-file)
        return "\\\\?\\" + os.path.normpath(path)
    else:
        return path


@pytest.fixture(scope="session")
def session_shared_datadir(tmpdir_factory):
    original_shared_path = pathlib.Path(os.path.realpath(__file__)).parent / "data"
    session_temp_path = tmpdir_factory.mktemp("session_data")
    shutil.copytree(
        _win32_longpath(original_shared_path),
        _win32_longpath(str(session_temp_path)),
        dirs_exist_ok=True,
    )
    return session_temp_path


@pytest.fixture
def lowsym_Hstrain_prim():
    return xtal.Prim(
        lattice=xtal.Lattice(
            np.array(
                [
                    [1.0, 0.3, 0.4],  # a
                    [0.0, 1.2, 0.5],  # b
                    [0.0, 0.0, 1.4],  # c
                ]
            ).transpose()
        ),
        coordinate_frac=np.array(
            [
                [0.0, 0.0, 0.0],
                [0.4, 0.5, 0.6],
                [0.24, 0.25, 0.23],
            ]
        ).transpose(),
        occ_dof=[["A"], ["A"], ["A"]],
        global_dof=[xtal.DoFSetBasis("Hstrain")],
    )


@pytest.fixture
def lowsym_disp_prim():
    return xtal.Prim(
        lattice=xtal.Lattice(
            np.array(
                [
                    [1.0, 0.3, 0.4],  # a
                    [0.0, 1.2, 0.5],  # b
                    [0.0, 0.0, 1.4],  # c
                ]
            ).transpose()
        ),
        coordinate_frac=np.array(
            [
                [0.0, 0.0, 0.0],
                [0.4, 0.5, 0.6],
                [0.24, 0.25, 0.23],
            ]
        ).transpose(),
        occ_dof=[["A"], ["A"], ["A"]],
        local_dof=[
            [xtal.DoFSetBasis("disp")],
            [xtal.DoFSetBasis("disp")],
            [xtal.DoFSetBasis("disp")],
        ],
    )


@pytest.fixture
def lowsym_occ_prim():
    return xtal.Prim(
        lattice=xtal.Lattice(
            np.array(
                [
                    [1.0, 0.3, 0.4],  # a
                    [0.0, 1.2, 0.5],  # b
                    [0.0, 0.0, 1.4],  # c
                ]
            ).transpose()
        ),
        coordinate_frac=np.array(
            [
                [0.0, 0.0, 0.0],
                [0.4, 0.5, 0.6],
                [0.24, 0.25, 0.23],
            ]
        ).transpose(),
        occ_dof=[["A", "B"], ["A", "B"], ["A", "B"]],
    )


@pytest.fixture
def lowsym_Hstrain_disp_prim():
    return xtal.Prim(
        lattice=xtal.Lattice(
            np.array(
                [
                    [1.0, 0.3, 0.4],  # a
                    [0.0, 1.2, 0.5],  # b
                    [0.0, 0.0, 1.4],  # c
                ]
            ).transpose()
        ),
        coordinate_frac=np.array(
            [
                [0.0, 0.0, 0.0],
                [0.4, 0.5, 0.6],
                [0.24, 0.25, 0.23],
            ]
        ).transpose(),
        occ_dof=[["A"], ["A"], ["A"]],
        local_dof=[
            [xtal.DoFSetBasis("disp")],
            [xtal.DoFSetBasis("disp")],
            [xtal.DoFSetBasis("disp")],
        ],
        global_dof=[xtal.DoFSetBasis("Hstrain")],
    )
