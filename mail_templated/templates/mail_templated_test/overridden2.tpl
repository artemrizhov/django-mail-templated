{% extends "mail_templated_test/overridden.tpl" %}

{% block body %}
{{ block.super }}Really.
{% endblock %}
