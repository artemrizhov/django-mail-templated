{% extends "mail_templated_test/overridden.tpl" %}

{% block subject_appendix %}. Appendix{% endblock %}

{% block body %}
{{ block.super }}Really.
{% endblock %}
