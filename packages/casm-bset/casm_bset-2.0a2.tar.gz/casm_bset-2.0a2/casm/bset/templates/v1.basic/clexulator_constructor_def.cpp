/// \brief Constructor
{{ clexulator_name }}::{{ clexulator_name }}()
    {%- raw %}
    // BaseClexulator({{ nlist_size }}, {{ n_corr }}, {{ n_point_corr_sites }})
    {% endraw %}
    : BaseClexulator({{ nlist_size }}, {{ n_corr }}, {{ n_point_corr_sites }}) {
{% if occ_site_functions|length > 0 %}

  // Occupation site basis functions
  {%- raw %}
  // m_occ_func_{{ sublattice_index }}_{{ site_function_index }}[{{ occupant_index }}]] = {{ value }};
  {% endraw %}
  {% for site_funcs in occ_site_functions %}
    {% set sublattice_index = site_funcs.sublattice_index %}
    {% for func in site_funcs.value %}
      {% set site_function_index  = loop.index0 %}
      {% for value in func %}
        {% set occupant_index = loop.index0 %}
  m_occ_func_{{ sublattice_index }}_{{ site_function_index }}[{{ occupant_index }}] = {{ value }};
      {% endfor %}
    {% endfor %}
  {% endfor %}
{% endif %}
{% if params|length > 0 %}

  // Parameter packs
  {%- raw %}
  // m_{{ param.name }}_param_key = m_params.allocate("{{ param.name }}", {{ param.rows }}, {{ param.cols }}, {{ param.is_independent }});
  {% endraw %}
  {% for param in params %}
  m_{{ param.name }}_param_key = m_params.allocate("{{ param.name }}", {{ param.rows }}, {{ param.cols }}, {{ param.is_independent }});
  {% endfor %}
{% endif %}
{% if continuous_dof|length > 0 %}

  // Register continuous DoF
  {%- raw %}
  // _register_global_dof("{{ dof.key }}", m_{{ dof.key }}_var_param_key.index());
  // _register_local_dof("{{ dof.key }}", m_{{ dof.key }}_var_param_key.index());
  {% endraw %}
  {% for dof in continuous_dof %}
    {% if dof.is_global %}
  _register_global_dof("{{ dof.key }}", m_{{ dof.key }}_var_param_key.index());
    {% else %}
  _register_local_dof("{{ dof.key }}", m_{{ dof.key }}_var_param_key.index());
    {% endif %}
  {% endfor %}
{% endif %}
{% if orbit_bfuncs|length > 0 %}

  // Orbit functions (evaluate functions without duplication)
  {%- raw %}
  // m_orbit_func_table[{{ function_index }}] = &{{ clexulator_name }}::eval_orbit_bfunc_{{ function_index }}<double>;
  {% endraw %}
  {% for func in orbit_bfuncs %}
    {% set function_index = func.linear_function_index %}
  m_orbit_func_table[{{ function_index }}] = &{{ clexulator_name }}::eval_orbit_bfunc_{{ function_index }}<double>;
  {% endfor %}
{% endif %}
{% if n_point_corr_sites > 0 %}

  // Site functions
  {%- raw %}
  // m_site_func_table[{{ neighbor_list_index }}][{{ function_index }}] =
  //     &{{ clexulator_name }}::eval_site_bfunc_{{ function_index }}_at_{{ neighbor_list_index }}<double>;
  {% endraw %}
  for (int i=0; i<{{ n_point_corr_sites }}; i++) {
    for (int j=0; j<{{ n_corr }}; j++) {
      m_site_func_table[i][j] = &{{ clexulator_name }}::zero_func<double>;
    }
  }
  {% for f_by_function_index in site_bfuncs %}
    {% set function_index = f_by_function_index.linear_function_index %}
    {% for f_by_neighbor_index in f_by_function_index.at %}
      {% set neighbor_list_index = f_by_neighbor_index.neighbor_list_index %}
      {% if f_by_neighbor_index.cpp %}
  m_site_func_table[{{ neighbor_list_index }}][{{ function_index }}] = &{{ clexulator_name }}::eval_site_bfunc_{{ function_index }}_at_{{ neighbor_list_index }}<double>;
      {% endif %}
    {% endfor %}
  {% endfor %}

  // Change in site functions due to an occupant change
  {%- raw %}
  // m_occ_delta_site_func_table[{{ neighbor_list_index }}][{{ function_index }}] =
  //     &{{ clexulator_name }}::eval_occ_delta_site_bfunc_{{ function_index }}_at_{{ neighbor_list_index }}<double>;
  {% endraw %}
  for (int i=0; i<{{ n_point_corr_sites }}; i++) {
    for (int j=0; j<{{ n_corr }}; j++) {
      m_occ_delta_site_func_table[i][j] = &{{ clexulator_name }}::zero_func<double>;
    }
  }
  {% for f_by_function_index in site_bfuncs %}
    {% set function_index = f_by_function_index.linear_function_index %}
    {% for f_by_neighbor_index in f_by_function_index.at %}
      {% set neighbor_list_index = f_by_neighbor_index.neighbor_list_index %}
      {% if f_by_neighbor_index.occ_delta_cpp %}
  m_occ_delta_site_func_table[{{ neighbor_list_index }}][{{ function_index }}] = &{{ clexulator_name }}::eval_occ_delta_site_bfunc_{{ function_index }}_at_{{ neighbor_list_index }}<double>;
      {% endif %}
    {% endfor %}
  {% endfor %}
{% endif %}

  // Neighbor list shape weight matrix
  m_weight_matrix.row(0) << {{ nlist_weight_matrix[0][0] }}, {{ nlist_weight_matrix[0][1] }}, {{ nlist_weight_matrix[0][2] }};
  m_weight_matrix.row(1) << {{ nlist_weight_matrix[1][0] }}, {{ nlist_weight_matrix[1][1] }}, {{ nlist_weight_matrix[1][2] }};
  m_weight_matrix.row(2) << {{ nlist_weight_matrix[2][0] }}, {{ nlist_weight_matrix[2][1] }}, {{ nlist_weight_matrix[2][2] }};

  // Indices of sublattices included in the neighbor list
  m_sublat_indices = std::set<int>{ {% if nlist_sublattice_indices %}
    {%- for i in nlist_sublattice_indices -%} {{ i }},{% endfor %}{% endif %} };

  // Total number of sublattices in prim
  m_n_sublattices = {{ nlist_total_n_sublattice }};

{% if complete_neighborhood.unitcells|length > 0 %}
  // Neighborhood of all basis functions
  m_neighborhood = std::set<xtal::UnitCell> {
  {% for neighbor in complete_neighborhood.unitcells %}
    xtal::UnitCell({{ neighbor[0] }}, {{ neighbor[1] }}, {{ neighbor[2] }}),
  {% endfor %}
  };

{% endif %}
  // Neighborhood by linear function index
  m_orbit_neighborhood.resize(corr_size());
  m_orbit_site_neighborhood.resize(corr_size());

{% for f in function_neighborhoods %}
  {% set function_index = f.linear_function_index %}
  {% if (f.same_as) and function_neighborhoods[f.same_as].sites|length > 0 %}
  m_orbit_neighborhood[{{function_index}}] = m_orbit_neighborhood[{{f.same_as}}];
  m_orbit_site_neighborhood[{{function_index}}] = m_orbit_site_neighborhood[{{f.same_as}}];

  {% else %}
    {% if f.unitcells|length > 0 %}
  m_orbit_neighborhood[{{function_index}}] = std::set<xtal::UnitCell> {
      {% for neighbor in f.unitcells %}
    xtal::UnitCell({{ neighbor[0] }}, {{ neighbor[1] }}, {{ neighbor[2] }}),
      {% endfor %}
  };

    {% endif %}
    {% if f.sites|length > 0 %}
  m_orbit_site_neighborhood[{{function_index}}] = std::set<xtal::UnitCellCoord> {
      {% for neighbor in f.sites %}
    xtal::UnitCellCoord({{ neighbor[0] }}, {{ neighbor[1] }}, {{ neighbor[2] }}, {{ neighbor[3] }}),
      {% endfor %}
  };

    {% endif %}
  {% endif %}
{% endfor %}
}

