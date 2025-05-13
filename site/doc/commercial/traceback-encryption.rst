:orphan:

######################
 Traceback Encryption
######################

When distributing a closed-source Python application, one of your
primary concerns is protecting your intellectual property. Standard
Python tracebacks, while invaluable for debugging, can inadvertently
reveal sensitive information about your code's internal structure, such
as file names, function names, line numbers, and even variable contents
in some contexts. This is something you typically want to avoid exposing
to end-users.

Additionally, presenting raw, technical tracebacks to users can be
confusing, unprofessional, and might even give them an incorrect
impression of your software's stability or quality.

**Nuitka Commercial's Traceback Encryption** feature elegantly solves
these problems.

It allows your compiled application to output encrypted tracebacks when
an unhandled exception occurs. To the end-user, this appears as an
opaque block of text, revealing nothing about your application's
internals. However, you, the developer, possess the key to decrypt this
block and retrieve the original, fully detailed traceback, enabling you
to diagnose and fix the issue effectively.

***************************************
 Benefits for Closed-Source Developers
***************************************

-  **Intellectual Property Protection**: Prevents end-users from
   gleaning insights into your proprietary code structure and logic from
   error messages.

-  **Professional User Experience**: Users are shielded from complex and
   potentially intimidating technical error dumps. Instead, they see a
   clean, encrypted string which they can forward to your support team.

-  **Undiminished Debugging Capability**: You retain full access to the
   detailed traceback information necessary for efficient debugging,
   just as if it were an unencrypted Python traceback.

-  **Controlled Information Disclosure**: Only individuals with the
   decryption key can access the sensitive details of the error,
   ensuring that this information remains within your organization.

**********
 Features
**********

You can decide to encrypt standard output, standard error, or only
tracebacks. The below examples encrypt all outputs, but you may allow
for mixed output, where only the tracebacks will be encrypted.

***************************
 How it Works - An Example
***************************

Consider a simple test program compiled with Nuitka Commercial and
traceback encryption enabled.

If this program encounters an error, instead of printing a standard
Python traceback, it will output something like this (the exact output
will vary):

.. code:: text

   Z-OeD9p76EpDzsVvSrLTwMM3q+VYLbvtEi9hJoeP8WgnPEnIEaQ8uxd2+wweKa2ljjBOPJkJpFG79io2utHh4tA4RqR95s4SDuDg==-A
   Z-D7a/0aXLl6YB1OrSA6ojlRg0zLcAqrhyo7uYLounqzgxmF+BMhwqqbgGLi9bSOg4-A
   X-gGUh2JbMEewix6kRRcxNJUR0OFLDYOZ8vnfwk2odAlwRHUhiHH/QL/8QGIoodhW3RpoKsjFNAd8IgusbWL2aRgyn0J8mbeVq/TNY-Y
   ... (and so on for each line of the original traceback)

This encrypted output can then be sent back to you. Using the decryption
key (e.g., `TracebackEncryptionTest.bin.key` in this example) and a
Nuitka utility, you can easily decode it:

.. code:: bash

   cat out.txt | python -m nuitka.tools.commercial.decrypt --key=TracebackEncryptionTest.bin.key

This will reveal the original traceback:

.. code:: text

   Lets also do stderr world

   Hello encrypted stdout world we got interrupted
   Got an exception: secret
   Traceback (most recent call last):
   File "TracebackEncryptionTest.py", line 24, in <module>
      f()
   File "TracebackEncryptionTest.py", line 21, in f
      raise KeyError(2)
   KeyError: 2

As you can see, the full context of the error, including file paths,
line numbers, and the exception type, is perfectly preserved for your
analysis, while remaining hidden from the end-user.

Nuitka Commercial currently supports symmetric encryption for
tracebacks, with plans to introduce asymmetric encryption in future
updates, offering even more flexibility in key management.

This feature is a crucial component for any developer looking to
distribute professional, secure, and robust Python applications while
safeguarding their valuable code.

***********************************
 Example Usage (from Nuitka tests)
***********************************

The following demonstrates compiling a test script, running it to
produce encrypted output, and then decrypting that output.

.. note::

   The `--force-stdout-spec` and `--force-stderr-spec` options mentioned
   in the example below are related to how Nuitka handles output streams
   and can be used to ensure all output, including tracebacks, is
   directed in a way that's making it easy to capture.

   The key file (e.g., `TracebackEncryptionTest.bin.key`) is generated
   during the Nuitka compilation process when traceback encryption is
   active. You must securely store this key to be able to decrypt
   tracebacks later.

The actual example execution:

----

.. code::

   python -m nuitka -plugin=traceback-encryption --encrypt-stderr --encrypt-stdout TracebackEncryptionTest.py

   # Run it, could also have --force-stdout-spec and --force-stderr-spec outputs used
    ./TracebackEncryptionTest.bin >out.txt 2>&1

   cat out.txt
   Z-OeD9p76EpDzsVvSrLTwMM3q+VYLbvtEi9hJoeP8WgnPEnIEaQ8uxd2+wweKa2ljjBOPJkJpFG79io2utHh4tA4RqR95s4SDuDg==-A
   Z-D7a/0aXLl6YB1OrSA6ojlRg0zLcAqrhyo7uYLounqzgxmF+BMhwqqbgGLi9bSOg4-A
   X-gGUh2JbMEewix6kRRcxNJUR0OFLDYOZ8vnfwk2odAlwRHUhiHH/QL/8QGIoodhW3RpoKsjFNAd8IgusbWL2aRgyn0J8mbeVq/TNY-Y
   X-KUm3etPVNdjaIA+VnJuNIOs8T7owi92TeQ3tYb2RzFljgsu2HJd1oiVS6dWNGEY=-Y
   X-NDtWFWpk5X1qva9SJwtn38g3L388w+WdCyaFRHZRG4Y4sfOX8JshYNs2o0WnxPctctHO991iPsYiHEdTu8EM4+4=-Y
   X-61h/DnsybZYxq1/MvLiQwXojrbIRaL97pgm45mQe/YPcBW0j9zYRIKUA49Q41N2T-Y
   X-fzO3OVAx+ugM6DnDXhlI/8KU4/lFbym4N9DzBy4xoxv+hNshIWw+y4pTlD9QAVGlUnwp+cR9Ry+k8fG/4vkOmA==-Y
   X-QXJO5o0V+i9XKGVYynMkleP3WCgrmaYImVHdR9JDPIL2GPgf6ezqaiYJy8fj5+Y0-Y
   X-ZRfYUYBbFKRbHZyCTlSnCYBzcWAcCkmeyn0XRd1zXjxcUzKtLtz5+uXgByWoLCWnhLccbSk=-Y
   X-ps7BFw5jxIpxsXRgvVb1BuxuKXt8a1PoppbgaZDPNRf/7z2ZD07AWVa/5Yv+tvqo-Y
   Z-3BG9tSlX/4veoI6PQTES5r4R0v3Zw8gkMlbd27JniqKiC1i7jpvk0aJ7+kuqErVT4eZELLtCarlYPkwpOfKNHn0RbkouvUoA0U3TW42/VIpR4CkXkhXdvQy1g2M6JXSA4qoV3InY0kqUgQlZhZxDk+LoOqqCTjYz4gjJezRs4tKIjXKL6Jff8ennY1YZshEVXtb2bZ9EEAtOZSAhhejITJYTvuMowErKeOw6NPcjPk42u2wtzYKhcRhuzUbCRd3j8Z+Zfbl/Ms7DQuytxoY3oTBbQhiwE0LDzqsksi19EOg7IuRvQ1dFoj6Jmw+VVwOkTZBO35HJ8BTdnVWBnfiBEJ5Z2tS+nnzgT0uOHpUDdgCw8VNgnG5htdiREqEL6zDPfr+ZQ3JkIDtnc+VDytYki3ZeBGQBCFkJHWgl7rcbcl/HdGIaBTYOhjZiU+V/iCZN6HPOHrPVdMPNoiHXJub1d/Ad3xWLtgXwExpqx4mzw1HET8MpeOowhq7m5+piNDGCA6DaM21HZwuxqoqNrEzhKddi+xdQ42v5OCw5Bh7pzG4H4sVDA7gC+MJ3f+7oZIPac+jnLYRABjnud0SYf6LMxL2QRIAUImLUnraqZL19me1lf8X0Scb70GTAGeoZGMind+EMlhJ5eegTjvapdrfifWc1j35nWsk4yC7D33WmWcbzDAn1uJAwT34rM2E7ytoXCB5Kayth//bop2MAyFOlNWJOthpr1q39w8p3YuOuH5stNV+GHdWHw1pYK4yvjWd1/XIEuxK+iczuRBgyFwpwFwr/u6TDWfTrEI36OKExOtS6OnUUwra6kBNYfJZJ/+uPoyA18GY5lSD1DgZzTdVdOhFfG4gRDXxjgR0YwukHOtzv4o9lJIBccESnGYVz+PEvUzMKUEoMHnPBxvfhg6fD1AsmbVezfe1q0nB60ItX3EnCWH+fr6F5CmGnXqangVHuYnrgtsyK8Da+46sOOTUPStWcIXQkjhp4MuPp+JpMXSoLNYLL23uaP7MtHTsgZI8Fs5aPoUVcTv6obGdaB1bA9b/pe93i3GFYbFBHxUe8tGnntBgXkhi1sEj/V5Z2/o8dRuM7Xr5hpPEGBjVbqdXHGqsyoWVnZMMDksjzrzq/fzunIkQwBnGeByqjy8TDK117mz9kT0Wc1dWS0utbZ8Wecx5xWbmrz3prFzr5+1xyJK1zLv1TiilXqU1jgVGQISfeTWttm5OxQWVZY1s+7IRoVJTYFypyIm4epuKM-A

   cat out.txt | python -m nuitka.tools.commercial.decrypt --key=TracebackEncryptionTest.bin.key
   Lets also do stderr world

   Hello encrypted stdout world we got interrupted
   Got an exception: secret
   Traceback (most recent call last):
   File "~/repos/Nuitka/TracebackEncryptionTest.py", line 24, in <module>
      f()
   File "~/repos/Nuitka/TracebackEncryptionTest.py", line 21, in f
      raise KeyError(2)
   KeyError: 2


Go `back to Nuitka commercial
</doc/commercial.html#protection-vs-reverse-engineering>`__ overview to
learn about more features or to subscribe to `Nuitka commercial
</doc/commercial.html#pricing>`__.
