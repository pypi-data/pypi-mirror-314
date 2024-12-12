from typing import Optional

import numpy as np

from casm.bset.misc import (
    almost_equal,
    factor_by_mode,
    irrational_to_tex_string,
)
from casm.bset.polynomial_functions import (
    PolynomialFunction,
    Variable,
)
from libcasm.clexulator import (
    PrimNeighborList,
)


class CppFormatProperties:
    """Holds options for C++ formatting"""

    def __init__(
        self,
        coeff_fmt_spec: str = ".10f",
        coeff_atol: float = 1e-10,
    ):
        """

        .. rubric:: Constructor

        Parameters
        ----------
        coeff_fmt_spec: str
            Format specification for coefficient printing.

        coeff_atol: float
            Tolerance for checking for zeros and ones.
        """
        self.coeff_fmt_spec = coeff_fmt_spec
        """str: Format specification for coefficient printing."""

        self.coeff_atol = coeff_atol
        """float: Tolerance for checking for zeros and ones."""


def is_one(x, atol: float = 1e-10):
    return almost_equal(x, 1.0, abs_tol=atol)


def occ_func_cpp_str(
    var: Variable,
    prim_neighbor_list: PrimNeighborList,
    occupant_index_argname: str,
    mode: str = "cpp",
) -> str:
    """Return a C++ expression to evaluate an occupation site basis variable

    Parameters
    ----------
    var: casm.bset.Variable
        A :class:`casm.bset.Variable` representing the occupation site basis
        function being evaluated.
    prim_neighbor_list: libcasm.clexulator.PrimNeighborList
        The primitive neighbor list, used to find the sublattice index
    occupant_index_argname: str
        The occupant index argument name. Usually "occ_i" or "occ_f".
    mode: str = "cpp"
        The mode for the output. Options are "cpp" and "latex".

    Returns
    -------
    cpp_str: str
        C++ expression to evaluate the specified variable, with form:

        .. code-block:: Python

            # b: int, sublattice index
            # m: int, site basis function index
            cpp_str = f"m_occ_func{b}_{m}[{occupant_index_argname}]"

    """
    if var.key != "occ":
        raise Exception('Error in occ_func_cpp_str: key != "occ"')
    # occupant_index_str = "occ_i", "occ_f"
    nlist_sublat_indices = prim_neighbor_list.sublattice_indices()
    i = var.neighborhood_site_index % len(nlist_sublat_indices)
    b = nlist_sublat_indices[i]
    m = var.site_basis_function_index
    n = var.neighborhood_site_index
    if mode == "cpp":
        return f"m_occ_func_{b}_{m}[{occupant_index_argname}]"
    elif mode == "latex":
        return f"{var.name}({occupant_index_argname}_{{{n}}})"
        # return f"\\phi_{{{b},{m}}}({occupant_index_argname}_{{{n}}})"
    else:
        raise ValueError(f"Invalid mode: {mode}")


def variable_cpp_str(
    var: Variable,
    prim_neighbor_list: PrimNeighborList,
    mode: str = "cpp",
    label_site_using: str = "neighborhood_site_index",
) -> str:
    """Return a C++ expression to access an evaluated variable

    Parameters
    ----------
    var: casm.bset.polynomial_functions.Variable
        The variable to be accessed.
    prim_neighbor_list: PrimNeighborList
        The PrimNeighborList used when constructing the functions.
    mode: str = "cpp"
        The mode for the output. Options are "cpp" and "latex".
    label_site_using = "neighborhood_site_index"
        The label to use for the site index in the output. Options are
        "neighborhood_site_index" and "cluster_site_index".

    Returns
    -------
    cpp_str: str
        A C++ expression for a function that accesses the evaluated value of the
        variable.

    """
    nlist_sublat_indices = prim_neighbor_list.sublattice_indices()
    if var.key == "occ":
        # occ DoF / site basis function
        i = var.neighborhood_site_index % len(nlist_sublat_indices)
        b = nlist_sublat_indices[i]
        m = var.site_basis_function_index
        n = var.neighborhood_site_index
        cl = var.cluster_site_index
        if mode == "cpp":
            return f"occ_func_{b}_{m}({n})"
        elif mode == "latex":
            if label_site_using == "neighborhood_site_index":
                return f"{var.name}(\\vec{{r}}_{{{n}}})"
            elif label_site_using == "cluster_site_index":
                return f"{var.name}(\\vec{{r}}_{{{cl}}})"
            else:
                raise ValueError(f"Invalid label_site_using: {label_site_using}")
        else:
            raise ValueError(f"Invalid mode: {mode}")
    elif var.neighborhood_site_index is not None:
        # local continuous DoF
        c = var.component_index
        n = var.neighborhood_site_index
        cl = var.cluster_site_index
        if mode == "cpp":
            return f"{var.key}_var_{c}<Scalar>({n})"
        elif mode == "latex":
            if label_site_using == "neighborhood_site_index":
                return f"{var.name}(\\vec{{r}}_{{{n}}})"
            elif label_site_using == "cluster_site_index":
                return f"{var.name}(\\vec{{r}}_{{{cl}}})"
            else:
                raise ValueError(f"Invalid label_site_using: {label_site_using}")
        else:
            raise ValueError(f"Invalid mode: {mode}")
    else:
        # global continuous DoF
        c = var.component_index
        if mode == "cpp":
            return f"{var.key}_var<Scalar>({c})"
        elif mode == "latex":
            return f"{var.name}"
        else:
            raise ValueError(f"Invalid mode: {mode}")


def monomial_cpp_str(
    variables: list[Variable],
    coeff: float,
    monomial_exponents: np.ndarray,
    prim_neighbor_list: PrimNeighborList,
    cpp_fmt: CppFormatProperties,
    mode: str = "cpp",
    label_site_using: str = "neighborhood_site_index",
) -> str:
    """Return a C++ expression to evaluate a monomial

    Parameters
    ----------
    variables: list[casm.bset.polynomial_functions.Variable]
        The variables associated with the PolynomialFunction including this monomial.
    coeff: float
        The monomial coefficient.
    prim_neighbor_list: PrimNeighborList
        The PrimNeighborList used when constructing the functions.
    cpp_fmt: CppFormatProperties
        C++ string formatting properties.
    mode: str = "cpp"
        The mode for the output. Options are "cpp" and "latex".
    label_site_using = "neighborhood_site_index"
        The label to use for the site index in the output. Options are
        "neighborhood_site_index" and "cluster_site_index".

    Returns
    -------
    cpp_str: str
        A C++ expression to evaluate the monomial and multiply by the coefficient.

    """
    if (monomial_exponents == np.zeros(monomial_exponents.shape)).all():
        return "1"

    use_mul = False
    cpp_str = ""
    if not is_one(coeff, atol=cpp_fmt.coeff_atol):
        cpp_str += f"{coeff:{cpp_fmt.coeff_fmt_spec}}"
        use_mul = True
    for i_var, x in enumerate(monomial_exponents):
        if x == 0:
            continue
        v = variable_cpp_str(
            variables[i_var],
            prim_neighbor_list,
            mode=mode,
            label_site_using=label_site_using,
        )
        if use_mul:
            if mode == "cpp":
                op = "*"
            elif mode == "latex":
                op = " "
            else:
                raise ValueError(f"Invalid mode: {mode}")
        else:
            op = ""
            use_mul = True
        if x == 1:
            cpp_str += f"{op}{v}"
        else:
            if mode == "cpp":
                cpp_str += f"{op}pow({v},{x})"
            elif mode == "latex":
                cpp_str += f"{op}{v}^{{{x}}}"
            else:
                raise ValueError(f"Invalid mode: {mode}")
    return cpp_str


def polynomial_sum_cpp_str(
    functions: list[PolynomialFunction],
    normalization: float,
    prim_neighbor_list: PrimNeighborList,
    cpp_fmt: CppFormatProperties,
    mode: str = "cpp",
    label_site_using: str = "neighborhood_site_index",
) -> str:
    """Return a C++ expression to evaluate a polynomial expression

    Parameters
    ----------
    functions: list[PolynomialFunction]
        The symmetrically equivalent cluster functions (i.e. that have the same
        expansion coefficient) associated with a single unit cell that need to be
        evaluated.
    normalization: float
        The normalization constant.
    prim_neighbor_list: PrimNeighborList
        The PrimNeighborList used when constructing the functions.
    cpp_fmt: CppFormatProperties
        C++ string formatting properties.
    mode: str = "cpp"
        The mode for the output. Options are "cpp" and "latex".
    label_site_using = "neighborhood_site_index"
        The label to use for the site index in the output. Options are
        "neighborhood_site_index" and "cluster_site_index".

    Returns
    -------
    cpp_str: str
        A C++ expression to evaluate the sum of polynomial functions.

    """
    if len(functions) == 0:
        return "0."

    prefix_coeff = []
    factored_coeff = []
    for function in functions:
        _prefix_coeff, _factored_coeff = factor_by_mode(function.coeff.data)
        prefix_coeff.append(_prefix_coeff)
        factored_coeff.append(_factored_coeff)

    common_prefix, factored_prefixes = factor_by_mode(np.array(prefix_coeff))

    cpp_str = ""
    if not is_one(common_prefix, atol=cpp_fmt.coeff_atol):
        if mode == "cpp":
            cpp_str += f"{common_prefix:{cpp_fmt.coeff_fmt_spec}} * "
        elif mode == "latex":
            limit = len(functions[0].variables) ** 2
            max_pow = 2
            common_prefix_tex = irrational_to_tex_string(
                common_prefix, limit=limit, max_pow=max_pow, abs_tol=1e-5
            )
            cpp_str += f"{common_prefix_tex} "
    if len(functions) > 1:
        cpp_str += "(\n"

    indent = "  "
    orbit_use_plus = False
    for i_func, function in enumerate(functions):
        if len(functions) > 1:
            cpp_str += indent * 2
        if orbit_use_plus:
            cpp_str += " + "
        else:
            orbit_use_plus = True
        if not is_one(factored_prefixes[i_func], atol=cpp_fmt.coeff_atol):
            cpp_str += f"{factored_prefixes[i_func]:{cpp_fmt.coeff_fmt_spec}} * "
        if len(function.monomial_exponents) > 1:
            cpp_str += "("
        cluster_use_plus = False
        for i_monomial, _monomial_exponents in enumerate(function.monomial_exponents):
            if cluster_use_plus:
                op = " + "
            else:
                op = ""
                cluster_use_plus = True
            cpp_str += op + monomial_cpp_str(
                variables=function.variables,
                coeff=factored_coeff[i_func][i_monomial],
                monomial_exponents=_monomial_exponents,
                prim_neighbor_list=prim_neighbor_list,
                cpp_fmt=cpp_fmt,
                mode=mode,
                label_site_using=label_site_using,
            )
        if len(function.monomial_exponents) > 1:
            cpp_str += ")"
        if len(functions) > 1:
            cpp_str += "\n"

    if len(functions) > 1:
        cpp_str += indent * 1 + ")"
    if not is_one(normalization, atol=cpp_fmt.coeff_atol):
        cpp_str += f" / {normalization}"
    return cpp_str


def orbit_bfunc_cpp_str(
    orbit_functions: list[PolynomialFunction],
    orbit_size: int,
    prim_neighbor_list: PrimNeighborList,
    cpp_fmt: CppFormatProperties,
    mode: str = "cpp",
    label_site_using: str = "neighborhood_site_index",
) -> str:
    """Return a C++ expression to evaluate a single orbit basis function

    Parameters
    ----------
    orbit_functions: list[PolynomialFunction]
        The symmetrically equivalent cluster functions (i.e. that have the same
        expansion coefficient) associated with a single unit cell that need to be
        evaluated.
    orbit_size: int
        The number of clusters in the orbit, per unit cell. Used for normalization.
    prim_neighbor_list: PrimNeighborList
        The PrimNeighborList used when constructing the functions.
    cpp_fmt: CppFormatProperties
        C++ string formatting properties.
    mode: str = "cpp"
        The mode for the output. Options are "cpp" and "latex".
    label_site_using = "neighborhood_site_index"
        The label to use for the site index in the output. Options are
        "neighborhood_site_index" and "cluster_site_index".

    Returns
    -------
    cpp_str: str
        A C++ expression to evaluate the sum of polynomial functions involved in the
        calculation of the contribution to the correlations from one unit cell (for a
        periodic cluster expansion) or for one local-cluster correlation value.

    """
    return polynomial_sum_cpp_str(
        functions=orbit_functions,
        normalization=float(orbit_size),
        prim_neighbor_list=prim_neighbor_list,
        cpp_fmt=cpp_fmt,
        mode=mode,
        label_site_using=label_site_using,
    )


def site_bfunc_cpp_str(
    point_functions: list[PolynomialFunction],
    orbit_size: int,
    prim_neighbor_list: PrimNeighborList,
    cpp_fmt: CppFormatProperties,
    mode: str = "cpp",
    label_site_using: str = "neighborhood_site_index",
) -> Optional[str]:
    """Return a C++ expression to evaluate a single point correlation function

    Parameters
    ----------
    point_functions: list[PolynomialFunction]
        The symmetrically equivalent cluster functions (i.e. that have the same
        expansion coefficient) that include the site at which the point correlations are
        evaluated.
    orbit_size: int
        The number of clusters in the orbit, per unit cell. Used for normalization.
    prim_neighbor_list: PrimNeighborList
        The PrimNeighborList used when constructing the functions.
    cpp_fmt: CppFormatProperties
        C++ string formatting properties.
    mode: str = "cpp"
        The mode for the output. Options are "cpp" and "latex".

    Returns
    -------
    cpp_str: str
        A C++ expression to evaluate a single point correlation function (for either
        periodic or local-cluster expansions).

    """
    if len(point_functions) == 0:
        return None
    return polynomial_sum_cpp_str(
        functions=point_functions,
        normalization=float(orbit_size),
        prim_neighbor_list=prim_neighbor_list,
        cpp_fmt=cpp_fmt,
        mode=mode,
        label_site_using=label_site_using,
    )


def occ_delta_site_bfunc_cpp_str(
    neighbor_list_index: int,
    point_functions: list[PolynomialFunction],
    orbit_size: int,
    prim_neighbor_list: PrimNeighborList,
    cpp_fmt: CppFormatProperties,
    mode: str = "cpp",
    label_site_using: str = "neighborhood_site_index",
) -> Optional[str]:
    """Return a C++ expression to evaluate the change in a single point correlation \
    function due to a change in occupation

    Parameters
    ----------
    neighbor_list_index: int
        The index in the prim neighbor list of the site with changing occupation.
    point_functions: list[PolynomialFunction]
        The symmetrically equivalent cluster functions (i.e. that have the same
        expansion coefficient) that include the site at which the point correlations are
        evaluated.
    orbit_size: int
        The number of clusters in the orbit, per unit cell. Used for normalization.
    prim_neighbor_list: PrimNeighborList
        The PrimNeighborList used when constructing the functions.
    cpp_fmt: CppFormatProperties
        C++ string formatting properties.
    mode: str = "cpp"
        The mode for the output. Options are "cpp" and "latex".

    Returns
    -------
    cpp_str: str
        A C++ expression to evaluate the change in a single point correlation function
        due to a change in occupation (for either periodic or local-cluster expansions).
"""
    if len(point_functions) == 0:
        return None

    def find_occ_site_var(monomial: PolynomialFunction):
        variables = monomial.variables
        if len(monomial.monomial_exponents) != 1:
            raise Exception(
                "Error in occ_delta_site_bfunc_cpp_str: "
                "failed to split point function into monomials"
            )

        occ_site_var = None
        for i_var, x in enumerate(monomial.monomial_exponents[0]):
            if x == 0:
                continue
            var = variables[i_var]
            if var.key != "occ":
                continue
            if var.neighborhood_site_index == neighbor_list_index:
                if occ_site_var is not None:
                    raise Exception(
                        "Error in occ_delta_site_bfunc_cpp_str: "
                        ">1 occ site basis function found in monomial"
                    )
                occ_site_var = var
        return occ_site_var

    monomials = []
    for point_function in point_functions:
        monomials += point_function.monomials()

    occ_delta_functions = {}
    for monomial in monomials:
        var = find_occ_site_var(monomial)
        if var is not None:
            if var not in occ_delta_functions:
                occ_delta_functions[var] = []
            occ_delta_functions[var].append(monomial / var)

    if len(occ_delta_functions) == 0:
        return None

    indent = "  "
    cpp_str = ""
    use_plus = False
    if mode == "cpp":
        occupant_index_argname_final = "occ_f"
        occupant_index_argname_init = "occ_i"
    elif mode == "latex":
        occupant_index_argname_final = "\\vec{r}^{\\ f}"
        occupant_index_argname_init = "\\vec{r}^{\\ i}"
    else:
        raise ValueError(f"Invalid mode: {mode}")

    for var, factored_point_functions in occ_delta_functions.items():
        site_var_final = occ_func_cpp_str(
            var=var,
            prim_neighbor_list=prim_neighbor_list,
            occupant_index_argname=occupant_index_argname_final,
            mode=mode,
        )
        site_var_init = occ_func_cpp_str(
            var=var,
            prim_neighbor_list=prim_neighbor_list,
            occupant_index_argname=occupant_index_argname_init,
            mode=mode,
        )
        if use_plus:
            cpp_str += "\n\n" + indent * 1 + " + "
        else:
            use_plus = True
        cpp_str += f"({site_var_final} - {site_var_init}) * "
        cpp_str += polynomial_sum_cpp_str(
            functions=factored_point_functions,
            normalization=float(orbit_size),
            prim_neighbor_list=prim_neighbor_list,
            cpp_fmt=cpp_fmt,
            mode=mode,
            label_site_using=label_site_using,
        )
    return cpp_str
