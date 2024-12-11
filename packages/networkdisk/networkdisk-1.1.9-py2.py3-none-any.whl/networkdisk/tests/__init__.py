from .divergence import run

"""
The function run collect testsClass from networkx sources
following (more or less) pytest idioms.
NetworkX tests not package through class will thue not be performed.

Some of the tests are simply not doable with networkdisk implementation.
Investigated test are marked explicitly with adequate explanation in the
file `test_info.json`.

Some tests and functions are simply blacklisted since they are simply
not relevant.
"""
