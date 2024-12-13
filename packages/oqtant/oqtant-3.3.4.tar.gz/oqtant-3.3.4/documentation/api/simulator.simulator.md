<!-- markdownlint-disable -->

<a href="../../oqtant/simulator/simulator.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `simulator.simulator`






---

<a href="../../oqtant/simulator/simulator.py#L34"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `TimeSpan`
TimeSpan(start: float, end: float) 

<a href="../../<string>"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(start: float, end: float) → None
```









---

<a href="../../oqtant/simulator/simulator.py#L40"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Simulator`
'Simulator' Defines methods for evolution and plotting of the system described by the Oqtant simulator. The Oqtant simulator is constantly in evolution and the inteface should not be relied upon for use external to the Oqtant API. 

<a href="../../oqtant/simulator/simulator.py#L55"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(potential: QMPotential)
```

Creates Three Wavefunctions: 
- One is In-Trap (IT) 
- One is Time of Flight Far Field (tof_ff) 
- One is Time of Flight Near Field (tof_nf) 



**Args:**
 potential: Defined with QMPotential object. 


---

#### <kbd>property</kbd> it_plot

Generate a simulation analog to an in-trap image from the Oqtant hardware. 



**Returns:**
 
 - <b>`dict`</b>:  data for generating an Image object(pixels, pixcal, rows, columns) 

---

#### <kbd>property</kbd> tof_output

Generate an simulation analog to a TOF image from the Oqtant hardware. 



**Returns:**
 
 - <b>`dict`</b>:  data for generating an Image object(pixels, pixcal, rows, columns) 



---

<a href="../../oqtant/simulator/simulator.py#L1223"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `animate_current`

```python
animate_current(frame_interval: int = 1, y_limit=10000.0) → FuncAnimation
```

Animates the density profiles and change in potentials over time.  This is an integrated profile along the x-direction and is different from a single slice. 

**Args:**
 
 - <b>`frame_interval`</b> (int):  number of frames to skip each interval, determines smoothness. default =1 
 - <b>`current_bound`</b> (float):   adjustable bound on the y-axis in the case that the current exceeds the default. 

**Returns:**
 
 - <b>`FuncAnimation`</b>:  an animation of the profile along the x-direction. 

---

<a href="../../oqtant/simulator/simulator.py#L1396"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `animate_density`

```python
animate_density(frame_interval=1, figsize=(8, 3), show_potential=True)
```

Animates the change in density and potential over time 



**Args:**
 
 - <b>`frame_interval`</b> (int):  number of frames to skip each interval, determines smoothness. default = 1 
 - <b>`show_potential`</b> (bool):  whether or not to show the potential on the animation. default = True 
 - <b>`figsize`</b> (tuple):  size of the output figure. default = (8,3) 



**Returns:**
 
 - <b>`FuncAnimation`</b>:  an animation of the profile along the x-direction. 

---

<a href="../../oqtant/simulator/simulator.py#L1297"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `animate_phase`

```python
animate_phase(
    frame_interval: int = 1,
    show_potential: bool = True,
    figsize=(8, 3)
)
```

Animate the change in phase 



**Args:**
 
 - <b>`frame_interval`</b> (int):  number of frames to skip each interval, determines smoothness. default =1 
 - <b>`show_potential`</b> (bool):  whether or not to show the potential on the animation. default = True 
 - <b>`figsize`</b> (tuple):  size of the output figure. default = (8,3) 



**Returns:**
 
 - <b>`FuncAnimation`</b>:  an animation of the profile along the x-direction. 

---

<a href="../../oqtant/simulator/simulator.py#L1493"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `animate_profiles`

```python
animate_profiles(frame_interval=1, y_limit=1312.0592504731997)
```

Animates the density profiles and change in potentials over time.  This is an integrated profile along the x-direction and is different from a single slice(!). 



**Args:**
 
 - <b>`frame_interval`</b> (int):  number of frames to skip each interval, determines smoothness. default = 1 
 - <b>`y_axis`</b> (float):   optional arguement to adjust the y-axis in the event that the density is to large. 



**Returns:**
 
 - <b>`FuncAnimation`</b>:  an animation of the profile along the x-direction. 

---

<a href="../../oqtant/simulator/simulator.py#L221"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `convert_intrap_to_nearfield`

```python
convert_intrap_to_nearfield(psi: ndarray) → ndarray
```

Performs interpolation of wave function between IT and TOF grids For handoff between evolve IT and in TOF modes. 



**Args:**
 
 - <b>`psi`</b> (ndarray):   a wave function of the IT grid (self.wavefunction.three_d_grid) 

**Returns:**
 
 - <b>`ndarray`</b>:   psi interpolated onto the TOF nearfield grid (self.wavefunction_tof_nf.three_d_grid) 

---

<a href="../../oqtant/simulator/simulator.py#L259"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `convert_nearfield_to_farfield`

```python
convert_nearfield_to_farfield(psi_tof_nf: ndarray) → ndarray
```

Interpolation of wave function between NF and FF grids For handoff between evolve NF and in FF modes. 



**Args:**
 
 - <b>`psi_tof_nf`</b> (ndarray):   a wave function of the NF grid (self.wavefunction_tof_nf.three_d_grid) 

**Returns:**
 
 - <b>`ndarray`</b>:   psi interpolated onto the TOF grid (self.wavefunction_tof_ff.three_d_grid) 

---

<a href="../../oqtant/simulator/simulator.py#L854"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `convert_timesteps`

```python
convert_timesteps(timesteps: list) → ndarray
```

Convert a list of arbitrary times (in oqtant units) to a list of simulator timestep indices. Simulation must already have been evaluated. 



**Args:**
 
 - <b>`timesteps`</b> (list):  list of times in oqtant units 



**Returns:**
 
 - <b>`ndarray `</b>:  array of simulator timestep indexes (not the values of the timesteps) 

---

<a href="../../oqtant/simulator/simulator.py#L938"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_column_densities`

```python
get_column_densities(time_ms: float) → tuple
```

Returns the column densities and slices of the condensate in cartesian coordinates for an arbitrary time. In correct coordinates to be returned to the user. 



**Args:**
 
 - <b>`time_ms`</b> (float):   time (in milliseconds) 

**Returns:**
 
 - <b>`tuple (column_zy, column_zx, slice_y, slice_x) `</b>:  the column densitites and slices at the desired time 

---

<a href="../../oqtant/simulator/simulator.py#L358"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_gpe`

```python
get_gpe(psi: ndarray) → ndarray
```

Implementation of the Gross-Pitaevskii Equation w/Neumann boundary conditions at r = 0 and Dirichlet at large x and r. If self.tof_nf or self.tof_ff == True, the external potential is ignored. 



**Args:**
 
 - <b>`psi`</b> (ndarray):  the current timestep wavefunction 



**Returns:**
 
 - <b>`ndarray`</b>:  wavefunction calculated by the Gross-Pitaevskii Equation 

---

<a href="../../oqtant/simulator/simulator.py#L904"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_grids`

```python
get_grids(time_ms: float) → tuple
```

Returns the x-grid in microns at a user specified time. 



**Args:**
 
 - <b>`time_ms`</b> (float):   time (in milliseconds) 

**Returns:**
 
 - <b>`tuple (dx, Lx, x_1d) `</b>:  the simulation resolution, length in x-direction, and length array in x-direction 

---

<a href="../../oqtant/simulator/simulator.py#L297"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_laplacian`

```python
get_laplacian(y: ndarray) → ndarray
```

Implementation of the second derivatives in x and r including forward, central, and backward formulas to second order accuracy 



**Args:**
 
 - <b>`y`</b> (ndarray):  function for which we calculate the laplacian 



**Returns:**
 
 - <b>`ndarray`</b>:  The laplacian of the function 

---

<a href="../../oqtant/simulator/simulator.py#L927"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_times`

```python
get_times()
```

Returns the an array of  times in oqtant units 



**Returns:**
 
 - <b>`array times `</b>:  the timesteps in oqtant units (milliseconds) 

---

<a href="../../oqtant/simulator/simulator.py#L792"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_time_far_field`

```python
is_time_far_field(time: float) → bool
```

Checks if the time is when the condensate is in far-field part of TOF. 



**Args:**
 
 - <b>`time`</b> (float):    time in simulation (!) units. 

**Returns:**
 
 - <b>`Bool`</b>:   True means the system is in FF of TOF mode at that time. 

---

<a href="../../oqtant/simulator/simulator.py#L761"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_time_intrap`

```python
is_time_intrap(time: float) → bool
```

Checks if the time is when the condensate is still in trap. 



**Args:**
 
 - <b>`time`</b> (float):    time in simulation units. 

**Returns:**
 
 - <b>`Bool`</b>:   True means the system is in IT mode at that time.  False means it is not (it is in TOF mode). 

---

<a href="../../oqtant/simulator/simulator.py#L776"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_time_near_field`

```python
is_time_near_field(time: float) → bool
```

Checks if the time is when the condensate is in near-field part of TOF. 



**Args:**
 
 - <b>`time`</b> (float):    time in simulation (!) units. 

**Returns:**
 
 - <b>`Bool`</b>:   True means the system is in NF of TOF mode at that time. 

---

<a href="../../oqtant/simulator/simulator.py#L489"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_wavefunction_at_boundary`

```python
is_wavefunction_at_boundary(psi: ndarray) → None
```

Warn user if the condensate is hitting the edge of the simulation. 



**Args:**
 
 - <b>`psi`</b> (ndarray):  the wave function 

---

<a href="../../oqtant/simulator/simulator.py#L140"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run_TOF`

```python
run_TOF() → None
```

This function runs the TOF evolution and turns on/off the far field grid as needed 



**Returns:**
  None 

---

<a href="../../oqtant/simulator/simulator.py#L189"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run_TOF_farField`

```python
run_TOF_farField() → None
```

This function evolves the condensate with ground = False, with no trapping potentials or optical potentials. It runs for the remaining time of flight of the quantum_matter object, beginning with the result wavefunction of run_TOF_nearField at 6ms. It uses the far field TOF grid: self.wavefunction_tof_ff.three_d_grid is created with argument FF = True 



**Returns:**
  None 

---

<a href="../../oqtant/simulator/simulator.py#L154"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run_TOF_nearField`

```python
run_TOF_nearField() → None
```

This function evolves the condensate with ground = False, with no trapping potentials or optical potentials. It runs for up to 6ms of the quantum_matter object, beginning with the result wavefunction of run_evolution It uses the near field TOF grid: self.wavefunction_tof_nf.three_d_grid is created with argument NF = True 



**Returns:**
  None 

---

<a href="../../oqtant/simulator/simulator.py#L113"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run_evolution`

```python
run_evolution() → None
```

Run the simulation in In-Trap (IT) mode. This function evolves the condensate with ground = False. It is done at positive times during the "experiment" stage (t=0). Optical potentials may be applied during this stage. It runs for the lifetime of the quantum_matter object It starts from the end result of running get_ground_state 



**Returns:**
  None 

---

<a href="../../oqtant/simulator/simulator.py#L387"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run_rk4`

```python
run_rk4(time_span: TimeSpan, stage_name: str = '') → None
```

Implementation of the Runge-Kutta 4th order method to evolve in time. Depends on if the simulation is in IT mode, tof_nf or tof_ff mode. 



**Args:**
 
 - <b>`time_span`</b> (TimeSpan):   a list of times (in milliseconds) 
 - <b>`stage_name`</b> (str):  name for the evolving stage. default = "" 

**Returns:**
 None 

---

<a href="../../oqtant/simulator/simulator.py#L90"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `set_ground_state`

```python
set_ground_state() → None
```

This function evolves the condensate with ground = True. It is done at negative times before the barriers are switched on. 2.5 simulation units of time is sufficient to settle down to the ground state. 



**Returns:**
  None 

---

<a href="../../oqtant/simulator/simulator.py#L1024"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show_column_densities`

```python
show_column_densities(times_ms: list, slices: bool = True, figsize=(15, 7))
```

Plots the column densities and slices of the condensate in cartesian coordinates for an input array of times. In correct coordinates to be returned to the user. 



**Args:**
 
 - <b>`times_ms`</b> (list):   a list of times (in milliseconds) 
 - <b>`slices`</b> (bool):  plot or not to plot slices 
 - <b>`figsize`</b> (tuple):  size of output figure. default = (15,7) 

**Returns:**
 None 

---

<a href="../../oqtant/simulator/simulator.py#L1190"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show_current`

```python
show_current(times_ms: list, figsize=(10, 7)) → None
```

Plot the flow for a given list of timesteps two separate subplots 



**Args:**
 
 - <b>`times_ms`</b> (list):  List of times (ms) at which to display current 
 - <b>`figsize`</b> (tuple):  size of output figure. default = (10,7) 



**Returns:**
 None 

---

<a href="../../oqtant/simulator/simulator.py#L971"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show_density_cylindrical`

```python
show_density_cylindrical(times_ms: list, figsize=(15, 7)) → None
```

Plots the density profile of the condensate in cylindrical coordinates for an input array of times. Useful coordinates for diagonising issues but not to be returned to the user. 



**Args:**
 
 - <b>`times_ms`</b> (list):   a list of times (in milliseconds/oqtant units) 
 - <b>`figsize`</b> (tuple):  size of output figure. default = (15,7) 

**Returns:**
 None 

---

<a href="../../oqtant/simulator/simulator.py#L831"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show_final_result`

```python
show_final_result() → None
```

Plot the density at the end of the simulation in cylindrical coordinates. Useful coordinates for diagonising issues but not to be returned to the user. 

---

<a href="../../oqtant/simulator/simulator.py#L1142"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show_phase`

```python
show_phase(times_ms: list, figsize=(10, 7)) → None
```

Plot the phase for a given list of timesteps This can only be displayed in cylindrical coordinates. It is a helpful tool still for the user.  The aspect ratio is still a bit weird. 



**Args:**
 
 - <b>`times_ms`</b> (list):  List of times to display 
 - <b>`figsize`</b> (tuple):  size of output figure. default = (10,7) 

**Returns:**
 None 

---

<a href="../../oqtant/simulator/simulator.py#L804"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `which_wavefunction_mode`

```python
which_wavefunction_mode(time: float) → WaveFunction
```

Checks which mode the time corresponds to and returns the correct wavefunction class. 



**Args:**
 
 - <b>`time`</b> (float):    time in simulation (!) units. 

**Returns:**
 
 - <b>`WaveFunction`</b>:   instance of the wavefunction class in the correct mode 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
