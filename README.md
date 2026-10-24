[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14976788.svg)](https://doi.org/10.5281/zenodo.14976788)
[![Release](https://img.shields.io/github/v/release/matthiaskoenig/tirzepatide-model)](https://github.com/matthiaskoenig/tirzepatide-model/releases)
[![Documentation](https://github.com/matthiaskoenig/tirzepatide-model/actions/workflows/docs.yml/badge.svg)](https://matthiaskoenig.github.io/tirzepatide-model/)
[![CI](https://github.com/matthiaskoenig/tirzepatide-model/actions/workflows/ci.yml/badge.svg)](https://github.com/matthiaskoenig/tirzepatide-model/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/docker/v/matthiaskoenig/tirzepatide?sort=semver&label=docker)](https://hub.docker.com/r/matthiaskoenig/tirzepatide)
[![Python](https://img.shields.io/badge/python-3.14-blue)](https://www.python.org)
[![Code license: MIT](https://img.shields.io/badge/code%20license-MIT-blue)](https://opensource.org/license/MIT)
[![Model license: CC BY-SA 4.0](https://img.shields.io/badge/model%20license-CC%20BY--SA%204.0-lightgrey)](https://creativecommons.org/licenses/by-sa/4.0/)

# Physiologically based pharmacokinetic (PBPK) model of tirzepatide

This repository provides the tirzepatide physiologically based pharmacokinetic (PBPK) model: the subcutaneous absorption of tirzepatide, its distribution with albumin into the interstitial space, its proteolytic cleavage, the distribution of its metabolites into a slow tissue pool and their excretion in the urine and the feces.

Documentation: <https://matthiaskoenig.github.io/tirzepatide-model/>

## Quick start

```bash
git clone https://github.com/matthiaskoenig/tirzepatide-model.git && cd tirzepatide-model
uv sync
uv run run_simulation pkdb_models.models.tirzepatide --action all -r results
```

## How to cite

> Mishra, A. & König, M. (2026). *Physiologically based pharmacokinetic (PBPK) model of tirzepatide*. Zenodo. https://doi.org/10.5281/zenodo.14976788

## License

* Source Code: [MIT](https://opensource.org/license/MIT)
* Documentation: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
* Models: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

&copy; 2025-2026 Abhinav Mishra and Matthias König
