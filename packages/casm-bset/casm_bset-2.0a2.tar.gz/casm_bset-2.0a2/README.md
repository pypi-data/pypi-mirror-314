<img alt="Shows the CASM logo" src="https://raw.githubusercontent.com/prisms-center/CASMcode_global/main/python/doc/_static/logo.svg" width="600" />

#### casm-bset

The casm-bset package is the CASM cluster expansion basis set construction module. This includes:

- Methods for generating coupled cluster expansion Hamiltonians of occupation, strain, displacement, and magnetic spin degrees of freedom (DoF) appropriate for the symmetry of any multi-component crystalline solid.
- Methods for generating C++ code for a CASM cluster expansion calculator (Clexulator) which efficiently evaluates the cluster expansion basis function for configuration represented using the CASM `ConfigDoFValues` data structure
- Generalized methods for creating symmetry adapted basis functions of other variables

This package is designed to work with the cluster expansion calculator (Clexulator) evaluation methods which are implemented in [libcasm-clexulator](https://github.com/prisms-center/CASMcode_clexulator). 


#### Install

    pip install casm-bset


#### Usage

See the [casm docs](https://prisms-center.github.io/CASMcode_pydocs/casm/overview/latest/).


#### About CASM

The casm-bset package is part of the [CASM](https://prisms-center.github.io/CASMcode_docs/) open source software package, which is designed to perform first-principles statistical mechanical studies of multi-component crystalline solids.

CASM is developed by the Van der Ven group, originally at the University of Michigan and currently at the University of California Santa Barbara.

For more information, see the [CASM homepage](https://prisms-center.github.io/CASMcode_docs/).


#### License

GNU Lesser General Public License (LGPL). Please see the file LICENSE for details.

