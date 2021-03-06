{
    'variables': {
        'werror': '',                       # Turn off -Werror in V8 build.
        'visibility%': 'hidden',            # V8's visibility setting
        'target_arch%': 'ia32',             # set v8's target architecture
        'host_arch%': 'ia32',               # set v8's host architecture
        'want_seperate_host_toolset': 0,    # V8 should not build target and host
        'library%': 'static_library',       # allow override to 'shared_library' for DLL/.so builds
        'component%': 'static_library',     # NB. these names match with what v8 expects
        'msvs_multi_core_compile': '0',     # we do enable multicore compiles, but no v8's method
        'gcc_version%': 'unknown',
        'clang%': 0,
        'phthon%': 'python',

        # Enable V8's post-mortem debuggin only on unix flavors.
        'conditions': [
            ['OS == "win"', {
                'os_posix': 0,
                'v8_postmortem_support': 'false'
            }, {
                'os_posix': 1,
                'v8_postmortem_support': 'false'
            }],
            ['GENERATOR == "ninja"', {
                'OBJ_DIR': '<(PRODUCT_DIR)/obj',
                'V8_BASE': '<(PRODUCT_DIR)/libv8_base.<(target_arch).a',
            }, {
                'OBJ_DIR': '<(PRODUCT_DIR)/obj.target',
                'V8_BASE': '<(PRODUCT_DIR)/obj.target/deps/v8/tools/gyp/libv8_base.<(target_arch).a',
            }],
        ],
    },

    'target_defaults': {
        'default_configuration': 'Release',
        'configurations': {
            'Debug': {
                'defines': [ 'DEBUG', '_DEBUG' ],
                'cflags': [ '-g', '-O0', '-std=c++11' ],
                'conditions': [
                    ['target_arch=="x64"', {
                        'msvs_configuration_platform': 'x64',
                    }],
                ],
                'msvs_settings': {
                    'VCCLCompilerTool': {
                        'RuntimeLibrary': 1,        # static debug 
                        'Optimization': 0,          # /Od, no optimization
                        'MinimalRebuild': 'false',
                        'OmitFramePointers': 'false',
                        'BasicRuntimeChecks': 3,    # /RTC1
                    },
                    'VCLinkerTool': {
                        'LinkIncremental': 2,   # enable incremental linking
                    },
                },
                'xcode_settings': {
                    'GCC_OPTIMIZATION_LEVEL': '0',  # stop gyp from defaulting to -Os
                },
            },
            'Release': {
                'cflags': [ '-O3', '-ffunction-sections', '-fdata-sections' ],
                'conditions': [
                    ['target_arch=="x64"', {
                        'msvs_configuration_platform': 'x64',
                    }],
                    ['OS=="solaris"', {
                        # pull in v8's postmortem metadata
                        'ldflags': [ '-Wl,-z,allextract' ]
                    }],
                    ['clang == 0 and gcc_version >= 40', {
                        'clfags': [ '-fno-tree-vrp' ], # Work around compiler bug 
                    }],
                    ['clang == 0 and gcc_version <= 44', {
                        'cflags': [ '-fno-tree-sink' ], # Work around compiler bug 
                    }],
                    ['OS!="mac" and OS!="win"', {
                        'clfags': [ '-fno-omit-frame-pointer' ],
                    }],
                ],
                'msvs_settings': {
                    'VCCLCompilerTool': {
                        'RuntimeLibrary': 0,
                        'Optimization': 3,
                        'FavorSizeOrSpeed': 1,
                        'InlineFunctionExpansion': 2,
                        'WholeProgramOptimization': 'true',
                        'OmitFramePointers': 'true',
                        'EnableFunctionLevelLinking': 'true',
                        'EnableIntrinsicFunctions': 'true',
                        'RuntimeTypeInfo': 'false',
                        'ExceptionHandling': '0',
                        'AdditionalOptions': [
                            '/MP',
                        ],
                    },
                    'VCLibrarianTool': {
                        'AdditionalOptions': [
                            '/LTCG',
                        ],
                    },
                    'VCLinkerTool': {
                        'LinkTimeCodeGeneration': 1,
                        'OptimizeReferences': 2,
                        'EnableCOMDATFolding': 2,
                        'LinkIncremental': 1
                    },
                },
            }
        },
        # Forcibly disable -Werror.  We support a wide range of compilers, it's
    # simply not feasible to squelch all warnings, never mind that the
    # libraries in deps/ are not under our control.
    'cflags!': ['-Werror'],
    'msvs_settings': {
      'VCCLCompilerTool': {
        'StringPooling': 'true', # pool string literals
        'DebugInformationFormat': 3, # Generate a PDB
        'WarningLevel': 3,
        'BufferSecurityCheck': 'true',
        'ExceptionHandling': 1, # /EHsc
        'SuppressStartupBanner': 'true',
        'WarnAsError': 'false',
      },
      'VCLibrarianTool': {
      },
      'VCLinkerTool': {
        'conditions': [
          ['target_arch=="x64"', {
            'TargetMachine' : 17 # /MACHINE:X64
          }],
        ],
        'GenerateDebugInformation': 'true',
        'RandomizedBaseAddress': 2, # enable ASLR
        'DataExecutionPrevention': 2, # enable DEP
        'AllowIsolation': 'true',
        'SuppressStartupBanner': 'true',
        'target_conditions': [
          ['_type=="executable"', {
            'SubSystem': 1, # console executable
          }],
        ],
      },
    },
    'msvs_disabled_warnings': [4351, 4355, 4800],
    'conditions': [
      ['OS == "win"', {
        'msvs_cygwin_shell': 0, # prevent actions from trying to use cygwin
        'defines': [
          'WIN32',
          # we don't really want VC++ warning us about
          # how dangerous C functions are...
          '_CRT_SECURE_NO_DEPRECATE',
          # ... or that C implementations shouldn't use
          # POSIX names
          '_CRT_NONSTDC_NO_DEPRECATE',
          'BUILDING_V8_SHARED=1',
          'BUILDING_UV_SHARED=1',
        ],
      }],
      [ 'OS in "linux freebsd openbsd solaris"', {
        'cflags': [ '-pthread', ],
        'ldflags': [ '-pthread' ],
      }],
      [ 'OS in "linux freebsd openbsd solaris android"', {
        'cflags': [ '-Wall', '-Wextra', '-Wno-unused-parameter', ],
        'cflags_cc': [ '-fno-rtti', '-fno-exceptions' ],
        'ldflags': [ '-rdynamic' ],
        'target_conditions': [
          ['_type=="static_library"', {
            'standalone_static_library': 1, # disable thin archive which needs binutils >= 2.19
          }],
        ],
        'conditions': [
          [ 'target_arch=="ia32"', {
            'cflags': [ '-m32' ],
            'ldflags': [ '-m32' ],
          }],
          [ 'target_arch=="x64"', {
            'cflags': [ '-m64' ],
            'ldflags': [ '-m64' ],
          }],
          [ 'OS=="solaris"', {
            'cflags': [ '-pthreads' ],
            'ldflags': [ '-pthreads' ],
            'cflags!': [ '-pthread' ],
            'ldflags!': [ '-pthread' ],
          }],
        ],
      }],
      [ 'OS=="android"', {
        'defines': ['_GLIBCXX_USE_C99_MATH'],
        'libraries': [ '-llog' ],
      }],
      ['OS=="mac"', {
        'defines': ['_DARWIN_USE_64_BIT_INODE=1'],
        'xcode_settings': {
          'ALWAYS_SEARCH_USER_PATHS': 'NO',
          'GCC_CW_ASM_SYNTAX': 'NO',                # No -fasm-blocks
          'GCC_DYNAMIC_NO_PIC': 'NO',               # No -mdynamic-no-pic
                                                    # (Equivalent to -fPIC)
          'GCC_ENABLE_CPP_EXCEPTIONS': 'NO',        # -fno-exceptions
          'GCC_ENABLE_CPP_RTTI': 'NO',              # -fno-rtti
          'GCC_ENABLE_PASCAL_STRINGS': 'NO',        # No -mpascal-strings
          'GCC_THREADSAFE_STATICS': 'NO',           # -fno-threadsafe-statics
          'PREBINDING': 'NO',                       # No -Wl,-prebind
          'MACOSX_DEPLOYMENT_TARGET': '10.5',       # -mmacosx-version-min=10.5
          'USE_HEADERMAP': 'NO',
          'OTHER_CFLAGS': [
            '-fno-strict-aliasing',
          ],
          'WARNING_CFLAGS': [
            '-Wall',
            '-Wendif-labels',
            '-W',
            '-Wno-unused-parameter',
          ],
        },
        'target_conditions': [
          ['_type!="static_library"', {
            'xcode_settings': {'OTHER_LDFLAGS': ['-Wl,-search_paths_first']},
          }],
        ],
        'conditions': [
          ['target_arch=="ia32"', {
            'xcode_settings': {'ARCHS': ['i386']},
          }],
          ['target_arch=="x64"', {
            'xcode_settings': {'ARCHS': ['x86_64']},
          }],
        ],
      }],
      ['OS=="freebsd" and node_use_dtrace=="true"', {
        'libraries': [ '-lelf' ],
      }]
    ],
  }
}