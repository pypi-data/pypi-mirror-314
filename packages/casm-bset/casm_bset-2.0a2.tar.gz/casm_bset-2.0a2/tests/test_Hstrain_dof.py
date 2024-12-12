import json

from utils.expected_Hstrain_functions import (
    expected_Hstrain_functions_fcc_1,
    expected_Hstrain_functions_hcp_1,
    expected_Hstrain_functions_lowsym_1,
)
from utils.helpers import (
    assert_expected_cluster_functions_detailed,
    assert_expected_functions,
)

import libcasm.configuration as casmconfig
import libcasm.xtal as xtal
import libcasm.xtal.prims as xtal_prims
from casm.bset import (
    build_cluster_functions,
)
from casm.bset.cluster_functions import (
    make_global_dof_matrix_rep,
)
from casm.bset.polynomial_functions import (
    Variable,
    make_symmetry_adapted_polynomials,
)


def test_Hstrain_fcc_1(session_shared_datadir):
    key = "Hstrain"
    xtal_prim = xtal_prims.FCC(
        r=0.5,
        occ_dof=["A"],
        global_dof=[xtal.DoFSetBasis(key)],
    )
    # print(xtal.pretty_json(xtal_prim.to_dict()))

    # test directly using make_symmetry_adapted_polynomials
    prim = casmconfig.Prim(xtal_prim)
    matrix_rep = make_global_dof_matrix_rep(
        prim=prim,
        key=key,
    )
    basis_set = make_symmetry_adapted_polynomials(
        matrix_rep=matrix_rep,
        variables=[
            Variable(name="{E_{xx}}", key=key),
            Variable(name="{E_{yy}}", key=key),
            Variable(name="{E_{zz}}", key=key),
            Variable(name="{\\sqrt{2}E_{yz}}", key=key),
            Variable(name="{\\sqrt{2}E_{xz}}", key=key),
            Variable(name="{\\sqrt{2}E_{xy}}", key=key),
        ],
        variable_subsets=[[0, 1, 2, 3, 4, 5]],
        min_poly_order=1,
        max_poly_order=3,
    )
    assert len(basis_set) == 10
    # print_expected_functions(basis_set)
    expected = expected_Hstrain_functions_fcc_1()
    assert_expected_functions(basis_set, expected)

    # test build_cluster_functions with only global DoF
    builder = build_cluster_functions(
        prim=xtal_prim,
        clex_basis_specs={
            "cluster_specs": {},
            "basis_function_specs": {
                "global_max_poly_order": 3,
            },
        },
    )
    functions, clusters = (builder.functions, builder.clusters)

    # print_expected_cluster_functions_detailed(
    #     functions,
    #     file=pathlib.Path(os.path.realpath(__file__)).parent
    #     / "data"
    #     / "expected_Hstrain_functions_fcc_1.json",
    # )
    with open(session_shared_datadir / "expected_Hstrain_functions_fcc_1.json") as f:
        assert_expected_cluster_functions_detailed(functions, clusters, json.load(f))

    assert_expected_functions(functions[0][0], expected)


def test_Hstrain_fcc_2(session_shared_datadir):
    """Test generating only strain polynomials when the prim also has occ DoF"""
    key = "Hstrain"
    xtal_prim = xtal_prims.FCC(
        r=0.5,
        occ_dof=["A", "B"],
        global_dof=[xtal.DoFSetBasis(key)],
    )
    # print(xtal.pretty_json(xtal_prim.to_dict()))

    # test build_cluster_functions with only global DoF
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
                "dofs": ["Hstrain"],
                "global_max_poly_order": 3,
            },
        },
    )
    functions, clusters = (builder.functions, builder.clusters)

    assert len(clusters) == 4
    assert len(clusters[0]) == 1
    assert len(clusters[1]) == 1
    assert len(clusters[2]) == 6
    assert len(clusters[3]) == 8

    assert len(functions) == 4
    assert len(functions[0]) == 1  # null cluster
    assert len(functions[0][0]) == 10
    assert len(functions[1]) == 1  # point cluster
    assert len(functions[1][0]) == 0
    assert len(functions[2]) == 6  # pair cluster
    assert len(functions[2][0]) == 0
    assert len(functions[3]) == 8  # triplet cluster
    assert len(functions[3][0]) == 0

    # print_expected_cluster_functions_detailed(
    #     functions,
    #     file=pathlib.Path(os.path.realpath(__file__)).parent
    #     / "data"
    #     / "expected_Hstrain_functions_fcc_2.json",
    # )
    with open(session_shared_datadir / "expected_Hstrain_functions_fcc_2.json") as f:
        assert_expected_cluster_functions_detailed(functions, clusters, json.load(f))

    expected = expected_Hstrain_functions_fcc_1()
    assert_expected_functions(functions[0][0], expected)


def test_Hstrain_fcc_3(session_shared_datadir):
    """Test generating only strain polynomials when the prim also has disp DoF"""
    key = "Hstrain"
    xtal_prim = xtal_prims.FCC(
        r=0.5,
        occ_dof=["A"],
        local_dof=[xtal.DoFSetBasis("disp")],
        global_dof=[xtal.DoFSetBasis(key)],
    )
    # print(xtal.pretty_json(xtal_prim.to_dict()))

    # test build_cluster_functions with only global DoF
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
                "dofs": ["Hstrain"],
                "global_max_poly_order": 3,
            },
        },
    )
    functions, clusters = (builder.functions, builder.clusters)

    assert len(clusters) == 4
    assert len(clusters[0]) == 1
    assert len(clusters[1]) == 1
    assert len(clusters[2]) == 6
    assert len(clusters[3]) == 8

    assert len(functions) == 4
    assert len(functions[0]) == 1  # null cluster
    assert len(functions[0][0]) == 10
    assert len(functions[1]) == 1  # point cluster
    assert len(functions[1][0]) == 0
    assert len(functions[2]) == 6  # pair cluster
    assert len(functions[2][0]) == 0
    assert len(functions[3]) == 8  # triplet cluster
    assert len(functions[3][0]) == 0

    # print_expected_cluster_functions_detailed(
    #     functions,
    #     file=pathlib.Path(os.path.realpath(__file__)).parent
    #     / "data"
    #     / "expected_Hstrain_functions_fcc_3.json",
    # )
    with open(session_shared_datadir / "expected_Hstrain_functions_fcc_3.json") as f:
        assert_expected_cluster_functions_detailed(functions, clusters, json.load(f))

    expected = expected_Hstrain_functions_fcc_1()
    assert_expected_functions(functions[0][0], expected)


def test_Hstrain_hcp_1(session_shared_datadir):
    key = "Hstrain"
    xtal_prim = xtal_prims.HCP(
        r=0.5,
        occ_dof=["A"],
        global_dof=[xtal.DoFSetBasis(key)],
    )
    # print(xtal.pretty_json(xtal_prim.to_dict()))

    # test directly using make_symmetry_adapted_polynomials
    prim = casmconfig.Prim(xtal_prim)
    matrix_rep = make_global_dof_matrix_rep(
        prim=prim,
        key=key,
    )
    basis_set = make_symmetry_adapted_polynomials(
        matrix_rep=matrix_rep,
        variables=[
            Variable(name="{E_{xx}}", key=key),
            Variable(name="{E_{yy}}", key=key),
            Variable(name="{E_{zz}}", key=key),
            Variable(name="{\\sqrt{2}E_{yz}}", key=key),
            Variable(name="{\\sqrt{2}E_{xz}}", key=key),
            Variable(name="{\\sqrt{2}E_{xy}}", key=key),
        ],
        variable_subsets=[[0, 1, 2, 3, 4, 5]],
        min_poly_order=1,
        max_poly_order=3,
    )
    assert len(basis_set) == 17

    # print_expected_functions(basis_set)
    expected = expected_Hstrain_functions_hcp_1()
    assert_expected_functions(basis_set, expected)

    # test build_cluster_functions with only global DoF
    builder = build_cluster_functions(
        prim=xtal_prim,
        clex_basis_specs={
            "cluster_specs": {},
            "basis_function_specs": {
                "dofs": ["Hstrain"],
                "global_max_poly_order": 3,
            },
        },
    )
    functions, clusters = (builder.functions, builder.clusters)

    assert len(clusters) == 1
    assert len(clusters[0]) == 1  # null cluster

    assert len(functions) == 1
    assert len(functions[0]) == 1  # null cluster
    assert len(functions[0][0]) == 17

    # print_expected_cluster_functions_detailed(
    #     functions,
    #     file=pathlib.Path(os.path.realpath(__file__)).parent
    #     / "data"
    #     / "expected_Hstrain_functions_hcp_1.json",
    # )
    with open(session_shared_datadir / "expected_Hstrain_functions_hcp_1.json") as f:
        assert_expected_cluster_functions_detailed(functions, clusters, json.load(f))

    assert_expected_functions(functions[0][0], expected)


def test_Hstrain_lowsym_1(lowsym_Hstrain_prim, session_shared_datadir):
    key = "Hstrain"
    xtal_prim = lowsym_Hstrain_prim
    # print(xtal.pretty_json(xtal_prim.to_dict()))

    # test directly using make_symmetry_adapted_polynomials
    prim = casmconfig.Prim(xtal_prim)
    factor_group_elements = prim.factor_group.elements
    assert len(factor_group_elements) == 1
    matrix_rep = make_global_dof_matrix_rep(
        prim=prim,
        key=key,
    )
    basis_set = make_symmetry_adapted_polynomials(
        matrix_rep=matrix_rep,
        variables=[
            Variable(name="{E_{xx}}", key=key),
            Variable(name="{E_{yy}}", key=key),
            Variable(name="{E_{zz}}", key=key),
            Variable(name="{\\sqrt{2}E_{yz}}", key=key),
            Variable(name="{\\sqrt{2}E_{xz}}", key=key),
            Variable(name="{\\sqrt{2}E_{xy}}", key=key),
        ],
        variable_subsets=[[0, 1, 2, 3, 4, 5]],
        min_poly_order=1,
        max_poly_order=3,
    )
    assert len(basis_set) == 83

    # print_expected_functions(basis_set)
    expected = expected_Hstrain_functions_lowsym_1()
    assert_expected_functions(basis_set, expected)

    # test build_cluster_functions with only global DoF
    builder = build_cluster_functions(
        prim=xtal_prim,
        clex_basis_specs={
            "cluster_specs": {},
            "basis_function_specs": {
                "dofs": ["Hstrain"],
                "global_max_poly_order": 3,
            },
        },
    )
    functions, clusters = (builder.functions, builder.clusters)

    assert len(clusters) == 1
    assert len(clusters[0]) == 1  # null cluster

    assert len(functions) == 1
    assert len(functions[0]) == 1  # null cluster
    assert len(functions[0][0]) == 83

    # print_expected_cluster_functions_detailed(
    #     functions,
    #     file=pathlib.Path(os.path.realpath(__file__)).parent
    #     / "data"
    #     / "expected_Hstrain_functions_lowsym_1.json",
    # )
    with open(session_shared_datadir / "expected_Hstrain_functions_lowsym_1.json") as f:
        assert_expected_cluster_functions_detailed(functions, clusters, json.load(f))

    assert_expected_functions(functions[0][0], expected)
