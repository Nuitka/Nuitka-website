################
 Nuitka Website
################

.. image:: posts/images/nuitka-website-logo.png
   :alt: Nuitka Logo

********
 Thanks
********

Please help and improve this in all ways, typos, cooler tech, better
looks, more information, etc. all is appreciated and necessary.

Right now, this is very much possible to improve. Your turn!

*******
 Usage
*******

This is used to build the Nuitka web site. Enhancements of all kinds are
welcome. You will need python 3.9 and ``pipenv`` to build it, and so far
this has only be done on Linux, but it ought to also work on Windows, you
can make that work as part of your contribution.

.. code:: bash

   # Creates a virtualenv with all that is needed to develop the
   # site.
   python3.9 -m pip install -U pipenv
   python3.9 -m pipenv install --dev

   # Need to do this at least once to make manuals, logos
   # available for build.
   python3.9 -m pipenv run python update.py --update-docs

   # Now lets build the site, to see if it's all correct.
   python3.9 -m pipenv run python update.py --build-site

   # Start local web server with the site, and do automatic
   # rebuilds
   python3.9 -m pipenv run python update.py --serve-site

   # Browse it (Linux)
   xdg-open http://localhost:8080
   # Browse it (Windows)
   explorer http://localhost:8080

*****************
 Usage of Sphinx
*****************

So the site is basically mostly an automation of importing a few files
from the Nuitka git repository, splitting up e.g. the ``Changelog.rst``
into pages, with otherwise using Sphinx to render it. Reference the
Sphinx documentation and esp. the one for read the docs theme and ABlog.

********************
 Image Optimization
********************

.. code:: bash

   # Optimize PNG files like this, normally not needed, this
   # is lossless.
   sudo apt-get install optipng
   find . -iname *.png -a -type f -exec optipng -o7 -zm1-9 {} \;

   # Optimize JPEG files like this, normally not needed, this
   # is lossless.
   sudo apt-get install jpegoptim
   find . -iname *.jpg -a -type f -exec jpegoptim {} \;
