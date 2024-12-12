#!/usr/bin/env python3

# SPDX-License-Identifier: MPL-2.0

import time
import subprocess
import os
import sys
import shutil
import re
import queue
import threading
import signal
import curses
import pathlib
import yaml
import argparse
import glob

from opencos import seed, deps_helpers, util

# Globals

debug_respawn = False
util.progname = "EDA"

# pyton 3.7+ dict() are ordered.
glbl_auto_tools_ordered = {
    # order these in a logical default.  Default to the "better" tool, by loading it first
    # ( name, executable, command-handler dict() )
    'verilator': {
        'exe': 'verilator',
        'handlers': {
            'elab': 'CommandElabVerilator',
            'sim': 'CommandSimVerilator',
        },
    },

    'gtkwave': {
        'exe': 'gtkwave',
        'handlers': {},
    },

    'vivado': {
        'exe': 'vivado',
        'handlers': {
            'elab': 'CommandElabVivado',
            'sim': 'CommandSimVivado',
            'synth': 'CommandSynthVivado',
            'proj': 'CommandProjVivado',
            'upload': 'CommandUploadVivado',
            'open': 'CommandOpenVivado',
            'flist': 'CommandFListVivado',
            'build': 'CommandBuildVivado',
        },
    },

    'questa': {
        'exe': 'qrun',
        'handlers': {
            'elab': 'CommandElabQuesta',
            'sim': 'CommandSimQuesta',
        },
    },

    'modelsim_ase': {
        'exe': 'vsim',
        'handlers': {
            'elab': 'CommandElabModelsimAse',
            'sim': 'CommandSimModelsimAse',
        },
    },

    'iverilog': {
        'exe': 'iverilog',
        'handlers': {
            'elab': 'CommandElabIverilog',
            'sim': 'CommandSimIverilog',
        },
    },
}

glbl_auto_tools_found = dict()
glbl_tools_loaded = set()

config = {
    'command_handler': dict(), # This is populated prior to calling main(), and overriden by tool_setup(..)
    'defines'        : {},

    'dep_command_enables': {
        'shell'            : True, # Enable DEPS to process shell@ commands.
        'work_dir_add_srcs': True, # Enable DEPS to process work_dir_add_srcs@ commands
        'peakrdl'          : True, # Enable DEPS to process peakrdl@ commands
    },
    'deps_yaml_supported': True,

    'dep_sub'                       : [ [ r'csr\@(\w+)\.txt', r'\1.sv@csrgen,\1.txt $root_dir/v_csr_regs_deps'], ],
    'vars'                          : { 'root_dir' : os.path.abspath(util.getcwd()) },
}

# Classes

class Tool:
    args = dict()
    error = util.error # use that module's method
    def __init__(self):
        self.args['tool'] = None
        self.args['xilinx'] = False


class Command:
    args = {
        "keep" : False,
        "force" : False,
        "fake" : False,
        "stop-before-compile": False,   # Usually in the self.do_it() method, stop prior to compile/elaborate/simulate
        "stop-after-compile": False,
        "stop-after-elaborate": False,  # Set to True to only run compile + elaboration (aka compile + lint)
        "lint": False, # Same as stop-after-elaborate
        "eda-dir" : "eda.work", # all eda jobs go in here
        "job-name" : "", # this is used to create a certain dir under "eda_dir"
        "work-dir" : "", # this can be used to run the job in a certain dir, else it will be <eda-dir>/<job-name> else <eda-dir>/<target>_<command>
        "sub-work-dir" : "", # this can be used to name the dir built under <eda-dir>, which seems to be same function as job-name??
        "suffix" : "",
        "design" : "", # not sure how this relates to top
        "logfile" : "",
    }
    def __init__(self, config:dict, command_name:str):
        self.modified_args = {}
        self.config = config
        self.command_name = command_name
        self.target = ""
        self.status = 0

    def error(self, *args, **kwargs):
        '''Returns None, child classes can call self.error(..) instead of util.error, which updates their self.status.'''
        self.status = util.error(*args, **kwargs)

    def create_work_dir(self):
        if (not os.path.exists(self.args['eda-dir'])): # use os.path.isfile / isdir also
            os.mkdir(self.args['eda-dir'])
        if self.args['design'] == "":
            if ('top' in self.args) and (self.args['top'] != ""):
                self.args['design'] = self.args['top']
            else:
                self.args['design'] = "design" # generic, i.e. to create work dir "design_upload"
        if self.target == "":
            self.target = self.args['design']
        if self.args['work-dir'] == '':
            if self.args['sub-work-dir'] == '':
                if self.args['job-name'] != '':
                    self.args['sub-work-dir'] = self.args['job-name']
                else:
                    self.args['sub-work-dir'] = f'{self.target}_{self.command_name}'
            self.args['work-dir'] = os.path.join(self.args['eda-dir'], self.args['sub-work-dir'])
        keep_file = os.path.join(self.args['work-dir'], "eda.keep")
        if (os.path.exists(self.args['work-dir'])):
            if os.path.exists(keep_file) and not self.args['force']:
                self.error(f"Cannot remove old work dir due to '{keep_file}'")
            util.info(f"Removing previous '{self.args['work-dir']}'")
            shutil.rmtree(self.args['work-dir'])
        os.mkdir(self.args['work-dir'])
        if (self.args['keep']):
            open(keep_file, 'w').close()
        util.info(f'Creating work-dir: {self.args["work-dir"]=}')
        return self.args['work-dir']

    def exec(self, work_dir, command_list, background=False, stop_on_error=True, quiet=False):
        if not quiet:
            util.info("exec: %s (in %s)" % (' '.join(command_list), work_dir))
        original_cwd = util.getcwd()
        os.chdir(work_dir)
        if self.args['fake']:
            util.info(f"FAKE: would have called os.system({' '.join(command_list)})")
            return "", "", 0
        elif not background:
            stdout = "" # these will be send direct to screen
            stderr = ""
            util.debug(f"About to call os.system({' '.join(command_list)})")
            return_code = os.system(" ".join(command_list)) >> 8
        elif True:
            util.debug(f"about to call subprocess.Popen({' '.join(command_list)})")
            PIPE=subprocess.PIPE
            STDOUT=subprocess.STDOUT
            proc = subprocess.Popen(command_list, stdout=PIPE, stderr=STDOUT)
            util.debug(f"about to call proc.communicate")
            stdout, stderr = proc.communicate()
            return_code = proc.returncode
            stdout = stdout.decode('utf-8') if stdout else ""
            stderr = stderr.decode('utf-8') if stderr else ""
            util.debug(f"stdout={stdout}")
            util.debug(f"stderr={stderr}")
            util.debug(f"return_code={return_code}")
        else:
            try:
                util.debug(f"about to call subprocess.check_output({' '.join(command_list)})")
                return_code = subprocess.check_output(command_list, stdout=subprocess.PIPE,stderr=subprocess.STDOUT).decode("utf-8")
                util.debug(f"subprocess.check_output result={return_code}")
            except subprocess.CalledProcessError as e:
                self.error(f"FAIL: {e.output.decode('utf-8')}")
                return "<BAD>", "", 1
            except KeyboardInterrupt as e:
                util.fancy_stop()
                util.info('EXEC: Control-C detected...')
                util.exit(-1)
                self.status += 1
                return "", "", 1
            except:
                e = sys.exc_info()[0]
                self.error(f"UNKNOWN FAIL: {str(e)}")
                return "<BAD>", "", 1

        os.chdir(original_cwd)
        if return_code:
            self.status += return_code
            if stop_on_error: self.error(f"exec: returned with error (return code: {return_code})")
            else            : util.debug(f"exec: returned with error (return code: {return_code})")
        else:
            util.debug(f"exec: returned without error (return code: {return_code})")
        return stderr, stdout, return_code

    def set_arg(self, key, value):

        # Do some minimal type handling, preserving the type(self.args[key])

        if type(self.args[key]) is dict:
            # if dict, update
            self.args[key].update(value)

        elif type(self.args[key]) is list:
            # if list, append (no duplicates)
            if type(value) is list:
                for x in value:
                    if x not in self.args[key]:
                        self.args[key].append(x)
            elif value not in self.args[key]:
                self.args[key].append(value)

        elif type(self.args[key]) is bool:
            # if bool, then attempt to convert string or int
            if type(value) in [bool, int]:
                self.args[key] = bool(value)
            elif type(value) is str:
                if value.lower() in ['false', '0']:
                    self.args[key] = False
                else:
                    self.args[key] = True
            else:
                raise Exception(f'set_arg({key=}, {value=}) bool, {type(self.args[key])=} {type(value)=}')

        elif type(self.args[key]) is int:
            # if int, attempt to convert string or bool
            if type(value) in [bool, int, str]:
                self.args[key] = int(value)
            else:
                raise Exception(f'set_arg({key=}, {value=}) int, {type(self.args[key])=} {type(value)=}')


        else:
            # else overwrite it as-is.
            self.args[key] = value

        self.modified_args[key] = True
        util.debug(f'Set arg["{key}"]="{self.args[key]}"')
        # we trap the writing of logfile here, because we must act immediately
        if key == "logfile": util.start_log(value)


    def get_argparser(self):
        ''' Returns an argparse.ArgumentParser() based on self.args (dict)'''

        # Preference is --args-with-dashes, which then become parsed.args_with_dashes, b/c
        # parsed.args-with-dashes is not legal python. Some of self.args.keys() still have - or _, so
        # this will handle both.
        # Also, preference is for self.args.keys(), to be str with - dashes
        parser = argparse.ArgumentParser(prog='eda', add_help=False, allow_abbrev=False)
        bool_action_kwargs = util.get_argparse_bool_action_kwargs()
        for key,value in self.args.items():
            if '_' in key and '-' in key:
                assert False, f'{self.args=} has {key=} with both _ and -, which is not allowed'
            if '_' in key:
                util.warning(f'{key=} has _ chars, prefer -')

            keys = [key] # make a list
            if '_' in key:
                keys.append(key.replace('_', '-')) # switch to POSIX dashes for argparse
            elif '-' in key:
                keys.append(key.replace('-', '_')) # also support --some_arg_with_underscores

            arguments = list() # list supplied to parser.add_argument(..) so one liner supports both.
            for this_key in keys:
                arguments.append(f'--{this_key}')

            # It's important to set the default=None on these, except for list types where default is list()
            # If the parsed Namespace has values set to None or [], we do not update. This means that as deps
            # are processed that have args set, they cannot override the top level args that were already set.
            # nor be overriden by defaults.
            if type(value) is bool:
                # For bool, support --key and --no-key with this action=argparse.BooleanOptionalAction.
                # Note, this means you cannot use --some-bool=True, or --some-bool=False, has to be --some-bool
                # or --no-some-bool.
                parser.add_argument(*arguments, default=None, help=f'{type(value).__name__} default={value}', **bool_action_kwargs)
            elif type(value) is list:
                parser.add_argument(*arguments, default=list(), action='append', help=f'{type(value).__name__} default={value}')
            elif type(value) in [int, str]:
                parser.add_argument(*arguments, default=None, type=type(value), help=f'{type(value).__name__} default={value}')
            elif value is None:
                parser.add_argument(*arguments, default=None, help=f'default={value}')
            else:
                assert False, f'{key=} {value=} how do we do argparse for this type of value?'

        return parser


    def run_argparser_on_list(self, tokens:list):
        ''' Creates an argparse.ArgumentParser() for all the keys in self.args, and attempts to parse
        from the provided list.

        Returns a list of the unparsed, or remaining, args from the provided list.
        '''

        if len(tokens) == 0:
            return list()
        parser = self.get_argparser()
        try:
            parsed, unparsed = parser.parse_known_args(tokens + [''])
            unparsed = list(filter(None, unparsed))
        except argparse.ArgumentError:
            util.error(f'problem attempting to parse_known_args for {tokens=}')

        parsed_as_dict = vars(parsed)
        for key,value in parsed_as_dict.items():
            # key should have _ instead of POSIX dashes, but we still support dashes like self.args['build-file'],
            # etc.
            if key not in self.args and '_' in key:
                # try with dashes instead of _
                key = key.replace('_', '-')
            assert key in self.args, f'{key=} not in {self.args=}'

            if value is None:
                continue # don't update a self.args[key] to None
            if type(value) is list and len(value) == 0:
                continue # don't update a self.args[key] that's a list() to an empty list.
            if type(value) is not list and self.modified_args.get(key, None):
                # For list types, we append. For all others they overwrite, so if we've already
                # modified the arg once, do not modify it again. Such as, command line set an arg,
                # but then a target tried to set it again; or a target set it, and then a dependent
                # target tried to set it again.
                util.debug(f"Command.run_argparser_on_list - skipping {key=} {value=} b/c arg is already modified.")
                continue
            if self.args[key] != value:
                util.debug(f"Command.run_argparser_on_list - setting set_arg b/c argparse -- {key=} {value=}")
                self.set_arg(key, value) # Note this has special handling for lists already.
                self.modified_args[key] = True

        return unparsed


    def process_tokens(self, tokens, process_all=True):
        '''Command.process_tokens(..) for all named self.args.keys() returns the unparsed tokens list'''

        unparsed = self.run_argparser_on_list(tokens)
        if process_all and len(unparsed) > 0:
            self.error(f"Didn't understand argument: '{unparsed=}' in {self.command_name=} context")

        return unparsed


    def do_it(self):
        self.error(f"No tool bound to command '{self.command_name}', you probably need to setup tool, or use '--tool <name>'")
        raise NotImplementedError

    def help(self):
        if self.command_name:
            util.info(f'Generic help for {self.command_name=}')
        else:
            util.info(f"Generic help (from class Command):")
        for k in sorted(self.args.keys()):
            v = self.args[k]
            if type(v) == bool :
                util.info(f"   {k:20} : boolean    : {v}")
            elif type(v) == int:
                util.info(f"   {k:20} : integer    : {v}")
            elif type(v) == list:
                util.info(f"   {k:20} : list       : {v}")
            elif type(v) == str:
                util.info(f"   {k:20} : string     : '{v}'")
            else:
                util.info(f"   {k:20} : <unknown>  : {v}")
        # TODO(drew): sort of less useful to also print out the help via argparse, so leave this off:
        #parser = self.get_argparser()
        #help_str = parser.format_help()
        #util.info(help_str)


class CommandDesign(Command):

    # Used by for DEPS work_dir_add_srcs@ commands, by class methods:
    #   update_file_lists_for_work_dir(..), and resolve_target(..)
    _work_dir_add_srcs_path_string = '@EDA-WORK_DIR@'

    def __init__(self, config:dict, command_name:str):
        Command.__init__(self, config=config, command_name=command_name)
        self.args.update({
            'seed': seed.get_seed(style="urandom"),
            'top': '',
            'all-sv': False,
        })
        self.defines = dict()
        self.incdirs = list()
        self.files = dict()
        self.targets = dict()
        self.files_v = list()
        self.files_sv = list()
        self.files_vhd = list()
        self.dep_shell_commands = list() # each list entry is a dict()
        self.dep_work_dir_add_srcs = set() # key: tuple (target_path, target_node, filename)
        self.oc_root = util.get_oc_root()
        for (d,v) in config.get('defines', dict()).items():
            self.defines[d] = v

        self.cached_deps_files = dict() # key = DEPS.yml file path, value = data.
        self.targets_dict = dict() # key = targets that we've already processed in DEPS files

    def run_dep_commands(self):
        # Run any shell@ commands from DEPS files
        self.run_dep_shell_commands()
        # Update any work_dir_add_srcs@ in our self.files, self.files_v, etc, b/c
        # self.args['work-dir'] now exists.
        self.update_file_lists_for_work_dir()

    def run_dep_shell_commands(self):
        # Runs from self.args['work-dir']
        all_cmds_lists = list()

        for iter,d in enumerate(self.dep_shell_commands):
            c = d['exec_list']
            all_cmds_lists.append([]) # blank line
            all_cmds_lists.append([f'# command {iter}: target: {d["target_path"]} : {d["target_node"]}']) # comment, where it came from
            all_cmds_lists.append(c)

        util.write_shell_command_file(dirpath=self.args['work-dir'], filename='pre_compile_dep_shell_commands.sh',
                                      command_lists=all_cmds_lists)

        # TODO(drew): currently I don't have a great way of scraping shell commands logs for errors
        for iter,d in enumerate(self.dep_shell_commands):
            util.info(f'run_dep_shell_commands {iter=}: {d=}')
            c = d['exec_list']
            self.exec(self.args['work-dir'], c)

    def update_file_lists_for_work_dir(self):
        if len(self.dep_work_dir_add_srcs) == 0:
            return

        # If we encounter any @EDA-WORK_DIR@some_file.v in self.files, self.files_v, etc, then replace it with:
        # self.args['work-dir'] / some_file.v:
        _work_dir_add_srcs_path_string_len = len(self._work_dir_add_srcs_path_string)
        work_dir_abspath = os.path.abspath(self.args['work-dir'])
        for key in list(self.files.keys()): # list so it's not an iterator, we're updating self.files.
            if type(key) is str and key.startswith(self._work_dir_add_srcs_path_string):
                new_key = os.path.join(work_dir_abspath, key[_work_dir_add_srcs_path_string_len :])
                self.files.pop(key)
                self.files[new_key] = True

        my_file_lists_list = [self.files_v, self.files_sv, self.files_vhd]
        for my_file_list in my_file_lists_list:
            for iter,value in enumerate(my_file_list):
                if value and type(value) is str and value.startswith(self._work_dir_add_srcs_path_string):
                    new_value = os.path.join(work_dir_abspath, value[_work_dir_add_srcs_path_string_len :])
                    my_file_list[iter] = new_value
                    util.debug(f"file lists: replaced {value} with {new_value}")



    def get_top_name(self, name):
        return os.path.splitext(os.path.basename(name))[0]

    def process_plusarg(self, plusarg:str, pwd=os.getcwd()):
        '''Retuns None, parses a +define+ or +incdir+ str and adds to self.defines or self.incdirs'''
        m = re.match(r'^\+define\+(\w+)$', plusarg)
        if m:
            k = m.group(1)
            self.defines[k] = None
            util.debug(f"Defined {k}")
            return
        m = re.match(r'^\+define\+(\w+)\=(\S+)$', plusarg)
        if m:
            k = m.group(1)
            v = m.group(2)
            m = re.match(r'^\"\%PWD\%\/(.*)\"$', v)
            if m: v = '"' + os.path.abspath(os.path.join(pwd, m.group(1))) + '"'
            m = re.match(r'^\%PWD\%\/(.*)$', v)
            if m: v = os.path.abspath(os.path.join(pwd, m.group(1)))
            self.defines[k] = v
            util.debug(f"Defined {k}={v}")
            return
        m = re.match(r'^\+incdir\+(\S+)$', plusarg)
        if m:
            incdir = m.group(1)
            if incdir not in self.incdirs:
                self.incdirs.append(os.path.abspath(incdir))
                util.debug(f"Added include dir '{os.path.abspath(incdir)}'")
            return
        self.error(f"Didn't understand +plusarg: '{plusarg}'")

    def append_shell_commands(self, cmds : list):
        # Each entry in cmds (list) should be a dict with keys ['target_node', 'target_path', 'exec_list']
        for entry in cmds:
            if entry is None or type(entry) is not dict:
                continue
            if entry in self.dep_shell_commands:
                # we've already run this exact command (target node, target path, exec list), don't run it
                # again
                continue

            assert 'exec_list' in entry, f'{entry=}'
            util.debug(f'adding - dep_shell_command: {entry=}')
            self.dep_shell_commands.append(entry)

    def append_work_dir_add_srcs(self, add_srcs : list):
        # Each entry in add_srcs (list) should be a dict with keys ['target_node', 'target_path', 'file_list']
        for entry in add_srcs:
            if entry is None or type(entry) is not dict:
                continue

            work_dir_files = entry['file_list']
            for filename in work_dir_files:
                # Unfortunately, self.args['work-dir'] doesn't exist yet and hasn't been set, so we'll add these
                # files as '@EDA-WORK_DIR@' + filename, and have to replace the EDA-WORK_DIR@ string later in our flow.
                filename_use = self._work_dir_add_srcs_path_string + filename
                dep_key_tuple = (
                    entry['target_path'],
                    entry['target_node'],
                    filename_use
                )
                if filename_use not in self.files:
                    util.debug(f'work_dir_add_srcs@ {dep_key_tuple=} added file {filename_use=}')
                    self.add_file(filename=filename_use, use_abspath=False)
                    # avoid duplicate calls, and keep a paper trail of which DEPS added
                    # files from the self.args['work-dir'] using this method.
                    self.dep_work_dir_add_srcs.add(dep_key_tuple) # add to set()
                elif dep_key_tuple not in self.dep_work_dir_add_srcs:
                    # we've already added the file so this dep was skipped for this one file.
                    util.warning(f'work_dir_add_srcs@ {dep_key_tuple=} but {filename_use=}' \
                                 + 'is already in self.files (duplicate dependency on generated file?)')


    def resolve_target(self, target, no_recursion=False):
        util.debug("Entered resolve_target(%s)" % (target))
        # self.target is a name we grab for the job (i.e. for naming work dir etc).  we don't want the path prefix.
        # TODO: too messy -- there's also a self.target, args['job-name'], args['work-dir'], args['design'], args['top'], args['sub-work-dir'] ...
        self.target = target
        m = re.match(r'.*\/([\w\_]+)$', self.target)
        if m: self.target = m.group(1)

        if target in self.targets_dict:
            # If we're encountered this target before, stop. We're not traversing again.
            return True

        self.targets_dict[target] = None
        if os.path.exists(target):
            # If the target is a file (we're at the root here processing CLI arg tokens)
            # and that file exists and has an extension, then there's no reason to go looking
            # in DEPS files, add the file and return True.
            file_base, file_ext = os.path.splitext(target)
            if file_ext != '':
                self.add_file(target)
                return True

        return self.resolve_target_core(target, no_recursion)

    def resolve_target_core(self, target, no_recursion):
        util.debug("Entered resolve_target_core(%s)" % (target))
        found_target = False
        util.debug("Starting to resolve target '%s'" % (target))
        target_path, target_node = os.path.split(target)

        found_deps_file = False
        deps_file = os.path.join(target_path, 'DEPS.yml')
        data = None
        if self.config['deps_yaml_supported'] and not found_deps_file:

            # Have we already unmarshalled this file before?
            data = self.cached_deps_files.get(target_path, None)

            # If we haven't, try reading it
            if data is None:
                data = util.yaml_safe_load(deps_file)
                self.cached_deps_files[target_path] = data

        # Continue if we have data, otherwise look for files other than DEPS.yml
        if data is not None:
            found_deps_file = True
            if target_node not in data:
                util.error(f'{target_node=} not in {deps_file=} (or is not a file that exists),' \
                           + f' {target=} {data.keys()=}')
            else:
                util.debug(f'Found {target_node=} in {deps_file=}')
                found_target = True

        if found_deps_file and found_target:

            # Start with the defaults
            entry = data.get('DEFAULTS', dict()).copy()

            # Lookup the entry from the DEPS dict:
            entry_raw = data[target_node]

            # Since we support a few schema flavors for a target (our 'target_node' key in a DEPS.yml file),
            # santize the entry so it's a dict() with a 'deps' key:
            entry_sanitized = deps_helpers.deps_list_target_sanitize(
                entry_raw, target_node=target_node, deps_file=deps_file
            )

            # Finally update entry (defaults) with what we looked up:
            entry.update(entry_sanitized)

            # For convenience, use an external class for this DEPS.yml table/dict
            # This could be re-used for any markup DEPS.json, DEPS.toml, DEPS.py, etc.
            deps_processor = deps_helpers.DepsProcessor(
                command_design_ref = self,
                deps_entry = entry,
                target = target,
                target_path = target_path,
                target_node = target_node,
                deps_file = deps_file
            )

            # Process the target, and get new (unprocessed) deps entries list.
            # This updates self (for defines, incdirs, top, args, etc)
            # This will skip remaining deps in self.targets_dict
            deps_targets_to_resolve = deps_processor.process_deps_entry()
            util.debug(f'   ... for {target_node=} {deps_file=}, {deps_targets_to_resolve=}')

            # Recurse on the returned deps (ordered list), if they haven't already been traversed.
            for x in deps_targets_to_resolve:
                if x and type(x) is tuple:
                    # if deps_processor.process_deps_entry() gave us a tuple, it's an
                    # unprocessed 'command' that we kept in order until now. Append it.
                    assert len(x) == 2, f'command tuple {x=} must be len 2, {target_node=} {deps_file=}'
                    shell_commands_list, work_dir_add_srcs_list = x
                    self.append_shell_commands( cmds=shell_commands_list )
                    self.append_work_dir_add_srcs( add_srcs=work_dir_add_srcs_list )

                elif x and x not in self.targets_dict:
                    self.targets_dict[x] = None # add it before processing.
                    if os.path.exists(x):
                        self.add_file(x)
                    else:
                        util.debug(f'   ... Calling resolve_target_core({x=})')
                        found_target |= self.resolve_target_core(x, no_recursion)


        # Done with DEPS.yml if it existed.


        # ------------------------------------------------------------
        # TODO(drew): to be removed with DEPS --> DEPS.yml
        deps_file = os.path.join(target_path, "DEPS")
        # yes, we reparse the DEPS file for every target we search for.  sometimes hitting a target causes
        # side effects (like defining things) which then could affect DEPS.  TBD is the specific case where one
        # target is pulled in multiple times and the defines/etc are different; it will just get read in first
        # time, but the same can be said for file lists in general (we don't support re-reading files with
        # different defines set, although this can always be done using `include in the sources)
        # In general it's common to run into this "race" condition, i.e.  lib_synchronizer with two conditional
        # implementations, we read it in before "GATE_SIM" is set by the top level target, because we pulled
        # in a lib element causing us to read lib/DEPS (we had more than one thing on command line for example).
        # so we don't worry about spending a few extra cycles and just doing it the "simple, inefficient" way.
        if not found_deps_file and os.path.isfile(deps_file):
            f = open( deps_file, 'r' )
            util.debug("Opened '%s'" % (deps_file))
            found_deps_file = True
            in_dep = False
            line_number = 0
            for line in f:
                line_number += 1
                # clear out comments
                m = re.match(r'^([^\#]*)\#.*$', line)
                if m:
                    line = m.group(1)
                # look for the declaration of a target, which looks like "<target> : [dep .. dep] \n [dep .. dep] \n"
                m = re.match(r'^\s*(\w+)\s*\:(.*)$', line)
                if m:
                    if in_dep:
                        util.debug("Done with %s at %s:%d" % (target, deps_file, line_number-1))
                        break # stop looking through this DEP file, we cannot appear more than once
                    elif m.group(1) == target_node:
                        in_dep = True # we have found our DEP!
                        found_target = True
                        line = m.group(2) # we trim down line and let lower code parse the rest
                        util.debug("Found %s at %s:%d" % (target, deps_file, line_number))
                        if no_recursion: return True
                    else:
                        continue # it's the start of a DEP, but not ours
                else:
                    if not in_dep:
                        continue # move on to next line if we aren't currently in the DEP

                # at this point we are processing a line from our DEP, but we may do some conversions on it
                for dep_sub in self.config['dep_sub']:
                    m = re.search(dep_sub[0], line)
                    if m:
                        line = re.sub(dep_sub[0], dep_sub[1], line)
                        # do we have any variables to substitute?
                        line_split = line.split()
                        for iter,word in enumerate(line_split):
                            # resolve ${thing} first
                            m = re.search(r'\$\{(\w+)\}', word)
                            if m and m.group(1) in self.config['vars']:
                                word = re.sub(r'\$\{%s\}' % (m.group(1)), self.config['vars'][m.group(1)], word)
                                line_split[iter] = word
                            # resolve $thing2
                            m = re.search(r'\$(\w+)', word)
                            if m and m.group(1) in self.config['vars']:
                                word = re.sub(r'\$%s' % (m.group(1)), self.config['vars'][m.group(1)], word)
                                line_split[iter] = word
                        line = ' '.join(line_split)

                # We can try for replacing any formatted strings, using self.args, and os.environ, in the
                # line:
                line = deps_helpers.line_with_var_subst(line=line, replace_vars_dict=self.args,
                                                        replace_vars_os_env=True,
                                                        target_node=target_node, target_path=target_path)

                # check for conditional inclusions based on defines
                m = re.match(r'^\s*(\w+)\s+\?([^\:]*)\s*(\:)?\s*(.*)*$', line)
                if m:
                    v = m.group(1)
                    l1 = m.group(2)
                    l2 = m.group(3)
                    line = l1 if v in self.defines else l2
                    if line == None: line = ""

                # check for setting an EDA argument
                m = re.match(r'^\s*\-\-([\w\-]+)\s*', line)
                if m:
                    Command.process_tokens(self, line.split())
                    continue


                # shell@
                # work_dir_add_srcs@
                # peakrdl@ (args)
                shell_commands_list = list() # list of dict()s
                work_dir_add_srcs_list = list() # list of dict()s

                # shell@
                # Is this a bare shell command in the format:
                #    shell@echo "hello world" > hello.txt
                #    shell@generate_something.sh
                #    shell@generate_this.py --input=some_data.json
                #    shell@vivado -mode tcl -script ./some.tcl -tclargs foo_ip 1.2 foo_part foo_our_name {property value}
                # These will be executed after performing all DEPS searching.
                ret_dict = deps_helpers.parse_deps_shell_str(
                    line=line, target_path=target_path, target_node=target_node,
                    enable=self.config['dep_command_enables']['shell']
                )
                if ret_dict:
                    line = ""
                    shell_commands_list.append(ret_dict) # process this later.

                # work_dir_add_srcs@
                # Did a previous shell@ command generate file(s) for .v, .sv, .vhdl that have not been compiled, and we'd
                # like to add them to our sources?
                # These will be executed after performing all DEPS searching, and after all shell commands executed.
                #     work_dir_add_srcs@ some_file.sv some_dir/some_other_file.v
                # Note that these are all rooted in the self.args['work-dir']
                ret_dict = deps_helpers.parse_deps_work_dir_add_srcs(
                    line=line, target_path=target_path, target_node=target_node,
                    enable=self.config['dep_command_enables']['work_dir_add_srcs']
                )
                if ret_dict:
                    line = ""
                    work_dir_add_srcs_list.append(ret_dict)

                # peakrdl@ (args)
                # peakrdl@ --cpuif axi4-lite-flat --top oc_eth_10g_1port_csrs ./oc_eth_10g_csrs.rdl
                #  -- need to snoop if --top (name) exists, that will be the (name).sv file
                #  -- need to create shell commands to add the Verilator waivers
                #  -- need to add work_dir_add_srcs@ for the two .sv files.
                ret_dict = deps_helpers.parse_deps_peakrdl(
                    line=line, target_path=target_path, target_node=target_node,
                    enable=self.config['dep_command_enables']['peakrdl']
                )
                if ret_dict:
                    line = ""
                    # add all the shell commands:
                    shell_commands_list += ret_dict['shell_commands_list'] # several entries.
                    # all the work_dir_add_srcs:
                    work_dir_add_srcs_list += [ ret_dict['work_dir_add_srcs'] ] # single entry append

                # Process all shell_commands_list:
                # This will track each shell command with its target_node and target_path
                self.append_shell_commands(cmds = shell_commands_list)

                # Process all work_dir_add_srcs_list:
                # This will track each added filename with its target_node and target_path
                self.append_work_dir_add_srcs(add_srcs = work_dir_add_srcs_list)

                # We are done with these, delete them:
                del shell_commands_list
                del work_dir_add_srcs_list


                for dep in line.split():

                    # see if this is a generated source file, which has a similar syntax to
                    # the bare shell command. (src)@(list)
                    m = re.match(r'^\s*([\w\.]+)\@(\S+)\s*$', dep)
                    if m:
                        source_file = m.group(1)
                        exec_csv = m.group(2)
                        exec_list = exec_csv.split(",")
                        util.info("Generating %s via '%s'" % (source_file, " ".join(exec_list)))
                        self.exec(target_path, exec_list)
                        if os.path.exists(os.path.join(target_path, source_file)):
                            util.debug("Done generating %s via '%s'" % (os.path.join(target_path, source_file), " ".join(exec_list)))
                            self.add_file(os.path.join(target_path, source_file))
                            continue
                        else:
                            self.error("Failed to generate %s via '%s'" % (source_file, " ".join(exec_list)))
                    # see if there's any conditionally included code

                    # check for compile-time Verilog style plusarg, which are supported under targets
                    # These are not run-time Verilog style plusargs comsumable from within the .sv:
                    m = re.match(r'^\+(define|incdir)\+\S+$', dep)
                    if m:
                        util.debug("Got plusarg %s for target %s at %s:%d" % (dep, target, deps_file, line_number))
                        self.process_plusarg(dep, target_path)
                        continue

                    # this dep hasn't been dealt with above, which are rare things, do it the normal way
                    dep_path = os.path.join(target_path, dep)
                    util.debug("Got dep %s for target %s at %s:%d" % (dep_path, target, deps_file, line_number))
                    if dep_path in self.targets_dict:
                        util.debug(" - already processed, skipping")
                        continue
                    self.targets_dict[dep_path] = None
                    if os.path.exists(dep_path):
                        util.debug(" - raw file, adding to file lists")
                        self.add_file(dep_path)
                    else:
                        util.debug(" - a target needing to be resolved, recursing...")
                        found_target |= self.resolve_target_core(dep_path, no_recursion)

        # TODO(drew): (end) to be removed with DEPS --> DEPS.yml
        # --------------------------------------------------------

        if not found_target:
            util.debug("Haven't been able to resolve %s via DEPS" % (target))
            for e in [ '.sv', '.v', '.vhd' ]:
                try_file = target + e
                util.debug("Looking for %s" % (try_file))
                if os.path.exists(try_file):
                    self.add_file(try_file)
                    found_target = True
                    break # move on to the next target
            if not found_target: # if STILL not found_this_target...
                self.error("Unable to resolve target '%s'" % (target))

        # if we've found any target since being called, it means we found the one we were called for
        return found_target

    def add_file(self, filename, use_abspath=True):
        file_base, file_ext = os.path.splitext(filename)
        if use_abspath:
            file_abspath = os.path.abspath(filename)
        else:
            file_abspath = filename


        if file_abspath in self.files:
            util.debug("Not adding file %s, already have it" % (file_abspath))
            return

        if file_ext == '.v' and not self.args['all-sv']:
            self.files[file_abspath] = True
            self.files_v.append(file_abspath)
            util.debug("Added Verilog file %s as %s" % (filename, file_abspath))
        elif file_ext == '.sv' or (file_ext == '.v' and self.args['all-sv']):
            self.files[file_abspath] = True
            self.files_sv.append(file_abspath)
            util.debug("Added SystemVerilog file %s as %s" % (filename, file_abspath))
        elif file_ext == '.vhd':
            self.files[file_abspath] = True
            self.files_vhd.append(file_abspath)
            util.debug("Added VHDL file %s as %s" % (filename, file_abspath))
        return file_abspath

    def process_tokens(self, tokens, process_all=True, pwd=None):
        util.debug(f'CommandDesign - process_tokens start - {tokens=}')

        # see if it's a flag/option like --debug, --seed <n>, etc
        # This returns all unparsed args, and doesn't error out due to process_all=False
        unparsed = Command.process_tokens(self, tokens, process_all=False)
        util.debug(f'CommandDesign - after Command.process_tokens(..) {unparsed=}')

        # deal with +define+ or +incdir+, consume it and remove from unparsed
        # walk the list, remove all items after we're done.
        remove_list = list()
        for token in unparsed:
            if any(token.startswith(x) for x in ['+define+', '+incdir+']):
                self.process_plusarg(token, pwd=pwd)
                remove_list.append(token)
        for x in remove_list:
            unparsed.remove(x)

        # by this point hopefully this is a target ... is it a simple filename?
        remove_list = list()
        for token in unparsed:
            if os.path.exists(token):
                file_abspath = self.add_file(token)
                file_base, file_ext = os.path.splitext(file_abspath)
                if file_ext == '':
                    # This probably isn't a file we want to use
                    util.warning(f'looking for deps {token=}, found {file_abspath=}' \
                                 + ' but has no file extension, we will not add this file')
                    # do not consume it, it's probably a named target in DEPS.yml
                    continue
                if self.args['top'] == "":
                    # if we haven't yet been given a top, or inferred one, we take the first one we get
                    # from a target name
                    self.args['top'] = self.get_top_name(file_abspath)
                    self.args['top-path'] = file_abspath
                    util.info(f"Inferred --top {self.args['top']} {file_abspath}")

                remove_list.append(token)
                continue # done with token.

            # we appear to be dealing with a target name which needs to be resolved (usually recursively)
            if token == os.sep:
                target_name = token # if it's absolute path, don't prepend anything
            else:
                target_name = os.path.join(".", token) # prepend ./so that we always have a <path>/<file>

            util.debug(f'Calling self.resolve_target on {target_name=}')
            if self.resolve_target(target_name):
                if self.args['top'] == '':
                    # if we haven't yet been given a top, or inferred one, we take the first one we get
                    # from a target name
                    self.args['top'] = self.get_top_name(target_name)
                    self.args['top-path'] = target_name
                    util.info(f"Inferred --top {self.args['top']} {target_name}")

                remove_list.append(token)
                continue # done with token

        for x in remove_list:
            unparsed.remove(x)

        # we were unable to figure out what this command line token is for...
        if process_all and len(unparsed) > 0:
            self.error(f"Didn't understand command remaining tokens {unparsed=} in CommandDesign")

        self.defines['OC_SEED'] = f"{self.args['seed']}"
        self.defines['OC_ROOT'] = f"\"{self.oc_root}\""
        return self.status


class CommandSim(CommandDesign):

    def __init__(self, config:dict):
        CommandDesign.__init__(self, config=config, command_name="sim")
        self.args["pre-sim-tcl"] = list()
        self.args['sim-plusargs'] = list() # lists are handled by 'set_arg(k,v)' so they append.
        self.args['sim-library'] = list()
        self.args['compile-args'] = list()
        self.args['elab-args'] = list()
        self.args['sim-args'] = list()
        self.args['coverage'] = False
        self.args['waves'] = False
        self.args['waves-start'] = 0
        self.args['pass-pattern'] = ""
        self.args['optimize'] = False
        self.args['verilate-args'] = list()

        # verilate-args: list of args you can only pass to Verilator, not used by other simulators, so
        # these can go in DEPS files for custom things like -CFLAGS -O0, etc.
        self.args['verilate-args'] = list()

        self.log_bad_strings = ['ERROR: ', 'FATAL: ']
        self.log_must_strings = list()

    def process_tokens(self, tokens, process_all=True):
        self.defines['SIMULATION'] = None
        ret = CommandDesign.process_tokens(self, tokens, process_all)
        # add defines for this job type
        if self.args['lint'] or self.args['stop-after-elaborate']:
            self.args['lint'] = True
            self.args['stop-after-elaborate'] = True
        if (self.args['top'] != ""):
            # create our work dir
            self.create_work_dir()
            self.run_dep_commands()
            self.do_it()
            ret = self.status
        return ret

    # Methods that derived classes may override:
    def run_commands_check_logs(self, commands : list, check_logs=True, log_filename='sim.log', bad_strings=[], must_strings=[]):
        for c in commands:
            assert type(c) is list, f'{self.target=} command {c=} is not a list, not going to run it'
            self.exec(self.args['work-dir'], c)
            if check_logs:
                self.check_logs_for_errors(filename=log_filename, bad_strings=bad_strings, must_strings=must_strings)


    def do_it(self):
        self.prepare_compile()
        self.compile()
        self.elaborate()
        self.simulate()
        return self.status

    def set_tool_defines(self):
        pass

    # Methods that derived classes may override:
    def prepare_compile(self):
        self.set_tool_defines()

    def check_logs_for_errors(self, filename : str, bad_strings=[], must_strings=[]):
        bad_strings += self.log_bad_strings
        must_strings += self.log_must_strings

        if self.args['pass-pattern'] != "":
            must_strings.append(self.args['pass-pattern'])

        if len(bad_strings) > 0 or len(must_strings) > 0:
            hit_bad_string = False
            hit_must_string_dict = dict.fromkeys(must_strings)
            fname = os.path.join(self.args['work-dir'], filename)
            with open(fname, "r") as f:
                for iter,line in enumerate(f):
                    if any(must_str in line for must_str in must_strings):
                        for k in hit_must_string_dict.keys():
                            if k in line:
                                hit_must_string_dict[k] = True
                    if any(bad_str in line for bad_str in bad_strings):
                        hit_bad_string = True
                        self.error(f"log {fname}:{iter} contains one of {bad_strings=}")

            if hit_bad_string:
                self.status += 1
            if any(x is None for x in hit_must_string_dict.values()):
                self.error(f"Didn't get all passing patternsin log {fname}: {must_strings=} {hit_must_string_dict=}")
                self.status += 1

    # Methods that derived classes must override:

    def compile(self):
        raise NotImplementedError

    def elaborate(self):
        raise NotImplementedError

    def simulate(self):
        raise NotImplementedError

    def get_compile_command_lists(self) -> list():
        ''' Returns a list of lists (list of command lists).'''
        raise NotImplementedError

    def get_elaborate_command_lists(self) -> list():
        ''' Returns a list of lists (list of command lists).'''
        raise NotImplementedError

    def get_simulate_command_lists(self) -> list():
        ''' Returns a list of lists (list of command lists).'''
        raise NotImplementedError

    def get_post_simulate_command_lists(self) -> list():
        ''' Returns a list of lists (list of command lists).'''
        raise NotImplementedError



class CommandElab(CommandSim):
    def __init__(self, config:dict):
        CommandSim.__init__(self, config=config)
        # add args specific to this simulator
        self.args['stop-after-elaborate'] = True
        self.args['lint'] = True
        self.args['verilate-args'] = list()

class CommandSynth(CommandDesign):
    def __init__(self, config:dict):
        CommandDesign.__init__(self, config, "synth")
        self.args['flatten-all'] = False
        self.args['flatten-none'] = False
        self.args['clock-ns'] = 5 # 200Mhz
        self.args['idelay-ns'] = 2
        self.args['odelay-ns'] = 2

    def process_tokens(self, tokens, process_all=True):
        self.defines['SYNTHESIS'] = None
        CommandDesign.process_tokens(self, tokens, process_all)
        # add defines for this job type
        if (self.args['top'] != ""):
            # create our work dir
            self.create_work_dir()
            self.run_dep_commands()
            self.do_it()

class CommandProj(CommandDesign):
    def __init__(self, config:dict):
        CommandDesign.__init__(self, config, "proj")

    def process_tokens(self, tokens, process_all=True):
        CommandDesign.process_tokens(self, tokens, process_all)
        # add defines for this job type
        if (self.args['top'] != ""):
            # create our work dir
            self.create_work_dir()
            self.run_dep_commands()
            self.do_it()

class CommandBuild(CommandDesign):
    def __init__(self, config:dict):
        CommandDesign.__init__(self, config, "build")
        self.args['build-script'] = "build.tcl"

    def process_tokens(self, tokens, process_all=True):
        CommandDesign.process_tokens(self, tokens, process_all)
        # add defines for this job type
        if (self.args['top'] != ""):
            # create our work dir
            self.create_work_dir()
            self.run_dep_commands()
            self.do_it()

_threads_start = 0
_threads_done = 0

class CommandParallelWorker(threading.Thread):
    def __init__(self, n, work_queue, done_queue):
        threading.Thread.__init__(self)
        self.n = n
        self.work_queue = work_queue
        self.done_queue = done_queue
        self.stop_request = False
        self.job_name = ""
        self.proc = None
        self.pid = None
        self.last_timer_debug = 0
        util.debug(f"WORKER_{n}: START")

    def run(self):
        global _threads_start
        global _threads_done
        while True:
            # Get the work from the queue and expand the tuple
            i, command_list, job_name, work_dir = self.work_queue.get()
            self.job_name = job_name
            try:
                util.debug(f"WORKER_{self.n}: Running job {i}: {job_name}")
                PIPE=subprocess.PIPE
                STDOUT=subprocess.STDOUT
                util.debug(f"WORKER_{self.n}: Calling Popen")
                proc = subprocess.Popen(command_list, stdout=PIPE, stderr=STDOUT)
                self.proc = proc
                util.debug(f"WORKER_{self.n}: Opened process, PID={proc.pid}")
                self.pid = proc.pid
                _threads_start += 1
                while proc.returncode == None:
                    try:
                        if (time.time() - self.last_timer_debug) > 10:
                            util.debug(f"WORKER_{self.n}: Calling proc.communicate")
                        stdout, stderr = proc.communicate(timeout=0.5)
                        util.debug(f"WORKER_{self.n}: got: \n*** stdout:\n{stdout}\n*** stderr:{stderr}")
                    except subprocess.TimeoutExpired:
                        if (time.time() - self.last_timer_debug) > 10:
                            util.debug(f"WORKER_{self.n}: Timer expired, stop_request={self.stop_request}")
                            self.last_timer_debug = time.time()
                        pass
                    if self.stop_request:
                        util.debug(f"WORKER_{self.n}: got stop request, issuing SIGINT")
                        proc.send_signal(signal.SIGINT)
                        util.debug(f"WORKER_{self.n}: got stop request, calling proc.wait")
                        proc.wait()
                    if False and self.stop_request:
                        util.debug(f"WORKER_{self.n}: got stop request, issuing proc.terminate")
                        proc.terminate()
                        util.debug(f"WORKER_{self.n}: proc poll returns is now {proc.poll()}")
                        try:
                            util.debug(f"WORKER_{self.n}: Calling proc.communicate")
                            stdout, stderr = proc.communicate(timeout=0.2) # for completeness, in case we ever pipe/search stdout/stderr
                            util.debug(f"WORKER_{self.n}: got: \n*** stdout:\n{stdout}\n*** stderr:{stderr}")
                        except subprocess.TimeoutExpired:
                            util.debug(f"WORKER_{self.n}: timeout waiting for comminicate after terminate")
                        except:
                            pass
                        util.debug(f"WORKER_{self.n}: proc poll returns is now {proc.poll()}")

                util.debug(f"WORKER_{self.n}: -- out of while loop")
                self.pid = None
                self.proc = None
                self.job_name = "<idle>"
                util.debug(f"WORKER_{self.n}: proc poll returns is now {proc.poll()}")
                try:
                    util.debug(f"WORKER_{self.n}: Calling proc.communicate one last time")
                    stdout, stderr = proc.communicate(timeout=0.1) # for completeness, in case we ever pipe/search stdout/stderr
                    util.debug(f"WORKER_{self.n}: got: \n*** stdout:\n{stdout}\n*** stderr:{stderr}")
                except subprocess.TimeoutExpired:
                    util.debug(f"WORKER_{self.n}: timeout waiting for communicate after loop?")
                except:
                    pass
                return_code = proc.poll()
                util.debug(f"WORKER_{self.n}: Finished job {i}: {job_name} with return code {return_code}")
                self.done_queue.put((i, job_name, return_code))
            finally:
                util.debug(f"WORKER_{self.n}: -- in finally block")
                self.work_queue.task_done()
                _threads_done += 1


class CommandParallel(Command):
    def __init__(self, config, command_name):
        Command.__init__(self, config, command_name)
        self.jobs = list()
        self.jobs_status = list()
        self.args['parallel'] = 1
        self.worker_threads = list()

    def __del__(self):
        util.debug(f"In Command.__del__, threads done/started: {_threads_done}/{_threads_start}")
        if _threads_start == _threads_done:
            return
        util.warning(f"Need to shut down {_threads_start-_threads_done} worker threads...")
        for w in self.worker_threads:
            if w.proc:
                util.warning(f"Requesting stop of PID {w.pid}: {w.job_name}")
                w.stop_request = True
        for i in range(10):
            util.debug(f"Threads done/started: {_threads_done}/{_threads_start}")
            if _threads_start == _threads_done:
                util.info(f"All threads done")
                return
            time.sleep(1)
        subprocess.Popen(['stty', 'sane']).wait()
        util.debug(f"Scanning workers again")
        for w in self.worker_threads:
            if w.proc:
                util.info(f"need to SIGINT WORKER_{w.n}, may need manual cleanup, check 'ps'")
                if w.pid:
                    os.kill(w.pid, signal.SIGINT)
        for i in range(5):
            util.debug(f"Threads done/started: {_threads_done}/{_threads_start}")
            if _threads_start == _threads_done:
                util.info(f"All threads done")
                return
            time.sleep(1)
        subprocess.Popen(['stty', 'sane']).wait()
        util.debug(f"Scanning workers again")
        for w in self.worker_threads:
            if w.proc:
                util.info(f"need to TERM WORKER_{w.n}, probably needs manual cleanup, check 'ps'")
                if w.pid:
                    os.kill(w.pid, signal.SIGTERM)
        for i in range(5):
            util.debug(f"Threads done/started: {_threads_done}/{_threads_start}")
            if _threads_start == _threads_done:
                util.info(f"All threads done")
                return
            time.sleep(1)
        subprocess.Popen(['stty', 'sane']).wait()
        util.debug(f"Scanning workers again")
        for w in self.worker_threads:
            if w.proc:
                util.info(f"need to KILL WORKER_{w.n}, probably needs manual cleanup, check 'ps'")
                if w.pid:
                    os.kill(w.pid, signal.SIGKILL)
        util.stop_log()
        subprocess.Popen(['stty', 'sane']).wait()

    def run_jobs(self, command):
        # this is where we actually run the jobs.  it's a messy piece of code and prob could use refactoring
        # but the goal was to share as much as possible (job start, end, pass/fail judgement, etc) while
        # supporting various mode combinations (parallel mode, verbose mode, fancy mode, etc) and keeping the
        # UI output functional and awesome sauce

        # walk targets to find the longest name, for display reasons
        longest_job_name = 0
        total_jobs = len(self.jobs)
        self.jobs_status = [None] * total_jobs
        for i in range(total_jobs):
            l = len(self.jobs[i]['name'])
            if l>longest_job_name: longest_job_name = l

        run_parallel = self.args['parallel'] > 1

        # figure out the width to print various numbers
        jobs_digits = len(f"{total_jobs}")
        jobs_fmt = "%%%dd" % jobs_digits # ugh, for printing out a number with N digits

        # run the jobs!
        running_jobs = {}
        passed_jobs = []
        failed_jobs = []
        workers = []
        jobs_complete = 0
        jobs_launched = 0
        num_parallel = min(len(self.jobs), self.args['parallel'])
        # 16 should really be the size of window or ?
        (columns,lines) = shutil.get_terminal_size()
        # we will enter fancy mode if we are parallel and we can leave 6 lines of regular scrolling output
        fancy_mode = util.args['fancy'] and (num_parallel > 1) and (num_parallel <= (lines-6))
        multi_cwd = util.getcwd() + os.sep

        if run_parallel:
            # we are doing this multi-threaded
            util.info(f"Parallel: Running multi-threaded, starting {num_parallel} workers")
            work_queue = queue.Queue()
            done_queue = queue.Queue()
            for x in range(num_parallel):
                worker = CommandParallelWorker(x, work_queue, done_queue)
                # Setting daemon to True will let the main thread exit even though the workers are blocking
                worker.daemon = True
                worker.start()
                self.worker_threads.append(worker)
                workers.append(x)
            if fancy_mode:
                # in fancy mode, we will take the bottom num_parallel lines to show state of workers
                util.fancy_start(fancy_lines=num_parallel)
                for x in range(num_parallel):
                    util.fancy_print(f"Starting worker {x}", x)

        while len(self.jobs) or len(running_jobs.items()):
            job_done = False
            job_done_quiet = False
            anything_done = False

            def sprint_job_line(job_number=0, job_name="", final=False, hide_stats=False):
                return (f"INFO: [EDA] " +
                        util.string_or_space(f"[job {jobs_fmt%job_number}/{jobs_fmt%total_jobs} ", final) +
                        util.string_or_space(f"| pass ", hide_stats or final) +
                        util.string_or_space(f"{jobs_fmt%len(passed_jobs)}/{jobs_fmt%jobs_complete} ", hide_stats) +
                        util.string_or_space(f"@ {(100*(jobs_complete))/total_jobs:5.1f}%", hide_stats or final) +
                        util.string_or_space(f"] ", final) +
                        f"{command} {(job_name+' ').ljust(longest_job_name+3,'.')}")

            # for any kind of run (parallel or not, fancy or not, verbose or not) ... can we launch a job?
            if len(self.jobs) and (len(running_jobs.items()) < num_parallel):
                # we are launching a job
                jobs_launched += 1
                anything_done = True
                job = self.jobs.pop(0)
                if job['name'].startswith(multi_cwd): job['name'] = job['name'][len(multi_cwd):]
                # in all but fancy mode, we will print this text at the launch of a job.  It may get a newline below
                job_text = sprint_job_line(jobs_launched, job['name'], hide_stats=run_parallel)
                command_list = job['command_list']
                cwd = util.getcwd()

                if run_parallel:
                    # multithreaded job launch: add to queue
                    worker = workers.pop(0) # we don't actually know which thread will pick up, but GUI will be consistent
                    running_jobs[str(jobs_launched)] = { 'name' : job['name'],
                                                         'number' : jobs_launched,
                                                         'worker' : worker,
                                                         'start_time' : time.time(),
                                                         'update_time' : time.time()}
                    work_queue.put((jobs_launched, command_list, job['name'], cwd))
                    suffix = "<START>"
                    if fancy_mode:
                        util.fancy_print(job_text+suffix, worker)
                    else:
                        # if we aren't in fancy mode, we will print a START line, periodic RUNNING lines, and PASS/FAIL line per-job
                        if len(failed_jobs): util.print_orange(job_text+util.string_yellow+suffix)
                        else:                util.print_yellow(job_text+util.string_yellow+suffix)
                else:
                    # single-threaded job launch, we are going to print out job info as we start each job... no newline
                    # since non-verbose silences the job and prints only <PASS>/<FAIL> after the trailing "..." we leave here
                    if len(failed_jobs): util.print_orange(job_text, end="")
                    else:                util.print_yellow(job_text, end="")
                    job_done_number = jobs_launched
                    job_done_name = job['name']
                    job_start_time = time.time()
                    if util.args['verbose']:
                        # previous status line gets a \n, then job is run passing stdout/err, then print 'job_text' again with pass/fail
                        util.print_green("")
                        # run job, sending output to the console
                        _, _, job_done_return_code = self.exec(cwd, command_list, background=False, stop_on_error=False, quiet=False)
                        # reprint the job text previously printed before running job(and given "\n" after the trailing "...")
                    else:
                        # run job, swallowing output (hope you have a logfile)
                        _, _, job_done_return_code = self.exec(cwd, command_list, background=True, stop_on_error=False, quiet=True)
                        job_done_quiet = True # in this case, we have the job start text (trailing "...", no newline) printed
                    job_done = True
                    job_done_run_time = time.time() - job_start_time
                    # Since we consumed the job, use the job['index'] to track the per-job status:

            if run_parallel:
                # parallel run, check for completed job
                if done_queue.qsize():
                    # we're collecting a finished job from a worker thread.  note we will only reap one job per iter of the big
                    # loop, so as to share job completion code at the bottom
                    anything_done = True
                    job_done = True
                    job_done_number, job_done_name, job_done_return_code = done_queue.get()
                    t = running_jobs[str(job_done_number)]
                    # in fancy mode, we need to clear the worker line related to this job.
                    if fancy_mode:
                        util.fancy_print(f"INFO: [EDA] Parallel: Worker Idle ...", t['worker'])
                    job_done_run_time = time.time() - t['start_time']
                    util.debug(f"removing job #{job_done_number} from running jobs")
                    del running_jobs[str(job_done_number)]
                    workers.append(t['worker'])

            if run_parallel:
                # parallel run, update the UI on job status
                for _,t in running_jobs.items():
                    if (fancy_mode or (time.time() - t['update_time']) > 30):
                        t['update_time'] = time.time()
                        job_text = sprint_job_line(t['number'], t['name'], hide_stats=True)
                        suffix = f"<RUNNING: {util.sprint_time(time.time() - t['start_time'])}>"
                        if fancy_mode:
                            util.fancy_print(f"{job_text}{suffix}", t['worker'])
                        else:
                            if len(failed_jobs): util.print_orange(job_text+util.string_yellow+suffix)
                            else:                util.print_yellow(job_text+util.string_yellow+suffix)

            # shared job completion code
            # single or multi-threaded, we can arrive here to harvest <= 1 jobs, and need {job, return_code} valid, and
            # we expect the start of a status line to have been printed, ready for pass/fail
            if job_done:
                jobs_complete += 1
                if job_done_return_code is None or job_done_return_code:
                    # embed the color code, to change color of pass/fail during the util.print_orange/yellow below
                    suffix = f"{util.string_red}<FAIL: {util.sprint_time(job_done_run_time)}>"
                    failed_jobs.append(job_done_name)
                else:
                    suffix = f"{util.string_green}<PASS: {util.sprint_time(job_done_run_time)}>"
                    passed_jobs.append(job_done_name)
                # we want to print in one shot, because in fancy modes that's all that we're allowed
                job_done_text = "" if job_done_quiet else sprint_job_line(job_done_number, job_done_name)
                if len(failed_jobs): util.print_orange(f"{job_done_text}{suffix}")
                else:                util.print_yellow(f"{job_done_text}{suffix}")
                self.jobs_status[job_done_number-1] = job_done_return_code

            if not anything_done:
                time.sleep(0.25) # if nothing happens for an iteration, chill out a bit

        if total_jobs:
            emoji = "< :) >" if (len(passed_jobs) == total_jobs) else "< :( >"
            util.info(sprint_job_line(final=True,job_name="jobs passed")+emoji, start="")
        else:
            util.info(f"Parallel: <No jobs found>")
        # Make sure all jobs have a set status:
        for iter,rc in enumerate(self.jobs_status):
            if rc is None or type(rc) != int:
                self.error(f'job {iter=} {rc=} did not return a proper return code')
                jobs_status[iter] = 1
        self.status = 0 if len(self.jobs_status) == 0 else max(self.jobs_status)
        util.fancy_stop()


class CommandMulti(CommandParallel):
    def __init__(self, config:dict):
        CommandParallel.__init__(self, config, "multi")
        self.args.update({
            'fail-if-no-targets': False
        })

    def resolve_target(self, base_path, target, command, level=0):
        util.debug(f"ENTER RESOLVE_TARGET L{level} base_path={base_path}, target={target}, command={command}")
        target_path_parts = target.split("/")
        if len(target_path_parts) == 1:
            util.debug(f"RESOLVE_TARGET L{level}: base_path={base_path}, {target} is a single-part target, look for matches in here")

            target_pattern = "^"+target_path_parts.pop(0)+"$"
            target_pattern = target_pattern.replace("*", r"[^\/]*")
            util.debug(f"RESOLVE_TARGET L{level}: base_path={base_path}, target_pattern={target_pattern}")

            deps_file = os.path.join(base_path, 'DEPS.yml')
            if self.config['deps_yaml_supported'] and os.path.isfile(deps_file):
                data = util.yaml_safe_load(deps_file)

                if data is not None:
                    deps_file_defaults = data.get('DEFAULTS', dict())

                    # Loop through all the targets in DEPS.yml, skipping DEFAULTS
                    for target_node, entry in data.items():

                        # Skip upper-case targets, including 'DEFAULTS':
                        if target_node == target_node.upper():
                            continue

                        m = re.match(target_pattern, target_node)
                        if not m:
                            # If the target_node in our deps_file doesn't match the pattern then skip.
                            continue

                        # Since we support a few schema flavors for a target (our 'target_node' key in a DEPS.yml file),
                        # santize the entry so it's a dict() with a 'deps' key:
                        entry_sanitized = deps_helpers.deps_list_target_sanitize(entry, target_node=target_node, deps_file=deps_file)

                        # Start with the defaults, and override with this entry_sanitized
                        entry_with_defaults = deps_file_defaults.copy()
                        entry_with_defaults.update(entry_sanitized)
                        entry = entry_with_defaults

                        multi_ignore_skip_this_target_node = False

                        # Check if this target_node should be skipped due to multi - ignore (commands or tools)
                        multi_ignore_commands_list = entry.get('multi', dict()).get('ignore', list())
                        for x in multi_ignore_commands_list:
                            if multi_ignore_skip_this_target_node:
                                # If we already found a reason to not use this target due to multi - ignore,
                                # then stop.
                                break

                            assert type(x) is dict, \
                                f'multi ignore: {x=} {multi_ignore_commands_list=} {deps_file_defaults=}' \
                                + f'  This needs to be a dict() entry with keys "commands" and "tools" {deps_file=} {target_node=}'

                            commands = x.get('commands', list())
                            tools = x.get('tools', list())
                            ignore_commands_list = deps_helpers.dep_str2list(commands)
                            ignore_tools_list = deps_helpers.dep_str2list(tools)

                            util.debug(f"RESOLVE_TARGET L{level}: {ignore_tools_list=}, {ignore_commands_list=} {target_node=}")
                            if command in ignore_commands_list or ignore_commands_list == ['None'] or \
                               len(ignore_commands_list) == 0:
                                # if commands: None, or commands is blank, then assume it is all commands.
                                # (note that yaml doesn't support *)

                                if which_tool(command) in ignore_tools_list or ignore_tools_list == ['None'] or \
                                   len(ignore_tools_list) == 0:
                                    # if tools: None, or tools is blank, then assume it is for all tools
                                    util.debug(f"RESOLVE_TARGET L{level}: Skipping {target_node=} due to using {command=} {which_tool(command)=} given {ignore_tools_list=} and {ignore_commands_list=}")
                                    multi_ignore_skip_this_target_node = True

                        if not multi_ignore_skip_this_target_node:
                            util.debug(f"RESOLVE_TARGET L{level}: Found dep {target_node=} matching {target_pattern=} {entry=}")
                            self.targets.append(os.path.join(base_path, target_node))




            # TODO(drew): deprecate old DEPS file.
            deps_file = os.path.join(base_path, "DEPS")
            if os.path.isfile(deps_file):
                f = open( deps_file, 'r' )
                util.debug(f"RESOLVE_TARGET L{level}: Opened '{deps_file}'")
                line_number = 0
                for line in f:
                    line_number += 1
                    # look for a pragma before clearing comments
                    m = re.match(r'^([^\#]*)\#\s*eda_multi\s+ignore\s+([^\#\s]*)\s*([^\#\s]*)?.*$', line)
                    if m:
                        ignore_target = m.group(1)
                        ignore_command = m.group(2)
                        ignore_toolstr = m.group(3) # can be comma separate list (no spaces tho)
                        ignore_tools_list = ignore_toolstr.split(',')
                        util.debug(f"RESOLVE_TARGET L{level}: {ignore_tools_list=}, {ignore_command=} {ignore_target=}")
                        if (ignore_command == command) or (ignore_command == "*"):
                            if ignore_toolstr != None and ignore_toolstr != "":
                                if which_tool(command) in ignore_tools_list:
                                    if ignore_target == "":
                                        util.debug(f"RESOLVE_TARGET L{level}: ignoring file, tool {which_tool(command)}, line: {line}")
                                        break
                                    else:
                                        util.debug(f"RESOLVE_TARGET L{level}: due to using tool {which_tool(command)}, ignoring line: {line}")
                                        continue
                            elif ignore_target == "":
                                util.debug(f"RESOLVE_TARGET L{level}: ignoring whole file {deps_file} due to {line} @ {line_number}")
                                break
                            else:
                                util.debug(f"RESOLVE_TARGET L{level}: ignoring line: {line}")
                                continue

                    # clear out comments
                    m = re.match(r'^([^\#]*)\#.*$', line)
                    if m:
                        line = m.group(1)
                    # look for the declaration of a target, which looks like "<target> : [dep .. dep] \n [dep .. dep] \n"
                    m = re.match(r'^\s*(\w+)\s*\:(.*)$', line)
                    if m:
                        dep_target = m.group(1)
                        m = re.match(target_pattern, dep_target)
                        if m:
                            util.debug(f"RESOLVE_TARGET L{level}: Found dep {dep_target} matching target pattern {target_pattern}")
                            self.targets.append(os.path.join(base_path, dep_target))
        else:
            # let's look at the first part of the multi-part target path, which should be a dir
            part = target_path_parts.pop(0)
            if part == ".":
                # just reprocess this directory (matches "./some/path" and retries as "some/path")
                util.debug(f"RESOLVE_TARGET L{level}: base_path={base_path}, processing {part}, recursing here")
                self.resolve_target(base_path, os.path.sep.join(target_path_parts), command, level+1)
            elif part == "...":
                util.debug(f"RESOLVE_TARGET L{level}: base_path={base_path}, processing {part}, recursing to check here")
                # first we check this dir: {"<base>",".../target"} should match "target" in <base>, so we call {"<base>","target"}
                self.resolve_target(base_path, os.path.sep.join(target_path_parts), command, level+1)
                # now we find all dirs in <base> ...
                util.debug(f"RESOLVE_TARGET L{level}: base_path={base_path}, processing {part}, looking through dirs...")
                wtg = os.listdir(base_path)
                for e in os.listdir(base_path):
                    util.debug(f"RESOLVE_TARGET L{level}: base_path={base_path},e={e},isdir={os.path.isdir(os.path.join(base_path,e))}")
                    if e == 'eda.work' or e == self.args['eda-dir']:
                        util.debug(f"RESOLVE_TARGET L{level}: base_path={base_path}, processing {part}, skipping work dir {e}")
                    elif os.path.islink(os.path.join(base_path,e)):
                        util.debug(f"RESOLVE_TARGET L{level}: base_path={base_path}, processing {part}, skipping link dir {e}")
                    elif os.path.isdir(os.path.join(base_path,e)):
                        util.debug(f"RESOLVE_TARGET L{level}: base_path={base_path}, processing {part}, recursing into {e}")
                        self.resolve_target(os.path.join(base_path,e), target, command, level+1)
            elif part.startswith("."):
                util.debug(f"RESOLVE_TARGET L{level}: base_path={base_path}, processing {part}, skipping hidden")
            elif part == self.args['eda-dir']:
                util.debug(f"RESOLVE_TARGET L{level}: base_path={base_path}, processing {part}, skipping eda.dir")
            elif os.path.isdir(os.path.join(base_path, part)):
                # reprocess in a lower directory (matches "some/...", enters "some/", and retries "...")
                util.debug(f"RESOLVE_TARGET L{level}: base_path={base_path}, processing {part}, recursing down")
                self.resolve_target(os.path.join(base_path, part), os.path.sep.join(target_path_parts), command, level+1)
            elif part == "*":
                # descend into every directory, we only go in if there's a DEPS though
                util.debug(f"RESOLVE_TARGET L{level}: base_path={base_path}, processing {part}, looking through dirs...")
                for e in os.listdir(base_path):
                    util.debug(f"RESOLVE_TARGET L{level}: base_path={base_path},e={e}")
                    if os.path.isdir(e):
                        util.debug(f"RESOLVE_TARGET L{level}: base_path={base_path},looking for ={os.path.join(base_path,e,'DEPS')}")
                        # TODO(drew): deprecate old DEPS file.
                        if os.path.isfile(os.path.join(base_path, e, "DEPS")) or \
                           os.path.isfile(os.path.join(base_path, e, "DEPS.yml")):
                            self.resolve_target(os.path.join(base_path, e), os.path.sep.join(target_path_parts), command, level+1)
            else:
                util.debug(f"RESOLVE_TARGET L{level}: base_path={base_path}, processing {part} ... but not sure what to do with it?")

    def process_tokens(self, tokens, process_all=True):
        # multi is special in the way it handles tokens, due to most of them being processed by a sub instance
        arg_tokens = [] # these are the tokens we will pass to the child eda processes
        command = ""
        target_globs = []
        parallelism = 1
        tool = None
        orig_tokens = tokens.copy()

        # TODO(drew): It might be nice to support CommandMulti.get_argparser() so we can
        # dump this help and know that --fake, --parallel, and --fail-if-no-targets exist
        # (like so this is auto-created via self.args dict())
        parser = argparse.ArgumentParser(prog='eda', add_help=False, allow_abbrev=False)
        bool_action_kwargs = util.get_argparse_bool_action_kwargs()
        parser.add_argument('--fake',     **bool_action_kwargs)
        parser.add_argument('--parallel', default=1, type=int)
        parser.add_argument('--fail-if-no-targets', action='store_true',  # don't support --no-(foo) on this arg.
                            help='set if you want `eda multi` to fail if no globbed targets found')
        try:
            parsed, unparsed = parser.parse_known_args(tokens + [''])
            unparsed = list(filter(None, unparsed))
        except argparse.ArgumentError:
            util.error(f'problem attempting to parse_known_args for {tokens=}')
        for key,value in vars(parsed).items():
            if key not in self.args and '_' in key:
                # try with dashes instead of _
                key = key.replace('_', '-')
            if value is None:
                continue
            self.args[key] = value # set fake, parallel, and fail_if_no_targets.
        if parsed.parallel < 1 or parsed.parallel > 256:
            self.error("Arg 'parallel' must be between 1 and 256")

        for value in unparsed:
            if value in config['command_handler'].keys():
                command = value
                unparsed.remove(value)
                break

        # Need to know the tool for this command, either it was set correctly via --tool and/or
        # the command (class) will tell us.
        tool = which_tool(command)

        util.debug(f"Multi: {unparsed=}, looking for target_globs")
        for token in unparsed:
            if token.startswith("-") or token.startswith("+"):
                arg_tokens.append(token)
            else:
                target_globs.append(token)

        if command == "": self.error(f"Didn't get a command after 'multi'!")

        # now we need to expand the target list
        util.debug(f"Multi: {orig_tokens=}")
        util.debug(f"Multi: {command=}")
        util.debug(f"Multi: {config=}")
        util.debug(f"Multi: {tool=}")
        util.debug(f"Multi: {target_globs=}")
        util.debug(f"Multi: {arg_tokens=}")
        self.targets = []
        cwd = util.getcwd()
        current_targets = 0
        for t in target_globs:
            self.resolve_target(cwd, t, command)
            if len(self.targets)==current_targets:
                # we didn't get any new targets, try globbing this one
                for f in glob.glob(t):
                    if os.path.isfile(f):
                        util.info(f"Adding raw file target: {f}")
                        self.targets.append(f)
            current_targest = len(self.targets)
        util.info(f"Multi: Expanded {target_globs} to {len(self.targets)} {command} targets")
        #sys.exit(0)
        if parsed.fail_if_no_targets and len(self.targets) == 0:
            util.error(f'Multi: --fail-if-no-targets set, and {self.targets=}')
        util.info(f"Multi: About to run: ", end="")
        if len(self.targets) > 20:
            for i in range(10):
                util.info(f"{self.targets[i]} , ", start="", end="")
            util.info(f"... ", start="", end="")
            for i in range(len(self.targets)-10, len(self.targets)):
                util.info(f" , {self.targets[i]}", start="", end="")
            util.info("", start="")
        else:
            util.info(" , ".join(self.targets), start="")
        util.debug(f"Multi: converting list of targets into list of jobs")
        self.jobs = []
        # TODO(drew): 'eda multi' will reinvoke 'eda', this may be flaky.
        eda_path = get_eda_exec('multi')
        for target in self.targets:
            command_list = [ eda_path, command ]
            if tool: command_list += [ '--tool', tool ]
            # if self.args['parallel']: command_list += ['--quiet']
            command_list += arg_tokens # put the args prior to the target.
            command_list += [target]
            this_job_dict = {
                'name' : target,
                'index' : len(self.jobs),
                'command_list' : command_list
            }
            util.debug(f'{this_job_dict=}')
            self.jobs.append(this_job_dict)
        self.run_jobs(command)
        return self.status


class CommandSweep(CommandDesign, CommandParallel):
    def __init__(self, config:dict):
        CommandDesign.__init__(self, config, "sweep")
        CommandParallel.__init__(self, config, "sweep")

    def process_tokens(self, tokens, process_all=True):
        # multi is special in the way it handles tokens, due to most of them being processed by a sub instance
        sweep_axis_list = []
        command = ""
        target = ""
        arg_tokens = []

        parser = argparse.ArgumentParser(prog='eda', add_help=False, allow_abbrev=False)
        parser.add_argument('--parallel', default=1, type=int)
        try:
            parsed, unparsed = parser.parse_known_args(tokens + [''])
            unparsed = list(filter(None, unparsed))
        except argparse.ArgumentError:
            util.error(f'problem attempting to parse_known_args for {tokens=}')
        for k,v in vars(parsed).items():
            self.args[k] = v # set parallel.
        if self.args['parallel'] < 1 or self.args['parallel'] > 256:
            self.error("Arg 'parallel' must be between 1 and 256")

        for value in unparsed:
            if value in config['command_handler'].keys():
                command = value
                unparsed.remove(value)
                break

        tokens = unparsed


        while len(tokens):
            token = tokens.pop(0)

            # command and --parallel already processed by argparse

            m = re.match(r'(\S+)\=\(([\d\.]+)\,([\d\.]+)(,([\d\.]+))?\)', token)
            if m:
                sweep_axis = { 'key' : m.group(1),
                               'values' : [  ] }
                for v in range(float(m.group(2)), (float(m.group(3))+1), (float(m.group(5)) if m.group(4) != None else 1.0)):
                    sweep_axis['values'].append(v)
                util.debug(f"Sweep axis: {sweep_axis['key']} : {sweep_axis['values']}")
                sweep_axis_list.append(sweep_axis)
                continue
            m = re.match(r'(\S+)\=\[([^\]]+)\]', token)
            if m:
                sweep_axis = { 'key' : m.group(1), 'values' : [] }
                for v in m.group(2).split(','):
                    v = v.replace(' ','')
                    sweep_axis['values'].append(v)
                util.debug(f"Sweep axis: {sweep_axis['key']} : {sweep_axis['values']}")
                sweep_axis_list.append(sweep_axis)
                continue
            if token.startswith('--') or token.startswith('+'):
                arg_tokens.append(token)
                continue
            if self.resolve_target(token, no_recursion=True):
                if target != "":
                    self.error(f"Sweep can only take one target, already got {target}, now getting {token}")
                target = token
                continue
            self.error(f"Sweep doesn't know what to do with arg '{token}'")
        if command == "": self.error(f"Didn't get a command after 'sweep'!")

        # now we need to expand the target list
        util.debug(f"Sweep: command:    '{command}'")
        util.debug(f"Sweep: arg_tokens: '{arg_tokens}'")
        util.debug(f"Sweep: target:     '{target}'")

        # now create the list of jobs, support one axis
        self.jobs = []
        self.expand_sweep_axis(command, target, arg_tokens, sweep_axis_list)
        return self.run_jobs(command)

    def expand_sweep_axis(self, command, target, arg_tokens, sweep_axis_list, sweep_string=""):
        util.debug(f"Entering expand_sweep_axis: command={command}, target={target}, arg_tokens={arg_tokens}, sweep_axis_list={sweep_axis_list}")
        if len(sweep_axis_list) == 0:
            # we aren't sweeping anything, create one job
            snapshot_name = target.replace('../','').replace('/','_') + sweep_string
            # TODO(drew): 'eda multi' will reinvoke 'eda', this may be flaky.
            eda_path = get_eda_exec('sweep')
            self.jobs.append({
                'name' : snapshot_name,
                'index' : len(self.jobs),
                'command_list' : ([eda_path, command, target, '--job_name', snapshot_name] + arg_tokens)
            })
            return
        sweep_axis = sweep_axis_list[0]
        for v in sweep_axis['values']:
            this_arg_tokens = []
            for a in arg_tokens:
                this_arg_tokens.append(a.replace(sweep_axis['key'], f"{v}"))
            next_sweep_axis_list = []
            if len(sweep_axis_list)>1:
                next_sweep_axis_list = sweep_axis_list[1:]
            v_string = f"{v}".replace('.','p')
            self.expand_sweep_axis(command, target, this_arg_tokens, next_sweep_axis_list, sweep_string+f"_{sweep_axis['key']}_{v_string}")

class CommandFList(CommandDesign):
    def __init__(self, config:dict):
        CommandDesign.__init__(self, config, "flist")
        self.args['eda-dir'] = 'eda.flist' # use a special directory here if files are generated.
        self.args['out'] = "flist.out"
        self.args['emit-define'] = True
        self.args['emit-incdir'] = True
        self.args['emit-v'] = True
        self.args['emit-sv'] = True
        self.args['emit-vhd'] = True
        self.args['prefix-define'] = "+define+"
        self.args['prefix-incdir'] = "+incdir+"
        self.args['prefix-v'] = ""
        self.args['prefix-sv'] = ""
        self.args['prefix-vhd'] = ""
        self.args['single-quote-define'] = False
        self.args['quote-define'] = True
        self.args['xilinx'] = False # we don't want --xilinx to error, but it doesn't do anything much
        self.args['build-script'] = "" # we don't want this to error either

    def set_tool_defines(self):
        pass

    def process_tokens(self, tokens, process_all=True):
        CommandDesign.process_tokens(self, tokens, process_all)
        self.do_it()
        return self.status

    def get_flist_dict(self) -> dict:
        self.set_tool_defines()

        # This will ignore args, and build a dict that an external caller can use, without generating
        # an actual .f file.
        ret = dict()
        for key in ['files_sv', 'files_v', 'files_vhd', 'defines', 'incdirs']:
            # These keys must exist, all are lists, defines is a dict
            x = getattr(self, key, None)
            if type(x) is list or type(x) is dict:
                ret[key] = x.copy()
            else:
                ret[key] = x
        return ret


    def do_it(self):
        # add defines for this job
        self.set_tool_defines()
        if (self.args['top'] != ""):
            if os.path.exists(self.args['out']):
                if self.args['force']:
                    util.info(f"Removing existing {self.args['out']}")
                    os.remove(self.args['out'])
                else:
                    self.error(f"Not overwriting {self.args['out']} unless you specify --force")

            # Note - we create a work_dir in case any DEPS commands created files that need to be
            # added to our sources.
            # TODO(drew): If we want this flist with generated files preserved, then this "create_work_dir()"
            # cannot use ./eda.work/ if other calls delete it. Consider: ./eda.flist/ ?
            self.create_work_dir()
            self.run_dep_commands()

            util.debug(f"Opening {self.args['out']} for writing")
            with open( self.args['out'] , 'w' ) as fo:
                print(f"## {self.args=}", file=fo)
                if self.args['emit-define']:
                    for d in self.defines:
                        if self.defines[d] == None:
                            print(f"{self.args['prefix-define']}{d}", file=fo)
                        else:
                            if self.args['single-quote-define'] : quote = '\''
                            elif self.args['quote-define'] : quote = '"'
                            else : quote = ''
                            print(f"{self.args['prefix-define']}{quote}{d}={self.defines[d]}{quote}", file=fo)
                if self.args['emit-incdir']:
                    for i in self.incdirs:
                        print(f"{self.args['prefix-incdir']}{i}", file=fo)
                if self.args['emit-v']:
                    for f in self.files_v:
                        print(f"{self.args['prefix-v']}{f}", file=fo)
                if self.args['emit-sv']:
                    for f in self.files_sv:
                        print(f"{self.args['prefix-sv']}{f}", file=fo)
                if self.args['emit-vhd']:
                    for f in self.files_vhd:
                        print(f"{self.args['prefix-vhd']}{f}", file=fo)
            util.info(f"Created {self.args['out']}")


class CommandWaves(CommandDesign):
    def __init__(self, config:dict):
        Command.__init__(self, config, "waves")

    def process_tokens(self, tokens, process_all=True):
        wave_file = None
        wave_dirs = []
        while len(tokens):
            # see if it's a flag/option like --debug, --seed <n>, etc
            rc = Command.process_tokens(self, tokens, process_all=False)
            if rc == 0:
                continue
            if os.path.isfile(tokens[0]):
                if (wave_file != None):
                    self.error(f"Was already given wave file {wave_file}, not sure what to do with {tokens[0]}")
                wave_file = os.path.abspath(tokens[0])
                tokens.pop(0)
                continue
            if os.path.isdir(tokens[0]):
                if (wave_file != None):
                    self.error(f"Was already given wave file {wave_file}, not sure what to do with {tokens[0]}")
                wave_dirs.append(tokens[0])
            self.error("Didn't understand command token: '%s' in CommandWaves" % (tokens[0]))
        if not wave_file:
            util.info(f"need to look for wave file")
            # we weren't given a wave file, so we will look for one!
            if (len(wave_dirs) == 0) and os.path.isdir(self.args['eda-dir']):
                wave_dirs.append(self.args['eda-dir'])
            if (len(wave_dirs) == 0):
                wave_dirs.append('.')
            all_files = []
            for d in wave_dirs:
                util.info(f"Looking for wavedumps below: {d}")
                for root, dirs, files in os.walk(d):
                    for f in files:
                        for e in [ '.wdb', '.vcd', '.wlf', '.fst' ]:
                            if f.endswith(e):
                                util.info(f"Found wave file: {os.path.join(root,f)}")
                                all_files.append(os.path.join(root,f))
            if len(all_files) > 1:
                all_files.sort(key=lambda f: os.path.getmtime(f))
                util.info(f"Choosing: {self.args['file']} (newest)")
            if len(all_files):
                wave_file = all_files[-1]
            else:
                self.error(f"Couldn't find any wave files below: {','.join(wave_dirs)}")

        wave_file = os.path.abspath(wave_file)
        util.info(f"decided on opening: {wave_file}")

        # TODO(drew): this feels a little customized per-tool, perhaps there's a better
        # way to abstract this configuration for adding other waveform viewers.
        if wave_file.endswith('.wdb'):
            if 'vivado' in glbl_tools_loaded:
                tcl_name = wave_file + '.waves.tcl'
                with open( tcl_name,'w') as fo :
                    print( 'current_fileset', file=fo)
                    print( 'open_wave_database %s' % wave_file, file=fo)
                command_list = ['vivado', '-source', tcl_name]
                self.exec(os.path.dirname(wave_file), command_list)
            else:
                self.error(f"Don't know how to open {wave_file} without Vivado")
        elif wave_file.endswith('.wlf'):
            if 'questa' in glbl_tools_loaded:
                command_list = ['vsim', wave_file]
                self.exec(os.path.dirname(wave_file), command_list)
            else:
                self.error(f"Don't know how to open {wave_file} without Questa")
        elif wave_file.endswith('.fst'):
            if 'gtkwave' in glbl_tools_loaded:
                command_list = ['gtkwave', wave_file]
                self.exec(os.path.dirname(wave_file), command_list)
            else:
                self.error(f"Don't know how to open {wave_file} without GtkWave")
        elif wave_file.endswith('.vcd'):
            if 'questa' in glbl_tools_loaded:
                command_list = ['vsim', wave_file]
                self.exec(os.path.dirname(wave_file), command_list)
            elif 'vivado' in glbl_tools_loaded:
                # I don't think this works, this is a placeholder, I'm sure Vivado can open a VCD
                # Also this would be a great place to start adding some open source (GTKWAVE) support...
                tcl_name = wave_file + '.waves.tcl'
                with open( tcl_name,'w') as fo :
                    print( 'current_fileset', file=fo)
                    print( 'open_wave_database %s' % wave_file, file=fo)
                command_list = ['vivado', '-source', tcl_name]
                self.exec(os.path.dirname(wave_file), command_list)
            else:
                self.error(f"Don't know how to open {wave_file} without Vivado or Questa")


class CommandUpload(CommandDesign):
    def __init__(self, config:dict):
        Command.__init__(self, config, "upload")

    def process_tokens(self, tokens, process_all=True):
        Command.process_tokens(self, tokens, process_all)
        self.create_work_dir()
        self.run_dep_commands()
        return self.do_it()

class CommandOpen(CommandDesign):
    def __init__(self, config:dict):
        Command.__init__(self, config, "open")

    def process_tokens(self, tokens, process_all=True):
        Command.process_tokens(self, tokens, process_all)
        return self.do_it()

class ToolVerilator(Tool):
    def __init__(self):
        Tool.__init__(self)
        self.verilator_major = 0
        self.verilator_minor = 0
        self.args['tool'] = 'verilator'

    def get_versions(self):
        verilator_path = shutil.which('verilator')
        if verilator_path is None:
            self.error('"verilator" not in path, need to get it (sudo apt-get install verilator)')
        verilator_coverage_path = shutil.which('verilator_coverage')
        if verilator_coverage_path is None:
            self.error('"verilator_coverage" not in path, need from same path as "verilator"')

        verilator_version_ret = subprocess.run(['verilator', '--version'], capture_output=True)
        util.debug(f'{verilator_path=} {verilator_version_ret=}')
        l = verilator_version_ret.split() # 'Verilator 5.027 devel rev v5.026-92-g403a197e2
        if len(l) < 1:
            self.error('verilator --version: returned unexpected string {verilator_version_ret=}')
        v = l[1].split('.')
        if len(v) != 2:
            self.error('verilator --version: returned unexpected string {verilator_version_ret=} {l[1]=}')
        self.verilator_major = l[0]
        self.verilator_minor = l[1]
        return

    def set_tool_defines(self):
        pass

class CommandSimVerilator(CommandSim, ToolVerilator):
    def __init__(self, config:dict):
        CommandSim.__init__(self, config)
        ToolVerilator.__init__(self)
        self.args['gui'] = False
        self.args['tcl-file'] = None
        self.log_bad_strings = ['ERROR: ', '%Error', '%Fatal']

    def set_tool_defines(self):
        ToolVerilator.set_tool_defines(self)

    # We do not override CommandSim.do_it()
    def prepare_compile(self):
        self.set_tool_defines()
        if self.args['xilinx']:
            self.error('Error: --xilinx with Verilator is not yet supported', do_exit=False)

        self.verilate_command_lists = self.get_compile_command_lists()
        self.verilated_exec_command_lists  = self.get_simulate_command_lists()
        self.verilated_post_exec_coverage_command_lists = self.get_post_simulate_command_lists()

        paths = ['obj_dir', 'logs']
        util.safe_mkdirs(base=self.args['work-dir'], new_dirs=paths)

        util.write_shell_command_file(dirpath=self.args['work-dir'], filename='compile_only.sh',
                                      command_lists=self.verilate_command_lists, line_breaks=True)

        util.write_shell_command_file(dirpath=self.args['work-dir'], filename='simulate_only.sh',
                                      command_lists = self.verilated_exec_command_lists +
                                      (self.verilated_post_exec_coverage_command_lists
                                       if self.args.get('coverage', True) else [])
                                      )

        util.write_shell_command_file(dirpath=self.args['work-dir'], filename='all.sh',
                                      command_lists = [
                                          ['./pre_compile_dep_shell_commands.sh'],
                                          ['./compile_only.sh'],
                                          ['./simulate_only.sh'],
                                      ])

        util.write_eda_config_and_args(dirpath=self.args['work-dir'], command_obj_ref=self)

    def compile(self):
        if self.args['stop-before-compile']:
            return
        self.run_commands_check_logs(self.verilate_command_lists, check_logs=False) # There are no logs

    def elaborate(self):
        pass

    def simulate(self):
        if self.args['stop-before-compile'] or self.args['stop-after-compile'] or \
           self.args['stop-after-elaborate']:
            # don't run this if we're stopping before/after compile/elab
            return

        # Note that this is not returning a pass/fail bash return code,
        # so we will likely have to log-scrape to deterimine pass/fail.
        self.run_commands_check_logs(self.verilated_exec_command_lists, log_filename='sim.log')

        if self.args.get('coverage', True):
            self.run_commands_check_logs(self.verilated_post_exec_coverage_command_lists, log_filename='sim.log')

    def get_compile_command_lists(self):

        verilate_command_list = [
            'verilator',
            '--binary',
            '--timing',
            '--assert',
            '--autoflush',
            '-j', '2', # we let verilator use 2 threads per job, to keep CPUs busy when we are cycling through lots of jobs
            # Disable Warnings with -Wno-Message.
            '-Wno-Width',
            '-Wno-SELRANGE',
            '-Wno-CASEINCOMPLETE',
            '-Wno-UNSIGNED', # In a parameterized .sv codebase, avoid warning for value >= P (if P==0)
            '-Wno-TIMESCALEMOD', # If one file has `timescale, then they all must (disable this)
            '-Wno-REALCVT', # implicit conversion of real to integer
            '-sv',
        ]

        # measurements taken from running eda multi sim top/tests/oc.*test --parallel 8 on AMD 5950X
        #  oc_chip_status_test  vvv               fast compile, very long runtime (simulation dominated)
        #  oc_cos_mbist_4x32_test     vvv         long compile, not long runtime  (compile/elab dominated)
        #'-CFLAGS', '-O0', # 7:43 - 9:09
        #'-CFLAGS', '-O1', # 0:30 - 3:47
        #'-CFLAGS', '-O2', # 0:24 - 5:55
        #'-CFLAGS', '-O3', # 0:22 - 6:07

        # We can only support one -CFLAGS followed by one -O[0-9] arg in self.args['verilate-args']:
        # TODO(drew): move this to util, sanitize verilate and compiler args:
        verilate_cflags_args_dict = dict()
        verilate_args = list() # will be combined verilate_args + compile-args
        prev_arg_is_cflags = False
        util.debug(f"{self.args['verilate-args']=}")
        util.debug(f"{self.args['compile-args']=}")
        for iter, arg in enumerate(self.args['verilate-args'] + self.args['compile-args']):
            # pick the first ones we see of these:
            if arg == '-CFLAGS':
                prev_arg_is_cflags = True
                if arg not in verilate_cflags_args_dict:
                    # We can only have 1
                    verilate_cflags_args_dict[arg] = True
                    verilate_args.append(arg)
                else:
                    util.debug('fPrevious saw -CFLAGS args {verilate_cflags_args_dict=}, skipping new {arg=}')

            elif arg.startswith('-O') and len(arg) == 3:
                if '-O' not in verilate_cflags_args_dict and prev_arg_is_cflags:
                    # We can only have 1
                    verilate_cflags_args_dict['-O'] = arg[-1]
                    verilate_args.append(arg)
                else:
                    util.debug('fPrevious saw -CFLAGS args {verilate_cflags_args_dict=}, skipping new {arg=}')
                prev_arg_is_cflags = False

            else:
                prev_arg_is_cflags = False
                verilate_args.append(arg)

        util.debug(f'{verilate_args=}')

        if '-CFLAGS' in verilate_args:
            # add whatever args were passed via 'compile-args' or 'verilate_args'. Note these will
            # take precedence over the --optimize arg.
            pass
        elif self.args['optimize']:
            verilate_command_list += '-CFLAGS', '-O3' # if a test is marked --optimize then we give it --O3 to pull down runtime
        else:
            verilate_command_list += '-CFLAGS', '-O1' # else we use -O1 which has best overall behavior

        verilate_command_list += verilate_args

        if self.args.get('waves', False):
            verilate_command_list += [
                '--trace-fst',
                '--trace-structs',
                '--trace-params',
            ]

        if self.args.get('coverage', True):
            verilate_command_list += [
                '--coverage'
            ]



        verilate_command_list += [
            '-top', self.args['top'],
            '-o', 'sim.exe',
        ]

        # incdirs
        for value in self.incdirs:
            verilate_command_list += [ f"+incdir+{value}" ]

        for k,v in self.defines.items():
            if v is None:
                verilate_command_list += [ f'+define+{k}' ]
            else:
                # Generally we should only support int and str python types passed as
                # +define+{k}={v}, but also for SystemVerilog plusargs
                verilate_command_list += [ f'+define+{k}={sanitize_defines_for_sh(v)}' ]

        assert len(self.files_sv) + len(self.files_v) > 0, \
            f'{self.target=} {self.files_sv=} and {self.files_v=} are empty, cannot call verilator'

        verilate_command_list += list(self.files_sv) + list(self.files_v)

        return [verilate_command_list] # single entry list


    def get_simulate_command_lists(self):

        # verilator needs the seed to be < 2*31-1
        verilator_seed = int(self.args['seed']) & 0xfff_ffff

        assert type(self.args['sim-plusargs']) is list, \
            f'{self.target=} {type(self.args["sim-plusargs"])=} but must be list'

        sim_plusargs = list()
        for x in self.args['sim-plusargs']:
            # For Verilator we need to add a +key=value if the + is missing
            if x[0] != '+':
                x = f'+{x}'
            sim_plusargs.append(x)

        # TODO(drew): don't have a use-case yet for self.args['sim-library', 'elab-args'] in the verilated executable
        # 'simulation' command list, but we may need to support them if we have more than 'work' library.

        # Note the | tee sim.log will ruin bash error codes, so we'll have to scrape
        # sim.log for errors later.
        verilated_exec_command_list = [
            './obj_dir/sim.exe',
            '+verilator+error+limit+100',
            f'+verilator+seed+{verilator_seed}',
            '+trace' if self.args['waves'] else '',
        ] + sim_plusargs + self.args['sim-args'] + [
            '|', 'tee sim.log',
        ]

        return [verilated_exec_command_list] # single entry list


    def get_post_simulate_command_lists(self):

        verilated_post_exec_coverage_command_list = [
            'verilator_coverage',
            '--annotate', 'logs/annotated',
            '--annotate-min', '1',
            'coverage.dat'
            '|', 'tee coverage.log'
        ]
        return [verilated_post_exec_coverage_command_list] # single entry list



class CommandElabVerilator(CommandSimVerilator):
    def __init__(self, config:dict):
        super().__init__(config)
        self.args['stop-after-elaborate'] = True


class ToolVivado(Tool):
    def __init__(self):
        Tool.__init__(self)
        self.vivado_year = None
        self.vivado_release = None
        self.args['xilinx'] = False
        self.args['part'] = 'xcu200-fsgd2104-2-e'
        self.args['tool'] = 'vivado'

    def get_versions(self):
        if self.vivado_year != None:
            return
        vivado_path = shutil.which('vivado')
        if vivado_path == None:
            self.error("Vivado not in path, need to setup (i.e. source /opt/Xilinx/Vivado/2022.2/settings64.sh")
        util.debug("vivado_path = %s" % vivado_path)
        m = re.search(r'(\d\d\d\d)\.(\d)', vivado_path)
        if m:
            self.vivado_year = int(m.group(1))
            self.vivado_release = int(m.group(2))
            self.vivado_version = float(m.group(1)+"."+m.group(2))
            return
        self.error("Vivado path doesn't specificy version, expecting (dddd.d)")

    # we wait to call this as part of do_it because we only want to run all this after all options
    # have been processed, as things like --xilinx will affect the defines.  Maybe it should be
    # broken into a tool vs library phase, but likely command line opts can also affect tools...
    def set_tool_defines(self):
        # Will only be called from an object which also inherits from CommandDesign, i.e. has self.defines
        self.get_versions()
        self.defines['OC_TOOL_VIVADO'] = None
        self.defines['OC_TOOL_VIVADO_%4d_%d' % (self.vivado_year, self.vivado_release)] = None
        if self.args['xilinx']:
            self.defines['OC_LIBRARY_ULTRASCALE_PLUS'] = None
            self.defines['OC_LIBRARY'] = "1"
        else:
            self.defines['OC_LIBRARY_BEHAVIORAL'] = None
            self.defines['OC_LIBRARY'] = "0"
        # Code can be conditional on Vivado versions and often keys of "X or older" ...
        if (self.vivado_version <= 2021.1): self.defines['OC_TOOL_VIVADO_2021_1_OR_OLDER'] = None
        if (self.vivado_version <= 2021.2): self.defines['OC_TOOL_VIVADO_2021_2_OR_OLDER'] = None
        if (self.vivado_version <= 2022.1): self.defines['OC_TOOL_VIVADO_2022_1_OR_OLDER'] = None
        if (self.vivado_version <= 2022.2): self.defines['OC_TOOL_VIVADO_2022_2_OR_OLDER'] = None
        if (self.vivado_version <= 2023.1): self.defines['OC_TOOL_VIVADO_2023_1_OR_OLDER'] = None
        if (self.vivado_version <= 2023.2): self.defines['OC_TOOL_VIVADO_2023_2_OR_OLDER'] = None
        if (self.vivado_version <= 2024.1): self.defines['OC_TOOL_VIVADO_2024_1_OR_OLDER'] = None
        if (self.vivado_version <= 2024.2): self.defines['OC_TOOL_VIVADO_2024_2_OR_OLDER'] = None
        # ... or "X or newer" ...
        if (self.vivado_version >= 2021.1): self.defines['OC_TOOL_VIVADO_2021_1_OR_NEWER'] = None
        if (self.vivado_version >= 2021.2): self.defines['OC_TOOL_VIVADO_2021_2_OR_NEWER'] = None
        if (self.vivado_version >= 2022.1): self.defines['OC_TOOL_VIVADO_2022_1_OR_NEWER'] = None
        if (self.vivado_version >= 2022.2): self.defines['OC_TOOL_VIVADO_2022_2_OR_NEWER'] = None
        if (self.vivado_version >= 2023.1): self.defines['OC_TOOL_VIVADO_2023_1_OR_NEWER'] = None
        if (self.vivado_version >= 2023.2): self.defines['OC_TOOL_VIVADO_2023_2_OR_NEWER'] = None
        if (self.vivado_version >= 2024.1): self.defines['OC_TOOL_VIVADO_2024_1_OR_NEWER'] = None
        if (self.vivado_version >= 2024.2): self.defines['OC_TOOL_VIVADO_2024_2_OR_NEWER'] = None
        # Our first tool workaround.  Older Vivado's don't correctly compare types in synthesis (sim seems OK, argh)
        if (self.vivado_version < 2023.2): self.defines['OC_TOOL_BROKEN_TYPE_COMPARISON'] = None
        util.debug(f"Setup tool defines: {self.defines}")


class CommandSimVivado(CommandSim, ToolVivado):

    sim_libraries = [
        'xil_defaultlib',
        'unisims_ver',
        'unimacro_ver',
        'xpm',
        'secureip',
        'xilinx_vip',
    ]

    def __init__(self, config:dict):
        CommandSim.__init__(self, config)
        ToolVivado.__init__(self)
        # add args specific to this simulator
        self.args['gui'] = False
        self.args['tcl-file'] = "sim.tcl"
        self.args['fpga'] = ""


    def set_tool_defines(self):
        ToolVivado.set_tool_defines(self)

    # We do not override CommandSim.do_it(), CommandSim.check_logs_for_errors(...)


    def prepare_compile(self):
        self.set_tool_defines()
        self.xvlog_commands = self.get_compile_command_lists()
        self.xelab_commands = self.get_elaborate_command_lists()
        self.xsim_commands = self.get_simulate_command_lists()

        util.write_shell_command_file(dirpath=self.args['work-dir'], filename='compile.sh',
                                      command_lists=self.xvlog_commands)
        util.write_shell_command_file(dirpath=self.args['work-dir'], filename='elaborate.sh',
                                      command_lists=self.xelab_commands)
        util.write_shell_command_file(dirpath=self.args['work-dir'], filename='simulate.sh',
                                      command_lists=self.xsim_commands)
        util.write_shell_command_file(dirpath=self.args['work-dir'], filename='all.sh',
                                      command_lists = [
                                          ['./pre_compile_dep_shell_commands.sh'],
                                          ['./compile.sh'],
                                          ['./elaborate.sh'],
                                          ['./simulate.sh'],
                                      ])

        util.write_eda_config_and_args(dirpath=self.args['work-dir'], command_obj_ref=self)

    def compile(self):
        if self.args['stop-before-compile']:
            return
        self.run_commands_check_logs(self.xvlog_commands, check_logs=True, log_filename='xvlog.log')

    def elaborate(self):
        if self.args['stop-before-compile'] or self.args['stop-after-compile']:
            return
        # In this flow, we need to run compile + elaborate separately (unlike ModelsimASE)
        self.run_commands_check_logs(self.xelab_commands, check_logs=True, log_filename='xelab.log',
                                     must_strings=['Built simulation snapshot snapshot'])

    def simulate(self):
        if self.args['stop-before-compile'] or self.args['stop-after-compile'] or \
           self.args['stop-after-elaborate']:
            return
        self.run_commands_check_logs(self.xsim_commands, check_logs=True, log_filename='xsim.log')

    def get_compile_command_lists(self) -> list():
        self.set_tool_defines()
        ret = list()

        # compile verilog
        if len(self.files_v) or self.args['xilinx']:
            command_list = [ 'xvlog' ]
            if util.args['verbose']: command_list += ['-v', '2']
            if self.args['xilinx']:
                command_list += [ os.path.join( os.environ['XILINX_VIVADO'], 'data/verilog/src/glbl.v') ]
            for value in self.incdirs:
                command_list.append('-i')
                command_list.append(value)
            for key in self.defines.keys():
                value = self.defines[key]
                command_list.append('-d')
                if value == None:    command_list.append(key)
                elif "\'" in value:  command_list.append("\"%s=%s\"" % (key, value))
                else:                command_list.append("\'%s=%s\'" % (key, value))
            command_list += self.args['compile-args']
            command_list += self.files_v
            ret.append(command_list)

        # compile systemverilog
        if len(self.files_sv):
            command_list = [ 'xvlog' ]
            command_list.append('-sv')
            if util.args['verbose']: command_list += ['-v', '2']
            for value in self.incdirs:
                command_list.append('-i')
                command_list.append(value)
            for key in self.defines.keys():
                value = self.defines[key]
                command_list.append('-d')
                if value == None:    command_list.append(key)
                elif "\'" in value:  command_list.append("\"%s=%s\"" % (key, value))
                else:                command_list.append("\'%s=%s\'" % (key, value))
            command_list += self.args['compile-args']
            command_list += self.files_sv
            ret.append(command_list)

        return ret # list of lists

    def get_elaborate_command_lists(self):
        # elab into snapshot
        command_list = [ 'xelab' ]
        command_list += [ self.args['top'], '-s', 'snapshot', '-timescale', '1ns/1ps', '--stats' ]
        if self.args['gui'] and self.args['waves']: command_list += ['-debug', 'all']
        elif self.args['gui']: command_list += ['-debug', 'typical']
        elif self.args['waves']: command_list += ['-debug', 'wave']
        if util.args['verbose']: command_list += ['-v', '2']
        if self.args['xilinx']:
            self.sim_libraries += self.args['sim-library'] # Add any command line libraries
            for x in self.sim_libraries:
                command_list += ['-L', x]
            command_list += ['glbl']
        command_list += self.args['elab-args']
        return [command_list]

    def get_simulate_command_lists(self):
        # create TCL
        tcl_name = os.path.abspath(os.path.join(self.args['work-dir'], self.args['tcl-file']))
        with open( tcl_name, 'w' ) as fo:
            if self.args['waves']:
                if self.args['waves-start']:
                    print("run %d ns" % self.args['waves-start'], file=fo)
                print("log_wave -recursive *", file=fo)
            print("run -all", file=fo)
            if not self.args['gui']:
                print("exit", file=fo)

        sv_seed = str(self.args['seed'])

        assert type(self.args["sim-plusargs"]) is list, \
            f'{self.target=} {type(self.args["sim-plusargs"])=} but must be list'

        # xsim uses: --testplusarg foo=bar
        xsim_plusargs_list = list()
        for x in self.args['sim-plusargs']:
            xsim_plusargs_list.append('--testplusarg')
            if x[0] == '+':
                x = x[1:]
            xsim_plusargs_list.append(f'\"{x}\"')

        # execute snapshot
        command_list = [ 'xsim' ]
        if self.args['gui']: command_list += ['-gui']
        command_list += ['snapshot', '--stats', '--tclbatch', tcl_name, "--onerror", "quit",
                         "--sv_seed", sv_seed] + xsim_plusargs_list
        command_list += self.args['sim-args']
        return [command_list] # single command



class CommandElabVivado(CommandSimVivado):
    def __init__(self, config:dict):
        CommandSimVivado.__init__(self, config)
        # add args specific to this simulator
        self.args['stop-after-elaborate'] = True


class CommandSynthVivado(CommandSynth, ToolVivado):
    def __init__(self, config:dict):
        CommandSynth.__init__(self, config)
        ToolVivado.__init__(self)
        # add args specific to this simulator
        self.args['gui'] = False
        self.args['tcl-file'] = "synth.tcl"
        self.args['xdc'] = ""
        self.args['fpga'] = ""

    def do_it(self):
        # add defines for this job
        self.set_tool_defines()

        # create TCL
        tcl_file = os.path.abspath(os.path.join(self.args['work-dir'], self.args['tcl-file']))
        v = ""
        if util.args['verbose']: v += " -verbose"
        elif util.args['quiet']: v += " -quiet"
        defines = ""
        for key in self.defines.keys():
            value = self.defines[key]
            defines += (f"-verilog_define {key}" + (" " if value == None else f"={value} "))
        incdirs = ""
        if len(self.incdirs):
            incdirs = " -include_dirs "+";".join(self.incdirs)
        flatten = ""
        if self.args['flatten-all']:    flatten = "-flatten_hierarchy full"
        elif self.args['flatten-none']: flatten = "-flatten_hierarchy none"
        with open( tcl_file, 'w' ) as fo:
            for f in self.files_v:     print(f"read_verilog {f}", file=fo)
            for f in self.files_sv:    print(f"read_verilog -sv {f}", file=fo)
            for f in self.files_vhd:   print(f"add_file {f}", file=fo)
            if self.args['xdc'] != "":
                default_xdc = False
                xdc_file = os.path.abspath(self.args['xdc'])
            else:
                default_xdc = True
                xdc_file = os.path.abspath(os.path.join(self.args['work-dir'], "default_constraints.xdc"))
                util.info(f"Creating default constraints: clock:{self.args['clock-ns']}ns, "+
                          f"idelay:{self.args['idelay-ns']}ns, odelay:{self.args['odelay-ns']}ns")
                with open( xdc_file, 'w' ) as ft:
                    print(f"create_clock -add -name clock -period {self.args['clock-ns']} [get_ports {{clock}}]", file=ft)
                    print(f"set_input_delay -max {self.args['idelay-ns']} -clock clock "+
                          f"[get_ports * -filter {{DIRECTION == IN && NAME !~ \"clock\"}}]", file=ft)
                    print(f"set_output_delay -max {self.args['odelay-ns']} -clock clock "+
                          f"[get_ports * -filter {{DIRECTION == OUT}}]", file=ft)
            print(f"create_fileset -constrset constraints_1 {v}", file=fo)
            print(f"add_files -fileset constraints_1 {xdc_file} {v}", file=fo)
            print(f"# FIRST PASS -- auto_detect_xpm", file=fo)
            print(f"synth_design -rtl -rtl_skip_ip -rtl_skip_constraints -no_timing_driven -no_iobuf "+
                  f"-top {self.args['top']} {incdirs} {defines} {v}", file=fo)
            print(f"auto_detect_xpm {v}", file=fo)
            print(f"synth_design -no_iobuf -part {self.args['part']} {flatten} -constrset constraints_1 "+
                  f"-top {self.args['top']} {incdirs} {defines} {v}", file=fo)
            print(f"write_verilog -force {self.args['top']}.vg {v}", file=fo)
            print(f"report_utilization -file {self.args['top']}.flat.util.rpt {v}", file=fo)
            print(f"report_utilization -file {self.args['top']}.hier.util.rpt {v} -hierarchical -hierarchical_depth 20", file=fo)
            print(f"report_timing -file {self.args['top']}.timing.rpt {v}", file=fo)
            print(f"report_timing_summary -file {self.args['top']}.summary.timing.rpt {v}", file=fo)
            print(f"report_timing -from [all_inputs] -file {self.args['top']}.input.timing.rpt {v}", file=fo)
            print(f"report_timing -to [all_outputs] -file {self.args['top']}.output.timing.rpt {v}", file=fo)
            print(f"report_timing -from [all_inputs] -to [all_outputs] -file {self.args['top']}.through.timing.rpt {v}", file=fo)
            print(f"set si [get_property -quiet SLACK [get_timing_paths -max_paths 1 -nworst 1 -setup -from [all_inputs]]]", file=fo)
            print(f"set so [get_property -quiet SLACK [get_timing_paths -max_paths 1 -nworst 1 -setup -to [all_outputs]]]", file=fo)
            print(f"set_false_path -from [all_inputs] {v}", file=fo)
            print(f"set_false_path -to [all_outputs] {v}", file=fo)
            print(f"set sf [get_property -quiet SLACK [get_timing_paths -max_paths 1 -nworst 1 -setup]]", file=fo)
            print(f"if {{ ! [string is double -strict $sf] }} {{ set sf 9999 }}", file=fo)
            print(f"if {{ ! [string is double -strict $si] }} {{ set si 9999 }}", file=fo)
            print(f"if {{ ! [string is double -strict $so] }} {{ set so 9999 }}", file=fo)
            print(f"puts \"\"", file=fo)
            print(f"puts \"*** ****************** ***\"", file=fo)
            print(f"puts \"***                    ***\"", file=fo)
            print(f"puts \"*** SYNTHESIS COMPLETE ***\"", file=fo)
            print(f"puts \"***                    ***\"", file=fo)
            print(f"puts \"*** ****************** ***\"", file=fo)
            print(f"puts \"\"", file=fo)
            print(f"puts \"** AREA **\"", file=fo)
            print(f"report_utilization -hierarchical", file=fo)
            print(f"puts \"** TIMING **\"", file=fo)
            print(f"puts \"\"", file=fo)
            if default_xdc:
                print(f"puts \"(Used default XDC: {xdc_file})\"", file=fo)
                print(f"puts \"DEF CLOCK NS  : [format %.3f {self.args['clock-ns']}]\"", file=fo)
                print(f"puts \"DEF IDELAY NS : [format %.3f {self.args['idelay-ns']}]\"", file=fo)
                print(f"puts \"DEF ODELAY NS : [format %.3f {self.args['odelay-ns']}]\"", file=fo)
            else:
                print(f"puts \"(Used provided XDC: {xdc_file})\"", file=fo)
            print(f"puts \"\"", file=fo)
            print(f"puts \"F2F SLACK     : [format %.3f $sf]\"", file=fo)
            print(f"puts \"INPUT SLACK   : [format %.3f $si]\"", file=fo)
            print(f"puts \"OUTPUT SLACK  : [format %.3f $so]\"", file=fo)
            print(f"puts \"\"", file=fo)

        # execute Vivado
        command_list = [ 'vivado', '-mode', 'batch', '-source', tcl_file, '-log', f"{self.args['top']}.synth.log" ]
        if not util.args['verbose']: command_list.append('-notrace')
        self.exec(self.args['work-dir'], command_list)

class CommandProjVivado(CommandProj, ToolVivado):
    def __init__(self, config:dict):
        CommandProj.__init__(self, config)
        ToolVivado.__init__(self)
        # add args specific to this simulator
        self.args['gui'] = True
        self.args['oc-vivado-tcl'] = True
        self.args['tcl-file'] = "proj.tcl"
        self.args['xdc'] = ""
        self.args['board'] = ""

    def do_it(self):
        # add defines for this job
        self.set_tool_defines()

        # create TCL
        tcl_file = os.path.abspath(os.path.join(self.args['work-dir'], self.args['tcl-file']))
        v = ""
        if util.args['verbose']: v += " -verbose"
        elif util.args['quiet']: v += " -quiet"

        with open( tcl_file, 'w' ) as fo:

            print(f"create_project {self.args['top']}_proj {self.args['work-dir']} {v}", file=fo)

            oc_root = util.get_oc_root()
            if self.args['oc-vivado-tcl'] and oc_root:
                print(f"source \"{oc_root}/boards/vendors/xilinx/oc_vivado.tcl\" -notrace", file=fo)
            if self.args['board'] != "":
                print(f"set_property board_part {self.args['board']} [current_project]", file=fo)

            incdirs = " ".join(self.incdirs)
            defines = ""
            for key in self.defines.keys():
                value = self.defines[key]
                defines += (f"{key} " if value == None else f"{key}={value} ")

            print(f"set_property include_dirs {{{incdirs}}} [get_filesets sources_1]", file=fo)
            print(f"set_property include_dirs {{{incdirs}}} [get_filesets sim_1]", file=fo)
            print(f"set_property verilog_define {{{defines}}} [get_filesets sources_1]", file=fo)
            print(f"set_property verilog_define {{SIMULATION {defines}}} [get_filesets sim_1]", file=fo)

            print(f"set_property -name {{STEPS.SYNTH_DESIGN.ARGS.MORE OPTIONS}} -value {{-verilog_define SYNTHESIS}} "+
                  f"-objects [get_runs synth_1]", file=fo)
            print(f"set_property {{xsim.simulate.runtime}} {{10ms}} [get_filesets sim_1]", file=fo)
            print(f"set_property {{xsim.simulate.log_all_signals}} {{true}} [get_filesets sim_1]", file=fo)

            for f in self.files_v + self.files_sv + self.files_vhd:
                if f.find("/sim/") >= 0: fileset = "sim_1"
                elif f.find("/tests/") >= 0: fileset = "sim_1"
                else: fileset = "sources_1"
                print(f"add_files -norecurse {f} -fileset [get_filesets {fileset}]", file=fo)

        # execute Vivado
        command_list = [ 'vivado', '-mode', 'gui', '-source', tcl_file, '-log', f"{self.args['top']}.proj.log" ]
        if not util.args['verbose']: command_list.append('-notrace')
        self.exec(self.args['work-dir'], command_list)
        util.info(f"Synthesis done, results are in: {self.args['work-dir']}")

class CommandBuildVivado(CommandBuild, ToolVivado):
    def __init__(self, config:dict):
        CommandBuild.__init__(self, config)
        ToolVivado.__init__(self)
        # add args specific to this simulator
        self.args['gui'] = False
        self.args['fpga'] = ""
        self.args['proj'] = False
        self.args['reset'] = False

    def do_it(self):
        # add defines for this job
        self.set_tool_defines()

        # create FLIST
        flist_file = os.path.join(self.args['work-dir'],'build.flist')
        util.debug(f"CommandBuildVivado: {self.args['top-path']=}")

        # TODO(drew): this might break depending on how 'eda' or 'eda.py' is called, for example
        # if this was pip installed as eda-cogni, then the command list here needs to reflect that.
        eda_path = get_eda_exec('flist')
        command_list = [
            eda_path, 'flist',
            '--tool', self.args['tool'],
            self.args['top-path'],
            '--force',
            '--xilinx',
            '--out', flist_file,
            '--no-emit-incdir',
            '--no-quote-define',
            '--prefix-define', '"oc_set_project_define "',
            '--prefix-sv', '"add_files -norecurse "',
            '--prefix-v', '"add_files -norecurse "',
            '--prefix-vhd', '"add_files -norecurse "'
        ]
        for key,value in self.defines.items():
            if value == None:   command_list += [ f"+define+{key}" ]
            elif "\'" in value: command_list += [ f"\"+define+{key}={value}\"" ]
            else:               command_list += [ f"\'+define+{key}={value}\'" ]
        cwd = util.getcwd()
        self.exec(cwd, command_list)

        if self.args['job-name'] == "":
            self.args['job-name'] = self.args['design']
        project_dir = 'project.'+self.args['job-name']

        # launch Vivado
        command_list = ['vivado']
        command_list += ['-mode', 'gui' if self.args['gui'] else 'batch' ]
        command_list += ['-log', os.path.join(self.args['work-dir'], self.args['top']+'.build.log') ]
        if not util.args['verbose']: command_list.append('-notrace')
        command_list += ['-source', self.args['build-script'] ]
        command_list += ['-tclargs', project_dir, flist_file] # these must come last, all after -tclargs get passed to build-script
        if self.args['proj']: command_list += ['--proj']
        if self.args['reset']: command_list += ['--reset']
        self.exec(cwd, command_list)

        util.info(f"Build done, results are in: {self.args['work-dir']}")

class CommandFListVivado(CommandFList, ToolVivado):
    def __init__(self, config:dict):
        CommandFList.__init__(self, config)
        ToolVivado.__init__(self)

class CommandUploadVivado(CommandUpload, ToolVivado):
    def __init__(self, config:dict):
        CommandUpload.__init__(self, config)
        ToolVivado.__init__(self)
        # add args specific to this simulator
        self.args['gui'] = False
        self.args['file'] = False
        self.args['usb'] = True
        self.args['host'] = "localhost"
        self.args['port'] = 3121
        self.args['target'] = 0
        self.args['tcl-file'] = "upload.tcl"

    def do_it(self):
        if self.args['file'] == False:
            util.info(f"Searching for bitfiles...")
            found_file = False
            all_files = []
            for root, dirs, files in os.walk("."):
                for file in files:
                    if file.endswith(".bit"):
                        found_file = os.path.abspath(os.path.join(root,file))
                        util.info(f"Found bitfile: {found_file}")
                        all_files.append(found_file)
            self.args['file'] = found_file
        if len(all_files) > 1:
            all_files.sort(key=lambda f: os.path.getmtime(f))
            self.args['file'] = all_files[-1]
            util.info(f"Choosing: {self.args['file']} (newest)")
        if self.args['file'] == False:
            self.error(f"Couldn't find a bitfile to upload")
        if self.args['usb']:
            util.info(f"Uploading bitfile: {self.args['file']}")
            util.info(f"Uploading via {self.args['host']}:{self.args['port']} USB target #{self.args['target']}")
            self.upload_usb_jtag(self.args['host'], self.args['port'], self.args['target'], self.args['file'])
        else:
            self.error(f"Only know how to upload via USB for now")

    def upload_usb_jtag(self, host, port, target, bit_file):
        # create TCL
        tcl_file = os.path.abspath(os.path.join(self.args['work-dir'], self.args['tcl-file']))
        ltx_file = os.path.splitext(bit_file)[0] + ".ltx"
        if not os.path.exists(ltx_file):
            ltx_file = False

        with open( tcl_file, 'w' ) as fo:
            print(f"open_hw", file=fo)
            print(f"connect_hw_server -url {host}:{port}", file=fo)
            print(f"refresh_hw_server -force_poll", file=fo)
            print(f"set hw_targets [get_hw_targets */xilinx_tcf/Xilinx/*]", file=fo)
            print(f"if {{ [llength $hw_targets] <= {target} }} {{", file=fo)
            print(f"  puts \"ERROR: There is no target number {target}\"", file=fo)
            print(f"}}", file=fo)
            print(f"current_hw_target [lindex $hw_targets {target}]", file=fo)
            print(f"open_hw_target", file=fo)
            print(f"refresh_hw_target", file=fo)
            print(f"current_hw_device [lindex [get_hw_devices] 0]", file=fo)
            print(f"refresh_hw_device [current_hw_device]", file=fo)
            print(f"set_property PROGRAM.FILE {bit_file} [current_hw_device]", file=fo)
            if ltx_file:
                print(f"set_property PROBES.FILE {ltx_file} [current_hw_device]", file=fo)
            print(f"program_hw_devices [current_hw_device]", file=fo)
            if self.args['gui']:
                print(f"refresh_hw_device [current_hw_device]", file=fo)
                print(f"display_hw_ila_data [ get_hw_ila_data hw_ila_data_1 -of_objects [get_hw_ilas] ]", file=fo)
            else:
                print(f"close_hw_target", file=fo)
                print(f"exit", file=fo)

        # execute Vivado
        command_list = [ 'vivado', '-source', tcl_file, '-log', f"fpga.upload.log" ]
        if not self.args['gui']:
            command_list.append('-mode')
            command_list.append('batch')
        self.exec(self.args['work-dir'], command_list)

class CommandOpenVivado(CommandOpen, ToolVivado):
    def __init__(self, config:dict):
        CommandOpen.__init__(self, config)
        ToolVivado.__init__(self)
        # add args specific to this simulator
        self.args['gui'] = True
        self.args['file'] = False

    def do_it(self):
        if self.args['file'] == False:
            util.info(f"Searching for project...")
            found_file = False
            all_files = []
            for root, dirs, files in os.walk("."):
                for file in files:
                    if file.endswith(".xpr"):
                        found_file = os.path.abspath(os.path.join(root,file))
                        util.info(f"Found project: {found_file}")
                        all_files.append(found_file)
            self.args['file'] = found_file
        if len(all_files) > 1:
            all_files.sort(key=lambda f: os.path.getmtime(f))
            self.args['file'] = all_files[-1]
            util.info(f"Choosing: {self.args['file']} (newest)")
        if self.args['file'] == False:
            self.error(f"Couldn't find an XPR Vivado project to open")
        projname = os.path.splitext(os.path.basename(self.args['file']))[0]
        projdir = os.path.dirname(self.args['file'])
        oc_root = util.get_oc_root()
        oc_vivado_tcl = os.path.join(oc_root, 'boards', 'vendors', 'xilinx', 'oc_vivado.tcl')
        command_list = [ 'vivado', '-source', oc_vivado_tcl, '-log', f"{projname}.open.log", self.args['file'] ]
        self.exec(projdir, command_list)


class ToolQuesta(Tool):
    def __init__(self):
        Tool.__init__(self)
        self.questa_major = None
        self.questa_minor = None
        self.starter_edition = False # Aka, modelsim_ase
        self.args['xilinx'] = False
        self.args['part'] = 'xcu200-fsgd2104-2-e'
        self.args['tool'] = 'questa'

    def get_versions(self):
        if self.questa_major != None:
            return
        qrun_path = shutil.which('qrun')
        if qrun_path == None:
            self.error(f"qrun not in path, need to setup (i.e. source /opt/intelFPGA_pro/23.4/settings64.sh")
        util.debug(f"qrun_path = %s" % qrun_path)
        m = re.search(r'(\d+)\.(\d+)', qrun_path)
        if m:
            self.questa_major = int(m.group(1))
            self.questa_minor = int(m.group(2))
            return
        self.error(f"Questa path doesn't specificy version, expecting (d+.d+)")
        if 'modelsim_ase' in qrun_path:
            util.warning("Questa path is for starter edition (modelsim_ase), consider using --tool modelsim_ase")
            self.starter_edition = True

    def set_tool_defines(self):
        # Will only be called from an object which also inherits from CommandDesign, i.e. has self.defines
        self.get_versions()
        self.defines['OC_TOOL_QUESTA'] = None
        self.defines['OC_TOOL_QUESTA_%d_%d' % (self.questa_major, self.questa_minor)] = None
        if self.args['xilinx']:
            self.defines['OC_LIBRARY_ULTRASCALE_PLUS'] = None
            self.defines['OC_LIBRARY'] = "1"
        else:
            self.defines['OC_LIBRARY_BEHAVIORAL'] = None
            self.defines['OC_LIBRARY'] = "0"

class CommandSimQuesta(CommandSim, ToolQuesta):
    def __init__(self, config:dict):
        CommandSim.__init__(self, config)
        ToolQuesta.__init__(self)
        # add args specific to this simulator
        self.args['gui'] = False
        self.args['tcl-file'] = "sim.tcl"
        self.shell_command = 'qrun'

    def set_tool_defines(self):
        ToolQuesta.set_tool_defines(self)

    def do_it(self):
        # add defines for this job
        self.set_tool_defines()

        # it all gets done with one command
        command_list = [ self.shell_command, "-64", "-sv" ]

        # incdirs
        for value in self.incdirs:
            command_list += [ f"+incdir+{value}" ]

        # defines
        for key in self.defines.keys():
            value = self.defines[key]
            if value == None:
                command_list += [ f"+define+{key}" ]
            elif type(value) is str and "\'" in value:
                command_list += [ f"\"+define+{key}={value}\"" ]
            else:
                command_list += [ f"\'+define+{key}={value}\'" ]

        # compile verilog
        for f in self.files_v:
            command_list += [ f ]

        # compile systemverilog
        for f in self.files_sv:
            command_list += [ f ]

        if self.args['xilinx']:
            if 'XILINX_VIVADO' not in os.environ:
                self.error("Vivado is not setup, no XILINX_VIVADO in env")
            command_list += [ os.path.join( os.environ['XILINX_VIVADO'], 'data/verilog/src/glbl.v') ]

        # misc options
        command_list += [ '-top', self.args['top'], '-timescale', '1ns/1ps', '-work', 'work.lib']
        command_list += [
            # otherwise lots of warnings about defaulting to "var" which isn't LRM behavior, and we don't need it
            '-svinputport=net',
            #  Existing package 'xxxx_pkg' at line 9 will be overwritten.
            '-suppress', 'vlog-2275',
            #  Extra checking for conflict in always_comb and always_latch variables is done at vopt time
            '-suppress', 'vlog-2583',
            #  Missing connection for port 'xxxx' (The default port value will be used)
            '-suppress', 'vopt-13159',
            #  Too few port connections for 'uAW_FIFO'.  Expected 10, found 8
            '-suppress', 'vopt-2685',
            #  Missing connection for port 'almostEmpty' ... unfortunately same message for inputs and outputs... :(
            '-note', 'vopt-2718',
        ]
        if self.args['gui']: command_list += ['-gui=interactive', '+acc', '-i']
        elif self.args['waves']: command_list += ['+acc', '-c']
        else: command_list += ['-c']
        if util.args['verbose']: command_list += ['-verbose']
        if self.args['xilinx']:
            # this will need some work
            self.error("THIS ISN'T GOING TO WORK, got --xilinx with Questa which isn't ready yet", do_exit=False)
            # command_list += "-L xil_defaultlib -L unisims_ver -L unimacro_ver -L xpm -L secureip -L xilinx_vip".split(" ")

        # check if we're bailing out early
        if self.args['stop-after-elaborate']:
            command_list += ['-elab', 'elab.output', '-do', '"quit"' ]

        # create TCL
        tcl_name = os.path.abspath(os.path.join(self.args['work-dir'], self.args['tcl-file']))
        with open( tcl_name, 'w' ) as fo:
            if self.args['waves']:
                if self.args['waves-start']:
                    print("run %d ns" % self.args['waves-start'], file=fo)
                print("add wave -r /*", file=fo)
            print("run -all", file=fo)
            if not self.args['gui']:
                print("quit", file=fo)
        command_list += ['-do', tcl_name ]

        # execute snapshot
        self.exec(self.args['work-dir'], command_list)


class CommandElabQuesta(CommandSimQuesta):
    def __init__(self, config:dict):
        CommandSimQuesta.__init__(self, config)
        # add args specific to this simulator
        self.args['stop-after-elaborate'] = True


class CommandSimModelsimAse(CommandSim, ToolQuesta):
    def __init__(self, config:dict):
        CommandSim.__init__(self, config)
        ToolQuesta.__init__(self)
        self.shell_command = 'vsim'
        self.starter_edition = True
        self.args['tool'] = 'modelsim_ase' # otherwise it's 'questa' from base class.
        self.args['gui'] = False
        self.log_bad_strings =  ['ERROR: ', 'FATAL: ']
        self.log_must_strings = [' vsim ', 'Errors: 0']

    def set_tool_defines(self):
        self.get_versions()
        add_defines = [
            'OC_ASSERT_PROPERTY_NOT_SUPPORTED',
            'OC_TOOL_MODELSIM_ASE'
        ]
        for a in add_defines:
            self.defines[a] = 1

    # We do override do_it() to avoid using CommandSimQuesta.do_it()
    def do_it(self):
        CommandSim.do_it(self)
        #    self.compile()   # runs if stop-before-compile is False, stop-after-compile is True
        #    self.elaborate() # runs if stop-before-compile is False, stop-after-compile is False, stop-after-elaborate is True
        #    self.simulate()  # runs if stop-* are all False (run the whole thing)


    def prepare_compile(self):
        self.set_tool_defines()
        self.write_vlog_dot_f()
        self.write_vsim_dot_do(dot_do_to_write='all')
        if self.args['xilinx']:
            self.error('Error: --xilinx with Modelsim ASE is not yet supported', do_exit=False)

        vsim_command_lists = self.get_compile_command_lists()
        util.write_shell_command_file(dirpath=self.args['work-dir'], filename='compile_only.sh',
                                      command_lists=vsim_command_lists)

        vsim_command_lists = self.get_elaborate_command_lists()
        util.write_shell_command_file(dirpath=self.args['work-dir'], filename='compile_elaborate_only.sh',
                                      command_lists=vsim_command_lists)

        vsim_command_lists = self.get_simulate_command_lists()
        util.write_shell_command_file(dirpath=self.args['work-dir'], filename='all.sh',
                                      command_lists = \
                                      [['./pre_compile_dep_shell_commands.sh']] + vsim_command_lists)

        util.write_eda_config_and_args(dirpath=self.args['work-dir'], command_obj_ref=self)

    def compile(self):
        if self.args['stop-before-compile']:
            # don't run anything, save everyting we've already run in _prep_compile()
            return
        if self.args['stop-after-compile']:
            vsim_command_lists = self.get_compile_command_lists()
            self.run_commands_check_logs(vsim_command_lists, log_filename='sim.log')

    def elaborate(self):
        if self.args['stop-before-compile']:
            return
        if self.args['stop-after-compile']:
            return
        if self.args['stop-after-elaborate']:
        # only run this if we stop after elaborate (simulate run it all)
            vsim_command_lists = self.get_elaborate_command_lists()
            self.run_commands_check_logs(vsim_command_lists, log_filename='sim.log')

    def simulate(self):
        if self.args['stop-before-compile'] or self.args['stop-after-compile'] or \
           self.args['stop-after-elaborate']:
            # don't run this if we're stopping before/after compile/elab
            return
        vsim_command_lists = self.get_simulate_command_lists()
        self.run_commands_check_logs(vsim_command_lists, log_filename='sim.log')

    def get_compile_command_lists(self):
        # This will also set up a compile.
        vsim_command_list = [
            'vsim',
            '' if self.args['gui'] else '-c',
            '-do', 'vsim_vlogonly.do', '-logfile', 'sim.log',
        ]
        return [vsim_command_list]

    def get_elaborate_command_lists(self):
        # This will also set up a compile, for vlog + vsim (0 time)
        vsim_command_list = [
            'vsim',
            '' if self.args['gui'] else '-c',
            '-do', 'vsim_lintonly.do', '-logfile', 'sim.log',
        ]
        return [vsim_command_list]

    def get_simulate_command_lists(self):
    # This will also set up a compile, for vlog + vsim (with run -a)
        vsim_command_list = [
            'vsim',
            '' if self.args['gui'] else '-c',
            '-do', 'vsim.do', '-logfile', 'sim.log',
        ]
        return [vsim_command_list]


    def write_vlog_dot_f(self, filename='vlog.f'):
        vlog_dot_f_lines = [
            '-sv',
            '-svinputport=net',
            '-lint',
            # vlog suppress warnings:
            # 2275 -  Existing package 'foo_pkg' will be overwritten.
            '-suppress', '2275',
            # 2555 - assignment to input port foo
            '-suppress', '2555',
            # 2583 - [SVCHK] - Extra checking for conflicts with always_comb and always_latch variables is done at vopt time.
            '-suppress', '2583',
            ]

        vlog_dot_f_fname = filename
        vlog_dot_f_fpath = os.path.join(self.args['work-dir'], vlog_dot_f_fname)

        for value in self.incdirs:
            vlog_dot_f_lines += [ f"+incdir+{value}" ]

        for k,v in self.defines.items():
            if v is None:
                vlog_dot_f_lines += [ f'+define+{k}' ]
            else:
                # Generally we should only support int and str python types passed as
                # +define+{k}={v}, but also for SystemVerilog plusargs
                vlog_dot_f_lines += [ f'+define+{k}={sanitize_defines_for_sh(v)}' ]


        vlog_dot_f_lines += self.args['compile-args']

        vlog_dot_f_lines += [
            '-source',
            ] + list(self.files_sv) + list(self.files_v)

        assert len(self.files_sv) + len(self.files_v) > 0, \
            f'{self.target=} {self.files_sv=} and {self.files_v=} are empty, cannot create a valid vlog.f'

        with open(vlog_dot_f_fpath, 'w') as f:
            f.writelines(line + "\n" for line in vlog_dot_f_lines)

    def write_vsim_dot_do(self, dot_do_to_write : list()):
        '''Writes files(s) based on dot_do_to_write(list, values [] or with items 'all', 'sim', 'lint', 'vlog'.'''

        vsim_dot_do_fname = 'vsim.do'
        vsim_dot_do_fpath = os.path.join(self.args['work-dir'], vsim_dot_do_fname)

        vsim_lintonly_dot_do_fname = 'vsim_lintonly.do'
        vsim_lintonly_dot_do_fpath = os.path.join(self.args['work-dir'], vsim_lintonly_dot_do_fname)

        vsim_vlogonly_dot_do_fname = 'vsim_vlogonly.do'
        vsim_vlogonly_dot_do_fpath = os.path.join(self.args['work-dir'], vsim_vlogonly_dot_do_fname)

        sv_seed = self.args['seed']

        sim_plusargs = list()
        for x in self.args['sim-plusargs']:
            # For vsim we need to add a +key=value if the + is missing
            if x[0] != '+':
                x = f'+{x}'
            sim_plusargs.append(x)

        sim_plusargs_str = ' '.join(sim_plusargs)

        assert type(self.args["sim-plusargs"]) is list, \
            f'{self.target=} {type(self.args["sim-plusargs"])=} but must be list'

        vsim_suppress_list = [
            # 3009: [TSCALE] - Module 'foo' does not have a timeunit/timeprecision specification in effect, but other modules do.
            '-suppress', '3009',
        ]
        vsim_suppress_list_str = ' '.join(vsim_suppress_list)

        voptargs_str = ""
        if self.args['gui'] or self.args['waves']:
            voptargs_str = "+acc"

        # TODO(drew): support self.args['sim_libary', 'elab-args', sim-args'] (3 lists) to add to vsim_one_liner.

        vsim_one_liner = "vsim -onfinish stop " \
            + f"-sv_seed {sv_seed} {sim_plusargs_str} {vsim_suppress_list_str} {voptargs_str} work.{self.args['top']}"

        vsim_vlogonly_dot_do_lines = [
            "if {[file exists work]} { vdel -all work; }",
            "vlib work;",
            "if {[catch {vlog -f vlog.f} result]} {",
            "    echo \"Caught $result \";",
            "    if {[batch_mode]} {",
            "        quit -f -code 20;",
            "    }",
            "}",
            "if {[batch_mode]} {",
            "    quit -f -code 0;",
            "}",
        ]

        vsim_lintonly_dot_do_lines = [
            "if {[file exists work]} { vdel -all work; }",
            "vlib work;",
            "quietly set qc 30;",
            "if {[catch {vlog -f vlog.f} result]} {",
            "    echo \"Caught $result \";",
            "    if {[batch_mode]} {",
            "        quit -f -code 20;",
            "    }",
            "}",
            "if {[catch { " + vsim_one_liner + " } result] } {",
            "    echo \"Caught $result\";",
            "    if {[batch_mode]} {",
            "        quit -f -code 19;",
            "    }",
            "}",
            "set TestStatus [coverage attribute -name SEED -name TESTSTATUS];",
            "if {[regexp \"TESTSTATUS += 0\" $TestStatus]} {",
            "    quietly set qc 0;",
            "} elseif {[regexp \"TESTSTATUS += 1\" $TestStatus]} {",
            "    quietly set qc 0;",
            "} else {",
            "    quietly set qc 2;",
            "}",
            "if {[batch_mode]} {",
            "    quit -f -code $qc;",
            "}",
        ]

        vsim_dot_do_lines = [
            "if {[file exists work]} { vdel -all work; }",
            "vlib work;",
            "quietly set qc 30;",
            "if {[catch {vlog -f vlog.f} result]} {",
            "    echo \"Caught $result \";",
            "    if {[batch_mode]} {",
            "        quit -f -code 20;",
            "    }",
            "}",
            "if {[catch { " + vsim_one_liner + " } result] } {",
            "    echo \"Caught $result\";",
            "    if {[batch_mode]} {",
            "        quit -f -code 19;",
            "    }",
            "}",
            "onbreak { resume; };",
            "log -r *; run -a;",
            "set TestStatus [coverage attribute -name SEED -name TESTSTATUS];",
            "if {[regexp \"TESTSTATUS += 0\" $TestStatus]} {",
            "    quietly set qc 0;",
            "} elseif {[regexp \"TESTSTATUS += 1\" $TestStatus]} {",
            "    quietly set qc 0;",
            "} else {",
            "    quietly set qc 2;",
            "}",
            "if {[batch_mode]} {",
            "    quit -f -code $qc;",
            "}",
        ]

        write_all = len(dot_do_to_write) == 0 or 'all' in dot_do_to_write
        if write_all or 'sim' in dot_do_to_write:
            with open(vsim_dot_do_fpath, 'w') as f:
                f.writelines(line + "\n" for line in vsim_dot_do_lines)

        if write_all or 'lint' in dot_do_to_write:
            with open(vsim_lintonly_dot_do_fpath, 'w') as f:
                f.writelines(line + "\n" for line in vsim_lintonly_dot_do_lines)

        if write_all or 'vlog' in dot_do_to_write:
            with open(vsim_vlogonly_dot_do_fpath, 'w') as f:
                f.writelines(line + "\n" for line in vsim_vlogonly_dot_do_lines)



class CommandElabModelsimAse(CommandSimModelsimAse):
    def __init__(self, config:dict):
        super().__init__(config)
        self.args['stop-after-elaborate'] = True


class ToolIverilog(Tool):
    def __init__(self):
        Tool.__init__(self)
        self.args['tool'] = 'iverilog'

    def get_versions(self):
        iverilog_path = shutil.which('iverilog')
        if iverilog_path is None:
            self.error('"iverilog" not in path, need to get it (https://iverilog.fandom.com/wiki/Installation_Guide)')

        iverilog_version_ret = subprocess.run(['iverilog', '-v'], capture_output=True)
        lines = iverilog_version_rets.tdout.decode("utf-8").split('\n')
        words = lines[0].split() # 'Icarus Verilog version 13.0 (devel) (s20221226-568-g62727e8b2)'
        version = words[3]
        util.debug(f'{iverilog_path=} {lines[0]=}')
        l = version.split('.')
        self.verilator_major = l[0]
        self.verilator_minor = l[1]
        return

    def set_tool_defines(self):
        self.defines.update({
            'SIMULATION': 1,
            'OC_TOOL_IVERILOG': 1,
            'OC_ASSERT_PROPERTY_NOT_SUPPORTED': 1,
        })


class CommandSimIverilog(CommandSim, ToolIverilog):
    def __init__(self, config:dict):
        CommandSim.__init__(self, config)
        ToolVerilator.__init__(self)
        self.args['gui'] = False
        self.args['tcl-file'] = None
        self.log_bad_strings = ['error: ', ': syntax error', 'I give up']

    def set_tool_defines(self):
        ToolIverilog.set_tool_defines(self)

    # We do not override CommandSim.do_it()
    def prepare_compile(self):
        self.set_tool_defines()
        if self.args['xilinx']:
            self.error('Error: --xilinx with Iverilog is not yet supported', do_exit=False)

        self.iverilog_command_lists = self.get_compile_command_lists()
        self.iverilog_exec_command_lists  = self.get_simulate_command_lists()

        paths = ['logs']
        util.safe_mkdirs(base=self.args['work-dir'], new_dirs=paths)

        util.write_shell_command_file(dirpath=self.args['work-dir'], filename='compile_only.sh',
                                      command_lists=self.iverilog_command_lists, line_breaks=True)

        util.write_shell_command_file(dirpath=self.args['work-dir'], filename='simulate_only.sh',
                                      command_lists = self.iverilog_exec_command_lists)


        util.write_shell_command_file(dirpath=self.args['work-dir'], filename='all.sh',
                                      command_lists = [
                                          ['./pre_compile_dep_shell_commands.sh'],
                                          ['./compile_only.sh'],
                                          ['./simulate_only.sh'],
                                      ])

        util.write_eda_config_and_args(dirpath=self.args['work-dir'], command_obj_ref=self)

    def compile(self):
        if self.args['stop-before-compile']:
            return
        self.run_commands_check_logs(self.iverilog_command_lists, check_logs=False)

    def elaborate(self):
        pass

    def simulate(self):
        if self.args['stop-before-compile'] or self.args['stop-after-compile'] or \
           self.args['stop-after-elaborate']:
            # don't run this if we're stopping before/after compile/elab
            return

        # Note that this is not returning a pass/fail bash return code,
        # so we will likely have to log-scrape to deterimine pass/fail.
        self.run_commands_check_logs(self.iverilog_exec_command_lists, log_filename='sim.log')

    def get_compile_command_lists(self):

        command_list = [
            'iverilog',
            '-g2012',
            '-gsupported-assertions',
            '-grelative-include',
            '-s', self.args['top'],
            '-o', 'sim.exe',
        ]

        if util.args['verbose']:
            command_list += ['-v']

        # incdirs
        for value in self.incdirs:
            command_list += [ '-I', value ]

        for k,v in self.defines.items():
            if v is None:
                command_list += [ '-D', k ]
            else:
                # Generally we should only support int and str python types passed as
                # +define+{k}={v}, but also for SystemVerilog plusargs
                command_list += [ '-D', f'{k}={sanitize_defines_for_sh(v)}' ]

        assert len(self.files_sv) + len(self.files_v) > 0, \
            f'{self.target=} {self.files_sv=} and {self.files_v=} are empty, cannot call iverilog'

        command_list += list(self.files_sv) + list(self.files_v)

        return [command_list]

    def get_simulate_command_lists(self):
        ret = [
            './sim.exe',
        ] + [
            '|', 'tee sim.log',
        ]

        # Need to return a list-of-lists, even though we only have 1 command
        return [ret]


class CommandElabIverilog(CommandSimIverilog):
    pass






# ****************************************************************************************************
# MAIN

# Set global 'config['command_handler'] entries for (command, Class) so we know which
# eda command (such as, command: eda sim) is handled by which class (such as class: CommandSim)
# These are also overriden depending on the tool, for example --tool verilator sets
# "sim": CommandSimVerilator.
config['command_handler'].update({
    "sim"    : CommandSim,
    "elab"   : CommandElab,
    "synth"  : CommandSynth,
    "flist"  : CommandFList,
    "proj"   : CommandProj,
    "multi"  : CommandMulti,
    "sweep"  : CommandSweep,
    "build"  : CommandBuild,
    "waves"  : CommandWaves,
    "upload" : CommandUpload,
    "open"   : CommandOpen,
})

def usage(tokens = []):
    if len(tokens) == 0:
        print(
"""
    Usage: eda <command> <options> <targets>

    Where <command> is one of:

    sim          - Simulates a DEPS target
    elab         - Elaborates a DEPS target (sort of sim based LINT)
    synth        - Synthesizes a DEPS target
    flist        - Create dependency from a DEPS target
    proj         - Create a project from a DEPS target for GUI sim/waves/debug
    multi        - Run multiple DEPS targets, serially or in parallel
    sweep        - Sweep one or more arguments across a range, serially or in parallel
    build        - Build for a board, creating a project and running build flow
    waves        - Opens waveform from prior simulation
    upload       - Uploads a finished design into hardware
    open         - Opens a project
    help         - This help (without args), or i.e. "eda help sim" for specific help
"""
        )
    elif tokens[0] in config['command_handler'].keys():
        sco = config['command_handler'][tokens[0]](config) # sub command object
        sco.help()
        return util.exit(0)
    else:
        util.info(f"Valid commands are: ")
        for k in sorted(config['command_handler'].keys()):
            util.info(f"   {k:20}")
        return util.error(f"Cannot provide help, don't understand command: '{tokens[0]}'")

def interactive():
    read_file = False
    while True:
        if read_file:
            line = f.readline()
            if line:
                print("%s->%s" % (fname, line), end="")
            else:
                read_file = False
                f.close()
                continue
        else:
            line = input('EDA->')
        m = re.match(r'^([^\#]*)\#.*$', line)
        if m: line = m.group(1)
        tokens = line.split()
        process_tokens(tokens)


def get_eda_exec(command:str=''):
    # NOTE(drew): This is kind of flaky. 'eda multi' reinvokes 'eda'. But the executable for 'eda'
    # is one of:
    # 1. pip3 install opencos-eda
    #    -- script 'eda', installed from PyPi
    # 2. pip3 uninstall .; python3 -m build; pip3 install
    #    -- script 'eda' but installed from local.
    # 2. (opencos repo)/bin/eda - a python wrapper to link to (opencos repo)/opencos/eda.py (package)
    #    packages cannot be run standalone, they need to be called as: python3 -m opencos.eda,
    #    and do not work with relative paths. This only works if env OC_ROOT is set or can be found.
    # 3. If you ran 'source bin/addpath' then you are always using the local (opencos repo)/bin/eda
    eda_path = shutil.which('eda')
    if not eda_path:
        # Can we run from OC_ROOT/bin/eda?
        oc_root = util.get_oc_root()
        if not oc_root:
            util.error(f"Need 'eda' in our path to run 'eda {command}', could not find env OC_ROOT, {eda_path=}, {oc_root=}")
        else:
            bin_eda = os.path.join(oc_root, 'bin', 'eda')
            if not os.path.exists(bin_eda):
                util.error(f"Need 'eda' in our path to run 'eda {command}', cound not find bin/, {eda_path=}, {oc_root=}, {bin_eda=}")
            else:
                util.info(f"'eda' not in path, using {bin_eda=} for 'eda' {command} executable")
                eda_path = os.path.abspath(bin_eda)

    return eda_path



def auto_tool_setup():
    for name, value in glbl_auto_tools_ordered.items():
        exe = value.get('exe', str())
        assert exe != '', f'{tool=} {value=} value missing "exe" {exe=}'
        p = shutil.which(exe)
        if p:
            glbl_auto_tools_found[name] = exe # populate key-value pairs
            util.info(f"Detected {name} ({p}), auto-setting up tool {name}")
            tool_setup(tool=name, quiet=True, auto_setup=True)


def tool_setup(tool : str, quiet : bool = False, auto_setup : bool = False):

    if not quiet and not auto_setup:
        util.info(f"Setup for tool: '{tool}'")

    if not tool:
        return

    if tool not in glbl_auto_tools_ordered:
        util.error(f"Don't know how to run tool_setup({tool=}), is not in {glbl_auto_tools_ordered=}")
        return

    if tool not in glbl_auto_tools_found:
        util.error(f"Don't know how to run tool_setup({tool=}), is not in {glbl_auto_tools_found=}")
        return

    if auto_setup and tool is not None and tool in glbl_tools_loaded:
        # Do I realy need to warn if a tool was loaded from auto_tool_setup(),
        # but then I also called it via --tool verilator? Only warn if auto_setup=True:
        util.warning(f"tool_setup: {auto_setup=} already setup for {tool}?")

    entry = glbl_auto_tools_ordered.get(tool, dict())
    tool_cmd_handler_dict = entry.get('handlers', dict())

    for command, str_class_name in tool_cmd_handler_dict.items():
        current_handler_cls = config['command_handler'].get(command, None)
        if str_class_name not in globals():
            # TODO(drew): if we allow external handling classes, might need to re-think the
            # use of 'globals()' above (try - except NameError?)
            util.error(f"{tool=} {command=} {str_class_name=} class not in globals()")
        else:
            # The defaults handlers (aka, command='sim' current_handler_cls=CommandSim)
            # aren't associated with a tool, so they can be overridden.
            if auto_setup and current_handler_cls is not None and issubclass(current_handler_cls, Tool):
                pass # skip, already has a tool associated with it, and we're in auto_setup=True
            else:
                # If we're not in auto_setup, then always override.
                cls = eval(str_class_name)
                assert issubclass(cls, Tool), f'{str_class_name=} is does not have Tool class associated with it'
                config['command_handler'][command] = cls

    glbl_tools_loaded.add(tool)


def which_tool(command):
    # returns which tool will be used for a command, given the current command_handlers
    if not command in config['command_handler'].keys():
        util.error("which_tool called with invalid command?")
    cobj = config['command_handler'][command](config=config)
    return cobj.args.get('tool', None)

def process_tokens(tokens):
    # this is the top level token processing function.  tokens can come from command line, setup file, or interactively.
    # we do one pass through all the tokens, triaging them into:
    # - those we can execute immediate (help, quit, and global opens like --debug, --color)
    # - a command (sim, synth, etc)
    # - command arguments (--seed, +define, +incdir, etc) which will be deferred and processed by the command
    deferred_tokens = []
    original_args = tokens.copy()
    command = ""

    parser = argparse.ArgumentParser(prog='eda', add_help=False, allow_abbrev=False)
    parser.add_argument('-q', '--quit', action='store_true')
    parser.add_argument('--exit', action='store_true')
    parser.add_argument('-h', '--help', action='store_true')
    parser.add_argument('--tool')
    try:
        parsed, unparsed = parser.parse_known_args(tokens + [''])
        unparsed = list(filter(None, unparsed))
    except argparse.ArgumentError:
        return util.error(f'problem attempting to parse_known_args for {tokens=}')

    # We support a few way of handling quit, exit, or --quit, --exit, -q
    if parsed.quit or parsed.exit or 'exit' in unparsed or 'quit' in unparsed:
        return util.exit(0)
    if parsed.help or 'help' in unparsed:
        if 'help' in unparsed:
            unparsed.remove('help')
        return usage(unparsed)

    # see if eda's util needs to process this (printing related)
    util_parsed_dict, unparsed = util.process_tokens(unparsed)

    util.debug(f'eda process_tokens: {parsed=} {unparsed=}')
    for value in unparsed:
        if value in config['command_handler'].keys():
            command = value
            unparsed.remove(value)
            break

    if parsed.tool:
        tool_setup(parsed.tool)


    deferred_tokens = unparsed
    if command == "":
        util.error("Didn't get a command!")
        return 1

    sco = config['command_handler'][command](config) # sub command object
    if not parsed.tool:
        use_tool = which_tool(command)
        util.info(f"--tool not specified, using default for {command=}: {use_tool}")

    setattr(sco, 'original_args', original_args)
    rc = sco.process_tokens(deferred_tokens)
    util.debug(f'Return from main process_tokens({tokens=}), {rc=}, {type(sco)=}')
    return rc


def sanitize_defines_for_sh(value):
    # Need to sanitize this for shell in case someone sends a +define+foo+1'b0,
    # which needs to be escaped as +define+foo+1\'b0, otherwise bash or sh will
    # think this is an unterminated string.
    if type(value) is str:
        value = value.replace("'", "\\" + "'")
    return value

# **************************************************************
# **** Interrupt Handler

def signal_handler(sig, frame):
    util.fancy_stop()
    util.info('Received Ctrl+C...', start='\nINFO: [EDA] ')
    util.exit(-1)

# **************************************************************
# **** Startup Code


def main(*args):
    ''' Returns return code (int), entry point for calling eda.main(*list) directly in py code'''

    # TODO(drew): support for an external "config" dict() (or yml, json, etc) so that
    # users can BYO tool if not yet supported for a command, or modify the behavior of a
    # tool (aka, CommandSimVerilator with different verilator args - could be done with
    # a derived class and modifying eda.config)
    args = list(args)
    if len(args) == 0:
        # If not one passed args, then use sys.argv:
        args = sys.argv[1:]

    # we haven't even started parsing anything yet, but it's nice to know if we want debug
    for arg in args:
        if "--debug" in arg:
            util.debug_level = 1
            util.args['debug'] = True

    util.debug(f"Script File: {os.path.realpath(__file__)}")
    util.debug(f"Script Args: {args=}")

    util.debug(f"Starting automatic tool setup...")
    auto_tool_setup()

    util.info(f"*** OpenCOS EDA ***")
    if len(args) == 1 and '--debug' in args:
        # special snowflake case if someone called with a singular arg --debug
        # (without --help or exit)
        return interactive()
    elif len(args) > 0: return process_tokens(list(args))
    else:             return interactive() # go interactive if not given any arguments


def main_cli(support_respawn=False):
    ''' Returns None, will exit with return code. Entry point for package script or __main__.'''

    if support_respawn and '--no-respawn' not in sys.argv:
        # If someone called eda.py directly (aka, __name__ == '__main__'),
        # then we still support a legacy mode of operation - where we check
        # for OC_ROOT (in env, or git repo) to make sure this is the right
        # location of eda.py by calling main_cli(support_respawn=True).
        # Otherwise, we do not respawn $OC_ROOT/bin/eda.py
        # Can also be avoided with --no-respawn.

        # Note - respawn will never work if calling as a package executable script,
        # which is why our package entrypoint will be main_cli() w/out support_respawn.
        main_maybe_respawn()


    signal.signal(signal.SIGINT, signal_handler)
    util.global_exit_allowed = True
    # Strip eda or eda.py from sys.argv, we know who we are if called from __main__:
    rc = main()
    util.exit(rc)


def main_maybe_respawn():
    ''' Returns None, will respawn - run - exit, or will return and the command

    is expected to run in main_cli()'''

    # First we check if we are respawning
    this_path = os.path.realpath(__file__)
    if debug_respawn: util.info(f"RESPAWN: this_path : '{this_path}'")
    oc_root = util.get_oc_root()
    if debug_respawn: util.info(f"RESPAWN: oc_root   : '{oc_root}'")
    cwd = util.getcwd()
    if debug_respawn: util.info(f"RESPAWN: cwd       : '{cwd}'")
    if oc_root:
        new_paths = [
            os.path.join(oc_root, 'opencos', 'eda.py'),
            os.path.join(oc_root, 'bin', 'eda'),
        ]
        if debug_respawn: util.info(f"RESPAWN: {new_paths=} {this_path=}")
        if this_path not in new_paths and os.path.exists(new_paths[0]):
            # we are not the correct version of EDA for this Git repo, we should respawn
            util.info(f"{this_path} respawning {new_paths[0]} in {cwd} with --no-respawn")
            sys.argv[0] = new_paths[0]
            sys.argv.insert(1, '--no-respawn')
            proc = subprocess.Popen(sys.argv, shell=0, cwd=cwd, universal_newlines=True)
            while True:
                try:
                    proc.communicate()
                    break
                except KeyboardInterrupt:
                    continue
            # get exit status from proc and return it
            util.exit(proc.returncode, quiet=True)
        else:
            if debug_respawn: util.info(f"RESPAWN: {oc_root=} respawn not necessary")
    else:
        if debug_respawn: util.info("RESPAWN: respawn not necessary")


if __name__ == '__main__':
    main_cli(support_respawn=True)

# TODO:
# * read config from config files (script dir, home dir, cwd upwards to ... ? )

# IDEAS:
# * options with no default (i.e. if user doesn't override, THEN we set it, like "seed" or "work-dir") can be given a
#   special type (DefaultVar) versus saying "None" so that help can say more about it (it's a string, it's default val
#   is X, etc) and it can be queried as to whether it's really a default val.  This avoids having to avoid default vals
#   that user can never set (-1, None, etc) which make it hard to infer the type.  this same object can be given help
#   info and simply "render" to the expected type (str, integer, etc) when used.
