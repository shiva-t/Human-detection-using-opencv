from google.cloud import datastore

datastore_client = datastore.Client()
task_key = datastore_client.key('Task',5634472569470976)
task_entity = datastore_client.get(task_key)
print(task_key)
print(task_entity)
print(task_entity['Done'])

