============
Diofant 0.13
============

Not Released Yet

New features
============

Major changes
=============

Compatibility breaks
====================

* Removed ``n()`` method from :class:`~diofant.core.evalf.EvalfMixin`, see :pull:`1114`.
* Former submodule ``diofant.polys.polyconfig`` now is :mod:`diofant.config`, see :pull:`1115`.
* Drop support for ``DIOFANT_DEBUG`` environment variable, see :pull:`1115`.
* Renamed ``Ring`` as :class:`~diofant.domains.ring.CommutativeRing`, see :pull:`1123`.
* Removed support for Python 3.7 and 3.8, see :pull:`1118` and :pull:`1124`.
* ``FiniteRing`` renamed to :class:`~diofant.domains.IntegerModRing`, see :pull:`1124`.

Minor changes
=============

Developer changes
=================

* Turn on type checking for the whole codebase, see :pull:`1114`.

Issues closed
=============

See the `release milestone <https://github.com/diofant/diofant/milestone/7?closed=1>`_
for complete list of issues and pull requests involved in this release.

These Sympy issues also were addressed:

* :sympyissue:`20861`: reduce_inequalities() gives impossible answer
* :sympyissue:`20874`: Port the PRS algorithm to the sparse polynomial implementation
* :sympyissue:`20902`: Incorrect inequality solving: False returned instead of answer
* :sympyissue:`20941`: Fails to Solve Definite Integral
* :sympyissue:`20973`: cancel raises PolynomialError for exp(1+O(x))
* :sympyissue:`20985`: TypeErrors appearing for simple plynomial manipulations (did not happen in v1.6.1)
