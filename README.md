Hamburger Server
================

## Setup
All dependencies are listed in `setup.py`. Ensure you have Python 3 installed.

1. Create VirtualEnvs Directory `mkdir ~/VirtualEnvs/`
2. Create ham VirtualEnv `python3 -m venv ~/VirtualEnvs/ham`
3. Setup development environment `python3 setup.py develop`

## Running Server
Ensure you have been given a `development.ini` file. It is not within
the repository for security reasons as it contains keys for various server services.

1. Place `development.ini` in `Hamburger/conf/`
2. `pserve conf/development.ini`

By default, Pyramid does not log interactions within the server except for errors.
If new code is written, you must exit and restart the server.

## Running Tests
Test are run with pytest.

`pytest --cov-report term-missing --cov=hamburger`


### Notes
If any changes are to be made, please submit a Pull Request and ask Austin Graham for review.
