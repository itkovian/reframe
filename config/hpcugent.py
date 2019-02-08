#
# CSCS ReFrame settings
#


class ReframeSettings:
    reframe_module = 'reframe'
    job_poll_intervals = [1, 2, 3]
    job_submit_timeout = 60
    checks_path = ['checks/']
    checks_path_recurse = True
    site_configuration = {
        'systems': {
            'victini    ': {
                'descr': 'HPCUGent victini',
                'hostnames': ['node320[1-9]', 'node32[1-8][0-9]', 'node329[0-6]'],
                'modules_system': 'lmod',
                'partitions': {
                    'victini': {
                        'scheduler': 'nativeslurm',
                        'modules': ['cluster/victini'],
                        'access':  [],
                        'environs': ['PrgEnv-intel'],
                        'descr': 'victini',
                        'max_jobs': 96,
                    },
                }
            },
            'skitty': {
                'descr': 'HPCUGent skitty',
                'hostnames': ['node310[1-9]', 'node31[1-6][0-9]', 'node317[0-2]'],
                'modules_system': 'lmod',
                'partitions': {
                    'skitty': {
                        'scheduler': 'nativeslurm',
                        'modules': ['cluster/skitty'],
                        'access':  [],
                        'environs': ['PrgEnv-intel'],
                        'descr': 'skitty',
                        'max_jobs': 72,
                    },
                }
            }
        },
        'environments': {
            '*': {
                'PrgEnv-intel': {
                    'type': 'ProgEnvironment',
                    'modules': ['icc/2018.3.222-GCC-7.3.0-2.30'],
                },
                'PrgEnv-gcc': {
                    'type': 'ProgEnvironment',
                    'modules': ['icc/GCC/7.3.0-2.30'],
                },
            }
        },
    }

    logging_config = {
        'level': 'DEBUG',
        'handlers': [
            {
                'type': 'file',
                'name': 'reframe.log',
                'level': 'DEBUG',
                'format': '[%(asctime)s] %(levelname)s: '
                          '%(check_info)s: %(message)s',
                'append': False,
            },

            # Output handling
            {
                'type': 'stream',
                'name': 'stdout',
                'level': 'INFO',
                'format': '%(message)s'
            },
            {
                'type': 'file',
                'name': 'reframe.out',
                'level': 'INFO',
                'format': '%(message)s',
                'append': False,
            }
        ]
    }

    perf_logging_config = {
        'level': 'DEBUG',
        'handlers': [
            #@ {
            #@     'type': 'graylog',
            #@     'host': 'your-server-here',
            #@     'port': 12345,
            #@     'level': 'INFO',
            #@     'format': '%(message)s',
            #@     'extras': {
            #@         'facility': 'reframe',
            #@         'data-version': '1.0',
            #@     }
            #@ },
            {
                'type': 'filelog',
                'prefix': '%(check_system)s/%(check_partition)s',
                'level': 'INFO',
                'format': (
                    '%(asctime)s|reframe %(version)s|'
                    '%(check_info)s|jobid=%(check_jobid)s|'
                    '%(check_perf_var)s=%(check_perf_value)s|'
                    'ref=%(check_perf_ref)s '
                    '(l=%(check_perf_lower_thres)s, '
                    'u=%(check_perf_upper_thres)s)|'
                    '%(check_perf_unit)s'
                ),
                'append': True
            }
        ]
    }


settings = ReframeSettings()
