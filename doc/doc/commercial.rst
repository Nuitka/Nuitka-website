:orphan:

.. meta::
   :description: Protect your IP against reverse engineering with the Python compiler Nuitka and turn your Python code into binary. Protect code, data, outputs and tracebacks!
   :keywords: python,compiler,protection,reverse engineering,encrypted,tracebacks,obfuscate,obfuscation,obfuscator

###################
 Nuitka Commercial
###################

As a commercial user of Python, you definitely need these critical
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

   .. grid-item::

       .. grid:: 1 1 1 1
           :gutter: 1

           .. grid-item-card::  Program Constants Data

               Obfuscate contained program constants data

               Your encryption keys, your program texts, your library usages, all
               expose textual information, that can be valuable input in Reverse
               Engineering.

               Normally these constants are plain and readable in the created
               programs (and of course your Python source code or bytecode).
               Compiling with Nuitka gives you protection of the code, but with the
               data being easily readable, it will be less effective.

               :doc:`Read more.... <commercial/protect-constants-data>`

           .. grid-item-card::  Contained Data Files

               Another aspect of data protection are your data files. When your program
               includes data files to work on, these are normally visible in the file
               system. This unnecessarily exposes your program, sometimes, e.g. via QML
               files of Qt, your program behavior can be changed by an attacker modifying
               these files, or they can copy their content easily.

               Therefore Nuitka commercial allows you to embed data files as part
               of the program constants and protect it in the same way as other
               constants. Without these files accessible, the attacker will not
               have these an an attack vector.

               :doc:`Read more.... <commercial/protect-data-files>`

   .. grid-item::

       .. grid:: 1 1 1 1
           :gutter: 1

           .. grid-item-card:: Encrypted Tracebacks

               When your program is deployed and crashing, you could take
               potentially successful steps against these tracebacks appearing. But
               when you need to support your client, you need to be able to to
               actually tell, why your software is crashing.

               Python tracebacks are good for this, but you cannot want them to be
               readable to the user. This is where traceback encryption comes in.
               Nuitka with the commercial plugin will make sure to encrypt all
               traceback outputs. They still carry the information as you want, but
               *only you* will be able to decode them.

               Symmetric encryption (and asymmetric encryption in a future update)
               are available for you to use there.

           .. grid-item-card:: Encrypted Outputs

               If you need to query information from a machine, or just in general
               want to have perfect protection, you can use the Nuitka plugin to
               make sure it can only output encrypted information on standard output
               and standard error.

               This will allow you to decode outputs as necessary, and will make
               sure it's not readable to anybody but you.

******************************
 Older OSes and Special Needs
******************************

.. grid:: 1 1 2 2

   .. grid-item::

       .. grid:: 1 1 1 1
           :gutter: 1

           .. grid-item-card::  Windows 7

               Deploying your program to Windows 7, or even Windows XP. We
               cannot make every program work on these (e.g. Qt6 requires even
               newer Windows 10), but if it works with Python, using older
               versions of packages, then Nuitka can make it portable.

           .. grid-item-card::  RHEL 7 support

               If your program works on RHEL 7 (CentOS 7), then Nuitka can make
               it portable from and to that one too.


   .. grid-item::

       .. grid:: 1 1 1 1
           :gutter: 1

           .. grid-item-card:: Commercial-only packages

               For select few packages, these are only supported with Nuitka commercial. This is because we made patches for older normally
               unsupported packages like PySide2, or because the package is
               for accepting payments, making their use clearly commercial.

               :doc:`Read more.... <commercial/commercial-only-packages>`

*************
 Convenience
*************

In this instance, you have special wishes that only commercial customers
will have and that are effort to maintain.

.. grid:: 1 1 2 2

   .. grid-item::

       .. grid:: 1 1 1 1
           :gutter: 1

           .. grid-item-card::  Windows Service

               Deploying your program as a Windows service is trivial.

               For this, there is a dedicated plugin in Nuitka that makes deployment of a practically unchanged program as a service very easy.

               :doc:`Read more.... <commercial/windows-service>`

       .. grid:: 1 1 1 1
           :gutter: 1

           .. grid-item-card::  Automatic Updates

               Automatic download, alerts to, applying updates of deployed software.

               This is not yet implemented, but will be added in a future update.

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

.. _pricing:

**********
 Purchase
**********

.. include:: /commercial/purchase-grid.inc

*************
 Limitations
*************

When you buy Nuitka commercial, parts of the, mostly the plugins that
implement the commercial only features are under a :doc:`license
<commercial-license>` that forbids you to distribute the Nuitka
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

#. Pay via Stripe and have that confirmed
#. You get access to the private GitHub repo ``Nuitka-commercial`` which
   contains Nuitka plus commercial only parts.
#. Optionally given more users in your GitHub organization access via
   token.
#. Nuitka commercial can then be used as a drop in replacement of Nuitka
   with more options.

********************
 Vendor Information
********************

In case you need to fill out a form for your company with vendor
information, please find the full set of information on this page
:doc:`/pages/impressum`.

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
