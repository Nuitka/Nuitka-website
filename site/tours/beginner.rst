:orphan:

.. meta::
   :description: The Nuitka beginner tour: what the Python compiler is and how to create your first executable.
   :keywords: nuitka,beginner,getting started,first steps,python compiler

######################
 Nuitka Beginner Tour
######################

Dear Python beginner,

you are new to Python, and maybe new to compilers too. This tour shows
you, without much jargon, what Nuitka can do for you and how to get
started. If you get stuck at any point, there is a community of
volunteers that is happy to help.

****************
 What is Nuitka
****************

Nuitka is a compiler for Python programs. Normally, a Python program
needs Python installed to run, and it runs directly from your source
files. Nuitka translates your program into a real executable, like the
programs you download from the internet, that runs on its own.

For you as a beginner, this has two nice effects:

-  Your program becomes faster.

-  You can give your program to other people, and they do not need
   Python at all.

Nuitka supports |SUPPORTED_PYTHONS|.

*************
 First Steps
*************

These five steps take you from a Python file to a program you can hand
to someone else. Every command works the same on Windows, Linux, and
macOS. Only the names of the files created differ, as noted along the
way.

.. tour-step:: Check Python

   Open a terminal in the folder of your program and make sure Python
   runs. Use the Python your program already works with.

   .. code:: bash

      python --version

   .. program-output::

      Python 3.13.9

   On Linux and macOS the command may be called ``python3``. Use that
   name everywhere below then.

.. tour-step:: Install Nuitka

   Nuitka is a normal Python package. Install it into the same Python,
   ideally into the virtual environment of your project.

   .. code:: bash

      python -m pip install -U Nuitka
      python -m nuitka --version

   .. program-output::

      4.4
      Commercial: None
      Python: 3.13.9 ...
      Flavor: CPython Official
      ...

.. tour-step:: Have a C compiler

   Nuitka turns your code into C, so it needs a C compiler. Pick your
   system:

   .. tab-set::

      .. tab-item:: Windows

         Nothing to do in most cases. If Visual Studio 2022 or the free
         *Build Tools for Visual Studio* with the C++ workload are
         installed, Nuitka uses them. Otherwise, Nuitka offers to
         download a C compiler on the first build. Answer ``yes``, it
         goes into a cache in your user folder and is reused.

      .. tab-item:: Linux

         Install ``gcc`` from your distribution. ``patchelf`` is needed
         for standalone and onefile programs.

         .. code:: bash

            sudo apt install gcc patchelf      # Debian, Ubuntu
            sudo dnf install gcc patchelf      # Fedora, RHEL

      .. tab-item:: macOS

         Install the command line tools of Xcode once.

         .. code:: bash

            xcode-select --install

.. tour-step:: Compile once to try it

   Without options, Nuitka compiles only your main file and the result
   still uses the Python installed on your machine. That is the
   quickest check that everything is set up. Use your own program, or
   this ``hello.py``:

   .. code:: python

      print("Hello from compiled Python")

   .. code:: bash

      python -m nuitka hello.py

   .. program-output::

      Nuitka: Starting Python compilation with:
      Nuitka:   Version '4.4' on Python 3.13 (flavor 'CPython Official') commercial grade 'not installed'.
      Nuitka: Completed Python level compilation and optimization.
      Nuitka: Generating source code for C backend compiler.
      Nuitka: Running C compilation via Scons.
      Nuitka: Successfully created 'hello.exe'.

   Run ``hello.exe`` (``./hello.bin`` on Linux and macOS). It prints
   exactly what ``python hello.py`` prints.

   .. program-output::

      Hello from compiled Python

.. tour-step:: Make it portable

   To give the program to someone without Python, choose a mode that
   includes Python. Start with ``standalone``, check that the program
   works from its folder, then switch to ``onefile`` if you want a
   single file.

   .. code:: bash

      python -m nuitka --mode=standalone hello.py
      python -m nuitka --mode=onefile hello.py

   .. program-output::

      Nuitka: Successfully created 'hello.dist\hello.exe'.
      Nuitka-Onefile: Creating single file from dist folder, this may take a while.
      Nuitka: Successfully created 'hello.exe'.

***********************
 Which mode do I need?
***********************

The ``--mode`` option decides what you get. Pick by what you want to
hand over.

.. list-table::
   :header-rows: 1
   :widths: 18 34 48

   -  -  Mode
      -  You get (from ``app.py``)
      -  Use it when

   -  -  ``accelerated``
      -  ``app.exe`` that uses the installed Python
      -  You run the program yourself and want it faster. This is the
         default.

   -  -  ``standalone``
      -  Folder ``app.dist`` with ``app.exe`` inside
      -  You install or copy the program to other machines, or build an
         installer.

   -  -  ``onefile``
      -  A single ``app.exe``
      -  You want one file to send, download, or put on a share.

   -  -  ``app``
      -  ``onefile``, but ``app.app`` bundle on macOS
      -  You ship a desktop program to Windows, Linux, and Mac users.

   -  -  ``module``
      -  ``app.cp313-win_amd64.pyd`` extension module
      -  You keep Python, but want one module compiled, e.g. for speed
         or to not ship its source.

   -  -  ``package``
      -  One extension module for a whole package
      -  Like ``module``, for a package directory.

On Linux and macOS the executables are named ``app.bin``, and extension
modules end in ``.so``.

**********************
 Examples by category
**********************

Each example shows the input, the command, what Nuitka creates, and what
happens when the result runs. Logs are shortened to the important lines.

.. tab-set::

   .. tab-item:: Command-line tool

      A small tool that adds up a column of a CSV file, the one from the
      recording on :doc:`/intro`. Arguments, standard output, and the
      exit code work exactly like with Python, so scripts and schedulers
      that call it do not change.

      .. example-part:: input
         :columns:

         .. code:: text

            csvsum/
            ├── csvsum.py
            └── sales.csv

         .. code:: python

            import argparse
            import csv
            from collections import defaultdict

            parser = argparse.ArgumentParser(description="Sum a CSV column per group.")
            parser.add_argument("file")
            parser.add_argument("--group", default="region")
            parser.add_argument("--column", default="amount")
            args = parser.parse_args()

            totals = defaultdict(float)
            with open(args.file, newline="") as f:
                for row in csv.DictReader(f):
                    totals[row[args.group]] += float(row[args.column])

            for group, total in sorted(totals.items()):
                print(f"{group:<10} {total:>12,.2f}")

      .. example-part:: command

         .. code:: bash

            python -m nuitka --mode=onefile csvsum.py

      .. example-part:: output
         :columns:

         .. code:: text

            csvsum/
            ├── csvsum.py
            ├── csvsum.exe     <- new
            └── sales.csv

         .. program-output::

            Nuitka: Running C compilation via Scons.
            Nuitka-Onefile: Creating single file from dist folder, this may take a while.
            Nuitka: Successfully created 'csvsum.exe'.

      .. example-part:: run

         .. code:: bash

            csvsum.exe sales.csv --column amount

         .. program-output::

            North          1,560.25
            South          1,396.25
            West           2,045.00

   .. tab-item:: Desktop GUI

      A Qt program with an icon and no console window. The plugin for
      your Qt binding makes sure the Qt plugins, translations, and
      libraries it needs are included.

      .. example-part:: input
         :columns:

         .. code:: text

            notes/
            ├── notes.py
            └── notes.ico

         .. code:: python

            import sys

            from PySide6.QtWidgets import (
                QApplication, QMainWindow, QPlainTextEdit)


            def main():
                app = QApplication(sys.argv)
                window = QMainWindow()
                window.setWindowTitle("Notes")
                window.setCentralWidget(QPlainTextEdit())
                window.resize(480, 320)
                window.show()
                return app.exec()


            if __name__ == "__main__":
                sys.exit(main())

      .. example-part:: command

         .. code:: bash

            python -m nuitka --mode=app --enable-plugins=pyside6 --windows-console-mode=disable --windows-icon-from-ico=notes.ico notes.py

      .. example-part:: output
         :columns:

         .. code:: text

            notes/
            ├── notes.py
            ├── notes.ico
            └── notes.exe      <- new, with icon

         .. program-output::

            Nuitka-Plugins:pyside6: Including Qt plugins 'iconengines,imageformats,platforms,styles,tls' below 'PySide6\qt-plugins'.
            Nuitka-Onefile: Creating single file from dist folder, this may take a while.
            Nuitka: Successfully created 'notes.exe'.

      .. example-part:: run

         Double-click ``notes.exe``. The Notes window opens, with no
         console window behind it. On macOS, the same command creates
         ``notes.app``, use ``--macos-app-icon`` for its icon.

   .. tab-item:: Data files

      A program that reads files that are not Python code, here a
      template and a configuration. Nuitka includes only code by
      default, so you name the data files. Locate them relative to
      ``__file__``, which works in Python and in every Nuitka mode.

      .. example-part:: input
         :columns:

         .. code:: text

            report/
            ├── report.py
            ├── config.json
            └── templates/
                └── report.html

         .. code:: python

            import json
            import os
            from string import Template

            HERE = os.path.dirname(__file__)


            def main():
                with open(os.path.join(HERE, "config.json")) as f:
                    config = json.load(f)
                with open(os.path.join(HERE, "templates", "report.html")) as f:
                    page = Template(f.read()).substitute(config)

                with open("report.html", "w") as f:
                    f.write(page)
                print("Wrote report.html for", config["company"])


            if __name__ == "__main__":
                main()

      .. example-part:: command

         .. code:: bash

            python -m nuitka --mode=standalone --include-data-dir=templates=templates --include-data-files=config.json=config.json report.py

      .. example-part:: output
         :columns:

         .. code:: text

            report.dist/       <- new, copy this folder
            ├── report.exe
            ├── config.json
            ├── templates/
            │   └── report.html
            ├── python313.dll
            └── ...

         .. program-output::

            Nuitka: Running C compilation via Scons.
            Nuitka: Successfully created 'report.dist\report.exe'.

      .. example-part:: run

         .. code:: bash

            report.dist\report.exe

         .. program-output::

            Wrote report.html for ACME Industrial

      Files that users edit after installation should live next to the
      program instead, see :ref:`onefile-finding-files`.

   .. tab-item:: Data science

      NumPy and pandas need no options. Their special needs are covered
      by the package configuration that comes with Nuitka. Compile from
      a virtual environment that contains only what the program uses,
      otherwise everything that gets imported is included too.

      .. example-part:: input
         :columns:

         .. code:: text

            forecast/
            ├── forecast.py
            └── sales.csv       (one row per sale)

         .. code:: python

            import numpy as np
            import pandas as pd


            def main():
                sales = pd.read_csv("sales.csv", parse_dates=["date"])
                daily = sales.groupby("date")["amount"].sum()

                days = np.arange(len(daily))
                slope, offset = np.polyfit(days, daily.to_numpy(), 1)
                nxt = slope * len(daily) + offset

                print(f"{len(daily)} days, trend {slope:+.2f} per day")
                print(f"Forecast for next day: {nxt:.2f}")


            if __name__ == "__main__":
                main()

      .. example-part:: command

         .. code:: bash

            python -m venv venv
            venv\Scripts\python -m pip install Nuitka numpy pandas
            venv\Scripts\python -m nuitka --mode=standalone forecast.py

      .. example-part:: output
         :columns:

         .. code:: text

            forecast.dist/     <- new
            ├── forecast.exe
            ├── numpy/
            ├── pandas/
            └── ...

         .. program-output::

            Nuitka: Completed Python level compilation and optimization.
            Nuitka: Running C compilation via Scons.
            Nuitka: Successfully created 'forecast.dist\forecast.exe'.

      .. example-part:: run

         .. code:: bash

            forecast.dist\forecast.exe

         .. program-output::

            5 days, trend +83.51 per day
            Forecast for next day: 2666.12

   .. tab-item:: Web service

      A small Flask service, served by Waitress, that runs on a server
      without Python installed. Templates are data files, so they are
      included like in the data files example.

      .. example-part:: input
         :columns:

         .. code:: text

            status/
            ├── status.py
            └── templates/
                └── index.html

         .. code:: python

            import platform

            from flask import Flask, render_template
            from waitress import serve

            app = Flask(__name__)


            @app.route("/")
            def index():
                return render_template(
                    "index.html", host=platform.node())


            if __name__ == "__main__":
                print("Serving on http://0.0.0.0:8000")
                serve(app, host="0.0.0.0", port=8000)

      .. example-part:: command

         .. code:: bash

            python -m nuitka --mode=standalone --include-data-dir=templates=templates status.py

      .. example-part:: output
         :columns:

         .. code:: text

            status.dist/       <- new
            ├── status.exe
            ├── templates/
            │   └── index.html
            └── ...

         .. program-output::

            Nuitka: Running C compilation via Scons.
            Nuitka: Successfully created 'status.dist\status.exe'.

      .. example-part:: run

         .. code:: bash

            status.dist\status.exe

         .. program-output::

            Serving on http://0.0.0.0:8000

      Opening ``http://<server>:8000`` in a browser shows the page
      rendered from ``templates/index.html``. Copy ``status.dist`` to the
      server, or into a slim container image, and start it from a
      service manager.

   .. tab-item:: Faster module

      Keep your Python program as it is and compile only one module,
      e.g. the one with the hot loop or the logic you do not want to
      ship as source. The rest of the program imports it like before.

      .. example-part:: input
         :columns:

         .. code:: text

            shop/
            ├── main.py
            └── pricing.py

         .. code:: python

            def net_price(gross, discount, tax_rate):
                price = gross * (1 - discount)
                return round(price * (1 + tax_rate), 2)


            def price_list(items, discount=0.05, tax_rate=0.19):
                return [net_price(gross, discount, tax_rate)
                        for gross in items]

      .. example-part:: command

         .. code:: bash

            python -m nuitka --mode=module pricing.py

      .. example-part:: output
         :columns:

         .. code:: text

            shop/
            ├── main.py
            ├── pricing.py
            ├── pricing.cp313-win_amd64.pyd  <- new
            └── pricing.pyi                  <- new, for editors

         .. program-output::

            Nuitka: Running C compilation via Scons.
            Nuitka: Successfully created 'pricing.cp313-win_amd64.pyd'.

      .. example-part:: run

         .. code:: bash

            python -c "import pricing; print(pricing.price_list([100, 250, 19.99]))"

         .. program-output::

            [113.05, 282.62, 22.6]

      Python prefers the compiled module over ``pricing.py`` in the same
      folder. It works only with the Python version it was compiled
      for, here 3.13.

*******************************
 Keep the options in your code
*******************************

Once a command works, put its options into the main file as comments.
Then ``python -m nuitka notes.py`` is all anybody needs to type, and the
options are kept with the code in version control. Options can depend on
the system, too.

.. code:: python

   # nuitka-project: --mode=app
   # nuitka-project: --enable-plugins=pyside6
   # nuitka-project-if: {OS} == "Windows":
   #    nuitka-project: --windows-console-mode=disable
   #    nuitka-project: --windows-icon-from-ico=notes.ico

   import sys

   from PySide6.QtWidgets import QApplication, QMainWindow

All forms are explained in :ref:`nuitka-project-options`.

***************************
 When something goes wrong
***************************

.. list-table::
   :header-rows: 1
   :widths: 35 65

   -  -  What you see
      -  What to do

   -  -  ``FileNotFoundError`` for a file that is not Python code

      -  The data file is not included. Add it with
         ``--include-data-dir`` or ``--include-data-files``, for a
         package's own files use ``--include-package-data``. See
         :ref:`data-files`.

   -  -  ``ModuleNotFoundError`` when the program runs

      -  The module is imported in a way Nuitka cannot see, e.g. by a
         name in a string. Add ``--include-module=name`` or
         ``--include-package=name``.

   -  -  A program built with ``--windows-console-mode=disable`` closes
         without a message
      -  The error went to the console that is disabled. Build once
         without that option to read it.

   -  -  The program works in standalone, but not in onefile
      -  Usually a file is searched next to the program. Read
         :ref:`onefile-finding-files`.

   -  -  You want to know what was included and why
      -  Add ``--report=compilation-report.xml`` and open the file. It
         is also what we ask for in bug reports.

**************
 Getting Help
**************

-  :doc:`/user-documentation/tutorial-setup-and-build` explains the
   setup in more detail, e.g. how to get a C compiler on Windows.

-  :doc:`/pages/support` lists the chat rooms and the issue tracker. The
   volunteers on the `Discord server <https://discord.gg/nZ9hr9tUck>`_
   help with first steps and questions.

-  :doc:`/user-documentation/common-issue-solutions` covers typical
   problems.

.. include:: ../variables.inc
