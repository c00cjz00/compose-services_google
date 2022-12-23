from abc import ABC
import time
from typing import Dict, List

from dotwiz import DotWiz
from gen3.query import Gen3Query
import yaml
from pprint import pprint
import copy


class GuppyVertex:
    """Represents a Vertex (index)."""
    name: str
    """The name of the Vertex."""
    graphql: Dict[str, str]
    """Keyed dictionary of graphql queries [aggregation,row,keys]."""
    guppy_service: Gen3Query
    """Authorized, initialized query helper."""

    def __init__(self, name, graphql, guppy_service):
        """ """
        self.name = name
        self.graphql = graphql
        self.guppy_service = guppy_service

    def aggregation(self, variables: object = {"filter": {"AND": []}, "sort": []}) -> Dict:
        """Return aggregations.
        @param variables:  graphql variables
        """
        data = self.guppy_service.graphql_query(self.graphql['aggregation'], variables=variables)['data']
        return DotWiz(data)

    def rows(self, variables: object = {"filter": {"AND": []}, "sort": []}) -> Dict:
        """Return page of rows.
        @param variables:  graphql variables
        """
        data = self.guppy_service.graphql_query(self.graphql['rows'], variables=variables)['data']
        return DotWiz(data)

    def keys(self, variables: object = {"filter": {"AND": []}, "sort": []}) -> Dict:
        """Return all the keys.
        @param variables:  graphql variables
        """
        keys_ = self.guppy_service.raw_data_download(
            data_type=self.name,
            fields=self.graphql['keys']['fields'],
            accessibility='all',
            filter_object=variables['filter']
        )
        return keys_


class GuppyGraph:
    """Traverses queries across several Vertices (indexes)."""

    vertices: Dict[str, GuppyVertex]
    """Dictionary of vertices."""

    keys: Dict[str, List[str]]
    """Dictionary of keys."""

    variables: Dict[str, object]
    """Dictionary of graphql query ."""

    def __init__(self, guppy_service: Gen3Query, config_path: str):
        self.guppy_service = guppy_service
        with open(config_path) as config:
            self.config = yaml.load(config, yaml.SafeLoader)
        self.vertices = {}
        for name, vertex_config in self.config['vertices'].items():
            self.vertices[name] = GuppyVertex(name, vertex_config['queries'], guppy_service)
        self.variables = {}
        self.keys = {}

    def query(self, vertex_name: str,  variables: object = None, debug=False) -> List[Dict]:
        start_time = time.time()

        if vertex_name not in self.vertices:
            raise Exception(f"Unknown {vertex_name}")

        inject_keys = True
        if vertex_name == 'patient' and variables:
            inject_keys = False

        # initialize filter variables
        get_keys = True
        if not variables:
            variables = copy.deepcopy(dict(self.config['variables']['default']))
            print('default variables', variables)
            get_keys = False
        self.variables[vertex_name] = variables

        # do we need to inject keys?
        key_name = self.config['vertices'][vertex_name]['keys']['inbound']['key_name']
        property_name = self.config['vertices'][vertex_name]['keys']['inbound']['property']
        if inject_keys and key_name in self.keys and len(self.keys[key_name]) > 0:
            # TODO - do we need to clear any occurrence of property_name out of AND clause first?
            print('injecting', {
                "IN": {property_name: len(self.keys[key_name])}
            },
                  f'keys into {vertex_name} from {key_name}  sample: {self.keys[key_name][:10]}')

            variables['filter']['AND'].append({
                "IN": {property_name: self.keys[key_name]}
            })

        # if there is a user specified filter, retrieve the keys
        keys = []
        if get_keys:
            key_name = self.config['vertices'][vertex_name]['keys']['outbound']['key_name']
            property_name = self.config['vertices'][vertex_name]['keys']['outbound']['property']
            keys = self.vertices[vertex_name].keys(variables=variables)
            self.keys[key_name] = list(set([k[property_name] for k in keys]))
            print('get_keys',  vertex_name, key_name, len(self.keys[key_name]))

        if debug:
            pprint(variables)

        results = [
            self.vertices[vertex_name].aggregation(variables=variables),
            self.vertices[vertex_name].rows(variables=variables),
            keys
        ]
        end_time = time.time()
        time_lapsed = end_time - start_time
        print(f'query {vertex_name} took', time_lapsed)
        return results
