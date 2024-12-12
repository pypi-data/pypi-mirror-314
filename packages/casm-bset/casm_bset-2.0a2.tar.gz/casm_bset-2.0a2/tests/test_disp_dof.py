import json

from utils.expected_disp_functions import (
    expected_disp_functions_fcc_1,
    expected_disp_functions_hcp_1,
    expected_disp_functions_lowsym_1,
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


def test_disp_fcc_1(session_shared_datadir):
    xtal_prim = xtal_prims.FCC(
        r=0.5,
        occ_dof=["A"],
        local_dof=[xtal.DoFSetBasis("disp")],
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
    assert len(functions[0][0]) == 0
    assert len(functions[1]) == 1
    assert len(functions[1][0]) == 3
    assert len(functions[2]) == 6
    assert len(functions[2][0]) == 26
    assert len(functions[3]) == 8
    assert len(functions[3][0]) == 37

    # from utils.helpers import print_expected_cluster_functions_detailed
    # import os
    # import pathlib
    #
    # print_expected_cluster_functions_detailed(
    #     functions,
    #     file=pathlib.Path(os.path.realpath(__file__)).parent
    #     / "data"
    #     / "expected_disp_functions_fcc_1.json",
    # )
    with open(session_shared_datadir / "expected_disp_functions_fcc_1.json") as f:
        assert_expected_cluster_functions_detailed(functions, clusters, json.load(f))

    # print_expected_cluster_functions(functions)
    assert_expected_cluster_functions(
        functions,
        expected_disp_functions_fcc_1(),
    )


def test_disp_hcp_1(session_shared_datadir):
    xtal_prim = xtal_prims.HCP(
        r=0.5,
        occ_dof=["A"],
        local_dof=[xtal.DoFSetBasis("disp")],
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
                "global_max_poly_order": 4,
            },
        },
    )
    functions, clusters = (builder.functions, builder.clusters)

    assert len(clusters) == 7
    assert clusters[0][0].size() == 0  # null
    assert len(clusters[0]) == 1
    assert clusters[1][0].size() == 1  # point
    assert len(clusters[1]) == 2
    assert clusters[2][0].size() == 2  # pair (out of basal plane)
    assert len(clusters[2]) == 6
    assert clusters[3][0].size() == 2  # pair (in basal plane)
    assert len(clusters[3]) == 6
    assert clusters[4][0].size() == 3  # triplet (in basal plane)
    assert len(clusters[4]) == 2
    assert clusters[5][0].size() == 3  # triplet (in basal plane)
    assert len(clusters[5]) == 2
    assert clusters[6][0].size() == 3  # triplet (out of basal plane)
    assert len(clusters[6]) == 12

    assert len(functions) == 7
    assert len(functions[0]) == 1
    assert len(functions[0][0]) == 0
    assert len(functions[1]) == 2
    assert len(functions[1][0]) == 6
    assert len(functions[2]) == 6
    assert len(functions[2][0]) == 43
    assert len(functions[3]) == 6
    assert len(functions[3][0]) == 43
    assert len(functions[4]) == 2
    assert len(functions[4][0]) == 20
    assert len(functions[5]) == 2
    assert len(functions[5][0]) == 20
    assert len(functions[6]) == 12
    assert len(functions[6][0]) == 99

    # print_expected_cluster_functions_detailed(
    #     functions,
    #     file=pathlib.Path(os.path.realpath(__file__)).parent
    #     / "data"
    #     / "expected_disp_functions_hcp_1.json",
    # )
    with open(session_shared_datadir / "expected_disp_functions_hcp_1.json") as f:
        assert_expected_cluster_functions_detailed(functions, clusters, json.load(f))

    # print_expected_cluster_functions(functions)
    expected_functions = expected_disp_functions_hcp_1()

    assert_expected_cluster_functions(
        functions,
        expected_functions,
    )


def test_disp_lowsym_1(lowsym_disp_prim, session_shared_datadir):
    xtal_prim = lowsym_disp_prim
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
                "global_max_poly_order": 4,
            },
        },
    )
    functions, clusters = (builder.functions, builder.clusters)

    assert len(clusters) == 24
    assert len(functions) == 24

    assert len(functions[0][0]) == 0
    assert len(functions[1][0]) == 34
    assert len(functions[2][0]) == 34
    assert len(functions[3][0]) == 34
    assert len(functions[4][0]) == 141
    assert len(functions[5][0]) == 141
    assert len(functions[6][0]) == 141
    assert len(functions[7][0]) == 141
    assert len(functions[8][0]) == 141
    assert len(functions[9][0]) == 141
    assert len(functions[10][0]) == 141
    assert len(functions[11][0]) == 141
    assert len(functions[12][0]) == 141
    assert len(functions[13][0]) == 141
    assert len(functions[14][0]) == 141
    assert len(functions[15][0]) == 141
    assert len(functions[16][0]) == 189
    assert len(functions[17][0]) == 189
    assert len(functions[18][0]) == 189
    assert len(functions[19][0]) == 189
    assert len(functions[20][0]) == 189
    assert len(functions[21][0]) == 189
    assert len(functions[22][0]) == 189
    assert len(functions[23][0]) == 189

    # print_expected_cluster_functions_detailed(
    #     functions,
    #     file=pathlib.Path(os.path.realpath(__file__)).parent
    #     / "data"
    #     / "expected_disp_functions_lowsym_1.json",
    # )
    with open(session_shared_datadir / "expected_disp_functions_lowsym_1.json") as f:
        assert_expected_cluster_functions_detailed(functions, clusters, json.load(f))

    # print_expected_cluster_functions(functions)
    expected_functions = expected_disp_functions_lowsym_1()

    assert_expected_cluster_functions(
        functions,
        expected_functions,
    )
