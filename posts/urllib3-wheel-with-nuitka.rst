#######
 Intro
#######

This post compares the pytest results of urllib3 to its nuitka-built
``.whl`` counterpart.

Urllib3 standalone test have already been covered. Manual testing is now
done to compare the pytest results of a nuitka wheel built using
``python setup.py bdist_nuitka`` to the regular pytest of the urllib3
package. Testing is done to ensure that nuitka is building the wheel
correctly. If the pytests pass/fail in the same way, that means Nuitka
built the wheel properly. Else if the tests differ, then something is
wrong. Virtualenv is used to create a clean environment with no outside
pollution.

At first, the urllib3 nuitka-wheel pytest was crashing because of the
unsafe assumption that imports will always exist (which is not the case
if exceptions are thrown). `Issue 413
<https://github.com/Nuitka/Nuitka/issues/413>`__ was filed to record and
fix this bug.

After the fixes, the pytests were ran again and the results were very
similar:

.. code::

   Regular pytests: ====== 3 failed, 836 passed, 456 skipped, 113 warnings in 47.54 seconds =======
   Nuitka wheel pytests: ====== 1 failed, 838 passed, 456 skipped, 113 warnings in 47.59 seconds =======

The extra passes are suspicious and require more investigation into why
they happen. To make that easy, we are going to fully automate the
process and compare outputs with verbose pytest modes.

####################
 Steps to Reproduce
####################

#. Clone urllib3 and nuitka into a new folder

#. Inside the urllib3 folder, issue ``python -m pip install -r
   dev-requirements.txt`` to install its requirements.

#. Issue ``python -m pytest --disable-warnings``, this runs the regular
   pytest for urllib3.

#. Change into the nuitka folder and issue ``python setup.py develop``.

#. Change back into urllib3 and issue ``python setup.py bdist_nuitka``
   to build the urllib3 wheel using nuitka. The newly built wheel should
   be found in the ``dist`` folder.

#. Use pip to uninstall the existing urllib3, then issue ``python -m pip
   install`` followed by the newly built ``.whl`` filename.

#. Issue ``python -m pytest --disable-warnings``, this runs the
   nuitka-built wheel pytest for urllib3.

##################
 Uncompile Python
##################

urllib3 regular pytest:

.. code::

   $ python -m pytest --disable-warnings
   ============================= test session starts =============================
   platform win32 -- Python 3.7.0, pytest-4.0.0, py-1.8.0, pluggy-0.11.0
   rootdir: C:\Users\Tommy\pipenv-testing\urllib3-testing\urllib3, inifile: setup.cfg
   plugins: timeout-1.3.1
   collected 1295 items

   test\test_collections.py ....................................s           [  2%]
   test\test_compatibility.py ...                                           [  3%]
   test\test_connection.py .....                                            [  3%]
   test\test_connectionpool.py ............................................ [  6%]
   ...........................                                              [  8%]
   test\test_exceptions.py .............                                    [  9%]
   test\test_fields.py ...............                                      [ 11%]
   test\test_filepost.py ...........                                        [ 11%]
   test\test_no_ssl.py ..                                                   [ 12%]
   test\test_poolmanager.py .........................                       [ 14%]
   test\test_proxymanager.py ...                                            [ 14%]
   test\test_queue_monkeypatch.py .                                         [ 14%]
   test\test_response.py ..................sss............................. [ 18%]
   ...........                                                              [ 19%]
   test\test_retry.py ..............................F.F.F..                 [ 21%]
   test\test_ssl.py ...............................                         [ 24%]
   test\test_util.py ...................................................... [ 28%]
   ........................................................................ [ 34%]
   ....................ss.s...s............................................ [ 39%]
   ............                                                             [ 40%]
   test\test_wait.py ...ssssss                                              [ 41%]
   test\contrib\test_pyopenssl.py sssssssssssssssssssssssssssssssssssssssss [ 44%]
   ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss [ 49%]
   ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss [ 55%]
   ssssssssssssssssssss                                                     [ 57%]
   test\contrib\test_pyopenssl_dependencies.py ss                           [ 57%]
   test\contrib\test_securetransport.py sssssssssssssssssssssssssssssssssss [ 59%]
   ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss [ 65%]
   ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss [ 71%]
   sssssssssssssssssss                                                      [ 72%]
   test\contrib\test_socks.py ..................                            [ 73%]
   test\with_dummyserver\test_chunked_transfer.py ........                  [ 74%]
   test\with_dummyserver\test_connectionpool.py ........................... [ 76%]
   .......................................                                  [ 79%]
   test\with_dummyserver\test_https.py .....................s....s......... [ 82%]
   .................................................Uncaught exception, closing connection.
   ........................................................................ [ 87%]
   ................................sssssssssssssssssssssssssssssssssss....  [ 93%]
   test\with_dummyserver\test_no_ssl.py ..                                  [ 93%]
   test\with_dummyserver\test_poolmanager.py ...............                [ 94%]
   test\with_dummyserver\test_proxy_poolmanager.py ................         [ 95%]
   test\with_dummyserver\test_socketlevel.py .............................. [ 98%]
   ......................                                                   [100%]
   ====== 3 failed, 836 passed, 456 skipped, 113 warnings in 47.54 seconds =======

######################
 Compiled with Nuitka
######################

nuitka wheel pytest:

.. code::

   $ python -m pytest --disable-warnings
   ============================= test session starts =============================
   platform win32 -- Python 3.7.0, pytest-4.0.0, py-1.8.0, pluggy-0.11.0
   rootdir: C:\Users\Tommy\pipenv-testing\urllib3-testing\urllib3, inifile: setup.cfg
   plugins: timeout-1.3.1
   collected 1295 items

   test\test_collections.py ....................................s           [  2%]
   test\test_compatibility.py ...                                           [  3%]
   test\test_connection.py .....                                            [  3%]
   test\test_connectionpool.py ............................................ [  6%]
   ...........................                                              [  8%]
   test\test_exceptions.py .............                                    [  9%]
   test\test_fields.py ...............                                      [ 11%]
   test\test_filepost.py ...........                                        [ 11%]
   test\test_no_ssl.py .F                                                   [ 12%]
   test\test_poolmanager.py .........................                       [ 14%]
   test\test_proxymanager.py ...                                            [ 14%]
   test\test_queue_monkeypatch.py .                                         [ 14%]
   test\test_response.py ..................sss............................. [ 18%]
   ...........                                                              [ 19%]
   test\test_retry.py .....................................                 [ 21%]
   test\test_ssl.py ...............................                         [ 24%]
   test\test_util.py ...................................................... [ 28%]
   ........................................................................ [ 34%]
   ....................ss.s...s............................................ [ 39%]
   ............                                                             [ 40%]
   test\test_wait.py ...ssssss                                              [ 41%]
   test\contrib\test_pyopenssl.py sssssssssssssssssssssssssssssssssssssssss [ 44%]
   ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss [ 49%]
   ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss [ 55%]
   ssssssssssssssssssss                                                     [ 57%]
   test\contrib\test_pyopenssl_dependencies.py ss                           [ 57%]
   test\contrib\test_securetransport.py sssssssssssssssssssssssssssssssssss [ 59%]
   ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss [ 65%]
   ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss [ 71%]
   sssssssssssssssssss                                                      [ 72%]
   test\contrib\test_socks.py ..................                            [ 73%]
   test\with_dummyserver\test_chunked_transfer.py ........                  [ 74%]
   test\with_dummyserver\test_connectionpool.py ........................... [ 76%]
   .......................................                                  [ 79%]
   test\with_dummyserver\test_https.py .....................s....s......... [ 82%]
   ........................................................................ [ 87%]
   ................................sssssssssssssssssssssssssssssssssss....  [ 93%]
   test\with_dummyserver\test_no_ssl.py ..                                  [ 93%]
   test\with_dummyserver\test_poolmanager.py ...............                [ 94%]
   test\with_dummyserver\test_proxy_poolmanager.py ................         [ 95%]
   test\with_dummyserver\test_socketlevel.py .............................. [ 98%]
   ......................                                                   [100%]
   ====== 1 failed, 838 passed, 456 skipped, 113 warnings in 47.59 seconds =======
