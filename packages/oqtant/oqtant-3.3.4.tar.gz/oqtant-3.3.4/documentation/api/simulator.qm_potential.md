<!-- markdownlint-disable -->

<a href="../../oqtant/simulator/qm_potential.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `simulator.qm_potential`






---

<a href="../../oqtant/simulator/qm_potential.py#L22"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `QMPotential`
'QMPotential' represents the quantum matter object potential (combination of magnetic trap/snapshot/barriers) in simulation units. Contains a 2D array of the potential energy in the simulation at a given time. 

<a href="../../oqtant/simulator/qm_potential.py#L56"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(quantum_matter)
```






---

#### <kbd>property</kbd> lifetime

Returns the lifetime of the simulation in simulation time units. 

---

#### <kbd>property</kbd> time_of_flight

If image type is in trap returns zero. Else calculate and return time of flight in the units of the sim 



---

<a href="../../oqtant/simulator/qm_potential.py#L131"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `potential_to_cartesian_oqt_units`

```python
potential_to_cartesian_oqt_units() → ndarray
```

Convert the potential object self.potential to cartesian coordinates and oqtant units (microns, kHz). 



**Returns:**
 
 - <b>`array`</b>:  the converted potential in cartesian coordinates and oqtant units 

---

<a href="../../oqtant/simulator/qm_potential.py#L81"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `update_potential`

```python
update_potential(time: ndarray, clip: bool = False) → None
```

Function to query the potential at a specific simulation time (sim units), from the Oqtant quantum matter object. Potential is updated with the magnetic trap 

Updates property self.potential 



**Args:**
 
 - <b>`time`</b> (np.ndarray[float]):   time (in simulation units) 
 - <b>`clip`</b> (boolean):  whether to clip 



**Returns:**
 None 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
