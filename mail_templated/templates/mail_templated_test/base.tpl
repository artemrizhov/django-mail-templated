{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello {{ name }}
{% endblock %}

{% block body %}
{{ name }}, this is a plain text message.
{% endblock %}
