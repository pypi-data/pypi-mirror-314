Test package
------------

This repo is for testing build and release automation of Python setuptools projects with
GitHub Actions

Below is the needed per-repsitory setup. The workflow file itself should not need
editing, instead you configure it via variables in `.github/workflows/release-vars.sh`.
You also need to enable Trusted Publisher uploads on PyPI and TestPI, and add an API key
as a repository secret in GitHub for Anaconda package uploads.

#### Configure repository name

This restricts upload steps to run only for workflows running in this repository.

1. Set `RELEASE_REPO` in `.github/workflows/release-vars.sh` to the username and
   repository name, e.g.
   ```bash
   export RELEASE_REPO="chrisjbillington/conda-build-test"
   ```

#### Set up Trusted Publisher package uploads

Per [the docs](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/):

1. Go to https://test.pypi.org/manage/account/publishing, fill in the details and *do*
   set the optional GitHub environment to `testpypi`.
2. Go to https://pypi.org/manage/account/publishing, fill in the details and *do*
   set the optional GitHub environment to `pypi`.

For both PyPI and Test PyPI, "Workflow name" is `release.yml`.

#### Set up Anaconda uploads

1. set `ANACONDA_USER` in `.github/workflows/release-vars.sh`, e.g:
   ```bash
   export ANACONDA_USER="cbillington"
   ```
2. Set `ANACONDA_API_TOKEN` as a repository secret in GitHub. If you don't have a token,
   create one on your Anaconda settings page, e.g.:
   https://anaconda.org/cbillington/settings/access
