
from dotwiz import DotWiz
from util import get_guppy_service

import logging
logger = logging.getLogger('dash')


def get_patients(dot_notation=True, variables={"filter": {"AND": []}, "sort": []}):
    """Fetch histogram of counts for all projects.
    @param variables: a graphql filter and sort
    @type dot_notation: bool render results as a lightweight class"""
    query = """
        query ($sort: JSON,$filter: JSON,) {
            patient (accessibility: all, offset: 0, first: 1000, , sort: $sort, filter: $filter,) {
                id
                gender
                extension_0_extension_0_valueCoding_code
                extension_0_extension_1_valueString
                project_id                    
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


def get_patient_ids(dot_notation=True, variables={"filter": {"AND": []}, "sort": []}):
    """Fetch patient ids first 10000 for filter.
    @param variables: a graphql filter and sort
    @type dot_notation: bool render results as a lightweight class"""
    query = """
        query ($sort: JSON,$filter: JSON,) {
            patient (accessibility: all, offset: 0, first: 10000, , sort: $sort, filter: $filter,) {
                id
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



def get_patient_histograms(dot_notation=True, variables={"filter": {"AND": []}}):
    """Fetch histogram of counts for all projects.
    @param variables: a graphql filter
    @type dot_notation: bool render results as a lightweight class"""

    histogram_query = """
        query ($filter: JSON) {
          _aggregation {
            patient(filter: $filter, filterSelf: false, accessibility: all) {
              gender {
                histogram {
                  key
                  count
                }
              }
              extension_0_extension_1_valueString {
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
              },
              _totalCount
            }
          }
        }

    """
    guppy_service = get_guppy_service()
    data = guppy_service.graphql_query(histogram_query, variables=variables)['data']
    if dot_notation:
        return DotWiz(data)
    return data
