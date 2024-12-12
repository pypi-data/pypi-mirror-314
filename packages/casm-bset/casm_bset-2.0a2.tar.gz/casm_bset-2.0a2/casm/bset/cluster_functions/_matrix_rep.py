from typing import Callable, Optional

import numpy as np
import scipy

import libcasm.configuration as casmconfig
import libcasm.sym_info as casmsyminfo
import libcasm.xtal as xtal
from casm.bset.polynomial_functions import (
    Variable,
)
from libcasm.clusterography import (
    Cluster,
    make_cluster_group,
    make_integral_site_coordinate_symgroup_rep,
    make_local_cluster_group,
    make_local_equivalence_map,
    make_local_equivalence_map_indices,
    make_local_orbit,
    make_periodic_equivalence_map,
    make_periodic_equivalence_map_indices,
    make_periodic_orbit,
)
from libcasm.sym_info import (
    SymGroup,
)

from ._discrete_functions import (
    get_occ_site_functions,
)
from ._misc import (
    make_equivalents_generators,
)


def make_global_dof_matrix_rep(
    prim: casmconfig.Prim,
    key: str,
):
    """Generate the group matrix representation for a global DoF

    Parameters
    ----------
    prim: :class:`~libcasm.configuration.Prim`
        The Prim
    key: str
        The name of the global DoF type. Must exist in `prim`.

    Returns
    -------
    matrix_rep: list[np.ndarray[np.float]]
        Matrix representation for the factor group acting on global DoF in
        the prim basis.
    """
    return prim.global_dof_matrix_rep(key)


def make_cluster_dof_info(
    cluster: Cluster,
    local_dof_matrix_rep: list[list[np.ndarray]],
):
    """Get cluster DoF information

    Parameters
    ----------
    cluster: Cluster
        The cluster of sites
    local_dof_matrix_rep: list[list[np.ndarray]]
        The local DoF matrix reps, `M`, for each operation in the prim factor group,
        for each sublattice,
        ``M = local_dof_matrix_rep[prim_factor_group_index][sublattice_index]``.

    Returns
    -------
    site_index_to_basis_index: dict[int, int]
        Specifies the beginning row or column, `basis_index`, in the cluster
        matrix representation for each site in the cluster,
        ``basis_index = site_index_to_basis_index[site_index]``.
    total_dim: int
        The total dimension of the resulting cluster DoF vector / and cluster
        matrix reps.

    """
    # Make a dict of site_index (index into the cluster) ->
    #   beginning row in cluster DoF space basis matrix for DoF from that site
    site_index_to_basis_index = {}
    total_dim = 0
    for site_index, integral_site_coordinate in enumerate(cluster.sites()):
        b = integral_site_coordinate.sublattice()
        site_dof_dim = local_dof_matrix_rep[0][b].shape[1]
        site_index_to_basis_index[site_index] = total_dim
        total_dim += site_dof_dim
    return (site_index_to_basis_index, total_dim)


def make_cluster_permutation_rep(
    prim: casmconfig.Prim,
    cluster: Cluster,
    cluster_group: SymGroup,
) -> list[list[int]]:
    """Make the cluster site permutation representation

    The cluster site permutation representation species how cluster sites map under
    application of cluster group operations, by index into the list of cluster sites.
    It satisfies:

    .. code-block:: Python

        from libcasm.xtal import IntegralSiteCoordinateRep
        from libcasm.sym_info import SymGroup
        from libcasm.clusterography import (
            Cluster,
            make_integral_site_coordinate_symgroup_rep,
            make_cluster_group,
        )
        from libcasm.configuration import Prim

        # prim: Prim
        # cluster: Cluster
        # cluster_group: SymGroup

        # Get the cluster group and permutation rep:
        factor_group_site_rep = make_integral_site_coordinate_symgroup_rep(
            group_elements=prim.factor_group.elements,
            xtal_prim=prim.xtal_prim,
        )
        cluster_group = make_cluster_group(
            cluster=cluster,
            group=prim.factor_group,
            lattice=prim.xtal_prim.lattice(),
            integral_site_coordinate_symgroup_rep=factor_group_site_rep,
        )
        # cluster_group_site_rep: list[IntegralSiteCoordinateRep]
        cluster_group_site_rep = make_integral_site_coordinate_symgroup_rep(
            group_elements=cluster_group.elements,
            xtal_prim=xtal_prim,
        )
        cluster_permutation_rep = make_cluster_permutation_rep(
            cluster=cluster,
            cluster_group=cluster_group,
            xtal_prim=prim.xtal_prim,
        )


        # assert
        for cluster_group_index in range(len(cluster_group_site_rep)):
            site_rep = cluster_site_rep[cluster_group_index]
            perm_rep = cluster_permutation_rep[cluster_group_index]
            for to_site_index, from_site_index in enumerate(perm_rep):
                assert cluster.site(to_site_index) == \
                    site_rep * cluster.site(from_site_index)


    Parameters
    ----------
    prim: casmconfig.Prim
        The prim.
    cluster: Cluster
        The cluster of sites
    cluster_group: SymGroup
        A group that maps the cluster onto itself. An exception is raised if an
        operation is not a cluster group operation.

    Returns
    -------
    cluster_permutation_rep: list[list[int]]
        The `cluster_permutation_rep` species how cluster sites map under application of
        cluster group operations, by index into the list of cluster sites, according to
        `from_site_index = cluster_permutation_rep[cluster_group_index][to_site_index]`,
        where `cluster_group_index` is an index into ``cluster_group.elements``, and
        `from_site_index` and `to_site_index` are indices into ``cluster.sites()``
        before and after application of the cluster group operation, respectively.

    """
    sites = cluster.sites()
    site_symgroup_rep = make_integral_site_coordinate_symgroup_rep(
        group_elements=cluster_group.elements,
        xtal_prim=prim.xtal_prim,
    )

    def find_site_index(site):
        for test_index, test_site in enumerate(sites):
            if test_site == site:
                return test_index
        raise Exception("Error in make_cluster_permutation_rep: Not a cluster group")

    # Get cluster permutation,
    #     from_site_index = cluster_perm[cluster_group_index][to_site_index]
    cluster_permutation_rep = []
    for site_rep in site_symgroup_rep:
        tperm = [None] * cluster.size()
        for from_site_index, site in enumerate(sites):
            to_site_index = find_site_index(site_rep * site)
            tperm[to_site_index] = from_site_index
        for x in tperm:
            if x is None:
                raise Exception("Error in make_cluster_permutation_rep: failed")
        cluster_permutation_rep.append(tperm)

    return cluster_permutation_rep


def make_equivalence_map_site_rep(
    xtal_prim: xtal.Prim,
    equivalence_map_ops: list[list[xtal.SymOp]],
) -> list[list[xtal.IntegralSiteCoordinateRep]]:
    """Make the :class:`~libcasm.xtal.IntegralSiteCoordinateRep` representation of an
    equivalence map

    Parameters
    ----------
    xtal_prim: xtal.Prim:
        The prim
    equivalence_map_ops: list[list[xtal.SymOp]]
        An orbit equivalence map

    Returns
    -------
    equivalence_map_site_rep: list[list[libcasm.xtal.IntegralSiteCoordinateRep]]
        The :class:`~libcasm.xtal.IntegralSiteCoordinateRep` representation of an
        equivalence map
    """
    equivalence_map_site_rep = []
    for eq_map_ops in equivalence_map_ops:
        equivalence_map_site_rep.append(
            [xtal.IntegralSiteCoordinateRep(op, xtal_prim) for op in eq_map_ops]
        )
    return equivalence_map_site_rep


class MakeVariableName:
    """A class to construct variable names for DoF

    - For continuous DoF, use the :class:`DoFSetBasis` axis names
    - For discrete DoF, use a template string. For example, the default is
      ``"\\phi_{{{b},{m}}}"`` where "{b}" is replaced by the sublattice index and
      "{m}" is replaced by the site function index, a number in the range 0 to M-1,
      where M is the number of occupants allowed on the site.

    """

    def __init__(
        self,
        occ_var_name: Optional[str] = None,
        occ_var_desc: Optional[str] = None,
    ):
        """

        .. rubric:: Constructor

        Parameters
        ----------
        occ_var_name: Optional[str]=None
            A template string for occupation variable names. The default is
            "\\phi_{{{b},{m}}}", where b is the sublattice index and m is the site
            function index.
        occ_var_desc: Optional[str]=None
            A description of the occupation variable, particularly for the meaning of
            the indices. The default is for the default `occ_var_name`.
        """
        if occ_var_name is None:
            occ_var_name = "\\phi_{{{b},{m}}}"
        if occ_var_desc is None:
            occ_var_desc = (
                "\\phi_{{{b},{m}}}, where "
                "$b$ is the sublattice index and "
                "$m$ is the site function index"
            )
        self.occ_var_name = occ_var_name
        self.occ_var_desc = occ_var_desc

    def __call__(
        self,
        xtal_prim: xtal.Prim,
        key: str,
        sublattice_index: Optional[int] = None,
        cluster_site_index: Optional[int] = None,
        component_index: Optional[int] = None,
        site_basis_function_index: Optional[int] = None,
        local_discrete_dof: list[str] = [],
    ) -> str:
        def make_variable_symbol(xtal_prim, key, sublattice_index):
            if sublattice_index is not None:
                dof = xtal_prim.local_dof()[sublattice_index]
            else:
                dof = xtal_prim.global_dof()
            axis_names = None
            for dof_basis_set in dof:
                if dof_basis_set.dofname() == key:
                    axis_names = dof_basis_set.axis_names()
                    break
            if axis_names is None:
                return "x"
            else:
                return axis_names[component_index]

        symbol = make_variable_symbol(xtal_prim, key, sublattice_index)

        if cluster_site_index is not None:
            if key in local_discrete_dof:
                # local discrete
                b = sublattice_index
                m = site_basis_function_index
                return self.occ_var_name.format(b=b, m=m)
            else:
                # local continuous
                return f"{symbol}"
        else:
            # global continuous
            return f"{symbol}"

    def to_dict(self):
        """Represent the MakeVariableName object as a Python dict"""
        return {
            "occ_var_name": self.occ_var_name,
            "occ_var_desc": self.occ_var_desc,
        }

    @staticmethod
    def from_dict(data: dict):
        """Construct a MakeVariableName object from a Python dict"""
        return MakeVariableName(
            occ_var_name=data.get("occ_var_name"),
            occ_var_desc=data.get("occ_var_desc"),
        )


def make_variable_name(
    xtal_prim: xtal.Prim,
    key: str,
    sublattice_index: Optional[int] = None,
    cluster_site_index: Optional[int] = None,
    component_index: Optional[int] = None,
    site_basis_function_index: Optional[int] = None,
    local_discrete_dof: list[str] = [],
):
    f = MakeVariableName()
    return f(
        xtal_prim=xtal_prim,
        key=key,
        sublattice_index=sublattice_index,
        cluster_site_index=cluster_site_index,
        component_index=component_index,
        site_basis_function_index=site_basis_function_index,
        local_discrete_dof=local_discrete_dof,
    )


def make_global_variables(
    prim: casmconfig.Prim,
    key: str,
    make_variable_name_f: Optional[Callable] = None,
):
    """Construct the variable list for a global degree of freedom (DoF)

    Parameters
    ----------
    prim: :class:`~libcasm.configuration.Prim`
        The Prim
    key: str
        The name of the global DoF type. Must exist in `prim`.
    make_variable_name_f: Optional[Callable] = None
        Allows specifying a custom class to construct variable names. The default
        class used is :class:`~casm.bset.cluster_functions.MakeVariableName`.
        Custom classes should have the same `__call__` signature as
        :class:`~casm.bset.cluster_functions.MakeVariableName`, and have
        `occ_var_name` and `occ_var_desc` attributes.

    Returns
    -------
    variables: list[`Variable <casm.bset.polynomial_functions.Variable>`_]
        A list of Variable for each component of DoF of type `key` from each site
        in `cluster`.
    variable_subsets: list[list[int]]
        Lists of variables (as indices into the `variables` list) which mix under
        application of symmetry. For example, if the variables are the 6
        strain components, then `var_subsets=[[0, 1, 2, 3, 4, 5]]`.
    """
    if make_variable_name_f is None:
        make_variable_name_f = make_variable_name

    def find_dof_basis_set(global_dof):
        for _dof_basis_set in global_dof:
            if _dof_basis_set.dofname() == key:
                return _dof_basis_set
        return None

    global_dof = prim.xtal_prim.global_dof()
    dof_basis_set = find_dof_basis_set(global_dof)
    if dof_basis_set is None:
        variables = []
        variable_subsets = [[]]
        return (variables, variable_subsets)

    variables = []
    for component_index, axis_name in enumerate(dof_basis_set.axis_names()):
        variables.append(
            Variable(
                name=make_variable_name_f(
                    xtal_prim=prim.xtal_prim,
                    key=key,
                    component_index=component_index,
                ),
                key=key,
                component_index=component_index,
            )
        )
    variable_subsets = [[i for i in range(len(variables))]]
    return (variables, variable_subsets)


def make_cluster_variables(
    prim: casmconfig.Prim,
    key: str,
    cluster: Cluster,
    make_variable_name_f: Optional[Callable] = None,
    local_discrete_dof: list[str] = [],
):
    """Construct the variable list for a cluster

    Parameters
    ----------
    prim: :class:`~libcasm.configuration.Prim`
        The Prim
    key: str
        The name of the local DoF type. Must exist in `prim`.
    cluster: Cluster
        The cluster of sites with DoF to be transformed by the matrix representations.
    make_variable_name_f: Optional[Callable] = None
        Allows specifying a custom class to construct variable names. The default
        class used is :class:`~casm.bset.cluster_functions.MakeVariableName`.
        Custom classes should have the same `__call__` signature as
        :class:`~casm.bset.cluster_functions.MakeVariableName`, and have
        `occ_var_name` and `occ_var_desc` attributes.
    local_discrete_dof: list[str]
        The types of local discrete degree of freedom (DoF).

    Returns
    -------
    variables: list[`Variable <casm.bset.polynomial_functions.Variable>`_]
        A list of Variable for each component of DoF of type `key` from each site
        in `cluster`.
    variable_subsets: list[list[int]]
        Lists of variables (as indices into the `variables` list) which mix under
        application of symmetry. For example, if the variables are the 3
        displacements on each site in a cluster of 2 sites, then
        `var_subsets=[[0, 1, 2], [3, 4, 5]]`.
    """
    if make_variable_name_f is None:
        make_variable_name_f = make_variable_name

    if key in local_discrete_dof:
        discrete_dof = prim.xtal_prim.occ_dof()
        # TODO: discrete_dof = prim.xtal_prim.discrete_dof(key)

        variables = []
        variable_subsets = []
        variable_index = 0
        for cluster_site_index, integral_site_coordinate in enumerate(cluster.sites()):
            b = integral_site_coordinate.sublattice()
            dof_basis_set = discrete_dof[b]
            site_variable_subset = []
            for site_basis_function_index in range(len(dof_basis_set)):
                variables.append(
                    Variable(
                        name=make_variable_name_f(
                            xtal_prim=prim.xtal_prim,
                            key=key,
                            site_basis_function_index=site_basis_function_index,
                            cluster_site_index=cluster_site_index,
                            sublattice_index=b,
                            local_discrete_dof=local_discrete_dof,
                        ),
                        key=key,
                        cluster_site_index=cluster_site_index,
                        site_basis_function_index=site_basis_function_index,
                    )
                )
                site_variable_subset.append(variable_index)
                variable_index += 1
            variable_subsets.append(site_variable_subset)
        return (variables, variable_subsets)

    else:

        def find_dof_basis_set(local_dof, b):
            for _dof_basis_set in local_dof[b]:
                if _dof_basis_set.dofname() == key:
                    return _dof_basis_set
            return None

        local_dof = prim.xtal_prim.local_dof()
        variables = []
        variable_subsets = []
        variable_index = 0
        for cluster_site_index, integral_site_coordinate in enumerate(cluster.sites()):
            b = integral_site_coordinate.sublattice()
            dof_basis_set = find_dof_basis_set(local_dof, b)
            if dof_basis_set is None:
                continue
            site_variable_subset = []
            for component_index in range(dof_basis_set.basis().shape[1]):
                variables.append(
                    Variable(
                        name=make_variable_name_f(
                            xtal_prim=prim.xtal_prim,
                            key=key,
                            component_index=component_index,
                            cluster_site_index=cluster_site_index,
                            sublattice_index=b,
                            local_discrete_dof=local_discrete_dof,
                        ),
                        key=key,
                        cluster_site_index=cluster_site_index,
                        component_index=component_index,
                    )
                )
                site_variable_subset.append(variable_index)
                variable_index += 1
            variable_subsets.append(site_variable_subset)
        return (variables, variable_subsets)


def make_equivalence_map_clusters(
    orbit: list[Cluster],
    equivalence_map_site_rep: list[list[xtal.IntegralSiteCoordinateRep]],
):
    """Generate the clusters that result from applying equivalence map operations to the
    prototype cluster, without permutation

    Parameters
    ----------
    orbit: list[Cluster]
        The orbit of clusters
    equivalence_map_site_rep: list[list[xtal.IntegralSiteCoordinateRep]]
        Site representations (xtal.IntegralSiteCoordinateRep) for each equivalence map
        operation.

    Returns
    -------
    equivalence_map_clusters: list[list[Cluster]]
        The clusters generated from applying equivalence map operations to the
        prototype cluster (``orbit[0]``), without any permutation. The generated
        clusters, ``equivalence_map_clusters[i][j]``, are equivalent to orbit
        element ``orbit[i]`` up to a permutation.


    """
    if len(orbit) == 0:
        raise Exception("Error in make_equivalence_map_matrix_rep: len(orbit)==0")
    prototype_cluster = orbit[0]
    equivalence_map_clusters = []
    for i_equiv, cluster in enumerate(orbit):
        clusters = []
        for site_rep in equivalence_map_site_rep[i_equiv]:
            # Make equivalence map cluster (no permutations)
            clusters.append(site_rep * prototype_cluster)
        equivalence_map_clusters.append(clusters)
    return equivalence_map_clusters


def make_cluster_matrix_rep_no_permutation(
    local_dof_matrix_rep: list[list[np.ndarray]],
    cluster: Cluster,
    prim_factor_group: SymGroup,
    prim_factor_group_index: int,
    site_rep: xtal.IntegralSiteCoordinateRep,
    total_dim: int,
    site_index_to_basis_index: dict[int, int],
):
    """Generate the cluster matrix representation, for a single DoF, for a single
    symmetry operation, without permutation amongst the cluster.

    Notes
    -----
    This function is used to make matrix representations of symmetr operations that can
    transform polynomial functions that have already been generated.

    It doesn't include permutations amongst sites on the same cluster, so it can't
    be used in generating the polynomial functions on the prototype cluster in the
    first place.

    Instead, the transformed cluster, with sites transformed but not permuted is also
    generated to allow proper DoF indexing.

    Parameters
    ----------
    local_dof_matrix_rep: list[list[np.ndarray]]
        The local DoF matrix reps, `M`, for each operation in the prim factor group,
        for each sublattice,
        ``M = local_dof_matrix_rep[prim_factor_group_index][sublattice_index]``.
    cluster: Cluster
        The initial cluster, before applying the symmetry operation
    prim_factor_group: SymGroup
        The prim factor group
    prim_factor_group_index: int
        The prim factor group index of the symmetry operation to make the matrix
        representation for.
    site_rep: xtal.IntegralSiteCoordinateRep
        Site representation for the symmetry operation.
    total_dim: int
        The total dimension of the resulting cluster matrix reps.
    site_index_to_basis_index: dict[int, int]
        Specifies the beginning row or column, `basis_index`, in the cluster matrix rep
        for each site in the cluster,
        ``basis_index = site_index_to_basis_index[site_index]``.

    Returns
    -------
    matrix_rep: np.ndarray[np.float64[total_dim,total_dim]]
        Matrix representations for the symmetry operation.

    inv_matrix_rep: np.ndarray[np.float64[total_dim,total_dim]]
        Matrix representations for the inverse operation of the symmetry operation.

    equiv_cluster: Cluster
        The cluster generated from the symmetry operation to
        `prototype_cluster`, without any permutation.

    """
    # Make equivalence map matrix rep (no permutations)
    matrix_rep = np.zeros((total_dim, total_dim))
    for site_index in range(cluster.size()):
        b = cluster.site(site_index).sublattice()
        U = local_dof_matrix_rep[prim_factor_group_index][b]
        pos = site_index_to_basis_index[site_index]
        dim = U.shape[0]
        matrix_rep[pos : pos + dim, pos : pos + dim] = U

    # Make equivalence map inverse matrix rep (no permutations)
    inv_prim_factor_group_index = prim_factor_group.inv(prim_factor_group_index)
    inv_matrix_rep = np.zeros((total_dim, total_dim))
    for site_index in range(cluster.size()):
        b = cluster.site(site_index).sublattice()
        U = local_dof_matrix_rep[inv_prim_factor_group_index][b]
        pos = site_index_to_basis_index[site_index]
        dim = U.shape[0]
        inv_matrix_rep[pos : pos + dim, pos : pos + dim] = U

    # Make equivalence map cluster (no permutations)
    equiv_cluster = site_rep * cluster

    return (matrix_rep, inv_matrix_rep, equiv_cluster)


def make_equivalence_map_matrix_rep(
    local_dof_matrix_rep: list[list[np.ndarray]],
    prototype_cluster: Cluster,
    symgroup: SymGroup,
    equivalence_map_indices: list[list[int]],
    equivalence_map_site_rep: list[list[xtal.IntegralSiteCoordinateRep]],
    total_dim: int,
    site_index_to_basis_index: dict[int, int],
):
    """Generate the cluster matrix representation and cluster for each equivalence map
    operation, for a single DoF

    Parameters
    ----------
    local_dof_matrix_rep: list[list[np.ndarray]]
        The local DoF matrix reps, `M`, for each operation in the prim factor group,
        for each sublattice,
        ``M = local_dof_matrix_rep[prim_factor_group_index][sublattice_index]``.
    prototype_cluster: Cluster
        The prototype cluster
    symgroup: SymGroup
        The symmetry group used to generate the orbit. May be the prim factor group or
        a direct subgroup (meaning symgroup.head_group is the prim factor group).
    equivalence_map_indices: list[list[int]]
        The indices of elements in `symgroup` elements list associated with each
        equivalence map operation.
    equivalence_map_site_rep: list[list[xtal.IntegralSiteCoordinateRep]]
        Site representations (xtal.IntegralSiteCoordinateRep) for each equivalence map
        operation.
    total_dim: int
        The total dimension of the resulting cluster matrix reps.
    site_index_to_basis_index: dict[int, int]
        Specifies the beginning row or column, `basis_index`, in the cluster matrix rep
        for each site in the cluster,
        ``basis_index = site_index_to_basis_index[site_index]``.

    Returns
    -------
    equivalence_map_matrix_rep: \
    list[list[np.ndarray[np.float64[total_dim,total_dim]]]]
        Matrix representations for equivalence map operations.

    equivalence_map_inv_matrix_rep: \
    list[list[np.ndarray[np.float64[total_dim,total_dim]]]]
        Matrix representations for the inverse operation of equivalence map operations.

    equivalence_map_clusters: list[list[Cluster]]
        The clusters generated from applying equivalence map operations to the
        prototype cluster without any permutation. The generated
        clusters, ``equivalence_map_clusters[i][j]``, are equivalent to orbit
        element ``orbit[i]`` up to a permutation.


    """
    ## Build equivalence map op matrix reps, without permutation
    equivalence_map_matrix_rep = []
    equivalence_map_inv_matrix_rep = []
    equivalence_map_clusters = []
    prim_factor_group = symgroup.head_group
    if prim_factor_group is None:
        prim_factor_group = symgroup
    prim_factor_group_index_list = symgroup.head_group_index
    for i_equiv in range(len(equivalence_map_indices)):
        matrix_rep = []
        inv_matrix_rep = []
        clusters = []
        for i_op in range(len(equivalence_map_indices[i_equiv])):
            # Make equivalence map matrix rep (no permutations)
            symgroup_index = equivalence_map_indices[i_equiv][i_op]
            prim_factor_group_index = prim_factor_group_index_list[symgroup_index]
            site_rep = equivalence_map_site_rep[i_equiv][i_op]

            (
                _matrix_rep,
                _inv_matrix_rep,
                _equiv_cluster,
            ) = make_cluster_matrix_rep_no_permutation(
                local_dof_matrix_rep=local_dof_matrix_rep,
                cluster=prototype_cluster,
                prim_factor_group=prim_factor_group,
                prim_factor_group_index=prim_factor_group_index,
                site_rep=site_rep,
                total_dim=total_dim,
                site_index_to_basis_index=site_index_to_basis_index,
            )

            matrix_rep.append(_matrix_rep)
            inv_matrix_rep.append(_inv_matrix_rep)
            clusters.append(_equiv_cluster)

        equivalence_map_matrix_rep.append(matrix_rep)
        equivalence_map_inv_matrix_rep.append(inv_matrix_rep)
        equivalence_map_clusters.append(clusters)
    return (
        equivalence_map_matrix_rep,
        equivalence_map_inv_matrix_rep,
        equivalence_map_clusters,
    )


def make_phenomenal_generating_matrix_rep(
    generating_group: casmsyminfo.SymGroup,
    local_dof_matrix_rep: list[list[np.ndarray]],
    equivalence_map_clusters: list[list[Cluster]],
    phenomenal_generating_indices: list[int],
    phenomenal_generating_site_rep: list[xtal.IntegralSiteCoordinateRep],
    total_dim: int,
    site_index_to_basis_index: dict[int, int],
):
    """Generate the cluster matrix representation and cluster for each symmetry 
    operation that generates a distinct local cluster expansion, for a single DoF

    Notes
    -----

    Proper usage of the results of this method to construct equivalent local cluster
    expansions depends on the following sequence:

    1. Cluster functions are constructed on the prototype local cluster
    2. Cluster functions and equivalent local clusters are generated for the equivalent
       local clusters in the prototype local cluster expansion using
       equivalence_map_inv_matrix_rep
    3. Cluster functions and equivalent local clusters are generated for each
       equivalent local cluster expansions by applying
       phenomenal_generating_inv_matrix_rep to the results of step 2.

    Parameters
    ----------
    generating_group: libcasm.sym_info.SymGroup
        The generating group. The head group of the generating group, which is
        required to be the prim factor group, is used to generate the equivalent
        local basis sets.
    local_dof_matrix_rep: list[list[np.ndarray]]
        The local DoF matrix reps, `M`, for each operation in the prim factor group,
        for each sublattice,
        ``M = local_dof_matrix_rep[prim_factor_group_index][sublattice_index]``.
    equivalence_map_clusters: list[list[libcasm.clusterography.Cluster]]
        The clusters generated from applying equivalence map operations to the
        prototype cluster without any permutation.
    phenomenal_generating_indices: list[int]
        The head group indices for each local basis set generating operation. In the
        vast majority of cases, the head group of the generating group is the prim
        factor group.
    phenomenal_generating_site_rep: list[xtal.IntegralSiteCoordinateRep]
        Site representations (xtal.IntegralSiteCoordinateRep) for each local basis
        set generating operation.
    total_dim: int
        The total dimension of the resulting cluster matrix reps.
    site_index_to_basis_index: dict[int, int]
        Specifies the beginning row or column, `basis_index`, in the cluster matrix rep
        for each site in the cluster,
        ``basis_index = site_index_to_basis_index[site_index]``.

    Returns
    -------
    phenomenal_generating_matrix_rep: \
    list[list[np.ndarray[np.float64[total_dim,total_dim]]]]
        Matrix representations for phenomenal generating operations. Indexing is
        ``phenomenal_generating_matrix_rep[i_clex][i_cluster]`.

    phenomenal_generating_inv_matrix_rep: \
    list[list[np.ndarray[np.float64[total_dim,total_dim]]]]
        Matrix representations for the inverse operation of phenomenal generating
        operations. Indexing is
        ``phenomenal_generating_inv_matrix_rep[i_clex][i_cluster]`.

    basis_set_clusters: list[list[Cluster]]
        The clusters generated from applying phenomenal generating operations to the
        prototype cluster, without any permutation. Indexing is
        ``basis_set_clusters[i_clex][i_cluster]`.


    """
    ## Build equivalence map op matrix reps, without permutation
    phenomenal_generating_matrix_rep = []
    phenomenal_generating_inv_matrix_rep = []
    basis_set_clusters = []
    prim_factor_group = generating_group.head_group
    if prim_factor_group is None:
        raise Exception(
            "Error in make_phenomenal_generating_matrix_rep: "
            "generating_group.head_group is None"
        )
    for i_clex in range(len(phenomenal_generating_indices)):
        matrix_rep = []
        inv_matrix_rep = []
        clusters = []

        # Make phenomenal generating matrix rep (no permutations)
        prim_factor_group_index = phenomenal_generating_indices[i_clex]
        site_rep = phenomenal_generating_site_rep[i_clex]

        for i_clust in range(len(equivalence_map_clusters)):
            (
                _matrix_rep,
                _inv_matrix_rep,
                _equiv_cluster,
            ) = make_cluster_matrix_rep_no_permutation(
                local_dof_matrix_rep=local_dof_matrix_rep,
                cluster=equivalence_map_clusters[i_clust][0],
                prim_factor_group=prim_factor_group,
                prim_factor_group_index=prim_factor_group_index,
                site_rep=site_rep,
                total_dim=total_dim,
                site_index_to_basis_index=site_index_to_basis_index,
            )

            matrix_rep.append(_matrix_rep)
            inv_matrix_rep.append(_inv_matrix_rep)
            clusters.append(_equiv_cluster)

        phenomenal_generating_matrix_rep.append(matrix_rep)
        phenomenal_generating_inv_matrix_rep.append(inv_matrix_rep)
        basis_set_clusters.append(clusters)
    return (
        phenomenal_generating_matrix_rep,
        phenomenal_generating_inv_matrix_rep,
        basis_set_clusters,
    )


def make_cluster_matrix_rep(
    local_dof_matrix_rep: list[list[np.ndarray]],
    cluster: Cluster,
    cluster_group: SymGroup,
    cluster_perm_rep: list[list[int]],
    total_dim: int,
    site_index_to_basis_index: dict[int, int],
):
    """Make the matrix representation for the cluster group, for a single DoF

    Parameters
    ----------
    local_dof_matrix_rep: list[list[np.ndarray]]
        The local DoF matrix reps, `M`, for each prim factor group operation, for each
        sublattice,
        ``M = local_dof_matrix_rep[prim_factor_group_index][sublattice_index]``.
    cluster: Cluster
        The cluster
    cluster_group: SymGroup
        The cluster group
    cluster_perm_rep: list[list[int]]
        The cluster permute representation,
        `from_site_index = cluster_permutation_rep[cluster_group_index][to_site_index]`.
    total_dim: int
        The total dimension of the resulting cluster matrix reps.
    site_index_to_basis_index: dict[int, int]
        Specifies the beginning row or column, `basis_index`, in the cluster matrix rep
        for each site in the cluster,
        ``basis_index = site_index_to_basis_index[site_index]``.

    Returns
    -------
    cluster_matrix_rep: list[np.ndarray[np.float64[total_dim, total_dim]]]
        The matrix representation for each element of the cluster group, including
        proper permutation.
    """

    # Make matrix rep, by filling in blocks with site matrix reps
    cluster_matrix_rep = []
    for cluster_group_index, prim_factor_group_index in enumerate(
        cluster_group.head_group_index
    ):
        trep = np.zeros((total_dim, total_dim))
        perm_rep = cluster_perm_rep[cluster_group_index]
        for to_site_index in range(cluster.size()):
            from_site_index = perm_rep[to_site_index]
            from_site_b = cluster.site(from_site_index).sublattice()
            U = local_dof_matrix_rep[prim_factor_group_index][from_site_b]

            row = site_index_to_basis_index[to_site_index]
            col = site_index_to_basis_index[from_site_index]
            dim = U.shape[0]
            trep[row : row + dim, col : col + dim] = U

        cluster_matrix_rep.append(trep)

    return cluster_matrix_rep


def make_occ_site_functions_matrix_rep(
    indicator_matrix_rep: list[list[np.ndarray]],
    integral_site_coordinate_symgroup_rep: list[xtal.IntegralSiteCoordinateRep],
    occ_site_functions: Optional[list[dict]] = None,
) -> list[list[np.ndarray]]:
    """Returns the symmetry group representation that describes how occupation site \
    functions transform under symmetry.

    Parameters
    ----------
    indicator_matrix_rep: list[list[np.ndarray]]
        The occupation indicator variable matrix representations, where the array
        `indicator_matrix_rep[prim_factor_group_index][sublattice_index]` transforms
        occupation indicator variables on the sublattice_index-th sublattice, by the
        prim_factor_group_index-th operation, to the indicator variables on the
        sublattice that the operation maps the occupants to.
    integral_site_coordinate_symgroup_rep: list[xtal.IntegralSiteCoordinateRep]
        Representation of the prim factor group for transforming
        :class:`libcasm.xtal.IntegralSiteCoordinate`.
    key: str
        The DoF key (i.e. "occ").
    occ_site_functions: Optional[list[dict]] = None
        List of occupation site basis functions. For each sublattice with discrete
        site basis functions, must include:

        - `"sublattice_index"`: int, index of the sublattice
        - `"value"`: list[list[float]], list of the site basis function values,
          as ``value[function_index][occupant_index]``.
        
    Returns
    -------
    occ_site_functions_matrix_rep: list[list[np.ndarray]]
        The array `local_dof_matrix_rep[prim_factor_group_index][sublattice_index]` is
        the matrix representation for transforming occupation site basis functions,
        on the sublattice_index-th sublattice, by the prim_factor_group_index-th
        operation, to the occupation site basis functions on the sublattice that the
        operation maps the occupants to.
    """
    site_rep = integral_site_coordinate_symgroup_rep

    # P = B * Phi, P: indicator functions (as rows), Phi: site functions (as rows)

    # Get Phi and Phi^-1 for each sublattice
    phi = []
    phi_inv = []
    constant_function_index = []
    for sublattice_index, indicator_rep in enumerate(indicator_matrix_rep[0]):
        site_functions = get_occ_site_functions(
            occ_site_functions=occ_site_functions,
            sublattice_index=sublattice_index,
        )

        # Check for constant site function
        if site_functions.shape == (0, 0):
            constant_function_index.append(None)
        else:
            found_constant_function_index = False
            for function_index, site_function in enumerate(site_functions):
                if (site_function == 1.0).all():
                    found_constant_function_index = True
                    constant_function_index.append(function_index)
            if found_constant_function_index is False:
                raise ValueError(
                    "Error in make_occ_site_functions_matrix_rep: "
                    "No constant function found for the occupation site basis "
                    f"functions on sublattice {sublattice_index}."
                )

        phi.append(site_functions)
        phi_inv.append(np.linalg.inv(site_functions))

    # Generate the matrix rep for transforming phi, M_phi,
    # from the matrix rep for transforming indicator functions, M_indicator:
    #     M_phi[b_init] = phi[b_final] * M_indicator[b_init] * phi_inv[b_init]
    occ_site_functions_matrix_rep = []
    mixing = False
    for prim_factor_group_index, indicator_op_rep in enumerate(indicator_matrix_rep):
        site_functions_op_rep = []
        for sublattice_index, indicator_rep in enumerate(indicator_op_rep):
            b = sublattice_index
            site = xtal.IntegralSiteCoordinate(b, [0, 0, 0])
            site_final = site_rep[prim_factor_group_index] * site
            b_final = site_final.sublattice()
            if phi[b_final].shape != phi_inv[b].shape:
                raise Exception(
                    "Error in make_occ_site_functions_matrix_rep: "
                    "phi[b_final].shape != phi_inv[b].shape"
                )
            if phi[b_final].shape == (0, 0):
                site_functions_op_rep.append(np.zeros((0, 0)))
                continue
            site_function_rep = phi[b_final] @ indicator_rep @ phi_inv[b]

            x = site_function_rep[:, constant_function_index[b]]
            if np.isclose(x, 0.0).sum() != len(x) - 1:
                mixing = True

            site_functions_op_rep.append(site_function_rep)
        occ_site_functions_matrix_rep.append(site_functions_op_rep)

    if mixing:
        print()
        print(
            "\n"
            "**** Error in make_occ_site_functions_matrix_rep: **********************\n"
            "* Invalid choice of occupation DoF site basis functions.               *\n"
            "* The constant function is mixing with non-constant functions.         *\n"
            "* Try using chebychev site basis functions or an isotropic default     *\n"
            "* occupant.                                                            *\n"
            "************************************************************************\n"
            "\n"
        )

        print("Occupation site basis functions:")
        for sublattice_index, indicator_rep in enumerate(indicator_matrix_rep[0]):
            print(f"~ sublattice_index: {sublattice_index} ~")
            site_functions = get_occ_site_functions(
                occ_site_functions=occ_site_functions,
                sublattice_index=sublattice_index,
            )
            print(site_functions)
            print()
        print()

        print("Site function matrix reps:")
        for i_fg, site_functions_op_rep in enumerate(occ_site_functions_matrix_rep):
            print(f"~~~ prim_factor_group_index: {i_fg} ~~~")
            for b, site_function_rep in enumerate(site_functions_op_rep):
                print(f"~ sublattice_index: {b} ~")
                x = site_function_rep[:, constant_function_index[b]]
                if np.isclose(x, 0.0).sum() != len(x) - 1:
                    print("********** Mixing **********")
                print("M:\n", site_function_rep)
                print()

        raise ValueError(
            "Error in make_occ_site_functions_matrix_rep: "
            "Invalid choice of occupation DoF site basis functions. "
            "The constant function is mixing with non-constant functions. "
            "Try using chebychev site basis functions."
        )

    return occ_site_functions_matrix_rep


class ClusterMatrixRepBuilder:
    """Builds cluster matrix representations of symmetry operations for generating \
    symmetry adapted polynomial functions on a particular cluster, for a single local \
    degree of freedom (DoF)

    Notes
    -----

    - ClusterMatrixRepBuilder builds the matrix representations for a single
      local degree of freedom for a given cluster.
    - The resulting matrices are block matrices that properly permute DoF amongst the
      cluster sites for the generating group operations which leave the cluster
      invariant (up to a permutation of sites).
    - The component blocks are the matrix representations for the local DoF values on
      a particular sublattice:

      - For continuous local DoF, the matrix representations for each sublattice are
        given by :func:`~libcasm.configuration.Prim.local_dof_matrix_rep`.
      - For discrete local DoF,
        :func:`~casm.bset.cluster_functions.make_occ_site_functions_matrix_rep` is
        used to construct the matrix representations for the occupation site basis
        functions given by `occ_site_functions` from the indicator variable
        representations given by
        :func:`~libcasm.configuration.Prim.local_dof_matrix_rep`.

    - For coupled cluster functions, block diagonal matrix representations can be built
      (i.e. using ``scipy.linalg.block_diag(*_all_matrices)``) from a list containing,
      for a single symmetry operation, the representations for global DoF given by
      :func:`~libcasm.configuration.Prim.global_dof_matrix_rep` followed by the
      representations for each local DoF.

    """

    def __init__(
        self,
        prim: casmconfig.Prim,
        generating_group: casmsyminfo.SymGroup,
        key: str,
        cluster: Cluster,
        phenomenal: Optional[Cluster] = None,
        make_variable_name_f: Optional[Callable] = None,
        local_discrete_dof: Optional[list[str]] = None,
        occ_site_functions: Optional[list[dict]] = None,
    ):
        """

        .. rubric:: Constructor

        Parameters
        ----------
        prim: casmconfig.Prim
            The prim.
        generating_group: casmsyminfo.SymGroup
            The symmetry group
        key: str
            The degree of freedom (DoF) to build the matrix representations for.
        cluster: Cluster
            The cluster on which to build the matrix representation
        phenomenal: Optional[Cluster] = None
            For local cluster functions, specifies the sites about which
            local-clusters orbits are generated. The phenomenal cluster must be chosen
            from one of the equivalents that is generated by
            :func:`~libcasm.clusterography.make_periodic_orbit` using the prim factor
            group.
        make_variable_name_f: Optional[Callable] = None
            Allows specifying a custom class to construct variable names. The default
            class used is :class:`~casm.bset.cluster_functions.MakeVariableName`.
            Custom classes should have the same `__call__` signature as
            :class:`~casm.bset.cluster_functions.MakeVariableName`, and have
            `occ_var_name` and `occ_var_desc` attributes.
        local_discrete_dof: Optional[list[str]] = None
            The types of local discrete degree of freedom (DoF). If `key` is in
            `local_discrete_dof`, then :func:`make_occ_site_functions_matrix_rep` is
            used to construct the matrix representations for the occupation site basis
            functions given by `occ_site_functions`.
        occ_site_functions: Optional[list[dict]] = None
            List of occupation site basis functions. For each sublattice with discrete
            site basis functions, must include:

            - `"sublattice_index"`: int, index of the sublattice
            - `"value"`: list[list[float]], list of the site basis function values,
              as ``value[function_index][occupant_index]``.
        """
        if generating_group is not prim.factor_group:
            if generating_group.head_group is not prim.factor_group:
                raise Exception(
                    "Error in OrbitMatrixRepBuilder: "
                    "generating_group is not prim.factor_group and "
                    "generating_group.head_group is not prim.factor_group."
                )

        if local_discrete_dof is None:
            local_discrete_dof = []

        ## Constructor parameters ##
        self.prim = prim
        """libcasm.configuration.Prim: The prim, with symmetry information."""

        self.generating_group = generating_group
        """libcasm.sym_info.SymGroup: The symmetry group to build matrix \
        representations for."""

        self.key = key
        """str: The degree of freedom (DoF) to build the matrix representations for."""

        self.cluster = cluster
        """libcasm.clusterography.Cluster: The cluster on which to build the matrix \
        representations."""

        self.phenomenal = phenomenal
        """Optional[libcasm.clusterography.Cluster]: For local cluster functions, \
        specifies the sites about which local-clusters orbits are generated. 
        
        The phenomenal cluster must be chosen from one of the equivalents that is
        generated by :func:`~libcasm.clusterography.make_periodic_orbit` using the 
        prim factor group."""

        ## Build cluster matrix rep ##
        generating_group_site_rep = make_integral_site_coordinate_symgroup_rep(
            group_elements=generating_group.elements,
            xtal_prim=prim.xtal_prim,
        )
        if key in local_discrete_dof:
            if occ_site_functions is None:
                raise Exception(
                    "Error in ClusterMatrixRepBuilder: "
                    "occ_site_functions is None for discrete DoF."
                )

            # # DEBUG:
            # indicator_matrix_rep = prim.local_dof_matrix_rep(key)
            # for i_fg, sublat_rep in enumerate(indicator_matrix_rep):
            #     print(f"~~~ fg: {i_fg} ~~~")
            #     for i_sublat, M in enumerate(sublat_rep):
            #         print(f"~ b: {i_sublat} ~")
            #         print(M)
            #         print()

            # For discrete DoF, we need to construct the matrix rep for the
            # site basis functions actually being used from the matrix rep
            # for the indicator variables
            local_dof_matrix_rep = make_occ_site_functions_matrix_rep(
                indicator_matrix_rep=prim.local_dof_matrix_rep(key),
                integral_site_coordinate_symgroup_rep=prim.integral_site_coordinate_symgroup_rep,
                occ_site_functions=occ_site_functions,
            )
        else:
            local_dof_matrix_rep = prim.local_dof_matrix_rep(key)

        if self.phenomenal is None:
            cluster_group = make_cluster_group(
                cluster=cluster,
                group=generating_group,
                lattice=prim.xtal_prim.lattice(),
                integral_site_coordinate_symgroup_rep=generating_group_site_rep,
            )
        else:
            cluster_group = make_local_cluster_group(
                cluster=cluster,
                phenomenal_group=generating_group,
                integral_site_coordinate_symgroup_rep=generating_group_site_rep,
            )
        cluster_perm_rep = make_cluster_permutation_rep(
            prim=prim,
            cluster=cluster,
            cluster_group=cluster_group,
        )
        variables, variable_subsets = make_cluster_variables(
            prim=prim,
            key=key,
            cluster=cluster,
            make_variable_name_f=make_variable_name_f,
            local_discrete_dof=local_discrete_dof,
        )
        site_index_to_basis_index, total_dim = make_cluster_dof_info(
            cluster, local_dof_matrix_rep
        )

        cluster_matrix_rep = make_cluster_matrix_rep(
            local_dof_matrix_rep=local_dof_matrix_rep,
            cluster=cluster,
            cluster_group=cluster_group,
            cluster_perm_rep=cluster_perm_rep,
            total_dim=total_dim,
            site_index_to_basis_index=site_index_to_basis_index,
        )

        ## Generated data ##
        self.dof_matrix_rep = local_dof_matrix_rep
        """list[list[np.ndarray]]: The matrix representations for transforming site \
        variables by prim factor group operations.
        
        The array ``M = dof_matrix_rep[i_factor_group][i_sublat_init]`` specifies that 
        the site variables transform according to
        ``x_final = M @ x_init``, where `x_init` are the site variables on an initial 
        site on the `i_sublat_init`-th sublattice and `x_final` are the site variables
        on the final site under the application of the `i_factor_group`-th prim factor
        group operation.
        
        For example, for occupation DoF, these are the matrix representations 
        that transform the site basis functions, not the indicator functions.
        """

        self.cluster_group = cluster_group
        """libcasm.sym_info.SymGroup: The subgroup of the generating group that leaves \
        `cluster` invariant.
        
        If this is for periodic cluster expansion (`phenomenal` is None), this 
        includes the cluster group elements may differ by a translation from the
        elements in `generating_group`. If this is for a local cluster expansion
        (`phenomenal` is not None), no additional translation can be included."""

        self.cluster_perm_rep = cluster_perm_rep
        """list[int[int]]: The `cluster_perm_rep` species how `cluster` sites permute \
        under application of cluster group operations.
        
        The convention is that 
        ``from_site_index = cluster_perm_rep[cluster_group_index][to_site_index]``,
        where `cluster_group_index` is an index into ``cluster_group.elements``, and
        `from_site_index` and `to_site_index` are indices into ``cluster.sites()``
        before and after application of the cluster group operation, respectively."""

        self.cluster_matrix_rep = cluster_matrix_rep
        """list[numpy.ndarray[numpy.float64[total_dim, total_dim]]]: The matrix \
        representations for transforming cluster site DoF values by cluster group \
        operations. 
        
        The array ``M = cluster_matrix_rep[cluster_group_index]`` specifies that a 
        vector of cluster site DoF values transforms under the application of the 
        `cluster_group_index`-th cluster group operation according to 
        ``x_after = M @ x_before.``"""

        self.variables = variables
        """list[casm.bset.polynomial_functions.Variable]:  The variables associated \
        with each element of the vector of cluster site DoF that can be transformed by \
        the cluster matrix representations."""

        self.variable_subsets = variable_subsets
        """list[list[int]]: Lists of variables (as indices into the `variables` list) \
        which mix under application of symmetry. 
        
        For example, if all variables are the 6 strain variables, then 
        `var_subsets=[[0,1,2,3,4,5]]`. If the variables are the 3 displacements on each 
        site in a cluster of 2 sites, then `variable_subsets=[[0, 1, 2], [3, 4, 5]]`."""

        self.site_index_to_basis_index = site_index_to_basis_index
        """dict[int, int]: Defines the mapping of cluster site DoF values to the \
        elements of the vectors transformed by the matrix representations.
        
        The beginning row or column, `basis_index`, in the cluster matrix representation
        for each site in the cluster is specified using the convention
        ``basis_index = site_index_to_basis_index[site_index]``."""

        self.total_dim = total_dim
        """int: The total dimension of the resulting cluster DoF vector and cluster \
        matrix reps."""

    def to_dict(self):
        """Represent the ClusterMatrixRepBuilder as a Python dict"""

        # This is primarily intended for use by
        # OrbitMatrixRepBuilder.to_dict(), so some duplicate information is
        # not included.
        return {
            "key": self.key,
            "dof_matrix_rep": [
                [m.tolist() for m in rep] for rep in self.dof_matrix_rep
            ],
            "cluster_group": self.cluster_group.head_group_index,
            "cluster_perm_rep": self.cluster_perm_rep,
            "cluster_matrix_rep": [m.tolist() for m in self.cluster_matrix_rep],
            "variables": [v.to_dict() for v in self.variables],
            "variable_subsets": self.variable_subsets,
            "site_index_to_basis_index": self.site_index_to_basis_index,
            "total_dim": self.total_dim,
        }


class OrbitMatrixRepBuilder:
    """Builds cluster matrix representations of symmetry operations for generating \
    polynomial functions on an orbit of clusters, coupling all local and global DoFs

    Notes
    -----

    OrbitMatrixRepBuilder performs the following steps:

    1. For the `cluster` provided, generate an orbit of equivalent clusters according
       to the operations in the provided symmetry group (`generating_group`).

       - Also generates the "equivalence map" which organizes generating group
         operations by which orbit element they map the prototype cluster onto.
       - If the matrix representations are for a local cluster expansion (if
         `phenomenal` is not None), then the prim factor group operations that generate
         the symmetrically equivalent phenomenal clusters are found and stored as
         "phenomenal generating ops".

    2. For the prototype cluster (the first element in the generated orbit), use
       :class:`~casm.bset.ClusterMatrixRepBuilder` to build matrix representations for
       each local DoF type for each generating group symmetry operation, along with
       vectors of :class:`~casm.bset.polynomial_functions.Variable` representing the
       individual local DoF components.

    3. Build coupled matrix representations (block diagonal matrices) combining the
       matrix representations for global and local DoFs for each generating group
       symmetry operation, along with a vector of
       :class:`~casm.bset.polynomial_functions.Variable` representing all individual
       global and local DoF components.

       - Global DoF matrix representations are obtained for the prim using
         :func:`~libcasm.configuration.Prim.global_dof_matrix_rep` and variables
         are constructed for each global DoF component.
       - Local DoF matrix representations and variables are obtained from step 2.

       The coupled matrix representations are stored organized by which orbit element
       they map the prototype cluster onto, in the same order as the equivalence map
       operations. The inverse matrices, which are the representations used for
       transforming cluster functions, are also constructed.

       The clusters created by transforming the prototype cluster to each equivalent
       cluster in the orbit are also constructed with sites ordered consistently for
       the same vector of variables (though they are now associated with different
       sites).

    3. If the matrix representations are for a local cluster expansion (if 
       `phenomenal` is not None), then for each phenomenal generating op, matrix
       representations are generated that transform DoF values associated with each
       cluster in the original orbit to a symmetrically equivalent cluster in the
       orbit around a symmetrically equivalent phenomenal cluster.

       The clusters created by transforming the cluster in the original orbit by
       the phenomenal generating ops are also constructed with sites ordered
       consistently for the same vector of variables (though they are again associated
       with different sites).


    """

    def __init__(
        self,
        prim: casmconfig.Prim,
        generating_group: casmsyminfo.SymGroup,
        global_dof: list[str],
        local_continuous_dof: list[str],
        local_discrete_dof: list[str],
        cluster: Cluster,
        phenomenal: Optional[Cluster] = None,
        make_variable_name_f: Optional[Callable] = None,
        occ_site_functions: list[dict] = [],
    ):
        """

        Parameters
        ----------
        prim: casmconfig.Prim
            The prim.
        generating_group: casmsyminfo.SymGroup
            The symmetry group for generating cluster functions. For periodic cluster
            functions, this is the prim factor group (usually) or a subgroup. For
            local cluster functions, this is the cluster group of the phenomenal
            cluster or a subgroup (often the subgroup which leaves an
            :class:`~libcasm.occ_events.OccEvent` invariant).
        global_dof: list[str]
            The types of global degree of freedom (DoF) to include in the matrix
            representation.
        local_continuous_dof: list[str]
            The types of local continuous degree of freedom (DoF) to include in the
            matrix representation.
        local_discrete_dof: list[str]
            The types of local discrete degree of freedom (DoF) to include in the
            matrix representation.
        cluster: Cluster
            A cluster in the orbit of clusters on which to generate matrix
            representations.
        phenomenal: Optional[Cluster] = None
            For local cluster functions, specifies the sites about which
            local-clusters orbits are generated. The phenomenal cluster must be chosen
            from one of the equivalents that is generated by
            :func:`~libcasm.clusterography.make_periodic_orbit` using the prim factor
            group.
        make_variable_name_f: Optional[Callable] = None
            Allows specifying a custom class to construct variable names. The default
            class used is :class:`~casm.bset.cluster_functions.MakeVariableName`.
            Custom classes should have the same `__call__` signature as
            :class:`~casm.bset.cluster_functions.MakeVariableName`, and have
            `occ_var_name` and `occ_var_desc` attributes.
        occ_site_functions: Optional[list[dict]] = None
            List of occupation site basis functions. For each sublattice with discrete
            site basis functions, must include:

            - `"sublattice_index"`: int, index of the sublattice
            - `"value"`: list[list[float]], list of the site basis function values,
              as ``value[function_index][occupant_index]``.

        """

        if generating_group is not prim.factor_group:
            if generating_group.head_group is not prim.factor_group:
                raise Exception(
                    "Error in OrbitMatrixRepBuilder: "
                    "the generating group must be the prim factor group "
                    "or a direct subgroup of the prim factor group."
                )

        if phenomenal is not None:
            if generating_group.head_group is None:
                raise Exception(
                    "Error in OrbitMatrixRepBuilder: "
                    "for local orbits, the generating group must be a direct subgroup "
                    "of the prim factor group."
                )

        ### Constructor parameters ###
        self.prim = prim
        """libcasm.configuration.Prim: The prim, with symmetry information."""

        self.generating_group = generating_group
        """libcasm.sym_info.SymGroup: The symmetry group used to construct equivalent \
        clusters and functions."""

        self.global_dof = global_dof
        """list[str]: The types of global degree of freedom (DoF) included in the \
        matrix representation. 
        
        All global DoF are continuous DoF."""

        self.local_continuous_dof = local_continuous_dof
        """list[str]: The types of local discrete degree of freedom (DoF) included \
        in the matrix representation."""

        self.local_discrete_dof = local_discrete_dof
        """list[str]: The types of local discrete degree of freedom (DoF) included \
        in the matrix representation."""

        self.cluster = cluster
        self.phenomenal = phenomenal
        self.make_variable_name_f = make_variable_name_f
        self.occ_site_functions = occ_site_functions
        """Optional[list[dict]]: List of occupation site basis functions. 
        
        For each sublattice with discrete site basis functions, must include:

        - `"sublattice_index"`: int, index of the sublattice
        - `"value"`: list[list[float]], list of the site basis function values,
          as ``value[function_index][occupant_index]``.
        """

        local_dof = local_continuous_dof + local_discrete_dof
        self.local_dof = local_dof
        """list[str]: The types of local continuous and discrete degrees of freedom \
        (DoF) included in the matrix representation.
        """

        ## The following generate all the matrix reps needed for this orbit:

        #
        ## Generate orbit, equivalence map, and cluster group
        #
        self.orbit = None
        """list[libcasm.clusterography.Cluster]: The generated orbit of clusters."""

        self.cluster_group = None
        """libcasm.sym_info.SymGroup: The subgroup of `generating_group` that leaves
        `orbit[0]` invariant."""

        self.equivalence_map_ops = None
        """list[list[libcasm.xtal.SymOp]: Symmetry operations that map the prototype \
        cluster to equivalent clusters.

        The SymOp in the list `equivalence_map_ops[i]` all map `orbit[0]`
        onto the same `i`-th equivalent cluster, including proper translation, up to a
        permutation of sites."""

        self.equivalence_map_indices = None
        """list[list[int]]: Indices into the `generating_group` elements list of \
        the corresponding SymOp in `equivalence_map_ops`."""

        self.equivalence_map_site_rep = None
        """list[list[libcasm.xtal.IntegralSiteCoordinateRep]]: Site transformation \
        representation of the corresponding SymOp in `equivalence_map_ops`."""

        self.equivalence_map_clusters = None
        """list[list[libcasm.clusterography.Cluster]]: The equivalent clusters that \
        the corresponding `equivalence_map_ops` all map ``orbit[0]`` onto.

        The elements of `equivalence_map_clusters` are:

        .. code-block:: Python

            equivalence_map_clusters[i][j] == equivalence_map_site_rep[i][j] * orbit[0]

        The clusters in the list ``equivalence_map_clusters[i]`` all have the same
        sites, but the order of sites may be permuted."""

        self._make_orbit_and_equivalence_map()

        #
        # ## If a local cluster expansion,
        # make equivalent phenomenal cluster generating symmetry operations

        self.phenomenal_generating_ops = None
        """list[libcasm.xtal.SymOp]: Symmetry operations that generate the \
        symmetrically equivalent phenomenal cluster (if a local cluster expansion)."""

        self.phenomenal_generating_indices = None
        """list[int]: Indices of prim factor group elements corresponding to \
        `phenomenal_generating_ops`."""

        self.phenomenal_generating_site_rep = None
        """list[libcasm.xtal.IntegralSiteCoordinateRep]: Symmetry group representation \
        for transforming IntegralSiteCoordinate and Cluster corresponding to 
        `phenomenal_generating_ops`."""

        self._make_phenomenal_generators()

        #
        ## Make global DoF variables, variable subsets,
        # and matrix reps for individual DoF

        self.global_variables = None
        """list[list[casm.bset.polynomial_functions.Variable]]: For each global DoF \
        in `global_dof`, the variables used in functions.

        The variable `global_variables[i_global_dof][i_var]`, is the `i_var`-th 
        global variable of the `i_global_dof`-th global DoF type, where `i_global_dof` 
        is an index into `global_dof`."""

        self.global_variable_subsets = None
        """list[list[list[int]]]: For each global DoF in `global_dof`, the variable \
        subsets.

        The each list in `global_variable_subsets[i_global_dof]` contains the indices
        of variables in `global_variables[i_global_dof]` that can mix under
        application of symmetry. This information is used in the calculation of 
        :func:`~casm.bset.polynomial_functions.monomial_inner_product()`.
        """

        self.global_matrix_rep = None
        R"""list[list[np.ndarray]]:  For each global DoF in `global_dof`, the matrix \
        representation of the prim factor group symmetry operations. 

        These are the matrix representations, :math:`M`, that transform a vector of
        global DoF values according to :math:`\vec{x}' = M \vec{x}`, where :math:`x_j`, 
        corresponds to `global_variables[i_global_dof][j]`. Index using 
        ``global_matrix_rep[i_global_dof][i_factor_group]``, where `i_factor_group` is 
        an index into the prim factor group."""

        self.global_inv_matrix_rep = None
        """list[list[np.ndarray]]: For each global DoF in `global_dof`, the matrix 
        representation of the inverse of corresponding generating group ops. 

        These are the matrix representations that should be used to generate functions \
        of a single global DoF type. Index using 
        ``global_inv_matrix_rep[i_global_dof][i_factor_group]``,
        where `i_factor_group` is an index into the prim factor group."""

        self._make_global_dof_info()

        #
        ## Make local DoF variables, variable subsets,
        # and matrix reps for individual DoF, including cluster matrix reps

        self.local_prototype = None
        """list[casm.bset.cluster_functions.ClusterMatrixRepBuilder]: For each local
        DoF in `local_dof`, the cluster matrix representations and associated
        information for the canonical equivalent cluster.
        """

        self.local_equivalence_map_matrix_rep = None
        R"""list[list[list[np.ndarray]]: For each local DoF in `local_dof`, the cluster
        matrix representation of corresponding `equivalence_map_ops`. 

        These are the matrix representations, :math:`M`, that transform a vector of
        local DoF values, :math:`\vec{x}`, on the prototype cluster,
        `local_prototype[i_local_dof].cluster`, to local DoF values on equivalent 
        clusters in the orbit, :math:`\vec{x}'`, according to 
        :math:`\vec{x}' = M \vec{x}`, where :math:`x_j` for both the prototype and 
        final cluster is specified by the variable
        `local_prototype[i_local_dof].variables[j]`. 

        The matrix representations are indexed using 
        ``local_equivalence_map_matrix_rep[i_local_dof][i_equiv][i_op]``,
        where `i_local_dof` is an index into `local_dof`, and `i_equiv` and `i_op`
        correspond to `equivalence_map_ops[i_equiv][i_op]` specifying the symmetry
        operation being represented and the equivalent cluster that is being mapped to.
        
        For the initial DoF values, :math:`\vec{x}`, the `cluster_site_index`
        of the variables is an index into the sites of
        `local_prototype[i_local_dof].cluster`. For the final DoF values, 
        :math:`\vec{x}'` the `cluster_site_index` of the variables is an index into
        the sites of the cluster (with sites in the proper order) stored in 
        `equivalance_map_clusters[i_equiv][i_op]`.
        """

        self.local_equivalence_map_inv_matrix_rep = None
        """list[list[list[np.ndarray]]: For each local DoF in `local_dof`, the cluster
        matrix representation of the inverse of corresponding `equivalence_map_ops`. 

        These matrix representations, the inverse matrices of 
        `local_equivalence_map_matrix_rep`, transform functions of a single local DoF 
        type on the prototype cluster to functions on a symmetrically equivalent 
        cluster in the orbit. Index using
        ``local_equivalence_map_inv_matrix_rep[i_local_dof][i_equiv][i_op]``."""

        self.local_phenomenal_generating_matrix_rep = None
        R"""list[list[list[np.ndarray]]: For each local DoF in `local_dof`, the cluster
        matrix representation of corresponding `phenomenal_generating_ops`, for each 
        cluster.

        These are the matrix representations, :math:`M`, that transform a vector of
        local DoF values on a cluster in `orbit`, :math:`\vec{x}`, to local DoF values,
        :math:`\vec{x}'`, on a cluster in the symmetrically equivalent orbit for a 
        local cluster expansion for a symmetrically equivalent phenomenal cluster,
        according to :math:`\vec{x}' = M \vec{x}`. The :math:`x_j` for both the initial
        and final cluster is specified by the variable
        `local_prototype[i_local_dof].variables[j]`. 
        
        The matrix representations are indexed using 
        ``local_phenomenal_generating_matrix_rep[i_local_dof][i_clex][i_cluster]``,
        where `i_local_dof` is the index into `local_dof`, `i_clex` is the index 
        into `phenomenal_generating_ops`, and `i_cluster` is the index into
        `orbit`.
        
        The initial cluster is `orbit[i_cluster]`. The final cluster (with sites in 
        the proper order) can be generated using ``site_rep * orbit[i_cluster]``, where 
        ``site_rep = phenomenal_generating_site_rep[i_clex]``."""

        self.local_phenomenal_generating_inv_matrix_rep = None
        """list[list[list[np.ndarray]]: For each local DoF in `local_dof`, the
        cluster matrix representation of the inverse of corresponding
        `phenomenal_generating_ops`, for each cluster.
        
        These matrix representations, the inverse matrices of 
        `local_phenomenal_generating_matrix_rep`, transform a cluster function of
        local DoF values on a cluster in `orbit` to a cluster function of local DoF 
        values on a cluster in the symmetrically equivalent orbit for a 
        local cluster expansion for a symmetrically equivalent phenomenal cluster.
        
        Index using
        ``local_phenomenal_generating_inv_matrix_rep[i_local_dof][i_clex][i_cluster]``,
        where `i_local_dof` is the index into `local_dof`, `i_clex` is the index 
        into `phenomenal_generating_ops`, and `i_cluster` is the index into
        `orbit`.
        
        The initial cluster is `orbit[i_cluster]`. The final cluster (with sites in 
        the proper order) can be generated using ``site_rep * orbit[i_cluster]``, where 
        ``site_rep = phenomenal_generating_site_rep[i_clex]``."""

        self._make_local_dof_info()

        #
        ## Combine individual DoF matrix reps
        # into a coupled matrix rep for the prototype cluster
        # Also, make variables and variable subsets for the coupled cluster functions

        self.prototype_matrix_rep = None
        """list[numpy.ndarray]: The coupled matrix representation of the symmetry
        operations that leave the prototype cluster invariant.

        These are the matrix representations that can be used to transform at the 
        same time all global DoF values and all local DoF values on the prototype 
        cluster to the final global DoF values and the local DoF values on a
        symmetrically equivalent cluster in the orbit.
         
        Index using ``prototype_matrix_rep[i_cluster_group]``, where `i_cluster_group`
        is an index into 
        :py:data:`OrbitMatrixRepBuilder.cluster_group.elements <casm.bset.cluster_functions.OrbitMatrixRepBuilder.cluster_group>`.
        The components of the DoF value vectors these matrices transform are described 
        by the corresponding elements of 
        :py:data:`OrbitMatrixRepBuilder.prototype_variables <casm.bset.cluster_functions.OrbitMatrixRepBuilder.prototype_variables>`.
        """  # noqa

        self.n_global_variables = None
        """int: The total number of global variables."""

        self.n_local_variables = None
        """int: The total number of local variables."""

        self.prototype_variables = None
        """list[casm.bset.polynomial_functions.Variable]: Variables representing all \
        global and local DoF included in coupled cluster functions on the prototype \
        cluster.

        The variables associated with each element of the vector of global DoF values 
        and prototype cluster site DoF values that can be transformed by the matrix 
        representations in `prototype_matrix_rep` and `equivalence_map_matrix_rep`.
        Global variables are included first, in the order specified by `global_dof`,
        followed by cluster site variables, in the order specified by `local_dof`."""

        self.prototype_variable_subsets = None
        """list[list[int]]: Lists of variables (as indices into the \
        `prototype_variables` list) which mix under application of symmetry. 

        For example, if all variables are the 6 strain variables, then 
        `var_subsets=[[0,1,2,3,4,5]]`. If the variables are the 3 displacements on 
        each site in a cluster of 2 sites, then 
        `variable_subsets=[[0,1,2], [3,4,5]]`. If those strain and displacement
        variables are coupled, with strain variables included first, then
        `variable_subsets=[[0,1,2,3,4,5], [6,7,8], [9,10,11]]`"""

        self._make_coupled_prototype_matrix_rep_and_variables()

        #
        ## Build equivalence map matrix reps
        # Build matrix reps which
        # transform cluster functions generated on the prototype cluster
        # to other clusters in the orbit

        self.equivalence_map_matrix_rep = None
        """list[list[numpy.ndarray]]: The coupled matrix rep of corresponding \
        `equivalence_map_ops`.

        These are the matrix representations that can be used to transform at the same
        time global DoF values and local DoF values from the prototype cluster onto
        equivalent clusters. Index using 
        ``equivalence_map_matrix_rep[i_equiv][i_op]``."""

        self.equivalence_map_inv_matrix_rep = None
        """list[list[numpy.ndarray]]: The inverse of the coupled matrix rep of \
        corresponding `equivalence_map_ops`.

        These are the matrix representations that should be used to generate coupled
        functions on the equivalent clusters from coupled functions on the prototype
        cluster. Index using ``equivalence_map_inv_matrix_rep[i_equiv][i_op]``."""

        self._make_equivalence_map_matrix_rep()

        #
        ## If a local cluster expansion,
        # Build phenomenal generating matrix reps which
        # transform cluster functions on all local clusters in the orbit
        # to cluster functions on a different but equivalent orbit of local clusters
        # around a symmetrically equivalent phenomenal cluster

        self.phenomenal_generating_matrix_rep = None
        """list[list[numpy.ndarray]]: The coupled matrix rep of corresponding \
        `phenomenal_generating_ops`, for each cluster. 

        These are the matrix representations that can be used to transform at the same 
        time global DoF values and local DoF values from clusters in the original 
        local-cluster orbit to local-clusters in the orbit for a symmetrically
        equivalent phenomenal cluster. Index using 
        ``phenomenal_generating_matrix_rep[i_clex][i_cluster]``, where 
        `i_clex` is the index into `phenomenal_generating_ops`, and `i_cluster` is the
        index into `orbit` of the initial cluster."""

        self.phenomenal_generating_inv_matrix_rep = None
        """list[list[numpy.ndarray]]: The inverse of the coupled matrix rep of \
        corresponding `phenomenal_generating_ops`, for each cluster.

        These are the matrix representations that should be used to generate coupled
        functions on the local-clusters in the orbit for a symmetrically equivalent
        phenomenal cluster from local-cluster functions in the original orbit. Index 
        using ``phenomenal_generating_inv_matrix_rep[i_clex][i_cluster]``, where 
        `i_clex` is the index into `phenomenal_generating_ops`, and `i_cluster` is the 
        index into `orbit` of the initial cluster."""

        self._make_phenomenal_generating_matrix_rep()

    def to_dict(self):
        """Store the OrbitMatrixRepBuilder in a dictionary."""

        # This is primarily intended for use by ClusterFunctionsBuilder.to_dict(),
        # so we won't include every attribute in the dictionary to avoid duplicates,
        # but we will include some duplicate information for clarity or convenience.
        data = {}

        data["cluster"] = {"sites": self.cluster.to_list()}
        data["phenomenal"] = (
            {"sites": self.phenomenal.to_list()}
            if self.phenomenal is not None
            else None
        )
        data["cluster_group"] = self.cluster_group.head_group_index

        # Add DoF info...
        data.update(
            {
                "global_dof": self.global_dof,
                "local_continuous_dof": self.local_continuous_dof,
                "local_discrete_dof": self.local_discrete_dof,
                "local_dof": self.local_dof,
                "n_global_variables": self.n_global_variables,
                "n_local_variables": self.n_local_variables,
            }
        )

        # Global variables and matrix reps
        data["global_variables"] = [
            [v.to_dict() for v in dof_vars] for dof_vars in self.global_variables
        ]
        data["global_variable_subsets"] = self.global_variable_subsets
        data["global_matrix_rep"] = [
            [m.tolist() for m in dof_rep] for dof_rep in self.global_matrix_rep
        ]
        data["global_inv_matrix_rep"] = [
            [m.tolist() for m in dof_rep] for dof_rep in self.global_inv_matrix_rep
        ]

        # Local variables and matrix reps
        data["local_prototype"] = [
            cluster_matrix_rep_builder.to_dict()
            for cluster_matrix_rep_builder in self.local_prototype
        ]

        # Matrix reps for local DoFs on clusters
        data["local_equivalence_map_matrix_rep"] = [
            [[m.tolist() for m in rep] for rep in dof_rep]
            for dof_rep in self.local_equivalence_map_matrix_rep
        ]
        data["local_equivalence_map_inv_matrix_rep"] = [
            [[m.tolist() for m in rep] for rep in dof_rep]
            for dof_rep in self.local_equivalence_map_inv_matrix_rep
        ]
        data["local_phenomenal_generating_matrix_rep"] = [
            [[m.tolist() for m in rep] for rep in dof_rep]
            for dof_rep in self.local_phenomenal_generating_matrix_rep
        ]
        data["local_phenomenal_generating_inv_matrix_rep"] = [
            [[m.tolist() for m in rep] for rep in dof_rep]
            for dof_rep in self.local_phenomenal_generating_inv_matrix_rep
        ]

        # Coupled matrix reps

        # Generate functions on the prototype cluster
        data["prototype_variables"] = [v.to_dict() for v in self.prototype_variables]
        data["prototype_variable_subsets"] = self.prototype_variable_subsets
        data["prototype_matrix_rep"] = [m.tolist() for m in self.prototype_matrix_rep]

        # Generate functions on equivalent clusters
        data["equivalence_map_indices"] = self.equivalence_map_indices
        data["equivalence_map_matrix_rep"] = [
            [m.tolist() for m in rep] for rep in self.equivalence_map_matrix_rep
        ]
        data["equivalence_map_inv_matrix_rep"] = [
            [m.tolist() for m in rep] for rep in self.equivalence_map_inv_matrix_rep
        ]

        # Generate functions for equivalent phenomenal clusters
        data["phenomenal_generating_indices"] = self.phenomenal_generating_indices
        data["phenomenal_generating_matrix_rep"] = (
            [[m.tolist() for m in rep] for rep in self.phenomenal_generating_matrix_rep]
            if self.phenomenal_generating_matrix_rep is not None
            else None
        )
        data["phenomenal_generating_inv_matrix_rep"] = (
            [
                [m.tolist() for m in rep]
                for rep in self.phenomenal_generating_inv_matrix_rep
            ]
            if self.phenomenal_generating_inv_matrix_rep is not None
            else None
        )

        return data

    def _make_orbit_and_equivalence_map(self):
        # Data used
        phenomenal = self.phenomenal
        cluster = self.cluster
        generating_group = self.generating_group
        prim = self.prim

        ## Generate orbit, equivalence map, and cluster group
        generating_group_site_rep = make_integral_site_coordinate_symgroup_rep(
            group_elements=generating_group.elements,
            xtal_prim=prim.xtal_prim,
        )
        if phenomenal is None:
            orbit = make_periodic_orbit(
                cluster,
                generating_group_site_rep,
            )
            cluster_group = make_cluster_group(
                cluster=orbit[0],
                group=generating_group,
                lattice=prim.xtal_prim.lattice(),
                integral_site_coordinate_symgroup_rep=generating_group_site_rep,
            )
            equivalence_map_indices = make_periodic_equivalence_map_indices(
                orbit=orbit,
                integral_site_coordinate_symgroup_rep=generating_group_site_rep,
            )
            equivalence_map_ops = make_periodic_equivalence_map(
                orbit=orbit,
                symgroup=generating_group,
                lattice=prim.xtal_prim.lattice(),
                integral_site_coordinate_symgroup_rep=generating_group_site_rep,
            )

        else:
            orbit = make_local_orbit(
                cluster,
                generating_group_site_rep,
            )
            cluster_group = make_local_cluster_group(
                cluster=orbit[0],
                phenomenal_group=generating_group,
                integral_site_coordinate_symgroup_rep=generating_group_site_rep,
            )
            equivalence_map_indices = make_local_equivalence_map_indices(
                orbit=orbit,
                integral_site_coordinate_symgroup_rep=generating_group_site_rep,
            )
            equivalence_map_ops = make_local_equivalence_map(
                orbit=orbit,
                phenomenal_group=generating_group,
                integral_site_coordinate_symgroup_rep=generating_group_site_rep,
            )

        if cluster_group.head_group is not prim.factor_group:
            raise Exception(
                "Error in OrbitMatrixRepBuilder: "
                "cluster_group.head_group must be the prim factor group."
            )

        equivalence_map_site_rep = make_equivalence_map_site_rep(
            xtal_prim=prim.xtal_prim,
            equivalence_map_ops=equivalence_map_ops,
        )
        equivalence_map_clusters = make_equivalence_map_clusters(
            orbit=orbit,
            equivalence_map_site_rep=equivalence_map_site_rep,
        )

        ## Generated data ##
        self.orbit = orbit
        self.cluster_group = cluster_group
        self.equivalence_map_ops = equivalence_map_ops
        self.equivalence_map_indices = equivalence_map_indices
        self.equivalence_map_site_rep = equivalence_map_site_rep
        self.equivalence_map_clusters = equivalence_map_clusters

    def _make_phenomenal_generators(self):
        # Data used
        phenomenal = self.phenomenal
        generating_group = self.generating_group
        prim = self.prim

        ## If a local cluster expansion,
        # make equivalent phenomenal generating symmetry operations
        phenomenal_generating_ops = None
        phenomenal_generating_indices = None
        phenomenal_generating_site_rep = None
        if phenomenal is not None:
            (
                phenomenal_generating_ops,
                phenomenal_generating_indices,
                phenomenal_generating_site_rep,
            ) = make_equivalents_generators(
                phenomenal=phenomenal,
                generating_group=generating_group,
                prim=prim,
            )

        # Data generated
        self.phenomenal_generating_ops = phenomenal_generating_ops
        self.phenomenal_generating_indices = phenomenal_generating_indices
        self.phenomenal_generating_site_rep = phenomenal_generating_site_rep

    def _make_global_dof_info(self):
        # Note: global DoF info could be factored out of each individual orbit

        # Data used
        generating_group = self.generating_group
        global_dof = self.global_dof
        prim = self.prim
        make_variable_name_f = self.make_variable_name_f

        ## Make global DoF variables, variable subsets,
        # and matrix reps for individual DoF
        global_variables = []
        global_variable_subsets = []
        global_matrix_rep = []
        global_inv_matrix_rep = []
        prim_factor_group = generating_group.head_group
        if prim_factor_group is None:
            prim_factor_group = generating_group
        for key in global_dof:
            _variables, _variable_subsets = make_global_variables(
                prim=prim,
                key=key,
                make_variable_name_f=make_variable_name_f,
            )
            global_variables.append(_variables)
            global_variable_subsets.append(_variable_subsets)

            prim_factor_group_matrix_rep = prim.global_dof_matrix_rep(key)
            prim_factor_group_inv_matrix_rep = []
            for prim_factor_group_index, op in enumerate(prim_factor_group.elements):
                prim_factor_group_inv_matrix_rep.append(
                    prim_factor_group_matrix_rep[
                        prim_factor_group.inv(prim_factor_group_index)
                    ]
                )
            global_matrix_rep.append(prim_factor_group_matrix_rep)
            global_inv_matrix_rep.append(prim_factor_group_inv_matrix_rep)

        # Data generated
        # global DoF info (lists, by global DoF in same order as global_dof):
        self.global_variables = global_variables
        self.global_variable_subsets = global_variable_subsets
        self.global_matrix_rep = global_matrix_rep
        self.global_inv_matrix_rep = global_inv_matrix_rep

    def _make_local_dof_info(self):
        # Data used
        local_dof = self.local_dof
        prim = self.prim
        generating_group = self.generating_group
        phenomenal = self.phenomenal
        orbit = self.orbit
        make_variable_name_f = self.make_variable_name_f
        occ_site_functions = self.occ_site_functions
        local_discrete_dof = self.local_discrete_dof

        equivalence_map_indices = self.equivalence_map_indices
        equivalence_map_site_rep = self.equivalence_map_site_rep

        phenomenal_generating_indices = self.phenomenal_generating_indices
        phenomenal_generating_site_rep = self.phenomenal_generating_site_rep

        ## Make local DoF variables, variable subsets,
        # and matrix reps for individual DoF, including cluster matrix reps
        local_prototype = []
        local_equivalence_map_matrix_rep = []
        local_equivalence_map_inv_matrix_rep = []
        local_phenomenal_generating_matrix_rep = []
        local_phenomenal_generating_inv_matrix_rep = []
        for key in local_dof:
            ## Build local DoF prototype cluster matrix rep (with permutation)
            _local_prototype = ClusterMatrixRepBuilder(
                prim=prim,
                generating_group=generating_group,
                key=key,
                cluster=orbit[0],
                make_variable_name_f=make_variable_name_f,
                local_discrete_dof=local_discrete_dof,
                occ_site_functions=occ_site_functions,
                phenomenal=phenomenal,
            )
            local_prototype.append(_local_prototype)

            ## Build local DoF equivalence map matrix reps (no permutation)
            # noinspection PyTupleAssignmentBalance
            _1, _2, _3 = make_equivalence_map_matrix_rep(
                local_dof_matrix_rep=_local_prototype.dof_matrix_rep,
                prototype_cluster=_local_prototype.cluster,
                symgroup=generating_group,
                equivalence_map_indices=equivalence_map_indices,
                equivalence_map_site_rep=equivalence_map_site_rep,
                total_dim=_local_prototype.total_dim,
                site_index_to_basis_index=_local_prototype.site_index_to_basis_index,
            )
            local_equivalence_map_matrix_rep.append(_1)
            local_equivalence_map_inv_matrix_rep.append(_2)

            if phenomenal is not None:
                ## Build local DoF phenomenal generating matrix reps (no permutation)
                # noinspection PyTupleAssignmentBalance
                _4, _5, _6 = make_phenomenal_generating_matrix_rep(
                    generating_group=generating_group,
                    local_dof_matrix_rep=_local_prototype.dof_matrix_rep,
                    equivalence_map_clusters=_3,
                    phenomenal_generating_indices=phenomenal_generating_indices,
                    phenomenal_generating_site_rep=phenomenal_generating_site_rep,
                    total_dim=_local_prototype.total_dim,
                    site_index_to_basis_index=_local_prototype.site_index_to_basis_index,
                )
                local_phenomenal_generating_matrix_rep.append(_4)
                local_phenomenal_generating_inv_matrix_rep.append(_5)

        # Data generated
        self.local_prototype = local_prototype
        self.local_equivalence_map_matrix_rep = local_equivalence_map_matrix_rep
        self.local_equivalence_map_inv_matrix_rep = local_equivalence_map_inv_matrix_rep
        self.local_phenomenal_generating_matrix_rep = (
            local_phenomenal_generating_matrix_rep
        )
        self.local_phenomenal_generating_inv_matrix_rep = (
            local_phenomenal_generating_inv_matrix_rep
        )

    def _make_coupled_prototype_matrix_rep_and_variables(self):
        # Data used
        cluster_group = self.cluster_group
        local_prototype = self.local_prototype
        global_matrix_rep = self.global_matrix_rep
        global_variables = self.global_variables
        global_variable_subsets = self.global_variable_subsets

        ## Combine individual DoF matrix reps
        # into a coupled matrix rep for the prototype cluster
        prototype_matrix_rep = []
        for cluster_group_index, prim_factor_group_index in enumerate(
            cluster_group.head_group_index
        ):
            _global_matrices = [x[prim_factor_group_index] for x in global_matrix_rep]
            _local_dof_matrices = [
                x.cluster_matrix_rep[cluster_group_index] for x in local_prototype
            ]
            _all_matrices = _global_matrices + _local_dof_matrices
            prototype_matrix_rep.append(scipy.linalg.block_diag(*_all_matrices))

        # Also, make variables and variable subsets for the coupled cluster functions
        n_global_variables = 0
        n_local_variables = 0
        prototype_variables = []
        prototype_variable_subsets = []
        for i, variables in enumerate(global_variables):
            offset = len(prototype_variables)
            n_global_variables += len(variables)
            prototype_variables += variables
            variable_subsets = global_variable_subsets[i]
            for subset in variable_subsets:
                prototype_variable_subsets.append([j + offset for j in subset])
        for i_local, x in enumerate(local_prototype):
            offset = len(prototype_variables)
            n_local_variables += len(x.variables)
            prototype_variables += x.variables
            for subset in x.variable_subsets:
                corrected_subset = []
                for j in subset:
                    corrected_subset.append(j + offset)
                prototype_variable_subsets.append(corrected_subset)

        # Data generated
        self.prototype_matrix_rep = prototype_matrix_rep
        self.n_global_variables = n_global_variables
        self.n_local_variables = n_local_variables
        self.prototype_variables = prototype_variables
        self.prototype_variable_subsets = prototype_variable_subsets

    def _make_equivalence_map_matrix_rep(self):
        # Data used
        generating_group = self.generating_group
        equivalence_map_ops = self.equivalence_map_ops
        equivalence_map_indices = self.equivalence_map_indices
        local_equivalence_map_matrix_rep = self.local_equivalence_map_matrix_rep
        local_equivalence_map_inv_matrix_rep = self.local_equivalence_map_inv_matrix_rep
        global_matrix_rep = self.global_matrix_rep
        global_inv_matrix_rep = self.global_inv_matrix_rep

        ## Build equivalence map matrix reps
        # Build matrix reps which
        # transform cluster functions generated on the prototype cluster
        # to other clusters in the orbit
        equivalence_map_matrix_rep = []  # transforms DoF
        equivalence_map_inv_matrix_rep = []  # transforms functions
        prim_factor_group_index_list = generating_group.head_group_index
        for i_equiv, ops in enumerate(equivalence_map_ops):
            _matrix_reps = []
            _inv_matrix_reps = []
            for i_op, op in enumerate(equivalence_map_ops[i_equiv]):
                generating_group_index = equivalence_map_indices[i_equiv][i_op]
                prim_factor_group_index = prim_factor_group_index_list[
                    generating_group_index
                ]

                _global_matrices = [
                    x[prim_factor_group_index] for x in global_matrix_rep
                ]
                _local_matrices = [
                    x[i_equiv][i_op] for x in local_equivalence_map_matrix_rep
                ]
                _all_matrices = _global_matrices + _local_matrices
                _matrix_reps.append(scipy.linalg.block_diag(*_all_matrices))

                _global_inv_matrices = [
                    x[prim_factor_group_index] for x in global_inv_matrix_rep
                ]
                _local_inv_matrices = [
                    x[i_equiv][i_op] for x in local_equivalence_map_inv_matrix_rep
                ]
                _all_inv_matrices = _global_inv_matrices + _local_inv_matrices
                _inv_matrix_reps.append(scipy.linalg.block_diag(*_all_inv_matrices))
            equivalence_map_matrix_rep.append(_matrix_reps)
            equivalence_map_inv_matrix_rep.append(_inv_matrix_reps)

        # Data generated
        self.equivalence_map_matrix_rep = equivalence_map_matrix_rep
        self.equivalence_map_inv_matrix_rep = equivalence_map_inv_matrix_rep

    def _make_phenomenal_generating_matrix_rep(self):
        # Data used
        phenomenal = self.phenomenal
        equivalence_map_ops = self.equivalence_map_ops
        phenomenal_generating_ops = self.phenomenal_generating_ops
        phenomenal_generating_indices = self.phenomenal_generating_indices
        global_matrix_rep = self.global_matrix_rep
        global_inv_matrix_rep = self.global_inv_matrix_rep
        local_phenomenal_generating_matrix_rep = (
            self.local_phenomenal_generating_matrix_rep
        )
        local_phenomenal_generating_inv_matrix_rep = (
            self.local_phenomenal_generating_inv_matrix_rep
        )

        ## If a local cluster expansion,
        # Build phenomenal generating matrix reps which
        # transform cluster functions on all local clusters in the orbit
        # to cluster functions on a different but equivalent orbit of local clusters
        # around a symmetrically equivalent phenomenal cluster
        phenomenal_generating_matrix_rep = None
        phenomenal_generating_inv_matrix_rep = None
        if phenomenal is not None:
            phenomenal_generating_matrix_rep: list[list[np.ndarray]] = []
            phenomenal_generating_inv_matrix_rep: list[list[np.ndarray]] = []
            for i_clex, _ in enumerate(phenomenal_generating_ops):
                _matrix_reps = []
                _inv_matrix_reps = []
                prim_factor_group_index = phenomenal_generating_indices[i_clex]
                for i_clust, _ in enumerate(equivalence_map_ops):
                    # get matrix rep
                    _global_matrices = [
                        x[prim_factor_group_index] for x in global_matrix_rep
                    ]
                    _local_matrices = [
                        x[i_clex][i_clust]
                        for x in local_phenomenal_generating_matrix_rep
                    ]
                    _all_matrices = _global_matrices + _local_matrices
                    _matrix_reps.append(scipy.linalg.block_diag(*_all_matrices))

                    # get inv matrix rep
                    _global_inv_matrices = [
                        x[prim_factor_group_index] for x in global_inv_matrix_rep
                    ]
                    _local_inv_matrices = [
                        x[i_clex][i_clust]
                        for x in local_phenomenal_generating_inv_matrix_rep
                    ]
                    _all_inv_matrices = _global_inv_matrices + _local_inv_matrices
                    _inv_matrix_reps.append(scipy.linalg.block_diag(*_all_inv_matrices))
                phenomenal_generating_matrix_rep.append(_matrix_reps)
                phenomenal_generating_inv_matrix_rep.append(_inv_matrix_reps)

        # Data generated
        self.phenomenal_generating_matrix_rep = phenomenal_generating_matrix_rep
        self.phenomenal_generating_inv_matrix_rep = phenomenal_generating_inv_matrix_rep
