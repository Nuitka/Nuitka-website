#######
 Intro
#######

This post compares the pytest results of dateutil to its nuitka-built
``.whl`` counterpart.

Dateutil standalone test have already been covered. Manual testing is
now done to compare the pytest results of a nuitka wheel built using
``python setup.py bdist_nuitka`` to the regular pytest of the dateutil
package. Testing is done to ensure that nuitka is building the wheel
correctly. If the pytests pass/fail in the same way, that means Nuitka
built the wheel properly. Else if the tests differ, then something is
wrong. Virtualenv is used to create a clean environment with no outside
pollution.

The pytest results were very similar:

.. code::

   Regular pytests: ============= 1977 passed, 76 skipped, 21 xfailed in 7.99 seconds =============
   Nuitka wheel pytests: ============= 1976 passed, 76 skipped, 21 xfailed in 7.89 seconds =============

####################
 Steps to Reproduce
####################

#. Clone dateutil and nuitka into a new folder

#. Inside the dateutil folder, issue ``python -m pip install -r
   requirements-dev.txt`` to install its requirements.

#. Issue ``python -m pytest --disable-warnings``, this runs the regular
   pytest for dateutil.

#. Change into the nuitka folder and issue ``python setup.py develop``.

#. Change back into dateutil and issue ``python setup.py bdist_nuitka``
   to build the dateutil wheel using nuitka. The newly built wheel
   should be found in the ``dist`` folder.

#. Use pip to uninstall the existing dateutil, then issue ``python -m
   pip install`` followed by the newly built ``.whl`` filename.

#. Issue ``python -m pytest --disable-warnings``, this runs the
   nuitka-built wheel pytest for dateutil.

##################
 Uncompile Python
##################

dateutil regular pytest:

.. code::

   ============================= test session starts =============================
   platform win32 -- Python 3.7.0, pytest-4.6.3, py-1.8.0, pluggy-0.12.0
   rootdir: C:\Users\Tommy\pipenv-testing\dateutil-testing\dateutil, inifile: setup.cfg
   plugins: hypothesis-4.24.3, cov-2.7.1
   collected 2074 items

   dateutil\test\test_easter.py ........................................... [  2%]
   ........................................................................ [  5%]
   ................................................                         [  7%]
   dateutil\test\test_import_star.py .                                      [  7%]
   dateutil\test\test_imports.py .......................                    [  9%]
   dateutil\test\test_internals.py ....                                     [  9%]
   dateutil\test\test_isoparser.py ........................................ [ 11%]
   ........................................................................ [ 14%]
   ........................................................................ [ 18%]
   ........................................................................ [ 21%]
   ........................................................................ [ 25%]
   .......x...x............................................................ [ 28%]
   ........................................................................ [ 31%]
   ........................................................................ [ 35%]
   .....................xx                                                  [ 36%]
   dateutil\test\test_parser.py ........................................... [ 38%]
   ........................................................................ [ 42%]
   ........................................................................ [ 45%]
   .................................xxxxxxxxxxxxxsss......                  [ 48%]
   dateutil\test\test_relativedelta.py .................................... [ 49%]
   .............................................                            [ 52%]
   dateutil\test\test_rrule.py ............................................ [ 54%]
   ........................................................................ [ 57%]
   ........................................................................ [ 61%]
   ........................................................................ [ 64%]
   ........................................................................ [ 68%]
   ........................................................................ [ 71%]
   ........................................................................ [ 75%]
   ................................................................x....... [ 78%]
   ..............                                                           [ 79%]
   dateutil\test\test_tz.py ............................s...........sssssss [ 81%]
   sssssssssssssssssssssssssssssssssssssssss..s............................ [ 84%]
   xxx..s......................................s........................... [ 88%]
   s....................................................................... [ 91%]
   ..........s....................................s.s....................ss [ 95%]
   sssssssssssss....s..........s........................................... [ 98%]
   .............                                                            [ 99%]
   dateutil\test\test_utils.py .......                                      [ 99%]
   dateutil\test\property\test_isoparse_prop.py .                           [ 99%]
   dateutil\test\property\test_parser_prop.py ..                            [ 99%]
   docs\exercises\solutions\mlk_day_rrule_solution.py .                     [100%]

   ============= 1977 passed, 76 skipped, 21 xfailed in 7.99 seconds =============

######################
 Compiled with Nuitka
######################

nuitka wheel pytest:

.. code::

   ============================= test session starts =============================
   platform win32 -- Python 3.7.0, pytest-4.6.3, py-1.8.0, pluggy-0.12.0
   rootdir: C:\Users\Tommy\pipenv-testing\dateutil-testing\dateutil, inifile: setup.cfg
   plugins: hypothesis-4.24.3, cov-2.7.1
   collected 2073 items

   test\test_easter.py .................................................... [  2%]
   ........................................................................ [  5%]
   .......................................                                  [  7%]
   test\test_import_star.py .                                               [  7%]
   test\test_imports.py .......................                             [  9%]
   test\test_internals.py ....                                              [  9%]
   test\test_isoparser.py ................................................. [ 11%]
   ........................................................................ [ 15%]
   ........................................................................ [ 18%]
   ........................................................................ [ 21%]
   ......................................................................x. [ 25%]
   ..x..................................................................... [ 28%]
   ........................................................................ [ 32%]
   ........................................................................ [ 35%]
   ............xx                                                           [ 36%]
   test\test_parser.py .................................................... [ 39%]
   ........................................................................ [ 42%]
   ........................................................................ [ 46%]
   ........................xxxxxxxxxxxxxsss......                           [ 48%]
   test\test_relativedelta.py ............................................. [ 50%]
   ....................................                                     [ 52%]
   test\test_rrule.py ..................................................... [ 54%]
   ........................................................................ [ 58%]
   ........................................................................ [ 61%]
   ........................................................................ [ 65%]
   ........................................................................ [ 68%]
   ........................................................................ [ 72%]
   ........................................................................ [ 75%]
   .......................................................x................ [ 79%]
   .....                                                                    [ 79%]
   test\test_tz.py ............................s...........ssssssssssssssss [ 81%]
   ssssssssssssssssssssssssssssssss..s............................xxx..s... [ 85%]
   ...................................s...........................s........ [ 88%]
   ........................................................................ [ 92%]
   .s....................................s.s....................sssssssssss [ 95%]
   ssss....s..........s.................................................... [ 99%]
   ....                                                                     [ 99%]
   test\test_utils.py .......                                               [ 99%]
   test\property\test_isoparse_prop.py .                                    [ 99%]
   test\property\test_parser_prop.py ..                                     [100%]

   ============= 1976 passed, 76 skipped, 21 xfailed in 7.89 seconds =============
