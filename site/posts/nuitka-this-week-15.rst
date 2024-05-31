.. post:: 2024/01/30
   :tags: Python, compiler, Nuitka, NTW
   :author: Kay Hayen

######################
 Nuitka this week #15
######################

This is a weekly update, or at least it's supposed to be of what's going
on in Nuitka land, for you to learn about ongoing developments and
important changes to the project.

In this issue, I am first going to cover a bit of backlog from news
update missed in the past, but also covering very exciting changes from
this week.

.. contents::

***************
 Nuitka Action
***************

A GitHub Action is a component used in GitHub workflows. These are yaml
driven configurations that can cause GitHub to do automatic building of
your software.

Many of the more professional users build their binaries as part of
GitHub workflows, and Nuitka and Nuitka commercial are both used in that
way a lot. Many times people do it on their own, i.e. install Nuitka by
hand, and call it by hand, which is kind of not the preferred way for
many people.

Enter the great `Nuitka Action
<https://github.com/Nuitka/Nuitka-Action>`__ which was originally
created by `Jim Kring <https://github.com/jimkring>`__, who handed over
the maintenance of it to the Nuitka organization that has further
refined it. This was a great contribution that makes it everything
easier for Nuitka users on GitHub if they want to use it.

.. code:: yaml

   - name: Build Executable
     uses: Nuitka/Nuitka-Action@main
     with:
       nuitka-version: main
       script-name: kasa_cli
       onefile: true

   - name: Upload Artifacts
     uses: actions/upload-artifact@v3
     with:
       name: ${{ runner.os }} Build
       path: |
         build/*.exe
         build/*.bin
         build/*.app/**/*

Options of Nuitka are exposed as yaml attributes. The documentation of
this mapping could be very much enhanced, but basically it's just
dropping the ``--`` part from e.g. ``--onefile`` and for toggles, you
say ``true``.

Now one interesting limitation of GitHub Action, I have come across this
week and that is that it's not easily possible to specify an option
twice. For some values in Nuitka, that however is necessary. Where
module names are acceptable, a ``,`` separation os supported, but with
file paths, we don't do that, e.g. not with ``--include-data-dir`` (note
``--include-package-data`` is much better to use) but that is the one it
came up for.

But now we support splitting by new-line from GitHub actions for
everything that produces a list value as a Nuitka option. See below for
a very nice example of how the ``|`` in Yaml makes that even easy to
read.

.. code:: yaml

   - name: Build Executable
     uses: Nuitka/Nuitka-Action@main
     with:
       nuitka-version: main
       script-name: kasa_cli
       onefile: true
       include-data-dir: |
         source_path_dir1=dest_path_dir1
         source_path_dir2=dest_path_dir2
         source_path_dir3=dest_path_dir3

.. note::

   This works with Nuitka 2.0 or higher.

The Nuitka-Action is permanently refined. Just today we updated its
caching action to latest, and there is an ongoing activity to improve
options. We started to generate options from Nuitka help output
directly, so that it is easier to add support for new Options in Nuitka,
and to generally make them more consistent.

***********
 Community
***********

On the Discord server, you can get in touch with an ever more vibrant
community of Nuitka users. You are welcome to join us on the `Discord
server for Nuitka community <https://discord.gg/nZ9hr9tUck>`__ where you
can hang out with the developers and ask questions. It's not intended as
an interactive manual. You are supposed to read the docs for yourself
first. And issues are best reported to GitHub.

I am also now occasionally on the Python Discord server. Mostly when I
get summoned to answer questions that my community thinks make sense,
and have been awarded the community role there, which is pretty nice. I
seem to make new connections there.

*******************
 Optimization Work
*******************

For me this is extremely exciting, this has been on my nerves for a long
time, and I didn't have the time to figure it out. Now for the
scalability work, I wanted to make sure the algorithm used for loop type
analysis is actually going to be sustainable, before I optimize the
implementation to scale better.

And low and behold, one of my oldest code examples, the one I mean to
demonstrate C type performance from Python code with, has failed to get
proper results for a long time now. But this changed this week and it's
part of the 2.0 release, making it my mind worth the bump itself.
Checkout this annotated code.

.. code:: python

   # Initially the value of undefined "i" is "NUITKA_NINT_UNASSIGNED"
   # in its indicator part. The C compiler will remove that assignment
   # as it's only checked in the assignment coming up.

   i = 0
   # Assignment from a constant, produces a value where both the C
   # and the object value are value. This is indicated by a value
   # of "NUITKA_NINT_BOTH_VALID". The code generation will assign
   # both the object member from a prepared value, and the clong
   # member to 0.

   # For the conditional check, "NUITKA_NINT_CLONG_VALID" will
   # always be set, and therefore function will resort to comparing
   # that clong member against 9 simply, that will always be very
   # fast. Depending on how well the C compiler can tell if an overflow
   # can even occur, such that an object might get created, it can even
   # optimize that statically. In this case it probably could, but we
   # do not rely on that to be fast.
   while i < 9:  # RICH_COMPARE_LT_CBOOL_NINT_CLONG
       # Here, we might change the type of the object. In Python2,
       # this can change from ``int`` to ``long``, and our type
       # analysis tells us that. We can consider another thing,
       # not "NINT", but "NINTLONG" or so, to special case that
       # code. We ignore Python2 here, but multiple possible types
       # will be an issue, e.g. list or tuple, float or complex.
       # So this calls a function, that returns a value of type
       # "NINT" (actually it will become an in-place operation
       # but lets ignore that too).
       # That function is "BINARY_OPERATION_ADD_NINT_NINT_CLONG"(i, 1)
       # and it is going to check if the CLONG is valid, add the one,
       # and set to result to a new int. It will reset the
       # "NUITKA_NINT_OBJECT_VALID" flag, since the object will not be
       # bothered to create.
       i = i + 1

   # Since "NUITKA_INT_OBJECT_VALID" not given, need to create the
   # PyObject and return it.
   return i

Now that the loop analysis works, I will be much happier to make the
value trace collection faster. I will describe it when I do it. From
here on for optimization, the C type ``NINT`` needs to be created and
code generation for the branching helper functions be added, and then
the should see this perform perfectly.

Functions like ``RICH_COMPARE_LT_CBOOL_NINT_CLONG`` will look like this.
We do not yet have ``RICH_COMPARE_LT_CBOOL_LONG_CLONG`` which it will
fall back to, but we did ``RICH_COMPARE_LT_CBOOL_INT_CLONG`` for Python2
a while ago, and we could expand that no problem.

.. code:: C

   extern bool RICH_COMPARE_LT_CBOOL_NINT_CLONG(nuitka_long *operand1, long operand2) {
      if (operand1->validity & NUITKA_LONG_VALUE_VALID) {
         return operand1->long_value < operand2;
      } else {
         return RICH_COMPARE_LT_CBOOL_LONG_CLONG(operand1->long_object, operand2);
      }
   }

Once I get to that, performance will get a hot topic. From there then,
adding sources of type information, be it profile guided compilation, be
it type annotations, be it ever better compile time type inference, will
start to make a lot more sense.

************
 Nuitka 2.0
************

The 2.0 release has been made. I am going to announce it separately. I
am usually waiting for a few days, to settle potentially regressions.
This time older C compiler support needed a fixup, there is always
something. And then I announce it when I feel that the regressions are
gone and that new users will not encounter obvious breakage at all.

******************
 Technical Writer
******************

When I first launched Nuitka commercial, I needed to get myself
financially supported, dropping my day job after 20 years. I am willing
to say that has happened.

Now as you all know, Nuitka is technically excellent. I cannot say the
same thing of the documentation. Large parts of Nuitka commercial are
still not even publicly described. The User Manual of Nuitka is good,
but not nearly as good as it should be. The website is kind of
unorganized. It's pretty obvious that my talent is not there. I have
received plenty of help over the years, but it's not been enough to
match Nuitka and Nuitka commercial outstanding quality.

So, what I did this week, after seeing that my financial projection for
the coming years seems to allow it, is to attempt and hire people on a
free lancing basis. The first step is a technical writer. She will know
very little of Python and even the terminal, but she will know how to
organize and improve the content of Nuitka.

It will take time for her to get there and this is very fresh.

**********************************
 Nuitka Website as a DevContainer
**********************************

As a first necessary step to make it easier to contribute to the Nuitka
documentation, the website repo, has gained DevContainer configuration.
It will install a small Ubuntu via docker (or podman if you configured
Visual Code like that), and run the pipenv environment and a daemon to
open the website.

The docs for that are spotty right now, and the Technical Writer that is
using that, is tasked to improve this right now.

It should become really easy that way to contribute enhancements to the
documentation.

I have yet to figure out how to handle the release matching
documentation vs. website documentation for user manual. But the idea is
certainly that the Nuitka documentation is edited on the website.

****************************
 Nuitka Website Refinements
****************************

With the DevContainer the need for ``translation`` and ``staging`` sites
is gone. The ``Nuitka/Website`` has been disbanded, since it was only
used to control access to "live" rendered branches of the website, that
are no more.

As part of the DevContainer process, the website build was changed to
Python 3.10 so that Ubuntu image is easier to use (was Debian 3.9 so
far). The used tools got all upgraded, and many small improvements came
out of it. Links got checked after the upgrade, finding a few broken
ones, and the translation dropdown is now only present when there are
actual translations. Previously e.g. all posts were having them, which
made no sense.

Making the container smoother to use will be an ongoing process. How to
integration Nuitka ``auto-format`` in an easy fashion is still being
looked at.

******************************
 Nuitka Package Configuration
******************************

So I added a `post that explains variables,
<https://nuitka.net/posts/nuitka-package-config-part3.html>`__ but the
one for parameters, I still need to do that and also update the actual
reference documentation.

*********
 Teasers
*********

Future TWN still have a lot to talk about, we will speak about
Nuitka-Python (our own Python fork with incredible capabilities), about
Nuitka-Watch (our way of making sure Nuitka works with PyPI packages and
hot-fixes to not regress), about compilation reports as a new feature,
Windows AV stuff, onefile improvements, and so on and so on. I got
interesting stuff for many weeks. Limiting myself for now or I will
never publish this.

**********************
 Twitter and Mastodon
**********************

I should be more active there, although often I fail due to not wanting
to talk about unfinished things, so actually I do not post there as
much.

-  `Follow @kayhayen on Twitter
   <https://twitter.com/kayhayen?ref_src=twsrc%5Etfw>`_

-  `Follow @kayhayen on Mastodon <https://fosstodon.org/@kayhayen>`_

And lets not forget, having followers make me happy. So do re-tweets.
Esp. those, please do them.

*************
 Help Wanted
*************

Nuitka definitely needs more people to work on it. I hope the technical
writer will aid us in better laying how ways for you to help.

If you are interested, I am tagging issues `help wanted
<https://github.com/kayhayen/Nuitka/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22>`_
and there is a bunch, and very likely at least one *you* can help with.
