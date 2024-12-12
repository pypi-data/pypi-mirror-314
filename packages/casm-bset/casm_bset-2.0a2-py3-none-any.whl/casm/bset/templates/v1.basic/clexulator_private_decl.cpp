{% if orbit_bfuncs|length > 0 %}

  // Orbit functions (evaluate functions without duplication)
  {%- raw %}
  // template<typename Scalar> Scalar eval_orbit_bfunc_{{ function_index }}() const;
  {% endraw %}
  {% for func in orbit_bfuncs %}
    {% set function_index = func.linear_function_index %}
  template<typename Scalar> Scalar eval_orbit_bfunc_{{ function_index }}() const;
  {% endfor %}
{% endif %}
{% if site_bfuncs|length > 0 %}

  // Site functions
  {%- raw %}
  // template<typename Scalar> Scalar eval_site_bfunc_{{ function_index }}_at_{{ neighbor_list_index }}() const;
  {% endraw %}
  {% for f_by_function_index in site_bfuncs %}
    {% set function_index = f_by_function_index.linear_function_index %}
    {% for f_by_neighbor_index in f_by_function_index.at %}
      {% set neighbor_list_index = f_by_neighbor_index.neighbor_list_index %}
      {% if f_by_neighbor_index.cpp %}
  template<typename Scalar> Scalar eval_site_bfunc_{{ function_index }}_at_{{ neighbor_list_index }}() const;
      {% endif %}
    {% endfor %}
  {% endfor %}

  // Change in site functions due to an occupant change
  {%- raw %}
  // template<typename Scalar> Scalar eval_occ_delta_site_bfunc_{{ function_index }}_at_{{ neighbor_list_index }}(int occ_i, int occ_f) const;
  {% endraw %}
  {% for f_by_function_index in site_bfuncs %}
    {% set function_index = f_by_function_index.linear_function_index %}
    {% for f_by_neighbor_index in f_by_function_index.at %}
      {% set neighbor_list_index = f_by_neighbor_index.neighbor_list_index %}
      {% if f_by_neighbor_index.occ_delta_cpp %}
  template<typename Scalar> Scalar eval_occ_delta_site_bfunc_{{ function_index }}_at_{{ neighbor_list_index }}(int occ_i, int occ_f) const;
      {% endif %}
    {% endfor %}
  {% endfor %}
{% endif %}

  // param_pack_type object, which stores temporary data for calculations
  mutable param_pack_type m_params;

  // typedef for method pointers for basis functions and site functions
  typedef double ({{ clexulator_name }}::*BasisFuncPtr)() const;

  // typedef for method pointers for change in site functions due to an occupant change
  typedef double ({{ clexulator_name }}::*DeltaBasisFuncPtr)(int, int) const;
{% if orbit_bfuncs|length > 0 %}

  // array of pointers to member functions for calculating basis functions
  {%- raw %}
  // BasisFuncPtr m_orbit_func_table[{{ n_corr }}];
  {% endraw %}
  BasisFuncPtr m_orbit_func_table[{{ n_corr }}];
{% endif %}
{% if n_point_corr_sites > 0 %}

  // array of pointers to member functions for calculating site functions
  {%- raw %}
  // BasisFuncPtr m_site_func_table[{{ n_point_corr_sites }}][{{ n_corr }}];
  {% endraw %}
  BasisFuncPtr m_site_func_table[{{ n_point_corr_sites }}][{{ n_corr }}];

  // array of pointers to member functions for calculating change in site functions due to an occupant change
  {%- raw %}
  // DeltaBasisFuncPtr m_occ_delta_site_func_table[{{ n_point_corr_sites }}][{{ n_corr }}];
  {% endraw %}
  DeltaBasisFuncPtr m_occ_delta_site_func_table[{{ n_point_corr_sites }}][{{ n_corr }}];
{% endif %}
{% if occ_site_functions|length > 0 %}

  // Occupation site basis functions
  {%- raw %}
  // double m_occ_func_{{ sublattice_index }}_{{ site_function_index }}[{{ n_occupants }}];
  {% endraw %}
  {% for site_funcs in occ_site_functions %}
    {% set sublattice_index = site_funcs.sublattice_index %}
    {% set n_occupants = site_funcs.n_occupants %}
    {% for func in site_funcs.value %}
      {% set site_function_index  = loop.index0 %}
  double m_occ_func_{{ sublattice_index }}_{{ site_function_index }}[{{ n_occupants }}];{% if site_funcs.constant_function_index == site_function_index %} // constant function{% endif +%}
    {% endfor %}
  {% endfor %}
{% endif %}
{% if params|length > 0 %}

  // Parameter packs
  {%- raw %}
  // param_pack_type::Key m_{{ param.name }}_param_key;
  {% endraw %}
  {% for param in params %}
  param_pack_type::Key m_{{ param.name }}_param_key;
  {% endfor %}
{% endif %}

  /// \brief Clone the {{ clexulator_name }}
  BaseClexulator *_clone() const override {
    return new {{ clexulator_name }}(*this);
  }

  // --- Standard method declarations --- //

  /// \brief Calculate contribution to global correlations from one unit cell
  /// Result is recorded in base_param_pack_type
  void _calc_global_corr_contribution() const override;

  /// \brief Calculate contribution to global correlations from one unit cell
  /// Result is recorded in double array starting at corr_begin
  void _calc_global_corr_contribution(double *corr_begin) const override;

  /// \brief Calculate contribution to select global correlations from one unit cell into base_param_pack_type
  /// Result is recorded in base_param_pack_type
  void _calc_restricted_global_corr_contribution(size_type const *ind_list_begin, size_type const *ind_list_end) const override;

  /// \brief Calculate contribution to select global correlations from one unit cell
  /// Result is recorded in double array starting at corr_begin
  void _calc_restricted_global_corr_contribution(double *corr_begin, size_type const *ind_list_begin, size_type const *ind_list_end) const override;

  /// \brief Calculate point correlations about neighbor site 'nlist_ind'
  /// For global clexulators, 'nlist_ind' only ranges over sites in the cell
  /// For local clexulators, 'nlist_ind' ranges over all sites in the neighborhood
  /// Result is recorded in base_param_pack_type
  void _calc_point_corr(int nlist_ind) const override;

  /// \brief Calculate point correlations about neighbor site 'nlist_ind'
  /// For global clexulators, 'nlist_ind' only ranges over sites in the cell
  /// For local clexulators, 'nlist_ind' ranges over all sites in the neighborhood
  /// Result is recorded in double array starting at corr_begin
  void _calc_point_corr(int nlist_ind, double *corr_begin) const override;

  /// \brief Calculate select point correlations about neighbor site 'nlist_ind'
  /// For global clexulators, 'nlist_ind' only ranges over sites in the cell
  /// For local clexulators, 'nlist_ind' ranges over all sites in the neighborhood
  /// Result is recorded in base_param_pack_type
  void _calc_restricted_point_corr(int nlist_ind, size_type const *ind_list_begin, size_type const *ind_list_end) const override;

  /// \brief Calculate select point correlations about neighbor site 'nlist_ind'
  /// For global clexulators, 'nlist_ind' only ranges over sites in the cell
  /// For local clexulators, 'nlist_ind' ranges over all sites in the neighborhood
  /// Result is recorded in double array starting at corr_begin
  void _calc_restricted_point_corr(int nlist_ind, double *corr_begin, size_type const *ind_list_begin, size_type const *ind_list_end) const override;

  /// \brief Calculate the change in point correlations due to changing an occupant at neighbor site 'nlist_ind'
  /// For global clexulators, 'nlist_ind' only ranges over sites in the cell
  /// For local clexulators, 'nlist_ind' ranges over all sites in the neighborhood
  /// Result is recorded in base_param_pack_type
  void _calc_delta_point_corr(int nlist_ind, int occ_i, int occ_f) const override;

  /// \brief Calculate the change in point correlations due to changing an occupant at neighbor site 'nlist_ind'
  /// For global clexulators, 'nlist_ind' only ranges over sites in the cell
  /// For local clexulators, 'nlist_ind' ranges over all sites in the neighborhood
  /// Result is recorded in double array starting at corr_begin
  void _calc_delta_point_corr(int nlist_ind, int occ_i, int occ_f, double *corr_begin) const override;

  /// \brief Calculate the change in select point correlations due to changing an occupant at neighbor site 'nlist_ind'
  /// For global clexulators, 'nlist_ind' only ranges over sites in the cell
  /// For local clexulators, 'nlist_ind' ranges over all sites in the neighborhood
  /// Result is recorded in base_param_pack_type
  void _calc_restricted_delta_point_corr(int nlist_ind, int occ_i, int occ_f, size_type const *ind_list_begin, size_type const *ind_list_end) const override;

  /// \brief Calculate the change in select point correlations due to changing an occupant at neighbor site 'nlist_ind'
  /// For global clexulators, 'nlist_ind' only ranges over sites in the cell
  /// For local clexulators, 'nlist_ind' ranges over all sites in the neighborhood
  /// Result is recorded in double array starting at corr_begin
  void _calc_restricted_delta_point_corr(int nlist_ind, int occ_i, int occ_f, double *corr_begin, size_type const *ind_list_begin, size_type const *ind_list_end) const override;

  /// \brief Evaluate site basis functions and copy values to parameter packs
  /// for orbit function evaluation
  template<typename Scalar>
  void _global_prepare() const;

  /// \brief Evaluate site basis functions and copy values to parameter packs
  /// for site function evaluation
  template<typename Scalar>
  void _point_prepare(int nlist_ind) const;

  /// \brief Default zero function for orbit function evaluation
  template <typename Scalar>
  Scalar zero_func() const {
    return Scalar(0.0);
  }

  /// \brief Default zero function for site function evaluation
  template <typename Scalar>
  Scalar zero_func(int, int) const {
    return Scalar(0.0);
  }
{% if occ_site_functions|length > 0 and "occ" in orbit_bfuncs_variables_needed %}

  // --- Occupation function evaluators and accessors: --- //
  {% raw %}
  // double const &eval_occ_func_{{ sublattice_index }}_{{ site_function_index }}(const int &nlist_ind) const {
  //   return m_occ_func_{{ sublattice_index }}_{{ site_function_index }}[_occ(nlist_ind)];
  // }
  //
  // double const &occ_func_{{ sublattice_index }}_{{ site_function_index }}(const int &nlist_ind) const {
  //   return m_params.read(m_occ_site_func_param_key, {{ site_function_index }}, nlist_ind);
  // }
  {% endraw %}

  {% for site_funcs in occ_site_functions %}
    {% set sublattice_index = site_funcs.sublattice_index %}
    {% set n_occupants = site_funcs.n_occupants %}
    {% for func in site_funcs.value %}
      {% set site_function_index  = loop.index0 %}
        {% if site_funcs.constant_function_index != site_function_index %}
  double const &eval_occ_func_{{ sublattice_index }}_{{ site_function_index }}(const int &nlist_ind) const {
    return m_occ_func_{{ sublattice_index }}_{{ site_function_index }}[_occ(nlist_ind)];
  }

  double const &occ_func_{{ sublattice_index }}_{{ site_function_index }}(const int &nlist_ind) const {
    return m_params.read(m_occ_site_func_param_key, {{ site_function_index }}, nlist_ind);
  }

        {% endif %}
    {% endfor %}
  {% endfor %}
{% endif %}
{% if continuous_dof|length > 0 %}
  {% for dof in continuous_dof %}
    {% if dof.key not in orbit_bfuncs_variables_needed %}

  // --- {{ dof.key }} DoF evaluators and accessors not required --- //

    {% elif dof.is_global %}

  // --- {{ dof.key }} Global DoF evaluators and accessors: --- //

  double eval_{{ dof.key }}_var(const int &ind) const {
    return (*(m_global_dof_ptrs[m_{{ dof.key }}_var_param_key.index()]))[ind];
  }

  template<typename Scalar>
  Scalar const &{{ dof.key }}_var(const int &ind) const {
    return param_pack_type::Val<Scalar>::get(m_params, m_{{ dof.key }}_var_param_key, ind);
  }
    {% else %}
  // --- {{ dof.key }} Local DoF evaluators and accessors: --- //
      {% raw %}
  // double eval_{{ dof.key }}_var_{{ sublattice_index }}_{{ component_index }}(const int &nlist_ind) const {
  //   return m_local_dof_ptrs[m_{{ key }}_var_param_key.index()]->col(_l(nlist_ind))[{{ component_index }}];
  // }
  //
  // template<typename Scalar>
  // Scalar const &{{ dof.key }}_var_{{ component_index }}(const int &nlist_ind) const {
  //   return param_pack_type::Val<Scalar>::get(m_params, m_{{ key }}_var_param_key, {{ component_index }}, nlist_ind);
  // }
      {% endraw %}
      {% for site in dof.sites %}
        {% set sublattice_index = site.sublattice_index %}
        {% for component_index in range(site.n_components) %}
  double eval_{{ dof.key }}_var_{{ sublattice_index }}_{{ component_index }}(const int &nlist_ind) const {
    return m_local_dof_ptrs[m_{{ dof.key }}_var_param_key.index()]->col(_l(nlist_ind))[{{ component_index }}];
  }
        {% endfor %}
      {% endfor %}
      {% for component_index in range(dof.max_n_components) %}
  template<typename Scalar>
  Scalar const &{{ dof.key }}_var_{{ component_index }}(const int &nlist_ind) const {
    return param_pack_type::Val<Scalar>::get(m_params, m_{{ dof.key }}_var_param_key, {{ component_index }}, nlist_ind);
  }
      {% endfor %}
    {% endif %}
  {% endfor %}
{% endif %}
