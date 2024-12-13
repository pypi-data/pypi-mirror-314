<!-- markdownlint-disable -->

<a href="../../oqtant/schemas/interpolation.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `schemas.interpolation`





---

<a href="../../oqtant/schemas/interpolation.py#L19"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `interpolation_to_kind`

```python
interpolation_to_kind(interpolation: InterpolationType) → str
```

Method to convert our InterpolationType to something scipy can understand 



**Args:**
 
 - <b>`interpolation`</b> (bert_schemas.job.InterpolationType):  Primitive job interpolation type 



**Returns:**
 
 - <b>`str`</b>:  A "kind" string to be used by scipy's interp1d 


---

<a href="../../oqtant/schemas/interpolation.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `interpolate_1d`

```python
interpolate_1d(
    xs: list[float],
    ys: list[float],
    x: float,
    interpolation: InterpolationType = 'LINEAR'
) → float
```

Method to interpolate a 1D list of pairs [xs, ys] at the evaluation point x 



**Args:**
 
 - <b>`xs`</b> (list[float]):  List of x values 
 - <b>`ys`</b> (list[float]):  List of y values 
 - <b>`x`</b> (float):  Desired x-coordinate to evaluate the resulting interpolation function 
 - <b>`interpolation`</b> (job_schema.InterpolationType, optional):  Interpolation style 



**Returns:**
 
 - <b>`float`</b>:  Interpolation function value at the specified x-coordinate 


---

<a href="../../oqtant/schemas/interpolation.py#L60"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `interpolate_1d_list`

```python
interpolate_1d_list(
    xs: list[float],
    ys: list[float],
    x_values: list[float],
    interpolation: InterpolationType = 'LINEAR'
) → list[float]
```

Method to interpolate a 1d list of pairs [xs, ys] at the evaluation points given by x_values 



**Args:**
 
 - <b>`xs`</b> (list[float]):  List of x values 
 - <b>`ys`</b> (list[float]):  List of y values 
 - <b>`x_values`</b> (list[float]):  Desired x-coordinates to evaluate the resulting interpolation function 
 - <b>`interpolation`</b> (job_schema.InterpolationType, optional):  Interpolation style 



**Returns:**
 
 - <b>`list[float]`</b>:  Floating point values corresponding to evaluation of the interpolation function  value at the specified x_values 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
