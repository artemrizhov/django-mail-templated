{{ START_SUBJECT_PART }}{% block subject %}
Hello {{ name }}
{% endblock %}{{ END_SUBJECT_PART }}

{{ START_BODY_PART }}{% block body %}
{{ name }}, this is a plain text message.
{% endblock %}{{ END_BODY_PART }}

{{ START_HTML_PART }}{% block html %}{% endblock %}{{ END_HTML_PART }}
