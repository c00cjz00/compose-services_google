from gen3.auth import Gen3Auth
from gen3.query import Gen3Query

auth = Gen3Auth('https://aced-training.compbio.ohsu.edu', refresh_file='../Secrets/credentials.json')

from models.guppy_graph import GuppyGraph

gg = GuppyGraph(Gen3Query(auth), 'guppy_graph.config.yaml')

print("********* All")

aggregation, rows, keys = gg.query('patient')
patient_aggregations = aggregation._aggregation.patient
assert sorted(patient_aggregations.keys()) == ['_totalCount', 'extension_0_extension_1_valueString', 'gender',
                                               'project_id']
print("How many patients?", {}, patient_aggregations._totalCount, len(keys))
print("What are there races?", patient_aggregations['extension_0_extension_1_valueString'])
print(rows.keys())
print("Number of patients in 1st page", len(rows.patient), "Total number of patients",
      rows._aggregation.patient._totalCount)

aggregation, rows, keys = gg.query('observation')
observation_aggregations = aggregation._aggregation.observation
assert sorted(observation_aggregations.keys()) == ['_totalCount', 'category', 'code_display', 'encounter_type',
                                                   'project_id']
print("How many observation 'categories' do they have?", observation_aggregations['category'])
print("Number of observation in 1st page", len(rows.observation), "Total number of observations",
      rows._aggregation.observation._totalCount)

print("********* Female")

patient_filter = {
    "filter": {
        "AND": [
            {"IN": {"gender": ["female"]}}
        ]
    }
}

aggregation, rows, keys = gg.query('patient', patient_filter)
patient_aggregations = aggregation._aggregation.patient
assert sorted(patient_aggregations.keys()) == ['_totalCount', 'extension_0_extension_1_valueString', 'gender',
                                               'project_id']
print("How many patients do we have with 'female' gender?", patient_filter, patient_aggregations._totalCount, len(keys))
print("What are there races?", patient_aggregations['extension_0_extension_1_valueString'])
print(rows.keys())
print("Number of patients in 1st page", len(rows.patient), "Total number of patients",
      rows._aggregation.patient._totalCount)

aggregation, rows, keys = gg.query('observation')
observation_aggregations = aggregation._aggregation.observation
assert sorted(observation_aggregations.keys()) == ['_totalCount', 'category', 'code_display', 'encounter_type',
                                                   'project_id']
print("How many observation 'categories' do they have?", observation_aggregations['category'])
print("Number of observation in 1st page", len(rows.observation), "Total number of observations",
      rows._aggregation.observation._totalCount)

print("********* laboratory Observations for female patients")

observation_filter = {"filter": {"AND": [{"IN": {"category": ["laboratory"]}}]}}

# note we are querying observation first
aggregation, rows, keys = gg.query('observation', observation_filter)
observation_aggregations = aggregation._aggregation.observation
assert sorted(observation_aggregations.keys()) == ['_totalCount', 'category', 'code_display', 'encounter_type',
                                                   'project_id']
print("How many observation 'categories' do they have?", observation_aggregations['category'])
# print(json.dumps(observation_filter))
print("Number of observation in 1st page", len(rows.observation), "Total number of observations",
      rows._aggregation.observation._totalCount)
# print(rows)

# patient_filter = {"filter": {'AND': []}}

aggregation, rows, keys = gg.query('patient')
patient_aggregations = aggregation._aggregation.patient

assert sorted(patient_aggregations.keys()) == ['_totalCount', 'extension_0_extension_1_valueString', 'gender',
                                               'project_id']
print("How many patients do we have?", {}, patient_aggregations._totalCount, len(keys))
print("What are there races?", patient_aggregations['extension_0_extension_1_valueString'])
print(rows.keys())
print("Number of patients in 1st page", len(rows.patient), "Total number of patients",
      rows._aggregation.patient._totalCount)

print('************ specific patient id in HOP')

patient_filter = {
    "filter": {
        "AND": [
            {"IN": {"id": ["5c6f0976d356e5010020f7bf"]}}
        ]
    }
}

aggregation, rows, keys = gg.query('patient', patient_filter)
patient_aggregations = aggregation._aggregation.patient
assert sorted(patient_aggregations.keys()) == ['_totalCount', 'extension_0_extension_1_valueString', 'gender',
                                               'project_id']
print("How many patients do we have with '5c6f0976d356e5010020f7bf' id?", patient_filter,
      patient_aggregations._totalCount, len(keys))

observation_filter = {"filter": {'AND': []}}

aggregation, rows, keys = gg.query('observation', observation_filter)
print(observation_filter)
observation_aggregations = aggregation._aggregation.observation
assert sorted(observation_aggregations.keys()) == ['_totalCount', 'category', 'code_display', 'encounter_type',
                                                   'project_id']
print("How many observation 'categories' do they have?", observation_aggregations['category'])
print('Should be in HOP', len(observation_aggregations.project_id.histogram) == 1,
      observation_aggregations.project_id.histogram[0].key == 'aced-HOP')
# print(json.dumps(observation_filter))
print("Number of observation in 1st page", len(rows.observation), "Total number of observations",
      rows._aggregation.observation._totalCount)

print('************ specific patient id in Diabetes')

patient_filter = {
    "filter": {
        "AND": [
            {"IN": {"id": ['9e91eac2-9d48-5339-adab-5b097e340fae']}}
        ]
    }
}

aggregation, rows, keys = gg.query('patient', patient_filter)
patient_aggregations = aggregation._aggregation.patient
assert sorted(patient_aggregations.keys()) == ['_totalCount', 'extension_0_extension_1_valueString', 'gender',
                                               'project_id']
print("How many patients do we have with '9e91eac2-9d48-5339-adab-5b097e340fae' id?", patient_filter,
      patient_aggregations._totalCount, len(keys))

observation_filter = {"filter": {'AND': []}}

aggregation, rows, keys = gg.query('observation', observation_filter)
print(observation_filter)
observation_aggregations = aggregation._aggregation.observation
assert sorted(observation_aggregations.keys()) == ['_totalCount', 'category', 'code_display', 'encounter_type',
                                                   'project_id']
print("How many observation 'categories' do they have?", observation_aggregations['category'])
print('Should be in HOP', len(observation_aggregations.project_id.histogram) == 1,
      observation_aggregations.project_id.histogram[0].key == 'aced-Diabetes')
# print(json.dumps(observation_filter))
print("Number of observation in 1st page", len(rows.observation), "Total number of observations",
      rows._aggregation.observation._totalCount)
