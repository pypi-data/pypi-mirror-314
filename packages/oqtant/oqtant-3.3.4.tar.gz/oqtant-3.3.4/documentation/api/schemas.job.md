<!-- markdownlint-disable -->

<a href="../../oqtant/schemas/job.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `schemas.job`




**Global Variables**
---------------
- **SIG_ABS**

---

<a href="../../oqtant/schemas/job.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_keys`

```python
print_keys(subject: Any, indent: int = 0, drill_lists: bool = False) → None
```

Print the keys of a nested dictionary or list 



**Args:**
 
 - <b>`subject`</b> (Any):  The subject to print the keys of 
 - <b>`indent`</b> (int, optional):  The number of spaces to indent. Defaults to 0 
 - <b>`drill_lists`</b> (bool, optional):  Whether to drill into lists. Defaults to False 


---

<a href="../../oqtant/schemas/job.py#L47"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `OqtantJob`
A class that represents a job submitted to Oqtant 


---

#### <kbd>property</kbd> formatted_time_submit

Property to format the job submit datetime and ensure it is in caller's local timezone 



**Returns:**
 
 - <b>`str`</b>:  The formatted datetime string 

---

#### <kbd>property</kbd> id

Property to get the id of an OqtantJob object 



**Returns:**
 
 - <b>`uuid.UUID`</b>:  The id of the OqtantJob object 

---

#### <kbd>property</kbd> input

Property to get the input values for the current run of an OqtantJob 



**Returns:**
 
 - <b>`bert_schemas.job.InputValues`</b>:  The input values for the current run 

---

#### <kbd>property</kbd> input_fields

Property to print out all of the input fields for an OqtantJob 

---

#### <kbd>property</kbd> job_type





---

#### <kbd>property</kbd> lifetime

Property to get the lifetime value for the current run 



**Returns:**
 
 - <b>`int`</b>:  The lifetime value for the current run 

---

#### <kbd>property</kbd> model_extra

Get extra fields set during validation. 



**Returns:**
  A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`. 

---

#### <kbd>property</kbd> model_fields_set

Returns the set of fields that have been explicitly set on this model instance. 



**Returns:**
  A set of strings representing the fields that have been set,  i.e. that were not filled from defaults. 

---

#### <kbd>property</kbd> run

Property to get the current run value for the job's input 



**Returns:**
 
 - <b>`int`</b>:  The current run value for the job's input 

---

#### <kbd>property</kbd> truncated_name

Property to truncate a job's name 



**Returns:**
 
 - <b>`str`</b>:  The truncated job name 



---

<a href="../../oqtant/schemas/job.py#L134"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `add_notes_to_input`

```python
add_notes_to_input(notes: str) → None
```

Method to add notes to the current run 



**Args:**
 
 - <b>`notes`</b> (str):  The notes to add to the input 

---

<a href="../../oqtant/schemas/job.py#L84"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `format_datetime`

```python
format_datetime(datetime_value: str | datetime) → str
```

Method to format any datetime and ensure it is in caller's local timezone 



**Args:**
 
 - <b>`datetime_value`</b> (str | datetime.datetime):  The datetime value to format 



**Returns:**
 
 - <b>`str`</b>:  The formatted datetime string 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
