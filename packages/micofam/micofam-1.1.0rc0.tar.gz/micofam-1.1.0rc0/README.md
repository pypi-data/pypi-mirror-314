# MiCoFaM
MiCoFaM (Micromechanical Composite Fatigue Modeler) is a model generator for creating representative volume elements (RVEs) consisting of fibre, interface and matrix phases for a given fiber volume content with randomized fiber placements. The application is provided as an ABAQUS plug-in.
## Downloading
Use GIT to get the latest code base. From the command line, use
```
git clone https://gitlab.dlr.de/dlr-sy/micofam micofam
```
If you check out the repository for the first time, you have to initialize all submodule dependencies first. Execute the following from within the repository. 
```
git submodule update --init --recursive
```
To fetch all refererenced submodules, use
```
git submodule foreach --recursive 'git checkout $(git config -f $toplevel/.gitmodules submodule.$name.branch || echo main)'
```
To update all refererenced submodules to the latest production level, use
```
git submodule foreach --recursive 'git pull origin $(git config -f $toplevel/.gitmodules submodule.$name.branch || echo main)'
```
## Installation
MiCoFaM can be installed and updated directly using [pip](https://pypi.org/project/micofam/). Use
```
pip install micofam
```
to install the latest release. Alternatively, 
MiCoFaM can be installed from source using [poetry](https://python-poetry.org). If you don't have [poetry](https://python-poetry.org) installed, run
```
pip install poetry --pre --upgrade
```
to install the latest version of [poetry](https://python-poetry.org) within your python environment. Use
```
poetry update
```
to update all dependencies in the lock file or directly execute
```
poetry install
```
to install all dependencies from the lock file. Last, you should be able to import MiCoFaM as a python package.
```python
import micofam
```
## Usage
Navigate to the local ./config folder and execute ABAQUS using
```
abaqus cae
```
ABAQUS CAE is now started with a modified plugin central directory already set. Alternatively, after installing the software through pip, display all available commands by using
```console
$ micofam --help
usage: MiCoFaM [-h] [-v] {info,start} ...

CLI commands for MiCoFaM.

positional arguments:
  {info,start}
    info         Show the current version and system information.
    start        Launch MiCoFaM on the current system. Starts ABAQUS in the process by default.

options:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
```
To launch the current software with a non-default graphical user interface backend, append a valid identifier to the start command. The backend `abaqus` if set by default.
```console
$ micofam start --help
usage: MiCoFaM start [-h] ...

positional arguments:
  backend     Backend application to start MiCoFaM. Defaults to abaqus.

options:
  -h, --help  show this help message and exit
```
For example, to start [MiCoFaM](https://gitlab.dlr.de/dlr-sy/micofam) with a `abq2023h5`, use
```
micofam start abq2023h5
```
## Contact
* [Caroline Lüders](mailto:caroline.lueders@dlr.de)
## Support
* [List of Contributors](CONTRIBUTING.md)