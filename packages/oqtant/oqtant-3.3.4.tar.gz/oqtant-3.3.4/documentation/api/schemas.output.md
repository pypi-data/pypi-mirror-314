<!-- markdownlint-disable -->

<a href="../../oqtant/schemas/output.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `schemas.output`





---

<a href="../../oqtant/schemas/output.py#L45"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `in_trap_check`

```python
in_trap_check(func)
```






---

<a href="../../oqtant/schemas/output.py#L633"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `round_sig`

```python
round_sig(x: float, sig: int = 2) → float
```

Method to round a number to a specified number of significant digits 



**Args:**
 
 - <b>`x`</b> (float):  The number to be rounded 
 - <b>`sig`</b> (int, optional):  The number of significant digits 



**Returns:**
 
 - <b>`float`</b>:  The rounded number 


---

<a href="../../oqtant/schemas/output.py#L646"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `TF_dist_2D`

```python
TF_dist_2D(
    xy_mesh: tuple[ndarray, ndarray],
    TFpOD: float,
    xc: float,
    yc: float,
    rx: float,
    ry: float,
    os: float
) → ndarray
```

Method to sample a 2D Thomas-Fermi distribution with given parameters on a grid of coordinates 



**Args:**
 
 - <b>`xy_mesh`</b> (tuple[numpy.ndarray, numpy.ndarray]):  Matrix containing meshgrid of image coordinates 
 - <b>`TFpOD`</b> (float):  Thomas-Fermi peak optical density 
 - <b>`xc`</b> (float):  Cloud center along the x direction (along gravity) 
 - <b>`yc`</b> (float):  Cloud center along the y direction 
 - <b>`rx`</b> (float):  Thomas-Fermi radius along the x direction 
 - <b>`ry`</b> (float):  Thomas-Fermi radius along the y direction (along gravity) 
 - <b>`os`</b> (float):  Constant offset 



**Returns:**
 
 - <b>`numpy.ndarray`</b>:  a 2D array of samples from a Thomas Fermi distribution 


---

<a href="../../oqtant/schemas/output.py#L683"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `Gaussian_dist_2D`

```python
Gaussian_dist_2D(
    xy_mesh: tuple[ndarray, ndarray],
    GpOD: float,
    xc: float,
    yc: float,
    sigx: float,
    sigy: float,
    os: float
) → ndarray
```

Method to sample a 2D Gaussian distribution with given parameters on a grid of coordinates 



**Args:**
 
 - <b>`xy_mesh`</b> (tuple[numpy.ndarray, numpy.ndarray]):  Matrix containing meshgrid of image coordinates 
 - <b>`GpOD`</b> (float):  Gaussian peak optical density 
 - <b>`xc`</b> (float):  Cloud center along the x direction (along gravity) 
 - <b>`yc`</b> (float):  Could center along the y direction 
 - <b>`sigx`</b> (float):  Gaussian spread along the x direction 
 - <b>`sigy`</b> (float):  Gaussian spread along the y direction (along gravity) 
 - <b>`os`</b> (float):  Constant offset 



**Returns:**
 
 - <b>`numpy.ndarray`</b>:  a 2D array of samples from a Gaussian distribution 


---

<a href="../../oqtant/schemas/output.py#L715"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `bimodal_dist_2D`

```python
bimodal_dist_2D(
    xy_mesh: tuple[ndarray, ndarray],
    GpOD: float,
    sigx: float,
    sigy: float,
    TFpOD: float,
    rx: float,
    ry: float,
    xc: float,
    yc: float,
    os: float
)
```

Method to sample a bimodal (Thomas-Fermi + Gaussian) distribution with given parameters on a grid of coordinates 



**Args:**
 
 - <b>`xy_mesh`</b> (tuple[numpy.ndarray, numpy.ndarray]):  Matrix containing meshgrid of image coordinates 
 - <b>`GpOD`</b> (float):  Gaussian peak optical density 
 - <b>`sigx`</b> (float):  Gaussian spread along the x direction 
 - <b>`sigy`</b> (float):  Gaussian spread along the y direction (along gravity) 
 - <b>`TFpOD`</b> (float):  Thomas-Fermi peak optical density 
 - <b>`rx`</b> (float):  Thomas-Fermi radius along the x direction 
 - <b>`ry`</b> (float):  Thomas-Fermi radius along the y direction (along gravity) 
 - <b>`xc`</b> (float):  Cloud center along the x direction (along gravity) 
 - <b>`yc`</b> (float):  Cloud center along the y direction 
 - <b>`os`</b> (float):  Constant offset 



**Returns:**
 
 - <b>`numpy.ndarray`</b>:  a 2D array of samples from a bimodal (Thomas-Fermi + Gaussian) distribution 


---

<a href="../../oqtant/schemas/output.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `OutputImageType`








---

<a href="../../oqtant/schemas/output.py#L40"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `AxisType`








---

<a href="../../oqtant/schemas/output.py#L55"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `OqtantOutput`
A class that represents the output of a job submitted to Oqtant 


---

#### <kbd>property</kbd> IT

Property that returns the shaped in-trap (IT) image of a job's output if it exists 



**Returns:**
 
 - <b>`numpy.ndarray`</b>:  The reshaped pixels of the IT image 

---

#### <kbd>property</kbd> TOF

Property that returns the shaped time of flight (TOF) image of a job's output if it exists 



**Returns:**
 
 - <b>`numpy.ndarray`</b>:  The reshaped pixels of the TOF image 

---

#### <kbd>property</kbd> atom_statistics

Property that prints out the atom statistics of a TIME_OF_FLIGHT image job's output 

---

#### <kbd>property</kbd> condensed_fraction





---

#### <kbd>property</kbd> condensed_population





---

#### <kbd>property</kbd> fields

Method to print out the output fields for an OqtantOutput 

---

#### <kbd>property</kbd> get_bimodal_fit_parameters





---

#### <kbd>property</kbd> image_type





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

#### <kbd>property</kbd> mot_population





---

#### <kbd>property</kbd> temperature





---

#### <kbd>property</kbd> thermal_population





---

#### <kbd>property</kbd> total_population







---

<a href="../../oqtant/schemas/output.py#L308"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `fit_bimodal_data2D`

```python
fit_bimodal_data2D(
    xi: list[float] = None,
    lb: list[float] = None,
    ub: list[float] = None
) → tuple[ndarray, ndarray, ndarray, float64]
```

Method to perform a fit via a trust region reflective algorithm 



**Args:**
 
 - <b>`xi`</b> (list[float] | None, optional):  List of fit parameter initial guesses 
 - <b>`lb`</b> (list[float] | None, optional):  List of fit parameter lower bounds 
 - <b>`ub`</b> (list[float] | None, optional):  List of fit parameter upper bounds 



**Returns:**
 
 - <b>`tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.float64]`</b>:  The calculated fit data 

---

<a href="../../oqtant/schemas/output.py#L187"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_image_data`

```python
get_image_data(image: OutputImageType | None = None) → ndarray | None
```

Method to retrieve the image data for the specified image type, if no image type is provided the job's imaging type will be returned 



**Args:**
 
 - <b>`image`</b> (oqtant.schemas.output.OutputImageType | None, optional):  The image type to retrieve 



**Returns:**
 
 - <b>`numpy.ndarray`</b>:  The image data for the specified image type 

---

<a href="../../oqtant/schemas/output.py#L233"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_image_pixcal`

```python
get_image_pixcal(image: OutputImageType) → float
```

Method to get the pixel calibration for the provided image type 



**Args:**
 
 - <b>`image`</b> (oqtant.schemas.output.OutputImageType):  The image type to retrieve the pixel calibration for 



**Returns:**
 
 - <b>`float`</b>:  The pixel calibration for the provided image 

---

<a href="../../oqtant/schemas/output.py#L284"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_image_space`

```python
get_image_space(
    datafile: ndarray = array([[0., 0., 0., ..., 0., 0., 0.],
       [0., 0., 0., ..., 0., 0., 0.],
       [0., 0., 0., ..., 0., 0., 0.],
       ...,
       [0., 0., 0., ..., 0., 0., 0.],
       [0., 0., 0., ..., 0., 0., 0.],
       [0., 0., 0., ..., 0., 0., 0.]]),
    centered: str = 'y'
) → tuple[meshgrid, int, int]
```

Method to generate a numpy.meshgrid of image coordinates 



**Args:**
 
 - <b>`datafile`</b> (numpy.ndarray, default):  A matrix of optical density data 
 - <b>`centered`</b> (str, optional):  The orientation of the image 



**Returns:**
 
 - <b>`tuple[numpy.meshgrid, int, int]`</b>:  The numpy.meshgrid of image coordinates 

---

<a href="../../oqtant/schemas/output.py#L267"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_slice`

```python
get_slice(axis: AxisType = 'x') → list[float]
```

Method that returns a list of data point representing a slice along the specified axis 



**Args:**
 
 - <b>`axis`</b> (oqtant.schemas.output.AxisType, optional):  The axis along which the take the slice 



**Returns:**
 
 - <b>`list[float]`</b>:  A list of data points representing the slice along the specified axis 

---

<a href="../../oqtant/schemas/output.py#L341"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `plot_fit_results`

```python
plot_fit_results(
    fit_params: ndarray,
    model: str = 'bimodal',
    file_name: str = None,
    plot_title: str = None,
    pix_cal: float = 1.0
) → None
```

Method to plot the results of a fit operation 



**Args:**
 
 - <b>`fit_params`</b> (numpy.ndarray):  List of parameters from a fit operation 
 - <b>`model`</b> (str. optional):  The shape(?) to use while plotting 
 - <b>`file_name`</b> (str | None, optional):  The name of the file to write the plot to 
 - <b>`plot_title`</b> (str | None, optional):  The title of the resulting plot result 
 - <b>`pix_cal`</b> (float, optional):  The pixel calibration to use while generating the plot 

---

<a href="../../oqtant/schemas/output.py#L553"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `plot_it`

```python
plot_it(
    file_name: str = None,
    figsize: tuple[int, int] = (12, 12),
    grid_on=False
) → None
```

Method to plot an in-trap image output 



**Args:**
 
 - <b>`file_name`</b> (str | None, optional):  The name of the file to write the plot to 
 - <b>`figsize`</b> (tuple[int, int], optional):  The size of the figure to generate 
 - <b>`grid_on`</b> (bool):  Show grid in plot? 

---

<a href="../../oqtant/schemas/output.py#L473"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `plot_slice`

```python
plot_slice(
    file_name: str = None,
    axis: AxisType = 'x',
    grid_on: bool = False
) → None
```

Method to generate a 1D slice plot of atom OD in x or y 



**Args:**
 
 - <b>`file_name`</b> (str | None, optional):  The name of the file to write the plot to 
 - <b>`axis`</b>:  (oqtant.schemas.output.AxisType, optional): The axis to use in the plot 
 - <b>`grid_on`</b> (bool, optional):  Flag to show grid lines or not in the plot 

---

<a href="../../oqtant/schemas/output.py#L432"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `plot_tof`

```python
plot_tof(
    file_name: str = None,
    figsize: tuple[int, int] = (12, 12),
    grid_on: bool = False
) → None
```

Method to generate a 2D plot of atom OD 



**Args:**
 
 - <b>`file_name`</b> (str | None, optional):  The name of the file to write the plot to 
 - <b>`figsize`</b> (tuple[int, int], optional):  The size of the figure to generate 
 - <b>`grid_on`</b> (bool, optional):  Flag to show grid lines or not in the plot 

---

<a href="../../oqtant/schemas/output.py#L589"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `plot_tof_3d`

```python
plot_tof_3d(
    file_name: str = None,
    view_angle: int = -45,
    figsize: tuple[int, int] = (10, 10)
) → None
```

Method to generate a 3D slice plot of atom OD 



**Args:**
 
 - <b>`file_name`</b> (str | None, optional):  The name of the file to write the plot to 
 - <b>`view_angle`</b> (int, optional):  Azimuthal/horizontal angle of "camera" view 
 - <b>`figsize`</b> (tuple[int, int], optional):  The size of the figure to generate 


---

<a href="../../oqtant/schemas/output.py#L625"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `OqtantPlotOutput`





---

#### <kbd>property</kbd> IT

Property that returns the shaped in-trap (IT) image of a job's output if it exists 



**Returns:**
 
 - <b>`numpy.ndarray`</b>:  The reshaped pixels of the IT image 

---

#### <kbd>property</kbd> TOF

Property that returns the shaped time of flight (TOF) image of a job's output if it exists 



**Returns:**
 
 - <b>`numpy.ndarray`</b>:  The reshaped pixels of the TOF image 

---

#### <kbd>property</kbd> atom_statistics

Property that prints out the atom statistics of a TIME_OF_FLIGHT image job's output 

---

#### <kbd>property</kbd> condensed_fraction





---

#### <kbd>property</kbd> condensed_population





---

#### <kbd>property</kbd> fields

Method to print out the output fields for an OqtantOutput 

---

#### <kbd>property</kbd> get_bimodal_fit_parameters





---

#### <kbd>property</kbd> image_type





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

#### <kbd>property</kbd> mot_population





---

#### <kbd>property</kbd> temperature





---

#### <kbd>property</kbd> thermal_population





---

#### <kbd>property</kbd> total_population







---

<a href="../../oqtant/schemas/output.py#L308"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `fit_bimodal_data2D`

```python
fit_bimodal_data2D(
    xi: list[float] = None,
    lb: list[float] = None,
    ub: list[float] = None
) → tuple[ndarray, ndarray, ndarray, float64]
```

Method to perform a fit via a trust region reflective algorithm 



**Args:**
 
 - <b>`xi`</b> (list[float] | None, optional):  List of fit parameter initial guesses 
 - <b>`lb`</b> (list[float] | None, optional):  List of fit parameter lower bounds 
 - <b>`ub`</b> (list[float] | None, optional):  List of fit parameter upper bounds 



**Returns:**
 
 - <b>`tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.float64]`</b>:  The calculated fit data 

---

<a href="../../oqtant/schemas/output.py#L187"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_image_data`

```python
get_image_data(image: OutputImageType | None = None) → ndarray | None
```

Method to retrieve the image data for the specified image type, if no image type is provided the job's imaging type will be returned 



**Args:**
 
 - <b>`image`</b> (oqtant.schemas.output.OutputImageType | None, optional):  The image type to retrieve 



**Returns:**
 
 - <b>`numpy.ndarray`</b>:  The image data for the specified image type 

---

<a href="../../oqtant/schemas/output.py#L233"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_image_pixcal`

```python
get_image_pixcal(image: OutputImageType) → float
```

Method to get the pixel calibration for the provided image type 



**Args:**
 
 - <b>`image`</b> (oqtant.schemas.output.OutputImageType):  The image type to retrieve the pixel calibration for 



**Returns:**
 
 - <b>`float`</b>:  The pixel calibration for the provided image 

---

<a href="../../oqtant/schemas/output.py#L284"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_image_space`

```python
get_image_space(
    datafile: ndarray = array([[0., 0., 0., ..., 0., 0., 0.],
       [0., 0., 0., ..., 0., 0., 0.],
       [0., 0., 0., ..., 0., 0., 0.],
       ...,
       [0., 0., 0., ..., 0., 0., 0.],
       [0., 0., 0., ..., 0., 0., 0.],
       [0., 0., 0., ..., 0., 0., 0.]]),
    centered: str = 'y'
) → tuple[meshgrid, int, int]
```

Method to generate a numpy.meshgrid of image coordinates 



**Args:**
 
 - <b>`datafile`</b> (numpy.ndarray, default):  A matrix of optical density data 
 - <b>`centered`</b> (str, optional):  The orientation of the image 



**Returns:**
 
 - <b>`tuple[numpy.meshgrid, int, int]`</b>:  The numpy.meshgrid of image coordinates 

---

<a href="../../oqtant/schemas/output.py#L267"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_slice`

```python
get_slice(axis: AxisType = 'x') → list[float]
```

Method that returns a list of data point representing a slice along the specified axis 



**Args:**
 
 - <b>`axis`</b> (oqtant.schemas.output.AxisType, optional):  The axis along which the take the slice 



**Returns:**
 
 - <b>`list[float]`</b>:  A list of data points representing the slice along the specified axis 

---

<a href="../../oqtant/schemas/output.py#L341"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `plot_fit_results`

```python
plot_fit_results(
    fit_params: ndarray,
    model: str = 'bimodal',
    file_name: str = None,
    plot_title: str = None,
    pix_cal: float = 1.0
) → None
```

Method to plot the results of a fit operation 



**Args:**
 
 - <b>`fit_params`</b> (numpy.ndarray):  List of parameters from a fit operation 
 - <b>`model`</b> (str. optional):  The shape(?) to use while plotting 
 - <b>`file_name`</b> (str | None, optional):  The name of the file to write the plot to 
 - <b>`plot_title`</b> (str | None, optional):  The title of the resulting plot result 
 - <b>`pix_cal`</b> (float, optional):  The pixel calibration to use while generating the plot 

---

<a href="../../oqtant/schemas/output.py#L553"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `plot_it`

```python
plot_it(
    file_name: str = None,
    figsize: tuple[int, int] = (12, 12),
    grid_on=False
) → None
```

Method to plot an in-trap image output 



**Args:**
 
 - <b>`file_name`</b> (str | None, optional):  The name of the file to write the plot to 
 - <b>`figsize`</b> (tuple[int, int], optional):  The size of the figure to generate 
 - <b>`grid_on`</b> (bool):  Show grid in plot? 

---

<a href="../../oqtant/schemas/output.py#L473"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `plot_slice`

```python
plot_slice(
    file_name: str = None,
    axis: AxisType = 'x',
    grid_on: bool = False
) → None
```

Method to generate a 1D slice plot of atom OD in x or y 



**Args:**
 
 - <b>`file_name`</b> (str | None, optional):  The name of the file to write the plot to 
 - <b>`axis`</b>:  (oqtant.schemas.output.AxisType, optional): The axis to use in the plot 
 - <b>`grid_on`</b> (bool, optional):  Flag to show grid lines or not in the plot 

---

<a href="../../oqtant/schemas/output.py#L432"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `plot_tof`

```python
plot_tof(
    file_name: str = None,
    figsize: tuple[int, int] = (12, 12),
    grid_on: bool = False
) → None
```

Method to generate a 2D plot of atom OD 



**Args:**
 
 - <b>`file_name`</b> (str | None, optional):  The name of the file to write the plot to 
 - <b>`figsize`</b> (tuple[int, int], optional):  The size of the figure to generate 
 - <b>`grid_on`</b> (bool, optional):  Flag to show grid lines or not in the plot 

---

<a href="../../oqtant/schemas/output.py#L589"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `plot_tof_3d`

```python
plot_tof_3d(
    file_name: str = None,
    view_angle: int = -45,
    figsize: tuple[int, int] = (10, 10)
) → None
```

Method to generate a 3D slice plot of atom OD 



**Args:**
 
 - <b>`file_name`</b> (str | None, optional):  The name of the file to write the plot to 
 - <b>`view_angle`</b> (int, optional):  Azimuthal/horizontal angle of "camera" view 
 - <b>`figsize`</b> (tuple[int, int], optional):  The size of the figure to generate 


---

<a href="../../oqtant/schemas/output.py#L629"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `OqtantNonPlotOutput`





---

#### <kbd>property</kbd> IT

Property that returns the shaped in-trap (IT) image of a job's output if it exists 



**Returns:**
 
 - <b>`numpy.ndarray`</b>:  The reshaped pixels of the IT image 

---

#### <kbd>property</kbd> TOF

Property that returns the shaped time of flight (TOF) image of a job's output if it exists 



**Returns:**
 
 - <b>`numpy.ndarray`</b>:  The reshaped pixels of the TOF image 

---

#### <kbd>property</kbd> atom_statistics

Property that prints out the atom statistics of a TIME_OF_FLIGHT image job's output 

---

#### <kbd>property</kbd> condensed_fraction





---

#### <kbd>property</kbd> condensed_population





---

#### <kbd>property</kbd> fields

Method to print out the output fields for an OqtantOutput 

---

#### <kbd>property</kbd> get_bimodal_fit_parameters





---

#### <kbd>property</kbd> image_type





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

#### <kbd>property</kbd> mot_population





---

#### <kbd>property</kbd> temperature





---

#### <kbd>property</kbd> thermal_population





---

#### <kbd>property</kbd> total_population







---

<a href="../../oqtant/schemas/output.py#L308"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `fit_bimodal_data2D`

```python
fit_bimodal_data2D(
    xi: list[float] = None,
    lb: list[float] = None,
    ub: list[float] = None
) → tuple[ndarray, ndarray, ndarray, float64]
```

Method to perform a fit via a trust region reflective algorithm 



**Args:**
 
 - <b>`xi`</b> (list[float] | None, optional):  List of fit parameter initial guesses 
 - <b>`lb`</b> (list[float] | None, optional):  List of fit parameter lower bounds 
 - <b>`ub`</b> (list[float] | None, optional):  List of fit parameter upper bounds 



**Returns:**
 
 - <b>`tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.float64]`</b>:  The calculated fit data 

---

<a href="../../oqtant/schemas/output.py#L187"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_image_data`

```python
get_image_data(image: OutputImageType | None = None) → ndarray | None
```

Method to retrieve the image data for the specified image type, if no image type is provided the job's imaging type will be returned 



**Args:**
 
 - <b>`image`</b> (oqtant.schemas.output.OutputImageType | None, optional):  The image type to retrieve 



**Returns:**
 
 - <b>`numpy.ndarray`</b>:  The image data for the specified image type 

---

<a href="../../oqtant/schemas/output.py#L233"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_image_pixcal`

```python
get_image_pixcal(image: OutputImageType) → float
```

Method to get the pixel calibration for the provided image type 



**Args:**
 
 - <b>`image`</b> (oqtant.schemas.output.OutputImageType):  The image type to retrieve the pixel calibration for 



**Returns:**
 
 - <b>`float`</b>:  The pixel calibration for the provided image 

---

<a href="../../oqtant/schemas/output.py#L284"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_image_space`

```python
get_image_space(
    datafile: ndarray = array([[0., 0., 0., ..., 0., 0., 0.],
       [0., 0., 0., ..., 0., 0., 0.],
       [0., 0., 0., ..., 0., 0., 0.],
       ...,
       [0., 0., 0., ..., 0., 0., 0.],
       [0., 0., 0., ..., 0., 0., 0.],
       [0., 0., 0., ..., 0., 0., 0.]]),
    centered: str = 'y'
) → tuple[meshgrid, int, int]
```

Method to generate a numpy.meshgrid of image coordinates 



**Args:**
 
 - <b>`datafile`</b> (numpy.ndarray, default):  A matrix of optical density data 
 - <b>`centered`</b> (str, optional):  The orientation of the image 



**Returns:**
 
 - <b>`tuple[numpy.meshgrid, int, int]`</b>:  The numpy.meshgrid of image coordinates 

---

<a href="../../oqtant/schemas/output.py#L267"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_slice`

```python
get_slice(axis: AxisType = 'x') → list[float]
```

Method that returns a list of data point representing a slice along the specified axis 



**Args:**
 
 - <b>`axis`</b> (oqtant.schemas.output.AxisType, optional):  The axis along which the take the slice 



**Returns:**
 
 - <b>`list[float]`</b>:  A list of data points representing the slice along the specified axis 

---

<a href="../../oqtant/schemas/output.py#L341"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `plot_fit_results`

```python
plot_fit_results(
    fit_params: ndarray,
    model: str = 'bimodal',
    file_name: str = None,
    plot_title: str = None,
    pix_cal: float = 1.0
) → None
```

Method to plot the results of a fit operation 



**Args:**
 
 - <b>`fit_params`</b> (numpy.ndarray):  List of parameters from a fit operation 
 - <b>`model`</b> (str. optional):  The shape(?) to use while plotting 
 - <b>`file_name`</b> (str | None, optional):  The name of the file to write the plot to 
 - <b>`plot_title`</b> (str | None, optional):  The title of the resulting plot result 
 - <b>`pix_cal`</b> (float, optional):  The pixel calibration to use while generating the plot 

---

<a href="../../oqtant/schemas/output.py#L553"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `plot_it`

```python
plot_it(
    file_name: str = None,
    figsize: tuple[int, int] = (12, 12),
    grid_on=False
) → None
```

Method to plot an in-trap image output 



**Args:**
 
 - <b>`file_name`</b> (str | None, optional):  The name of the file to write the plot to 
 - <b>`figsize`</b> (tuple[int, int], optional):  The size of the figure to generate 
 - <b>`grid_on`</b> (bool):  Show grid in plot? 

---

<a href="../../oqtant/schemas/output.py#L473"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `plot_slice`

```python
plot_slice(
    file_name: str = None,
    axis: AxisType = 'x',
    grid_on: bool = False
) → None
```

Method to generate a 1D slice plot of atom OD in x or y 



**Args:**
 
 - <b>`file_name`</b> (str | None, optional):  The name of the file to write the plot to 
 - <b>`axis`</b>:  (oqtant.schemas.output.AxisType, optional): The axis to use in the plot 
 - <b>`grid_on`</b> (bool, optional):  Flag to show grid lines or not in the plot 

---

<a href="../../oqtant/schemas/output.py#L432"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `plot_tof`

```python
plot_tof(
    file_name: str = None,
    figsize: tuple[int, int] = (12, 12),
    grid_on: bool = False
) → None
```

Method to generate a 2D plot of atom OD 



**Args:**
 
 - <b>`file_name`</b> (str | None, optional):  The name of the file to write the plot to 
 - <b>`figsize`</b> (tuple[int, int], optional):  The size of the figure to generate 
 - <b>`grid_on`</b> (bool, optional):  Flag to show grid lines or not in the plot 

---

<a href="../../oqtant/schemas/output.py#L589"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `plot_tof_3d`

```python
plot_tof_3d(
    file_name: str = None,
    view_angle: int = -45,
    figsize: tuple[int, int] = (10, 10)
) → None
```

Method to generate a 3D slice plot of atom OD 



**Args:**
 
 - <b>`file_name`</b> (str | None, optional):  The name of the file to write the plot to 
 - <b>`view_angle`</b> (int, optional):  Azimuthal/horizontal angle of "camera" view 
 - <b>`figsize`</b> (tuple[int, int], optional):  The size of the figure to generate 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
