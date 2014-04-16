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

			'dependencies': [ './deps/v8/tools/gyp/v8.gyp:v8' ],
		},
	],
}