.. post:: 2010/08/18 07:49
   :tags: compiler, Nuitka, Python
   :author: Kay Hayen

###############################
 Releasing Nuitka to the World
###############################

Obviously this is very exciting step for me. I am releasing Nuitka
today. Finally. For a long time I knew I would, but actually doing it,
is a different beast. Reaching my goals for release turned out to be
less far away than I hope, so instead of end of August, I can already
release it now.

Currently it's not more than 4% faster than CPython. No surprise there,
if all you did, is removing the bytecode interpretation so far. It's not
impressive at all. It's not even a reason to use it. But it's also only
a start. Clearly, once I get into optimizing the code generation of
Nuitka, it will only get better, and then probably in sometimes dramatic
steps. But I see this as a long term goal.

I want to have infrastructure in the code place, before doing lots of
possible optimizations that just make Nuitka unmaintainable. And I will
want to have a look at what others did so far in the domain of type
inference and how to apply that for my project.

I look forward to the reactions about getting this far. The supported
language volume is amazing, and I have a set of nice tricks used. For
example the way generator functions are done is a clever hack.

Where to go from here? Well, I guess, I am going to judge it by the
feedback I receive. I personally see "constant propagation" as a
laudable first low hanging fruit, that could be solved.

Consider this readable code on the module level:

.. code:: python

   meters_per_nautical_mile = 1852


   def convertMetersToNauticalMiles(meters):
       return meters / meters_per_nautical_mile


   def convertNauticalMilesToMeters(miles):
       return miles * meters_per_nautical_mile

Now imagine you are using this very frequently in code. Quickly you
determine that the following will be much faster:

.. code:: python

   def convertMetersToNauticalMiles(meters):
       return meters / 1852


   def convertNauticalMilesToMeters(miles):
       return miles * 1852

Still good? Well, probably next step you are going to inline the
function calls entirely. For optimization, you are making your code less
readable. I do not all appreciate that. My first goal is there to make
the more readable code perform as well or better as the less readable
variant.

But yes, lets see what happens. Oh, and you will find its `latest
version here </pages/download.html>`_.

Kay Hayen
