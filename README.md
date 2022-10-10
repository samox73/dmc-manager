## Prerequisites and Setup
To start working with this, you just need to setup a virtual environment (or have all packages)
installed locally.

For easy virtual env management, use 
[virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/).
After setting it up, proceed as follows:
- `mkvirtualenv my_environment_name`
- `workon my_environment_name`
- (in the root of this repository) `pip install -r requirements.txt`
- (in the root of this repository) `add2virtualenv .`

The last line is needed so that the directory gets included in the `PYTHONPATH`
environment variable. This way we can use the module `manager` without actually
installing it. But beware, this sets your working directory in python scipts 
also to this path. That's why simple directory setup is needed at the begin 
of the examples. 

## Usage
See the `examples/easy_template` folder for a simple `momuntum_vs_energy` calculation.
