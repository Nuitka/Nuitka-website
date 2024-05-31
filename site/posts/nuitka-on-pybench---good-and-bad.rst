.. post:: 2011/04/16 11:52
   :tags: benchmark, compiler, Nuitka, Python
   :author: Kay Hayen

#############################
 Looking where Nuitka stands
#############################

In case you wonder, [what Nuitka is](/pages/overview.html), look here.
Over the 0.3.x release cycle, I have mostly looked at its performance
with "pystone". I merely wanted to have a target to look at and `enjoy
the progress </pages/performance.html>`_ we have made there.

In the context of the Windows port then, Khalid Abu Bakr used the
pybench on Windows and that got me interested. It's a nice collection of
micro benchmarks, which is quite obviously aimed for looking CPython
implementations only. In that it's quite good to check where Nuitka is
good at, and where it can still take improvements for the milestone 2
stuff.

*************************
 Enhancements to PyBench
*************************

-  The pybench refused to accept that Nuitka could use so little time on
   some tests, I needed to hack it to allow it.

-  Then it had "ZeroDivisionError" exceptions, because Nuitka can run
   fully predictable code not at all, thus with a time of 0ms, which
   gives interesting factors.

-  Also these are many results, we are going to care for regressions
   only, so there is an option now to output only tests with negative
   values.

***********************
 The Interesting Parts
***********************

-  Nuitka currently has some fields where optimizations are already so
   effective as to render the whole benchmark pointless. Longterm, most
   of PyBench will not be looked at anymore, where the factor becomes
   "infinity", there is little point in looking at it. We will likely
   just use it as a test that optimizations didn't suddenly regress.
   Publishing the numbers will not be as interesting.

-  Then there are slow downs. These I take seriously, because of course
   I expect that Nuitka shall only be faster than CPython. Sometimes the
   implementation of Nuitka for some rarely used features is sub par
   though. I color coded these in red in the table below.

-  ComplexPythonFunctionCalls: These are twice as slow, which is an
   tribute to the fact, that the code in this domain is only as good as
   it needs to be. Of course function calls are very important, and this
   needs to be addressed.

-  TryRaiseExcept: This is much slower because of the cost of the raise
   statement, which is extremely high currently. For every raise, a
   frame object with a specific code object is created, so the traceback
   will point to the correct location. This is very inefficient, and
   wasteful. We need to be able to create code objects that can be used
   for all lines needed, and then we can re-use it and only have one
   frame object per function, which then can be re-used itself. There is
   already some work for that in [current git](/doc/download.html)
   (0.3.9 pre 2), but it's not yet complete at all.

-  WithRaiseExcept: Same problem as TryRaiseExcept, the exception
   raising is too expensive.

-  Note also that -90% is in fact much worse that +90%, the "diff"
   numbers from pybench make improvements look much better than
   regressions do. You can also checkout the comparison on the new
   [benchmark pages](https://speedcenter.nuitka.net) that I am just
   creating, they are based on codespeed, which I will blog upon
   separately.

Look at this table of results as produced by pybench:

*******************
 Benchmark Results
*******************

.. raw:: html

   <table summary="Comparing CPython and Nuitka with PyBench">
   <tbody>
   <tr>
   <td>**<span style="color: #000000;">Test Name</span>**</td>
   <td>**<span style="color: #000000;">min CPython</span>**</td>
   <td>**<span style="color: #000000;">min Nuitka</span>**</td>
   <td>**<span style="color: #000000;">di</span><span style="color: #000000;">ff</span>**</td>
   </tr>
   <tr>
   <td>BuiltinFunctionCalls</td>
   <td>76ms</td>
   <td>54ms</td>
   <td>+41.0%</td>
   </tr>
   <tr>
   <td>BuiltinMethodLookup</td>
   <td>57ms</td>
   <td>47ms</td>
   <td>+22.1%</td>
   </tr>
   <tr>
   <td>CompareFloats</td>
   <td>79ms</td>
   <td>0ms</td>
   <td><span style="color: #339966;">+inf%</span></td>
   </tr>
   <tr>
   <td>CompareFloatsIntegers</td>
   <td>75ms</td>
   <td>0ms</td>
   <td><span style="color: #339966;">+inf%</span></td>
   </tr>
   <tr>
   <td>CompareIntegers</td>
   <td>76ms</td>
   <td>0ms</td>
   <td><span style="color: #339966;">+inf%</span></td>
   </tr>
   <tr>
   <td>CompareInternedStrings</td>
   <td>68ms</td>
   <td>32ms</td>
   <td>+113.0%</td>
   </tr>
   <tr>
   <td>CompareLongs</td>
   <td>60ms</td>
   <td>0ms</td>
   <td><span style="color: #339966;">+inf%</span></td>
   </tr>
   <tr>
   <td>CompareStrings</td>
   <td>86ms</td>
   <td>62ms</td>
   <td>+38.2%</td>
   </tr>
   <tr>
   <td>CompareUnicode</td>
   <td>61ms</td>
   <td>50ms</td>
   <td>+21.9%</td>
   </tr>
   <tr>
   <td>ComplexPythonFunctionCalls</td>
   <td>86ms</td>
   <td>179ms</td>
   <td><span style="color: #ff0000;">-52.3%</span></td>
   </tr>
   <tr>
   <td>ConcatStrings</td>
   <td>98ms</td>
   <td>99ms</td>
   <td>-0.6%</td>
   </tr>
   <tr>
   <td>ConcatUnicode</td>
   <td>127ms</td>
   <td>124ms</td>
   <td>+2.3%</td>
   </tr>
   <tr>
   <td>CreateInstances</td>
   <td>76ms</td>
   <td>52ms</td>
   <td>+46.8%</td>
   </tr>
   <tr>
   <td>CreateNewInstances</td>
   <td>58ms</td>
   <td>47ms</td>
   <td>+22.1%</td>
   </tr>
   <tr>
   <td>CreateStringsWithConcat</td>
   <td>85ms</td>
   <td>90ms</td>
   <td>-6.5%</td>
   </tr>
   <tr>
   <td>CreateUnicodeWithConcat</td>
   <td>74ms</td>
   <td>68ms</td>
   <td>+9.5%</td>
   </tr>
   <tr>
   <td>DictCreation</td>
   <td>58ms</td>
   <td>36ms</td>
   <td>+60.9%</td>
   </tr>
   <tr>
   <td>DictWithFloatKeys</td>
   <td>67ms</td>
   <td>44ms</td>
   <td>+51.7%</td>
   </tr>
   <tr>
   <td>DictWithIntegerKeys</td>
   <td>64ms</td>
   <td>30ms</td>
   <td>+113.8%</td>
   </tr>
   <tr>
   <td>DictWithStringKeys</td>
   <td>60ms</td>
   <td>26ms</td>
   <td>+130.6%</td>
   </tr>
   <tr>
   <td>ForLoops</td>
   <td>47ms</td>
   <td>15ms</td>
   <td><span style="color: #339966;">+216.2%</span></td>
   </tr>
   <tr>
   <td>IfThenElse</td>
   <td>67ms</td>
   <td>16ms</td>
   <td><span style="color: #339966;">+322.5%</span></td>
   </tr>
   <tr>
   <td>ListSlicing</td>
   <td>69ms</td>
   <td>70ms</td>
   <td>-0.9%</td>
   </tr>
   <tr>
   <td>NestedForLoops</td>
   <td>72ms</td>
   <td>25ms</td>
   <td>+187.4%</td>
   </tr>
   <tr>
   <td>NestedListComprehensions</td>
   <td>87ms</td>
   <td>42ms</td>
   <td>+105.9%</td>
   </tr>
   <tr>
   <td>NormalClassAttribute</td>
   <td>62ms</td>
   <td>77ms</td>
   <td>-18.9%</td>
   </tr>
   <tr>
   <td>NormalInstanceAttribute</td>
   <td>56ms</td>
   <td>24ms</td>
   <td>+129.7%</td>
   </tr>
   <tr>
   <td>PythonFunctionCalls</td>
   <td>72ms</td>
   <td>34ms</td>
   <td>+116.1%</td>
   </tr>
   <tr>
   <td>PythonMethodCalls</td>
   <td>84ms</td>
   <td>38ms</td>
   <td>+120.0%</td>
   </tr>
   <tr>
   <td>Recursion</td>
   <td>97ms</td>
   <td>56ms</td>
   <td>+73.1%</td>
   </tr>
   <tr>
   <td>SecondImport</td>
   <td>61ms</td>
   <td>47ms</td>
   <td>+31.6%</td>
   </tr>
   <tr>
   <td>SecondPackageImport</td>
   <td>66ms</td>
   <td>29ms</td>
   <td>+125.4%</td>
   </tr>
   <tr>
   <td>SecondSubmoduleImport</td>
   <td>86ms</td>
   <td>32ms</td>
   <td>+172.0%</td>
   </tr>
   <tr>
   <td>SimpleComplexArithmetic</td>
   <td>74ms</td>
   <td>62ms</td>
   <td>+18.3%</td>
   </tr>
   <tr>
   <td>SimpleDictManipulation</td>
   <td>65ms</td>
   <td>35ms</td>
   <td>+89.7%</td>
   </tr>
   <tr>
   <td>SimpleFloatArithmetic</td>
   <td>77ms</td>
   <td>56ms</td>
   <td>+39.3%</td>
   </tr>
   <tr>
   <td>SimpleIntFloatArithmetic</td>
   <td>58ms</td>
   <td>39ms</td>
   <td>+48.3%</td>
   </tr>
   <tr>
   <td>SimpleIntegerArithmetic</td>
   <td>59ms</td>
   <td>37ms</td>
   <td>+57.7%</td>
   </tr>
   <tr>
   <td>SimpleListComprehensions</td>
   <td>75ms</td>
   <td>33ms</td>
   <td>+128.7%</td>
   </tr>
   <tr>
   <td>SimpleListManipulation</td>
   <td>57ms</td>
   <td>27ms</td>
   <td>+109.4%</td>
   </tr>
   <tr>
   <td>SimpleLongArithmetic</td>
   <td>68ms</td>
   <td>57ms</td>
   <td>+19.9%</td>
   </tr>
   <tr>
   <td>SmallLists</td>
   <td>69ms</td>
   <td>41ms</td>
   <td>+66.6%</td>
   </tr>
   <tr>
   <td>SmallTuples</td>
   <td>66ms</td>
   <td>98ms</td>
   <td>-32.2%</td>
   </tr>
   <tr>
   <td>SpecialClassAttribute</td>
   <td>63ms</td>
   <td>49ms</td>
   <td>+29.1%</td>
   </tr>
   <tr>
   <td>SpecialInstanceAttribute</td>
   <td>130ms</td>
   <td>24ms</td>
   <td><span style="color: #339966;">+434.5%</span></td>
   </tr>
   <tr>
   <td>StringMappings</td>
   <td>67ms</td>
   <td>62ms</td>
   <td>+8.5%</td>
   </tr>
   <tr>
   <td>StringPredicates</td>
   <td>69ms</td>
   <td>59ms</td>
   <td>+16.6%</td>
   </tr>
   <tr>
   <td>StringSlicing</td>
   <td>73ms</td>
   <td>47ms</td>
   <td>+54.8%</td>
   </tr>
   <tr>
   <td>TryExcept</td>
   <td>57ms</td>
   <td>0ms</td>
   <td><span style="color: #339966;">+3821207.1%</span></td>
   </tr>
   <tr>
   <td>TryFinally</td>
   <td>65ms</td>
   <td>26ms</td>
   <td>+153.4%</td>
   </tr>
   <tr>
   <td>TryRaiseExcept</td>
   <td>64ms</td>
   <td>610ms</td>
   <td><span style="color: #ff0000;">-89.5%</span></td>
   </tr>
   <tr>
   <td>TupleSlicing</td>
   <td>76ms</td>
   <td>67ms</td>
   <td>+12.7%</td>
   </tr>
   <tr>
   <td>UnicodeMappings</td>
   <td>88ms</td>
   <td>91ms</td>
   <td>-2.9%</td>
   </tr>
   <tr>
   <td>UnicodePredicates</td>
   <td>64ms</td>
   <td>59ms</td>
   <td>+8.8%</td>
   </tr>
   <tr>
   <td>UnicodeProperties</td>
   <td>69ms</td>
   <td>63ms</td>
   <td>+8.8%</td>
   </tr>
   <tr>
   <td>UnicodeSlicing</td>
   <td>80ms</td>
   <td>68ms</td>
   <td>+17.6%</td>
   </tr>
   <tr>
   <td>WithFinally</td>
   <td>84ms</td>
   <td>26ms</td>
   <td><span style="color: #339966;">+221.2%</span></td>
   </tr>
   <tr>
   <td>WithRaiseExcept</td>
   <td>67ms</td>
   <td>1178ms</td>
   <td><span style="color: #ff0000;">-94.3%</span></td>
   </tr>
   </tbody>
   </table>
