# -*- coding: utf-8 -*-
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %                MiCoFaM - Classes and Functions               %
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
Registration of ABAQUS-PlugIn MiCoFaM. 
 
@note: ABAQUS plug-in.       
@version:  1.0    
----------------------------------------------------------------------------------------------
@requires:
       - 

@change: 
       -    
   
@author: Gordon Just
----------------------------------------------------------------------------------------------
"""

import os, sys
from abaqusGui import getAFXApp, Activator, AFXMode, afxCreatePNGIcon #@UnresolvedImport
from abaqusConstants import ALL #@UnresolvedImport

# Store the current path.  
thisDir = os.path.dirname(os.path.abspath(__file__))

# Expand the current search scope and import toplevel script
sys.path.insert(0,os.path.dirname(thisDir))
try: 
    from micofam import __version__ #@UnresolvedImport
# Support typer in main script causing a syntax error in outdated ABAQUS releases
except SyntaxError: __version__ = str(os.getenv("mic_api_version"))
del sys.path[0]

# Prepare plug-in to be registered with additional STM software.
if (os.path.exists(os.path.join(os.path.dirname(thisDir),"stmlab"))):
    sub_menu = 'DLR (SY-STM)|'
else:
    sub_menu = ''

# Get current active set.  
toolset = getAFXApp().getAFXMainWindow().getPluginToolset()

# Register MiCoFaM plug-in
toolset.registerGuiMenuButton(
    buttonText=sub_menu+"MiCoFaM", 
    object=Activator(os.path.join(thisDir, 'micofam_db.py')),
    kernelInitString='',
    messageId=AFXMode.ID_ACTIVATE,
    icon=afxCreatePNGIcon(os.path.join(thisDir,"res",'icon.png')),
    applicableModules=ALL,
    version=__version__,
    author='Gordon Just',
    description='Static and Cyclic RVE Analysis',
    helpUrl='N/A'
)

if __name__ == '__main__':
    pass