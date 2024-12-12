# ~/ClientFactory/src/clientfactory/clients/search/core.py
import enum, typing as t
from dataclasses import dataclass, field, fields, asdict
from clientfactory.utils.request import RequestMethod
from clientfactory.resources import Resource, ResourceConfig
from clientfactory.clients.search.adapters import AlgoliaConfig, RESTConfig,  GQLConfig
from loguru import logger as log

class ParameterType(enum.Enum):
    QUERY = enum.auto()
    FILTER = enum.auto()
    PAGE = enum.auto()
    HITS = enum.auto()
    SORT = enum.auto()
    FACET = enum.auto()
    CUSTOM = enum.auto()

@dataclass
class Parameter: # the instantiated name will be the kwarg bozo
    name: t.Optional[str] = None
    default: t.Optional[t.Any] = None
    type: t.Optional[t.Type] = None
    required: bool = False
    paramtype: ParameterType = ParameterType.CUSTOM


    def __post_init__(self):
        log.debug(f"Parameter.__post_init__ | initializing parameter[{self.name}]")
        if (self.default is not None) and (self.type is not None) and (not isinstance(self.default, self.type)):
            log.debug(f"Parameter.__post_init__ | enforcing type[{self.type}] on default[{self.default}]")
            try:
                self.default = self.type(self.default)
            except Exception as e:
                log.error(f"Parameter.__post_init__ | type enforcement failed: {str(e)}")
                raise ValueError(f"Exception enforcing parameter type: {self.type} on default value: {self.default}")

@dataclass
class Payload:
    key: str = 'json'
    parameters: dict[str, Parameter] = field(default_factory=dict)

    def __init__(self, *args, **kwargs):
        log.debug(f"Payload.__init__ | creating payload with args[{args}] kwargs[{kwargs}]")
        parameters = {}
        # Handle positional args
        for arg in args:
            log.debug(f"Payload.__init__ | processing arg[{arg}]")
            if isinstance(arg, Parameter):
                if arg.name is None: # variable name when None
                    arg.name = next((k for k, v in kwargs.items() if v is arg), arg.__class__.__name__.lower())
                parameters[arg.name] = arg
            elif isinstance(arg, dict):
                for k, v in arg.items():
                    if isinstance(v, Parameter):
                        parameters[k] = v
                    else:
                        param = Parameter(**v if isinstance(v, dict) else {'name': v})
                        parameters[k] = param
            elif isinstance(arg, str):
                param = Parameter(name=arg)
                parameters[arg] = param

        # Handle keyword args
        for k, v in kwargs.items():
            log.debug(f"Payload.__init__ | processing kwarg[{k}={v}]")
            if isinstance(v, Parameter):
                if v.name is None:
                    v.name = k
                parameters[k] = v
            else:
                param = Parameter(name=k, **v if isinstance(v, dict) else {'name': v})
                parameters[k] = param

        log.debug(f"Payload.__init__ | initialized with parameters[{parameters}]")
        self.parameters = parameters


    def map(self, **kwargs) -> dict:
        log.debug(f"Payload.map | mapping kwargs[{kwargs}]")
        mapped = {}
        for k, v in kwargs.items():
            if k not in self.parameters:
                log.warning(f"payload.map | received unexpected parametert: [{k}]")
                continue
            param = self.parameters[k]
            mapped[param.name] = v

        for name, param in self.parameters.items():
            if name not in kwargs and param.default is not None:
                log.debug(f"payload.map | applying default[{param.default}] for parameter[{name}]")
                mapped[param.name] = param.default

        log.debug(f"payload.map | mapped[{mapped}]")
        return mapped

    def validate(self, **kwargs) -> bool:
        log.debug(f"Payload.validate | validating kwargs[{kwargs}]")

        # guard unexpected args
        if invalid:=[k for k in kwargs if k not in self.parameters]:
            log.error(f"payload.validate | invalid parameters: [{invalid}]")
            raise ValueError(f"Invalid Parameters: {invalid}")

        # guard missing required
        if missingrequired := [
            name for name, param in self.parameters.items()
            if param.required and name not in kwargs
        ]:
            log.error(f"payload.validate | missing required parameters: [{missingrequired}]")
            raise ValueError(f"missing required parameters: [{missingrequired}]")

        # type check
        for name, value in kwargs.items():
            param = self.parameters[name]
            if param.type and not isinstance(value, param.type):
                try:
                    param.type(value)
                except:
                    log.error(f"Payload.validate | invalid type for parameter[{name}]: expected[{param.type}] got[{type(value)}]")
                    raise ValueError(f"Invalid type for {name}: expected {param.type}, got {type(value)}")

        return True


class ProtocolType(enum.Enum):
    REST = enum.auto()
    GRAPHQL = enum.auto()
    ALGOLIA = enum.auto()

@dataclass
class Protocol:
    type: ProtocolType
    method: RequestMethod

    def __post_init__(self):
        log.debug(f"Protocol.__post_init__ | initializing protocol[{self.type}] method[{self.method}]")
        # some logic to handle different input datatypes to standardize to the annotated ones
        # kinda like in `Payload`
        pass

@dataclass(init=True)
class SearchResourceConfig(ResourceConfig):
    """Configuration for search resources"""
    protocol: Protocol = field(default_factory=lambda: Protocol(ProtocolType.REST, RequestMethod.GET))
    payload: Payload = field(default_factory=Payload)
    oncall: bool = False
    adaptercfg: t.Optional[(RESTConfig | AlgoliaConfig | GQLConfig)] = None
    # potentially other configs

    @classmethod
    def FromResourceConfig(cls, cfg: ResourceConfig, **kwargs) -> 'SearchResourceConfig':
        return cls(
            name=cfg.name,
            path=cfg.path,
            methods=cfg.methods,
            children=cfg.children,
            parent=cfg.parent,
            protocol=kwargs.get('protocol', Protocol(ProtocolType.REST, RequestMethod.GET)),
            payload=kwargs.get('payload', Payload()),
            oncall=kwargs.get('oncall', False),
            adaptercfg=kwargs.get('adaptercfg', None)
        )



"""
Now supports:
    query = Parameter(name="q")
    hits = Parameter(name="per_page")

    # All these work:
    payload = Payload(query, hits)
    payload = Payload({'query': query, 'hits': hits})
    payload = Payload({'query': 'q', 'hits': 'per_page'})
    payload = Payload('query', 'hits')
    payload = Payload(query='q', hits='per_page')
"""
