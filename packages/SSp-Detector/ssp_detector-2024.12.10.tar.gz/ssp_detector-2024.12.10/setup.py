#  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#   Copyright (c) 2024. Simon J. Guillot. All rights reserved.                            +
#   Redistribution and use in source and binary forms, with or without modification, are strictly prohibited.
#                                                                                         +
#   THIS CODE IS PROVIDED BY THE COPYRIGHT HOLDER "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
#   BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#   IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
#   OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#   DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
#   STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS CODE,
#   EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

try:
    import io
    import os
    from setuptools import setup

    _has_setuptools = True
except ImportError:
    from distutils.core import setup
path = os.path.abspath(os.path.dirname(__name__))

DISTNAME = "SSp_Detector"
VERSION = "2024.12.10"
if not VERSION:
    pr = DISTNAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(path, pr, pr, "__version__.py")) as v:
        VERSION = "\n" + v.read()
else:
    VERSION = VERSION
DESCRIPTION = "Sleep spindles detector"
try:
    with io.open(os.path.join(path, "SSp_Detector\README.md"), encoding="utf-8") as f:
        LONG_DESCRIPTION = "\n" + f.read()
except FileNotFoundError:
    LONG_DESCRIPTION = (
        "SSp_Detector: open-source Python package to detect sleep spindles using absolute or relative "
        "power."
    )
DESCRIPTION_CONTENT_TYPE = "text/markdown"
URL = "https://github.com/sjg2203/SSp_Detector"
MAINTAINER = "Simon J. Guillot"
MAINTAINER_EMAIL = "simon.guillot@inserm.fr"
LICENSE = "Apache 2.0 license"
PACKAGES = ["SSp_Detector"]
INSTALL_REQUIRES = [
    "mne>=1.5.1",
    "outdated",
    "numpy>=1.24.3",
    "pandas>=2.0.0",
    "scipy>=1.11",
]
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: Unix",
    "Operating System :: MacOS",
    "Operating System :: Microsoft :: Windows",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

if __name__ == "__main__":
    setup(
        name=DISTNAME,
        author=MAINTAINER,
        author_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type=DESCRIPTION_CONTENT_TYPE,
        license=LICENSE,
        url=URL,
        version=VERSION,
        install_requires=INSTALL_REQUIRES,
        packages=PACKAGES,
        classifiers=CLASSIFIERS,
    )
