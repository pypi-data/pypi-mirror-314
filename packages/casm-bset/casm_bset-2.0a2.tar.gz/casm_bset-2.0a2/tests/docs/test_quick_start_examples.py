def test_quick_start_ex1():
    import libcasm.configuration as casmconfig
    import libcasm.xtal.prims as xtal_prims
    from casm.bset import make_clex_basis_specs

    # Construct a ternary FCC prim
    xtal_prim = xtal_prims.FCC(
        r=0.5,
        occ_dof=["A", "B", "C"],
    )
    prim = casmconfig.Prim(xtal_prim)

    # Construct ClexBasisSpecs
    # max_length: list[float] | None
    #     The maximum site-to-site distance by cluster size
    #     (i.e. null, point, pair, triplet clusters).
    #     For a periodic cluster expansion, the null and point
    #     distances are arbitrary and can be set to 0.0.
    # occ_site_basis_functions_specs: Any
    #     Function type for occupation DoFs
    clex_basis_specs = make_clex_basis_specs(
        prim=prim,
        max_length=[0.0, 0.0, 3.01, 2.01],
        occ_site_basis_functions_specs="occupation",
    )

    # tests:
    from casm.bset.cluster_functions import ClexBasisSpecs

    assert isinstance(clex_basis_specs, ClexBasisSpecs)


def test_quick_start_ex2():
    import libcasm.configuration as casmconfig
    import libcasm.xtal.prims as xtal_prims
    from casm.bset.cluster_functions import ClexBasisSpecs

    # Construct a ternary FCC prim
    xtal_prim = xtal_prims.FCC(
        r=0.5,
        occ_dof=["A", "B", "C"],
    )
    prim = casmconfig.Prim(xtal_prim)

    # Define a cluster expansion basis set using a Python dict
    clex_basis_specs = ClexBasisSpecs.from_dict(
        data={
            "basis_function_specs": {
                "dof_specs": {"occ": {"site_basis_functions": "occupation"}}
            },
            "cluster_specs": {
                "orbit_branch_specs": {
                    "0": {"max_length": 0.0},
                    "1": {"max_length": 0.0},
                    "2": {"max_length": 3.01},
                    "3": {"max_length": 2.01},
                },
            },
        },
        prim=prim,
    )

    # tests:
    assert isinstance(clex_basis_specs, ClexBasisSpecs)


def test_quick_start_write_and_evaluate():
    import libcasm.configuration as casmconfig
    import libcasm.xtal.prims as xtal_prims
    from casm.bset import make_clex_basis_specs

    # Construct a ternary FCC prim
    xtal_prim = xtal_prims.FCC(
        r=0.5,
        occ_dof=["A", "B", "C"],
    )
    prim = casmconfig.Prim(xtal_prim)

    # Construct ClexBasisSpecs
    # max_length: maximum site-to-site distance
    #     for null, point, pair, triplet clusters
    # occ_site_basis_functions_specs: site basis
    #     function type for occupation DoFs
    clex_basis_specs = make_clex_basis_specs(
        prim=prim,
        max_length=[0.0, 0.0, 3.01, 2.01],
        occ_site_basis_functions_specs="occupation",
    )

    ## Write clexulator source code

    import tempfile

    import numpy as np

    import libcasm.clexulator as casmclex
    from casm.bset import write_clexulator

    # Create a temporary directory to write the Clexulator source code
    # For example only - change this to a permanent directory
    tmp_dir = tempfile.TemporaryDirectory()
    bset_dir = tmp_dir.name

    # Write the Clexulator source code to `src_path`
    # bset_dir: pathlib.Path
    #     The directory to write the Clexulator source file
    # src_path: pathlib.Path
    #    The path to the Clexulator source file (or a
    #    prototype Clexulator source file if a local cluster
    #    expansion).
    # local_src_path: Optional[list[pathlib.Path]]
    #    If a local cluster expansion, the paths to the local
    #    Clexulator source files.
    # prim_neighbor_list: libcasm.clexulator.PrimNeighborList
    #    The neighbor list for the prim
    src_path, local_src_path, prim_neighbor_list = write_clexulator(
        prim=prim,
        clex_basis_specs=clex_basis_specs,
        bset_dir=bset_dir,
        project_name="TestProject",
        bset_name="default",
    )

    ## Compiling and constructing a clexulator

    # Compile and construct a clexulator
    clexulator = casmclex.make_clexulator(
        source=str(src_path),
        prim_neighbor_list=prim_neighbor_list,
    )

    ## Evaluating correlations

    # Construct a Supercell (conventional FCC cubic cell)
    supercell = casmconfig.Supercell(
        prim=prim,
        transformation_matrix_to_super=np.array(
            [
                [-1, 1, 1],
                [1, -1, 1],
                [1, 1, -1],
            ],
            dtype="int",
        ),
    )

    # Construct a neighbor list for the supercell
    supercell_neighbor_list = casmclex.SuperNeighborList(
        supercell.transformation_matrix_to_super,
        prim_neighbor_list,
    )

    # Construct a default Configuration (with [A, B, B, C] occupation)
    config = casmconfig.Configuration(supercell)
    config.set_occupation([0, 1, 1, 2])

    # Construct a correlations calculator, pointed at `config`'s DoF values
    corr = casmclex.Correlations(
        supercell_neighbor_list=supercell_neighbor_list,
        clexulator=clexulator,
        config_dof_values=config.dof_values,
    )

    # Evaluate the correlations
    # correlation_values: np.ndarray, the correlation values
    corr_per_supercell = corr.per_supercell()
    corr_per_unitcell = corr.per_unitcell(corr_per_supercell)  # noqa F841

    ## Evaluating a cluster expansion

    # Construct a SparseCoefficients object
    # from basis function indices and coefficients (using the m * V values)
    formation_energy_coefficients = casmclex.SparseCoefficients(
        index=[0, 1, 3],  # linear function indices
        value=[-1.0, -0.1, 0.02],  # coefficients, using the m * V values
    )

    # Construct a cluster expansion calculator,
    # pointed at `config`'s DoF values
    clex = casmclex.ClusterExpansion(
        supercell_neighbor_list=supercell_neighbor_list,
        clexulator=clexulator,
        coefficients=formation_energy_coefficients,
        config_dof_values=config.dof_values,
    )

    # Evaluate the cluster expansion
    # for the configuration with its current occupation
    clex_formation_energy_per_unitcell = clex.per_unitcell()

    # Change the occupation of the configuration (to [B, A, B, C])
    config.set_occupation([1, 0, 1, 2])

    # Evaluate the cluster expansion
    # for the configuration with its current occupation
    clex_formation_energy_per_unitcell = clex.per_unitcell()  # noqa F841

    ## Calculate the effect of changes in DoF values

    # Get the change in the cluster expansion *per-supercell* value
    # for a proposed change in the occupation on one site,
    # leaving the occupation unchanged.
    assert config.occ(2) == 1  # B

    delta_clex_formation_energy_per_supercell = clex.occ_delta_value(  # noqa F841
        linear_site_index=2,
        new_occ=0,  # A
    )

    assert config.occ(2) == 1  # B
