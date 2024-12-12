from typing import Optional

from casm.bset.parsing import to_dict


class BasisFunctionSpecs:
    R"""Basis function specifications

    BasisFunctionSpecs is used to specify the type and order of basis functions that
    CASM generates.
    """

    def __init__(
        self,
        dofs: Optional[list[str]] = None,
        dof_specs: dict = {},
        global_max_poly_order: Optional[int] = None,
        orbit_branch_max_poly_order: dict = {},
        param_pack_type: str = "default",
    ):
        """
        .. rubric:: Constructor

        Parameters
        ----------
        dofs: Optional[list[str]] = None
            An array of string of dof type names that should be used to construct basis
            functions. The default value is all DoF types included in the prim.

        dof_specs: dict = {}
            Provides DoF-particular specifications for constructing basis functions,
            as described in the section
            :ref:`DoF Specifications <sec-dof-specifications>`.

        global_max_poly_order: Optional[int] = None
            The maximum polynomial order for cluster functions of continuous DoF.
            If None, the maximum polynomial order is set to the cluster size. May be
            overridden on a per-orbit-branch basis by `orbit_branch_max_poly_order`.

        orbit_branch_max_poly_order: dict = {}
            Specifies the maximum polynomial order on a per-orbit-branch basis, where
            an "orbit branch" is the set of cluster orbits with the same number of
            sites per cluster. Keys indicate the orbit branch, specified using the
            string value of the cluster size as the key, and the value is the maximum
            polynomial order for that orbit branch. For example:

            .. code-block:: Python

                orbit_branch_max_poly_order={
                    "1": 6, # 1-site clusters, max order 6
                    "2": 5, # 2-site clusters, max order 5
                }

        param_pack_type: str = "default"
            Controls the implementation used for evaluating the cluster expansion basis
            functions. Options are “default” or “diff”, which enables fadbad automatic
            differentiating.

        """

        self.dof_specs: dict = dof_specs
        """dict: DoF-particular specifications for constructing basis functions.
        
        See the :class:`casm.bset.BasisFunctionSpecs` constructor for details
        """

        self.dofs: Optional[list[str]] = dofs
        """Optional[list[str]]: An array of string of dof type names that should be
        used to construct basis functions. 
        
        The default value is all DoF types included in the prim.
        """

        self.global_max_poly_order: Optional[int] = global_max_poly_order
        """Optional[int]: Sets default lower bound on maximum polynomial order
        
        For example, if ``global_max_poly_order = 3``, then the maximum polynomial
        order requested for orbit branches not specified in
        :py:data:`~casm.bset.BasisFunctionSpecs.orbit_branch_max_poly_order`
        is ``max(3, cluster_size)``.
        
        See the
        :py:data:`~casm.bset.BasisFunctionSpecs.orbit_branch_max_poly_order`
        documentation for further details.
        """
        self.orbit_branch_max_poly_order: dict = orbit_branch_max_poly_order
        """dict: Sets orbit branch maximum polynomial order
        
        By default, for a given cluster orbit, polynomials of order up to the
        cluster size are created. Higher order polynomials can be requested either
        on a per-orbit-branch or global basis. The most specific level specified
        is used. Orbit branches are specified using the string value of the cluster
        size as a key.
        
        Example:

        .. code-block:: Python
        
            basis_function_specs = BasisFunctionSpecs(
                ...
                # use maximum polynomial order == 7,
                # for orbits of cluster size == 4
                orbit_branch_max_poly_order = {"4": 7},
                
                # use max(3, cluster size), for all other orbits
                global_max_poly_order = 3,
                ...
            )
                
        """

        self.param_pack_type: str = param_pack_type
        """str: Controls the implementation used for evaluating the cluster expansion
        basis functions. 
        
        Options are “default” or “diff”, which enables fadbad automatic differentiating.
        """

    @staticmethod
    def from_dict(data):
        """Construct BasisFunctionSpecs from a Python dictionary

        See the CASM documentation for the `BasisFunctionSpecs format`_.

        .. _`BasisFunctionSpecs format`: https://prisms-center.github.io/CASMcode_docs/formats/casm/basis_set/BasisFunctionSpecs/


        Parameters
        ----------
        data : dict
            A Python dictionary formatted as documented

        Returns
        -------
        basis_function_specs : BasisFunctionSpecs
            The created BasisFunctionSpecs
        """
        return BasisFunctionSpecs(
            dofs=data.get("dofs"),
            dof_specs=data.get("dof_specs", {}),
            global_max_poly_order=data.get("global_max_poly_order"),
            orbit_branch_max_poly_order=data.get("orbit_branch_max_poly_order", {}),
            param_pack_type=data.get("param_pack_type", "default"),
        )

    def to_dict(self):
        """Represent the BasisFunctionSpecs as a Python dictionary

        See the CASM documentation for the `BasisFunctionSpecs format`_.

        .. _`BasisFunctionSpecs format`: https://prisms-center.github.io/CASMcode_docs/formats/casm/basis_set/BasisFunctionSpecs/


        Returns
        -------
        data : dict
            The BasisFunctionSpecs as a Python dictionary

        """
        data = {}
        to_dict(self.dofs, data, "dofs")
        to_dict(self.dof_specs, data, "dof_specs")
        to_dict(self.global_max_poly_order, data, "global_max_poly_order")
        to_dict(self.orbit_branch_max_poly_order, data, "orbit_branch_max_poly_order")

        if self.param_pack_type != "default":
            to_dict(self.param_pack_type, data, "param_pack_type")

        return data
