import copy
import math
import sys
from collections import namedtuple
from typing import Optional, TypeVar, Union

import numpy as np
import opt_einsum
import sparse

from casm.bset.misc import (
    factor_by_mode,
    irrational_to_tex_string,
)
from libcasm.counter import IntCounter


def is_canonical_coord(x: np.ndarray):
    """Check if a 1d array of tensor coordinates is sorted in decreasing order"""
    n = len(x) - 1
    for i in range(n):
        if x[i] < x[i + 1]:
            return False
    return True


def make_canonical_coord(x):
    """Return a copy of a 1d array of tensor coordinates, sorted in decreasing order"""
    return np.sort(x)[::-1]


def is_lowest_equivalent_coord(x: np.ndarray):
    """Check if a 1d array of tensor coordinates is sorted in ascending order"""
    n = len(x) - 1
    for i in range(n):
        if x[i] > x[i + 1]:
            return False
    return True


def make_lowest_equivalent_coord(x):
    """Return a copy of a 1d array of tensor coordinates, sorted in ascending order"""
    return np.sort(x)


def tensor_coord_to_monomial_exponents(x, n_size):
    """Convert tensor coordinates to vector of exponents form

    Example 1:

    .. code-block::

        # strain monomial {e_1}^4
        n_size=6
        x=np.array([0, 0, 0, 0], dtype='int')

        # equivalent vector of exponents
        n=np.array([4, 0, 0, 0, 0, 0], dtype='int')

    Example 2:

    .. code-block::

        # strain monomial {e_1}^2 {e_2}^1 {e_3}
        n_size=6
        x=np.array([2, 1, 0, 0], dtype='int')

        # equivalent vector of exponents
        n=np.array([2, 1, 1, 0, 0, 0], dtype='int')


    Parameters
    ----------
    x: np.ndarray[np.int]
        Tensor indices
    n_size: int
        Number of variable components, i.e. 6 for strain.

    Returns
    -------
    n: np.ndarray[np.int]
        Vector of monomial exponents
    """
    n = np.zeros((n_size,), dtype="int")
    for i in x:
        n[i] += 1
    return n


def monomial_exponents_to_tensor_coord(n):
    """Convert vectors of monomial exponents to tensor coordinates

    Parameters
    ----------
    n: np.ndarray[np.int]
        Vector of monomial exponents

    Returns
    -------
    x: np.ndarray[np.int]
        Tensor indices
    n_size: int
        Number of variable components, i.e. 6 for strain.
    """
    x = np.zeros((n.sum(),), dtype="int")
    j = 0
    i = n.size - 1
    while i > 0:
        while n[i] > 0:
            x[j] = i
            j += 1
            n[i] -= 1
        i -= 1
    return (x, n.size)


class FunctionRep:
    """Symmetry operation representation used to transform PolynomialFunction

    Currently, symmetry is applied to tensor coefficients using einstein summation
    notation. An improvement is planned to be made using the method described in
    Appendix C of J.C. Thomas, A. Van der Ven / Journal of the Mechanics and Physics of
    Solids 107 (2017) 76–95. DOI: 10.1016/j.jmps.2017.06.009

    """

    def __init__(
        self,
        matrix_rep: np.ndarray,
    ):
        """

        .. rubric:: Constructor

        Parameters
        ----------
        matrix_rep: np.ndarray[np.float64[m,m]]
            Describes the effect of applying a symmetry operation on a vector of
            variables.
        """

        self.matrix_rep = matrix_rep
        """np.ndarray[np.float64[m,m]]: Describes the effect of applying a symmetry 
        operation on a vector of variables.
        """

        self.sparse_matrix_rep = sparse.COO.from_numpy(matrix_rep)
        """sparse.COO: The `matrix_rep` as a sparse.COO array."""

    def __mul__(self, rhs):
        if isinstance(rhs, PolynomialFunction):
            dim = len(rhs.coeff.shape)
            result = rhs.copy()

            # A: result.coeff,
            # M: self.matrix_rep / self.sparse_matrix_rep
            #
            # Ex: indices_before, [i, j], indices_after
            #
            # dim = 1: A_a M_al -> A_l
            # i=0, j=1: [0], [0, 1], [1] # A_a M_al -> A_l
            #
            # dim = 2: A_ab M_al M_bm -> A_lm
            # i=0, j=2: [0, 1], [0, 2] -> [2, 1] # A_ab M_al -> A_lb
            # i=1, j=3: [2, 1], [1, 3] -> [2, 3] # A_lb M_bm -> A_lm
            #
            # dim = 3: A_abc M_al M_bm M_cn -> A_lmn
            # i=0, j=3: [0, 1, 2], [0, 3] -> [3, 1, 2] # A_abc M_al -> A_lbc
            # i=1, j=4: [3, 1, 2], [1, 4] -> [3, 4, 2] # A_lbc M_bm -> A_lmc
            # i=2, j=5: [3, 4, 2], [2, 5] -> [3, 4, 5] # A_lmc M_cn -> A_lmn
            #
            # etc.

            indices_before = [i for i in range(dim)]
            indices_after = [i for i in range(dim)]
            j = dim
            for i in range(dim):
                indices_after[i] = j
                result.coeff = opt_einsum.contract(
                    result.coeff,
                    indices_before,
                    self.sparse_matrix_rep,
                    [i, j],
                    indices_after,
                )
                indices_before = copy.deepcopy(indices_after)
                j += 1
            result.monomial_exponents = result.tensor_coords_to_monomial_exponents()

            result.make_canonical()
            result.prune()
            return result
        else:
            raise Exception(
                "Error in FunctionRep * X, with X="
                + str(type(rhs))
                + ": not implemented"
            )


VariableData = namedtuple(
    "VariableData",
    [
        "key",
        "cluster_site_index",
        "component_index",
        "site_basis_function_index",
        "neighborhood_site_index",
    ],
)


class Variable:
    r"""Represents a variable in a PolynomialFunction

    This class is used to keep the information necessary for collecting the degree
    of freedom (DoF) values necessary for evaluating polynomial functions.

    """

    def __init__(
        self,
        name: str,
        key: str,
        cluster_site_index: Optional[int] = None,
        component_index: Optional[int] = None,
        site_basis_function_index: Optional[int] = None,
        neighborhood_site_index: Optional[int] = None,
    ) -> object:
        R"""

        .. rubric:: Constructor

        Parameters
        ----------
        name: str
            Name used for identification and printing. For example:

            - "{e_1}", "{e_2}", etc. or "{E_{xx}}", "{E_{yy}}", etc. for strain
              degrees of freedom;
            - "{d_1}", "{d_2}", etc. or "dx", "dy", "dz" for displacement degrees of
              freedom;
            - "{\\\\\\phi_1}", "{\\\\\\phi_2}", etc. for occupation site basis
              functions, or "{\\\\\\phi_{a,1}}", "{\\\\\\phi_{a,2}}", etc. and
              "{\\\\\\phi_{b,1}}", "{\\\\\\phi_{b,2}}", etc. for occupation site basis
              functions on symmetrically distinct sites :math:`a` and :math:`b`.

        key: str
            Name of the degree of freedom (DoF) this variable represents.

        cluster_site_index: Optional[int] = None
            For site variables, the cluster site index of the site associated with the
            variable.

        component_index: Optional[int] = None
            For vector-valued continuous variables, the component of the vector this
            variable corresponds to.

        site_basis_function_index: Optional[int] = None
            For discrete occupation variables, the site basis function index
            this variable corresponds to.

        neighborhood_site_index: Optional[int] = None
            For site variables, the neighbor list index of the site associated with the
            variable.

            Used for printing expressions for evaluation of functions in terms of
            values on sites determined by the neighbor list position.

        """

        self.name = name
        R"""str: Name used for identification and printing.
        
        For example:
         
        - "{e_1}", "{e_2}", etc. or "{E_{xx}}", "{E_{yy}}", etc. for strain
          degrees of freedom; 
        - "{d_1}", "{d_2}", etc. or "dx", "dy", "dz" for displacement degrees of 
          freedom;
        - "{\phi_1}", "{\phi_2}", etc. for occupation site basis functions, or
          "{\phi_{a,1}}", "{\phi_{a,2}}", etc. and "{\phi_{b,1}}", "{\phi_{b,2}}", etc.
          for occupation site basis functions on symmetrically distinct sites :math:`a`
          and :math:`b`.
        """

        self.key = key
        """str: Name of the degree of freedom (DoF) this variable represents."""

        self.cluster_site_index = cluster_site_index
        """Optional[int]: For site variables, the cluster site index of the site 
        associated with the variable. 
        
        This is used for:

        - checking if a polynomial function includes all sites in a cluster
        - in combination with a cluster to determine the neighbor list index
        - printing latex formulas for functions on a cluster
        """

        self.component_index = component_index
        """Optional[int]: For vector-valued continuous variables, the component of \
        the vector this variable corresponds to.
        """

        self.site_basis_function_index = site_basis_function_index
        """Optional[int]: For occupation variables, the site basis function index \
        this variable corresponds to.
        """

        self.neighborhood_site_index = neighborhood_site_index
        """Optional[int]: For site variables, the neighbor list index of the site \
        associated with the variable.
        
        Used for printing expressions for evaluation of functions in terms of values on 
        sites determined by the neighbor list position.
        """

    def to_dict(self):
        data = {
            "name": self.name,
            "key": self.key,
        }
        if self.cluster_site_index is not None:
            data["cluster_site_index"] = self.cluster_site_index
        if self.component_index is not None:
            data["component_index"] = self.component_index
        if self.site_basis_function_index is not None:
            data["site_basis_function_index"] = self.site_basis_function_index
        if self.neighborhood_site_index is not None:
            data["neighborhood_site_index"] = self.neighborhood_site_index
        return data

    @staticmethod
    def from_dict(data):
        return Variable(
            name=data["name"],
            key=data["key"],
            cluster_site_index=data.get("cluster_site_index"),
            component_index=data.get("component_index"),
            site_basis_function_index=data.get("site_basis_function_index"),
            neighborhood_site_index=data.get("neighborhood_site_index"),
        )

    def _to_tuple(self):
        if self.neighborhood_site_index is None:
            return VariableData(
                self.key,
                self.cluster_site_index,
                self.component_index,
                self.site_basis_function_index,
                self.neighborhood_site_index,
            )
        else:
            # when neighborhood_site_index is set, we don't want to
            # compare cluster_site_index
            return VariableData(
                self.key,
                None,
                self.component_index,
                self.site_basis_function_index,
                self.neighborhood_site_index,
            )

    def __hash__(self):
        return hash(self._to_tuple())

    def __eq__(self, other):
        if isinstance(other, Variable):
            return self._to_tuple() == other._to_tuple()
        return NotImplemented


def is_subcluster_function(x: np.ndarray, variables: list[Variable], n_sites: int):
    site_included = [False] * n_sites
    for i in range(len(x)):
        csi = variables[x[i]].cluster_site_index
        if csi is not None:
            site_included[csi] = True
    return not all(site_included)


PolynomialFunctionType = TypeVar("PolynomialFunction")


class PolynomialFunction:
    r"""Represents a polynomial function as a sum monomial terms of the same order

    For example, if there are two variables, :math:`\vec{x} = [x_1, x_2]`,
    then PolynomialFunction can represent one of:

    .. math::

        f(\vec{x}) &= f_1 x{_1} + f_2 x{_2},

        f(\vec{x}) &= f_1 x{_1}^2 + f_2 x{_1} x{_2} + f_3 x{_2}^2,

        f(\vec{x}) &= f_1 x{_1}^3 + f_2 x{_1}^2 x{_2} + f_3 x{_1} x{_2}^2 + f_4 x{_2}^3,

        f(\vec{x}) &= f_1 x{_1}^4 + f_2 x{_1}^3 x{_2} + f_3 x{_1}^2 x{_2}^2 + \
        f_4 x{_1} x{_2}^3 + f_5 x{_2}^4,

        \mathrm{etc.}

    PolynomialFunction does not currently represent sums of monomials with
    different order (i.e. :math:`f_1 x{_1} + f_2 x{_1}^2`).

    """

    def __init__(
        self,
        coeff: sparse.COO,
        variables: list[Variable],
        variable_subsets: list[list[int]],
        tol: float = 1e-10,
    ):
        """

        .. rubric:: Constructor

        Parameters
        ----------
        coeff: sparse.COO
            A sparse tensor specifying non-zero monomial terms and corresponding
            coefficients.
        variables: list[Variable]
            The variables in the monomial terms.
        variable_subsets: list[list[int]]
            Lists of variables (as indices into the `variables` list) which mix under
            application of symmetry. For example, if all variables are the 6 strain
            variables, then `var_subsets=[[0,1,2,3,4,5]]`. If the variables are the 3
            displacements on each site in a cluster of 2 sites, then
            `variable_subsets=[[0, 1, 2], [3, 4, 5]]`.
        tol: float
            A tolerance used for pruning coefficients which are approximately zero.
        """

        self.coeff = coeff
        """sparse.COO: A sparse tensor holding coefficients of a polynomial.

        Example, polynomial with maximum order=2:

            A_ij = coeff,

        and the polynomial function is:

            f(x) = A_ij x_i x_j

        Example, a polynomial with maximum order=3:

            A_ijk = coeff,

        and the polynomial function is:

            f(x) = A_ijk x_i x_j x_k

        Operations (`*`, `+=`, `-=`, etc.) can be expected to also make
        `coeff` canonical and prune the coefficients that are
        approximately zero."""

        self.variables = variables
        """list[casm.bset.polynomial_functions.Variable]: The variables `x` of the 
        polynomial."""

        self.monomial_exponents = self.tensor_coords_to_monomial_exponents()
        """list[numpy.ndarray[numpy.int]]: The corresponding vectors of exponents for 
        the monomials (i.e. the non-zero tensor coefficients).

        For example:

        .. code-block:: Python

            n_size = len(variables)
            monomial_exponents[i] = tensor_coord_to_monomial_exponents(
                coeff.coords[:,i], n_size)

        The `monomial_exponents` is determined from `coeff` and must be updated
        whenever coeff.coords is modified."""

        self.variable_subsets = variable_subsets
        """list[list[int]]: Lists of variables (as indices into the `variables` list) 
        which mix under application of symmetry. 
        
        For example, if all variables are the 6 strain variables, then 
        `var_subsets=[[0,1,2,3,4,5]]`. If the variables are the 3 displacements on 
        each site in a cluster of 2 sites, then 
        `variable_subsets=[[0, 1, 2], [3, 4, 5]]`. This information is used in the 
        calculation of :func:`monomial_inner_product()`."""

        self.tol = tol
        """float: A tolerance used for pruning coefficients which are approximately 
        zero."""

    @staticmethod
    def zeros(
        shape: tuple[int],
        variables: list[Variable],
        variable_subsets: list[list[int]],
        tol: float = 1e-10,
    ):
        """Construct a new PolynomialFunction with all zero coefficients

        Parameters
        ----------
        shape: tuple[int]
            The shape of the coefficients tensor
        variables: list[Variable]
            The variables in the monomial terms.
        tol: float
            A tolerance used for pruning coefficients which are approximately zero.

        Returns
        -------
        function: PolynomialFunction
            A PolynomialFunction with all zero coefficients
        """
        coords = np.array([])
        data = np.array([])

        # Note: Constructing a zero-value sparse.COO gives a DeprecationWarning
        # in sparse 0.14.0, but it is erroneous and should not in the next release
        # (see https://github.com/pydata/sparse/pull/581)
        import warnings

        warnings.filterwarnings(
            "ignore",
            message="coords should be an ndarray. "
            "This will raise a ValueError in the future.",
        )

        return PolynomialFunction(
            coeff=sparse.COO(coords, data, shape=shape, prune=True),
            variables=variables,
            variable_subsets=variable_subsets,
            tol=tol,
        )

    def order(self):
        """Return the polynomial order"""
        return len(self.coeff.shape)

    def prune(self):
        """Update to remove sparse tensor components that are approximately zero."""
        mask = np.abs(self.coeff.data) > self.tol
        self.coeff = sparse.COO(
            self.coeff.coords[:, mask],
            self.coeff.data[mask],
            shape=self.coeff.shape,
            prune=True,
        )
        self.monomial_exponents = self.tensor_coords_to_monomial_exponents()
        return self

    def copy(self):
        return copy.deepcopy(self)

    def monomials(self):
        """Return individual monomials

        Returns
        -------
        monomials: list[PolynomialFunction]
            List of monomials which together sum to this polynomial
        """
        monomials = []
        for i in range(self.coeff.coords.shape[1]):
            mask = [i]

            monomials.append(
                PolynomialFunction(
                    coeff=sparse.COO(
                        self.coeff.coords[:, mask],
                        self.coeff.data[mask],
                        shape=self.coeff.shape,
                        prune=True,
                    ),
                    variables=self.variables,
                    variable_subsets=self.variable_subsets,
                    tol=self.tol,
                )
            )
        return monomials

    def __isub__(self, rhs: PolynomialFunctionType):
        self.coeff -= rhs.coeff
        self.make_canonical()
        self.prune()
        self.monomial_exponents = self.tensor_coords_to_monomial_exponents()
        return self

    def __iadd__(self, rhs: PolynomialFunctionType):
        self.coeff += rhs.coeff
        self.make_canonical()
        self.prune()
        self.monomial_exponents = self.tensor_coords_to_monomial_exponents()
        return self

    def __imul__(self, c: Union[float | Variable]):
        if isinstance(c, float):
            self.coeff *= c
            return self
        elif isinstance(c, Variable):
            i_var = self.variables.index(c)

            n_var = len(self.variables)
            order = self.coeff.coords.shape[0]
            n_monomial = self.coeff.coords.shape[1]
            coords_new = np.array(
                self.coeff.coords.copy().tolist() + [i_var] * n_monomial,
                dtype="int",
            )
            shape_new = [n_var] * (order + 1)

            self.coeff = sparse.COO(
                coords_new, self.coeff.data, shape=shape_new, prune=True
            )
            self.make_canonical()
            self.prune()
            self.monomial_exponents = self.tensor_coords_to_monomial_exponents()
            return self
        else:
            raise NotImplementedError

    def __mul__(self, c: Union[float | Variable]):
        result = self.copy()
        result *= c
        return result

    def __rmul__(self, c: Union[float | Variable]):
        return self * c

    def can_factor_by(self, var: Variable):
        """Check if a variable can be factored out of this polynomial

        Parameters
        ----------
        var: casm.bset.Variable
            Variable to be factored out.

        Returns
        -------
        result: bool
            True if this polynomial can be factored by `var`; False otherwise.
        """
        if var not in self.variables:
            return False
        i_var = self.variables.index(var)
        coords_list = self.coeff.coords.copy().transpose().tolist()
        for monomial_coords in coords_list:
            if i_var not in monomial_coords:
                return False
        return True

    def __itruediv__(self, c: Union[float | Variable]):
        if isinstance(c, float):
            self.coeff /= c
            return self
        elif isinstance(c, Variable):
            i_var = self.variables.index(c)

            n_var = len(self.variables)
            order = self.coeff.coords.shape[0]

            coords_list = self.coeff.coords.copy().transpose().tolist()
            for monomial_coords in coords_list:
                monomial_coords.remove(i_var)
            coords_new = np.array(coords_list, dtype="int").transpose()
            shape_new = [n_var] * (order - 1)

            self.coeff = sparse.COO(
                coords_new, self.coeff.data, shape=shape_new, prune=True
            )
            self.make_canonical()
            self.prune()
            self.monomial_exponents = self.tensor_coords_to_monomial_exponents()
            return self
        else:
            raise NotImplementedError

    def __truediv__(self, c: Union[float | Variable]):
        result = self.copy()
        result /= c
        return result

    def make_canonical(self):
        """Shift sparse tensor values from non-canonical coordinates to canonical \
        coordinates and prune zeros

        For example, coordinates `[0, 1]` and `[0, 2]` are non-canonical (increasing),
        so convert them from:

        .. code-block:: Python

            self.coeff.coords = [
                [0, 1, 2, 0],
                [1, 0, 0, 2],
            ]
            self.coeff.data = [1., 2., 3., 4.]

        To:

        .. code-block:: Python

            self.coeff.coords = [
                [1, 2],
                [0, 0],
            ]
            self.coeff.data = [3., 7.]

        Note that `self.coeff.data` must be updated appropriately.

        """
        if len(self.coeff.data) == 0:
            return self

        # copy canonical coords/data
        coords = self.coeff.coords.transpose().tolist()
        data = self.coeff.data.tolist()
        _coords = []
        _data = []
        for i in range(len(coords)):
            x = coords[i]
            v = data[i]
            if is_lowest_equivalent_coord(x):
                _coords.append(x)
                _data.append(v)
                continue
            x_canonical = make_lowest_equivalent_coord(x).tolist()

            found = False
            for j in range(len(_coords)):
                if _coords[j] == x_canonical:
                    found = True
                    _data[j] += v
                    break
            if not found:
                _coords.append(x_canonical)
                _data.append(v)

        # sort
        coords, data = zip(*sorted(zip(_coords, _data)))

        coords = np.array(coords).transpose()
        data = np.array(data)
        mask = np.abs(data) > self.tol
        self.coeff = sparse.COO(
            coords[:, mask],
            data[mask],
            shape=self.coeff.shape,
            prune=True,
        )
        self.monomial_exponents = self.tensor_coords_to_monomial_exponents()
        return self

    def tensor_coords_to_monomial_exponents(self):
        """Return sparse tensor coords as a list of vectors of monomial exponents

        Returns
        -------
        monomial_exponents: list[np.ndarray[np.int]]
            A list of vectors of monomial exponents, with one vector per monomial term
            with non-zero coefficient (i.e. one per coordinate in the `self.coeff`
            sparse tensor).
        """
        n_size = len(self.variables)
        coords = self.coeff.coords
        n_coords = coords.shape[1]
        return [
            tensor_coord_to_monomial_exponents(coords[:, i], n_size)
            for i in range(n_coords)
        ]

    def scalar_product(self, rhs: PolynomialFunctionType):
        r"""Scalar product

        Evaluates the Frobenius scalar product, :math:`\langle f, g \rangle_F`, of two
        polynomials, i.e. the sum of the :func:`monomial_inner_product` between each
        monomial term in the two polynomials. For example:

        .. math::

            f = f_1 {x_1}^2 + f_2 {x_1} {x_2} + f_3 {x_2}^2

            g = g_1 {x_1} * y + g_2 {x_2}^2

            \langle f, g \rangle_F = \\
                \langle f_1 {x_1}^2, g_1 {x_1} * {x_2} \rangle \\
                + \langle f_1 {x_1}^2, g_2 {x_2}^2 \rangle \\
                + \langle f_2 {x_1} y, g_1 {x_1} * {x_2} \rangle \\
                + \langle f_2 {x_1} y, g_2 {x_2}^2 \rangle \\
                + \langle f_3 {x_2}^2, g_1 {x_1} * {x_2} \rangle \\
                + \langle f_3 {x_2}^2, g_2 {x_2}^2 \rangle

        The :func:`monomial_inner_product` is defined to be 0 for monomials differing
        only by their exponents, so this simplifies to:

        .. math::

            \langle f, g \rangle_F = \\
                \langle f_2 {x_1} y, g_1 {x_1} * {x_2} \rangle \\
                + \langle f_3 {x_2}^2, g_2 {x_2}^2 \rangle


        Parameters
        ----------
        rhs: PolynomialFunction
            The second polynomial.

        Returns
        -------
        product: float
            Frobeinius scalar product of this PolynomialFunction and `rhs`, as defined
            above.
        """
        a_exp = self.monomial_exponents
        a_coeff = self.coeff.data
        a_size = len(a_exp)

        b_exp = rhs.monomial_exponents
        b_coeff = rhs.coeff.data
        b_size = len(b_exp)

        prod = 0.0
        for i_a in range(a_size):
            for i_b in range(b_size):
                prod += monomial_inner_product(
                    a_coeff[i_a],
                    a_exp[i_a],
                    b_coeff[i_b],
                    b_exp[i_b],
                    self.variable_subsets,
                )
        return prod

    def normalize(self):
        self.coeff /= np.sqrt(self.scalar_product(self))
        return self

    def __lt__(self, rhs):
        a = self.coeff.coords
        b = rhs.coeff.coords
        if a.shape[1] != b.shape[1]:
            return a.shape[1] < b.shape[1]
        elif not np.all(a == b):
            return a.T.tolist() < b.T.tolist()
        a = self.coeff.data
        b = self.coeff.data

        if np.allclose(a, b):
            return False
        return a.tolist() < b.tolist()

    def __gt__(self, rhs):
        return rhs < self

    def __le__(self, rhs):
        return not rhs < self

    def __ge__(self, rhs):
        return not self < rhs

    def __eq__(self, rhs):
        return not self < rhs and not rhs < self

    def __ne__(self, rhs):
        return self < rhs or rhs < self

    def _basic_print(self):
        """Basic printing for development"""
        limit = len(self.variables) ** 2
        max_pow = 2

        a_tex = 0
        coeff_tex = []

        if len(self.coeff.data) != 0:
            a, factored_data = factor_by_mode(self.coeff.data)

            a_tex = irrational_to_tex_string(
                a, limit=limit, max_pow=max_pow, abs_tol=1e-5
            )
            coeff_tex = [
                irrational_to_tex_string(x, limit=limit, max_pow=max_pow, abs_tol=1e-5)
                for x in factored_data
            ]

        print("coordinates:")
        print(self.coeff.coords)
        print("coefficients:")
        print(f"{a_tex} * [", end="")
        for s in coeff_tex:
            print(f"{s}, ", end="")
        print("]")

    def to_dict(self):
        """Represent as a Python dict"""
        limit = len(self.variables) ** 2
        max_pow = 2

        a_tex = 0
        coeff_tex = []

        if len(self.coeff.data) != 0:
            a, factored_data = factor_by_mode(self.coeff.data)

            a_tex = irrational_to_tex_string(
                a, limit=limit, max_pow=max_pow, abs_tol=1e-5
            )
            coeff_tex = [
                irrational_to_tex_string(x, limit=limit, max_pow=max_pow, abs_tol=1e-5)
                for x in factored_data
            ]

        tex_prefactor_str = str(a_tex)
        tex_coeff_str = [str(x) for x in coeff_tex]

        return {
            "coeff_coords": self.coeff.coords.T.tolist(),
            "coeff_data": self.coeff.data.tolist(),
            "coeff_shape": list(self.coeff.shape),
            "variables": [var.to_dict() for var in self.variables],
            "variable_subsets": self.variable_subsets,
            "monomial_exponents": [x.tolist() for x in self.monomial_exponents],
            "tex_prefactor": tex_prefactor_str,
            "tex_coeff": tex_coeff_str,
            "tol": self.tol,
        }

    @staticmethod
    def from_dict(data):
        """Construct from a Python dict"""
        variables = [Variable.from_dict(x) for x in data["variables"]]
        variable_subsets = data["variable_subsets"]
        coords = np.array(data["coeff_coords"], dtype=int).T
        _data = np.array(data["coeff_data"])
        shape = tuple(data["coeff_shape"])
        tol = data.get("tol", 1e-10)
        return PolynomialFunction(
            coeff=sparse.COO(coords, _data, shape=shape, prune=True),
            variables=variables,
            variable_subsets=variable_subsets,
            tol=tol,
        )

    def latex_formula(
        self,
    ):
        """Latex printing for development
        It might be good to take variables as strings."""
        variables = self.variables
        exponents = self.monomial_exponents
        a, factored_data = factor_by_mode(self.coeff.data)

        limit = len(variables) ** 2
        max_pow = 2

        # build terms
        latex_formula = ""
        for i, val in enumerate(
            factored_data
        ):  # len(factored_data) is the number of terms
            coeff = a * factored_data[i]
            if np.isclose(coeff, 1):
                coeff_tex = ""
            else:
                coeff_tex = irrational_to_tex_string(
                    a * factored_data[i], limit=limit, max_pow=max_pow, abs_tol=1e-5
                )
            polynomial_tex = ""
            for j, exp in enumerate(exponents[i]):
                if exp == 0:
                    continue  # constant contribution
                if exp == 1:
                    polynomial_tex += f" * ({variables[j].name})"
                else:
                    polynomial_tex += f" * ({variables[j].name})^{exp}"
            polynomial_tex = polynomial_tex.strip("* ")
            latex_formula += f"{coeff_tex} * [{polynomial_tex}] + "

        return latex_formula.strip("*+ ")

    def _latex_print(self):
        """Latex printing for development
        It might be good to take variables as strings."""
        print(self.latex_formula())


def monomial_inner_product(
    a_coeff: float,
    n_a: list[int],
    b_coeff: float,
    n_b: list[int],
    variable_subsets: list[list[int]],
) -> float:
    r"""Evaluates the monomial inner product

    Evaluates the monomial inner product as defined by Eq. (C.4) of :cite:`THOMAS2017a`:

    .. math::

        \left \langle \alpha^{(\vec{n})}\prod_{m} x_m^{n_m},
        \beta^{(\vec{n}')}\prod_{m'} x_{m'}^{n'_{m'}} \right \rangle
        = \alpha^{(\vec{n})}\beta^{(\vec{n}')}
        \frac{1}{\prod_l(\sum_{m \in S_l} n_{m})!}
        \prod_m\delta_{n_{m}n'_{m}}n_{m}!

    where:

    - :math:`\vec{x}`: the vector of variable components,
      i.e. for strain, :math:`\vec{x}=[e_1, e_2, e_3, e_4, e_5, e_6 ]`.
    - :math:`\alpha^{(\vec{n})}`: the coefficient for the first monomial
    - :math:`\vec{n}`: the vector of exponents for the first monomial
    - :math:`\beta^{(\vec{n}')}`: the coefficient for the second monomial
    - :math:`\vec{n}'`: the vector of exponents for the second monomial
    - :math:`S_l`: the subsets of indices of variables which mix under application of
      symmetry. For example, in a cluster of 2 sites with 3 site displacement degrees
      of freedom on each site (:math:`dx`, :math:`dy`, :math:`dz`), there are 6 total
      variables, the first three (with indices [0,1,2]) being the displacements on the
      first site and the second three (with indices [3, 4, 5]) being the displacements
      on the second site. Then the variable subsets would be :math:`S_1=[0, 1, 2]` and
      :math:`S_2=[3, 4, 5]`.

    Parameters
    ----------
    a_coeff: float
        The coefficient for the first monomial, :math:`\alpha^{(\vec{n})}`.
    n_a: np.ndarray[np.int]
        The vector of exponents for the first monomial, :math:`\vec{n}`
    b_coeff: float
        The coefficient for the first monomial, :math:`\beta^{(\vec{n})}`.
    n_b: np.ndarray[np.int]
        The vector of exponents for the second monomial, :math:`\vec{n}'`
    variable_subsets: list[list[int]]
        The subsets of variables which mix under application of symmetry, as indices
        into the vectors of exponents.

    Returns
    -------
    product: float
        The monomial inner product, as defined above.
    """
    if n_a.size != n_b.size:
        raise Exception("Error in monomial_inner_product: size mismatch")

    # Evaluate: factorial_prod = \prod_m\delta_{n_{m}n'_{m}}n_{m}!
    factorial_prod = 1
    for m in range(n_a.size):
        # if any delta_{n_{m}n'_{m}} == 0, can return 0.0
        if n_a[m] != n_b[m]:
            return 0.0
        factorial_prod *= math.factorial(n_a[m])

    factorial_quotient = 1.0
    for subset in variable_subsets:
        sum = 0
        for m in subset:
            sum += n_a[m]
        factorial_quotient *= math.factorial(sum)

    # return a_coeff * b_coeff * (1.0 / math.factorial(np.sum(n_a))) * factorial_prod
    return a_coeff * b_coeff * factorial_prod / factorial_quotient


def gram_schmidt(
    functions: list[PolynomialFunction],
) -> list[PolynomialFunction]:
    """Apply the Gram-Schmidt procedure to orthonormalize a list of PolynomialFunction

    Parameters
    ----------
    functions: list[PolynomialFunction]
        A list of :class:`~casm.bset.coo.PolynomialFunction`.

    Returns
    -------
    orthonormalized_functions: list[PolynomialFunction]
        Functions after applying Gram-Schmidt
    """
    orthonormalized_functions = []
    for f in functions:
        if len(f.coeff.data) == 0:
            continue
        next = f.copy()
        next.make_canonical()
        next.prune()
        for g in orthonormalized_functions:
            next -= next.scalar_product(g) * g
        if len(next.coeff.data) != 0:
            next.normalize()
            orthonormalized_functions.append(next)
    orthonormalized_functions.sort()
    return orthonormalized_functions


class ExponentSumConstraint:
    """Data structure that specifies an exponent sum for filtering monomials"""

    def __init__(
        self,
        variables: list[int],
        sum: list[int],
    ):
        """

        .. rubric:: Constructor

        Parameters
        ----------
        variables: list[int]
            Indices of the variables included in the constraint
        sum: list[int]
            The sum of the exponents of the specified variables
            must be in the `sum` list for the constraint to
            be satisfied.
        """
        self.variables = variables
        """list[int]: Indices of the variables in the
        :py:data:`PolynomialFunction.variables <casm.bset.polynomial_functions.PolynomialFunction.variables>`
        list that are included in the constraint."""  # noqa

        self.sum = sum
        """list[int]: The sum of the exponents of the specified variables must be in \
        the `sum` list for the constraint to be satisfied."""

    def satisfied(self, monomial_exponents):
        curr_sum = 0
        for i_var in self.variables:
            curr_sum += monomial_exponents[i_var]
        return curr_sum in self.sum

    def to_dict(self):
        """Represent as a Python dict"""
        return {"variables": self.variables, "sum": self.sum}

    @staticmethod
    def from_dict(data):
        """Construct from a Python dict"""
        return ExponentSumConstraint(
            variables=data["variables"],
            sum=data["sum"],
        )


def all_constraints_satisfied(constraints, monomial_exponents):
    for constraint in constraints:
        if not constraint.satisfied(monomial_exponents):
            return False
    return True


def make_symmetry_adapted_polynomials(
    matrix_rep: list[np.ndarray],
    variables: list[Variable],
    variable_subsets: list[list[int]],
    max_poly_order: int,
    min_poly_order: int = 1,
    orthonormalize_in_place: bool = True,
    constraints: list[ExponentSumConstraint] = [],
    eps: float = 1e-14,
    verbose: bool = False,
) -> list[PolynomialFunction]:
    """Generate symmetry adapted polynomial functions

    This method systematically enumerates monomial terms of varying order, applies
    group operations to construct symmetry adapted polynomials, and then orthogonalizes
    the results using the Gram-Schmidt method.

    Notes
    -----

    To support cluster expansion function construction, if any variable has a
    `cluster_site_index` which is not None, then the set of
    `cluster_site_index` is found, and monomials are checked to ensure that they
    have at least one variable on every site in the cluster. Any monomial which
    only has variables on a sub-cluster of sites is skipped.

    Parameters
    ----------
    matrix_rep: list[np.ndarray[np.float]]
        Matrix representation for the symmetry groups acting on the variables.
    variables: list[Variable]
        Describes the variable elements of the vector that `matrix_rep` acts on.
    variable_subsets: list[list[int]]
        The indices of Variable in `variables` which mix under application of symmetry,
        or permute as a group. A subset could be strain variables, displacement
        variables on a site, or occupant site basis functions on a site.
    max_poly_order: int
        Maximum order (sum of exponents) in monomials of the generated
        polynomials.
    min_poly_order: int = 1
        Minimum order (sum of exponents) in monomials of the generated
        polynomials.
    orthonormalize_in_place = True
        If True, orthonormalize symmetry adapted polynomials as they are generated,
        otherwise generate all symmetry adapted polynomials of a particular order and
        then orthonormalize.
    constraints: list[ExponentSumConstraint]
        If any constraint is not satisfied, the candidate monomial is skipped. This
        can be used to ensure one and only one of mutually exclusive discrete variables
        is included in any monomial.
    eps: float = 1e-14
        Tolerance used for identifying zeros in the matrix representations.
    verbose: bool = False
        Print progress statements

    Returns
    -------
    functions: list[PolynomialFunction]
        A list of :class:`~casm.bset.polynomial_function.PolynomialFunction` that are
        invariant to symmetry operations in `matrix_rep` and have been orthonormalized
        according to the scalar product defined in :cite:`THOMAS2017a`.
    """

    n_variables = len(variables)

    function_rep = []
    for i in range(len(matrix_rep)):
        M = matrix_rep[i].copy()
        M[np.abs(M) < eps] = 0.0
        S = FunctionRep(matrix_rep=M)
        function_rep.append(S)

    # check if cluster function:
    is_cluster_function = False
    n_sites = None
    for var in variables:
        if var.cluster_site_index is not None:
            is_cluster_function = True
            if n_sites is None or var.cluster_site_index >= n_sites:
                n_sites = var.cluster_site_index + 1

    # Holds orthonormalized symmetry adapted polynomials of all orders
    all_functions = []

    in_place = orthonormalize_in_place

    for poly_order in range(min_poly_order, max_poly_order + 1):
        if verbose:
            print(f"Working on symmetry adapted polynomials of order {poly_order}")
            if in_place:
                print("Progress (generated / orthonormalized):")
            else:
                print("Progress (generated):")
            sys.stdout.flush()

        # Holds symmetry adapted polynomials of order poly_order
        functions = []
        if in_place:
            orthonormalized_functions = []

        # Counter over all sparse tensor coordinates
        counter = IntCounter(
            initial=[0] * poly_order,
            final=[n_variables - 1] * poly_order,
            increment=[1] * poly_order,
        )

        shape = [n_variables] * poly_order

        f_count = 0
        for x in counter:
            # Using the sparse tensor representation, permutations of coords
            # indicate an equivalent monomial so we skip all but the canonical coord
            if not is_canonical_coord(x):
                continue

            # For cluster functions, want at least one dof from each site:
            if is_cluster_function and is_subcluster_function(x, variables, n_sites):
                continue

            # Skip monomials that do not satisfy exponent constraints
            monomial_exponents = tensor_coord_to_monomial_exponents(x, n_variables)
            if not all_constraints_satisfied(constraints, monomial_exponents):
                continue

            # print("Adding monomial:", x)

            # Create polynomial function coefficients tensor
            coords = x.reshape((-1, 1))  # 2d array with single column containing x
            data = [1.0]  # coefficient value for monomial specified by x
            f_init = PolynomialFunction(
                coeff=sparse.COO(coords, data, shape=shape, prune=True),
                variables=variables,
                variable_subsets=variable_subsets,
            )

            # Apply Reynolds operator to construct symmetrized polynomials
            f_sum = PolynomialFunction.zeros(
                shape=shape,
                variables=variables,
                variable_subsets=variable_subsets,
            )
            for i, S in enumerate(function_rep):
                f_sum += S * f_init

            # If function is not enforced to be 0 by symmetry,
            # then add it to the growing list of symmetry adapted functions
            if len(f_sum.coeff.data) != 0:
                if in_place:
                    next = f_sum.copy()
                    for g in orthonormalized_functions:
                        next -= next.scalar_product(g) * g
                    if len(next.coeff.data) != 0:
                        next.normalize()
                        orthonormalized_functions.append(next)
                functions.append(f_sum)

            if verbose:
                print(".", end="")
                f_count += 1
                sys.stdout.flush()
                if f_count % 10 == 0:
                    if in_place:
                        print(f" {len(functions)} / {len(orthonormalized_functions)}")
                    else:
                        print(f" {len(functions)}")

        if verbose:
            print()
            print(f"- Checked {f_count} monomials of order {poly_order}")
            print(
                f"- Generated {len(functions)} symmetry "
                f"adapted polynomials of order {poly_order}"
            )

        if not in_place:
            orthonormalized_functions = gram_schmidt(functions)
        else:
            orthonormalized_functions.sort()
        all_functions += orthonormalized_functions

        if verbose:
            print(
                f"- Generated {len(orthonormalized_functions)} "
                f"orthonormalized functions of order {poly_order}"
            )
            print(f"- Generated {len(all_functions)} total orthonormalized functions")
            print("")

    return all_functions
