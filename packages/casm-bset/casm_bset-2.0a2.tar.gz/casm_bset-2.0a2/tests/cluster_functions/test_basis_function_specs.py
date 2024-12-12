from casm.bset.cluster_functions import BasisFunctionSpecs


def test_basis_function_specs_1():
    basis_function_specs = BasisFunctionSpecs(
        dofs=["occ", "Hstrain"],
        dof_specs={
            "occ": {
                "site_basis_functions": "occupation",
            }
        },
        orbit_branch_max_poly_order={
            # use maximum polynomial order 6,
            # for orbits of cluster size 1
            "1": 6,
            # use maximum polynomial order 5,
            # for orbits of cluster size 4
            "2": 5,
        },
        # use max(3, cluster size) for all other orbits
        global_max_poly_order=3,
    )

    assert isinstance(basis_function_specs, BasisFunctionSpecs)

    data = basis_function_specs.to_dict()
    assert isinstance(data, dict)
    assert data["dofs"] == ["occ", "Hstrain"]
    assert data["orbit_branch_max_poly_order"] == {"1": 6, "2": 5}
    assert data["global_max_poly_order"] == 3
    assert data["dof_specs"] == {"occ": {"site_basis_functions": "occupation"}}
    assert "default" not in data

    basis_function_specs_in = BasisFunctionSpecs.from_dict(data)
    assert isinstance(basis_function_specs_in, BasisFunctionSpecs)
    assert basis_function_specs_in.dofs == ["occ", "Hstrain"]
    assert basis_function_specs_in.dof_specs == {
        "occ": {"site_basis_functions": "occupation"}
    }
    assert basis_function_specs_in.global_max_poly_order == 3
    assert basis_function_specs_in.orbit_branch_max_poly_order == {"1": 6, "2": 5}
    assert basis_function_specs_in.param_pack_type == "default"


def test_basis_function_specs_2():
    basis_function_specs = BasisFunctionSpecs()

    assert isinstance(basis_function_specs, BasisFunctionSpecs)

    data = basis_function_specs.to_dict()
    assert isinstance(data, dict)
    assert "dofs" not in data
    assert "orbit_branch_max_poly_order" not in data
    assert "global_max_poly_order" not in data
    assert "dof_specs" not in data
    assert "param_pack_type" not in data

    basis_function_specs_in = BasisFunctionSpecs.from_dict(data)
    assert isinstance(basis_function_specs_in, BasisFunctionSpecs)
    assert basis_function_specs_in.dofs is None
    assert basis_function_specs_in.dof_specs == {}
    assert basis_function_specs_in.global_max_poly_order is None
    assert basis_function_specs_in.orbit_branch_max_poly_order == {}
    assert basis_function_specs_in.param_pack_type == "default"
