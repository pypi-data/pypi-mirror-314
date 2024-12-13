<!-- markdownlint-disable -->

<a href="../../oqtant/schemas/quantum_matter.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `schemas.quantum_matter`




**Global Variables**
---------------
- **TYPE_CHECKING**
- **DEFAULT_NAME**
- **TEMPERATURE_TO_EVAP_FREQUENCY**


---

<a href="../../oqtant/schemas/quantum_matter.py#L61"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `OqtantLogin`
OqtantLogin(access_token: 'str | None' = None) 

<a href="../../<string>"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(access_token: 'str | None' = None) → None
```









---

<a href="../../oqtant/schemas/quantum_matter.py#L66"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `QuantumMatter`
A class that represents user inputs to create and manipulate quantum matter 


---

#### <kbd>property</kbd> input

Property to get the job input values of a QuantumMatter object 



**Returns:**
 
 - <b>`bert_schemas.job.InputVales`</b>:  The job input values of the QuantumMatter object's current result 

---

#### <kbd>property</kbd> job_type

Property to get the job type of a submitted QuantumMatter object 



**Returns:**
 
 - <b>`bert_schemas.job.JobType`</b>:  The type of the job 

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

#### <kbd>property</kbd> rf_evaporation

Property to get the RF evaporation data of a QuantumMatter object 



**Returns:**
 
 - <b>`bert_schemas.job.RfEvaporation`</b>:  The RF evaporation values of the job's current result 

---

#### <kbd>property</kbd> run_count

Property to get the number of job runs for a submitted QuantumMatter object 



**Returns:**
 
 - <b>`int`</b>:  The total run number of the job 

---

#### <kbd>property</kbd> status

Property to get the job status of a submitted QuantumMatter object 



**Returns:**
 
 - <b>`bert_schemas.job.JobStatus`</b>:  The status of the job 

---

#### <kbd>property</kbd> time_complete

Property to get the time the current job was completed 



**Returns:**
 
 - <b>`str`</b>:  The time the current job was completed 

---

#### <kbd>property</kbd> time_start

Property to get the time the current job was run 



**Returns:**
 
 - <b>`str`</b>:  The time the current job was run 

---

#### <kbd>property</kbd> time_submit

Property to get the time the current job was submitted 



**Returns:**
 
 - <b>`str`</b>:  The time the current job was submitted 



---

<a href="../../oqtant/schemas/quantum_matter.py#L431"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `corrected_rf_power`

```python
corrected_rf_power(frequency_mhz: 'float', power_mw: 'float') → float
```

Method to calculate the corrected RF power based on the given frequency and power 



**Args:**
 
 - <b>`frequency_mhz`</b> (float):  The frequency in MHz 
 - <b>`power`</b> (float):  The power in mW 



**Returns:**
 
 - <b>`float`</b>:  The corrected RF power in mW 

---

<a href="../../oqtant/schemas/quantum_matter.py#L451"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `corrected_rf_powers`

```python
corrected_rf_powers(
    frequencies: 'list[float]',
    powers: 'list[float]'
) → list[float]
```

Method to calculate the corrected RF powers based on the given lists of frequencies and powers 



**Args:**
 
 - <b>`frequencies`</b> (list[float]):  The frequencies in MHz 
 - <b>`powers`</b> (list[float]):  The powers in mW 



**Returns:**
 
 - <b>`list[float]`</b>:  The corrected list of RF powers in mW 

---

<a href="../../oqtant/schemas/quantum_matter.py#L225"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `from_input`

```python
from_input(
    name: 'str',
    input: 'InputValues',
    note: 'JobNote | None' = None,
    client: 'OqtantClient | None' = None
) → QuantumMatter
```

Method to create a new QuantumMatter object using the input values of an existing job 



**Args:**
 
 - <b>`name`</b> (str):  Name of the quantum matter 
 - <b>`input`</b> (bert_schemas.job.InputValues):  The input values 
 - <b>`note`</b> (bert_schemas.job.JobNote | None):  The notes for the input, can be None 
 - <b>`client`</b> (oqtant.oqtant_client.OqtantClient | None, optional):  An instance of OqtantClient 



**Returns:**
 
 - <b>`QuantumMatter`</b>:  A new QuantumMatter object created using the input data 

---

<a href="../../oqtant/schemas/quantum_matter.py#L277"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `from_oqtant_job`

```python
from_oqtant_job(job: 'OqtantJob', client: 'OqtantClient') → QuantumMatter
```

Method to create a new QuantumMatter object using an existing OqtantJob 



**Args:**
 
 - <b>`job`</b> (oqtant.schemas.job.OqtantJob):  The OqtantJob object to create from 
 - <b>`client`</b> (oqtant.oqtant_client.OqtantClient):  An instance of OqtantClient 
 - <b>`run`</b> (int, optional):  The specific run to use 



**Returns:**
 
 - <b>`QuantumMatter`</b>:  A new QuantumMatter object created using the OqtantJob data 

---

<a href="../../oqtant/schemas/quantum_matter.py#L568"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_ideal_optical_potential`

```python
get_ideal_optical_potential(
    time: 'float',
    positions: 'list[float]'
) → list[float]
```

Method to calculate the "ideal" optical potential from constituent optical objects 



**Args:**
 
 - <b>`time`</b> (float):  time, in ms, for which the optical potential should be evaluated 
 - <b>`positions`</b> (list[float]):  positions, in microns, where potential should be evaluated 



**Returns:**
 
 - <b>`list[float]`</b>:  list of potential energies, in kHz, at the request time and positions 

---

<a href="../../oqtant/schemas/quantum_matter.py#L546"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_magnetic_potential`

```python
get_magnetic_potential(positions: 'list[float]') → list[float]
```

Method to calculate the magnetic potentials for a given set of positions 



**Args:**
 
 - <b>`positions`</b> (list[float]):  The positions at which to calculate the potentials 



**Returns:**
 
 - <b>`list[float]`</b>:  List of magnetic potentials in kHz corresponding to the given positions 

---

<a href="../../oqtant/schemas/quantum_matter.py#L588"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_potential`

```python
get_potential(
    time: 'float',
    positions: 'list[float]',
    include_magnetic: 'bool' = True
) → list[float]
```

Method to calculate the optical and magnetic potential at the given time for each position 



**Args:**
 
 - <b>`time`</b> (float):  The time at which to calculate the potential 
 - <b>`positions`</b> (list[float]):  The positions at which to calculate the potential 
 - <b>`include_magnetic`</b> (bool, optional):  Flag to include contributions from magnetic trap 

**Returns:**
 
 - <b>`list[float]`</b>:  List of potential energy corresponding to each request position 

---

<a href="../../oqtant/schemas/quantum_matter.py#L389"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_result`

```python
get_result(run: 'int | None' = None) → None
```

Method to get the results of a hardware job 



**Args:**
 
 - <b>`run`</b> (int, optional):  The specific run to get 

---

<a href="../../oqtant/schemas/quantum_matter.py#L356"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_sim_result`

```python
get_sim_result() → None
```

Method to get the results of a simulator job. Alerts the user if simulation results are invalid due to boundary collision. 

---

<a href="../../oqtant/schemas/quantum_matter.py#L88"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `model_post_init`

```python
model_post_init(*args) → None
```





---

<a href="../../oqtant/schemas/quantum_matter.py#L301"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `output_values_to_oqtant_output`

```python
output_values_to_oqtant_output(
    output_values: 'PlotOutput | NonPlotOutput'
) → OqtantPlotOutput | OqtantNonPlotOutput
```

Method to convert a completed job's output values to OqtantOutput 



**Args:**
 
 - <b>`output_values`</b> (PlotOutput|NonPlotOutput):   The output values to convert to OqtantPlotOutput 



**Returns:**
 (oqtant.schemas.output.OqtantPlotOutput | oqtant.schemas.output.OqtantNonPlotOutput): The converted output values 

---

<a href="../../oqtant/schemas/quantum_matter.py#L715"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show_barrier_dynamics`

```python
show_barrier_dynamics() → None
```

Method to plot the time dynamics of every Barrier object within a QuantumMatter object 

---

<a href="../../oqtant/schemas/quantum_matter.py#L750"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show_laser_pulse_timing`

```python
show_laser_pulse_timing(figsize=(6, 4)) → None
```

Method to plot the timing of a single terminator pulse in the experiment 



**Args:**
 
 - <b>`figsize (tuple, optional) `</b>:  Size of the output plot 

---

<a href="../../oqtant/schemas/quantum_matter.py#L610"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show_potential`

```python
show_potential(
    times: 'list[float]' = [0.0],
    xlimits: 'list[float]' = [-61.0, 61],
    ylimits: 'list[float]' = [-1.0, 101.0],
    include_ideal: 'bool' = False,
    include_magnetic: 'bool' = True,
    include_terminator: 'bool' = False
) → None
```

Method to plot the (optical) potential energy surface at the specified times 



**Args:**
 
 - <b>`times`</b> (list[float], optional):  The times for which to display the potential energy 
 - <b>`xlimits`</b> (list[float], optional):  The plot limits for the x axis 
 - <b>`ylimits`</b> (list[float], optional):  The plot limits for the y axis 
 - <b>`include_ideal`</b> (bool, optional):  Flag for including target potential in plot 
 - <b>`include_magnetic`</b> (bool, optional):  Flag to include contributions from magnetic trap 
 - <b>`include_terminator`</b> (bool, optional):  Flag to include the position of the terminator beam relative to the trap 

---

<a href="../../oqtant/schemas/quantum_matter.py#L464"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show_rf_dynamics`

```python
show_rf_dynamics(corrected: 'bool' = False) → None
```

Method to plot the dynamics of a QuantumMatter object's RF output 



**Args:**
 
 - <b>`corrected`</b> (bool, optional):  Flag to correct the RF power 

---

<a href="../../oqtant/schemas/quantum_matter.py#L334"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `submit`

```python
submit(track: 'bool' = False, sim: 'bool' = False) → None
```

Method to submit a QuantumMatter object to Oqtant to become a job and run on hardware or as a simulation 



**Args:**
 
 - <b>`track`</b> (bool, optional):  Flag to poll for job updates after submission 
 - <b>`sim`</b> (bool, optional):  Flag to use the simulator backend instead of real hardware 

---

<a href="../../oqtant/schemas/quantum_matter.py#L327"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `submit_sim`

```python
submit_sim() → None
```

Method to submit a QuantumMatter object to be run as a simulation 

---

<a href="../../oqtant/schemas/quantum_matter.py#L321"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `write_to_file`

```python
write_to_file(*args, **kwargs) → None
```

Method to write the results of a submitted QuantumMatter object to a file. Wrapper for OqtantClient.write_job_to_file 


---

<a href="../../oqtant/schemas/quantum_matter.py#L812"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `QuantumMatterFactory`
An abstract factory for creating instances of the QuantumMatter schema classes 

<a href="../../oqtant/schemas/quantum_matter.py#L815"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```








---

<a href="../../oqtant/schemas/quantum_matter.py#L1049"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_barrier`

```python
create_barrier(
    positions: 'list[float]' = [0.0, 0.0],
    heights: 'list[float]' = [0.0, 0.0],
    widths: 'list[float]' = [1.0, 1.0],
    times: 'list[float]' = [0.0, 10.0],
    shape: 'ShapeType' = 'GAUSSIAN',
    interpolation: 'InterpolationType' = 'LINEAR'
) → Barrier
```

Method to create a Barrier object 



**Args:**
 
 - <b>`positions`</b> (list[float], optional):  The barrier positions 
 - <b>`heights`</b> (list[float], optional):  The barrier heights 
 - <b>`widths`</b> (list[float], optional):  The barrier widths 
 - <b>`times`</b> (list[float], optional):  The barrier times 
 - <b>`shape`</b> (bert_schemas.job.ShapeType, optional):  The barrier shape 
 - <b>`interpolation`</b> (bert_schemas.job.InterpolationType, optional):  The barrier interpolation type 



**Returns:**
 
 - <b>`oqtant.schemas.optical.Barrier`</b>:  A new Barrier object 



**Raises:**
 
 - <b>`ValueError`</b>:  if data lists are not of equal length 

---

<a href="../../oqtant/schemas/quantum_matter.py#L1088"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_barrier_from_input`

```python
create_barrier_from_input(input: 'Barrier') → Barrier
```

Method to create a Barrier object from the input values of a job 



**Args:**
 
 - <b>`input`</b> (bert_schemas.job.Barrier):  The input values 



**Returns:**
 
 - <b>`oqtant.schemas.optical.Barrier`</b>:  A new Barrier object created using the input data 

---

<a href="../../oqtant/schemas/quantum_matter.py#L1013"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_landscape`

```python
create_landscape(
    snapshots: 'list[Snapshot]' = [Snapshot(time_ms=Decimal('0'), potentials_khz=[0.0, 0.0], positions_um=[-10.0, 10.0], spatial_interpolation=<InterpolationType.LINEAR: 'LINEAR'>), Snapshot(time_ms=Decimal('2'), potentials_khz=[0.0, 0.0], positions_um=[-10.0, 10.0], spatial_interpolation=<InterpolationType.LINEAR: 'LINEAR'>)]
) → Landscape
```

Method to create a Landscape object from a list Snapshot objects 



**Args:**
 
 - <b>`snapshots`</b> (list[oqtant.schemas.optical.Snapshot], optional):  List of snapshots, defaults if not provided 



**Returns:**
 
 - <b>`oqtant.schemas.optical.Landscape`</b>:  A new Landscape object 

---

<a href="../../oqtant/schemas/quantum_matter.py#L1037"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_landscape_from_input`

```python
create_landscape_from_input(input: 'OpticalLandscape') → Landscape
```

Method to create a Landscape object from the input values of a job 



**Args:**
 
 - <b>`input`</b> (bert_schemas.job.OpticalLandscape):  The input values 



**Returns:**
 
 - <b>`oqtant.schemas.optical.Landscape`</b>:  A new Landscape object created using the input data 

---

<a href="../../oqtant/schemas/quantum_matter.py#L918"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_quantum_matter`

```python
create_quantum_matter(
    name: 'str | None' = None,
    temperature: 'float | None' = None,
    lifetime: 'float | None' = None,
    image: 'ImageType | None' = None,
    time_of_flight: 'float | None' = None,
    rf_evap: 'RfEvap | None' = None,
    rf_shield: 'RfShield | None' = None,
    barriers: 'list[Barrier] | None' = None,
    landscape: 'Landscape | None' = None,
    lasers: 'list[Laser] | None' = None,
    note: 'str | None' = None
) → QuantumMatter
```

Method to create a QuantumMatter object 



**Args:**
 
 - <b>`name`</b> (str | None, optional):  The name of the quantum matter 
 - <b>`temperature`</b> (float | None, optional):  The quantum matter temperature 
 - <b>`lifetime`</b> (float | None, optional):  The quantum matter lifetime 
 - <b>`image`</b> (bert_schemas.job.ImageType | None, optional):  The quantum matter image type 
 - <b>`time_of_flight`</b> (float | None, optional):  The quantum matter time of flight 
 - <b>`rf_evap`</b> (oqtant.schemas.rf.RfEvap | None, optional):  The quantum matter RF evaporation 
 - <b>`rf_shield`</b> (oqtant.schemas.rf.RfShield | None, optional):  The quantum matter RF shield 
 - <b>`barriers`</b> (list[oqtant.schemas.optical.Barrier] | None, optional):  The quantum matter barriers 
 - <b>`landscape`</b> (oqtant.schemas.optical.Landscape | None, optional):  The quantum matter landscape 
 - <b>`lasers`</b> (list[bert_schemas.job.Lasers] | None, optional):  The quantum matter lasers 
 - <b>`note`</b> (str | None, optional):  A note about the quantum matter 



**Returns:**
 
 - <b>`QuantumMatter`</b>:  A new QuantumMatter object 

---

<a href="../../oqtant/schemas/quantum_matter.py#L957"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_quantum_matter_from_input`

```python
create_quantum_matter_from_input(
    name: 'str',
    input: 'InputValues',
    note: 'JobNote | None' = None
) → QuantumMatter
```

Method to create a QuantumMatter object using the input values of a job. Wrapper for QuantumMatter.from_input 



**Args:**
 
 - <b>`name`</b> (str):  The name of the quantum matter 
 - <b>`input`</b> (bert_schemas.job.InputValues):  The input values 
 - <b>`note`</b> (job_schema.job.JobNote | None):  The notes for the input, can be None 



**Returns:**
 
 - <b>`QuantumMatter`</b>:  A new QuantumMatter object created using the input data 

---

<a href="../../oqtant/schemas/quantum_matter.py#L1178"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_rf_evap`

```python
create_rf_evap(
    times: 'list' = [0],
    powers: 'list' = [0],
    frequencies: 'list' = [0],
    interpolation: 'str' = 'LINEAR'
) → RfEvap
```

Method to create a RfEvap object 



**Args:**
 
 - <b>`times`</b> (list[int], optional):  The time values in milliseconds 
 - <b>`powers`</b> (list[list[float], optional):  The power values in milliwatts 
 - <b>`frequencies`</b> (list[float], optional):  The frequency values in megahertz 
 - <b>`interpolation`</b> (bert_schemas.job.InterpolationType, optional):  The interpolation type to be used 



**Returns:**
 
 - <b>`oqtant.schemas.rf.RfEvap`</b>:  A new RfEvap object 

---

<a href="../../oqtant/schemas/quantum_matter.py#L1203"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_rf_evap_from_input`

```python
create_rf_evap_from_input(input: 'RfEvaporation') → RfEvap
```

Method to create a RfEvap object from the input values of a job 



**Args:**
 
 - <b>`input`</b> (bert_schemas.job.RfEvaporation):  The input values 



**Returns:**
 
 - <b>`oqtant.schemas.rf.RfEvap`</b>:  A new RfEvap object created using the input data 

---

<a href="../../oqtant/schemas/quantum_matter.py#L1141"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_rf_sequence`

```python
create_rf_sequence(
    times: 'list' = [0],
    powers: 'list' = [0],
    frequencies: 'list' = [0],
    interpolation: 'str' = 'LINEAR'
) → RfSequence
```

Method to create a RfSequence object 



**Args:**
 
 - <b>`times`</b> (list[int], optional):  The time values in milliseconds 
 - <b>`powers`</b> (list[list[float], optional):  The power values in milliwatts 
 - <b>`frequencies`</b> (list[float], optional):  The frequency values in megahertz 
 - <b>`interpolation`</b> (bert_schemas.job.InterpolationType, optional):  The interpolation type to be used 



**Returns:**
 
 - <b>`oqtant.schemas.rf.RfSequence`</b>:  A new RfSequence object 

---

<a href="../../oqtant/schemas/quantum_matter.py#L1166"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_rf_sequence_from_input`

```python
create_rf_sequence_from_input(input: 'RfEvaporation') → RfSequence
```

Method to create a RfSequence object from the input values of a job 



**Args:**
 
 - <b>`input (bert_schemas.job.RfEvaporation`</b>:  The input values 



**Returns:**
 
 - <b>`oqtant.schemas.rf.RfSequence`</b>:  A new RfSequence object created using the input data 

---

<a href="../../oqtant/schemas/quantum_matter.py#L1215"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_rf_shield`

```python
create_rf_shield(
    power: 'float' = 0,
    frequency: 'float' = 0,
    lifetime: 'EndTimeMs' = 1.0
) → RfShield
```

Method to create a RfShield object 



**Args:**
 
 - <b>`power`</b> (float, optional):  The RfShield power 
 - <b>`frequency`</b> (float, optional):  The RfShield frequency 
 - <b>`lifetime`</b> (float, optional):  The RfShield lifetime 



**Returns:**
 
 - <b>`oqtant.schemas.rf.RfShield`</b>:  A new RfShield object 

---

<a href="../../oqtant/schemas/quantum_matter.py#L1236"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_rf_shield_from_input`

```python
create_rf_shield_from_input(input: 'RfEvaporation') → RfShield
```

Method to create a RfShield object from the input values of a job 



**Args:**
 
 - <b>`input`</b> (bert_schemas.job.RfEvaporation):  The input values 



**Returns:**
 
 - <b>`oqtant.schemas.rf.RfShield`</b>:  A new RfShield object created using the input data 

---

<a href="../../oqtant/schemas/quantum_matter.py#L976"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_snapshot`

```python
create_snapshot(
    time: 'float' = 0,
    positions: 'list' = [-10, 10],
    potentials: 'list' = [0, 0],
    interpolation: 'InterpolationType' = 'LINEAR'
) → Snapshot
```

Method to create a Snapshot object 



**Args:**
 
 - <b>`time`</b> (float, optional):  The time in milliseconds 
 - <b>`positions`</b> (list, optional):  A list of positions in micrometers 
 - <b>`potentials`</b> (list, optional):  A list of potentials in kilohertz 
 - <b>`interpolation`</b> (bert_schemas.job.InterpolationType, optional):  The type of interpolation for spatial data 



**Returns:**
 
 - <b>`oqtant.schemas.optical.Snapshot`</b>:  A new Snapshot object 

---

<a href="../../oqtant/schemas/quantum_matter.py#L1001"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_snapshot_from_input`

```python
create_snapshot_from_input(input: 'Landscape') → Snapshot
```

Method to create a Snapshot object using the input values of a job 



**Args:**
 
 - <b>`input`</b> (bert_schemas.job.Landscape):  The landscape input data 



**Returns:**
 
 - <b>`oqtant.schemas.optical.Snapshot`</b>:  A new Snapshot object created using the input data 

---

<a href="../../oqtant/schemas/quantum_matter.py#L1100"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_terminator`

```python
create_terminator(time_on: 'float', time_off: 'float') → Laser
```

Method to create terminator pulse 



**Args:**
 
 - <b>`time_on (float) `</b>:  time to start the pulse in ms 
 - <b>`time_off (float) `</b>:  time to end the pulse in ms 



**Returns:**
 
 - <b>`oqtant.schemas.optical.Laser`</b>:  A new Laser object 

---

<a href="../../oqtant/schemas/quantum_matter.py#L1129"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_terminator_from_input`

```python
create_terminator_from_input(input: 'Laser') → Laser
```

Method to create a Laser object from the input values of a job 



**Args:**
 
 - <b>`input`</b> (bert_schemas.job.Laser):  The input values 



**Returns:**
 
 - <b>`oqtant.schemas.optical.Laser`</b>:  A new Laser object created using the input data 

---

<a href="../../oqtant/schemas/quantum_matter.py#L837"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_client`

```python
get_client(token: 'str | None' = None) → None
```

Method to get an instance of OqtantClient and assign it to self.client 



**Args:**
 
 - <b>`token`</b> (str | None, optional):  Token to use when working outside of a notebook 

---

<a href="../../oqtant/schemas/quantum_matter.py#L819"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_login`

```python
get_login() → Auth
```

Method to display the authentication widget inside of a notebook, if no access token file is found. 



**Returns:**
 
 - <b>`ipyauth.Auth`</b>:  The authentication widget 

---

<a href="../../oqtant/schemas/quantum_matter.py#L873"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_matter_from_file`

```python
load_matter_from_file(*args, **kwargs) → QuantumMatter
```

Method to create a QuantumMatter object using data in a file. Wrapper for OqtantClient.load_job_from_file 



**Returns:**
 
 - <b>`QuantumMatter`</b>:  A new QuantumMatter object created using the file data 

---

<a href="../../oqtant/schemas/quantum_matter.py#L883"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_matter_from_job_id`

```python
load_matter_from_job_id(job_id: 'str', run: 'int' = 1) → QuantumMatter
```

Method to create a QuantumMatter object using data from an existing job in the database 



**Args:**
 
 - <b>`job_id`</b> (str):  The id of the job to get from the database 
 - <b>`run`</b> (int, optional):  The specific run to get 



**Returns:**
 
 - <b>`QuantumMatter`</b>:  A new QuantumMatter object created using the jobs data 

---

<a href="../../oqtant/schemas/quantum_matter.py#L846"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `search_jobs`

```python
search_jobs(*args, **kwargs) → list[dict]
```

Method to search for jobs. Wrapper for OqtantClient.search_jobs 



**Returns:**
 
 - <b>`list[dict]`</b>:  The jobs found for the search criteria 

---

<a href="../../oqtant/schemas/quantum_matter.py#L864"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show_job_limits`

```python
show_job_limits() → dict
```

Method to show the current job limits of the authenticated user. Wrapper for OqtantClient.show_job_limits 



**Returns:**
 
 - <b>`dict`</b>:  The job limit information for the authenticated user 

---

<a href="../../oqtant/schemas/quantum_matter.py#L855"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show_queue_status`

```python
show_queue_status(*args, **kwargs) → list[dict]
```

Method to show the current queue status of jobs submitted by the authenticated user. Wrapper for OqtantClient.show_queue_status 



**Returns:**
 
 - <b>`list[dict]`</b>:  The jobs found for the search criteria along with their queue status 

---

<a href="../../oqtant/schemas/quantum_matter.py#L909"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `submit_list_as_batch`

```python
submit_list_as_batch(*args, **kwargs) → str
```

Method to submit multiple QuantumMatter objects as a single job. Wrapper for OqtantClient.submit_list_as_batch 



**Returns:**
 
 - <b>`str`</b>:  The ID of the submitted job 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
