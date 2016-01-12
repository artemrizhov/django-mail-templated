{% extends "mail_templated/base.tpl" %}
{% load i18n %}

{% block subject %}
Hello {{ name }}
{% endblock %}

{% block body %}
{% blocktrans with user_name=name %}
{{ user_name }}, this is a plain text message.
{% endblocktrans %}
{% endblock %}
