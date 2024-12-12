/// \brief Calculate contribution to global correlations from one unit cell
void {{ clexulator_name }}::_calc_global_corr_contribution(
    double *corr_begin) const {
  _calc_global_corr_contribution();
  for (size_type i = 0; i < corr_size(); i++) {
    *(corr_begin + i) =
        param_pack_type::Val<double>::get(m_params, m_corr_param_key, i);
  }
}

/// \brief Calculate contribution to global correlations from one unit cell
void {{ clexulator_name }}::_calc_global_corr_contribution() const {
  m_params.pre_eval();
  {
    _global_prepare<double>();
    for (size_type i = 0; i < corr_size(); i++) {
      param_pack_type::Val<double>::set(m_params, m_corr_param_key, i,
                                  (this->*m_orbit_func_table[i])());
    }
  }
  m_params.post_eval();
}

/// \brief Calculate contribution to select global correlations from one unit cell
void {{ clexulator_name }}::_calc_restricted_global_corr_contribution(
    double *corr_begin,
    size_type const *ind_list_begin,
    size_type const *ind_list_end) const {
  _calc_restricted_global_corr_contribution(ind_list_begin, ind_list_end);
  for(; ind_list_begin < ind_list_end; ind_list_begin++) {
    *(corr_begin + *ind_list_begin) = param_pack_type::Val<double>::get(m_params, m_corr_param_key, *ind_list_begin);
  }
}

/// \brief Calculate contribution to select global correlations from one unit cell
void {{ clexulator_name }}::_calc_restricted_global_corr_contribution(size_type const *ind_list_begin, size_type const *ind_list_end) const {
  m_params.pre_eval();
  {
    _global_prepare<double>();
    for(; ind_list_begin < ind_list_end; ind_list_begin++) {
      param_pack_type::Val<double>::set(m_params, m_corr_param_key, *ind_list_begin, (this->*m_orbit_func_table[*ind_list_begin])());
    }
  }
  m_params.post_eval();
}

/// \brief Calculate point correlations about basis site 'nlist_ind'
void {{ clexulator_name }}::_calc_point_corr(int nlist_ind, double *corr_begin) const {
{% if n_point_corr_sites > 0 %}
  _calc_point_corr(nlist_ind);
  for(size_type i = 0; i < corr_size(); i++) {
    *(corr_begin + i) = param_pack_type::Val<double>::get(m_params, m_corr_param_key, i);
  }
{% endif %}
}

/// \brief Calculate point correlations about basis site 'nlist_ind'
void {{ clexulator_name }}::_calc_point_corr(int nlist_ind) const {
{% if n_point_corr_sites > 0 %}
  m_params.pre_eval();
  {
    _point_prepare<double>(nlist_ind);
    for(size_type i = 0; i < corr_size(); i++) {
      param_pack_type::Val<double>::set(m_params, m_corr_param_key, i, (this->*m_site_func_table[nlist_ind][i])());
    }
  }
  m_params.post_eval();
{% endif %}
}

/// \brief Calculate select point correlations about basis site 'nlist_ind'
void {{ clexulator_name }}::_calc_restricted_point_corr(int nlist_ind, double *corr_begin, size_type const *ind_list_begin, size_type const *ind_list_end) const {
{% if n_point_corr_sites > 0 %}
  _calc_restricted_point_corr(nlist_ind, ind_list_begin, ind_list_end);
  for(; ind_list_begin < ind_list_end; ind_list_begin++) {
    *(corr_begin + *ind_list_begin) = param_pack_type::Val<double>::get(m_params, m_corr_param_key, *ind_list_begin);
  }
{% endif %}
}

/// \brief Calculate select point correlations about basis site 'nlist_ind'
void {{ clexulator_name }}::_calc_restricted_point_corr(int nlist_ind, size_type const *ind_list_begin, size_type const *ind_list_end) const {
{% if n_point_corr_sites > 0 %}
m_params.pre_eval();
  {
    _point_prepare<double>(nlist_ind);
    for(; ind_list_begin < ind_list_end; ind_list_begin++) {
      param_pack_type::Val<double>::set(m_params, m_corr_param_key, *ind_list_begin, (this->*m_site_func_table[nlist_ind][*ind_list_begin])());
    }
  }
  m_params.post_eval();
{% endif %}
}

/// \brief Calculate the change in point correlations due to changing an occupant
void {{ clexulator_name }}::_calc_delta_point_corr(int nlist_ind, int occ_i, int occ_f, double *corr_begin) const {
{% if n_point_corr_sites > 0 %}
  _calc_delta_point_corr(nlist_ind, occ_i, occ_f);
  for(size_type i = 0; i < corr_size(); i++) {
    *(corr_begin + i) = param_pack_type::Val<double>::get(m_params, m_corr_param_key, i);
  }
{% endif %}
}

/// \brief Calculate the change in point correlations due to changing an occupant
void {{ clexulator_name }}::_calc_delta_point_corr(int nlist_ind, int occ_i, int occ_f) const {
{% if n_point_corr_sites > 0 %}
  m_params.pre_eval();
  {
    _point_prepare<double>(nlist_ind);
    for(size_type i = 0; i < corr_size(); i++) {
      param_pack_type::Val<double>::set(m_params, m_corr_param_key, i, (this->*m_occ_delta_site_func_table[nlist_ind][i])(occ_i, occ_f));
    }
  }
  m_params.post_eval();
{% endif %}
}

/// \brief Calculate the change in select point correlations due to changing an occupant
void {{ clexulator_name }}::_calc_restricted_delta_point_corr(int nlist_ind, int occ_i, int occ_f, double *corr_begin, size_type const *ind_list_begin, size_type const *ind_list_end) const {
{% if n_point_corr_sites > 0 %}
  _calc_restricted_delta_point_corr(nlist_ind, occ_i, occ_f, ind_list_begin, ind_list_end);
  for(; ind_list_begin < ind_list_end; ind_list_begin++) {
    *(corr_begin + *ind_list_begin) = param_pack_type::Val<double>::get(m_params, m_corr_param_key, *ind_list_begin);
  }
{% endif %}
}

/// \brief Calculate the change in select point correlations due to changing an occupant
void {{ clexulator_name }}::_calc_restricted_delta_point_corr(int nlist_ind, int occ_i, int occ_f, size_type const *ind_list_begin, size_type const *ind_list_end) const {
{% if n_point_corr_sites > 0 %}
  m_params.pre_eval();
  {
    _point_prepare<double>(nlist_ind);
    for(; ind_list_begin < ind_list_end; ind_list_begin++) {
      param_pack_type::Val<double>::set(m_params, m_corr_param_key, *ind_list_begin, (this->*m_occ_delta_site_func_table[nlist_ind][*ind_list_begin])(occ_i, occ_f));
    }
  }
  m_params.post_eval();
{% endif %}
}

/// --- Prepare variables for global corr evaluation  ---

template<typename Scalar>
void {{ clexulator_name }}::_global_prepare() const {
{% for key, variables in orbit_bfuncs_variables_needed.items() %}
  {%- if key == "occ" %}{# /*DISCRETE DOF*/ #}
    {% set param_key = "m_occ_site_func_param_key" %}
  {% else %}
    {% set param_key = "m_" + key + "_var_param_key" %}
  {% endif %}
  if(m_params.eval_mode({{ param_key}}) != param_pack_type::READ) {
    {%- if key == "occ" %}{# /*DISCRETE DOF*/ #}
      {% raw %}
    // param_pack_type::Val<Scalar>::set(
    //     m_params, {{ param_key}}, {{ site_function_index }}, {{ neighbor_list_index }},
    //     eval_occ_func_{{ sublattice_index }}_{{ site_function_index }}({{ neighbor_list_index }}));
      {% endraw %}
    {% elif neighbor_list_index is not none %}{# /*LOCAL CONTINUOUS DOF*/ #}
      {% raw %}
    // param_pack_type::Val<Scalar>::set(m_params, {{ param_key}}, {{ component_index }}, {{ neighbor_list_index }}, eval_{{ key }}_var_{{ sublattice_index }}_{{ component_index }}({{ neighbor_list_index }}));
      {% endraw %}
    {% else %}{# /*GLOBAL CONTINUOUS DOF*/ #}
      {% raw %}
    // param_pack_type::Val<Scalar>::set(m_params, {{ param_key}}, {{ component_index }}, eval_{{ key }}_var({{ component_index }}));
      {% endraw %}
    {% endif %}
    {% for var_indices in variables %}
      {% set neighbor_list_index = var_indices[1] %}
      {% set sublattice_index = var_indices[2] %}
      {% if key == "occ" %}{# /*DISCRETE DOF*/ #}
        {% set site_function_index = var_indices[0] %}
    param_pack_type::Val<Scalar>::set(m_params, {{ param_key}}, {{ site_function_index }}, {{ neighbor_list_index }}, eval_occ_func_{{ sublattice_index }}_{{ site_function_index }}({{ neighbor_list_index }}));
      {% elif neighbor_list_index is not none %}{# /*LOCAL CONTINUOUS DOF*/ #}
        {% set component_index = var_indices[0] %}
    param_pack_type::Val<Scalar>::set(m_params, {{ param_key}}, {{ component_index }}, {{ neighbor_list_index }}, eval_{{ key }}_var_{{ sublattice_index }}_{{ component_index }}({{ neighbor_list_index }}));
      {% else %}{# /*GLOBAL CONTINUOUS DOF*/ #}
        {% set component_index = var_indices[0] %}
    param_pack_type::Val<Scalar>::set(m_params, {{ param_key}}, {{ component_index }}, eval_{{ key }}_var({{ component_index }}));
      {% endif %}
    {% endfor %}
  }
{% endfor %}
}
{% if orbit_bfuncs|length > 0 %}

/// --- Global corr contributions ---
  {% raw %}
// template<typename Scalar>
// Scalar {{ clexulator_name }}::eval_orbit_bfunc_{{ function_index }}() const {
//   // orbit_index: {{ orbit_index }}
//   // function_index: {{ function_index }}
//   return {{ factored_orbit_prefix }}(
//     {{ factored_cluster_prefix_0 }}({{ factored_cluster_function_0 }})
//     + {{ factored_cluster_prefix_1 }}({{ factored_cluster_function_1 }})
//     ...
//     ) / {{ orbit_mult }};
// }
  {% endraw %}
  {% for func in orbit_bfuncs %}
    {% set function_index = func.linear_function_index %}
    {% set orbit_index = func.linear_orbit_index %}
    {% set cpp = func.cpp %}
    {% if cpp %}

template<typename Scalar>
Scalar {{ clexulator_name }}::eval_orbit_bfunc_{{ function_index }}() const {
  // orbit_index: {{ orbit_index }}
  // function_index: {{ function_index }}
  return {{ cpp }};
}
    {% endif %}
  {% endfor %}
{% endif %}

///  --- Prepare variables for point corr evaluation  ---

template<typename Scalar>
void {{ clexulator_name }}::_point_prepare(int nlist_ind) const {
{% if n_point_corr_sites > 0 %}
  switch(nlist_ind) {
  {% for site_bfuncs_variables_needed in site_bfuncs_variables_needed_at %}
    {% set neighbor_list_index = loop.index0 %}
  case {{ neighbor_list_index }}:
    {% for key, variables in site_bfuncs_variables_needed.items() %}
      {%- if key == "occ" %}{# /*DISCRETE DOF*/ #}
        {% set param_key = "m_occ_site_func_param_key" %}
      {% else %}
        {% set param_key = "m_" + key + "_var_param_key" %}
      {% endif %}
    if(m_params.eval_mode({{ param_key }}) != param_pack_type::READ) {
      {%- if key == "occ" %}{# /*DISCRETE DOF*/ #}
        {% raw %}
      // param_pack_type::Val<Scalar>::set(
      //     m_params, {{ param_key}}, {{ site_function_index }}, {{ neighbor_list_index }},
      //     eval_occ_func_{{ sublattice_index }}_{{ site_function_index }}({{ neighbor_list_index }}));
        {% endraw %}
      {% elif neighbor_list_index is not none %}{# /*LOCAL CONTINUOUS DOF*/ #}
        {% raw %}
      // param_pack_type::Val<Scalar>::set(m_params, {{ param_key}}, {{ component_index }}, {{ neighbor_list_index }}, eval_{{ key }}_var_{{ sublattice_index }}_{{ component_index }}({{ neighbor_list_index }}));
        {% endraw %}
      {% else %}{# /*GLOBAL CONTINUOUS DOF*/ #}
        {% raw %}
      // param_pack_type::Val<Scalar>::set(m_params, {{ param_key}}, {{ component_index }}, eval_{{ key }}_var({{ component_index }}));
        {% endraw %}
      {% endif %}
      {% for var_indices in variables %}
        {% set neighbor_list_index = var_indices[1] %}
        {% set sublattice_index = var_indices[2] %}
        {% if key == "occ" %}{# /*DISCRETE DOF*/ #}
          {% set site_function_index = var_indices[0] %}
      param_pack_type::Val<Scalar>::set(m_params, {{ param_key}}, {{ site_function_index }}, {{ neighbor_list_index }}, eval_occ_func_{{ sublattice_index }}_{{ site_function_index }}({{ neighbor_list_index }}));
        {% elif neighbor_list_index is not none %}{# /*LOCAL CONTINUOUS DOF*/ #}
          {% set component_index = var_indices[0] %}
      param_pack_type::Val<Scalar>::set(m_params, {{ param_key}}, {{ component_index }}, {{ neighbor_list_index }}, eval_{{ key }}_var_{{ sublattice_index }}_{{ component_index }}({{ neighbor_list_index }}));
        {% else %}{# /*GLOBAL CONTINUOUS DOF*/ #}
          {% set component_index = var_indices[0] %}
      param_pack_type::Val<Scalar>::set(m_params, {{ param_key}}, {{ component_index }}, eval_{{ key }}_var({{ component_index }}));
        {% endif %}
      {% endfor %}
    }
    {% endfor %}
    break;
  {% endfor %}
  } // switch
{% endif %}
}
{% if site_bfuncs|length > 0 %}
  {% set vars = {'first': True} %}
  {% for f_by_function_index in site_bfuncs %}
    {% set function_index = f_by_function_index.linear_function_index %}
    {% set orbit_index = f_by_function_index.linear_orbit_index %}
    {% for f_by_neighbor_index in f_by_function_index.at %}
      {% set neighbor_list_index = f_by_neighbor_index.neighbor_list_index %}
      {% set cpp = f_by_neighbor_index.cpp %}
      {% if cpp %}
        {% if vars.first %}

/// --- Point corr ---
          {% raw %}
// template<typename Scalar>
// Scalar {{ clexulator_name }}::eval_site_bfunc_{{ function_index }}_at_{{ neighbor_list_index }}() const {
//   // orbit_index: {{ orbit_index }}
//   // function_index: {{ function_index }}
//   return {{ factored_orbit_prefix }} * (
//     {{ factored_cluster_prefix_0 }}({{ factored_cluster_function_0 }})
//     + {{ factored_cluster_prefix_1 }}({{ factored_cluster_function_1 }})
//     ...
//     ) / {{ orbit_mult }};
// }
          {% endraw %}
          {% if vars.update({'first': False}) %} {% endif %}
        {% endif %}

template<typename Scalar>
Scalar {{ clexulator_name }}::eval_site_bfunc_{{ function_index }}_at_{{ neighbor_list_index }}() const {
  // orbit_index: {{ orbit_index }}
  // function_index: {{ function_index }}
  return {{ cpp }};
}
      {% endif %}
    {% endfor %}
  {% endfor %}
{% endif %}
{% if site_bfuncs|length > 0 %}
  {% set vars = {'first': True} %}
  {% for f_by_function_index in site_bfuncs %}
    {% set function_index = f_by_function_index.linear_function_index %}
    {% set orbit_index = f_by_function_index.linear_orbit_index %}
    {% for f_by_neighbor_index in f_by_function_index.at %}
      {% set neighbor_list_index = f_by_neighbor_index.neighbor_list_index %}
      {% set occ_delta_cpp = f_by_neighbor_index.occ_delta_cpp %}
      {% if occ_delta_cpp %}
        {% if vars.first %}

/// --- Delta point corr ---
          {% raw %}
// template<typename Scalar>
// Scalar {{ clexulator_name }}::eval_occ_delta_site_bfunc_{{ function_index }}_at_{{ neighbor_list_index }}(int occ_i, int occ_f) const {
//   // orbit_index: {{ orbit_index }}
//   // function_index: {{ function_index }}
//   return (m_occ_func{{ sublattice_index }}_{{ site_function_index }}[occ_f] - m_occ_func{{ sublattice_index }}_{{ site_function_index }}[occ_i]) * {{ factored_orbit_prefix }} * (
//     {{ factored_cluster_prefix_0 }}({{ factored_cluster_function_0 }})
//     + {{ factored_cluster_prefix_1 }}({{ factored_cluster_function_1 }})
//     ...
//     ) / {{ orbit_mult }};
// }
          {% endraw %}
          {% if vars.update({'first': False}) %} {% endif %}
        {% endif %}

template<typename Scalar>
Scalar {{ clexulator_name }}::eval_occ_delta_site_bfunc_{{ function_index }}_at_{{ neighbor_list_index }}(int occ_i, int occ_f) const {
  // orbit_index: {{ orbit_index }}
  // function_index: {{ function_index }}
  return {{ occ_delta_cpp }};
}
      {% endif %}
    {% endfor %}
  {% endfor %}
{% endif %}