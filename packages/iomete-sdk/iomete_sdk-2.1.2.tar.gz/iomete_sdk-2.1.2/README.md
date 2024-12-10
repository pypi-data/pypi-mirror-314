# IOMETE SDK

This is the IOMETE SDK for Python. 
It provides convenient access to the IOMETE API from applications written in the Python language.

## Installation

Install the package with:

```bash
pip install iomete-sdk
```

## Usage - Spark Job API

### Import and initialize the client
```python
from iomete_sdk.spark import SparkJobApiClient
from iomete_sdk.api_utils import ClientError

HOST = "<YOUR_DATAPLANE_HOST>" # https://dataplane-endpoint.example.com
API_KEY = "<YOU_IOMETE_API_KEY>"

job_client = SparkJobApiClient(
    host=HOST,
    api_key=API_KEY,
)
```

### Create a new job
```python
response = job_client.create_job(payload={
        "name": "job-name",
        "namespace": "k8s-namespace",
        "jobUser": "job-user",
        "jobType": "MANUAL/SCHEDULED/STREAMING",
        "template": {
            "applicationType": "python",
            "image": f"iomete/spark-py:3.5.3-v1",
            "mainApplicationFile": "path/to/job.py",
            "configMaps": [{
                "key": "application.conf",
                "content": "[SELECT 1]",
                "mountPath": "/etc/configs"
            }],
            "deps": {
                "pyFiles": ["path/to/dependencies.zip"]
            },
            "instanceConfig": {
                "singleNodeDeployment": False, "driverType": "driver-x-small",
                "executorType": "exec-x-small", "executorCount": 1
            },
            "restartPolicy": {"type": "Never"},
            "maxExecutionDurationSeconds": "max-execution-duration",
            "volumeId": "volume-id",
        }
    })

job_id = response["id"]
```

### Get jobs
```python
response = job_client.get_jobs()
```

### Get job
```python
response = job_client.get_job(job_id=job_id)
```

### Update job
```python
response = job_client.update_job(job_id=job_id, payload=updated_payload)
```

### Delete job
```python
response = job_client.delete_job(job_id=job_id)
```


### Submit job run
```python
response = job_client.submit_job_run(job_id=job_id, payload={})
```

### Cancel job run
```python
response = job_client.cancel_job_run(job_id=job_id, run_id=run_id)
```

### Get Job Runs
```python
response = job_client.get_job_runs(job_id=job_id)
```

### Get Job Run
```python
response = job_client.get_job_run(job_id=job_id, run_id=run_id)
```

### Get Job Run Logs
```python
response = job_client.get_job_run_logs(job_id=job_id, run_id=run_id, time_range="5m")
```
**Supported Time Range:** 5m, 15m, 30m, 1h, 3h, 6h, 12h, 24h, 2d, 7d, 14d, 30d 

### Get Job Run Metrics
```python
response = job_client.get_job_run_metrics(job_id=job_id, run_id=run_id)
```



