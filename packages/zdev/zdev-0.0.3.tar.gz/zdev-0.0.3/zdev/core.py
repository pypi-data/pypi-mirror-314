"""
Development helpers for quick & easy handling of regular tasks
"""

import os
import re
import sys
import time
import shutil
import numpy as np
import inspect
import datetime as dt
import importlib
import sounddevice as sd
from functools import partial

from zdev.colors import *
from zdev.indexing import file_goto
from zdev.searchstr import S_IDENT_W_DOT_HYP, S_DOC_STR_QUOTES


# EXPORTED DATA
DEP_FILE_TYPES = ('.py', '.pyw') # file types to include for dependency search
DEP_PKG_BUILTIN = [ # definition of "builtin" packages -> sorted acc. to # chars
    'io', 'os', 're',
    'csv', 'sys',
    'json', 'math', 'stat', 'time', 'uuid',
    #5
    'base64', 'ctypes', 'pickle', 'shutil', 'typing',
    'asyncio', 'inspect', 'logging', 'zipfile',
    'datetime', 'requests', 'winsound',
    'functools', 'importlib', 'threading',
    'concurrent', 'statistics', 'subprocess', 
    #11
    'configparser',
    #12, #13, #14,
    'multiprocessing',
    #16
    #specials:
    '__future__'
    ]
DEP_PKG_KNOWN = [ # definition of "known" packages -> sorted acc. to # chars
    #2
    'PIL', # pip -> pillow
    'dash', 'h5py', 
    'flask', 'numpy', 'pydub', 'PyQt5', 'scipy',
    'pandas', 'plotly', 'psutil',
    'skimage', # pip -> scikit-image
    'openpyxl', 'psycopg2', 'pydantic', 'tifffile', 
    'soundfile', 'streamlit',
    'matplotlib',
    'sounddevice',
    #12 #13 #14
    'influxdb_client',
    #16
    ]

# INTERNAL PARAMETERS & DEFAULTS

# regex patterns
_RX_IMPORT = re.compile(r'(?P<tag>import )(?P<module>'+S_IDENT_W_DOT_HYP+r')')
_RX_IMPORT_FROM = re.compile(r'(?P<tag1>from )(?P<module>'+S_IDENT_W_DOT_HYP+r')(?P<tag2> import )')
_RX_WHITESPACE = re.compile(r'\s*')
_RX_QUOTES = re.compile(r'["\']')


def howmany(obj):
    """ Returns number of references inherent to PyObject 'obj' in CPython memory. """
    return sys.getrefcount(obj)


def isint(x, check_all=False):
    """ Returns an 'any-integer-type' indication (also works for arrays). """
    try:
        len(x)
        x = x[0]
    except:
        x
    finally:
        if (type(x) in (int, np.int64, np.int32, np.int16, np.int8)):
            return True
        else:
            return False


def isfloat(x):
    """ Returns an 'any-float-type' indication (also works for arrays). """
    try:
        len(x)
        x = x[0]
    except:
        x
    finally:
        if (type(x) in (float, np.float64, np.float32, np.float16)):
            return True
        else:
            return False


def iscomplex(x):
    """ Returns an 'any-complex-type' indication (also works for arrays). """
    try:
        len(x)
        x = x[0]
    except:
        x
    finally:
        if (type(x) in (complex, np.complex128, np.complex64)):
            return True
        else:
            return False


def fileparts(the_file):
    """ Returns absolute path, filename and extension (mimic MATLAB function). """    
    fname, ext = None, None
    full_name = os.path.abspath(the_file)
    if (os.path.isdir(full_name)):
        path = full_name
    else:
        path = os.path.dirname(full_name)
        filename = os.path.basename(full_name)
        try:
            *tmp, ext = filename.split('.')[:]
            fname = '.'.join(tmp)
            # Note: Ensures that '.' in filename are kept & only last is counted as extension!
        except:
            fname = filename
    return path, fname, ext


def anyfile(path, base, formats):
    """ Checks if folder 'path' contains a file 'base' in *any* of the acceptable 'formats'.

    Args:
        path (str): Folder location in which to look for files.
        base (str): Base of the filename to which the format/extension will be appended.
        formats (list of str): List of known formats to probe for. In order to robustify this
            helper function, leading '.' (if present) are automatically dealt with.

    Returns:
        fname_existing (str): Full filename of the 1st existing file that matched the
            combination of 'base' + a format from the list.
    """
    if (type(formats) is str):
        formats = [formats]
    for fmt in formats:
        if (fmt.startswith('.')):
            fmt = fmt[1:]
        fname_existing = os.path.join(path, base+'.'+fmt)
        if (os.path.isfile(fname_existing)):
            return fname_existing
    # Note: The same job is done by the following - using abbreviations ;)
    # [ os.path.join(p,b+'.'+f) for f in fmts if (os.path.isfile(os.path.join(p,b+'.'+f))) ][0]
    return None


#
# HOW??????????
#   --> really search for this in ALL folders!!! 
#   --> if possible, then rename to "filesize" (only)

def filesize_str(bytes_, binary=True):
    """ Returns string w/ proper file size acc. to https://en.wikipedia.org/wiki/Byte

    Args:
        bytes_ (int): Number of bytes = file size.
        binary (bool, optional): Switch for having binary bases instead of decimal ones (i.e.
            calculating "MiB/GiB/..." instead of "MB/GB/..."). Defaults to 'True'.
    Returns:
        bytes_str (str): Proper string of the file size (to be inserted into text).
    """

    # init
    num_bytes = int(bytes_)
    unit = [ 'Bytes', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y' ]

    # select reference for computations
    if (binary):
        base = 1024
        addon = 'i'
    else:
        base = 1000
        addon = ''

    # create appropriate string representation
    if (num_bytes < base):
        bytes_str = f"{num_bytes} {unit[0]}"
    else:
        order = 0
        while (True):
            order += 1
            if (num_bytes < base**(order+1)):
                res = divmod(num_bytes, base**order)
                bytes_str = f"{res[0]+res[1]/(base**order):.2f} {unit[order]}{addon}B"
                break
            if (order >= len(unit)):
                bytes_str = "more_than_YiB"

    return bytes_str


def storage(payload, num_days=1, downsample=0):
    """ Computes required number of bytes to store 'payload' for a given reference interval.

    The "payload" structure may refer to a set of monitoring data for CBM (condition-based
    maintenance) purposes and is given as dict indicating the number of recorded signals for
    each data type and acquisition rate. In addition, a 'downsample' step can be specified to
    move all signals from their original rate by this amount of intervals w/ lower acquisition
    rate. In this way, a less densly-sampled or aggregated data set (e.g. for more "historic"
    phasess in the past) can be modeled & computed.

    Args:
        payload (dict): Payload of different data types, sampled at different rates.
            Available rates are 'ms'|'sec'|'min'|'hour'|'day'.
            Available dtypes are 'bit'|'byte'|'short'|'int'|'float'|'long'|'double'.
        num_days (int, optional): Reference interval for computations. Defaults to 1 day.
        downsample (int, optional): If desired, specifies the number of sampling intervals to
            shift data acquisition frequency (for all entries). Defaults to 0.

    Returns:
        num_bytes (int): Total number of bytes required for 'payload' within 'num_days'.

    Examples: The following illustrates the computation for a given payload. If desired, the
        result may be converted to a string by using "filesize_str(num_bytes, binary=True)".

        payload = { 'byte':  {'sec': 75, 'min': 250, 'hour': 2000},
                    'int':   {'min': 150, 'hour': 800},
                    'double': {'min': 30, 'hour': 200, 'day': 500} }

        (default, per day)       --> num_bytes =   8216800 ~ 7.84 MiB
        (default, per year)     --> num_bytes = 2999132000 ~ 2.79 GiB
        (downsample=1, per day)  --> num_bytes =    144960 ~ 141.56 KiB
        (downsample=1, per month) --> num_bytes =  52910400 ~ 4.15 MiB

        Note: Since the daily rates for the 'double' data could not be further reduced, the
        latter two examples correspond to the following modified payload:

        payload_downsampled = { 'byte':  {'min': 75, 'hour': 250, 'day': 2000},
                                'int':   {'hour': 150, 'day': 800},
                                'double': {'hour': 30, 'day': 700} }
    """

    # internal settings (all values refer to a daily perspective)
    _RATE = { # 'CCS': 25*1000*60*60*24, # "CCS rate" ~ 40usec (1/(512*f0) == 39.625 us @ 50 Hz)
              'ms':   1000*60*60*24,
              'sec':  60*60*24,
              'min':  60*24,
              'hour': 24,
              'day':   1 }
    _TIMEBASE = list( _RATE.keys() )
    _SIZEOF = { 'double': 8, 'float': 4,
                'long': 8, 'int': 4, 'short': 2,
                'byte': 1, 'bit': (1/8) }
    # Note: A 'bit' is treated separately since it can be "stacked" (i.e. 1 byte = 8 bits)!

    # breakpoint()

    # parse payload & compute daily storage
    all_data = 0
    for dtype in payload.keys():

        for rate in payload[dtype].keys():
            if (payload[dtype][rate] == 0): # ignore/skip empty fields
                continue

            # reduce frequency of data acquisition?
            aq = rate
            if (downsample):
                 idx = _TIMEBASE.index(rate) + downsample
                 if (idx < len(_TIMEBASE)):
                     aq = _TIMEBASE[idx]
                 else:
                     print(f"Warning: Could NOT reduce rate for data '{dtype}' @ '{rate}' (keeping original)")

            # compute storage
            if (dtype == 'bit'):
                req = np.ceil(payload[dtype][rate]*_SIZEOF['bit']) * _SIZEOF['byte'] * _RATE[aq]
            else:
                req = payload[dtype][rate] * _SIZEOF[dtype] * _RATE[aq]
            all_data += req

    # scale to reference interval
    num_bytes = all_data * num_days

    return num_bytes


def showtime(t_slow, t_fast, labels=['slow','fast'], show_factor=True, indent=None):
    """ Compares two processing durations (e.g. 'slow' Python vs. 'fast' C implementation). """

    # compute metrics
    speed_fac = t_slow / t_fast
    gain = 100.0 * (speed_fac-1.0)

    # configure formatting
    L = max([len(labels[0]), len(labels[1])])
    if (indent is not None):
        shift = " "*int(indent)
    else:
        shift = ""
    if (not show_factor):
        if (gain >= 0.0):
            qualifier = "faster"
        else:
            qualifier = "slower"

    # print comparison (speed factor or gain in %)
    if (indent is None):
        print("-"*64)
    print(f"{shift}{labels[0]:{L}} ~ {t_slow:.3e} sec")
    if (show_factor):
        print(f"{shift}{labels[1]:{L}} ~ {t_fast:.3e} sec  ==> speed factor ~ {speed_fac:.2f}")
    else:
        print(f"{shift}{labels[1]:{L}} ~ {t_fast:.3e} sec  ==> {qualifier} by {gain:.0f}%")
    if (indent is None):
        print("-"*64)

    return


def massfileop(root, pattern, mode='count', params=[], max_depth=99, dry=True, verbose=0):
    """ Performs mass file operations in 'root' using 'pattern' in a certain 'mode'.

    Args:
        root (str): Base location where to start traversing all subfolders for 'pattern'. Note
            that this requires intermediate and trailing '\\' (e.g. 'C:\\Windows\\').
        pattern (str): Filename or regex pattern to be used for operation.
        mode (str): Operation to be applied to all files matching the search pattern.
            Available options are:
                'count':    simply counts the number of matches (will overwrite 'verbose=0')
                'chmod':    change file's attributes (i.e. read/write permissions)
                'stamp':    update file's time information by "touching" it
                'remove':   delete all matched files (CAUTION: "Dry" run is highly recommended!)
                'rename':   rename filenames of matches acc. to specification in 'params'
                'replace':  replace text in files acc. to specification in 'params'
        params (2-tuple): Additional parameters required, depending on mode of operation, i.e.
                if 'rename':    params = [ orig_fname_part, new_fname_part ]
                if 'replace':   params = [ orig_line_tag, new_line ]
            Defaults to '[]' (i.e. unused).
        max_depth (int, optional): Maximum level of subfolder search, Default to '99'.
        dry (bool, optional): Switch for performing a "dry run" w/o actual changes to the files.
            Defaults to 'True'.
            Note: This should always be used first for testing, such that no harm is done! For
            the more advanced file operations checks on feasibility will still become apparent.
        verbose (int, optional): Mode of status messages where '0 = off', '1 = files' and '2 =
            track all visited folders'. Defaults to '0'.

    Returns:
        result (int/list/None): Depends on 'mode' of operation. Will be an integer if 'count',
            a list of files if 'collect' and 'None' in all other cases.

    Examples: (make sure to set 'dry_run=True' to test first!)

        (1) Some typical use may be to get rid of all 'desktop.ini' files on Windows systems:
            >>> massfileop(r'C:\', 'desktop.ini', mode='remove', dry_run=True)

        (2) Replace parts of header/comment lines in all Python files of a project:
            >>> massfileop('C:\\MyProject', '\\.py', mode='replace', params=['#*old*','#*new*'])

        (3) Replace (parts of the) filename, but only for matching CSV-files:
            >>> massfileop('C:\\MyProject', '\\.csv', mode='rename',
                           params=['#*old*','#*new*'])
    """

    # init
    rx = re.compile(pattern)
    results = []
    num_found = 0
    num_modified = 0

    # feedback on progress
    if (verbose):
        print("-"*64)
        print("Starting MASS-FILE-OPERATION @ "+time.strftime("%H:%M:%S (%Y-%m-%d):"))
        print(f"Looking for '{pattern}' under <{root}>")
        print("")
        print(f"Applying operation '{mode}'...")
        print("")

    # traverse all folders under given root...
    for path, folders, files in os.walk(root): #[:-1]): # Note: remove trailing '\\'?

        path_ = path[:-1] + os.sep
        depth = path_[len(root):].count(os.sep)

        # ... as long as maximum depth is not yet reached...
        if (depth >= (max_depth+1)):
            if (verbose > 1): print(f"Skipping <{os.path.join(path)}> (MAX DEPTH reached!)")
            continue
        else:
            the_folder = os.path.join(path)
            if (verbose > 1): print(f"Entering <{the_folder}>")
            for fname in files:

                # step 1: check if file matches pattern
                if (rx.search(fname) is not None):
                    the_file = os.path.join(the_folder, fname)

                    # register file
                    num_found += 1
                    results.append( the_file )
                    if (verbose > 1): 
                        print(f"  -> Found '{fname}'")
                    elif (verbose):  
                        print(f"  -> Found '{the_file}'")

                    # step 2: (try to) apply selected file operation
                    # simple
                    if (mode in ('count','chmod','stamp','remove')):
                        if (not dry):
                            try:
                                if (mode == 'count'):
                                    pass # do nothing ;)
                                elif (mode == 'chmod'):
                                    os.chmod(the_file, params[0])
                                elif (mode == 'stamp'):
                                    mytime = dt.datetime.now().timestamp()
                                    os.utime(the_file, (mytime,mytime))
                                elif (mode == 'remove'):
                                    os.remove(the_file)
                                num_modified += 1
                            except:
                                print(f"Warning: Could NOT {mode} '{the_file}'!")
                        else:
                            pass # do nothing

                    # advanced (check feasibility)
                    elif (mode in ('rename','replace')):

                        if (mode == 'rename'):
                            try:
                                if (type(params[0]) is re.Pattern): # RegEx replacement
                                    str_old = params[0].search(fname).group()
                                    str_new = params[1]
                                    fname_re = re.sub(str_old, str_new, fname)
                                    # print(str_old, str_new, fname_re)
                                else: # assume simple string replacement
                                    fname_re = re.sub(params[0], params[1], fname)
                                if (fname_re != fname):
                                    if (not dry):
                                        shutil.move(the_file, os.path.join(the_folder,fname_re))
                                        num_modified += 1
                            except:
                                print(f"     Warning: Could NOT {mode} '{the_file}'!")

                        elif (mode == 'replace'):

                            #
                            # TODO: apply 'dry_run' scheme for feasibility testing!
                            #

                            if (not dry):
                                with open(the_file, mode='rt+') as tf:
                                    pos = file_goto(tf, params[0], mode='tag', nextline=False)
                                    if (pos is not None):
                                        tf.seek(pos[0]-1, 0) # -1 / otherwise 1st char is eaten
                                        #time.sleep(0.100)
                                        print(f"tell = {tf.tell()}")
                                        text = tf.readlines()
                                        # breakpoint()
                                        # text[0] = params[1]+'\n'
                                        tmp = text[0]
                                        print(f"pos = {pos} // found tmp as: {tmp}")
                                        text[0] = re.sub(params[0], params[1], tmp)
                                        print(f" --> now it is: {text[0]}")
                                        tf.seek(pos[0], 0)
                                        tf.writelines(text)
                                        num_modified += 1
                            else:
                                pass # do nothing

    # print short summary
    if (verbose):
        print("")
        print(f"Found {num_found} files")
        print(f"Modified {num_modified} files")
        print("-"*64)

    return results


def dep_per_file(D, src_file, show_imports=True, trace_back=True, verbose=False):
    """ normal func for higher-level tracing 

    Args:
        # todo

    Returns:
        # todo    
    
    """
    _, fname, __ = fileparts(src_file)
    with open(src_file, mode='rt') as sf:             
        inside_doc_string = False

        for n, line in enumerate(sf.readlines(), start=1):

            # determine indentation level
            indent_level = 0
            whitespace = _RX_WHITESPACE.match(line)
            if (whitespace): indent_level = int(whitespace.end()/4)                        

            line = line.strip()
            
            # skip DOC-STRINGS
            chkdoc = line.split(S_DOC_STR_QUOTES)
            if (chkdoc[0] != line):                            
                if (inside_doc_string):                                
                    inside_doc_string = False # leaving
                elif (len(chkdoc) == 2):
                    inside_doc_string = True # entering
                else: # (len(chkdoc) == 3)
                    pass # doc-string is entered & left on the same line!                            
            if (inside_doc_string):
                continue

            # skip COMMENTS (only "full-comment" lines)
            if (line.startswith('#')):
                continue
                
            # check for dependency                        
            dep_type = None
            if (not indent_level): # @ top level
                if (not dep_type):
                    chk = _RX_IMPORT_FROM.match(line)
                    if (chk): dep_type = 'from_import'
                if (not dep_type):
                    chk = _RX_IMPORT.match(line)
                    if (chk): dep_type = 'import'                           
            else: # @ function/class definitions                           
                if (not dep_type):
                    chk = _RX_IMPORT_FROM.search(line)
                    if (chk): dep_type = 'from_import_in_func'
                if (not dep_type):
                    chk = _RX_IMPORT.search(line)
                    if (chk): dep_type = 'import_in_func'

            if (not dep_type): continue # w/ next line

            # discard hit if it is within another string!
            before = line[:chk.span()[0]]
            after = line[chk.span()[1]:]
            if (_RX_QUOTES.search(before)):
                if (verbose):   
                    print(f"line #{n:-4d}: discarding hit, since it is within string expression!")
                continue

            # record new dependency                        
            mod_name = chk.groupdict()['module']
            pkg_name = mod_name.split('.')[0]
            # pkg_name = mod_name.split('.')[:-1] # FIXME: how to deal w/ nested modules?

            if (pkg_name in DEP_PKG_BUILTIN):
                if (mod_name not in D['builtin']):
                    D['builtin'].append(mod_name)
            elif (pkg_name in DEP_PKG_KNOWN):
                if (mod_name not in D['known']):
                    D['known'].append(mod_name)
            elif (mod_name not in D['user']):                           
                D['user'].append(mod_name)

            # extract source file's import lists?
            if (show_imports):
                line_cleaned = line.split('#')[0].strip()
                if (fname not in  D['imports'].keys()):
                    D['imports'][fname] = [(line_cleaned, n),]
                else:
                    D['imports'][fname].append((line_cleaned, n))

            # add source file to list of module-requesting files?
            if (trace_back):
                if (mod_name not in D['tracing'].keys()):
                    D['tracing'][mod_name] = [(src_file, n),]
                else:
                    D['tracing'][mod_name].append((src_file, n))            

            # print info about analysis progress
            if (verbose):
                if (dep_type == 'import'):
                    print(f"line #{n:-4d}: depends on module <{mod_name}>")
                elif (dep_type == 'from_import'):
                    print(f"line #{n:-4d}: depends on (parts of) module <{mod_name}>")
                elif (dep_type == 'import_in_func'):
                    print(f"line #{n:-4d}: some function depends on module <{mod_name}>")
                else: # (dep_type == 'from_import_in_func')
                    print(f"line #{n:-4d}: some function depends on (parts of) module <{mod_name}>")

    return D


def dependencies(root, excludes=['venv',], show_imports=False, trace_back=True, trace_level=2,          
                 save_dep=True, save_req=True, verbose=False):
    """ Lists all dependencies required for files in a given 'root' folder.

    Args:
        root (str): Base location for dependency search (e.g project folder).
        excludes (list, optional): Subfolders in root that should be excluded from the search
            (if any). Defaults to 'venv'.
        show_imports (bool, optional): Switch for extracting a list of all import statements 
            in the source files. Defaults to 'False'.
        trace_back (bool, optional): Switch for adding a list of all "requesting" files 
            associated w/ each dependency. Defaults to 'False'.
        trace_level (int, optional): Number of levels to analyse dependencies even further, only
            relevant if back-tracing is enabled. A value of '2' will analyse also direct 
            dependencies of required files whereas '3' will also track back the indirect ones
            (i.e. "dependencies of the dependencies of the files required in the sources").
             Defaults to '2'.
        save_dep (bool, optional): Switch for saving the results to 'requirements.info'.
            Defaults to 'True'.
        save_req (bool, optional): Switch for saving 'requirements.txt' for a batch install by
            "pip" (e.g. 'pip install -r %FILE%' or via a FOR-loop). Defaults to 'True'.
        verboes (bool, optional): Switch for status messages on the search. Defaults to 'False'.

    Returns:
        D (dict): Dict with keys 'builtin', 'builtin_pkg', 'known', 'known_pkg', 'user', 
            'user_pkg' as well as 'imports' and 'traceback'. Note that the latter will only be
            populated if tracing is activated, otherwise it will remain an empty list.
    """

    # init
    root_norm = os.path.normpath(root)
    project_path, project_name, _ = fileparts(root_norm)
    if (project_name is None):
        project = os.path.basename(project_path)
    else:
        project = project_name    
    D = { 'builtin': [], 'builtin_pkg': [], 
          'known': [], 'known_pkg': [],
          'user': [], 'user_pkg': [],
          'imports': {},
          'tracing': {} }
    
    if (verbose):
        print("-"*64)
        print(f"Starting DEPENDENCY analysis for <{project}>...")
        print("")

    # traverse all folders & files in project
    num_folders, num_files = 0, 0
    for path, _, files in os.walk(root_norm):
        path_norm = os.path.normpath(path)
        sub = path_norm.replace(root_norm+os.path.sep, '')

        # respect excludes
        checks = [sub.startswith(tree) for tree in excludes]
        if (any(checks)):
            if (verbose): print(f"o Excluded <{sub}>")
            continue
        else:
            if (verbose): print(f"o Traversing FOLDER <{sub}>")
            num_folders += 1

        # check all relevant files
        for fname in files:
            if (fname.endswith(DEP_FILE_TYPES)):
                full_file = os.path.abspath(os.path.join(path_norm, fname))
                if (verbose): print(f"  + Checking files '{fname}'")
                D = dep_per_file(D, full_file, show_imports, trace_back, verbose=False)
    
    if (verbose): print("")

    # trace recursively?
    if (trace_back):

        # 2nd level = DIRECT dependencies of required files
        if (trace_level >= 2): 
            if (verbose): print(f"o Tracing back to 2nd level...")            
            D2 = { 'builtin': [], 'builtin_pkg': [], 'known': [], 'known_pkg': [],
                   'user': [], 'user_pkg': [],
                   'imports': {}, 'tracing': {} }
            
            # analyse by (temporary) import of direct dependency files
            for n, dep_file in enumerate(D['user']):
                if (verbose): print(f"  - Back-tracking own dependencies of '{dep_file}'")
                try:
                    the_module = importlib.import_module(dep_file)
                    the_file = inspect.getsourcefile(the_module)
                    dep_per_file(D2, the_file, False, False, False)
                    del the_module
                except: 
                    pass # fixme: what to do?
            
            # merge dependencies (i.e. only consider additional modules)
            D['user_L2'] = D2['user']
            for dep in D2['user']:
                if (dep not in D['user']):
                    D['user'].append(dep)
                else:
                    D['user_L2'].remove(dep)
            del D2
        # Note: After this step D['user_L2'] should only contain modules that have been added 
        # during level-2 analysis!

        if (verbose): print("")

        # 3rd level = INDIRECT dependencies of required files
        if (trace_level >= 3): 
            if (verbose): print(f"o Tracing back to 3rd level...")
            D3 = { 'builtin': [], 'builtin_pkg': [], 'known': [], 'known_pkg': [],
                   'user': [], 'user_pkg': [],
                   'imports': {}, 'tracing': {} }
            
            # further analyse by (temporary) import of indirect dependency files
            for n, dep_file in enumerate(D['user_L2']):
                if (verbose): print(f"  - Back-tracking own dependencies of '{dep_file}'")
                try:
                    the_module = importlib.import_module(dep_file)
                    the_file = inspect.getsourcefile(the_module)
                    dep_per_file(D3, the_file, False, False, False)                
                    del the_module
                except:
                    pass # fixme: what to do?

            # merge dependencies (i.e. only consider additional modules)
            D['user_L3'] = D3['user']
            for dep in D3['user']:
                if (dep not in D['user']):
                    D['user'].append(dep)
                else:
                    D['user_L3'].remove(dep)
            del D3
    
    elif (verbose): print("No tracing back to deeper levels")

    # sort modules dependencies & identify packages
    D['builtin'].sort(key=lambda item: item.lower())
    for item in D['builtin']:
        pkg = item.split('.')[0]
        if (pkg not in D['builtin_pkg']): D['builtin_pkg'].append(pkg)
    D['known'].sort(key=lambda item: item.lower())
    for item in D['known']:
        pkg = item.split('.')[0]
        if (pkg not in D['known_pkg']): D['known_pkg'].append(pkg)
    D['user'].sort(key=lambda item: item.lower())
    for item in D['user']:
        pkg = item.split('.')[0]
        if (pkg not in D['user_pkg']): D['user_pkg'].append(pkg)

    # sort import lists and traceback (if any)
    chk = dict(sorted(D['imports'].items(), key=lambda item: item[0].lower()))
    D['imports'] = chk
    for item in D['imports']:
        if (type(item) is list): item.sort(key=lambda item: item.lower())

    chk = dict(sorted(D['tracing'].items(), key=lambda item: item[0].lower()))
    D['tracing'] = chk
    for item in D['tracing']:
        if (type(item) is list): item.sort(key=lambda item: item.lower())
    
    # print summary
    if (verbose):
        print("")
        print("...finished DEPENDENCY analysis!")
        print("")
        print(f"{len(D['builtin'])} BUILTIN modules from {len(D['builtin_pkg'])} packages required:")
        print(f"{D['builtin']}")
        print("")
        print(f"{len(D['known'])} KNOWN modules from {len(D['known_pkg'])} packages required:")
        print(f"{D['known']}")
        print("")
        print(f"{len(D['user'])} USER modules from {len(D['user_pkg'])} packages required:")
        print(f"{D['user']}")
        print("-"*64)

    # store results to file?
    if (save_dep):
        with open(os.path.join(project_path, 'requirements.info'), mode='wt') as df:
            df.write("================================================================================\n")
            df.write(f"DEPENDENCY Analysis for <{project}> @ {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            df.write("================================================================================\n")
            df.write("\n")
            df.write("--------------------------------------------------------------------------------\n")
            df.write("SUMMARY:\n")
            df.write(f" o Searched in {num_folders} folders / {num_files} files\n")
            df.write(f" o Found {len(D['builtin'])} builtin modules from {len(D['builtin_pkg'])} packages\n")
            df.write(f" o Found {len(D['known'])} known modules from {len(D['known_pkg'])} packages\n")
            df.write(f" o Found {len(D['user'])} user modules from {len(D['user_pkg'])} packages\n")
            df.write("--------------------------------------------------------------------------------\n")
            df.write("\n")
            df.write("---- BUILTIN modules ------------\n")
            df.write("\n")
            for item in D['builtin']:
                df.write(f"+ {item}\n")
            df.write("\n")
            df.write("---- KNOWN modules --------------\n")
            df.write("\n")
            for item in D['known']:
                df.write(f"+ {item}\n")
            df.write("\n")
            df.write("---- USER modules ---------------\n")
            df.write("\n")
            for item in D['user']:
                df.write(f"+ {item}\n")
            df.write("\n\n\n")
            if (show_imports):
                df.write("--------------------------------------------------------------------------------\n")
                df.write("---- LIST OF IMPORTS (by each source file) -------------------------------------\n")
                df.write("--------------------------------------------------------------------------------\n")               
                for src_file in D['imports']:
                    df.write("\n")
                    df.write(f"<{src_file}>\n")
                    for idx in range(len(D['imports'][src_file])):

                        df.write(f"    #{D['imports'][src_file][idx][1]:-4d}: {D['imports'][src_file][idx][0]}\n")
            else:
                df.write("NO LISTING of imports (from each source file) has been performed.\n")
            df.write("\n\n\n")
            if (trace_back):
                df.write("--------------------------------------------------------------------------------\n")
                df.write("---- BACK-TRACING OF DEPENDENCIES (for each requirements) ----------------------\n")
                df.write("--------------------------------------------------------------------------------\n")
                # Note: i.e. which module/package is required and imported by which source file?
                for dep_file in D['tracing']:
                    df.write("\n")
                    df.write(f"<{dep_file}>\n")
                    for idx in range(len(D['tracing'][dep_file])):
                        df.write(f"    {D['tracing'][dep_file][idx][0]} @ {D['tracing'][dep_file][idx][1]}\n")
            else:
                df.write("NO BACK-TRACING of dependencies (as required by source files) has been performed.\n")
            df.write("\n")

    # store list of package requirements? (e.g. for batch install in virtual environments)
    if (save_req):
        with open(os.path.join(project_path, 'requirements.txt'), mode='wt') as rf:
            for req in D['known_pkg']:
                try:
                    xyz = eval(f"__import__('{req}')")
                    rf.write(f"{req}=={xyz.__version__}\n")
                except:
                    rf.write(f"{req}\n")
        if ('xyz' in dir()):
            del xyz    

    return D


#### FULL
# def dependencies(root, excludes=['venv',], list_imports=False, trace_back=True, track_level=None,
#                  save_dep=True, save_req=False, verbose=False):
#     """ Lists all dependencies required for files in a given 'root' folder.

#     Args:
#         root (str): Base location for dependency search (e.g project folder).
#         excludes (list, optional): Subfolders in root that should be excluded from the search
#             (if any). Defaults to 'venv'.
#         list_imports (bool, optional): Switch for extracting the list of all import statements 
#             in the source files. Defaults to 'False'.
#         trace_back (bool, optional): Switch for adding a list of all "requesting" files 
#             associated w/ each dependency. Defaults to 'False'.

#         ###
#         ### TODO: trace_level ?
#         ###

#         save_dep (bool, optional): Switch for saving the results to 'dependencies.txt'.
#             Defaults to 'True'.
#         save_req (bool, optional): Switch for saving 'requirements.txt' for a batch install by
#             "pip" (e.g. 'pip install -r %FILE%' or via a FOR-loop). Defaults to 'True'.
#         verboes (bool, optional): Switch for status messages on the search. Defaults to 'False'.

#     Returns:
#         D (dict): Dict with keys 'builtin', 'builtin_pkg', 'known', 'known_pkg', 'user', 
#             'user_pkg' as well as 'imports' and 'traceback'. Note that the latter will only be
#             populated if tracing is activated, otherwise it will remain an empty list.
#     """

#     # init
#     root_norm = os.path.normpath(root)
#     project_path, project_name, _ = fileparts(root_norm)
#     if (project_name is None):
#         project = os.path.basename(project_path)
#     else:
#         project = project_name
#     D = { 'builtin': [], 'builtin_pkg': [],
#           'known': [], 'known_pkg': [],
#           'user': [], 'user_pkg': [],
#           'imports': {},
#           'tracing': {} }

#     if (verbose):
#         print("-"*64)
#         print(f"Starting DEPENDENCY analysis for <{project}>...")
#         print("")

#     # traverse all folders & files in project
#     num_folders, num_files = 0, 0
#     for path, _, files in os.walk(root_norm):
#         path_norm = os.path.normpath(path)
#         sub = path_norm.replace(root_norm+os.path.sep, '')

#         # respect excludes
#         checks = [sub.startswith(tree) for tree in excludes]
#         if (any(checks)):
#             if (verbose): print(f"o Excluded <{sub}>")
#             continue
#         else:
#             if (verbose): print(f"o Traversing FOLDER <{sub}>")
#             num_folders += 1

#         # check all relevant files
#         for fname in files:
#             if (fname.endswith(DEP_FILE_TYPES)):
#                 with open(os.path.abspath(os.path.join(path_norm, fname)), mode='rt') as pf:
#                     src_file = pf.buffer.name
#                     if (verbose): print(f"  + Checking FILE '{src_file}'")                    
#                     num_files += 1
                   
#                     inside_doc_string = False
#                     for n, line in enumerate(pf.readlines(), start=1):

#                         # determine indentation level
#                         indent_level = 0
#                         whites = _RX_WHITESPACE.match(line)
#                         if (whites): indent_level = int(whites.end()/4)                        

#                         line = line.strip()
                        
#                         # skip DOC-STRINGS
#                         chkdoc = line.split(S_DOC_STR_QUOTES)
#                         if (chkdoc[0] != line):                            
#                             if (inside_doc_string):                                
#                                 inside_doc_string = False # leaving
#                             elif (len(chkdoc) == 2):
#                                 inside_doc_string = True # entering
#                             else: # (len(chkdoc) == 3)
#                                 pass # doc-string is entered & left on the same line!                            
#                         if (inside_doc_string):
#                             continue

#                         # skip COMMENTS (only "full-comment" lines)
#                         if (line.startswith('#')):
#                             continue
                            
#                         # check for dependency                        
#                         dep_type = None
#                         if (not indent_level): # @ top level
#                             if (not dep_type):
#                                 chk = _RX_IMPORT_FROM.match(line)
#                                 if (chk): dep_type = 'from_import'
#                             if (not dep_type):
#                                 chk = _RX_IMPORT.match(line)
#                                 if (chk): dep_type = 'import'                           
#                         else: # @ function/class definitions                           
#                             if (not dep_type):
#                                 chk = _RX_IMPORT_FROM.search(line)
#                                 if (chk): dep_type = 'from_import_in_func'
#                             if (not dep_type):
#                                 chk = _RX_IMPORT.search(line)
#                                 if (chk): dep_type = 'import_in_func'

#                         if (not dep_type):
#                             continue # with next line in file

#                         # validation checks for robustness
#                         before = line[:chk.span()[0]]
#                         after = line[chk.span()[1]:]
#                         if (_RX_QUOTES.search(before)):
#                             if (verbose): print(f"    - #{n:-4d}: match, but discarded since in string expression")
#                             continue

#                         # record new dependency                        
#                         mod_name = chk.groupdict()['module']
#                         pkg_name = mod_name.split('.')[0]
#                         # pkg_name = mod_name.split('.')[:-1]

#                         if (pkg_name in DEP_PKG_BUILTIN):
#                             if (mod_name not in D['builtin']):
#                                 D['builtin'].append(mod_name)
#                         elif (pkg_name in DEP_PKG_KNOWN):
#                             if (mod_name not in D['known']):
#                                 D['known'].append(mod_name)
#                         elif (mod_name not in D['user']):                           
#                             D['user'].append(mod_name)

#                         # track source files' import lists?
#                         if (list_imports):
#                             line_cleaned = line.split('#')[0].strip()
#                             if (fname not in  D['imports'].keys()):
#                                 D['imports'][fname] = [(line_cleaned, n),]
#                             else:
#                                 D['imports'][fname].append((line_cleaned, n))

#                         # track dependencies to requesting source files?
#                         if (trace_back):
#                             if (mod_name not in D['tracing'].keys()):
#                                 D['tracing'][mod_name] = [(src_file, n),]
#                             else:
#                                 D['tracing'][mod_name].append((src_file, n))

#                         if (verbose):
#                             if (dep_type == 'import'):
#                                 print(f"    - #{n:-4d}: depends on module <{mod_name}>")
#                             elif (dep_type == 'from_import'):
#                                 print(f"    - #{n:-4d}: depends on (parts of) module <{mod_name}>")
#                             elif (dep_type == 'import_in_func'):
#                                 print(f"    - #{n:-4d}: some function depends on module <{mod_name}>")
#                             else: # (dep_type == 'from_import_in_func')
#                                 print(f"    - #{n:-4d}: some function depends on (parts of) module <{mod_name}>")

#     # sort modules dependencies & identify packages
#     D['builtin'].sort(key=lambda item: item.lower())
#     for item in D['builtin']:
#         pkg = item.split('.')[0]
#         if (pkg not in D['builtin_pkg']): D['builtin_pkg'].append(pkg)
#     D['known'].sort(key=lambda item: item.lower())
#     for item in D['known']:
#         pkg = item.split('.')[0]
#         if (pkg not in D['known_pkg']): D['known_pkg'].append(pkg)
#     D['user'].sort(key=lambda item: item.lower())
#     for item in D['user']:
#         pkg = item.split('.')[0]
#         if (pkg not in D['user_pkg']): D['user_pkg'].append(pkg)

#     # sort import lists and traceback (if any)
#     chk = dict(sorted(D['imports'].items(), key=lambda item: item[0].lower()))
#     D['imports'] = chk
#     for item in D['imports']:
#         if (type(item) is list): item.sort(key=lambda item: item.lower())

#     chk = dict(sorted(D['tracing'].items(), key=lambda item: item[0].lower()))
#     D['tracing'] = chk
#     for item in D['tracing']:
#         if (type(item) is list): item.sort(key=lambda item: item.lower())
    
#     # print summary
#     if (verbose):
#         print("")
#         print("...finished DEPENDENCY analysis!")
#         print("")
#         print(f"{len(D['builtin'])} BUILTIN modules from {len(D['builtin_pkg'])} packages required:")
#         print(f"{D['builtin']}")
#         print("")
#         print(f"{len(D['known'])} KNOWN modules from {len(D['known_pkg'])} packages required:")
#         print(f"{D['known']}")
#         print("")
#         print(f"{len(D['user'])} USER modules from {len(D['user_pkg'])} packages required:")
#         print(f"{D['user']}")
#         print("-"*64)

#     # #
#     # # FIXME: how to do 2nd-level checks? (i.e. what files req by/inside req files?)
#     # # if (trace_level > 1)
#     # print("<<<<<<<<<<<<<<<<< TEST ON 2nd LEVEL CHECK >>>>>>>>>>>>>>>>>>>>>>>>>>>>")
#     #
#     # for dep_file in D['user']:
#     #     print(f"==> look at  {dep_file}")
#     #     exec(f"import {dep_file} as THE_MODULE")
#     #     time.sleep(0.5)
#     #     THE_FILE = inspect.getsourcefile(THE_MODULE) # .getfile
#     #     THE_CONTENTS = inspect.getsource(THE_MODULE)
#     #     print(CHK_PATH)
#     #
#     # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")


#     # store results to file?
#     if (save_dep):
#         with open(os.path.join(project_path, 'dependencies.txt'), mode='wt') as df:
#             df.write("================================================================================\n")
#             df.write(f"DEPENDENCIES for <{project}> @ {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
#             df.write("================================================================================\n")
#             df.write("\n")
#             df.write("--------------------------------------------------------------------------------\n")
#             df.write("SUMMARY:\n")
#             df.write(f" o Searched in {num_folders} folders / {num_files} files\n")
#             df.write(f" o Found {len(D['builtin'])} builtin modules from {len(D['builtin_pkg'])} packages\n")
#             df.write(f" o Found {len(D['known'])} known modules from {len(D['known_pkg'])} packages\n")
#             df.write(f" o Found {len(D['user'])} user modules from {len(D['user_pkg'])} packages\n")
#             df.write("--------------------------------------------------------------------------------\n")
#             df.write("\n")
#             df.write("---- BUILTIN modules ------------\n")
#             df.write("\n")
#             for item in D['builtin']:
#                 df.write(f"+ {item}\n")
#             df.write("\n")
#             df.write("---- KNOWN modules --------------\n")
#             df.write("\n")
#             for item in D['known']:
#                 df.write(f"+ {item}\n")
#             df.write("\n")
#             df.write("---- USER modules ---------------\n")
#             df.write("\n")
#             for item in D['user']:
#                 df.write(f"+ {item}\n")
#             df.write("\n\n\n")
#             if (list_imports):
#                 df.write("--------------------------------------------------------------------------------\n")
#                 df.write("---- LIST OF IMPORTS (by each source file) -------------------------------------\n")
#                 df.write("--------------------------------------------------------------------------------\n")               
#                 for src_file in D['imports']:
#                     df.write("\n")
#                     df.write(f"<{src_file}>\n")
#                     for idx in range(len(D['imports'][src_file])):

#                         df.write(f"    #{D['imports'][src_file][idx][1]:-4d}: {D['imports'][src_file][idx][0]}\n")
#             else:
#                 df.write("NO LISTING of imports (from each source file) has been performed.\n")
#             df.write("\n\n\n")
#             if (trace_back):
#                 df.write("--------------------------------------------------------------------------------\n")
#                 df.write("---- BACK-TRACING OF DEPENDENCIES (for each requirements) ----------------------\n")
#                 df.write("--------------------------------------------------------------------------------\n")
#                 # Note: i.e. which module/package is required and imported by which source file?
#                 for dep_file in D['tracing']:
#                     df.write("\n")
#                     df.write(f"<{dep_file}>\n")
#                     for idx in range(len(D['tracing'][dep_file])):
#                         df.write(f"    {D['tracing'][dep_file][idx][0]} @ {D['tracing'][dep_file][idx][1]}\n")
#             else:
#                 df.write("NO BACK-TRACING of dependencies (as required by source files) has been performed.\n")
#             df.write("\n")

#     # store list of package requirements? (e.g. for batch install in virtual environments)
#     if (save_req):
#         with open(os.path.join(project_path, 'requirements.txt'), mode='wt') as rf:
#             for req in D['known_pkg']:
#                 try:
#                     xyz = eval(f"__import__('{req}')")
#                     rf.write(f"{req}=={xyz.__version__}\n")
#                 except:
#                     rf.write(f"{req}\n")
#         if ('xyz' in dir()):
#             del xyz    

#     return D


def quickplay(x, fs=48000, dtype=np.int16, normalise=True, device='default'):
    """ Quickly plays 'x' as an audio signal.

    Args:
        x (array-type): Any array type, will be converted to 'ndarray'.
        fs (float, optional): Sampling rate for playback.
        normalise (bool, optional): Switch for normalising volume. Defaults to 'True'.
        device (str, optional): Playback device. Defaults to 'default'.

    Returns:
        --
    """

    if (type(x) is not np.ndarray):
        x = np.array(x)

    if (normalise):
        x_peak = np.max(np.abs(x))
        xn = x / x_peak
    else:
        xn = x

    if (dtype is None):
        dtype = xn.dtype
        xs = xn
    elif (dtype == np.int16):
        xs = xn * 32767 # 16-bit signed integer
        xs = xs.astype(dtype)

    # PortAudio
    player = sd.OutputStream(samplerate=fs, channels=1, dtype=dtype)
    player.start()
    player.write(xs)

    return

qplay = partial(quickplay, device='default')
