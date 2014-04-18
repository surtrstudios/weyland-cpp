{
	'variables': {
		'v8_use_snapshot%': 'true',
	},

	'targets': [
		{
			'target_name': 'weyland',
			'type': 'executable',

            'sources': [
                'src/main.cc',
                'example/simple.js',
            ],

			'dependencies': [ 
                'weyland_base',
                './deps/v8/tools/gyp/v8.gyp:v8',
                './deps/surtrlog/surtrlog.gyp:surtrlog'
            ],
		},
        {
            'target_name': 'weyland_base',
            'type': '<(library)',

            'sources': [
                'src/base/base.cc',
                'src/base/package.cc',
                'include/weyland/version.h',
                'include/weyland/package.h',
            ],

            'include_dirs': [
                'include'
            ],

            'dependencies': [
                './deps/surtrlog/surtrlog.gyp:surtrlog'
            ],

            'direct_dependent_settings': {
                'include_dirs': [
                    'include'
                ],
            },
        },
        {
            'target_name': 'weyland_tests',
            'type': 'executable',

            'sources': [
                'test/weyland_test.cc',
            ],

            'dependencies': [
                'weyland_base',
                '<(gtest_dir)/gtest.gyp:gtest_main',
            ],
        },
	],
}