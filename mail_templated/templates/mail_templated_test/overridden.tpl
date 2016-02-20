{% extends "mail_templated_test/base.tpl" %}

{% block subject %}
Overridden hello {{ name }}{% block subject_appendix %}{% endblock %}
{% endblock %}

{% block body %}
{{ name }}, this is overridden message.
{% endblock %}
