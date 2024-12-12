import json

import numpy as np
from utils.helpers import (
    assert_expected_cluster_functions_detailed,
    make_discrete_magnetic_atom,
)

import libcasm.configuration as casmconfig
import libcasm.xtal as xtal
from casm.bset import (
    build_cluster_functions,
)
from casm.bset.cluster_functions import (
    get_occ_site_functions,
)


def test_occ_fcc_1a(session_shared_datadir):
    """Baseline test - occupation basis functions

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
                "dof_specs": {"occ": {"site_basis_functions": "occupation"}}
            },
        },
        verbose=False,
    )
    functions, clusters = (builder.functions, builder.clusters)

    _occ_site_functions = builder.occ_site_functions.copy()
    print(xtal.pretty_json(_occ_site_functions))

    for b in [0, 1, 2, 3]:
        expected = np.array(
            [
                [1.0, 1.0],
                [0.0, 1.0],
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
    #     / "expected_occ_site_functions_fcc_1.json",
    # )
    with open(session_shared_datadir / "expected_occ_site_functions_fcc_1.json") as f:
        assert_expected_cluster_functions_detailed(functions, clusters, json.load(f))


def test_occ_fcc_1b(session_shared_datadir):
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
                "dof_specs": {"occ": {"site_basis_functions": "occupation"}}
            },
        },
        verbose=False,
    )
    functions, clusters = (builder.functions, builder.clusters)

    _occ_site_functions = builder.occ_site_functions.copy()
    print(xtal.pretty_json(_occ_site_functions))

    for b in [0, 1, 3]:
        expected = np.array(
            [
                [1.0, 1.0],
                [0.0, 1.0],
            ]
        )
        assert np.allclose(builder.occ_site_functions[b]["value"], expected)

    for b in [2]:
        expected = np.array(
            [
                [1.0, 1.0],
                [1.0, 0.0],
            ]
        )
        assert np.allclose(builder.occ_site_functions[b]["value"], expected)

    ## Compare to functions generated in test 1a ##

    # print_expected_cluster_functions_detailed(
    #     functions,
    #     file=pathlib.Path(os.path.realpath(__file__)).parent
    #     / "data"
    #     / "expected_occ_site_functions_fcc_1b.json",
    # )
    with open(session_shared_datadir / "expected_occ_site_functions_fcc_1.json") as f:
        assert_expected_cluster_functions_detailed(functions, clusters, json.load(f))


def test_occ_fcc_2a(session_shared_datadir):
    """Baseline test - ternary occupation basis functions

    To be compared with test_occ_fcc_2b,
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
            ["B", "C", "D"],
            ["B", "C", "D"],
            ["B", "C", "D"],
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
                "dof_specs": {"occ": {"site_basis_functions": "occupation"}}
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
                [0.0, 1.0],
            ]
        )
        assert np.allclose(builder.occ_site_functions[b]["value"], expected)

    for b in [1, 2, 3]:
        expected = np.array(
            [
                [1.0, 1.0, 1.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
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
    #     / "expected_occ_site_functions_fcc_2.json",
    # )
    with open(session_shared_datadir / "expected_occ_site_functions_fcc_2.json") as f:
        assert_expected_cluster_functions_detailed(functions, clusters, json.load(f))


def test_occ_fcc_2b(session_shared_datadir):
    """Change order of occupants

    This affects the site basis function (phi) values on that sublattice,
    but the generated functions are the same as test_occ_fcc_2a
    (because they are functions of the phi which remain in the same order).
    """

    occ_dof = [
        ["A", "B"],
        ["B", "C", "D"],
        ["B", "D", "C"],
        ["C", "D", "B"],
    ]
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
        occ_dof=occ_dof,
    )
    prim = casmconfig.Prim(xtal_prim)
    occ_symgroup_rep = prim.occ_symgroup_rep

    for i_factor_group, occ_op_rep in enumerate(occ_symgroup_rep):
        site_rep = prim.integral_site_coordinate_symgroup_rep[i_factor_group]
        for i_sublat_before, occ_sublat_rep in enumerate(occ_op_rep):
            site_before = xtal.IntegralSiteCoordinate(i_sublat_before, [0, 0, 0])
            site_after = site_rep * site_before
            i_sublat_after = site_after.sublattice()
            for i_occ_before in range(len(occ_sublat_rep)):
                i_occ_after = occ_sublat_rep[i_occ_before]
                assert (
                    occ_dof[i_sublat_before][i_occ_before]
                    == occ_dof[i_sublat_after][i_occ_after]
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
                "dof_specs": {"occ": {"site_basis_functions": "occupation"}}
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
                [0.0, 1.0],
            ]
        )
        assert np.allclose(builder.occ_site_functions[b]["value"], expected)

    for b in [1]:
        # B, C, D
        expected = np.array(
            [
                [1.0, 1.0, 1.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
            ]
        )
        assert np.allclose(builder.occ_site_functions[b]["value"], expected)

    for b in [2]:
        # B, D, C
        expected = np.array(
            [
                [1.0, 1.0, 1.0],
                [0.0, 0.0, 1.0],
                [0.0, 1.0, 0.0],
            ]
        )
        assert np.allclose(builder.occ_site_functions[b]["value"], expected)

    for b in [3]:
        # C, D, B
        expected = np.array(
            [
                [1.0, 1.0, 1.0],
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
            ]
        )
        assert np.allclose(builder.occ_site_functions[b]["value"], expected)

    # print_expected_cluster_functions_detailed(
    #     functions,
    #     file=pathlib.Path(os.path.realpath(__file__)).parent
    #     / "data"
    #     / "expected_occ_site_functions_fcc_2.json",
    # )
    with open(session_shared_datadir / "expected_occ_site_functions_fcc_2.json") as f:
        assert_expected_cluster_functions_detailed(functions, clusters, json.load(f))


def test_occ_fcc_3a(session_shared_datadir):
    """Baseline - prim with occupation DoF with chemistry and magspin

    To be compared with test_occ_fcc_3b,
    where the occupants are ordered differently.
    """

    # Lattice vectors
    lattice = xtal.Lattice(np.eye(3))

    # Basis sites positions, as columns of a matrix,
    # in fractional coordinates with respect to the lattice vectors
    coordinate_frac = np.array(
        [
            [0.0, 0.0, 0.0],
            [0.0, 0.5, 0.5],
            [0.5, 0.0, 0.5],
            [0.5, 0.5, 0.0],
        ]
    ).transpose()

    # Occupation degrees of freedom (DoF)
    occupants = {
        "A.up": make_discrete_magnetic_atom(name="A", value=1, flavor="C"),
        "A.down": make_discrete_magnetic_atom(name="A", value=-1, flavor="C"),
        "B.up": make_discrete_magnetic_atom(name="B", value=1, flavor="C"),
        "B.down": make_discrete_magnetic_atom(name="B", value=-1, flavor="C"),
        "C": xtal.make_atom(name="C"),
    }
    occ_dof = [
        ["C", "A.up", "A.down"],
        ["C", "A.up", "A.down", "B.up", "B.down"],
        ["C", "A.up", "A.down", "B.up", "B.down"],
        ["C", "A.up", "A.down", "B.up", "B.down"],
    ]

    xtal_prim = xtal.Prim(
        lattice=lattice,
        coordinate_frac=coordinate_frac,
        occ_dof=occ_dof,
        occupants=occupants,
    )
    prim = casmconfig.Prim(xtal_prim)
    assert len(prim.factor_group.elements) == 96
    occ_symgroup_rep = prim.occ_symgroup_rep

    for i_factor_group, occ_op_rep in enumerate(occ_symgroup_rep):
        site_rep = prim.integral_site_coordinate_symgroup_rep[i_factor_group]
        for i_sublat_before, occ_sublat_rep in enumerate(occ_op_rep):
            site_before = xtal.IntegralSiteCoordinate(i_sublat_before, [0, 0, 0])
            site_after = site_rep * site_before
            i_sublat_after = site_after.sublattice()
            for i_occ_before in range(len(occ_sublat_rep)):
                i_occ_after = occ_sublat_rep[i_occ_before]

                orientation_name_before = occ_dof[i_sublat_before][i_occ_before]
                orientation_name_after = occ_dof[i_sublat_after][i_occ_after]

                # assert occupants map (chemical name match)
                assert (
                    occupants[orientation_name_before].name()
                    == occupants[orientation_name_after].name()
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
                        "site_basis_functions": {
                            "type": "occupation",
                            "reference_occ": ["C", "C", "C", "C"],
                        }
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
        # "C", "A.up", "A.down"
        expected = np.array(
            [
                [1.0, 1.0, 1.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
            ]
        )
        assert np.allclose(builder.occ_site_functions[b]["value"], expected)

    for b in [1, 2, 3]:
        # "C", "A.up", "A.down", "B.up", "B.down"
        expected = np.array(
            [
                [1.0, 1.0, 1.0, 1.0, 1.0],
                [0.0, 1.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 1.0],
            ]
        )
        assert np.allclose(builder.occ_site_functions[b]["value"], expected)

    # print_expected_cluster_functions_detailed(
    #     functions,
    #     file=pathlib.Path(os.path.realpath(__file__)).parent
    #     / "data"
    #     / "expected_occ_site_functions_fcc_3.json",
    # )
    with open(session_shared_datadir / "expected_occ_site_functions_fcc_3.json") as f:
        assert_expected_cluster_functions_detailed(functions, clusters, json.load(f))


def test_occ_fcc_3b(session_shared_datadir):
    """Change order of occupants

    This affects the site basis function (phi) values on that sublattice,
    but the generated functions are the same as test_occ_fcc_3a
    (because they are functions of the phi which remain in the same order).
    """

    # Lattice vectors
    lattice = xtal.Lattice(np.eye(3))

    # Basis sites positions, as columns of a matrix,
    # in fractional coordinates with respect to the lattice vectors
    coordinate_frac = np.array(
        [
            [0.0, 0.0, 0.0],
            [0.0, 0.5, 0.5],
            [0.5, 0.0, 0.5],
            [0.5, 0.5, 0.0],
        ]
    ).transpose()

    # Occupation degrees of freedom (DoF)
    occupants = {
        "A.up": make_discrete_magnetic_atom(name="A", value=1, flavor="C"),
        "A.down": make_discrete_magnetic_atom(name="A", value=-1, flavor="C"),
        "B.up": make_discrete_magnetic_atom(name="B", value=1, flavor="C"),
        "B.down": make_discrete_magnetic_atom(name="B", value=-1, flavor="C"),
        "C": xtal.make_atom(name="C"),
    }
    occ_dof = [
        ["A.up", "A.down", "C"],
        ["A.up", "A.down", "B.up", "B.down", "C"],
        ["A.up", "A.down", "B.up", "B.down", "C"],
        ["A.up", "A.down", "B.up", "B.down", "C"],
    ]

    xtal_prim = xtal.Prim(
        lattice=lattice,
        coordinate_frac=coordinate_frac,
        occ_dof=occ_dof,
        occupants=occupants,
    )
    prim = casmconfig.Prim(xtal_prim)
    assert len(prim.factor_group.elements) == 96
    occ_symgroup_rep = prim.occ_symgroup_rep

    for i_factor_group, occ_op_rep in enumerate(occ_symgroup_rep):
        site_rep = prim.integral_site_coordinate_symgroup_rep[i_factor_group]
        for i_sublat_before, occ_sublat_rep in enumerate(occ_op_rep):
            site_before = xtal.IntegralSiteCoordinate(i_sublat_before, [0, 0, 0])
            site_after = site_rep * site_before
            i_sublat_after = site_after.sublattice()
            for i_occ_before in range(len(occ_sublat_rep)):
                i_occ_after = occ_sublat_rep[i_occ_before]

                orientation_name_before = occ_dof[i_sublat_before][i_occ_before]
                orientation_name_after = occ_dof[i_sublat_after][i_occ_after]

                # assert occupants map (chemical name match)
                assert (
                    occupants[orientation_name_before].name()
                    == occupants[orientation_name_after].name()
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
                        "site_basis_functions": {
                            "type": "occupation",
                            "reference_occ": ["C", "C", "C", "C"],
                        }
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
        # "A.up", "A.down", "C"
        expected = np.array(
            [
                [1.0, 1.0, 1.0],
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
            ]
        )
        assert np.allclose(builder.occ_site_functions[b]["value"], expected)

    for b in [1, 2, 3]:
        # "A.up", "A.down", "B.up", "B.down", "C"
        expected = np.array(
            [
                [1.0, 1.0, 1.0, 1.0, 1.0],
                [1.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 1.0, 0.0],
            ]
        )
        assert np.allclose(builder.occ_site_functions[b]["value"], expected)

    # import os
    # import pathlib
    # from utils.helpers import print_expected_cluster_functions_detailed

    # print_expected_cluster_functions_detailed(
    #     functions,
    #     file=pathlib.Path(os.path.realpath(__file__)).parent
    #     / "data"
    #     / "expected_occ_site_functions_fcc_3.json",
    # )
    with open(session_shared_datadir / "expected_occ_site_functions_fcc_3.json") as f:
        assert_expected_cluster_functions_detailed(functions, clusters, json.load(f))


def test_occ_fcc_4a(session_shared_datadir):
    """Baseline - prim with occupation DoF with molecular orientation

    To be compared with test_occ_fcc_4b,
    where the occupants are ordered differently.
    """

    mol_x = xtal.Occupant(
        name="mol",
        atoms=[
            xtal.AtomComponent(name="B", coordinate=[-0.1, 0.0, 0.0], properties={}),
            xtal.AtomComponent(name="B", coordinate=[0.1, 0.0, 0.0], properties={}),
        ],
    )
    mol_y = xtal.Occupant(
        name="mol",
        atoms=[
            xtal.AtomComponent(name="B", coordinate=[0.0, -0.1, 0.0], properties={}),
            xtal.AtomComponent(name="B", coordinate=[0.0, 0.1, 0.0], properties={}),
        ],
    )
    mol_z = xtal.Occupant(
        name="mol",
        atoms=[
            xtal.AtomComponent(name="B", coordinate=[0.0, 0.0, -0.1], properties={}),
            xtal.AtomComponent(name="B", coordinate=[0.0, 0.0, 0.1], properties={}),
        ],
    )
    atom_A = xtal.Occupant(
        name="A",
        atoms=[
            xtal.AtomComponent(name="A", coordinate=[0.0, 0.0, 0.0], properties={}),
        ],
    )
    occupants = {"mol.x": mol_x, "mol.y": mol_y, "mol.z": mol_z, "A": atom_A}
    occ_dof = [
        ["A"],
        ["A", "mol.x", "mol.y", "mol.z"],
        ["A", "mol.x", "mol.y", "mol.z"],
        ["A", "mol.x", "mol.y", "mol.z"],
    ]
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
        occ_dof=occ_dof,
        occupants=occupants,
    )
    prim = casmconfig.Prim(xtal_prim)
    assert len(prim.factor_group.elements) == 48
    occ_symgroup_rep = prim.occ_symgroup_rep

    for i_factor_group, occ_op_rep in enumerate(occ_symgroup_rep):
        site_rep = prim.integral_site_coordinate_symgroup_rep[i_factor_group]
        for i_sublat_before, occ_sublat_rep in enumerate(occ_op_rep):
            site_before = xtal.IntegralSiteCoordinate(i_sublat_before, [0, 0, 0])
            site_after = site_rep * site_before
            i_sublat_after = site_after.sublattice()
            for i_occ_before in range(len(occ_sublat_rep)):
                i_occ_after = occ_sublat_rep[i_occ_before]

                orientation_name_before = occ_dof[i_sublat_before][i_occ_before]
                orientation_name_after = occ_dof[i_sublat_after][i_occ_after]

                # assert occupants map (chemical name match)
                assert (
                    occupants[orientation_name_before].name()
                    == occupants[orientation_name_after].name()
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
                "dof_specs": {"occ": {"site_basis_functions": "occupation"}}
            },
        },
        verbose=False,
    )
    functions, clusters = (builder.functions, builder.clusters)

    _occ_site_functions = builder.occ_site_functions.copy()
    print(xtal.pretty_json(_occ_site_functions))

    for b in [0]:
        # "A"
        expected = np.array(
            [
                [1.0],
            ]
        )

        assert np.allclose(
            get_occ_site_functions(builder.occ_site_functions, b),
            expected,
        )

    for b in [1]:
        # "A", "mol.x", "mol.y", "mol.z"
        expected = np.array(
            [
                [1.0, 1.0, 1.0, 1.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ]
        )
        assert np.allclose(
            get_occ_site_functions(builder.occ_site_functions, b),
            expected,
        )

    for b in [2]:
        # "A", "mol.x", "mol.y", "mol.z"
        expected = np.array(
            [
                [1.0, 1.0, 1.0, 1.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ]
        )
        assert np.allclose(
            get_occ_site_functions(builder.occ_site_functions, b),
            expected,
        )

    for b in [3]:
        # "A", "mol.x", "mol.y", "mol.z"
        expected = np.array(
            [
                [1.0, 1.0, 1.0, 1.0],
                [0.0, 0.0, 0.0, 1.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
            ]
        )
        assert np.allclose(
            get_occ_site_functions(builder.occ_site_functions, b),
            expected,
        )

    # import os
    # import pathlib
    # from utils.helpers import print_expected_cluster_functions_detailed
    #
    # print_expected_cluster_functions_detailed(
    #     functions,
    #     file=pathlib.Path(os.path.realpath(__file__)).parent
    #     / "data"
    #     / "expected_occ_site_functions_fcc_4.json",
    # )
    with open(session_shared_datadir / "expected_occ_site_functions_fcc_4.json") as f:
        assert_expected_cluster_functions_detailed(functions, clusters, json.load(f))


def test_occ_fcc_4b(session_shared_datadir):
    """Change order of occupants

    This affects the site basis function (phi) values on that sublattice,
    but the generated functions are the same as test_occ_fcc_3a
    (because they are functions of the phi which remain in the same order).
    """

    mol_x = xtal.Occupant(
        name="mol",
        atoms=[
            xtal.AtomComponent(name="B", coordinate=[-0.1, 0.0, 0.0], properties={}),
            xtal.AtomComponent(name="B", coordinate=[0.1, 0.0, 0.0], properties={}),
        ],
    )
    mol_y = xtal.Occupant(
        name="mol",
        atoms=[
            xtal.AtomComponent(name="B", coordinate=[0.0, -0.1, 0.0], properties={}),
            xtal.AtomComponent(name="B", coordinate=[0.0, 0.1, 0.0], properties={}),
        ],
    )
    mol_z = xtal.Occupant(
        name="mol",
        atoms=[
            xtal.AtomComponent(name="B", coordinate=[0.0, 0.0, -0.1], properties={}),
            xtal.AtomComponent(name="B", coordinate=[0.0, 0.0, 0.1], properties={}),
        ],
    )
    atom_A = xtal.Occupant(
        name="A",
        atoms=[
            xtal.AtomComponent(name="A", coordinate=[0.0, 0.0, 0.0], properties={}),
        ],
    )
    occupants = {"mol.x": mol_x, "mol.y": mol_y, "mol.z": mol_z, "A": atom_A}
    occ_dof = [
        ["A"],
        ["A", "mol.x", "mol.y", "mol.z"],
        ["mol.x", "mol.y", "mol.z", "A"],
        ["A", "mol.y", "mol.z", "mol.x"],
    ]
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
        occ_dof=occ_dof,
        occupants=occupants,
    )
    prim = casmconfig.Prim(xtal_prim)
    assert len(prim.factor_group.elements) == 48
    occ_symgroup_rep = prim.occ_symgroup_rep

    for i_factor_group, occ_op_rep in enumerate(occ_symgroup_rep):
        site_rep = prim.integral_site_coordinate_symgroup_rep[i_factor_group]
        for i_sublat_before, occ_sublat_rep in enumerate(occ_op_rep):
            site_before = xtal.IntegralSiteCoordinate(i_sublat_before, [0, 0, 0])
            site_after = site_rep * site_before
            i_sublat_after = site_after.sublattice()
            for i_occ_before in range(len(occ_sublat_rep)):
                i_occ_after = occ_sublat_rep[i_occ_before]

                orientation_name_before = occ_dof[i_sublat_before][i_occ_before]
                orientation_name_after = occ_dof[i_sublat_after][i_occ_after]

                # assert occupants map (chemical name match)
                assert (
                    occupants[orientation_name_before].name()
                    == occupants[orientation_name_after].name()
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
                        "site_basis_functions": {
                            "type": "occupation",
                            "reference_occ": ["A", "A", "A", "A"],
                        }
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
        # "A"
        expected = np.array(
            [
                [1.0],
            ]
        )

        assert np.allclose(
            get_occ_site_functions(builder.occ_site_functions, b),
            expected,
        )

    for b in [1]:
        # "A", "mol.x", "mol.y", "mol.z"
        expected = np.array(
            [
                [1.0, 1.0, 1.0, 1.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ]
        )
        assert np.allclose(
            get_occ_site_functions(builder.occ_site_functions, b),
            expected,
        )

    for b in [2]:
        # "mol.x", "mol.y", "mol.z", "A"
        expected = np.array(
            [
                [1.0, 1.0, 1.0, 1.0],
                [0.0, 1.0, 0.0, 0.0],
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
            ]
        )
        assert np.allclose(
            get_occ_site_functions(builder.occ_site_functions, b),
            expected,
        )

    for b in [3]:
        # "A", "mol.y", "mol.z", "mol.x"
        expected = np.array(
            [
                [1.0, 1.0, 1.0, 1.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ]
        )
        assert np.allclose(
            get_occ_site_functions(builder.occ_site_functions, b),
            expected,
        )

    # print_expected_cluster_functions_detailed(
    #     functions,
    #     file=pathlib.Path(os.path.realpath(__file__)).parent
    #     / "data"
    #     / "expected_occ_site_functions_fcc_4.json",
    # )
    with open(session_shared_datadir / "expected_occ_site_functions_fcc_4.json") as f:
        assert_expected_cluster_functions_detailed(functions, clusters, json.load(f))


def test_occ_fcc_5a(session_shared_datadir):
    """Prim with occupation DoF with Cmagspin A.up, A.down"""

    atom_A_up = xtal.Occupant(
        name="A",
        atoms=[
            xtal.AtomComponent(
                name="A",
                coordinate=[0.0, 0.0, 0.0],
                properties={"Cmagspin": [1.0]},
            ),
        ],
    )
    atom_A_down = xtal.Occupant(
        name="A",
        atoms=[
            xtal.AtomComponent(
                name="A",
                coordinate=[0.0, 0.0, 0.0],
                properties={"Cmagspin": [-1.0]},
            ),
        ],
    )
    occupants = {"A.up": atom_A_up, "A.down": atom_A_down}
    occ_dof = [
        ["A.up", "A.down"],
    ]

    xtal_prim = xtal.Prim(
        lattice=xtal.Lattice(
            column_vector_matrix=np.array(
                [
                    [0.0, 2.0, 2.0],
                    [2.0, 0.0, 2.0],
                    [2.0, 2.0, 0.0],
                ]
            ),
        ),
        coordinate_frac=np.array(
            [
                [0.0, 0.0, 0.0],
            ]
        ).T,
        occ_dof=occ_dof,
        occupants=occupants,
    )
    prim = casmconfig.Prim(xtal_prim)
    assert len(prim.factor_group.elements) == 96
    occ_symgroup_rep = prim.occ_symgroup_rep

    for i_factor_group, occ_op_rep in enumerate(occ_symgroup_rep):
        site_rep = prim.integral_site_coordinate_symgroup_rep[i_factor_group]
        for i_sublat_before, occ_sublat_rep in enumerate(occ_op_rep):
            site_before = xtal.IntegralSiteCoordinate(i_sublat_before, [0, 0, 0])
            site_after = site_rep * site_before
            i_sublat_after = site_after.sublattice()
            for i_occ_before in range(len(occ_sublat_rep)):
                i_occ_after = occ_sublat_rep[i_occ_before]

                orientation_name_before = occ_dof[i_sublat_before][i_occ_before]
                orientation_name_after = occ_dof[i_sublat_after][i_occ_after]

                # assert occupants map (chemical name match)
                assert (
                    occupants[orientation_name_before].name()
                    == occupants[orientation_name_after].name()
                )

    # print(xtal.pretty_json(xtal_prim.to_dict()))

    builder = build_cluster_functions(
        prim=xtal_prim,
        clex_basis_specs={
            "cluster_specs": {
                "orbit_branch_specs": {
                    "2": {"max_length": 4.01},
                    "3": {"max_length": 1.01},
                },
            },
            "basis_function_specs": {
                "dof_specs": {"occ": {"site_basis_functions": "chebychev"}}
            },
        },
        verbose=False,
    )
    functions, clusters = (builder.functions, builder.clusters)

    _occ_site_functions = builder.occ_site_functions.copy()
    print(xtal.pretty_json(_occ_site_functions))

    for b in [0]:
        # "A.up, A.down"
        expected = np.array(
            [
                [1.0, 1.0],
                [-1.0, 1.0],
            ]
        )

        assert np.allclose(
            get_occ_site_functions(builder.occ_site_functions, b),
            expected,
        )

    from casm.bset.json_io import dump

    dump(builder.to_dict(), "cluster_functions.json", force=True)

    # import os
    # import pathlib
    # from utils.helpers import print_expected_cluster_functions_detailed
    #
    # print_expected_cluster_functions_detailed(
    #     functions,
    #     file=pathlib.Path(os.path.realpath(__file__)).parent
    #     / "data"
    #     / "expected_occ_site_functions_fcc_5.json",
    # )
    with open(session_shared_datadir / "expected_occ_site_functions_fcc_5.json") as f:
        assert_expected_cluster_functions_detailed(functions, clusters, json.load(f))
