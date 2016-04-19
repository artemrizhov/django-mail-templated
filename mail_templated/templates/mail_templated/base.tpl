{{ TAG_START_SUBJECT }}{% autoescape off %}{% block subject %}{% endblock %}{% endautoescape %}{{ TAG_END_SUBJECT }}

{{ TAG_START_BODY }}{% autoescape off %}{% block body %}{% endblock %}{% endautoescape %}{{ TAG_END_BODY }}

{{ TAG_START_HTML }}{% block html %}{% endblock %}{{ TAG_END_HTML }}
