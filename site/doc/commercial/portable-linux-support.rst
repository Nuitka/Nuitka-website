:orphan:

########################
 Portable Linux Support
########################

Building a Linux standalone binary that runs on other Linux
distributions is challenging. On Linux, compiled software is typically
linked against specific versions of system libraries such as glibc, and
the binary will refuse to run on an older version.

**Nuitka Commercial** solves this with a **container-based build tool**
that produces truly portable Linux binaries.

**************
 How It Works
**************

The container uses **CentOS 7** (based on Fedora 19) as the build
environment. Software compiled here will run on practically any modern
Linux distribution — from older LTS releases to the latest Fedora or
Ubuntu — because it links against the oldest realistic set of system
libraries.

The container runs via **Podman**, which operates without root
privileges or a persistent daemon, making it lightweight and secure to
set up.

Inside the container, Nuitka uses an improved C toolchain from EPEL and
SCL, providing a modern compiler that produces better-optimized code
than the default CentOS 7 toolchain. Python is built from source with
options tuned for Nuitka, including static linking support.

Your source code and build directory are mounted into the container, and
the build output lands in your build directory on the host — identical
to a local Nuitka compilation, but portable across Linux distributions.

The tool automatically handles Python version selection, pip dependency
installation, and optional wheel packages. A custom ``requirements.txt``
can be provided for project-specific dependencies.

Go `back to Nuitka commercial
</doc/commercial.html#older-oses-and-special-needs>`__ overview to learn
about more features or to subscribe to `Nuitka commercial
</doc/commercial.html#pricing>`__.
