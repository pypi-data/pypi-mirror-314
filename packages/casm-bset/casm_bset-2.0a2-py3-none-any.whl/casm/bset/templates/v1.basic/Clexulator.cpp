{% extends "base.cpp" %}



{% block global_include %}
#include <cstddef>
#include "casm/clexulator/BaseClexulator.hh"
#include "casm/clexulator/BasicClexParamPack.hh"
#include "casm/global/eigen.hh"
{% endblock %}



{% block namespace_clexulator_decl %}
typedef ClexParamPack base_param_pack_type;
typedef BasicClexParamPack param_pack_type;
{% endblock %}

{% block clexulator_public_decl %}
  {{ clexulator_name }}();

  ~{{ clexulator_name }}();

  base_param_pack_type const &param_pack() const override { return m_params; }

  base_param_pack_type &param_pack() override { return m_params; }

{% endblock %}



{% block clexulator_private_decl %}
{% include "v1.basic/clexulator_private_decl.cpp" %}
{% endblock %}



{% block clexulator_public_def %}
{% include "v1.basic/clexulator_constructor_def.cpp" %}

{{ clexulator_name }}::~{{ clexulator_name }}() {
  //nothing here
}

{% endblock %}


{% block clexulator_private_def %}
{% include "v1.basic/clexulator_private_def.cpp" %}
{% endblock %}

{% block global_def %}
extern "C" {

/// \brief Returns a clexulator::BaseClexulator* owning a {{ clexulator_name }}
CASM::clexulator::BaseClexulator *make_{{ clexulator_name }}() {
  return new CASM::clexulator::{{ clexulator_name }}();
}

}
{% endblock %}