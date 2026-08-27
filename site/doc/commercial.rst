:orphan:

.. meta::
   :description: Protect your IP against reverse engineering with the Python compiler Nuitka and turn your Python code into binary. Protect code, data, outputs, and tracebacks!
   :keywords: python,compiler,protection,reverse engineering,encrypted,tracebacks,obfuscate,obfuscation,obfuscator

###################
 Nuitka Commercial
###################

As a commercial user of Python, you need these critical features only
**Nuitka Commercial** offers. Protect your **code**, **data**,
**outputs**, and **tracebacks** while still enjoying major convenience
features for your application.

************************************
 Protection vs. Reverse Engineering
************************************

Hiding your source code and contained keys is crucial to your IP
protection. For this, you need the **Nuitka Commercial** package. It
includes plugins that achieve the following:

.. grid:: 1 1 2 2
   :gutter: 1
   :class-container: hub-card-set commercial-feature-hub

   .. grid-item::

       .. grid:: 1 1 1 1
           :gutter: 1

           .. grid-item-card::  :doc:`/doc/commercial/protect-constants-data`

               Obfuscate contained program constants data

               Your encryption keys, your program texts, your library usages,
               all expose textual information that can be valuable input in
               Reverse Engineering.

               With **Nuitka**, these constants are plain and readable in the
               compiled programs, just like in your **Python** source code or
               its bytecode.

               Compiling with **Nuitka** protects the source code, but with the
               data still being easily readable, it will be less effective than **Nuitka Commercial**, which goes all the way.

           .. grid-item-card::  :doc:`/doc/commercial/protect-data-files`

               Another aspect of data protection is your data files. When your
               program includes data files to work with, these have to be
               visible in the file system. These files unnecessarily expose your
               program to risks. For example, via QML files of Qt, your program
               behavior can be changed by an attacker modifying these files, or
               they can copy their content easily.

               Therefore, **Nuitka Commercial** allows you to embed data files
               as part of the program constants and protect them that way.
               Without these files, the attacker cannot use them as an attack
               vector.

           .. grid-item-card::  :doc:`/doc/commercial/protect-dll-files`

               For best protection of your program at runtime, you need to make sure that DLLs and Python extension modules cannot be swapped out.

               Therefore, **Nuitka VM** lets you embed DLL files as part of an executable that runs inside a protected VM (provided by a different product), that then is used to prevent that attack vector as well.

   .. grid-item::

       .. grid:: 1 1 1 1
           :gutter: 1

           .. grid-item-card:: :doc:`/doc/commercial/traceback-encryption`

               When your program is deployed and crashing, you could take
               steps to prevent these tracebacks from appearing.
               But when you need to support your client, you must be able to
               tell why your software is crashing.

               Python tracebacks are suitable for this, but you do not want
               them to be readable to the user. At this point, traceback encryption
               comes in handy. **Nuitka Commercial** allows you to encrypt all
               traceback outputs. They still carry the information you want, but
               *only you* will be able to decode them.

               Symmetric encryption is available now, with asymmetric
               encryption planned for a future update.

           .. grid-item-card:: Encrypted Outputs :doc:`/doc/commercial/traceback-encryption`

               If you need to query information from a machine or just in general
               want to have perfect protection, you can use the Nuitka plugin to
               make sure it can only output encrypted information on standard output
               and standard error.

               You will be able to decode outputs as necessary, and we will make
               sure it is not readable to anybody but you.

******************************
 Older OSes and Special Needs
******************************

.. grid:: 1 1 2 2
   :gutter: 1
   :class-container: hub-card-set commercial-feature-hub

   .. grid-item::

       .. grid:: 1 1 1 1
           :gutter: 1

           .. grid-item-card:: :doc:`/doc/commercial/legacy-windows-support`

               Deploy to **Windows 7** or even **Windows XP**

               We cannot make your program work on those OSes unless it
               already does. For example, Qt6 requires at least a recent
               Windows 10 version.

               But if it works with **Python** on these OSes, using older
               versions of packages and older toolchain, **Nuitka Commercial**
               allows you to make it portable.

           .. grid-item-card:: :doc:`/doc/commercial/portable-linux-support`

               .. _portable-linux:

               Deploy to **Linux** with a portable build result

               If your program works on RHEL 7 (or CentOS 7 derivatives), then **Nuitka Commercial** can make it portable across all standard Linux distributions,
               using a container build.


   .. grid-item::

       .. grid:: 1 1 1 1
           :gutter: 1

           .. grid-item-card:: :doc:`/doc/commercial/commercial-only-packages`

               For a select few packages, these are supported only with **Nuitka Commercial**. For example, we made patches for older
               packages like PySide2, or because the package handles
               accepting payments for your commercial product.

*************
 Convenience
*************

In this instance, you may have specific needs that only commercial
customers have, which would require significant effort to implement
yourself, but which are included with **Nuitka Commercial**. The time
saved for development may already justify the investment.

.. grid:: 1 1 2 2
   :gutter: 1
   :class-container: hub-card-set commercial-feature-hub

   .. grid-item::

       .. grid:: 1 1 1 1
           :gutter: 1

           .. grid-item-card:: :doc:`/doc/commercial/windows-service`

                Deploying your program as a **Windows Service** becomes trivial.

                For this, **Nuitka Commercial** has a dedicated plugin that makes deploying your practically unchanged program as a **Windows Service** very easy.

   .. grid-item::

       .. grid:: 1 1 1 1
           :gutter: 1

           .. grid-item-card:: :doc:`/doc/commercial/automatic-updates`

               Support for automatic downloads, alerts to them, and
               automatic applying updates of your deployed software.

               Currently supported for **onefile** mode, with standalone
               mode coming in a future update.

*************
 Sponsorship
*************

You are happy with using **Nuitka** and want to benefit more because it
solves a crucial part of your deployment workflow. You may or may not
need the priority package or the **Nuitka Commercial** package.

You can pay this relatively large amount and help **Nuitka** development
in general. And you can know that you get the best support or simply
reward the high-quality service you got with **Nuitka**.

Naturally, sponsors will be entitled to all access and treated with
highest priority.

.. _pricing:

**********
 Purchase
**********

.. include:: /commercial/purchase-grid.inc

*************
 Limitations
*************

When you buy **Nuitka Commercial**, parts of the code - mostly the
plugins that implement the commercial features - are under a
:doc:`license <commercial-license>` that forbids you to distribute the
**Nuitka Commercial** source code. That should be obvious, but otherwise
it does not limit your use of **Nuitka Commercial** at all.

You can use **Nuitka Commercial** on

-  **All** your machines, and **all** OSes

-  **All** your software, deploy as many products and copies as you want

-  Even **after ending the subscription**, you can continue using the
   version you had at the time of cancellation.

Essentially, you are as free with **Nuitka Commercial** as with standard
**Nuitka**. You are only prohibited from distributing **Nuitka
Commercial** to third parties.

**********
 Delivery
**********

#. Pay via Stripe and have that confirmed
#. You get access to the private GitHub repo called
   ``Nuitka-commercial`` which contains **Nuitka Commercial**.
#. Optionally, you can give more users in your GitHub organization
   access via access tokens.
#. **Nuitka Commercial** is a drop-in replacement for **Nuitka** with
   only more options.

**********************
 Reseller Information
**********************

For resellers, there is a page with the information needed:
:doc:`/commercial/resellers`

********************
 Vendor Information
********************

In case you need to fill out a form for your company with the vendor
information, please find the complete set of information on this page
:doc:`/pages/impressum`.

************
 Contact Us
************

Please use `this form to contact us
<https://docs.google.com/forms/d/e/1FAIpQLSeGVpDqhuD0-hkcbsxzQD85PmDdZ_Z31HBIk3ttojcpbSlagg/viewform?usp=sf_link>`_
with the intent of buying Nuitka services, but you still have open
questions.

You can also ask us to solve your deployment: we work in your
environment, set up the compilation, debug it, and you compensate us for
the time spent.

.. important::

   If all you want to do is to purchase, notice the purchase buttons
   above in the Pricing_ section. There is no need to fill out the form,
   Stripe collects all needed information.
