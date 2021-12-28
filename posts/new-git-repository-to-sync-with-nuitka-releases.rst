For you git fans out there I have just added a new method to download
Nuitka from something I call the release git repository:

.. code::

   git clone http://git.nuitka.net/Nuitka.git

Then do your own modifications, and do:

.. code::

   git pull --rebase

each time there is a new release. You will be led through the merge
process as usual. To reduce your differences, feel free to send me the
patches you create with:

.. code::

   git format-patch <commit-id>

and I will incorporate useful stuff.

.. admonition:: Please note

   If you publish your own git repository, please be so kind and name it
   "Nuitka-unofficial" or similar, or else it might be mistaken with the
   real thing, and drop me a line about it, just so I know.

Kay Hayen
