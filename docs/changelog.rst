Changelog
=========

2.6.x
-----

- Fixed a bug with default body and html message.

- Added `context` parameter to the `render()` method.

- Made the `template_name` parameter not required for the `load_template()`
  method.

- Removed *args from the `send_mail()` function.

2.5.x
-----

- Added application settings.

- Added ability to cleanup the message object (enabled in ``send_mail()`` by
  default).

2.4.x
-----

- Fixed setup.py, added missing files to the package.

- Added more tests.

2.3.x
-----

- Made ``template_name`` argument required when ``render=True`` passed
  to ``__init__()``.
  
- Removed argument ``render`` of method ``send()``.

- Added public property ``is_rendered``.

- Added more tests.

2.2.x
-----

- Fixed compatibility with Python 3

2.1.x
-----

- Added full support of template inheritance.

- Added obligatory base email template.

- Fixed broken pickling/unpickling feature.

- ``render=True`` is now ignored on initialisation without template. Raised
  error before.

2.0.x
-----

*This is intermediate version with broken pickling/unpickling feature.*
Using of next or previous version is highly recommended.

- Slightly changed the list of arguments for ``EmailMessage.__init__()``.
  
- Replaced template and template\_name property setters with method
  ``load_template()``.
  
- Added method ``render()``.

- Added support for late initialisation.

- Improved tests.

1.0.x
-----

- Fixed the multilingual templates support for Django >= 1.8.
