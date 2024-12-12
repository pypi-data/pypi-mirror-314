import numpy as np

import libcasm.configuration as casmconfig
import libcasm.xtal.prims as xtal_prims
from casm.bset.cluster_functions import BasisFunctionSpecs, ClexBasisSpecs
from libcasm.clusterography import (
    ClusterSpecs,
)


def test_clex_basis_specs_1():
    # Construct ClexBasisSpecs
    xtal_prim = xtal_prims.FCC(
        r=0.5,
        occ_dof=["A", "B", "C"],
    )
    prim = casmconfig.Prim(xtal_prim)

    clex_basis_specs = ClexBasisSpecs(
        cluster_specs=ClusterSpecs(
            xtal_prim=prim.xtal_prim,
            generating_group=prim.factor_group,
            max_length=[0.0, 0.0, 1.01, 1.01],
        ),
        basis_function_specs=BasisFunctionSpecs(
            dof_specs={
                "occ": {
                    "site_basis_functions": "occupation",
                }
            },
            orbit_branch_max_poly_order={"1": 6, "2": 5},
            global_max_poly_order=3,
        ),
    )
    assert isinstance(clex_basis_specs, ClexBasisSpecs)

    # Output dict
    data = clex_basis_specs.to_dict()

    cspecs_data = data["cluster_specs"]
    assert isinstance(cspecs_data, dict)

    bfuncs_data = data["basis_function_specs"]
    assert isinstance(bfuncs_data, dict)
    assert "dofs" not in bfuncs_data
    assert bfuncs_data["orbit_branch_max_poly_order"] == {"1": 6, "2": 5}
    assert bfuncs_data["global_max_poly_order"] == 3
    assert bfuncs_data["dof_specs"] == {"occ": {"site_basis_functions": "occupation"}}
    assert "default" not in bfuncs_data

    # Read dict
    clex_basis_specs_in = ClexBasisSpecs.from_dict(data, prim=prim)

    cluster_specs_in = clex_basis_specs.cluster_specs
    assert isinstance(cluster_specs_in, ClusterSpecs)
    assert cluster_specs_in.xtal_prim() == prim.xtal_prim
    assert len(cluster_specs_in.generating_group().elements) == 48
    assert np.allclose(cluster_specs_in.max_length(), [0.0, 0.0, 1.01, 1.01])

    basis_function_specs_in = clex_basis_specs_in.basis_function_specs
    assert isinstance(basis_function_specs_in, BasisFunctionSpecs)
    assert basis_function_specs_in.dofs is None
    assert basis_function_specs_in.dof_specs == {
        "occ": {"site_basis_functions": "occupation"}
    }
    assert basis_function_specs_in.global_max_poly_order == 3
    assert basis_function_specs_in.orbit_branch_max_poly_order == {"1": 6, "2": 5}
    assert basis_function_specs_in.param_pack_type == "default"
