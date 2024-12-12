{
    "dev_data/collectors/collectors.py": [
        {
            "class_name": "DataCollectorBase",
            "bases": [
                "IterableDataset"
            ],
            "docstring": "Base class for data collectors.",
            "description": "This class is a base implementation for data collectors in machine learning models, providing a foundation for collecting and storing data. It offers methods to update policy weights, iterate over the collected data, shut down the collector, set a seed for reproducibility, load state dictionaries, and load pre-trained models from saved state dictionaries.",
            "overview": "",
            "functions": [
                {
                    "function_name": "update_policy_weights_",
                    "args": [
                        {
                            "arg_name": "policy_weights",
                            "return_type": "Optional[TensorDictBase]",
                            "default_value": "None",
                            "description": "This parameter is used to specify the weights assigned to each policy in a policy-based approach, allowing for customization of the model's behavior and decision-making process."
                        }
                    ],
                    "signature": "update_policy_weights_(self, policy_weights: Optional[TensorDictBase]=None) -> None",
                    "function_code": "def update_policy_weights_(self, policy_weights: Optional[TensorDictBase]=None) -> None:\n    \"\"\"Updates the policy weights if the policy of the data collector and the trained policy live on different devices.\n\n        Args:\n            policy_weights (TensorDictBase, optional): if provided, a TensorDict containing\n                the weights of the policy to be used for the udpdate.\n\n        \"\"\"\n    if policy_weights is not None:\n        self.policy_weights.data.update_(policy_weights)\n    elif self.get_weights_fn is not None:\n        self.policy_weights.data.update_(self.get_weights_fn())",
                    "docstring": "Updates the policy weights if the policy of the data collector and the trained policy live on different devices.\n\nArgs:\n    policy_weights (TensorDictBase, optional): if provided, a TensorDict containing\n        the weights of the policy to be used for the udpdate.",
                    "description": "This function is used to update the weights of a policy in a reinforcement learning context, allowing for efficient and adaptive policy updates. It takes an optional parameter `policy_weights` which can be used to specify new weights for the policy, or it will use the existing weights if not provided. The function does not return any value, instead updating the internal state of the object it is called on."
                },
                {
                    "function_name": "next",
                    "args": [],
                    "signature": "next(self)",
                    "function_code": "def next(self):\n    try:\n        if self._iterator is None:\n            self._iterator = iter(self)\n        out = next(self._iterator)\n        out.clear_device_()\n        return out\n    except StopIteration:\n        return None",
                    "docstring": "",
                    "description": "This function is used to move to the next item in a sequence or iterator, typically used when working with loops or iterating over data structures such as lists or generators. It advances the internal state of the object to point to the next element in the sequence, allowing for efficient iteration and processing of data."
                },
                {
                    "function_name": "shutdown",
                    "args": [],
                    "signature": "shutdown(self)",
                    "function_code": "@abc.abstractmethod\ndef shutdown(self):\n    raise NotImplementedError",
                    "docstring": "",
                    "description": "This function is used to initiate a shutdown process, likely terminating or closing various system resources, such as processes, connections, or applications, to bring the system to a safe state and prevent potential data loss or corruption."
                },
                {
                    "function_name": "iterator",
                    "args": [],
                    "signature": "iterator(self) -> Iterator[TensorDictBase]",
                    "function_code": "@abc.abstractmethod\ndef iterator(self) -> Iterator[TensorDictBase]:\n    raise NotImplementedError",
                    "docstring": "",
                    "description": "This function is used to create an iterator for a TensorDictBase object, allowing it to be traversed and iterated over in a controlled manner."
                },
                {
                    "function_name": "set_seed",
                    "args": [
                        {
                            "arg_name": "seed",
                            "return_type": "int",
                            "default_value": "",
                            "description": "This parameter is used to initialize the random number generator, allowing for reproducibility of results and enabling users to set a specific starting point for their random number generation."
                        },
                        {
                            "arg_name": "static_seed",
                            "return_type": "bool",
                            "default_value": "False",
                            "description": "This parameter is used to enable or disable the use of a static seed for random number generation, allowing for reproducibility and deterministic behavior in simulations."
                        }
                    ],
                    "signature": "set_seed(self, seed: int, static_seed: bool=False) -> int",
                    "function_code": "@abc.abstractmethod\ndef set_seed(self, seed: int, static_seed: bool=False) -> int:\n    raise NotImplementedError",
                    "docstring": "",
                    "description": "This function is used to initialize a random number generator with a specified seed value, allowing for reproducibility and control over the sequence of random numbers generated. The function takes an optional parameter 'static_seed' which defaults to False, indicating whether the seed should be set as static or not."
                },
                {
                    "function_name": "state_dict",
                    "args": [],
                    "signature": "state_dict(self) -> OrderedDict",
                    "function_code": "@abc.abstractmethod\ndef state_dict(self) -> OrderedDict:\n    raise NotImplementedError",
                    "docstring": "",
                    "description": "This function is used to retrieve and return a dictionary representation of the model's state, which captures its current weights and other parameters. The returned dictionary can be used for serialization or loading purposes, allowing the model to be saved and restored at a later time."
                },
                {
                    "function_name": "load_state_dict",
                    "args": [
                        {
                            "arg_name": "state_dict",
                            "return_type": "OrderedDict",
                            "default_value": "",
                            "description": "This parameter is used to store and retrieve the model's state, which includes all the learned parameters and their values. It allows for saving and loading a trained model, enabling tasks such as model checkpointing, serialization, and deserialization. The state dictionary can be used to restore a model from a saved state, effectively reviving the model's weights and biases."
                        }
                    ],
                    "signature": "load_state_dict(self, state_dict: OrderedDict) -> None",
                    "function_code": "@abc.abstractmethod\ndef load_state_dict(self, state_dict: OrderedDict) -> None:\n    raise NotImplementedError",
                    "docstring": "",
                    "description": "This function is used to load a pre-trained model's state dictionary into the current model instance, allowing for the restoration of previously trained weights and parameters. It takes an ordered dictionary containing the model's state as input and updates the internal state of the model with the loaded values, effectively reloading the model from a saved checkpoint or resume training from a previous point."
                }
            ]
        }
    ]
}
