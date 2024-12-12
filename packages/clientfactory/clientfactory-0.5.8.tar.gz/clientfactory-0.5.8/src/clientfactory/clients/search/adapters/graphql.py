# ~/ClientFactory/src/clientfactory/clients/search/adapters/graphql.py
import enum, typing as t
from dataclasses import dataclass, field
from clientfactory.clients.search.adapters import Adapter

class GQLOps(enum.Enum): # operators
    EQ = "eq"
    GT = "gt"
    LT = "lt"
    GTE = "gte"
    LTE = "lte"
    IN = "in"
    CONTAINS = "contains"

@dataclass
class GQLConfig:
    operation: str = "search"  # Default operation name
    query: str = ""           # GraphQL query string
    filtermapping: dict = field(default_factory=dict)  # Custom filter field mappings

@dataclass
class GraphQL(Adapter):
    config: GQLConfig = field(default_factory=GQLConfig)

    def formatparams(self, params, **kwargs) -> dict:
        # Could add param transformation logic here
        return {"variables": params}

    def formatfilters(self, filters, **kwargs) -> dict:
        gqlfilters = {}
        for k, v in filters.items():
            if isinstance(v, dict):
                # Handle complex filters with operators
                # e.g., {"price": {"gt": 100}}
                gqlfilters[k] = v
            else:
                # Simple equality
                gqlfilters[k] = {"eq": v}
        return {"variables": {"filter": gqlfilters}}

    def formatpagination(self, page, hits, **kwargs) -> dict:
        return {"variables": {
            "page": page,
            "first": hits,
            # Could add optional offset/after cursor
            **({"after": kwargs["cursor"]} if "cursor" in kwargs else {})
        }}

    def formatsorting(self, field, order, **kwargs) -> dict:
        return {"variables": {
            "sort": {
                "field": field,
                "order": order.upper()
            }
        }}

    def formatall(self, **kwargs) -> dict:
        formatted = super().formatall(**kwargs)
        variables = {}

        # Handle both direct params and nested params
        params = kwargs.get('params', {})
        if isinstance(params, dict):
            variables.update(params)

        # Handle sorting specifically
        if 'sort' in kwargs and 'order' in kwargs:
            sort_params = self.formatsorting(kwargs['sort'], kwargs['order'])
            if 'variables' in sort_params:
                variables.update(sort_params['variables'])

        # Merge other formatted parameters
        for k, v in formatted.items():
            if isinstance(v, dict) and "variables" in v:
                variables.update(v["variables"])
            else:
                variables[k] = v

        return {
            "query": self.config.query,
            "operationName": self.config.operation,
            "variables": variables
        }
