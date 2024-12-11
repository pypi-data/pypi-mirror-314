# codi-cooperatiu-internal-tools

Internal tools and modules of Codi Cooperatiu

## flowbite_css

`flowbite_css` automatically applies form customizations. These customizations use Flowbite styles, a customization of Tailwind.

### Configuration

To use these customizations, you need to add the `flowbite_css` app to the `INSTALLED_APPS` parameter in the `settings.py` file.

#### CODI_COOP_ENABLE_MONKEY_PATCH

The `CODI_COOP_ENABLE_MONKEY_PATCH` parameter in the `settings.py` file controls whether a monkey patch is applied to Django's form fields within your application.

By default, the `CODI_COOP_ENABLE_MONKEY_PATCH` parameter is disabled (`False`). This means the monkey patch will not be applied. If you want to enable the monkey patch, you need to add the `CODI_COOP_ENABLE_MONKEY_PATCH` parameter to the `settings.py` file and set it to `True`.

#### Examples:

**Enable monkey patching:**

```python
# settings.py

CODI_COOP_ENABLE_MONKEY_PATCH = True
```

When this parameter is enabled (`True`), Django form fields such as `CharField`, `EmailField`, `IntegerField`, `ChoiceField`, `MultipleChoiceField`, and `BooleanField` will use the custom fields defined in your application (`CharBoundField`, `BooleanBoundField`, etc.), enabling custom styling and behavior in your forms.

**Disable monkey patching:**

```python
# settings.py

CODI_COOP_ENABLE_MONKEY_PATCH = False  # Default value
```

If this parameter is disabled (`False`), Django's form fields will work with their default behavior and styling, without additional customizations.

#### FORM_RENDERER

You can also use a custom template to render all the HTML associated with the fields (`<label />` and any other HTML) with Flowbite classes. In this case, you need to use the `CustomFormRenderer` form renderer by configuring the `FORM_RENDERER` parameter in the `settings.py` file:

```python
# settings.py

FORM_RENDERER = "flowbite_css.renderers.CustomFormRenderer"
```

# Contribution

## Install Requirements

Make sure you are using python >3.10.

Install the development dependencies by navigating to the "codi-cooperatiu-internal-tools" folder and running:

```commandline
pip install -r requirements.txt
```

In addition to these requirements, you also need to install Django. To install the current version of Django:

```commandline
pip install django
```

The code comes with git hook scripts. These can be installed by running:

```commandline
pre-commit install
```

The pre-commit hook will now run automatically when making a git commit, checking adherence to the style guide (black, isort, and flake8).

## Run Tests

Before submitting a pull request, run the full test suite of "codi-cooperatiu-internal-tools" using:

```commandline
make test
```

If you do not have `make` installed, the test suite can also be executed using:

```commandline
pytest --ds=tests.test_settings --cov=flowbite_classes
```

## Run linting, formatting and tests using tox

[Install tox](https://tox.wiki/en/4.23.2/installation.html) in a isolated
environment, for exampel if you use pip, run:

```commandline
python -m pip install --user tox
```

Then you can run it with:

```commandline
python -m tox
```

One of the tox commands is the linter, you can run it alone with:

```commandline
python -m tox -e lint
```

Note that tox is meant to be run in the github action that will provide different
python versions, but if you run it like that it will only run in the version
that you have in your environment.

## Publishing a New Version to PyPI

To release a new version of the library to PyPI, follow these steps:

1. **Prepare a Release Branch:**
   - Ensure all changes are merged into the `master` branch.
   - Create a new branch named after the release version (e.g., `v1.2.3`).
   - Update the `version` field in the `project` section of the `pyproject.toml` file to the new release version.
   - Commit the changes with a message like `Version <release-version>`.
   - Push the branch to the remote repository and create a pull request titled `Version <release-version>`.

2. **Tag the Release:**
   - Once the pull request has been reviewed and merged, create a Git tag for the release. Use the following command:
     ```bash
     git tag -a <release-version> <commit> -m "Release <release-version>"
     ```
     Replace `<release-version>` with the version number (e.g., `v1.2.3`) and `<commit>` with the commit hash of the merged pull request.
   - Push the tag to the remote repository:
     ```bash
     git push origin <release-version>
     ```

3. **Create a GitHub Release:**
   - Open the [GitHub Releases page](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository#creating-a-release).
   - Click "Draft a new release."
   - In the **Tag version** field, select the previously pushed tag `<release-version>`.
   - Use `<release-version>` as the release title.
   - In the description, list the changes introduced in this release compared to the previous version.
   - Click "Publish release."

4. **Automatic Deployment:**
   - Once the release is published, GitHub Actions will automatically trigger the deployment process and publish the new version of the library to PyPI, as configured in the repository.
