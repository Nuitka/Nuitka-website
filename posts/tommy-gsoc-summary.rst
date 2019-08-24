Intro
=====

As Google Summer of Code (GSoC) is coming to an end, I am writing this blog post as a final summary describing all the work I have 
done as well as my experiences in this program.



Summary of My Work
==================

- `#314 run_all.py new special-comment mechanism & Urllib3Using.py <https://github.com/Nuitka/Nuitka/pull/314>`__

  * Before GSoC started, I looked around for whatever work I could help with.

  * In this pull request, I added a ``checkRequirements`` function for the Nuitka standalone test suite.

  * This function checks for special-comments at the top of standalone tests in the format of
    ``# nuitka-skip-unless-expression: expression to be evaluated`` OR ``# nuitka-skip-unless-imports: module1,module2,...``
    and will decide whether to skip a test depending on if its specified requirements are met.

  * In addition, standalone test ``Urllib3Using.py`` was created.

  * This pull request was soon merged and allowed me the lucky opportunity of GSoC 2019 with Nuitka :)


- `#339 Standalone tests for botocore & boto3 + fix to Urllib3Using.py <https://github.com/Nuitka/Nuitka/pull/339>`__

  * This PR was also created before the start of GSoC.

  * Standalone test ``Boto3Using.py`` was created using ``moto`` to mock AWS calls which did not turn out well.

  * Changed ``Urllib3Using.py`` with the addition of python version checks as a fix to
    `Issue #373 <https://github.com/Nuitka/Nuitka/issues/373>`__.


- `Urllib3 Wheel with Nuitka Pytest Results <https://nuitka.net/posts/urllib3-wheel-with-nuitka.html>`__
  and `Python-Dateutil Wheel with Nuitka Pytest Results <https://nuitka.net/posts/dateutil-wheel-with-nuitka.html>`__

  * At the start of GSoC, I performed manual pytest comparison for PyPI packages ``urllib3`` and ``dateutil``.

  * The findings of my testing were documented in these postings.

  * Manual testing compares the pytest results of an installed nuitka wheel built using 
    ``python setup.py bdist_nuitka`` to the regular pytest results of each package. 
  
  * Testing is done to ensure that nuitka is building the wheel correctly. 
  
  * If the pytests pass/fail in the same way, that means Nuitka built the wheel properly. 
  
  * Else if the tests differ, then something is wrong. 
  
  * Virtualenv is used to create a clean environment with no outside pollution.

  * Over the course of performing manual testing, I became familiar with the use of ``virtualenv``, ``wheel``, and ``pytest``.

  * A bug was found with the package ``urllib3`` bdist and I created 
    `Issue #413 <https://github.com/Nuitka/Nuitka/issues/413>`__ to document the bug.


- `#440 Automating PyPI Wheel Pytest <https://github.com/Nuitka/Nuitka/pull/440>`__ 

  * After familiarizing myself with how ``virtualenv``, ``wheel``, and ``pytest`` work, I started to work on a script which
    would automate the pytest comparison for top PyPI packages.

  * The script first uses ``git`` to update each package if it is already existing in the local cache, else it will ``git clone``
    that package into the local cache.
  
  * The script then uses calls to ``os.system`` to automate the creation of a ``virtualenv`` which is then used to install ``pytest``
    and ``pip install`` the package's requirements (if any) for running pytest.

  * The script then handles each package depending on different needs before building a regular wheel with ``python setup.py bdist_wheel``.

  * This wheel is then installed into the ``virtualenv``, after which ``subprocess.Popen`` is used to run and capture the output
    of ``python -m pytest --disable-warnings`` into a string.

  * The script then resets the package to its original state and builds a nuitka-compiled wheel using ``python setup.py bdist_nuitka``.

  * This compiled wheel is then installed into the ``virtualenv``, after which ``subprocess.Popen`` is used to run and capture the output
    of ``python -m pytest --disable-warnings`` into another string.

  * The two strings containing pytest outputs are then compared to find differences.

  * If no differences are found, this means ``bdist_nuitka`` worked properly. Else Nuitka compilation did something wrong.

  * The above process is repeated for each suitable PyPI package from the PyPI top 50. (Some packages are left out if they do not
    contain a test suite or if they do not need to be tested)

  * At the end, a colored summary is given for all the packages tested.

  * This automation script is meant to be run regularly to inform developers of Nuitka regressions.


- `Issue #477 Unable to compile modules listed under unworthy_namespaces <https://github.com/Nuitka/Nuitka/issues/477>`__
  
  * Raised due to package ``pycparser`` failing in the automated test suite.

  * This issue will be addressed in the future.


- `Issue #479 bdist_nuitka fails for packages containing py_modules only <https://github.com/Nuitka/Nuitka/issues/479>`__

  * While I worked on `#440 <https://github.com/Nuitka/Nuitka/pull/440>`__, I found a bug with ``bdist_nuitka`` failing
    on PyPI packages containing py_modules only.
  
  * This bug occurs due to Nuitka making the assumption that a main package always exists for all packages. However,
    some packages contain only a main module and not a main package.

  * Applies to PyPI packages ``decorator``, ``ipaddress``, and ``pyparsing``.


- `#483 Add support for py_modules_only compilation <https://github.com/Nuitka/Nuitka/pull/483>`__ 

  * This pull request changes ``bdist_nuitka.py`` and various other files to fix 
    `Issue #479 <https://github.com/Nuitka/Nuitka/issues/479>`__.

  * Checks are added for the ``bdist_nuitka`` command to see if a main package exists. If there is not a main package,
    it will set its compile target to the main module instead.

  * This also addressed the case of a package with both a main package and a main module, in which case both are included
    inside the resulting wheel.

  * In addition, ``distutils`` examples ``py_modules_only`` and ``package_and_module`` were created and added for future testing.

  * During this PR, I found an import bug in Nuitka and hotfixed it with 
    `#487 Fixup_import_module <https://github.com/Nuitka/Nuitka/pull/487>`__.


- `#484 PyPI Standalone Tests <https://github.com/Nuitka/Nuitka/pull/484>`__

  * This pull request adds more standalone tests for each top PyPI package.


- `#495 Improve pypi automation <https://github.com/Nuitka/Nuitka/pull/495>`__

  * Improves the PyPI test suite created in `#440 <https://github.com/Nuitka/Nuitka/pull/440>`__ with functional improvements,
    readability improvements, and added documentation.



Things I learned
================

Before GSoC, I was very uncomfortable with working inside a terminal. I was unfamiliar with many basic bash commands because I
simply did not have any prior professional industrial experiences. I was also very unfamiliar with the Git flow, which is 
evident in the messy commit histories of my earliest pull requests.

As I continued throughout my GSoC journey, however, I became much more comfortable with working inside the terminal as well 
as using ``git`` as a version-control system (shoutout to my mentor Kay Hayen for helping me through all the annoying conflicts).

Although I am still no expert, I can confidently say that I am now far more proficient working with ``git`` and inside the terminal.

In addition, I became much more familiar with many of the most popular PyPI packages as well as the inner workings of ``python``, 
which I believe will help me go very far in my career as a software developer.

Overall, the GSoC experience was truly astounding and I am more than thankful to my mentor Kay Hayen as well as Google for making
this amazing program possible.


Yours, 
`Tommy <https://github.com/tommyli3318>`__