import vertexai
from vertexai.tuning import sft

vertexai.init(project="mlops-501911", location="us-central1")

job_v1 = sft.SupervisedTuningJob("projects/588656205385/locations/us-central1/tuningJobs/4076595636659552256")
job_v2 = sft.SupervisedTuningJob("projects/588656205385/locations/us-central1/tuningJobs/883543500853870592")

print("v1 state:", job_v1.state)
print("v2 state:", job_v2.state)
print("v1 endpoint:", job_v1.tuned_model_endpoint_name)
print("v2 endpoint:", job_v2.tuned_model_endpoint_name)