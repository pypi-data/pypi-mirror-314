<!-- markdownlint-disable -->

<a href="../../oqtant/util/auth.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `util.auth`




**Global Variables**
---------------
- **verifier**

---

<a href="../../oqtant/util/auth.py#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_random`

```python
generate_random(length: int) → str
```

Method to generate a random base64 string 



**Args:**
 
 - <b>`length`</b> (int):  The length to make the string 



**Returns:**
 
 - <b>`str`</b>:  The generated base64 string 


---

<a href="../../oqtant/util/auth.py#L51"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_challenge`

```python
generate_challenge(verifier: str) → str
```

Method to generate a base64 string to serve as an auth0 challenge 



**Args:**
 
 - <b>`verifier`</b> (str):  A base64 string to create the challenge off of 



**Returns:**
 
 - <b>`str`</b>:  The generated challenge 


---

<a href="../../oqtant/util/auth.py#L64"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_authentication_url`

```python
get_authentication_url(auth_server_port: int) → None
```

Method to generate the auth0 authentication url 



**Args:**
 
 - <b>`auth_server_port`</b> (int):  The port of the server auth0 should redirect to 


---

<a href="../../oqtant/util/auth.py#L89"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `main`

```python
main(request: Request, code: str) → str
```

Main route to handle user authentication 



**Args:**
 
 - <b>`request`</b> (fastapi.Request):  The request object 
 - <b>`code`</b> (str):  The code provided by auth0 to be verified 



**Returns:**
 
 - <b>`str`</b>:  Message on whether the user successfully authenticated 


---

<a href="../../oqtant/util/auth.py#L109"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `login`

```python
login(request: Request) → RedirectResponse
```

Route to initiate the authentication process 



**Args:**
 
 - <b>`request`</b> (Request):  The request object 



**Returns:**
 
 - <b>`RedirectResponse`</b>:  A redirect to auth0 universal login 


---

<a href="../../oqtant/util/auth.py#L124"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_token`

```python
get_token(verifier: str, code: str, auth_server_port: int) → dict
```

Method to get an authentication token from auth0 after a user authenticates 



**Args:**
 
 - <b>`verifier`</b> (str):  The base64 string to provide along with the code challenge 
 - <b>`code`</b> (str):  The code challenge returned from auth0 
 - <b>`auth_server_port`</b> (int):  The port the local server is running on 



**Returns:**
 
 - <b>`dict`</b>:  The json response from auth0, should contain the authentication token 


---

<a href="../../oqtant/util/auth.py#L150"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_user_token`

```python
get_user_token(auth_server_port: int = 8080) → str
```

Method to initiate the user authentication process 



**Args:**
 
 - <b>`auth_server_port`</b> (int, optional):  The port to run the server on locally 



**Returns:**
 
 - <b>`str`</b>:  The authentication token 


---

<a href="../../oqtant/util/auth.py#L172"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `notebook_login`

```python
notebook_login() → Auth
```

Method to get an authenticate widget 



**Returns:**
 
 - <b>`ipyauth.Auth`</b>:  The authentication widget 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
