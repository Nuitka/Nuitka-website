.. meta::
   :description: Protect your IP against reverse engineering with the Python compiler Nuitka and turn your Python code into binary. Protect code, data, outputs and tracebacks!
   :keywords: python,compiler,protection,reverse engineering,encrypted,tracebacks,obfuscate,obfuscation,obfuscator

###################
 Nuitka Commercial
###################

As a commercial user of Python, you definitely need these 4 critical
features that only Nuitka commercial offers. Protect your code, your
data, your outputs, and tracebacks while still enjoying major
convenience features for your application.

************************************
 Protection vs. Reverse Engineering
************************************

Hiding your source code and contained keys is crucial to your IP
protection. For this, you need the Nuitka commercial package. It
contains plugins to Nuitka that will achieve the following:

.. grid:: 1 1 2 2

   .. grid-item-card::  Program Constants Data
      :class-item: nuitka-grid-security

      Obfuscate contained program constants data

      Your encryption keys, your program texts, your library usages, all
      expose textual information, that can be valuable input in Reverse
      Engineering.

      Normally these constants are plain and readable in the created
      programs (and of course your Python source code or bytecode).
      Compiling with Nuitka gives you protection of the code, but with the
      data being easily readable, it will be less effective.

      `Read more.... <commercial/protect-constants-data.html>`__

   .. grid-item-card::  Contained Data Files
      :class-item: nuitka-grid-security

      Another aspect of data protection are your data files. When your program
      includes data files to work on, these are normally visible in the file
      system. This unnecessarily exposes your program, sometimes, e.g. via QML
      files of Qt, your program behavior can be changed by an attacker modifying
      these files, or they can copy their content easily.

      Therefore Nuitka commercial allows you to embed data files as part
      of the program constants and protect it in the same way as other
      constants. Without these files accessible, the attacker will not
      have these an an attack vector.

      `Read more.... <commercial/protect-data-files.html>`__


   .. grid-item-card:: Encrypted Tracebacks
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

..      TODO: When that page has sufficient contents.
..      `Read more.... <commercial/encrypted-tracebacks.html>`__

   .. grid-item-card:: Encrypted Outputs
      :class-item: nuitka-grid-security

      If you need to query information from a machine, or just in general
      want to have perfect protection, you can use the Nuitka plugin to
      make sure it can only output encrypted information on standard output
      and standard error.

      This will allow you to decode outputs as necessary, and will make
      sure it's not readable to anybody but you.


   .. grid-item-card:: Commercial-only packages
      :class-item: nuitka-grid-security

      For select few packages, these are only supported with Nuitka commercial.

      `Read more.... <commercial/commercial-only-packages.html>`__

*******************************************
 Special needs (Commercial only use cases)
*******************************************

In this instance, you have special wishes that only commercial customers
will have and that are effort to maintain.

-  You might e.g. you want to deploy a Windows service

   For this, there is a dedicated plugin in Nuitka that makes deployment
   of a practically unchanged program as a service very easy.

   `Read more.... <commercial/windows-service.html>`__

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
your issues. If you subscribe to this, reported issues will be solved
with highest priority, to enable you using Nuitka.

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

         `Subscribe now </stripe/checkout-commercial-subscription>`__

       - Commercial only Features

       - All your applications

       - Standard Support

   .. grid-item-card::  Nuitka Priority
      :class-item: nuitka-grid-offer nuitka-offer-priority

       .. container:: nuitka-price

           € 250

       .. container:: nuitka-buy

         `Subscribe now </stripe/checkout-priority-subscription>`__

       - Best Support

       - Issues have **Priority**

       - **No** Commercial features


   .. grid-item-card::  Full Package
      :class-item: nuitka-grid-offer nuitka-offer-full-package

       .. container:: nuitka-price

           € 400

       .. container:: nuitka-buy

         `Subscribe now </stripe/checkout-full-subscription>`__

       - Nuitka Commercial **plus**

       - Nuitka Priority


   .. grid-item-card::  Sponsor
      :class-item: nuitka-grid-offer nuitka-offer-sponsor

       .. container:: nuitka-price

           € 1000

       .. container:: nuitka-buy

         `Subscribe now </stripe/checkout-sponsor-subscription>`__

       - Best Support

       - Nuitka Commercial

       - Roadmap Influence

       - Use Cases Priority

.. important::

   Click the buttons in the boxes above if Stripe payment works for you
   (bank transfer, credit card, SEPA debit charge, etc).

*************
 Limitations
*************

When you buy Nuitka commercial, parts of the, mostly the plugins that
implement the commercial only features are under a `license
<commercial-license>`__ that forbids you to distribute the Nuitka
commercial source code. That should be obvious, but otherwise it does
not limit your use of Nuitka at all.

You can use Nuitka commercial on

-  All your machines, all OSes

-  All your software, deploy as many as you want

-  Even after ending the subscription (on that particular version you
   have)

Basically you are as free with Nuitka commercial as with standard
Nuitka. Only for distribution of that Nuitka commercial version to third
parties, you are limited.

**********
 Delivery
**********

#. Pay via Stripe or Crypto currency and have that confirmed
#. You get access to the private GitHub repo ``Nuitka-commercial`` which
   contains Nuitka plus commercial only parts.
#. Optionally given more users in your GitHub organization access via
   token.
#. Nuitka commercial can then be used as a drop in replacement of Nuitka
   with more options.

************
 Contact Us
************

Please use `this form to contact us
<https://docs.google.com/forms/d/e/1FAIpQLSeGVpDqhuD0-hkcbsxzQD85PmDdZ_Z31HBIk3ttojcpbSlagg/viewform?usp=sf_link>`_
with intent of buying Nuitka services, but still open questions. You can
also ask for solving your deployment, where working in your environment
the compilation is done by us, and we will be compensated for our time
extra.

.. important::

   If all you want to do is to purchase, notice the purchase buttons
   above in the Pricing_ section. There is no need to fill out the form,
   Stripe collects all needed information.
