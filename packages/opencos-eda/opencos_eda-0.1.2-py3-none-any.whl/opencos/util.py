
# SPDX-License-Identifier: MPL-2.0

import sys
import subprocess
import datetime
import os
import time
import atexit
import shutil
import traceback
import argparse

# Conditional imports for loading this as a module instead of package
# where someone may not have pyyaml installed.
try:
    import yaml
except:
    pass

global_exit_allowed = False
progname = "UNKNOWN"
progname_in_message = True
logfile = None
loglast = 0
debug_level = 0

args = {
    'color' : True,
    'quiet' : False,
    'verbose' : False,
    'debug' : False,
    'fancy' : sys.stdout.isatty(),
    'warnings' : 0,
    'errors' : 0,
}

def yaml_safe_load(filepath:str):
    '''Returns dict or None from filepath (str)'''

    data = None
    with open(filepath) as f:
        debug(f'Opened {filepath=}')

        if 'yaml' not in globals().keys():
            util.error(
                'package "yaml" (via pyyaml) was not imported,' \
                + f' yet we encountered a {filepath=} file that needs to be parsed.' \
                + ' Please pip install pyyaml or similar.'
                        )

        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            if hasattr(e, 'problem_mark'):
                mark = e.problem_mark
                error(f"Error parsing {filepath=}: line {mark.line + 1}, column {mark.column +1}: {e.problem}")
            else:
                error(f"Error loading YAML {filepath=}:", e)

    return data


def yaml_safe_writer(data:dict, filepath:str) -> None:

    if filepath.endswith('.yml'):
        if 'yaml' not in globals().keys():
            warning(
                'package "yaml" (via pyyaml) was not imported, ' \
                + f' yet we would like to save {filepath=}, skipping'
            )
        else:
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False)
    else:
        warning(f'{filepath=} to be written for this extension not implemented.')



def start_log(filename, force=False):
    global logfile, loglast
    if os.path.exists(filename):
        if force:
            info(f"Overwriting '{filename}', which exists, due to --force-logfile.")
        else:
            error(f"The --logfile path '{filename}' exists.  Use --force-logfile (vs --logfile) to override.")
    try:
        logfile = open( filename, 'w')
        debug(f"Opened logfile '{filename}' for writing")
    except Exception as e:
        error(f"Error opening '{filename}' for writing!")

def write_log(text, end):
    global logfile, loglast
    sw = text.startswith(f"INFO: [{progname}]")
    if (((time.time() - loglast) > 10) and
        (text.startswith(f"DEBUG: [{progname}]") or
         text.startswith(f"INFO: [{progname}]") or
         text.startswith(f"WARNING: [{progname}]") or
         text.startswith(f"ERROR: [{progname}]"))):
        dt = datetime.datetime.now().ctime()
        print(f"INFO: [{progname}] Time: {dt}", file=logfile)
        loglast = time.time()
    print(text, end=end, file=logfile)
    logfile.flush()
    os.fsync(logfile)

def stop_log():
    global logfile, loglast
    if logfile:
        debug(f"Closing logfile")
        logfile.close()
    logfile = None
    loglast = 0

atexit.register(stop_log)

def get_argparse_bool_action_kwargs():
    bool_kwargs = dict()
    x = getattr(argparse, 'BooleanOptionalAction', None)
    if x is not None:
        bool_kwargs['action'] = x
    else:
        bool_kwargs['action'] = 'store_true'
    return bool_kwargs


def process_tokens(tokens:list):
    global debug_level

    parser = argparse.ArgumentParser(prog='util.process_tokens', add_help=False, allow_abbrev=False)
    # We set allow_abbrev=False so --force-logfile won't try to attempt parsing shorter similarly
    # named args like --force, we want those to go to unparsed list.
    # For bools, support --color and --no-color with this action=argparse.BooleanOptionalAction
    # -- however Python3.8 and older does not support this, so as a workaround, use kwargs for
    #    boolean actions:
    bool_action_kwargs = get_argparse_bool_action_kwargs()

    parser.add_argument('--color', **bool_action_kwargs)
    parser.add_argument('--quiet', **bool_action_kwargs)
    parser.add_argument('--verbose', **bool_action_kwargs)
    parser.add_argument('--fancy', **bool_action_kwargs)
    parser.add_argument('--debug', **bool_action_kwargs)
    parser.add_argument('--debug-level', type=int, default=0)
    parser.add_argument('--logfile', type=str, default='')
    parser.add_argument('--force-logfile', type=str, default='')
    parser.add_argument('--no-respawn', action='store_true')
    try:
        parsed, unparsed = parser.parse_known_args(tokens + [''])
        unparsed = list(filter(None, unparsed))
    except argparse.ArgumentError:
        error(f'problem attempting to parse_known_args for {tokens=}')

    debug(f'util.process_tokens: {parsed=} {unparsed=}  from {tokens=}')

    if parsed.debug_level: set_debug_level(parsed.debug_level)
    elif parsed.debug:     set_debug_level(1)
    else:                  debug_level = 0

    if parsed.force_logfile != '':
        start_log(parsed.force_logfile, force=True)
    elif parsed.logfile != '':
        start_log(parsed.logfile, force=False)

    parsed_as_dict = vars(parsed)
    for key,value in parsed_as_dict.items():
        if value is not None:
            args[key] = value # only update with non-None values to our global 'args' dict
    return parsed_as_dict, unparsed

# ********************
# fancy support
# In fancy mode, we take the bottom fancy_lines_ lines of the screen to be written using fancy_print,
# while the lines above that show regular scrolling content (via info, debug, warning, error above).
# User should not use print() when in fancy mode

fancy_lines_ = []

def fancy_start(fancy_lines = 4, min_vanilla_lines = 4):
    global fancy_lines_
    (columns,lines) = shutil.get_terminal_size()
    if (fancy_lines < 2):
        error(f"Fancy mode requires at least 2 fancy lines")
    if (fancy_lines > (lines-min_vanilla_lines)):
        error(f"Fancy mode supports at most {(lines-min_vanilla_lines)} fancy lines, given {min_vanilla_lines} non-fancy lines")
    if len(fancy_lines_): error(f"We are already in fancy line mode??")
    for _ in range(fancy_lines-1):
        print("") # create the requisite number of blank lines
        fancy_lines_.append("")
    print("", end="") # the last line has no "\n" because we don't want ANOTHER blank line below
    fancy_lines_.append("")
    # the cursor remains at the leftmost character of the bottom line of the screen

def fancy_stop():
    global fancy_lines_
    if len(fancy_lines_): # don't do anything if we aren't in fancy mode
        # user is expected to have painted something into the fancy lines, we can't "pull down" the regular
        # lines above, and we don't want fancy_lines_ blank or garbage lines either, that's not pretty
        fancy_lines_ = []
        # since cursor is always left at the leftmost character of the bottom line of the screen, which was
        # one of the fancy lines which now has the above-mentioned "something", we want to move one lower
        print("")

def fancy_print(text, line):
    global fancy_lines_
    # strip any newline, we don't want to print that
    if text.endswith("\n"): text.rstrip()
    lines_above = len(fancy_lines_) - line - 1
    if lines_above:
        print(f"\033[{lines_above}A"+ # move cursor up
              text+f"\033[1G"+ # desired text, then move cursor to the first character of the line
              f"\033[{lines_above}B", # move the cursor down
              end="", flush=True)
    else:
        print(text+f"\033[1G", # desired text, then move cursor to the first character of the line
              end="", flush=True)
    fancy_lines_[line] = text

def print_pre():
    # stuff we do before printing any line
    if len(fancy_lines_):
        # Also, note that in fancy mode we don't allow the "above lines" to be partially written, they
        # are assumed to be full lines ending in "\n"
        # As always, we expect the cursor was left in the leftmost character of bottom line of screen
        print(f"\033[{len(fancy_lines_)-1}A"+ # move the cursor up to where the first fancy line is drawn
              f"\033[0K", # clear the old fancy line 0
              end="",flush=True)

def print_post(text, end):
    # stuff we do after printing any line
    if len(fancy_lines_):
        #time.sleep(1)
        # we just printed a line, including a new line, on top of where fancy line 0 used to be, so cursor
        # is now at the start of fancy line 1.
        # move cursor down to the beginning of the final fancy line (i.e. standard fancy cursor resting place)
        for x in range(len(fancy_lines_)):
            print("\033[0K",end="") # erase the line to the right
            print(fancy_lines_[x],flush=True,end=('' if x==(len(fancy_lines_)-1) else '\n'))
            #time.sleep(1)
        print("\033[1G", end="", flush=True)
    if logfile: write_log(text, end=end)

string_red = f"\x1B[31m"
string_green = f"\x1B[32m"
string_orange = f"\x1B[33m"
string_yellow = f"\x1B[39m"
string_normal = f"\x1B[0m"

def print_red(text, end='\n'):
    print_pre()
    print(f"{string_red}{text}{string_normal}" if args['color'] else f"{text}", end=end, flush=True)
    print_post(text, end)

def print_green(text, end='\n'):
    print_pre()
    print(f"{string_green}{text}{string_normal}" if args['color'] else f"{text}", end=end, flush=True)
    print_post(text, end)

def print_orange(text, end='\n'):
    print_pre()
    print(f"{string_orange}{text}{string_normal}" if args['color'] else f"{text}", end=end, flush=True)
    print_post(text, end)

def print_yellow(text, end='\n'):
    print_pre()
    print(f"{string_yellow}{text}{string_normal}" if args['color'] else f"{text}", end=end, flush=True)
    print_post(text, end)

def set_debug_level(level):
    global debug_level
    debug_level = level
    args['debug'] = (level > 0)
    args['verbose'] = (level > 1)
    info(f"Set debug level to {debug_level}")

# the <<d>> stuff is because we change progname after this is read in.  if we instead infer progname or
# get it passed somehow, we can avoid this ugliness / performance impact (lots of calls to debug happen)
def debug(text, level=1, start='<<d>>', end='\n'):
    if start=='<<d>>': start = f"DEBUG: " + (f"[{progname}] " if progname_in_message else "")
    if args['debug'] and (((level==1) and args['verbose']) or (debug_level >= level)):
        print_yellow(f"{start}{text}", end=end)

def info(text, start='<<d>>', end='\n'):
    if start=='<<d>>': start = f"INFO: " + (f"[{progname}] " if progname_in_message else "")
    if not args['quiet']:
        print_green(f"{start}{text}", end=end)

def warning(text, start='<<d>>', end='\n'):
    if start=='<<d>>': start = f"WARNING: " + (f"[{progname}] " if progname_in_message else "")
    args['warnings'] += 1
    print_orange(f"{start}{text}", end=end)

def error(text, error_code=-1, do_exit=True, start='<<d>>', end='\n'):
    if start=='<<d>>': start = f"ERROR: " + (f"[{progname}] " if progname_in_message else "")
    args['errors'] += 1
    print_red(f"{start}{text}", end=end)
    if do_exit:
        if args['debug']: print(traceback.print_stack())
        return exit(error_code)
    else:
        if error_code is None:
            return 0
        else:
            return abs(int(error_code))

def exit(error_code=0, quiet=False):
    if global_exit_allowed:
        if not quiet: info(f"Exiting with {args['warnings']} warnings, {args['errors']} errors")
        sys.exit(error_code)

    if error_code is None:
        return 0
    else:
        return abs(int(error_code))

def getcwd():
    try:
        cc = os.getcwd()
    except Exception as e:
        error("Unable to getcwd(), did it get deleted from under us?")
    return cc

_oc_root=None
_oc_root_set=False
def get_oc_root(error_on_fail:bool=False):
    global _oc_root
    global _oc_root_set
    '''Returns a str or False for the root directory of *this* repo.

    If environment variable OC_ROOT is set, that is used instead, otherwise attempts to use
    `git rev-parse`
    '''
    # if we've already run through here once, just return the memorized result
    if _oc_root_set: return _oc_root

    # try looking for an env var
    s = os.environ.get('OC_ROOT')
    if s:
        # TODO: is this really highest priority?
        debug(f'get_oc_root() -- returning from env: {s=}')
        _oc_root = s.strip()
    else:
        # try asking GIT
        cp = subprocess.run('git rev-parse --show-toplevel', stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                            shell=True, universal_newlines=True)
        if cp.returncode != 0:
            # TODO: at some point, address the fact that not all repos are oc_root.  Is this function asking for
            # the repo we are in?  or a pointer to the oc_root which maybe elsewhere on the system?
            if error_on_fail: error(f'Unable to get a OC_ROOT directory using git rev-parse')
            else:             info(f'Unable to get a OC_ROOT directory using git rev-parse')
        else:
            _oc_root = cp.stdout.strip()

    # there is no sense running through this code more than once
    _oc_root_set = True
    return _oc_root

def string_or_space(text, whitespace=False):
    if whitespace:
        return " " * len(text)
    else:
        return text

def sprint_time(s):
    s = int(s)
    txt = ""
    do_all = False
    # days
    if (s >= (24*60*60)): # greater than 24h, we show days
        d = int(s/(24*60*60))
        txt += f"{d}d:"
        s -= (d*24*60*60)
        do_all = True
    # hours
    if do_all or (s >= (60*60)):
        d = int(s/(60*60))
        txt += f"{d:2}:"
        s -= (d*60*60)
        do_all = True
    # minutes
    d = int(s/(60))
    txt += f"{d:02}:"
    s -= (d*60)
    # seconds
    txt += f"{s:02}"
    return txt


def safe_mkdirs(base : str, new_dirs : list):
    for p in new_dirs:
        p = os.path.join(base, p)
        try:
            os.mkdir(p)
        except:
            try:
                os.system(f'mkdir -p {p}')
            except FileExistsError:
                pass
            else:
                error(f'unable to mkdir {p=}')

def write_shell_command_file(dirpath : str, filename : str, command_lists : list, line_breaks : bool = False):
    ''' Writes new file at {dirpath}/{filename} as a bash shell command, using command_lists (list of lists)

    -- dirpath (str)        -- directory where file is written (usually eda.work/{target}_sim
    -- filename (str)       -- filename, for example compile_only.sh
    -- command_lists (list) -- list of lists. each item in the list is a list of commands (aka, how
                               subprocess.run(args) uses a list of commands.
    -- line_breaks (bool)   -- Set to True to have 1 word per line in the file followed by a line break.
                               Default False has an entry in command_lists all on a single line.

    Returns None, writes the file and chmod's it to 0x755.

    '''
    # command_lists should be a list-of-lists.
    bash_path = shutil.which('bash')
    assert type(command_lists) is list, f'{command_lists=}'
    fullpath = os.path.join(dirpath, filename)
    with open(fullpath, 'w') as f:
        f.write('#!' + bash_path + '\n\n')
        for c in command_lists:
            assert type(c) is list, f'{c=} (c must be a list) {command_lists=}'
            if len(c) > 0:
                if line_breaks:
                    # line_breaks=True - have 1 word per line, followed by \ \n
                    sep = " \\" + "\n"
                    f.write(sep.join(c))
                    f.write(" ;\n")
                else:
                    # line_break=False (default) - all words on 1 line.
                    f.write(' '.join(c))
                    f.write(" ;\n")
            else:
                f.write("\n")
        f.write("\n")
        f.close()
        os.chmod(fullpath, 0o755)


def write_eda_config_and_args(dirpath : str, filename='eda_config.yml', command_obj_ref=None):
    if command_obj_ref is None:
        return
    fullpath = os.path.join(dirpath, filename)
    data = dict()
    for x in ['command_name', 'target', 'original_args', 'config', 'args', 'modified_args', 'files_v', 'files_sv', 'files_vhd']:
        data[x] = getattr(command_obj_ref, x, None)
    data['command_name'] = command_obj_ref.command_name

    yaml_safe_writer(data=data, filepath=fullpath)
