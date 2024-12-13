

class DataCollectorBase(IterableDataset, metaclass=abc.ABCMeta):
    """Base class for data collectors."""

    _iterator = None
    total_frames: int
    frames_per_batch: int
    trust_policy: bool
    compiled_policy: bool
    cudagraphed_policy: bool

    def _get_policy_and_device(
        self,
        policy: Callable[[Any], Any] | None = None,
        observation_spec: TensorSpec = None,
        policy_device: Any = NO_DEFAULT,
        env_maker: Any | None = None,
        env_maker_kwargs: dict | None = None,
    ) -> Tuple[TensorDictModule, Union[None, Callable[[], dict]]]:
        """Util method to get a policy and its device given the collector __init__ inputs.

        Args:
            policy (TensorDictModule, optional): a policy to be used
            observation_spec (TensorSpec, optional): spec of the observations
            policy_device (torch.device, optional): the device where the policy should be placed.
                Defaults to self.policy_device
            env_maker (a callable or a batched env, optional): the env_maker function for this device/policy pair.
            env_maker_kwargs (a dict, optional): the env_maker function kwargs.

        """
        if policy_device is NO_DEFAULT:
            policy_device = self.policy_device

        if not self.trust_policy:
            env = getattr(self, "env", None)
            policy = _make_compatible_policy(
                policy,
                observation_spec,
                env=env,
                env_maker=env_maker,
                env_maker_kwargs=env_maker_kwargs,
            )
        if not policy_device:
            return policy, None

        if isinstance(policy, nn.Module):
            param_and_buf = TensorDict.from_module(policy, as_module=True)
        else:
            # Because we want to reach the warning
            param_and_buf = TensorDict()

        i = -1
        for p in param_and_buf.values(True, True):
            i += 1
            if p.device != policy_device:
                # Then we need casting
                break
        else:
            if i == -1 and not self.trust_policy:
                # We trust that the policy policy device is adequate
                warnings.warn(
                    "A policy device was provided but no parameter/buffer could be found in "
                    "the policy. Casting to policy_device is therefore impossible. "
                    "The collector will trust that the devices match. To suppress this "
                    "warning, set `trust_policy=True` when building the collector."
                )
            return policy, None

        def map_weight(
            weight,
            policy_device=policy_device,
        ):

            is_param = isinstance(weight, Parameter)
            is_buffer = isinstance(weight, Buffer)
            weight = weight.data
            if weight.device != policy_device:
                weight = weight.to(policy_device)
            elif weight.device.type in ("cpu", "mps"):
                weight = weight.share_memory_()
            if is_param:
                weight = Parameter(weight, requires_grad=False)
            elif is_buffer:
                weight = Buffer(weight)
            return weight

        # Create a stateless policy, then populate this copy with params on device
        get_original_weights = functools.partial(TensorDict.from_module, policy)
        with param_and_buf.to("meta").to_module(policy):
            policy = deepcopy(policy)

        param_and_buf.apply(
            functools.partial(map_weight),
            filter_empty=False,
        ).to_module(policy)
        return policy, get_original_weights

    def update_policy_weights_(
        self, policy_weights: Optional[TensorDictBase] = None
    ) -> None:
        """Updates the policy weights if the policy of the data collector and the trained policy live on different devices.

        Args:
            policy_weights (TensorDictBase, optional): if provided, a TensorDict containing
                the weights of the policy to be used for the udpdate.

        """
        if policy_weights is not None:
            self.policy_weights.data.update_(policy_weights)
        elif self.get_weights_fn is not None:
            self.policy_weights.data.update_(self.get_weights_fn())

    def __iter__(self) -> Iterator[TensorDictBase]:
        yield from self.iterator()

    def next(self):
        try:
            if self._iterator is None:
                self._iterator = iter(self)
            out = next(self._iterator)
            # if any, we don't want the device ref to be passed in distributed settings
            out.clear_device_()
            return out
        except StopIteration:
            return None

    @abc.abstractmethod
    def shutdown(self):
        raise NotImplementedError

    @abc.abstractmethod
    def iterator(self) -> Iterator[TensorDictBase]:
        raise NotImplementedError

    @abc.abstractmethod
    def set_seed(self, seed: int, static_seed: bool = False) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def state_dict(self) -> OrderedDict:
        raise NotImplementedError

    @abc.abstractmethod
    def load_state_dict(self, state_dict: OrderedDict) -> None:
        raise NotImplementedError

    def _read_compile_kwargs(self, compile_policy, cudagraph_policy):
        self.compiled_policy = compile_policy not in (False, None)
        self.cudagraphed_policy = cudagraph_policy not in (False, None)
        self.compiled_policy_kwargs = (
            {} if not isinstance(compile_policy, typing.Mapping) else compile_policy
        )
        self.cudagraphed_policy_kwargs = (
            {} if not isinstance(cudagraph_policy, typing.Mapping) else cudagraph_policy
        )

    def __repr__(self) -> str:
        string = f"{self.__class__.__name__}()"
        return string

    def __class_getitem__(self, index):
        raise NotImplementedError

    def __len__(self) -> int:
        if self.total_frames > 0:
            return -(self.total_frames // -self.frames_per_batch)
        raise RuntimeError("Non-terminating collectors do not have a length")


