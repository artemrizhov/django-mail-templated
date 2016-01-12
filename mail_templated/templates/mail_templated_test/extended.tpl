{% extends "mail_templated_test/base.tpl" %}

{% block subject %}
Hello {{ name }}
{% endblock %}

{% block body %}
{{ name }}, this is a base message.
{% endblock %}
