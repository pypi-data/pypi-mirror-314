import json

from utils.expected_Hstrain_disp_functions import (
    expected_Hstrain_disp_functions_fcc_1,
    expected_Hstrain_disp_functions_hcp_1,
    expected_Hstrain_disp_functions_lowsym_1,
)
from utils.helpers import (
    assert_expected_cluster_functions,
    assert_expected_cluster_functions_detailed,
)

import libcasm.xtal as xtal
import libcasm.xtal.prims as xtal_prims
from casm.bset import (
    build_cluster_functions,
)


def test_Hstrain_disp_fcc_1(session_shared_datadir):
    xtal_prim = xtal_prims.FCC(
        r=0.5,
        occ_dof=["A"],
        local_dof=[xtal.DoFSetBasis("disp")],
        global_dof=[xtal.DoFSetBasis("Hstrain")],
    )
    print(xtal.pretty_json(xtal_prim.to_dict()))

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
                "global_max_poly_order": 4,
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
    assert len(functions[0]) == 1
    assert len(functions[0][0]) == 21
    assert len(functions[1]) == 1
    assert len(functions[1][0]) == 15
    assert len(functions[2]) == 6
    assert len(functions[2][0]) == 105
    assert len(functions[3]) == 8
    assert len(functions[3][0]) == 67

    # print_expected_cluster_functions_detailed(
    #     functions,
    #     file=pathlib.Path(os.path.realpath(__file__)).parent
    #     / "data"
    #     / "expected_Hstrain_disp_functions_fcc_1.json",
    # )
    with open(
        session_shared_datadir / "expected_Hstrain_disp_functions_fcc_1.json"
    ) as f:
        assert_expected_cluster_functions_detailed(functions, clusters, json.load(f))

    # print_expected_cluster_functions(functions)
    # assert False
    expected_functions = expected_Hstrain_disp_functions_fcc_1()

    assert_expected_cluster_functions(
        functions,
        expected_functions,
    )


def test_Hstrain_disp_hcp_1(session_shared_datadir):
    xtal_prim = xtal_prims.HCP(
        r=0.5,
        occ_dof=["A"],
        local_dof=[xtal.DoFSetBasis("disp")],
        global_dof=[xtal.DoFSetBasis("Hstrain")],
    )
    print(xtal.pretty_json(xtal_prim.to_dict()))

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
                "global_max_poly_order": 4,
            },
        },
    )
    functions, clusters = (builder.functions, builder.clusters)

    # print_expected_cluster_functions_detailed(
    #     functions,
    #     file=pathlib.Path(os.path.realpath(__file__)).parent
    #     / "data"
    #     / "expected_Hstrain_disp_functions_hcp_1.json",
    # )
    with open(
        session_shared_datadir / "expected_Hstrain_disp_functions_hcp_1.json"
    ) as f:
        assert_expected_cluster_functions_detailed(functions, clusters, json.load(f))

    # print_expected_cluster_functions(functions)
    # assert False
    expected_functions = expected_Hstrain_disp_functions_hcp_1()

    assert_expected_cluster_functions(
        functions,
        expected_functions,
    )


def test_Hstrain_disp_lowsym_1(lowsym_Hstrain_disp_prim, session_shared_datadir):
    xtal_prim = lowsym_Hstrain_disp_prim
    print(xtal.pretty_json(xtal_prim.to_dict()))

    builder = build_cluster_functions(
        prim=xtal_prim,
        clex_basis_specs={
            "cluster_specs": {
                "orbit_branch_specs": {
                    "2": {"max_length": 1.01},
                },
            },
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
    #     / "expected_Hstrain_disp_functions_lowsym_1.json",
    # )
    with open(
        session_shared_datadir / "expected_Hstrain_disp_functions_lowsym_1.json"
    ) as f:
        assert_expected_cluster_functions_detailed(functions, clusters, json.load(f))

    # print_expected_cluster_functions(functions)
    # assert False
    expected_functions = expected_Hstrain_disp_functions_lowsym_1()

    assert_expected_cluster_functions(
        functions,
        expected_functions,
    )
