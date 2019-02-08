import reframe as rfm
import reframe.utility.sanity as sn


@rfm.required_version('>=2.14')
@rfm.simple_test
class StreamTest(rfm.RegressionTest):
    def __init__(self):
        super().__init__()
        self.descr = 'STREAM Benchmark'
        self.exclusive_access = True
        # All available systems are supported
        self.valid_systems = ['*']
        self.valid_prog_environs = ['PrgEnv-intel']
        self.modules = ['STREAM/5.10-intel-2018b']

        self.build_system = None
        self.sanity_patterns = sn.assert_found(
            r'Solution Validates: avg error less than', self.stdout)
        self.num_tasks = 1
        self.num_tasks_per_node = 1
        self.stream_cpus_per_task = {
            'delcatty:delcatty': 16,
            'phanpy:phanpy': 24,
            'golett:golett': 24,
            'swalot:swalot': 20,
            'victini:victini': 36,
            'skitty:skitty': 36,
        }

        self.variables = {
            'OMP_PLACES': 'threads',
            'OMP_PROC_BIND': 'spread'
        }
        self.stream_bw_reference = {
            'PrgEnv-intel': {
                'skitty:skitty': {'triad': (50223.0, -0.15, None)},
                'victini:victini': {'triad': (56643.0, -0.25, None)},
            },
        }
        self.perf_patterns = {
            'triad': sn.extractsingle(r'Triad:\s+(?P<triad>\S+)\s+\S+',
                                      self.stdout, 'triad', float),
            'add': sn.extractsingle(r'Add:\s+(?P<add>\S+)\s+\S+',
                                    self.stdout, 'add', float),
            'copy': sn.extractsingle(r'Copy:\s+(?P<copy>\S+)\s+\S+',
                                     self.stdout, 'copy', float),
            'scale': sn.extractsingle(r'Scale:\s+(?P<scale>\S+)\s+\S+',
                                      self.stdout, 'scale', float),
        }

        self.tags = {'production', 'maintenance_check'}
        self.maintainers = ['ag']

    def setup(self, partition, environ, **job_opts):
        self.num_cpus_per_task = self.stream_cpus_per_task[partition.fullname]
        envname = environ.name

        self.reference = self.stream_bw_reference[envname]
        # On SLURM there is no need to set OMP_NUM_THREADS if one defines
        # num_cpus_per_task, but adding for completeness and portability
        self.variables['OMP_NUM_THREADS'] = str(self.num_cpus_per_task)

        super().setup(partition, environ, **job_opts)
