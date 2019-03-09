There is now a Windows installer and a Debian package of `Nuitka
</pages/overview.html>`_ available on the `Download </pages/download.html>`_
page. Please try it out and give me feedback.

Specifically I do know that the Debian package won't work on Debian Squeeze, but
only on Debian Wheezy (Testing) maybe it does on Ubuntu as well, please
report. If you have anything to criticize about the package, let me know. There
is no apt source now, I hope to get it into Debian proper directly.

UPDATE: After Stani's report that Ubuntu has an older Scons, I lowered the
dependency and updated the package on the `Download </pages/download.html>`_
page. It may now work on Ubuntu as well.

And then, the Windows installer still requires you to install MinGW and add it
to your path, but it's clearly a huge step ahead. It's created with distutils,
and that works very well. If you have the skills to enhance it, so e.g. the PATH
variable is changed, or it will launch a MinGW install if not present, contact
me and help.

UPDATE: And the idea that I got while writing a reply to "swong" is also now
implemented. The new Nuitka on Windows simply guesses the PATH to MinGW to be
the default path ``C:\MinGW`` or at least ``\MinGW`` and from there, it ought to
just run after you installed it. Of course you can still set your own PATH
environment and make the pick yourself.

Yours,
Kay Hayen
