.. _spkg_sagemath_ecl:

=====================================================================
sagemath_ecl: Embeddable Common Lisp
=====================================================================

About SageMath
--------------

   "Creating a Viable Open Source Alternative to
    Magma, Maple, Mathematica, and MATLAB"

   Copyright (C) 2005-2024 The Sage Development Team

   https://www.sagemath.org

SageMath fully supports all major Linux distributions, recent versions of
macOS, and Windows (Windows Subsystem for Linux).

See https://doc.sagemath.org/html/en/installation/index.html
for general installation instructions.


About this pip-installable distribution package
-----------------------------------------------

This pip-installable distribution ``passagemath-ecl`` is a distribution of a part of the Sage Library.
It ships the Cython interface to Embeddable Common Lisp.


What is included
----------------

* Binary wheels on PyPI contain a prebuilt copy of
  `Embeddable Common Lisp <https://doc.sagemath.org/html/en/reference/spkg/ecl.html>`_

Type
----

standard


Dependencies
------------

- $(PYTHON)
- $(PYTHON_TOOLCHAIN)
- :ref:`spkg_cysignals`
- :ref:`spkg_cython`
- :ref:`spkg_ecl`
- :ref:`spkg_gmpy2`
- :ref:`spkg_maxima`
- :ref:`spkg_pkgconfig`
- :ref:`spkg_python_build`
- :ref:`spkg_sage_setup`
- :ref:`spkg_sagemath_categories`
- :ref:`spkg_sagemath_environment`

Version Information
-------------------

package-version.txt::

    10.5.5

version_requirements.txt::

    passagemath-ecl ~= 10.5.5.0


Equivalent System Packages
--------------------------

(none known)

