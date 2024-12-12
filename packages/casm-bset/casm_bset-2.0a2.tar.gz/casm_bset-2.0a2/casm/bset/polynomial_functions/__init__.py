R"""Generate symmetry-adapted polynomials

This module includes:

- :class:`~casm.bset.polynomial_function.Variable`, A variable, :math:`x_i`, in a
  function, which can be transformed by symmetry operations into a linear combination
  of other variables according to user provided symmetry representation matrices,
  :math:`\pmb{M}`, according to :math:`x_j = M_{ji} x_i`.
- :class:`~libcasm.bset.polynomial_function.PolynomialFunction`, A
  polynomial function of a list of :class:`~casm.bset.polynomial_function.Variable`,
  restricted to monomials of the same order (i.e. :math:`x + y` and
  :math:`x_1^2 + x_1x_2 + x_2^2`, but not :math:`x_1 + x_2 + x_1^2 + x_1 x_2 + x_2^2`).
- :class:`~libcasm.bset.polynomial_function.FunctionRep`, A data structure that
  transforms PolynomialFunction according to the user provided symmetry representation
  matrices.

Notes:

- This module works generically; it is not restricted to describing functions of
  crystal degrees of freedom. However, it does allow giving Variable the optional
  attributes `site_basis_function_index`, `cluster_site_index`, and
  `neighborhood_site_index` to support cluster function generation.
- This module uses symmetry representation matrices determined elsewhere.

"""

from ._polynomial_function import (
    ExponentSumConstraint,
    FunctionRep,
    PolynomialFunction,
    Variable,
    gram_schmidt,
    is_canonical_coord,
    make_canonical_coord,
    make_symmetry_adapted_polynomials,
    monomial_exponents_to_tensor_coord,
    monomial_inner_product,
    tensor_coord_to_monomial_exponents,
)
