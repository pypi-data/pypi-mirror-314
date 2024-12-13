<!-- markdownlint-disable -->

<a href="../../oqtant/oqtant_client.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `oqtant_client`




**Global Variables**
---------------
- **TYPE_CHECKING**
- **barrier_manipulator_job**
- **ultracold_matter_job**

---

<a href="../../oqtant/oqtant_client.py#L759"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_oqtant_client`

```python
get_oqtant_client(token: 'str') → OqtantClient
```

Method to create a new OqtantClient instance. 



**Args:**
 
 - <b>`token`</b> (str):  The auth0 token required for interacting with the Oqtant REST API 



**Returns:**
 
 - <b>`OqtantClient`</b>:  Authenticated instance of OqtantClient 


---

<a href="../../oqtant/oqtant_client.py#L774"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_client`

```python
get_client(port: 'int' = 8080) → OqtantClient
```

Method to get both an authentication token and an instance of OqtantClient 



**Args:**
 
 - <b>`port`</b> (int, optional):  Specific port to run the authentication server on 



**Returns:**
 
 - <b>`OqtantClient`</b>:  An authenticated instance of OqtantClient 


---

<a href="../../oqtant/oqtant_client.py#L49"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `OqtantClient`
Python class for interacting with Oqtant This class contains tools for: 
    - Accessing all of the functionality of the Oqtant Web App (https://oqtant.infleqtion.com) 
        - BARRIER (Barrier Manipulator) jobs 
        - BEC (Ultracold Matter) jobs 
    - Building parameterized (i.e. optimization) experiments using QuantumMatter 
    - Submitting and retrieve results How Oqtant works: 
    - Instantiate a QuantumMatterFactory and log in with your Oqtant account 
    - Create QuantumMatter objects with the QuantumMatterFactory 
        - 1D parameter sweeps are supported 
    - Submit the QuantumMatter to Oqtant to be run on the hardware in a FIFO queue 
        - Once submitted a job is created and associated with the QuantumMatter object 
    - Retrieve the results of the job from Oqtant into the QuantumMatter object 
        - These results are available in future python sessions 
    - Extract, visualize, and analyze the results Need help? Found a bug? Contact oqtant@infleqtion.com for support. Thank you! 

<a href="../../oqtant/oqtant_client.py#L69"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(settings, token, debug: 'bool' = False)
```






---

#### <kbd>property</kbd> external_user_id







---

<a href="../../oqtant/oqtant_client.py#L374"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `cancel_job`

```python
cancel_job(job_id: 'str') → None
```

Method to cancel a single job with the Oqtant REST API 



**Args:**
 
 - <b>`job_id`</b> (str):  The job id of the job to cancel 

---

<a href="../../oqtant/oqtant_client.py#L739"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `check_version`

```python
check_version() → bool
```

Method to compare the currently installed version of Oqtant with the latest version in PyPi and will raise a warning if it is older 



**Returns:**
 
 - <b>`bool`</b>:  True if current version is latest, False if it is older 

---

<a href="../../oqtant/oqtant_client.py#L113"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `convert_matter_to_job`

```python
convert_matter_to_job(matter: 'QuantumMatter') → OqtantJob | None
```

Method to convert a QuantumMatter object to an OqtantJob object 



**Args:**
 
 - <b>`matter`</b> (oqtant.schemas.quantum_matter.QuantumMatter):  The QuantumMatter object to be converted 



**Returns:**
 
 - <b>`oqtant.schemas.job.OqtantJob`</b>:  The resulting OqtantJob object 

---

<a href="../../oqtant/oqtant_client.py#L292"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_job`

```python
create_job(
    name: 'str',
    job_type: 'JobType',
    runs: 'int' = 1,
    job: 'dict | None' = None
) → OqtantJob
```

Method to create an instance of OqtantJob. When not providing a dictionary of job data this method will return an OqtantJob instance containing predefined input data based on the value of job_type and runs. If a dictionary is provided an OqtantJob instance will be created using the data contained within it. 



**Args:**
 
 - <b>`name`</b> (str):  The name of the job to be created 
 - <b>`job_type`</b> (bert_schemas.job.JobType):  The type of job to be created 
 - <b>`runs`</b> (int):  The number of runs to include in the job 
 - <b>`job`</b> (dict | None, optional):  Dictionary of job inputs to use instead of the defaults 



**Returns:**
 
 - <b>`oqtant.schemas.job.OqtantJob`</b>:  an OqtantJob instance of the provided dictionary or predefined input data 

---

<a href="../../oqtant/oqtant_client.py#L392"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `delete_job`

```python
delete_job(job_id: 'str') → None
```

Method to delete a single job with the Oqtant REST API 



**Args:**
 
 - <b>`job_id`</b> (str):  The job id of the job to delete 

---

<a href="../../oqtant/oqtant_client.py#L274"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `generate_oqtant_job`

```python
generate_oqtant_job(job: 'dict') → OqtantJob
```

Method to generate an instance of OqtantJob from the provided dictionary that contains the job details and input. Will validate the values and raise an informative error if any violations are found 



**Args:**
 
 - <b>`job`</b> (dict):  Dictionary containing job details and input 



**Returns:**
 
 - <b>`oqtant.schemas.job.OqtantJob`</b>:  an OqtantJob instance containing the details and input from the  provided dictionary 

---

<a href="../../oqtant/oqtant_client.py#L238"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_job`

```python
get_job(job_id: 'str', run: 'int' = 1) → OqtantJob
```

Method to get an OqtantJob from the Oqtant REST API. This will always be a targeted query for a specific run. If the run is omitted then this will always return the first run of the job. Will return results for any job regardless of it's status 



**Args:**
 
 - <b>`job_id`</b> (str):  This is the external_id of the job to fetch 
 - <b>`run`</b> (int, optional):  The run to target, this defaults to the first run if omitted 



**Returns:**
 
 - <b>`oqtant.schemas.job.OqtantJob`</b>:  An OqtantJob instance with the values of the job queried 

---

<a href="../../oqtant/oqtant_client.py#L627"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_job_limits`

```python
get_job_limits(show_results: 'bool' = False) → dict
```

Method to get job limits from the Oqtant REST API 



**Args:**
 
 - <b>`show_results`</b> (bool, optional):  Flag to print out the results 



**Returns:**
 
 - <b>`dict`</b>:  Dictionary of job limits 

---

<a href="../../oqtant/oqtant_client.py#L673"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_queue_status`

```python
get_queue_status(
    job_type: 'JobType | None' = None,
    name: 'JobName | None' = None,
    submit_start: 'str | None' = None,
    submit_end: 'str | None' = None,
    note: 'str | None' = None,
    limit: 'int' = 50,
    include_complete: 'bool' = False,
    show_results: 'bool' = False
) → list
```

Method to get the queue status of jobs submitted by the authenticated user 



**Args:**
 
 - <b>`job_type`</b> (bert_schemas.job.JobType | None, optional):  The type of jobs to filter results on 
 - <b>`name`</b> (bert_schemas.job.JobName | None, optional):  The name of the job(s) to filter results on 
 - <b>`submit_start`</b> (str, optional):  The earliest job submission date to filter results on 
 - <b>`submit_end`</b> (str, optional):  The latest job submission date to filter results on 
 - <b>`note`</b> (str | None, optional):  The notes value to filter results on 
 - <b>`limit`</b> (int, optional):  The limit on the number of results to be returned 
 - <b>`include_complete`</b> (bool, optional):  Flag to include completed jobs in results 
 - <b>`show_results`</b> (bool, optional):  Flag to print out the results 



**Returns:**
 
 - <b>`list[dict]`</b>:  List of jobs that matched the provided query parameters 

---

<a href="../../oqtant/oqtant_client.py#L603"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_raw_images`

```python
get_raw_images(job_id: 'str') → list
```

Method to get raw images from the Oqtant REST API 



**Args:**
 
 - <b>`job_id`</b> (str):  The external_id of the job to fetch 



**Returns:**
 
 - <b>`dict`</b>:  Dictionary of raw images 

---

<a href="../../oqtant/oqtant_client.py#L142"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_sim_result`

```python
get_sim_result(sim: 'Simulator', image_type: 'ImageType') → Simulator
```

Method to get the result of a simulation 



**Args:**
 
 - <b>`sim`</b> (oqtant.simulator.Simulator):  The Simulator object 



**Returns:**
 
 - <b>`oqtant.simulator.Simulator`</b>:  The Simulator object 

---

<a href="../../oqtant/oqtant_client.py#L576"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_job_from_file`

```python
load_job_from_file(file_path: 'str', refresh: 'bool' = True) → OqtantJob
```

Method to load an OqtantJob instance from a file. Will refresh the job data from the Oqtant REST API by default 



**Args:**
 
 - <b>`file_path`</b> (str):  The full path to the file to read 
 - <b>`refresh`</b> (bool, optional):  Flag to refresh the job data from Oqtant 



**Returns:**
 
 - <b>`OqtantJob`</b>:  An OqtantJob instance of the loaded job 

---

<a href="../../oqtant/oqtant_client.py#L410"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run_jobs`

```python
run_jobs(
    job_list: 'list[OqtantJob]',
    track_status: 'bool' = False,
    write: 'bool' = False
) → list[str]
```

Method to submit a list of OqtantJobs to the Oqtant REST API. This method provides some optional functionality to alter how it behaves. Providing it with an argument of track_status=True will make it wait and poll the Oqtant REST API until all jobs in the list have completed. Providing it with and argument of write=True  will make it write the results of the jobs to file when they complete (only applies when the track_status argument is True) 



**Args:**
 
 - <b>`job_list`</b> (list[oqtant.schemas.job.OqtantJob]):  The list of OqtantJob instances to submit for processing 
 - <b>`track_status`</b> (bool, optional):  Flag to return immediately or wait and poll until all jobs have completed 
 - <b>`write`</b> (bool, optional):  Flag to write job results to file 



**Returns:**
 
 - <b>`list[str]`</b>:  List of the external_id(s) returned for each submitted job in job_list 

---

<a href="../../oqtant/oqtant_client.py#L444"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `search_jobs`

```python
search_jobs(
    job_type: 'JobType | None' = None,
    name: 'JobName | None' = None,
    submit_start: 'str | None' = None,
    submit_end: 'str | None' = None,
    notes: 'str | None' = None,
    limit: 'int' = 100,
    show_results: 'bool' = False
) → list[dict]
```

Method to submit a query to the Oqtant REST API to search for jobs that match the provided criteria. The search results will be limited to jobs that meet your Oqtant account access 



**Args:**
 
 - <b>`job_type`</b> (bert_schemas.job.JobType | None, optional):  The type of the jobs to search for 
 - <b>`name`</b> (bert_schemas.job.JobName | None, optional):  The name of the job to search for 
 - <b>`submit_start`</b> (str | None, optional):  The earliest submit date of the jobs to search for 
 - <b>`submit_start`</b> (str | None, optional):  The latest submit date of the jobs to search for 
 - <b>`notes`</b> (str | None, optional):  The notes of the jobs to search for 
 - <b>`limit`</b> (int, optional):  The limit for the number of jobs returned (max: 100) 
 - <b>`show_results`</b> (bool, optional):  Flag to print out the results of the search 



**Returns:**
 
 - <b>`list[dict]`</b>:  A list of jobs matching the provided search criteria 

---

<a href="../../oqtant/oqtant_client.py#L667"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show_job_limits`

```python
show_job_limits() → None
```

Method to print out job limit information Wrapper for OqtantClient.get_job_results 

---

<a href="../../oqtant/oqtant_client.py#L733"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show_queue_status`

```python
show_queue_status(*args, **kwargs) → None
```

Method to show queue status information Wrapper for OqtantClient.get_queue_status 

---

<a href="../../oqtant/oqtant_client.py#L177"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `submit`

```python
submit(
    matter: 'QuantumMatter',
    track: 'bool' = False,
    sim: 'bool' = False
) → str
```

Method to submit a QuantumMatter object for execution, returns the resulting job id 



**Args:**
 
 - <b>`matter`</b> (oqtant.schemas.quantum_matter.QuantumMatter):  The QuantumMatter object to submit for execution 
 - <b>`track`</b> (bool, optional):  Flag to track the status of the resulting job 
 - <b>`sim`</b> (bool, optional):  Flag to submit job as a simulation 



**Returns:**
 
 - <b>`str`</b>:  The Job ID of the submitted job 

---

<a href="../../oqtant/oqtant_client.py#L330"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `submit_job`

```python
submit_job(job: 'OqtantJob', write: 'bool' = False) → dict
```

Method to submit a single OqtantJob to the Oqtant REST API. Upon successful submission this method will return a dictionary containing the external_id of the job and it's position in the queue. Will write the job data to file when the write argument is True. 







**Args:**
 
 - <b>`job`</b> (oqtant.schemas.job.OqtantJob):  The OqtantJob instance to submit for processing 
 - <b>`write`</b> (bool, optional):  Flag to write job data to file 



**Returns:**
 
 - <b>`dict`</b>:  Dictionary containing the external_id of the job and it's queue position 

---

<a href="../../oqtant/oqtant_client.py#L195"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `submit_list_as_batch`

```python
submit_list_as_batch(
    matter_list: 'list[QuantumMatter]',
    track: 'bool' = False,
    name: 'str | None' = None,
    sim: 'bool' = False
) → QuantumMatter
```

Method to submit a list of QuantumMatter objects as a batch job for execution 



**Args:**
 
 - <b>`matter_list`</b> (list[oqtant.schemas.quantum_matter.QuantumMatter]):  The list of QuantumMatter objects to  submit as a single batch job 
 - <b>`track`</b> (bool, optional):  Whether to track the status of the job 
 - <b>`name`</b> (str | None, optional):  The name of the batch job. If None, the name of the first program will be used 
 - <b>`sim`</b> (bool):  If the user intended to submit a sim job as batch or not. Will throw an exception as we do not allow simulator jobs as batch. 

**Returns:**
 
 - <b>`str`</b>:  The ID of the submitted job 

---

<a href="../../oqtant/oqtant_client.py#L164"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `submit_sim`

```python
submit_sim(matter: 'QuantumMatter') → Simulator
```

Method to submit a QuantumMatter object for simulation 



**Args:**
 
 - <b>`matter`</b> (oqtant.schemas.quantum_matter.QuantumMatter):  A QuantumMatter object 



**Returns:**
 
 - <b>`oqtant.simulator.Simulator`</b>:  The Simulator object 

---

<a href="../../oqtant/oqtant_client.py#L506"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `track_jobs`

```python
track_jobs(pending_jobs: 'list[OqtantJob]', write: 'bool' = False) → None
```

Method that polls the Oqtant REST API with a list of OqtantJobs and waits until all of them have completed. Will output each job's status while it is polling and will output a message when all jobs have completed. When the write argument is True it will also write the jobs' data to file when they complete 



**Args:**
 
 - <b>`pending_jobs`</b> (list[oqtant.schemas.job.OqtantJob]):  List of OqtantJobs to track 
 - <b>`write`</b> (bool, optional):  Flag to write job results to file 

---

<a href="../../oqtant/oqtant_client.py#L547"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `write_job_to_file`

```python
write_job_to_file(
    job: 'OqtantJob',
    file_name: 'str | None' = None,
    file_path: 'str | None' = None
) → None
```

Method to write an OqtantJob instance to a file 



**Args:**
 
 - <b>`job`</b> (oqtant.schemas.job.OqtantJob):  The OqtantJob instance to write to file 
 - <b>`file_name`</b> (str | None, optional):  custom name of the file 
 - <b>`file_path`</b> (str | None, optional):  full path to the file to write, including  the name of the file 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
