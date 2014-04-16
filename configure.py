#!/usr/bin/env python

# Configuraiton script for bootstrapping the gyp build 
# This script is based on the node configures script found at https://github.com/joyent/node/blob/master/configure

import optparse
import os 
import pprint
import shlex
import subprocess
import sys

CC = os.environ.get('CC', 'cc')

root_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root_dir, 'tools', 'gyp', 'pylib'))
from gyp.common import GetFlavor

# parse our options 
parser = optparse.OptionParser()

# Options should be in alphabetical order but keep --prefix at the top
parser.add_option('--prefix',
    action='store',
    dest='prefix',
    help='select the install prefix (defaults to /usr/local)')

parser.add_option('--debug',
    action='store_true',
    dest='debug',
    help='also build debug build')

parser.add_option('--dest-cpu',
    action='store',
    dest='dest_cpu',
    help='CPU architecture to build for. Valid values are: arm, ia32, x64')

parser.add_option('--dest-os',
    action='store',
    dest='dest_os',
    help='operating system to build for. Valid values are: '
         'win, mac, solaris, freebsd, openbsd, linux, android')

parser.add_option('--gdb',
    action='store_true',
    dest='gdb',
    help='add gdb support')

parser.add_option('--ninja',
    action='store_true',
    dest='use_ninja',
    help='gnerate files for the ninja build system')

parser.add_option('--shared-v8',
    action='store_true',
    dest='shared_v8',
    help='link to a shared V8 DLL instead of static linking')

parser.add_option('--shared-v8-includes',
    action='store',
    dest='shared_v8_includes',
    help='directory containing V8 header files')

parser.add_option('--shared-v8-libname',
    action='store',
    dest='shared_v8_libname',
    help='alternative lib name to link to (default: \'v8\')')

parser.add_option('--shared-v8-libpath',
    action='store',
    dest='shared_v8_libpath',
    help='a directory to search for the shared V8 DLL')

parser.add_option('--with-icu-path',
    action='store',
    dest='with_icu_path',
    help='Path to icu.gyp (ICU i18n, Chromium version only.)')

parser.add_option('--without-snapshot',
    action='store_true',
    dest='without_snapshot',
    help='build without snapshotting V8 libraries. You might want to set'
         'this for cross-compiling [Default: False]')

parser.add_option('--xcode',
    action='store_true',
    dest='use_xcode',
    help='generate build fiels for use with xcode')

(options, args) = parser.parse_args()

def b(value):
    """Return the string 'true' if value is truthy, 'false' otherwise"""
    if value:
        return 'true'
    else:
        return 'false'

def cc_macros():
    """Checks predefined macros using the CC command."""

    try:
        p = subprocess.Popen(shlex.split(CC) + ['-dM', '-E', '-'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    except OSError:
        print '''Weyland configure error: No accetable C compiler found!

            Please make sure you have a C compiler installed on your system and/or
            consider adjusting the CC environment variable if you installed 
            it in a non-standard prefix.
            '''
        sys.exit()

    p.stdin.write('\n')
    out = p.communicate()[0]

    out = str(out).split('\n')

    k = {}
    for line in out:
        lst = shlex.split(line)
        if len(lst) > 2:
            key = lst[1]
            val = lst[2]
            k[key] = val 
    return k

def host_arch_win():
    """Host architecture check using environ vars"""

    arch = os.environ.get('PROCESSOR_ARCHITECTURE', 'x86')

    matchup = {
        'AMD64' : 'x64',
        'x86'   : 'ia32',
        'arm'   : 'arm',
        'mips'  : 'mips',
    }

    return matchup.get(arch, 'ia32')

def host_arch_cc(o):
    """Host architecture check using the CC command."""

    k = cc_macros()

    matchup = {
        '__x86_64__' : 'x64',
        '__i386__'   : 'ia32',
        '__arm__'    : 'arm',
        '__mips__'   : 'mips',
    }

    rtn = 'ia32'

    for i in matchup:
        if i in k and k[i] != '0':
            rtn = matchup[i]
            break

    return rtn

def configure_weyland(o):
    if options.dest_os == 'android':
        o['variables']['OS'] = 'android'
    o['variables']['weyland_prefix'] = os.path.expanduser(options.prefix or '')
    o['default_configuration'] = 'Debug' if options.debug else 'Release'

    host_arch = host_arch_win() if os.name == 'nt' else host_arch_cc()
    target_arch = options.dest_cpu or host_arch
    o['variables']['host_arch'] = host_arch
    o['variables']['target_arch'] = target_arch

def configure_v8(o):
    o['variables']['weyland_shared_v8'] = b(options.shared_v8)
    o['variables']['v8_enable_gdbjit'] = 1 if options.gdb else 0
    o['variables']['v8_no_strict_aliasing'] = 1 # Work around for compiler bugs 
    o['variables']['v8_optimized_debug'] = 0    # Compile with -O0 in debug builds.
    o['variables']['v8_random_seed'] = 0        # Use random seed for hash tables. 
    o['variables']['v8_use_snapshot'] = b(not options.without_snapshot)

    # assume shared_v8 if one of these is set
    if options.shared_v8_libpath:
        o['libraries'] += ['-L%s' % options.shared_v8_libpath]
    if options.shared_v8_libname:
        o['libraries'] += ['-l%s' % options.shared_v8_libname]
    elif options.shared_v8:
        o['libraries'] += ['-lv8']
    if options.shared_v8_includes:
        o['include_dirs'] += [options.shared_v8_includes]

def configure_icu(o):
    have_icu_path = bool(options.with_icu_path)
    o['variables']['v8_enable_i18n_support'] = int(have_icu_path)
    if have_icu_path:
        o['variables']['icu_gyp_path'] = options.with_icu_path

def configure_gtest(o):
    o['variables']['gtest_dir'] = os.path.join(root_dir, "tools", "gtest")

# determine the "flavor" (operating system) we're building for,
# leveraging gyp's GetFlavor function
flavor_params = {}
if (options.dest_os):
    flavor_params['flavor'] = options.dest_os
flavor = GetFlavor(flavor_params)

output = {
    'variables': { 'python': sys.executable },
    'include_dirs': [],
    'libraries': [],
    'defines': [],
    'cflags': [],
}

configure_weyland(output)
configure_v8(output)
configure_icu(output)
configure_gtest(output)

# variables should be a root level element,
# move everything else to target_defaults
variables = output['variables']
del output['variables']
output = {
    'variables': variables,
    'target_defaults': output
}
pprint.pprint(output, indent=2)

def write(filename, data):
    filename = os.path.join(root_dir, filename)
    print 'creating ', filename
    f = open(filename, 'w+')
    f.write(data)

write('config.gypi', '# Do not edit. Generated by the configure script.\n' +
                     pprint.pformat(output, indent=2) + '\n')

config = {
    'BUILDTYPE': 'Debug' if options.debug else 'Release',
    'USE_NINJA': str(int(options.use_ninja or 0)),
    'USE_XCODE': str(int(options.use_xcode or 0)),
    'PYTHON': sys.executable,
}

if options.prefix:
    config['PREFIX'] = options.prefix 

config = '\n'.join(map('='.join, config.iteritems())) + '\n'

write('config.mk',
    '# Do not edit. Generated by the configure script.\n' + config)

gyp_args = [sys.executable, 'tools/gyp_weyland.py', '--no-parallel']

if options.use_ninja:
    gyp_args += ['-f', 'ninja-' + flavor]
elif options.use_xcode:
    gyp_args += ['-f', 'xcode']
elif flavor == 'win':
    gyp_args += ['-f', 'msvs', '-G', 'msvs_version=auto']
else:
    gyp_args += ['f', 'make-' + flavor]

gyp_args += args 

subprocess.call(gyp_args)