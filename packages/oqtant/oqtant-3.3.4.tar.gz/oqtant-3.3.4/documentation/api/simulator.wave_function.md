<!-- markdownlint-disable -->

<a href="../../oqtant/simulator/wave_function.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `simulator.wave_function`






---

<a href="../../oqtant/simulator/wave_function.py#L21"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `WaveFunction`
'WaveFunction' Defines representation for a wavefunction It is sensitive to whether the system is in Time of Flight (TOF) or In Trap (IT) mode 

<a href="../../oqtant/simulator/wave_function.py#L27"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(tof_nf: bool = False, tof_ff: bool = False)
```

Initializes a wavefuntion in Time of Flight Near Field (tof_nf) or Time of Flight Far Field (tof_ff) 

**Args:**
 
 - <b>`tof_nf`</b>:  Indicates if WaveFunction uses Time of Flight (TOF) Near field 
 - <b>`tof_ff`</b>:  Indicates if WaveFunction uses TOF Far Field 


---

#### <kbd>property</kbd> atom_number

Returns atom number calculated from the current wavefunction 



**Returns:**
 
 - <b>`float`</b>:  number of atoms in the simulation (normalized to 1) 

---

#### <kbd>property</kbd> column_densities

Returns the column densities (#/Length^2) 

Returns  tuple : (column_zy -  the zy axes, column_zx -  the zx axes, profiles - the profiles in the x and z axes) 

---

#### <kbd>property</kbd> com_position

Returns the center of mass coordinates of the cloud in X direction The center of mass cannot be displaced in the radial direction by assumption Returns 1 scalar, useful for diagnostics 



**Returns:**
 
 - <b>`float `</b>:  the center of mass in the X direction 

---

#### <kbd>property</kbd> current

Returns the total current along the X-direction, 1D array 



**Returns:**
 
 - <b>`ndarray `</b>:  current in the X direction (simulator units) 

---

#### <kbd>property</kbd> density

Get the density of the wavefunction. 

**Returns:**
 
 - <b>`ndarray`</b>:  the density of the wave function 

---

#### <kbd>property</kbd> density_profiles

Returns the density profiles along the x and r axes.  #/Length These match the integrated column densities 

---

#### <kbd>property</kbd> flow

Returns the superfluid velocities in X and R directions in two 2D arrays 



**Returns:**
 
 - <b>`tuple`</b>:  (flow_r - flow in R direction, flow_x - flow in X direction). Simulator units. 

---

#### <kbd>property</kbd> phase

Returns the phase of the wave function 



**Returns:**
 
 - <b>`ndarray`</b>:  the phase of the wavefunction (cylindrical coordinates, sim units) 

---

#### <kbd>property</kbd> widths

Returns the widths of the condensate (\Delta r and \Delta x) in radial and x directions 

Returns  tuple: (Delta r, Delta x) simulation units. 



---

<a href="../../oqtant/simulator/wave_function.py#L38"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `initial_psi`

```python
initial_psi(sigma_x: int = 1, sigma_r: int = 1) → ndarray
```

Defines the initial wave function of the system with controllable widths. 



**Args:**
 
 - <b>`sigma_x`</b> (int):   width in the x direction 
 - <b>`sigma_r`</b> (int):   width in the r direction 



**Returns:**
 
 - <b>`psi np.ndarray`</b>:   initial wave function 

---

<a href="../../oqtant/simulator/wave_function.py#L86"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `integrate_prob_distro`

```python
integrate_prob_distro(psi: ndarray) → float
```

Calculate the probability density function by integrating the square of the absolute value of the wavefunction. 

**Args:**
 
 - <b>`psi`</b> (np.ndarray):  The wavefunction 

**Returns:**
 
 - <b>`float`</b>:  The probability distribution 

---

<a href="../../oqtant/simulator/wave_function.py#L59"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `normalize`

```python
normalize(psi: ndarray) → ndarray
```

Normalizes the wave function to the number of atoms Applies normalization directly to psi. This feels wonky as psi is a member of the Wavefunction class, however in the runge-kutta method we advance psi without saving to the wavefunction so we need to be able to normalize a passed in psi. We just have to assume the psi passed in maintains the same coordinates as the psi in the wavefunction. 



**Args:**
 
 - <b>`psi`</b> (np.ndarray):   wavefunction 



**Returns:**
 normalized np.ndarray 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
