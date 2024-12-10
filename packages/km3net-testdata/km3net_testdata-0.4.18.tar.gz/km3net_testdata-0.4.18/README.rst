KM3NeT TestData
===============

.. image:: https://git.km3net.de/km3py/km3net-testdata/badges/master/pipeline.svg
    :target: https://git.km3net.de/km3py/km3net-testdata/pipelines

.. image:: https://git.km3net.de/km3py/km3net-testdata/badges/master/coverage.svg
    :target: https://km3py.pages.km3net.de/km3net-testdata/coverage

.. image:: https://git.km3net.de/examples/km3badges/-/raw/master/docs-latest-brightgreen.svg
    :target: https://km3py.pages.km3net.de/km3net-testdata


A hybrid Python/Julia package to get access to KM3NeT sample files for testing and development
purposes.

Installation and usage
----------------------

Python
``````

    pip install km3net-testdata

The file paths can be access in Python scripts using the ``data_path()`` function:

.. code-block:: python

    from km3net_testdata import data_path

    filename = data_path("offline/km3net_offline.root")

Notice the underscore in the Python package name (PyPI forces ``-`` but Python
package names are not allowed to use ``-``).

Julia
`````

Make sure the "KM3NeT Julia Registry" is added to your local Julia registries,
see https://git.km3net.de/common/julia-registry for more information.
The Julia package is called ``KM3NeTTestData`` and can be installed the usual way:

.. code-block:: julia

    julia> import Pkg; Pkg.add("KM3NeTTestData")

The package exports the ``datapath()`` function which can be used similar to the Python implementation:

.. code-block:: julia

    julia> using KM3NeTTestData

    julia> filename = datapath("offline", "km3net_offline.root")
    "/Users/tamasgal/.julia/packages/KM3NeTTestData/zb9oT/src/../km3net_testdata/data/offline/km3net_offline.root"

Shell
`````

To use the Python module in e.g. shell scripts, it can be called directly to
print the filepath:

.. code-block:: shell

   $ python -m km3net_testdata offline/km3net_offline.root
   /full/path/to/offline/km3net_offline.root

It can be combined with other shell tools, as usual:

.. code-block:: shell

  $ head -n 5 $(python -m km3net_testdata detx/detx_v3.detx)
  # a comment line
  # another comment line starting with '#'
  23 v3
  1500000000.1 9999999999.0
  UTM WGS84 32N 256500.0 4743000.0 -2425.0

Acknowledgements
----------------

The project idea and implementation were inspired by the Scikit-HEP Project https://github.com/scikit-hep/scikit-hep-testdata
