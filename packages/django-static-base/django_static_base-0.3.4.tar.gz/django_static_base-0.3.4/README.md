# django-static-base [![PyPi license](https://img.shields.io/pypi/l/django-static-base.svg)](https://pypi.python.org/pypi/django-static-base)

[![PyPi status](https://img.shields.io/pypi/status/django-static-base.svg)](https://pypi.python.org/pypi/django-static-base)
[![PyPi version](https://img.shields.io/pypi/v/django-static-base.svg)](https://pypi.python.org/pypi/django-static-base)
[![PyPi python version](https://img.shields.io/pypi/pyversions/django-static-base.svg)](https://pypi.python.org/pypi/django-static-base)
[![PyPi downloads](https://img.shields.io/pypi/dm/django-static-base.svg)](https://pypi.python.org/pypi/django-static-base)
[![PyPi downloads](https://img.shields.io/pypi/dw/django-static-base.svg)](https://pypi.python.org/pypi/django-static-base)
[![PyPi downloads](https://img.shields.io/pypi/dd/django-static-base.svg)](https://pypi.python.org/pypi/django-static-base)

## GitHub ![GitHub release](https://img.shields.io/github/tag/DLRSP/django-static-base.svg) ![GitHub release](https://img.shields.io/github/release/DLRSP/django-static-base.svg)

## Test [![codecov.io](https://codecov.io/github/DLRSP/django-static-base/coverage.svg?branch=main)](https://codecov.io/github/DLRSP/django-static-base?branch=main) [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/DLRSP/django-static-base/main.svg)](https://results.pre-commit.ci/latest/github/DLRSP/django-static-base/main) [![gitthub.com](https://github.com/DLRSP/django-static-base/actions/workflows/ci.yaml/badge.svg)](https://github.com/DLRSP/django-static-base/actions/workflows/ci.yaml)

## Check Demo Project
* Check the demo repo on [GitHub](https://github.com/DLRSP/example/tree/django-static-base)

## Requirements
-   Python 3.8+ supported.
-   Django 4.2+ supported.

## Setup
1. Install from **pip**:
    ```shell
    pip install django-static-base
    ```

2. Add `'static_base'` to your `INSTALLED_APPS` setting.

    ``` python title="settings.py"
    INSTALLED_APPS = [
        # ...other apps
        "static_base"
    ]
    ```

3. Add the following pre-requisites to your `base.html` template

    ``` html title="base.html"
    <html>
    <head>
    ...
      <link rel="stylesheet" type="text/css" href="{% static 'base/css/bootstrap.css' %}">
    ...
    </head>
    <body>
    ...
      <script type="text/javascript" src="{% static 'base/js/jquery.min.js' %}"></script>
      <script type="text/javascript" src="{% static 'base/js/bootstrap.min.js' %}"></script>
      <script type="text/javascript" src="{% static 'base/js/plugins/lazysizes.min.js' %}" async></script>
    ...
      <script type="module" src="{% static 'base/js/plugins/instantpage.min.js' %}" defer></script>
    </body>
    </html>
    ```

4. Add all your needed plugins or customization to your `base.html` template or sub-templates used by your project

    ``` html title="base.html"
    <html>
    <head>
    ...
      <link rel="stylesheet" type="text/css" href="{% static 'base/css/plugins/jquery.smartmenus.bootstrap-4.css' %}">
    ...
      <link rel="stylesheet" type="text/css" href="{% static 'base/css/style-btn.css' %}">
      <link rel="stylesheet" type="text/css" href="{% static 'base/css/color/blue.css' %}">
    ...
      <link rel="stylesheet" type="text/css" href="{% static 'base/css/custom.css' %}">
    ...
    </head>
    <body>
    ...
      <script type="text/javascript" src="{% static 'base/js/jquery.min.js' %}"></script>
      <script type="text/javascript" src="{% static 'base/js/bootstrap.min.js' %}"></script>
    ...
      <script type="module" src="{% static 'base/js/plugins/instantpage.min.js' %}" defer></script>
    </body>
    </html>
    ```

## Run Example Project

```shell
git clone --depth=50 --branch=django-static-base https://github.com/DLRSP/example.git DLRSP/example
cd DLRSP/example
python manage.py runserver
```

Now browser the app @ http://127.0.0.1:8000
