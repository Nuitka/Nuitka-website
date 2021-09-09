################
 Nuitka Website
################

.. image:: posts/images/nuitka-website-logo.png
   :alt: Nuitka Logo

*******
 Usage
*******

This is used to build the Nuitka web site. Enhancements of all kinds are
welcome. You will need python 3.7 and pipenv to build it, and so far
this has only be done on Linux, but it ought to also work on Windows:

.. code:: sh

   # On Ubuntu only
   sudo apt-get install optipng jpegoptim

   # Creates a virtualenv with all that is needed to develop the
   # site.
   python3.7 -m pip install -U pipenv
   python3.7 -m pipenv install --dev

   # Need to do this at least once to copy manuals, logos
   python3.7 -m pipenv run python update.py --update-docs
   # Now lets build the site
   python3.7 -m pipenv run python update.py --build-site

   # Start local web server with the site.
   python3.7 -m pipenv run nikola auto

   # Browse it (Linux)
   xdg-open http://localhost:8080
   # Browse it (Windows)
   explorer http://localhost:8080

*****************
 Usage of Nikola
*****************

So the site is basically mostly an automation of importing a few files
from the git repository, splitting up e.g. the ``Changelog.rst`` into
pages, with otherwise using Nikola to render it. Reference the `Nikola
handbook <https://getnikola.com/handbook.html>`__ if you have any
questions about how it does that, but it's easy enough.

********
 Thanks
********

Please help and improve this in all ways, typos, cooler tech, better
looks, more information, etc. all is appreciated and necessary.

Right now, this is very rough and the first public release after running
this in private for the longest time. The code is a hack and ugly, and
the content could be way more readable. Your turn!
