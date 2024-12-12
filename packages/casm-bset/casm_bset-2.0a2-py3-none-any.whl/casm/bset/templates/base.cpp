{% block global_include %}{% endblock %}
{% block global_comment %}{% endblock %}
{% block global_decl %}{% endblock %}

namespace CASM {
namespace clexulator {

{% block namespace_clexulator_decl %}{% endblock %}

class {{ clexulator_name }}
    : public clexulator::BaseClexulator {
 public:
{% block clexulator_public_decl %}{% endblock %}
 private:
{% block clexulator_private_decl %}{% endblock %}
};

{% block clexulator_public_def %}{% endblock %}
{% block clexulator_private_def %}{% endblock %}
}  // namespace clexulator
}  // namespace CASM

{% block global_def %}{% endblock %}