
from dotwiz import DotWiz
from util import get_guppy_service

import logging
logger = logging.getLogger('dash')


def get_files(dot_notation=True, variables={"filter": {"AND": []}, "sort": []}):
    """Fetch histogram of counts for all projects.
    @param variables: a graphql filter and sort
    @type dot_notation: bool render results as a lightweight class"""
    query = """
        query ($sort: JSON,$filter: JSON,) {
            file (accessibility: all, offset: 0, first: 1000, , sort: $sort, filter: $filter,) {
                file_id  
                patient_id    
                file_category    
                file_name    
                file_size    
                object_id    
            }
            _aggregation {
              file (filter: $filter, accessibility: all) {
                _totalCount
              }
            }
        }    
    """
    guppy_service = get_guppy_service()
    data = guppy_service.graphql_query(query, variables=variables)['data']
    data = DotWiz(data)
    return [f for f in data.file]


def get_file_histograms(dot_notation=True, variables={"filter": {"AND": []}}):
    """Fetch histogram of counts for all projects.
    @param variables: a graphql filter
    @type dot_notation: bool render results as a lightweight class"""

    histogram_query = """
query ($filter: JSON,) {
    file (accessibility: all, offset: 0, first: 20, , filter: $filter,) {
      
    project_id
    

    patient_id
    

    patient_gender
    

    patient_disability_adjusted_life_years
    

    patient_ombCategory
    

    patient_ombCategory_detail
    

    patient_us_core_birthsex
    

    patient_quality_adjusted_life_years
    

    file_category
    

    file_name
    

    file_size
    

    object_id
    
    }
    _aggregation {
      file (filter: $filter, accessibility: all) {
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
