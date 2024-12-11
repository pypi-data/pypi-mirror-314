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

import os

from outdated import warn_if_outdated

from .ssp_detector import *

path = os.path.abspath(os.path.dirname(__name__))

# Define logger
logging.basicConfig(
    format="%(asctime)s|%(levelname)s|%(message)", datefmt="%y-%b-%d %H:%M:%S"
)

__author__ = "Simon J. Guillot <simon.guillot@inserm.fr>"
DISTNAME = "SSp_Detector"
VERSION = "2024.12.10"
if not VERSION:
    pr = DISTNAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(path, pr, pr, "__version__.py")) as v:
        VERSION = "\n" + v.read()
else:
    VERSION = VERSION
__version__ = VERSION

# Warn if newer version is available
warn_if_outdated("SSp_Detector", __version__)
