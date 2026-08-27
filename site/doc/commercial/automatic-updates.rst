:orphan:

###################
 Automatic Updates
###################

The ``automatic-updates`` plugin enables your compiled binary to
automatically check for and download updates upon startup. It is
currently supported for **onefile mode** (using the Onefile Bootstrap
binary).

.. important::

   Standalone distributions and macOS app-bundles are not yet supported,
   but we are working on that.

**************
 How It Works
**************

You enable the plugin and specify the URL from which to fetch the update
configuration:

.. code:: bash

   python -m nuitka --mode=onefile --enable-plugin=automatic-updates --automatic-update-url="https://yourdomain.com/update.toml" your_program.py

The URL must point to a TOML file that contains the download URL and the
CRC32 checksum of the new executable. The compiled program will fetch
this TOML file in a background thread upon startup, verify the CRC32,
and if a newer version is available, it will transparently download and
replace the running executable.

When the update is completed, the binary will be swapped on disk so that
the next time the user launches the application, they will be running
the updated version.

********************
 update.toml Format
********************

Example ``update.toml`` format:

.. code:: toml

   url = "https://yourdomain.com/downloads/your_program_v2.exe"
   crc32 = 123456789

****************************************
 Automatically Generating the TOML File
****************************************

Instead of creating the ``update.toml`` file manually and figuring out
the binary's CRC32 checksum on your own, you can have Nuitka generate
the configuration file for you during the build. By providing the
desired TOML output file path, the plugin will compute the exact CRC32
checksum of your compiled binary and write the complete TOML config:

.. code:: bash

   python -m nuitka --mode=onefile --enable-plugin=automatic-updates \
       --automatic-update-url="https://yourdomain.com/update.toml" \
       --auto-update-toml-file=update.toml \
       your_program.py

******************************
 URL Specs with ``{VERSION}``
******************************

You can use the ``{VERSION}`` tag in the URL, which Nuitka resolves at
runtime to your file version. This gives you full flexibility in
structuring your update infrastructure:

.. code:: bash

   --auto-update-url-spec=http://yourdomain.com/{VERSION}/update.toml

***************
 Complete Demo
***************

#. Ensure you have a local HTTP server running to serve the update
   files:

   .. code:: bash

      rm -rf auto-update-test
      mkdir auto-update-test
      python -m http.server --bind localhost --dir auto-update-test 27272

#. Compile the initial executable (Version 1.0) and configure it to look
   for updates on the local server:

   .. code:: bash

      python -m nuitka --mode=onefile --file-version=1.0 \
          --force-runtime-environment-variable=FILE_VERSION=1.0 \
          --output-dir=auto-update-test/1.0 \
          --enable-plugin=automatic-updates \
          --auto-update-url-spec=http://localhost:27272/{VERSION}/update.toml \
          --auto-update-toml-file=auto-update-test/1.0/update.toml \
          --auto-update-debug \
          AutoUpdatingTest.py

   .. note::

      We use ``--force-runtime-environment-variable`` to force
      ``FILE_VERSION`` for demonstration purposes. This is not required
      for the auto-update feature itself.

#. Compile the updated executable (Version 1.1):

   .. code:: bash

      python -m nuitka --mode=onefile --file-version=1.1 \
          --force-runtime-environment-variable=FILE_VERSION=1.1 \
          --output-dir=auto-update-test/1.1 \
          --enable-plugin=automatic-updates \
          --auto-update-url-spec=http://localhost:27272/{VERSION}/update.toml \
          --auto-update-toml-file=auto-update-test/1.1/update.toml \
          --auto-update-debug \
          AutoUpdatingTest.py

#. Copy the 1.0 binary into the current directory and run it. V1.0
   initially does not update because the configuration points to itself:

   .. code:: bash

      cp auto-update-test/1.0/AutoUpdatingTest.bin .
      ./AutoUpdatingTest.bin

   Output:

   .. code:: text

      AUTO UPDATE: Thread started.
      AUTO UPDATE: Expanded info URL to 'http://localhost:27272/1.0/update.toml'.
      AUTO UPDATE: CRC32 http://localhost:27272/1.0/AutoUpdatingTest.bin matches already.
      This is version 1.0

#. Copy the 1.1 update config into the 1.0 directory and re-run:

   .. code:: bash

      cp auto-update-test/1.1/update.toml auto-update-test/1.0/update.toml
      ./AutoUpdatingTest.bin

   Output:

   .. code:: text

      AUTO UPDATE: Thread started.
      AUTO UPDATE: Expanded info URL to 'http://localhost:27272/1.0/update.toml'.
      AUTO UPDATE: URL to check 'http://localhost:27272/1.1/AutoUpdatingTest.bin'.
      AUTO UPDATE: Downloaded to '/dev/fd/4' .
      AUTO UPDATE: May not yet update.
      This is version 1.0
      AUTO UPDATE: May update.
      AUTO UPDATE: Updated.

   On the next launch, the binary is already updated:

   .. code:: text

      AUTO UPDATE: Thread started.
      AUTO UPDATE: Expanded info URL to 'http://localhost:27272/1.1/update.toml'.
      AUTO UPDATE: CRC32 http://localhost:27272/1.1/AutoUpdatingTest.bin matches already.
      This is version 1.1

*******************
 Debugging Updates
*******************

Use ``--auto-update-debug`` during compilation to enable debug traces
that show the update thread's activity, URLs being fetched, and whether
updates were found or applied.

Go `back to Nuitka Commercial </doc/commercial.html#convenience>`__
overview to learn about more features or to subscribe to `Nuitka
Commercial </doc/commercial.html#pricing>`__.
