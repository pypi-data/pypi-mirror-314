"""Convenience methods for parsing arguments to top-level methods"""

import json
import pathlib
import typing

import libcasm.clexulator as casmclex
import libcasm.configuration as casmconfig
import libcasm.xtal as xtal
from casm.bset.cluster_functions import (
    ClexBasisSpecs,
)


def as_Prim(
    x: typing.Union[xtal.Prim, casmconfig.Prim, dict, str, pathlib.Path],
) -> casmconfig.Prim:
    """Return input as a Prim instance

    Parameters
    ----------
    x: Union[libcasm.xtal.Prim, libcasm.configuration.Prim, dict, str, pathlib.Path]
        The prim, with symmetry information. May be provided as a Prim instance, a Prim
        dict, or the path to a file containing the Prim dict.

    Returns
    -------
    prim: libcasm.configuration.Prim
        The prim, with symmetry information.

    """
    if isinstance(x, (str, pathlib.Path)):
        with open(x, "r") as f:
            x = json.load(f)
    if isinstance(x, dict):
        x = casmconfig.Prim.from_dict(x)
    if isinstance(x, xtal.Prim):
        x = casmconfig.Prim(xtal_prim=x)
    if not isinstance(x, casmconfig.Prim):
        raise Exception("Error in as_Prim: failed")
    return x


def as_ClexBasisSpecs(
    x: typing.Union[ClexBasisSpecs, dict, str, pathlib.Path],
    prim: casmconfig.Prim,
) -> ClexBasisSpecs:
    """Return input as a ClexBasisSpecs instance

    Parameters
    ----------
    x: Union[casm.bset.cluster_functions.ClexBasisSpecs, dict, str, pathlib.Path]
        Parameters specifying the cluster orbits and basis function type and order. May
        be provided as a ClexBasisSpecs instance, a ClexBasisSpecs dict, or the path
        to a file containing a ClexBasisSpecs dict.
    prim: libcasm.configuration.Prim
        The prim, with symmetry information.

    Returns
    -------
    cluster_basis_specs: casm.bset.cluster_functions.ClexBasisSpecs
        The ClexBasisSpecs

    """
    if isinstance(x, (str, pathlib.Path)):
        print(x)
        with open(x, "r") as f:
            x = json.load(f)
    if isinstance(x, dict):
        x = ClexBasisSpecs.from_dict(x, prim=prim)
    if not isinstance(x, ClexBasisSpecs):
        raise Exception("Error in as_ClexBasisSpecs: failed")
    return x


def as_bset_dir(x: typing.Union[str, pathlib.Path, None] = None):
    """Return input as a Path

    Parameters
    ----------
    x: Union[pathlib.Path, str, None] = None
        The path to the basis set directory where the Clexulator and related files
        should be written. If None, the current working directory is used.

    Returns
    -------
    bset_dir: pathlib.Path
        The path to the basis set directory.
    """
    if x is None:
        x = pathlib.Path.cwd()
    x = pathlib.Path(x)
    return x


def as_PrimNeighborList(
    x: typing.Optional[casmclex.PrimNeighborList],
    prim: casmconfig.Prim,
):
    """Return input as a Path

    Parameters
    ----------
    x: Optional[PrimNeighborList]
        The :class:`PrimNeighborList` is used to uniquely index sites with local
        variables included in the cluster functions, relative to a reference unit cell.
        If None, a default neighbor list is constructed.
    prim: libcasm.configuration.Prim
        The prim, with symmetry information.

    Returns
    -------
    prim_neighbor_list: libcasm.clexulator.PrimNeighborList
        The PrimNeighborList.

    """
    if x is None:
        x = casmclex.make_default_prim_neighbor_list(xtal_prim=prim.xtal_prim)
    if not isinstance(x, casmclex.PrimNeighborList):
        raise Exception("Error in as_PrimNeighborList: failed")
    return x
