################
 Nuitka Website
################

********
 Thanks
********

This is how https://nuitka.net is built.

Please help and improve this in all ways, typos, better looks, more
information, etc. all is appreciated and necessary. There is very
extensive information available at
https://nuitka.net/pages/website-manual.html with all the details

Right now, this is very much possible to improve in so many ways. Your
turn!

********
Tests
********

This project includes **visual regression tests** to ensure
the UI remains consistent across changes.

Golden Images
=============

Golden images act as the **baseline reference** for visual comparisons.

Generate Golden Images
----------------------

Golden images can now be generated either **locally** or via **GitHub Actions CI**.

**Local (CLI) Method:**

.. code-block:: bash
   python update.py --update-golden \
     --browsers chromium,firefox,webkit \
     --devices desktop,mobile \
     --pages home,about \
     --wait 1000 \
     --clean \
     --verbose

**CI Method (GitHub Actions):**

The `Update Golden Images` workflow automatically runs on pushes to main branches
or can be triggered manually to update the golden images in CI.

- The workflow uses **matrix combinations** of browsers (Chromium, Firefox, WebKit) and devices (desktop, mobile).
- Generated golden images are **cached** for faster subsequent test runs.
- A backup of golden images is uploaded as an **artifact** with 90-day retention.

Trigger the workflow manually in GitHub under **Actions → Update Golden Images → Run workflow**,
or via GitHub CLI:

.. code-block:: bash
   gh workflow run "Update Golden Images" --ref <branch> \
     -f browsers="chromium,firefox,webkit" \
     -f devices="desktop,mobile" \
     -f pages="all"

CLI Options
-----------

- ``--browsers`` → Browsers to test (Chromium, Firefox, WebKit)
- ``--devices`` → Viewports (desktop, mobile)
- ``--pages`` → Pages to capture (e.g., ``home,about``)
- ``--wait`` → Delay (in ms) before taking the screenshot
- ``--clean`` → Remove old screenshots before generating
- ``--verbose`` → Enable detailed logging

Running Tests
=============

All tests are executed with **pytest**:

.. code-block:: bash
   pytest tests/regression.py -v

Make sure to run this inside your **pipenv shell**.

Test Output
===========

The following directories are created when running tests:

- **CURRENT_DIR** → Latest screenshots from the test run
- **DIFF_DIR** → Visual diffs highlighting failed comparisons
- **GOLDEN_DIR** → Baseline golden reference images