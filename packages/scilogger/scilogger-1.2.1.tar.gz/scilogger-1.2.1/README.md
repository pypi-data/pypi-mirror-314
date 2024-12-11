# SciLogger - Python Logging for Science 

> * **Repository: [github.com/otvam/scilogger](https://github.com/otvam/scilogger)**
> * **PyPi: [pypi.org/project/scilogger](https://pypi.org/project/scilogger)**
> * **Conda: [anaconda.org/conda-forge/scilogger](https://anaconda.org/conda-forge/scilogger)**

## Summary

**SciLogger** is a **Python Logging** module:
* Specially targeted for **scientific applications**.
* Use a **global timer** to measure the **elapsed time**.
* Provide a class for **timing code blocks**.
* Definition of **custom indentation levels**.
* Definition of **colors** for the logging levels.

**SciLogger** is using a global **INI configuration** file:
* First, the **default configuration** is loaded (`scilogger/scilogger.ini`).
* Afterward, a **custom file** can be loaded with an environment variable (`SCILOGGER`)

SciLogger is written in Python without any external dependencies.

## Warning

* This logging module is **based** on the **Python logging module**.
* The philosophy of this logging module is slightly different. 
* Mixing both modules can create strange/incorrect behaviors.

## Example

An example is located in the `example` folder of the repository:
* `run_logger.py` contains an example file for the logger
* `configlogger.ini` contains a custom configuration file

```bash
# Set the configuration file.
export SCILOGGER="configlocal.ini"

# Run the Python script.
python run_logger.py
```

## Project Links

* Repository: https://github.com/otvam/scilogger
* Releases: https://github.com/otvam/scilogger/releases
* Tags: https://github.com/otvam/scilogger/tags
* Issues: https://github.com/otvam/scilogger/issues
* PyPi: https://pypi.org/project/scilogger
* Conda: https://anaconda.org/conda-forge/scilogger

## Author

* **Thomas Guillod**
* Email: guillod@otvam.ch
* Website: https://otvam.ch

## Copyright

> (c) 2023 - Thomas Guillod
> 
>  BSD 2-Clause "Simplified" License
