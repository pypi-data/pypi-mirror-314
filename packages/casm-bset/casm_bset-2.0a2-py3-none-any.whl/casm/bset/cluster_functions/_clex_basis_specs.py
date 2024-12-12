from typing import TypeVar

import libcasm.configuration as casmconfig
from casm.bset.parsing import (
    required_from_dict,
)
from libcasm.clusterography import ClusterSpecs

from ._basis_function_specs import (
    BasisFunctionSpecs,
)

ClexBasisSpecsType = TypeVar("ClexBasisSpecs")


class ClexBasisSpecs:
    """Cluster expansion basis set specifications

    A cluster expansion basis set is specified by two components, one specifying
    basis function type and order, and one specifying cluster orbits.

    The `ClexBasisSpecs format`_ is used for the `bspecs.json` file in a CASM project.

    .. _`ClexBasisSpecs format`: https://prisms-center.github.io/CASMcode_docs/formats/casm/clex/ClexBasisSpecs/

    """

    def __init__(
        self,
        cluster_specs: ClusterSpecs,
        basis_function_specs: BasisFunctionSpecs,
    ):
        """
        .. rubric:: Constructor

        Parameters
        ----------
        cluster_specs: libcasm.clusterography.ClusterSpecs
            Specifies which cluster orbits will be included in the cluster expansion
            basis functions.
        basis_function_specs: casm.bset.cluster_functions.BasisFunctionSpecs
            Specifies how the cluster expansion basis function type and order.
        """
        self.cluster_specs = cluster_specs
        """libcasm.clusterography.ClusterSpecs: Cluster orbit specifications
        
        Specifies which cluster orbits will be included in the cluster expansion 
        basis functions.
        """

        self.basis_function_specs = basis_function_specs
        """casm.bset.cluster_functions.BasisFunctionSpecs: Basis function specifications
        
        Specifies the cluster expansion basis function type and order.
        """

    def is_periodic(self):
        if self.cluster_specs.phenomenal() is None:
            return True
        return False

    @staticmethod
    def from_dict(
        data: dict,
        prim: casmconfig.Prim,
    ) -> ClexBasisSpecsType:
        """Construct ClexBasisSpecs from a Python dictionary

        See the CASM documentation for the `ClexBasisSpecs format`_.

        .. _`ClexBasisSpecs format`: https://prisms-center.github.io/CASMcode_docs/formats/casm/clex/ClexBasisSpecs/


        Parameters
        ----------
        data : dict
            A Python dictionary formatted as documented
        prim: libcasm.configuration.Prim
            The prim, with symmetry information.

        Returns
        -------
        clex_basis_specs : ClexBasisSpecs
            The created ClexBasisSpecs
        """
        if "cluster_specs" not in data:
            raise Exception("Error in ClexBasisSpecs.from_dict: no cluster_specs")
        if "params" in data["cluster_specs"]:
            # v1 format:
            cluster_specs_data = data["cluster_specs"]
            cluster_specs_key = "params"
        else:
            # v2 format:
            cluster_specs_data = data
            cluster_specs_key = "cluster_specs"

        return ClexBasisSpecs(
            cluster_specs=required_from_dict(
                ClusterSpecs,
                cluster_specs_data,
                cluster_specs_key,
                xtal_prim=prim.xtal_prim,
                prim_factor_group=prim.factor_group,
                integral_site_coordinate_symgroup_rep=prim.integral_site_coordinate_symgroup_rep,
            ),
            basis_function_specs=required_from_dict(
                BasisFunctionSpecs, data, "basis_function_specs"
            ),
        )

    def to_dict(self) -> dict:
        """Represent the ClexBasisSpecs as a Python dictionary

        See the CASM documentation for the `ClexBasisSpecs format`_.

        .. _`ClexBasisSpecs format`: https://prisms-center.github.io/CASMcode_docs/formats/casm/clex/ClexBasisSpecs/


        Returns
        -------
        data : dict
            The ClexBasisSpecs as a Python dictionary

        """
        return {
            "cluster_specs": self.cluster_specs.to_dict(),
            "basis_function_specs": self.basis_function_specs.to_dict(),
        }
