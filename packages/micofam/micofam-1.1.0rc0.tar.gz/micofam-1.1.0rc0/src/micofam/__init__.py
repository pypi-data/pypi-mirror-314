# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %                             MICOFAM                          %
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
Main entry point of MiCoFaM package
 
@note: MiCoFaM command line interface
Created on 03.12.2024

@version:  1.0    
----------------------------------------------------------------------------------------------
@requires:
       - 

@change: 
       -    
   
@author: garb_ma                                                     [DLR-SY,STM Braunschweig]
----------------------------------------------------------------------------------------------
"""

## @package MiCoFaM
# Micromechanical Composite Fatigue Modeler.
## @author 
# Marc Garbade
## @date
# 12.09.2024
## @par Notes/Changes
# - Added documentation  // mg 12.09.2024

import os, sys
import subprocess
import argparse

# Try to import metadata reader. Allowed to fail.
try: import importlib_metadata
except (ImportError, SyntaxError) as _: pass

try: import tomlkit
except (ImportError, SyntaxError) as _: pass

try:
    ## Try to use typer as a modern CLI interface. 
    # Is allowed to fail
    from typing import Optional #@UnresolvedImport

    from typer import Typer as Command, Argument
    from typer import Context, Exit, Option
except (ImportError, SyntaxError) as _: pass

## Absolute system path to MiCoFaM.
MiCoFaMPath = os.path.dirname(os.path.abspath(__file__))

## Get the current project name
__project__ = os.path.basename(os.path.normpath(MiCoFaMPath))

## Provide canonical version identifiers
try:
    # Obtain version directly from metadata
    __version__ = importlib_metadata.version(__project__)
except:
    # We have a partial install 
    try:
        # Obtain version directly from metadata
        with open(os.path.join(MiCoFaMPath,os.path.pardir,os.path.pardir,"pyproject.toml")) as pyproject: content = pyproject.read()
        __version__ = tomlkit.parse(content)["tool"]["poetry"]["version"]
    except Exception as _:
        # We have only the source code
        __version__ = str(os.getenv("mic_api_version","0.0.0dev"))

# Create version info for compatibility
__version_info__ = tuple(__version__.split("."))

## Definition of dictionary with default settings.
# Set the current project name
__settings__ = {"__base__" : "MiCoFaM"}

# All descriptions for duplicate methods and arguments
__help__= { "backend": 'Backend application to start %s. Defaults to abaqus.' % __settings__["__base__"],
            "info":"Show the current version and system information.",
            "main": 'CLI commands for %s.' % __settings__["__base__"],
            "start": "Launch %s on the current system. Starts ABAQUS in the process by default." % __settings__["__base__"],
            "version": "%s (%s)" % (__settings__["__base__"],__version__),
            }

def run(*args, **kwargs):
    """
    Run the application as a plugin for ABAQUS. Defaults to abaqus if no explicit version was provided.
    """
    # Local variables
    delimn = " "
    abq_env_file = "abaqus_v6.env"
    # Define base command
    command = [x for x in args];
    # Check if a local environment file exists
    env_exists = os.path.exists(os.path.join(os.getcwd(),abq_env_file))
    # If command is empty, args was empty and no explicit version of ABAQUS was stated
    if command: command.extend(["cae"])
    else: command = ["abaqus","cae"]
    # Set micofam path as central plugin directory for abaqus
    with open("abaqus_v6.env", 'a+') as f:
        f.seek(0)
        if not any("plugin_central_dir" in x for x in f.readlines()):
            f.write(r"plugin_central_dir=r'%s'" % MiCoFaMPath)
    # Set current version as an environment variable to show version in ABAQUS
    env = os.environ.copy(); env.update({"mic_api_version":__version__})
    # Execute run command
    subprocess.check_call(delimn.join(command), env=env, shell=True)
    # Remove environment file completely
    if not env_exists: 
        os.remove(os.path.join(os.getcwd(),abq_env_file))
    # Remove local entry. Only when environment file is modified by this script
    else: 
        with open("abaqus_v6.env", "r+") as f:
            d = f.readlines(); f.seek(0)
            for i in d:
                if not MiCoFaMPath in i: f.write(i)
            f.truncate()
    pass

try:
    # Modern interface using typer. Overwrite legacy method. Allowed to fail
    main = Command(help=__help__["main"], context_settings={"help_option_names": ["-h", "--help"]}, no_args_is_help=True)

    # Create a function to return the current version
    def __version_callback(value):
        # type: (bool) -> None
        """
        Callback function to return the current version
        """
        # Only return value is requested. False by default
        if value:
            print(__help__["version"])
            raise Exit()
        pass

    # Modified entrypoint for typer interface
    @main.callback()
    def common(
        ctx: Context,
        version: Optional[bool] = Option(None, "--version", "-v", help="Show the current version.", callback=__version_callback, is_eager=True)):
        """
        Main entrypoint of STMLab CLI. All other commands are derived from here
        """
        pass

    # Entrypoint to return local system and version information
    @main.command("info",help=__help__["info"])
    def info(): 
        """
        Return local system information
        """
        return __version_callback(True)

    # Unified entry point to start application with a user-defined backend
    @main.command("start",help=__help__["start"])
    def launch(
        backend: Optional[str] = Argument(default=None,case_sensitive=False)):
        """
        Unified launch application entry point
        """
        args = []
        if backend: args.append(str(backend).lower())
        return run(*args)

except:
    # Solution w/o typer installed.
    def main():
        """
        Main entrypoint for MiCoFaM.
        """
        # Set description for CLI command
        parser = argparse.ArgumentParser(prog=__settings__["__base__"], description=__help__["main"])
        parser.add_argument('-v', '--version', action='version', version=__help__["version"])
        # Add all subcommands
        subparsers = parser.add_subparsers(dest='command')
        # Add info command
        subparsers.add_parser('info', help=__help__["info"])
        # Add arguments to install object
        _ = subparsers.add_parser("start", help=__help__["start"])
        _.add_argument("backend", type=str, help=__help__["backend"], nargs=argparse.REMAINDER)
        # Call functions from command line
        args = parser.parse_args()
        if args.command in ["info"]: parser.parse_args(['--version'])
        elif args.command in ["start"]: run(*args.backend)
        # Always print help by default
        else: parser.print_help(sys.stdout)
        # Return nothing if called directly.
        return 0

if __name__ == "__main__":
    main(); sys.exit()