################
 Nuitka Website
################

.. image:: ../images/nuitka-website-logo.png
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
this has only be done on Linux, but it ought to also work on Windows,
you can make that work as part of your contribution.

.. code:: bash

   # Creates a virtualenv with all that is needed to develop the
   # site.
   python3 -m pip install -U invoke
   python3 -m invoke virtualenv

   # Now lets build the site, to see if it's all correct.
   python3 -m invoke doc

   # Optionally build the localized sites.
   python3 -m invoke intl -l zh_CN
   python3 -m invoke intl -l de_DE
   ...

   # Start local web server with the site, and do automatic
   # rebuilds. Localization are rebuilt if they were previously
   # built.
   python3 -m invoke run -t serve-site

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
Sphinx documentation and esp. the one for Read the Docs theme and ABlog.

*************
 Translation
*************

Translations of the Nuitka website are very welcome. We have a team for
those want to work on it, with push rights to the repository. Right now
a ``translation`` branch is used, but the plan is for it to be merged,
and to provide the infrastructure in the ``main`` branch.

Here is a table of the files to translate and their styles. Everything
that is not mentioned here, should be asked about if in doubt. Not all
pages make sense to translate.

.. note::

   important

   Before translating, I would love you to also actually review the
   content, if you agree it makes sense, if it can be better structured.
   This is very much needed unfortunately.

.. note::

   There are plans to get rid of ``pages`` and ``doc`` sub-folders of
   the site folder ``doc``. For URLs, these are plain bad, and would
   e.g. be much better as ``python-compiler`` and the like. A plan will
   be devised and put into place, but it will just move and renamed
   pages.

Directory ``posts/``
====================

At this time, the blog posts, esp. old ones should not be translated. I
believe often new content will be created in post form, and then moved
over to pages for translation. A current example are tutorial style
pages including screenshots, which depending on how the e.g. Python
installer look in your language, Explorer and shell prompt, even
screenshots might have to be translated. This will come only later
though.

Page ``pages/donations.rst``
============================

Yes, please go ahead. Let me know if there is any need to hint Paypal,
or when Paypal is not available in your country, what alternative ways
we could use.

Page ``pages/overview.rst``
===========================

Please hold off from this one. It currently is a duplicate of content
that is just the same in ``index.rst`` and not linked, so please ignore
it for now. There is a plan to have a feel good more like a cross road
entry page, that will lead to the kind of page, that the home page is
right now.

Page ``pages/pyside2.rst``
==========================

Very important kind of page, of which I want to have more. Nuitka links
itself to this from the plugin, and it's a landing page to inform users
about troubles that can be expected. We want to have some boilerplate
for this, and a general way of adding these. These user hint pages are
where I think we ought to help the users from real Nuitka to find the
information, and even localized for their needs.

Page ``pages/support.rst``
==========================

This one is not mentioning the Discord server yet, I will add that soon
though. Very important page that should be linked to from many places.

Page ``pages/gsoc2019.rst``
===========================

This is historical information, translation makes no sense, not sure
what to do with it. But if Nuitka were to do it again, we would
translate it ideally for the next time.

Page ``pages/impressum.rst``
============================

This one is required by law in my country, translators might want to add
their information here. I cannot take responsibility for the content of
translations, as I cannot verify it in many cases.

Page ``pages/Presentations.rst``
================================

This one probably should get more love content wise. It's under
construction. I want to go over the blog and link all information from
there. But if you are aware of material in your language, please go
ahead and add it.

Page ``Streaming.rst``
======================

Since this about an English offer, not sure it makes sense, I will also
update it in near future somewhat, but making clear it's going to be an
English content, I think it ought to be translated on a basic level at
the beginning of the page, and then have untranslated content?

Page ``doc/api-doc.rst``
========================

Translation makes no sense and cannot be done currently anyway. The API
doc is going to be generated with Spinx, Doxygen docs are without love.

Page ``doc/commercial.rst`` and folder ``commercial``
=====================================================

Translation is very welcome. There will be more content added over time.
For payment options, please check out if they work for your country and
if not, help me find alternatives. I was e.g. rejected for AliPay in
China, but maybe other things can work. And Russia e.g. has no Paypal
(which I mean to add as an alternative still).

Page ``doc/factory.rst``
========================

Very useful to have it translated.

Page ``doc/welcome.rst``
========================

This is just a playground for me, do not translate, unless we want to
play around with translation mechanics. We will want to e.g. have an
intelligent language switcher at some point, and could try it out there.

Page ``doc/Changelog.rst``
==========================

Do not translate, this is a bizarre amount of work.

Page ``download.rst``
=====================

Very welcome, but beware that ``download.rst.j2`` is the real source.
Tables are generated into the document, this is probably a harder case
technically, so hold off until this is sorted out.

Page ``developer-manual.rst``
=============================

Makes no sense to translate. But potentially there is content that
belongs to user manual in there or should be split off.

Page ``roadmap.rst``
====================

Much like changelog, not as much work, but also not as important.

Page ``doc/user-manual.rst``
============================

This one is most important in my mind, optimization section needs a
serious update from my side, maybe ignore that, until I get there.
Review applies here very much. I think Tutorial parts might be factored
out to separate documents.

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
