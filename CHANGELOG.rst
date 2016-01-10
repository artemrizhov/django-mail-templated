===============================
Django-Mail-Templated Changelog
===============================

2.0.0
=====
* Slightly changed the list of arguments for `EmailMessage.__init__()`.
* Replaced `template` and `template_name` property setters with method
 `load_template()`.
* Added method `render()`.
* Added support for late initialisation.
* Improved tests.
* Added comments.

1.0.0
=====
* Fixed the multilingual templates support for Django >= 1.8.

