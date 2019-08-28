Hello everyone!

GSoC 2019 has almost come to an end! It's the time to wrap up this mega event
started back in May 2019. Under the mentorship of Mentor Hayen, my learning
experience has undergone a roller-coaster ride and it has not only boosted my
growth as a developer but also as an individual. Over the last 3 months the
followings are my major contributions to this project:


Built-ins Optimizations
=======================

* "any": `PR #246 <https://github.com/Nuitka/Nuitka/pull/246>`__
    * `nuitka.nodes.BuiltinAnyNodes` node added to optimize the "any" built-in.
    * Developed an algorithm to predict the "any" for arguments having repetitive values at compile time.
      For example:

         any([0]*255) -> False

         any([False, False, True]) -> True

    * Extended support for `range`, `set` and `dict` built-ins.
    * Added the optimized C side support too
    * Added a method `getMetaClassBase` to make Python 2 and Python 3 compatible while working with metaclasses.

* Issue reported and closed `Issue #349 <https://github.com/Nuitka/Nuitka/issues/349>`__
    * Created a new module `nuitka.nodes.IterationHandles` to work with iterables.
    * Added support of Iteration for non-mutable types.

* "all": `PR #407 <https://github.com/Nuitka/Nuitka/pull/407>`__
    * Added `nuitka.nodes.BuiltinAllNodes` to optimize the "all" built-ins.
    * Developed an algorithm similar to "any" to predict the "all" arguments.
      For example:

        all([0, 0, 1]) -> False

        all([True]*100) -> True

    * Other similar optimizations are done like "any" built-in.
    * Additionally, added a new testing module `tests.optimizations.CommonOptimizations` to test the built-ins optimizations at the same place.

* "abs": `PR #419 <https://github.com/Nuitka/Nuitka/pull/419>`__
   * Added new operation node `ExpressionOperationAbs` to optimize the `abs` built-in.
   * Manually added `shapeSlotAbs` to different shapes.
   * Finally pre-computed the compile time constant `abs`

* "max" and "min": `PR #442 <https://github.com/Nuitka/Nuitka/pull/442>`__
   * This PR is work in progress and is half complete.
   * This is the first optimizations in which I used reformulations instead of added in a new node.
   * Pseudo-code of "min" reformulation:

     .. code-block:: python

       def _min(a, b, c, ...):
        tmp_arg1 = a
        tmp_arg2 = b
        tmp_arg3 = c
        ...
        result = tmp_arg1
        if keyfunc is None: # can be decided during re-formulation
            tmp_key_result = keyfunc(result)
            tmp_key_candidate = keyfunc(tmp_arg2)
            if tmp_key_candidate < tmp_key_result:
                result = tmp_arg2
                tmp_key_result = tmp_key_candidate
            tmp_key_candidate = keyfunc(tmp_arg3)
            if tmp_key_candidate < tmp_key_result:
                result = tmp_arg3
                tmp_key_result = tmp_key_candidate
            ...
        else:
            if tmp_arg2 < result:
                result = tmp_arg2
            if tmp_arg3 < result:
                result = tmp_arg3
            ...
         return result

   * Adding support for `keyfunc` is pending

* "zip": `PR #462 <https://github.com/Nuitka/Nuitka/pull/462>`__
   * This built-in uses both types of optimizations that the previous built-ins optimizations used.
   * `zip` for Python 2 uses the reformulations.
   * Pseudo-code of "zip" reformulation:

   .. code-block:: python

       def _zip(a, b, c, ... ):
       # First assign, to preserve order of execution,
       # the arguments might be complex expressions.
       tmp_arg1 = a
       tmp_arg2 = b
       tmp_arg3 = c
       ...
       tmp_iter_1 = iter(tmp_arg1)
       tmp_iter_2 = iter(tmp_arg2)
       tmp_iter_3 = iter(tmp_arg3)
       ...
       # could be more
       tmp_result = []
       try:
           while 1:
               tmp_result.append(
                   (
                        next(tmp_iter_1),
                        next(tmp_iter_2),
                        next(tmp_iter_3),
                        ...
                   )
                )
          except StopIteration:
              pass
        return tmp_result

   * `zip` for Python 3 needs a new node that calls the `zip` because unlike `zip` in Python 2, `zip` in Python 3 returns a    `zipobject`.

Test suite
==========

* Search mode "All": `PR #378 <https://github.com/Nuitka/Nuitka/pull/378>`__
   * In the test suite, I added a new search mode "all" that will test all the modules and return all the results at once. For example:

   .. code-block:: sh

      $ ./tests/basics/run_all.py all
         Using concrete python 2.7.12 on x86_64
         Comparing output of 'Asserts.py' using '/usr/bin/python' with flags silent, expect_success, remove_output,     recurse_all, original_file, cpython_cache, plugin_enable:pylint-warnings ...
         .
         .
         .
         .
         Total 0 error(s) found.



* Search mode "Only": `PR #333 <https://github.com/Nuitka/Nuitka/pull/333>`__
   * Added "only" search mode to test only a single module. For example:

   .. code-block:: sh

      $ ./tests/basics/run_all.py only BuiltinsTest.py
         Using concrete python 2.7.12 on x86_64
         Skipping Asserts.py
         Skipping Assignments.py
         Skipping BigConstants.py
         Skipping Branching.py
         Skipping BuiltinOverload.py
         Skipping BuiltinSuper.py
         Comparing output of 'BuiltinsTest.py' using '/usr/bin/python' with flags silent, expect_success, remove_output, recurse_all, original_file, cpython_cache, plugin_enable:pylint-warnings ...


* Reported and closed Issue #334: `PR #336 <https://github.com/Nuitka/Nuitka/pull/336>`__
   * Fixed the autoformat bug by reading and writing the files in bytes instead of string.

Documentation
=============
* Nuitka git work flow: `PR #485 <https://github.com/Nuitka/Nuitka/pull/485>`__

And other minor doc fixes are added with their respective pull requests.

What I learned
==============
* Learned the software engineering principles and how to keep my work clean.
* I also learned how to effectively use software designing principles like `DRY <https://en.wikipedia.org/wiki/Don%27t_repeat_yourself>`__ and `KISS <https://en.wikipedia.org/wiki/KISS_principle>`__.
* Got exposed to Nuitka internals which helped me to better understand how compilers in general work.
* Explored how CPython works internally.
* Got some great advice from Mentor Hayen about starting my professional career in Software engineering.

Overall, it was a great experience to be a part of Nuitka :)

| Yours,
| `Batakrishna <https://bksahu.github.io>`__
