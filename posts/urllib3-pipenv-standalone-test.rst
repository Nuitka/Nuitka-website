This post compares the pytests of urllib3 to its nuitka-built .whl counterpart
The results were very similar:
	Regular pytests: ====== 3 failed, 836 passed, 456 skipped, 113 warnings in 47.54 seconds =======
	Nuitka wheel pytests: ====== 1 failed, 838 passed, 456 skipped, 113 warnings in 47.59 seconds =======


urllib3 normal pytests:
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





urllib3 nuitka wheel pytests:
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