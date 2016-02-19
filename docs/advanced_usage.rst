Advanced usage
==============

.. _inheritance:

Base template and inheritance
-----------------------------

The email template is rendered as a solid document, and all email message parts
(subject, body and html) appears concatenated after rendering.
The base template ``mail_templated/base.tpl`` contains special markers for the
email message parts, so that they can be found and extracted after rendering.
It looks likes this:

**mail_templated/base.tpl**

.. code-block:: html+django

  {{ '{#start_subject#}' }}{% block subject %}{% endblock %}{{ '{#end_subject#}' }}

  {{ '{#start_body#}' }}{% block body %}{% endblock %}{{ '{#end_body#}' }}

  {{ '{#start_html#}' }}{% block html %}{% endblock %}{{ '{#end_html#}' }}

This approach eliminates the dependency on the inner implementation of the
Django template engine which tends to change.
This is the only way to provide robust and full support for template
inheritance. Django template engine takes a lot of changes from time to time,
so it would be a bad idea to extract and render the blocks separately.
But anyway you should not worry about that markup in normal situation. Just
extend the base template and use the template blocks as usually.

You can define your own base template. In this case your base template should
extend the base template of *mail_templated* to be sure any future changes will
not affect your code.



