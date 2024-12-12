import json

import numpy as np
from utils.helpers import (
    assert_expected_cluster_functions_detailed,
)

import libcasm.xtal as xtal
from casm.bset import (
    build_cluster_functions,
)


def test_composition_occ_fcc_1a(session_shared_datadir):
    """Baseline test - composition basis functions

    To be compared with test_occ_fcc_1b,
    where the occupants on i_sublat=2 are ordered differently.
    """

    xtal_prim = xtal.Prim(
        lattice=xtal.Lattice(
            column_vector_matrix=np.eye(3),
        ),
        coordinate_frac=np.array(
            [
                [0.0, 0.0, 0.0],
                [0.0, 0.5, 0.5],
                [0.5, 0.0, 0.5],
                [0.5, 0.5, 0.0],
            ]
        ).T,
        occ_dof=[
            ["A", "B"],
            ["B", "C"],
            ["B", "C"],
            ["B", "C"],
        ],
    )
    # print(xtal.pretty_json(xtal_prim.to_dict()))

    builder = build_cluster_functions(
        prim=xtal_prim,
        clex_basis_specs={
            "cluster_specs": {
                "orbit_branch_specs": {
                    "2": {"max_length": 1.01},
                    "3": {"max_length": 1.01},
                },
            },
            "basis_function_specs": {
                "dof_specs": {
                    "occ": {
                        "site_basis_functions": [
                            {
                                "sublat_indices": [0],
                                "composition": {"A": 0.25, "B": 0.75},
                            },
                            {
                                "sublat_indices": [1],
                                "composition": {"C": 0.25, "B": 0.75},
                            },
                        ]
                    }
                }
            },
        },
        verbose=False,
    )
    functions, clusters = (builder.functions, builder.clusters)

    _occ_site_functions = builder.occ_site_functions.copy()
    print(xtal.pretty_json(_occ_site_functions))

    for b in [0]:
        expected = np.array(
            [
                [1.0, 1.0],
                [1.1338934190276813, -0.37796447300922736],
            ]
        )
        assert np.allclose(builder.occ_site_functions[b]["value"], expected)

    for b in [1, 2, 3]:
        expected = np.array(
            [
                [1.0, 1.0],
                [-0.37796447300922736, 1.1338934190276813],
            ]
        )
        assert np.allclose(builder.occ_site_functions[b]["value"], expected)

    # import os
    # import pathlib
    # from utils.helpers import print_expected_cluster_functions_detailed
    #
    # print_expected_cluster_functions_detailed(
    #     functions,
    #     file=pathlib.Path(os.path.realpath(__file__)).parent
    #     / "data"
    #     / "expected_occ_site_functions_fcc_1_composition.json",
    # )
    with open(
        session_shared_datadir / "expected_occ_site_functions_fcc_1_composition.json"
    ) as f:
        assert_expected_cluster_functions_detailed(functions, clusters, json.load(f))


def test_composition_occ_fcc_1b(session_shared_datadir):
    """Change order of occupants on i_sublat=2

    This affects the site basis function (phi) values on that sublattice,
    but the generated functions are the same
    (because they are functions of the phi which remain in the same order).
    """
    xtal_prim = xtal.Prim(
        lattice=xtal.Lattice(
            column_vector_matrix=np.eye(3),
        ),
        coordinate_frac=np.array(
            [
                [0.0, 0.0, 0.0],
                [0.0, 0.5, 0.5],
                [0.5, 0.0, 0.5],
                [0.5, 0.5, 0.0],
            ]
        ).T,
        occ_dof=[
            ["A", "B"],
            ["B", "C"],
            ["C", "B"],
            ["B", "C"],
        ],
    )
    # print(xtal.pretty_json(xtal_prim.to_dict()))

    builder = build_cluster_functions(
        prim=xtal_prim,
        clex_basis_specs={
            "cluster_specs": {
                "orbit_branch_specs": {
                    "2": {"max_length": 1.01},
                    "3": {"max_length": 1.01},
                },
            },
            "basis_function_specs": {
                "dof_specs": {
                    "occ": {
                        "site_basis_functions": [
                            {
                                "sublat_indices": [0],
                                "composition": {"A": 0.25, "B": 0.75},
                            },
                            {
                                "sublat_indices": [1],
                                "composition": {"C": 0.25, "B": 0.75},
                            },
                        ]
                    }
                }
            },
        },
        verbose=False,
    )
    functions, clusters = (builder.functions, builder.clusters)

    _occ_site_functions = builder.occ_site_functions.copy()
    print(xtal.pretty_json(_occ_site_functions))

    for b in [0, 2]:
        expected = np.array(
            [
                [1.0, 1.0],
                [1.1338934190276813, -0.37796447300922736],
            ]
        )
        assert np.allclose(builder.occ_site_functions[b]["value"], expected)

    for b in [1, 3]:
        expected = np.array(
            [
                [1.0, 1.0],
                [-0.37796447300922736, 1.1338934190276813],
            ]
        )
        assert np.allclose(builder.occ_site_functions[b]["value"], expected)

    ## Compare to functions generated in test 1a ##

    # import os
    # import pathlib
    # from utils.helpers import print_expected_cluster_functions_detailed
    #
    # print_expected_cluster_functions_detailed(
    #     functions,
    #     file=pathlib.Path(os.path.realpath(__file__)).parent
    #     / "data"
    #     / "expected_occ_site_functions_fcc_1_composition.json",
    # )
    with open(
        session_shared_datadir / "expected_occ_site_functions_fcc_1_composition.json"
    ) as f:
        assert_expected_cluster_functions_detailed(functions, clusters, json.load(f))
