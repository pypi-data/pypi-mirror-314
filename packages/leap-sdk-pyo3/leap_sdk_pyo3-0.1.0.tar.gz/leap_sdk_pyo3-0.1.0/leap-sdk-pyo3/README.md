### Steps to build python bindings

1. Create a virtual env for pyo3
```bash
pyenv virtualenv 3.10.15 pyo3-dev
pyenv activate pyo3-dev
```

2. [Optional]Install maturin if not installed

3. [Optional, only for new projects] Init maturin
```bash
maturin init
>> choose pyo3
```

4. Generate Wheel , install the wheel for python developement
```bash
maturin develop  #- wheel is generated.
python
>>> import leap_sdk_pyo3
>>> leap_sdk_pyo3.sum_as_string(5, 20)
'25'
```


### Steps to build and invoke RUST code directly.

1. This code invokes the main.rs
```bash
RUST_LOG=info cargo run --bin server
```