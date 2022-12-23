import json

from dotwiz import DotWiz
from util import get_guppy_service

import logging
logger = logging.getLogger('dash')


def get_observations(variables={"filter": {"AND": []}}):
    """Query histogram on patient_id to get all unique patients
    @type variables: object graphql filter object
    @return list of patient_id strings
    """
    query = """
        query ($filter: JSON) {
          observation(accessibility: all, offset: 0, first: 20, filter: $filter) {
            patient_id
            category
            code_display
            valueQuantity_value
            valueQuantity_unit
            valueCodeableConcept_coding_0_display
            valueString
            component_0_code_coding_0_display
            component_0_valueQuantity_value
            component_0_valueQuantity_unit
            component_0_valueCodeableConcept_coding_0_code
            component_1_code_coding_0_display
            component_1_valueQuantity_value
            component_1_valueQuantity_unit
            component_1_valueCodeableConcept_coding_0_code
            valueBoolean
          }
          _aggregation {
            observation(filter: $filter, accessibility: all) {
              _totalCount
            }
          }
        }
  
    """
    guppy_service = get_guppy_service()
    data = guppy_service.graphql_query(query, variables=variables)['data']
    return DotWiz(data)


def get_observation_histograms(dot_notation=True, variables={"filter": {"AND": []}}):
    """Fetch histogram of counts for all observations.
    @param variables: a graphql filter
    @type dot_notation: bool render results as a lightweight class
    """

    histogram_query = """
    query ($filter: JSON) {
      _aggregation {
        observation(filter: $filter, filterSelf: false, accessibility: all) {
          category {
            histogram {
              key
              count
            }
          }
          encounter_type {
            histogram {
              key
              count
            }
          }
          code_display {
            histogram {
              key
              count
            }
          }
          project_id {
            histogram {
              key
              count
            }
          }
        }
      }
    }

    
    """
    guppy_service = get_guppy_service()
    data = guppy_service.graphql_query(histogram_query, variables=variables)['data']
    if dot_notation:
        return DotWiz(data)
    return data


def get_patient_ids(dot_notation=True, variables={"filter": {"AND": []}, "sort": []}):
    """Fetch patient ids first 10000 for filter.
    @param variables: a graphql filter and sort
    @type dot_notation: bool render results as a lightweight class"""
    query = """
        query ($sort: JSON,$filter: JSON,) {
            observation (accessibility: all, offset: 0, first: 10000, , sort: $sort, filter: $filter,) {
                id, patient_id
            }
            _aggregation {
              patient (filter: $filter, accessibility: all) {
                _totalCount
              }
            }
        }    
    """
    guppy_service = get_guppy_service()
    data = guppy_service.graphql_query(query, variables=variables)['data']
    return DotWiz(data)
