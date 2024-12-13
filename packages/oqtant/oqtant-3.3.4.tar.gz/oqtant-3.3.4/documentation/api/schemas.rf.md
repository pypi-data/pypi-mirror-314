<!-- markdownlint-disable -->

<a href="../../oqtant/schemas/rf.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `schemas.rf`






---

<a href="../../oqtant/schemas/rf.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ConversionError`








---

<a href="../../oqtant/schemas/rf.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `RfSequence`
A class that represents a sequence of radio frequency powers/frequencies in time 


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

<a href="../../oqtant/schemas/rf.py#L57"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `from_input`

```python
from_input(rf_evaporation: 'RfEvaporation') → RfSequence
```

Method to create a RfSequence object using the input values of a job 



**Args:**
 
 - <b>`rf_evaporation`</b> (bert_schemas.job.RfEvaporation):  The input values 



**Returns:**
 
 - <b>`RfSequence`</b>:  A new RfSequence object created using the input data 

---

<a href="../../oqtant/schemas/rf.py#L69"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_frequencies`

```python
get_frequencies(times: 'list[float]') → list[float]
```

Method to calculate the RF evaporation frequencies of a RfSequence object at the specified times 



**Args:**
 
 - <b>`times`</b> (list[float]):  The times, in ms, at which the RF frequencies are calculated 



**Returns:**
 
 - <b>`list[float]`</b>:  The calculated frequencies, in MHz, at the specified times 

---

<a href="../../oqtant/schemas/rf.py#L85"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_powers`

```python
get_powers(times: 'list[float]') → list[float]
```

Method to calculate the RF evaporation powers at of a RfSequence object at the specified times 



**Args:**
 
 - <b>`times`</b> (list[float]):  The times, in ms, at which the RF powers are calculated 



**Returns:**
 
 - <b>`list[float]`</b>:  The RF powers, in mW, at the specified times 

---

<a href="../../oqtant/schemas/rf.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `new`

```python
new(
    times: 'list[float]' = [0],
    powers: 'list[float]' = [0],
    frequencies: 'list[float]' = [0],
    interpolation: 'InterpolationType' = 'LINEAR'
) → RfSequence
```

Method to create a new RfSequence object 



**Args:**
 
 - <b>`times`</b> (list[float], optional):  List of times, in ms 
 - <b>`powers`</b> (list[float], optional):  List of powers, in MHz 
 - <b>`frequencies`</b> (list[float], optional):  List of powers, mW 
 - <b>`interpolation`</b> (bert_schemas.job.InterpolationType, optional):  Interpolation type of the RF sequence 



**Returns:**
 
 - <b>`RfSequence`</b>:  A new RfSequence object 


---

<a href="../../oqtant/schemas/rf.py#L97"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `RfEvap`
A class that represents the forced RF evaporation that cools atoms to quantum degeneracy. 


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

<a href="../../oqtant/schemas/rf.py#L126"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `from_input`

```python
from_input(rf_evaporation: 'RfEvaporation') → RfEvap
```

Method to create a RfEvap object using the input values of a job 



**Args:**
 
 - <b>`rf_evaporation`</b> (bert_schemas.job.RfEvaporation):  The input values 



**Returns:**
 
 - <b>`RfEvap`</b>:  A new RfEvap object created using the input data 

---

<a href="../../oqtant/schemas/rf.py#L69"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_frequencies`

```python
get_frequencies(times: 'list[float]') → list[float]
```

Method to calculate the RF evaporation frequencies of a RfSequence object at the specified times 



**Args:**
 
 - <b>`times`</b> (list[float]):  The times, in ms, at which the RF frequencies are calculated 



**Returns:**
 
 - <b>`list[float]`</b>:  The calculated frequencies, in MHz, at the specified times 

---

<a href="../../oqtant/schemas/rf.py#L85"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_powers`

```python
get_powers(times: 'list[float]') → list[float]
```

Method to calculate the RF evaporation powers at of a RfSequence object at the specified times 



**Args:**
 
 - <b>`times`</b> (list[float]):  The times, in ms, at which the RF powers are calculated 



**Returns:**
 
 - <b>`list[float]`</b>:  The RF powers, in mW, at the specified times 

---

<a href="../../oqtant/schemas/rf.py#L100"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `new`

```python
new(
    times: 'list[float]' = [0],
    powers: 'list[float]' = [0],
    frequencies: 'list[float]' = [0],
    interpolation: 'InterpolationType' = 'LINEAR'
) → RfEvap
```

Method to create a new RfEvap object 



**Args:**
 
 - <b>`times`</b> (list[float], optional):  List of times, in ms 
 - <b>`powers`</b> (list[float], optional):  List of powers, in MHz 
 - <b>`frequencies`</b> (list[float], optional):  List of powers, mW 
 - <b>`interpolation`</b> (bert_schemas.job.InterpolationType, optional):  Interpolation type of the RF evaporation 



**Returns:**
 
 - <b>`RfEvap`</b>:  A new RfEvap object 


---

<a href="../../oqtant/schemas/rf.py#L154"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `RfShield`
A class that represents an RF shield (at fixed frequency and power) being applied during the 'experiment' phase/stage. 


---

#### <kbd>property</kbd> frequency

Property to get the frequency value of a RfShield object 



**Returns:**
 
 - <b>`float`</b>:  The shield's frequency, in MHz 

---

#### <kbd>property</kbd> lifetime

Property to get the lifetime value of a RfShield object 



**Returns:**
 
 - <b>`float`</b>:  The amount of time, in ms, that the shield will exist 

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

#### <kbd>property</kbd> power

Property to get the power value of a RfShield object 



**Returns:**
 
 - <b>`float`</b>:  The shield's power, in mW 



---

<a href="../../oqtant/schemas/rf.py#L173"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `cross_validate`

```python
cross_validate() → RfShield
```





---

<a href="../../oqtant/schemas/rf.py#L258"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `frequencies`

```python
frequencies(times: 'list[float]') → list[float]
```

Method to generate a list of frequencies using the provided list of times 



**Args:**
 
 - <b>`times`</b> (list[float]):  The times, in ms, at which the frequencies are generated 



**Returns:**
 
 - <b>`list`</b> (float):  The calculated frequencies, in MHz, at the specified times 

---

<a href="../../oqtant/schemas/rf.py#L220"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `from_input`

```python
from_input(rf_evaporation: 'RfEvaporation') → RfShield
```

Method to create a RfShield object using the input values of a job 



**Args:**
 
 - <b>`rf_evaporation`</b> (bert_schemas.job.RfEvaporation):  The input values 



**Returns:**
 
 - <b>`RfShield`</b>:  A new RfShield object created using the input data 

---

<a href="../../oqtant/schemas/rf.py#L194"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `new`

```python
new(
    lifetime: 'float',
    frequency: 'float',
    power: 'float',
    interpolation: 'InterpolationType' = 'LINEAR'
) → RfShield
```

Method to create a new RfShield object 



**Args:**
 
 - <b>`lifetime`</b> (float):  Lifetime of the shield, in ms 
 - <b>`frequency`</b> (float | None):  Frequency of the shield, in MHz 
 - <b>`power`</b> (float | None):  Power of the shield, in mW 
 - <b>`interpolation`</b> (bert_schemas.job.InterpolationType, optional):  Interpolation type of the shield 



**Returns:**
 
 - <b>`RfShield`</b>:  A new RfShield object 

---

<a href="../../oqtant/schemas/rf.py#L278"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `powers`

```python
powers(times: 'list[float]') → list[float]
```

Method to generate a list of powers using the provided list of times 



**Args:**
 
 - <b>`times`</b> (list[float]):  The times, in ms, at which the powers are generated 



**Returns:**
 
 - <b>`list`</b> (float):  The calculated powers, in mW, at the specified times 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
