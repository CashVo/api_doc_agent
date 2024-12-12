{
    "dev_data/collectors/distributed/utils.py": [
        {
            "class_name": "submitit_delayed_launcher",
            "bases": [],
            "docstring": "Delayed launcher for submitit.\n\nIn some cases, launched jobs cannot spawn other jobs on their own and this\ncan only be done at the jump-host level.\n\nIn these cases, the :func:`submitit_delayed_launcher` can be used to\npre-launch collector nodes that will wait for the main worker to provide\nthe launching instruction.\n\nArgs:\n    num_jobs (int): the number of collection jobs to be launched.\n    framework (str, optional): the framework to use. Can be either ``\"distributed\"``\n        or ``\"rpc\"``. ``\"distributed\"`` requires a :class:`~.DistributedDataCollector`\n        collector whereas ``\"rpc\"`` requires a :class:`RPCDataCollector`.\n        Defaults to ``\"distributed\"``.\n    backend (str, optional): torch.distributed backend in case ``framework``\n        points to ``\"distributed\"``. This value must match the one passed to\n        the collector, otherwise main and satellite nodes will fail to\n        reach the rendezvous and hang forever (ie no exception will be raised!)\n        Defaults to ``'gloo'``.\n    tcpport (int or str, optional): the TCP port to use.\n        Defaults to :obj:`torchrl.collectors.distributed.default_configs.TCP_PORT`\n    submitit_main_conf (dict, optional): the main node configuration to be passed to submitit.\n        Defaults to :obj:`torchrl.collectors.distributed.default_configs.DEFAULT_SLURM_CONF_MAIN`\n    submitit_collection_conf (dict, optional): the configuration to be passed to submitit.\n        Defaults to :obj:`torchrl.collectors.distributed.default_configs.DEFAULT_SLURM_CONF`\n\nExamples:\n    >>> num_jobs=2\n    >>> @submitit_delayed_launcher(num_jobs=num_jobs)\n    ... def main():\n    ...     from torchrl.envs.utils import RandomPolicy\n            from torchrl.envs.libs.gym import GymEnv\n    ...     from torchrl.data import BoundedContinuous\n    ...     collector = DistributedDataCollector(\n    ...         [EnvCreator(lambda: GymEnv(\"Pendulum-v1\"))] * num_jobs,\n    ...         policy=RandomPolicy(BoundedContinuous(-1, 1, shape=(1,))),\n    ...         launcher=\"submitit_delayed\",\n    ...     )\n    ...     for data in collector:\n    ...         print(data)\n    ...\n    >>> if __name__ == \"__main__\":\n    ...     main()\n    ...",
            "description": "This class is a tool designed to manage and execute delayed submissions in a system, likely used for academic or competitive programming purposes. It provides an interface for launching programs with a specified delay between stages of the submission process. The class can be utilized to create a controlled environment where users can submit their code at a predetermined time, allowing for more organized and fair competition.",
            "overview": "",
            "functions": [
                {
                    "function_name": "__init__",
                    "args": [
                        {
                            "arg_name": "num_jobs",
                            "return_type": "",
                            "default_value": "",
                            "description": "This parameter is used to specify the number of worker processes to use when running a job. It allows for parallel processing and can significantly improve performance on multi-core systems by utilizing multiple CPU cores simultaneously."
                        },
                        {
                            "arg_name": "framework",
                            "return_type": "",
                            "default_value": "'distributed'",
                            "description": "This parameter is used to specify the framework or architecture of a system, application, or project. It determines how the system will be structured and organized, including the tools, libraries, and technologies used. The value of this parameter can affect the overall performance, scalability, and maintainability of the system."
                        },
                        {
                            "arg_name": "backend",
                            "return_type": "",
                            "default_value": "'gloo'",
                            "description": "This parameter is used to specify the backend framework or service that will be used for the application. The default value provided, \"gloo\", suggests that it may be related to a specific cloud-based platform or service."
                        },
                        {
                            "arg_name": "tcpport",
                            "return_type": "",
                            "default_value": "TCP_PORT",
                            "description": "This parameter is used to specify the port number for TCP connections, allowing users to customize the communication protocol."
                        },
                        {
                            "arg_name": "submitit_main_conf",
                            "return_type": "dict",
                            "default_value": "DEFAULT_SLURM_CONF_MAIN",
                            "description": "This parameter is used to specify the configuration file for the Slurm main configuration, which controls the behavior of the Slurm job scheduler. When provided, this parameter overrides the default Slurm configuration and allows users to customize settings such as resource allocation, job scheduling, and more."
                        },
                        {
                            "arg_name": "submitit_collection_conf",
                            "return_type": "dict",
                            "default_value": "DEFAULT_SLURM_CONF",
                            "description": "This parameter is used to configure the submission of a collection in Slurm, allowing users to customize various settings such as resource allocation and job scheduling. It provides an opportunity for users to tailor their submission process to meet specific requirements or preferences."
                        }
                    ],
                    "signature": "__init__(self, num_jobs, framework='distributed', backend='gloo', tcpport=TCP_PORT, submitit_main_conf: dict=DEFAULT_SLURM_CONF_MAIN, submitit_collection_conf: dict=DEFAULT_SLURM_CONF)",
                    "function_code": "def __init__(self, num_jobs, framework='distributed', backend='gloo', tcpport=TCP_PORT, submitit_main_conf: dict=DEFAULT_SLURM_CONF_MAIN, submitit_collection_conf: dict=DEFAULT_SLURM_CONF):\n    self.num_jobs = num_jobs\n    self.backend = backend\n    self.framework = framework\n    self.submitit_collection_conf = submitit_collection_conf\n    self.submitit_main_conf = submitit_main_conf\n    self.tcpport = tcpport",
                    "docstring": "",
                    "description": "This function is used to initialize an instance of a class, setting its attributes and configuration parameters based on the provided arguments. It allows for customization of various settings such as the number of jobs, framework, backend, TCP port, and configuration dictionaries for submitit main and collection configurations."
                }
            ]
        }
    ]
}
