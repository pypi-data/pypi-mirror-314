"""
Basic initialization routines for a Python 3.xx session
"""

import os
import sys
import shutil
import inspect

from zdev.core import dependencies
from zdev.validio import force_remove
from zdev.core import fileparts


# INTERNAL PARAMETERS & DEFAULTS
_BASE = [
    r'T:\\Python',                                                  # straight @ home
    r'C:\\Users\\z00176rb\\OneDrive - Siemens Energy\\Dev\\Python', # NEW SE client @ work
    ]
_ENVIRONMENT = [
    r'ZDevTools',
    r'CBM',
    r'DSAP',
    r'RefDB',
    ]
_DEP_TRACKING = True # switch [bool] to trace-back requirements ("Which module is used where?")
_DEP_SET_FLAGS = False # switch [bool] to set flag (if module is contained in project folder)
_IMPORT_PATH = '__imports' # location of user packages/modules (in case of project deployment)
_IMPORT_FOLDERS = [
    r'zdev',
    r'zbm'
    r'dsap',
    r'refdb',
    r'remaster',
    ]

def init_session(root, env=None, verbose=True):
    """ Init routine to set a defined 'sys.path' environment for a new Python session.

    This function provides initialisation for a new Python console (e.g. IPython in Spyder).
    As such, it may also be employed in a 'startup' file to make all required user-defined 
    modules known for a stand-alone use of a project deployed on any machine other than the
    development host. To this end, the 'root'+'env' folders will be inserted into 'sys.path'.
     
    Args:
        root (str or list): Base folder to be added to 'sys'path' and to act as root path of 
            the environment. If multiple potential candidates are given, the first one existing
            will be used. Note that this allows to simultaneously work with different roots
            (e.g. on private vs. work machines).
        env (list, optional): List of environment folders that might be appended to 'sys.path' 
            in addition as 'os.path.join(root, env[n])'. Defaults to 'None'.
        verbose (bool, optional): Switch to print initialisation progress. Defaults to 'True'.

    Returns:
        track (dict): Dict w/ keys 'root' and 'folders' to check on actual success.
    """
    track = {'base': '', 'folders': []}

    # get proper base folder
    if (type(root) is list):
        for base in root:
            if (os.path.isdir(base)):
                if (verbose): print(f"init_session: using base <{base}>")
                track['base'] = base
                break
    elif (type(root) is str):
        base = root
    else:
        raise TypeError(f"Unknown type of root folder") 

    # ...and add folders to beginning of path
    num_errors = 0
    if (env is not None):
        for n, item in enumerate(env, start=1):
            folder = os.path.join(base, item)
            if (os.path.isdir(folder)):
                if (folder not in sys.path):
                    sys.path.insert(n, folder)
                    if (verbose): print(f"init_session: added <{folder}> to 'sys.path'")
                    track['folders'].append(folder)
                else:
                    if (verbose): print(f"init_session: <{folder}> was already present in 'sys.path'")
            else:
                if (verbose): print(f"init_session: could not include <{folder}> in 'sys.path'")
                num_errors += 1

    # Note: Position '0' is always the current script path or '' in REPL, so add 'root' only at
    # the end in order to have it in position #1 ;)
    if (base not in sys.path):
        sys.path.insert(1, base)

    # completion
    if (num_errors):
        if (verbose): print(f"init_session: finished with {num_errors} ERRORS (check above)")
    else:
        if (verbose): print(f"init_session: FINISHED SUCCESSFULLY (ready for work)")

    return track


def project_deploy(folder):
    """ Collects dependencies & prepares application in 'folder' before deployment.

    This step analyzes all dependencies of the files located in the project folder and gathers
    any necessary user files by copying them into the local '_IMPORT_PATH'. Note that this
    should be done only once in the process of "packaging" an application as stand-alone item
    for execution on *any other machine* (e.g. where no system Python is present).
    For more information on the complete deployment see 'auto_deploy.bat'.

    Args:
        folder (str): Location of the project containing all necessary files and sub-folders.

    Returns:
        num_errors (int): Number of encountered errors (if any).
    """
    # from zdev.core import dependencies
    # from zdev.validio import force_remove

    # step 0: set environment
    back = os.getcwd()
    os.chdir(folder)

    # step 1: create local import folder
    root = os.getcwd()
    dest = os.path.join(root, _IMPORT_PATH)
    if (os.path.isdir(dest)):
        print(f"(1) Purging local folder <{dest}>")
        shutil.rmtree(dest, onerror=force_remove)
    else:
        print(f"(1) Creating local folder <{dest}>")
    os.mkdir(dest)

    # step 2: hide folders on development host (to simulate clean environment)
    print(f"(2) Preparing 'sys.path'")
    for item in _IMPORT_FOLDERS:
        sub_folder = os.path.join(dest, item)
        if (sub_folder in sys.path):
            sys.path.remove(sub_folder)

    # step 3: check for dependencies in all project files
    print(f"(3) Analysing dependencies")
    dep = dependencies(root, excludes=['venv'], trace_back=_DEP_TRACKING, save_dep=True,
                       save_req=True, verbose=False)

    # step 4: collect & copy required files
    print(f"(4) Collecting modules (i.e. copy to local import folder)")
    num_errors = 0
    for module in dep['user']:
        print(f"    + locating '{module}'")

        # decompose module subpath & create subfolder hierarchy (if necessary)
        mod_parts = module.split('.')
        mod_subpath = ''
        chk = dest
        for sub in mod_parts[:-1]:
            mod_subpath = os.path.join(mod_subpath, sub)
            chk = os.path.join(chk, sub)
            if (not os.path.isdir(chk)):
                os.mkdir(chk)

        # check for module
        module_found = False
        src = os.path.join(root, mod_subpath, mod_parts[-1]+'.py')
        if (os.path.isfile(src)):
            if (_DEP_SET_FLAGS):
                fh = open(os.path.join(dest, mod_subpath, mod_parts[-1]+'_in_project'), 'wt')
                fh.close()
            module_found = True
        else: # ...check for module in all locations
            for location in sys.path:
                src = os.path.join(location, mod_subpath, mod_parts[-1]+'.py')
                if (os.path.isfile(src)):
                    shutil.copy(src, os.path.join(dest, mod_subpath))
                    module_found = True
                    break

        if (not module_found):
            print(f"  --> Error: Could not find '{module}'!")
            num_errors += 1

    #todo: CLEANUP STEPS, e.g. remove folders that are completely empty (= own packages!)?

    # step 5: create 'startup.py' file for project
    print("(5) Creating Python 'startup' file")
    project_startup_py(folder)

    # step 6: create BAT-file!
    print("(6) Creating BAT-file for ease-of-start!")
    project_startup_bat(r'T:/Python/DSAP/DSAP_app.py') ########### what to do?
    # project_startup_bat('DSAP_app')

    ### suggestion: re-work on how DSAP is called
    ### i.e. best = call with args from CLI (arg1 = cfg file, always to be givne!!!!!!!!!)



    # complete & switch back to initial folder
    if (not num_errors):
        print(f"Finished SUCCESSFULLY (ready for creating Python virtual env)")
    else:
        print(f"Finished with {num_errors} ERRORS! (check above)")

    os.chdir(back)
    return num_errors


def project_startup_py(folder):
    """ Generate a 'startup.py' file in the project's 'folder' to correctly set all imports.

    Args:
        folder (str): Location of the project containing all necessary files and sub-folders.

    Returns:
        --
    """

    # get implementation of "init" function & set actual environment
    func_def = inspect.getsource(init_session)
    func_def = func_def.replace("base=BASE", f"base=None")
    user_imports = []
    for item in _IMPORT_FOLDERS:
        local_pkg = os.path.join(os.path.normpath(_IMPORT_PATH), item)
        if (os.path.isdir(local_pkg)):
            user_imports.append( local_pkg )
    func_def = func_def.replace("env=ENVIRONMENT", f"env={user_imports}")

    # create startup file
    with open(os.path.join(folder, 'startup.py'), mode='wt') as sf:
        sf.write('"""\n')
        sf.write(f"Startup file for project '{os.path.normpath(folder).split(os.sep)[-1]}'\n")
        sf.write(f"This *FILE HAS BEEN AUTO-GENERATED* and may be overwritten - DO NOT TOUCH!!\n")
        sf.write(f"For details see 'zdev.base.project_startup_py()'.\n")
        sf.write('"""\n')
        sf.write("import os\n")
        sf.write("import sys\n")
        sf.write("\n")
        sf.writelines( func_def )
        sf.write("\n")
        sf.write("#%% MAIN\n")
        sf.write("if (__name__ == '__main__'):\n")
        sf.write("    print('Initialising project...')\n")
        sf.write("    init_session()\n")
        sf.write("    print('...done - have phun! ;)')\n")
    return


def project_startup_bat(app_main):
    """ Create a BAT-file for a direct start of the project's "entry point".

    Note that 'app_main' is expected to be a PY-file and must reside directly in the project's
    folder (i.e. at top level). Typically, the call is given as an 'if (__name__ == "__main__")'
    construct. The resulting BAT-file will be named 'app_main_START.BAT'.

    Args:
        app_main (str): Filename of type *.py (w/ or w/o extension), containing the initial call
            ("entry point" of the project).

    Returns:
        --
    """
    # from zdev.core import fileparts

    # create filename
    fpath, fname, _ = fileparts(app_main)
    app_file = fname+'.py'
    bat_file = os.path.join(fpath, fname+'_START.BAT')

    # write batch file
    with open(bat_file, mode='wt') as bf:
        bf.write("@ECHO off\n")
        str_start = r'CMD /k "venv\Scripts\activate & '
        str_call = f"from startup import *; init_session(); exec(open('{app_file}').read());"
        str_stop = r' & deactivate"'
        bf.write(str_start + 'PYTHON -c "' + str_call + '"' + str_stop + '\n')
        bf.write("PAUSE\n")

    return



#===============================================================================================
#===============================================================================================
#===============================================================================================

# #%% MAIN
# if (__name__ == "__main__"):
#     print("Initialising Python...")
#     init_session(root=BASE, env=ENVIRONMENT)
#     from zdev import * # make default package accessible
#     #from zdev.core import *
#     print("...done - have phun! ;)")