# Setup

If you want to use the most recent SDK code in this repo

```bash
$ cd client-pys/dynamofl
$ pip install -e .
$ pip install -r requirements.txt
# to uninstall the local version run `pip uninstall dynamofl`
```

If you want to use the SDK code published to PyPi (which may be older than the SDK code in this repo)

```bash
$ pip install dynamofl
```

## Running samples

Install the dependencies of the samples/ folder

```bash
$ cd client-py/samples
$ pip install -r requirements.txt
```

Create `.env` file.

```bash
$ cp .env.example .env
```

Then set the `API_HOST` and `API_KEY` (generated from the UI) in `.env` file.

Run basic sample

```bash
$ python sample.py
```

## Deprecated hack. Tired of copy-pasting your latest changes into `site-packages` ?

Follow the steps below to run the `samples` against your latest code

1. Open `<venv>/bin/activate`
2. Paste the below code snippet to the end of file and set `CLIENT_PY_DIR`

```
CLIENT_PY_DIR=<absolute path to client-py repo>
SYSPATHS=$($VIRTUAL_ENV/bin/python -c "import sys; print(':'.join(x for x in sys.path if x))")
export PYTHONPATH=$SYSPATHS":"$CLIENT_PY_DIR
```

3. Run `pip uninstall dynamofl` to delete the `dynamofl` package from `site-packages`

<br>

> To test against a published `dynamofl` SDK, run `pip install dynamofl` before running the samples

# Build and publish the package

NOTE: Building the package would delete the `dist` directory and `dynamofl.egg-info` file at the root of `client-py`

### Build

1. Ensure the libraries listed in `client-py/build_requirements.txt` is installed in the venv
2. Activate the venv
3. Check the latest version deployed at `https://pypi.org/project/dynamofl/`
4. Decide the new version and then do `export BUILD_VERSION_CORE=<new-version>` E.g
   - `export BUILD_VERSION_CORE=0.0.73`
5. Run `./build-sdk.sh dynamofl`. A dist folder will be created at `dynamofl/dist`

### Publish

6. `cd dynamofl`
7. Please get the pypi token from the team in case you don't have it
8. Run `twine upload dist/* -u __token__ -p <token>`.
