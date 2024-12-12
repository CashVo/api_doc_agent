{
    "dev_data/collectors/collectors.py": [
        {
            "class_name": "DataCollectorBase",
            "bases": [
                "IterableDataset"
            ],
            "docstring": "Base class for data collectors.",
            "description": "",
            "overview": "",
            "functions": [
                {
                    "function_name": "update_policy_weights_",
                    "args": [
                        {
                            "arg_name": "policy_weights",
                            "return_type": "Optional[TensorDictBase]",
                            "default_value": "None",
                            "description": ""
                        }
                    ],
                    "signature": "update_policy_weights_(self, policy_weights: Optional[TensorDictBase]=None) -> None",
                    "function_code": "def update_policy_weights_(self, policy_weights: Optional[TensorDictBase]=None) -> None:\n    \"\"\"Updates the policy weights if the policy of the data collector and the trained policy live on different devices.\n\n        Args:\n            policy_weights (TensorDictBase, optional): if provided, a TensorDict containing\n                the weights of the policy to be used for the udpdate.\n\n        \"\"\"\n    if policy_weights is not None:\n        self.policy_weights.data.update_(policy_weights)\n    elif self.get_weights_fn is not None:\n        self.policy_weights.data.update_(self.get_weights_fn())",
                    "docstring": "Updates the policy weights if the policy of the data collector and the trained policy live on different devices.\n\nArgs:\n    policy_weights (TensorDictBase, optional): if provided, a TensorDict containing\n        the weights of the policy to be used for the udpdate.",
                    "description": ""
                },
                {
                    "function_name": "next",
                    "args": [],
                    "signature": "next(self)",
                    "function_code": "def next(self):\n    try:\n        if self._iterator is None:\n            self._iterator = iter(self)\n        out = next(self._iterator)\n        out.clear_device_()\n        return out\n    except StopIteration:\n        return None",
                    "docstring": "",
                    "description": ""
                },
                {
                    "function_name": "shutdown",
                    "args": [],
                    "signature": "shutdown(self)",
                    "function_code": "@abc.abstractmethod\ndef shutdown(self):\n    raise NotImplementedError",
                    "docstring": "",
                    "description": ""
                },
                {
                    "function_name": "iterator",
                    "args": [],
                    "signature": "iterator(self) -> Iterator[TensorDictBase]",
                    "function_code": "@abc.abstractmethod\ndef iterator(self) -> Iterator[TensorDictBase]:\n    raise NotImplementedError",
                    "docstring": "",
                    "description": ""
                },
                {
                    "function_name": "set_seed",
                    "args": [
                        {
                            "arg_name": "seed",
                            "return_type": "int",
                            "default_value": "",
                            "description": ""
                        },
                        {
                            "arg_name": "static_seed",
                            "return_type": "bool",
                            "default_value": "False",
                            "description": ""
                        }
                    ],
                    "signature": "set_seed(self, seed: int, static_seed: bool=False) -> int",
                    "function_code": "@abc.abstractmethod\ndef set_seed(self, seed: int, static_seed: bool=False) -> int:\n    raise NotImplementedError",
                    "docstring": "",
                    "description": ""
                },
                {
                    "function_name": "state_dict",
                    "args": [],
                    "signature": "state_dict(self) -> OrderedDict",
                    "function_code": "@abc.abstractmethod\ndef state_dict(self) -> OrderedDict:\n    raise NotImplementedError",
                    "docstring": "",
                    "description": ""
                },
                {
                    "function_name": "load_state_dict",
                    "args": [
                        {
                            "arg_name": "state_dict",
                            "return_type": "OrderedDict",
                            "default_value": "",
                            "description": ""
                        }
                    ],
                    "signature": "load_state_dict(self, state_dict: OrderedDict) -> None",
                    "function_code": "@abc.abstractmethod\ndef load_state_dict(self, state_dict: OrderedDict) -> None:\n    raise NotImplementedError",
                    "docstring": "",
                    "description": ""
                }
            ]
        }
    ]
}
