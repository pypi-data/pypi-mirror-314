=======
CHANGES
=======

5.1 (2024-12-09)
----------------

- Add support for Python 3.12, 3.13.

- Drop support for Python 3.7.


5.0 (2023-02-07)
----------------

- Drop support for Python 2.7, 3.4, 3.5, 3.6.

- Add support for Python 3.7, 3.8, 3.9, 3.10, 3.11.

- Drop support for ``zope.app.skins`` which is deprecated since 2006.


4.0.1 (2017-05-25)
------------------

- Remove long-deprecated <browser:layer> configuration which was hidden
  behind a ``have deprecatedlayers`` condition. That directive simply
  doesn't exist any longer and defining that feature would cause an
  "Unknown directive" ConfigurationError.


4.0.0 (2017-04-27)
------------------

- Remove test dependency on ``zope.app.zcmlfiles``,
  ``zope.app.testing`` and several others.
- The ``zope.app.form`` dependency has been replaced with
  ``zope.formlib``.
- Add support for PyPy, Python 3.4, 3.5 and 3.6.


3.5.3 (2012-01-23)
------------------

- Replaced an undeclared test dependency on ``zope.app.authentication`` with
  ``zope.password``.

- Replaced an undeclared test dependency on ``zope.app.folder`` with
  ``zope.site``.


3.5.2 (2010-09-14)
------------------

- Removed not needed test dependency on ``zope.app.zptpage``.

- Replaced test dependency on ``zope.app.securitypolicy`` by
  ``zope.securitypolicy``.

- Using Python's ``doctest`` instead of deprecated ``zope.testing.doctest``.


3.5.1 (2010-01-08)
------------------

- Fix tests using a newer zope.publisher that requires zope.login.

3.5.0 (2009-02-01)
------------------

- Use zope.container instead of zope.app.container.

3.4.1 (2007-10-31)
------------------

- Resolve ``ZopeSecurityPolicy`` deprecation warning.


3.4.0 (2007-10-27)
------------------

- Initial release independent of the main Zope tree.
