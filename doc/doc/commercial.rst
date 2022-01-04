###################
 Nuitka Commercial
###################

If you are a commercial user of Nuitka, you fall into one of 4
categories, which Nuitka tries to address.

*************************************
 Protection vs. Reverse Enginneering
*************************************

Hiding your source code and contained keys is crucial to your IP
protection. For this, you need the Nuitka commercial package. It
contains plugins to Nuitka that will achieve the following:

.. grid:: 1 1 2 2

   .. grid-item-card::  Program Constants Data
      :class-item: nuitka-grid-security

      Obfuscucate contained program constants data

      Your encryption keys, your program texts, your library usages, all
      expose textual information, that can be valuable input in Reverse
      Enginneering.

      Normally these constants are plain and readable in the created
      programs (and of course your Python source code or bytecode).
      Compiling with Nuitka gives you protection of the code, but with the
      data being easily readable, it will be less effective.

   .. grid-item-card::  Contained Data Files
      :class-item: nuitka-grid-security

      Another facet of the same issue is datafiles. When your program
      includes data files to work on, these are visible in the file system.
      Sometimes, e.g. via QML files of Qt, your program behaviour can be
      changed by changing these files.

      Therefore Nuitka commercial allows you to include data files as part
      of the program constants and protect it in the same way as other
      constants. Without these files accessible, the attacker will have no
      attack vector for Reverse Enginneering.

   .. grid-item-card:: Encrypted tracebacks
      :class-item: nuitka-grid-security

      When your program is deployed and crashing, you could take
      potentially successful steps against these tracebacks appearing. But
      when you need to support your client, you need to be able to to
      actually tell, why your software is crashing.

      Python tracebacks are good for this, but you cannot want them to be
      readable to the user. This is very traceback encryption comes in.
      Nuitka with the commercial plugin will make sure to encrypt all
      traceback outputs. They still carry the information as you want, but
      *only you* will be able to decode them.

      Symmetric encryption (and asymmetric encryption in a future update)
      are available for you to use there.

      In a future update, you can decide which information is transferred,
      and what is part of the encryption, and which part is not, e.g.
      hostname, client name, etc. could be output int plain text, while the
      variable names and values would not be, depending on your choice!

   .. grid-item-card:: Encrypted outputs
      :class-item: nuitka-grid-security

      If you need to query information from a machine, or just in general
      want to have perfect protection, you can use the Nuitka plugin to
      make sure it can only output encrypted information on standard output
      and standard error.

      This will allow you to decode outputs as necessary, and will make
      sure it's not readable to anybody but you.

*******************************************
 Special needs (Commercial only use cases)
*******************************************

In this instance, you have special wishes that only commercial customers
will have and that are effort to maintain.

-  You might e.g. you want to deploy a Windows service

   For this, there is a dedicated plugin in Nuitka that makes deployment
   of a practically unchanged program as a service very easy.

-  You might need to support special commercial grade software.

   This can be done, but you might have to pay for the development time
   this takes.

-  You might need to support very old OSes, e.g. RHEL 5.

   Again, this can be done, but you might have to pay for the
   development time this takes.

-  Automatic download, alerts to, applying updates of deployed software.

   This is not yet implemented, but will be added in a future update.

   Support for these things will also be covered in the Nuitka
   commercial package, and while you might not care necessarily about
   hiding your source or data, but much rather you care about the
   quality of deployment of your software.

**************************
 Priority Issue Solutions
**************************

You might have an issue that blocks you from using Nuitka, which you
want to use though, because of performance gains, the IP protection,
with or without the commercial plugins.

The Nuitka Priority package gives you access to elevated priority of
your issues. If you buy this, reported issues will be solved with
highest priority, to enable you using Nuitka.

*************
 Sponsorship
*************

You are happy in using Nuitka and you want to benefit it, because it
solves a crucial part of your workflow in deployment. You may or may not
need the priority package or the commercial package. You can pay the
relatively large amount and help Nuitka development in general. And you
can know that it remains active and supported and pay back to the
relatively free service you get on a daily basis.

Naturally sponsors will be entitled to all access and treated with
highest priority.

*********
 Pricing
*********

.. grid:: 1 2 2 4

   .. grid-item-card::  Nuitka Commercial
      :class-item: nuitka-grid-offer nuitka-offer-commercial

       .. container:: nuitka-price

           € 250

       .. container:: nuitka-buy

           `Buy Now <https://buy.stripe.com/4gwaHmgmG4s4h2g001>`__

       - Commercial only Features

       - All your applications

       - Standard Support

   .. grid-item-card::  Nuitka Priority
      :class-item: nuitka-grid-offer nuitka-offer-priority

       .. container:: nuitka-price

           € 250

       .. container:: nuitka-buy

           `Buy Now <https://buy.stripe.com/7sI6r6b2mf6IaDS9AC>`__

       - Best Support

       - Issues have **Priority**

       - **No** Commercial features


   .. grid-item-card::  Full Package
      :class-item: nuitka-grid-offer nuitka-offer-full-package

       .. container:: nuitka-price

           € 400

       .. container:: nuitka-buy

           `Buy Now <https://buy.stripe.com/3cs7va1rM8Ik5jy003>`__

       - Nuitka Commercial **plus**

       - Nuitka Priority


   .. grid-item-card::  Sponsor
      :class-item: nuitka-grid-offer nuitka-offer-sponsor

       .. container:: nuitka-price

           € 1000

       .. container:: nuitka-buy

           `Buy Now <https://buy.stripe.com/9AQ3eUb2maQs7rG28c>`__

       - Best Support

       - Nuitka Commercial

       - Roadmap Influence

       - Use Cases Priority

-  Nuitka commercial subscription

   Currently 250 EUR (or 300 USD), valid for one year, renewal same
   price. `Buy Now <https://buy.stripe.com/4gwaHmgmG4s4h2g001>`__.

-  Nuitka Priority package

   Currently 250 EUR (or 300 USD), valid for one year, renewal same
   price. `Buy Now <https://buy.stripe.com/7sI6r6b2mf6IaDS9AC>`__.

-  Nuitka Full Package

   Contains Nuitka Commercial subscription and priority package. Priced
   at 400 EUR (or 500 USD). `Buy Now
   <https://buy.stripe.com/3cs7va1rM8Ik5jy003>`__.

-  Nuitka Sponsors

   Pick your value.

************
 Contact Us
************

Please use `this form to contact us
<https://docs.google.com/forms/d/e/1FAIpQLSeGVpDqhuD0-hkcbsxzQD85PmDdZ_Z31HBIk3ttojcpbSlagg/viewform?usp=sf_link>`_
with intent of buying Nuitka products
