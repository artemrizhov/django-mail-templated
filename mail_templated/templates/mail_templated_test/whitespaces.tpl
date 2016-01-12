{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello {{ name }}
{% endblock %}

{% block body %}
  {{ name }}, this is a message with preceding and trailing whitespaces.{{ '  ' }}
{% endblock %}
