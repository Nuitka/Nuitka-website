.. post:: 2015/01/06 12:46:50
   :tags: Python, Nuitka, compiler
   :author: Kay Hayen

######################################
 Article about Nuitka Standalone Mode
######################################

There is a really well written article about Nuitka written by Tom
Sheffler.

.. note::

   The article has since become unavailable unfortunately.

It inspired me to finally become clean with ``__file__`` attributes in
standalone mode. Currently it points to where your source was when
things were compiled. In the future (in standalone mode, for accelerated
mode that continues to be good), it will point into the ``.dist``
folder, so that the SWIG workaround may become no longer necessary.

Thanks Tom for sharing your information, and good article.

|  Yours,
|  Kay
