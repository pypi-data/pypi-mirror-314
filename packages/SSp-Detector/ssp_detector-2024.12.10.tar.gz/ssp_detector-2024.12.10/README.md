# Sleep Spindles Detector
<img src="./docs/SSp_Detector_logo.png" width="300"/>

[![PyPI - Version](https://img.shields.io/pypi/v/SSp_Detector?logo=pypi)](https://pypi.python.org/pypi/SSp-Detector)
[![Conda (channel only)](https://img.shields.io/conda/vn/conda-forge/SSp_Detector?logo=anaconda&color=green)](https://anaconda.org/conda-forge/SSp_Detector)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/SSp-Detector.svg?logo=python)](https://pypi.python.org/pypi/SSp-Detector)
[![License](https://img.shields.io/github/license/sjg2203/SSp_Detector?logo=apache)](https://github.com/sjg2203/SSp_Detector/blob/main/LICENSE)
[![Security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![PyPI - Status](https://img.shields.io/pypi/status/SSp_Detector)](https://pypi.python.org/pypi/SSp-Detector)
[![Hit](https://img.shields.io/endpoint?url=https%3A%2F%2Fhits.dwyl.com%2Fsjg2203%2FSSp_Detector.svg&color=red)](http://hits.dwyl.com/sjg2203/SSp_Detector)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

[Sleep Spindles Detector](https://github.com/sjg2203/SSp_Detector) toolbox analyses raw EEG signals to then extrapolate the number of sleep spindles using either the absolute or relative Sigma power (11-16Hz).

The toolbox is optimised for Python 3.10 and above and was tested on both Windows and macOS ARM.

> [!NOTE]
> All dependencies are listed in [requirements](requirements.txt), Python 3.10 minimum.

## Citation [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10066031.svg)](https://doi.org/10.5281/zenodo.10066031)

If you use this toolbox, please cite as followed:

 - Guillot, S.J.<a id="cy-effective-orcid-url" class="underline" href="https://orcid.org/0000-0002-1623-7091" target="orcid.widget" rel="me noopener noreferrer" style="vertical-align: top"><img src="https://orcid.org/sites/default/files/images/orcid_16x16.png" style="width: 1em; margin-inline-start: 0.5em" alt="ORCID"/></a> (2023). Sleep spindles detector (2024.12.10). GitHub, Zenodo. https://doi.org/10.5281/zenodo.10066031

## Contribution [![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/sjg2203/SSp_Detector/issues)

These pipelines were created and is maintained by SJG.

Contributions are more than welcome so feel free to submit a [pull request](https://github.com/sjg2203/SSp_Detector/pulls)!

To report a bug, please open a new [issue](https://github.com/sjg2203/SSp_Detector/issues).

Note that this program is provided with NO WARRANTY OF ANY KIND under Apache 2.0 [license](LICENSE).

## Installation of Python package

To install the toolbox, simply use:

- Using conda [![Board Status](https://dev.azure.com/conda-forge/feedstock-builds/_apis/build/status/ssp_detector-feedstock?branchName=main)](https://anaconda.org/conda-forge/ssp_detector)

```python
conda install -c cf-staging ssp_detector
```

- Using pip [![Pypi package](https://github.com/sjg2203/SSp_Detector/actions/workflows/pypi_publish.yml/badge.svg?branch=main)](https://github.com/sjg2203/SSp_Detector/actions/workflows/pypi_publish.yml) [![PyPI - Wheel](https://img.shields.io/pypi/wheel/SSp_Detector)](https://pypi.python.org/pypi/SSp-Detector)

```python
pip install ssp_detector
```

Everything worked if the following command do not return any error:

```python
import mne
from ssp_detector import spindles_abs
from ssp_detector import spindles_rel
from tkinter import filedialog as fd

#Load an EDF file using MNE
edf=fd.askopenfilename(title='SELECT EDF FILE',filetypes=(("EDF files","*.edf"),("all files","*.*")))
raw=mne.io.read_raw_edf(edf,preload=True)
sfreq=raw.info['sfreq']

#Return sleep spindles count
spindles_abs(raw,sf=sfreq,thresh={'abs_pow':1.25})
spindles_rel(raw,sf=sfreq,thresh={'rel_pow':0.2})
```

Absolute Sigma power formula:
```math
P_{abs\sigma}(dB)=log10(\tfrac{\int_{11}^{16}\left|x(t)\right|^{2}dt}{\int_{0.1}^{45}\left|x(t)\right|^{2}dt})$
log10(\tfrac{\int_{11}^{16}\left|x(t)\right|^{2}dt}{\int_{0.5}^{4}\left|x(t)\right|^{2}dt})
```

Relative Sigma power formula:
```math
P_{rel\sigma}(dB)=log10(\tfrac{\int_{11}^{16}\left|x(t)\right|^{2}dt}{\int_{0.1}^{45}\left|x(t)\right|^{2}dt})$
log10(\tfrac{\int_{11}^{16}\left|x(t)\right|^{2}dt}{\int_{0.1}^{45}\left|x(t)\right|^{2}dt})
```
