[![PyPI version](https://badge.fury.io/py/curia.svg)](https://badge.fury.io/py/curia)

[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Curia-ai_curia-python-sdk&metric=alert_status&token=e6d33fff8f3c9375c06d3b3deba711b1891c0b0b)](https://sonarcloud.io/dashboard?id=Curia-ai_curia-python-sdk)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=Curia-ai_curia-python-sdk&metric=bugs&token=e6d33fff8f3c9375c06d3b3deba711b1891c0b0b)](https://sonarcloud.io/dashboard?id=Curia-ai_curia-python-sdk)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Curia-ai_curia-python-sdk&metric=coverage&token=e6d33fff8f3c9375c06d3b3deba711b1891c0b0b)](https://sonarcloud.io/dashboard?id=Curia-ai_curia-python-sdk)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=Curia-ai_curia-python-sdk&metric=sqale_rating&token=e6d33fff8f3c9375c06d3b3deba711b1891c0b0b)](https://sonarcloud.io/dashboard?id=Curia-ai_curia-python-sdk)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=Curia-ai_curia-python-sdk&metric=reliability_rating&token=e6d33fff8f3c9375c06d3b3deba711b1891c0b0b)](https://sonarcloud.io/dashboard?id=Curia-ai_curia-python-sdk)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=Curia-ai_curia-python-sdk&metric=security_rating&token=e6d33fff8f3c9375c06d3b3deba711b1891c0b0b)](https://sonarcloud.io/dashboard?id=Curia-ai_curia-python-sdk)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=Curia-ai_curia-python-sdk&metric=vulnerabilities&token=e6d33fff8f3c9375c06d3b3deba711b1891c0b0b)](https://sonarcloud.io/dashboard?id=Curia-ai_curia-python-sdk)

![Release](https://github.com/Curia-ai/curia-python-sdk/workflows/Release%20Workflow/badge.svg)

# Curia Python SDK
Curia Python SDK is a Python library for interacting with the Curia Platform.

For detailed documentation, including the API reference, see our docs at https://Curia-ai.github.io/curia-python-sdk/.

### Installing the Curia Python SDK
The Curia Python SDK is built to public PyPi and can be installed with `pip` as follows: 
```
pip install curia
```

You can install from source by cloning this repository and utilizing poetry:
```
git clone https://github.com/Curia-ai/curia-python-sdk.git
cd curia-python-sdk
poetry install
```

##### Supported Operating Systems
Curia Python SDK supports Unix/Linux and Mac.

##### Supported Python Versions
Curia Python SDK is tested on:
- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11

##### Curia Permissions
The Curia Python SDK requires a Curia API Token to access the Curia API. To access your API Token visit the instance
of the curia platform you are utilizing and access the developer settings, e.g. in prod:
```
https://aledade.dev.curia.ai/settings/developer
```

### Development
#### Installing dependencies
While the Curia Python SDK supports Python 3.8+, we develop using Python 3.9. One of the easiest ways to install Python 3.9 is with [pyenv](https://github.com/pyenv/pyenv)
```
pyenv install 3.9.7
pyenv local 3.9.7
```

Curia Python SDK uses [Poetry](https://python-poetry.org/) for dependency management. We suggest installing poetry 
through pipx. You can install pipx with Homebrew:
```brew install pipx```

Once pipx is installed, you can install poetry:
```pipx install poetry```

Once poetry is installed, you can install the dependencies for the Curia Python SDK.

To install dependencies, run:
```
poetry install
```

To install dependencies for development, run:
```
poetry install --with=dev
```

#### Poe Commands
We utilize [Poe](https://poethepoet.natn.io/index.html), a poetry plugin, to handle common tasks. To see a list of commands, run:
```
poetry run poe --help
```

##### Running tests

To run tests, run:
```
poetry run poe test
```

##### Running linting
To run linting, run:
```
poetry run poe lint
```

##### Building the SDK
To build the SDK, run:
```
poetry run poe build
```

##### To clean build artifacts and test artifacts
To clean build artifacts and test artifacts, run:
```
poetry run poe clean
```

##### Building docs
Curia Python SDK has Sphinx docs.
To build the docs, run:
```
poetry run poe build-docs
```

To preview the site with a Python web server:
```
cd docs/_build/html
python -m http.server 8000
```
View the docs by visiting http://localhost:8080

##### Manually using the Swagger Codegen

Portions of the Curia Python SDK are generated using the Swagger Codegen. To manually regenerate the SDK, you will need
to install gnu-sed. Visit https://medium.com/@bramblexu/install-gnu-sed-on-mac-os-and-set-it-as-default-7c17ef1b8f64 to see how to install gnu-sed for consistency in fixing swagger imports
```export PATH="/usr/local/opt/gnu-sed/libexec/gnubin:$PATH"```

Once you have gnu-sed installed, you can run the following command to regenerate the SDK:
```
poetry run poe swagger-codegen-prod
```
to regenerate the SDK from the production environment, or
```
poetry run poe swagger-codegen-dev
```
to regenerate the SDK from the development environment.


## Cut your own release (not recommended)
Sometimes we may have updates that are currently in the development environment, 
but not accessible in production yet.  When this happens, the SDK will not reflect
the latest changes in develop.  To be able to use new features of the API, you can
cut a new release of the SDK and use the latest version.  

*BE CAREFUL - MAKE SURE YOU KNOW WHY YOU ARE DOING THIS* 

To cut a new release based on the Dev API, run `poetry run poe swagger-codegen-dev`.  In order 
to get some sed commands to work on Mac, you will need to install and use 
[Gnu-Sed](#use-gnu-sed)

First, update the version in `src/curia/__init__.py`
Then build the source distribution: `poetry run poe build`
Make sure you have twine installed: `pip install twine`.
Finally, upload the new distribution to pypi: `python -m twine upload dist/*`
You will be prompted for a username and password.  
- Your username is `__token__`
- Your password is stored in 1Password in the Curia vault in the `PyPi Curia Project` secure document
