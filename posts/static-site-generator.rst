.. post:: 2012/01/26 07:32
   :tags: Python
   :author: Kay Hayen

#######################
 Static Site Generator
#######################

Hello,

somehow triggered by reading about Mynth, and the re-post of the last
release announcement on my feed, just because I added a missing category
to the post, I am wondering what it takes to achieve the following:

   -  Edit the pages site as ReST (reStructured text) document with
      links inside
   -  Edit posts as single ReST files
   -  Have it look decent and provide feeds, proper caching headers,
      etc.
   -  Generate a static site from with, with more control over what kind
      of updates makes it into the feed.

I am currently very annoyed, because:

   -  I would normally generate code examples now with "rst2html" and
      replace the existing Wordpress plugin that renders in JavaScript.
      Except I cannot without re-posting all these articles, or removing
      the "python" tag from them.

   -  The documentation of Nuitka is in ReST and I even intend to expand
      it with UML diagrams generated from text. Making the cross to HTML
      content is difficult.

   -  Some pages only replicate content from the User or Developer
      Manual, keeping those updated, in sync, etc. is a dull thing to
      do.

   -  Extending Wordpress in Python is not feasible. And in php, I doubt
      I want to master.

Other stuff in favor of it, is that Wordpress or any CMS needs more
memory and more time to process than static pages of course. I can't
right now let anyone fork and edit the pages in a practical manner. So
while for User Manual and Developer Manual of Nuitka I will get
corrections, for the website it's not happening.

Is Mynth an appropriate intermediate step? Do I really want to learn one
of these strange templating languages or even consider software that has
no Debian package. I never considered "virtualenv" and "pip" much of
options to run software on a website. I guess I am more tied to Debian
than to Python still.

Over the last months I have occasionally looked at Pyramids, but it
seems overly complex, if all you want is to simplify the authoring. I
have seen that e.g. Trac supports ReST as an exception, but that feels
too little for a hefty software like that.

I may end up with using ReST to generate HTML which is then uploaded via
XMLRPC to Wordpress. Won't give me the "static" benefits. Won't solve
the post update problem. But at least will let me edit more easily.

|  Yours,
|  Kay
