# softdes-nytimes-countries

These files focus on looking at how the New York Times covers regime changes related to U.S. intervention and influence.
The full report can be found in `ComputationalEssay.ipynb`. 

`obtaining.py` has functions that can be used to obtain data about the number of keyword hits and headlines each month from New York Times Article Search API; it can also write them to a cvs. 

`processing.py` has functions that read a csv and formats headlines, both for word cloud generation and for using Google's Natural Language API. 

`visualization.py` contains functions that can generate various plots from a csv.

Collected data for each country is stored in a csv in `CountryData` with corresponding flags in `CountryFlags`.

## Requirements Before Running
To use the all functions, you must do all of the following:
1. Install `pyjq` library to use `processing.py` and `obtaining.py`.
    - Make sure that it can build the wheel: `python -m pip install --upgrade pip setuptools wheel`
    - Make sure that you have all of the following packages: `flex`, `bison`, `libtool`, `make`, `automake`, and `autoconfig`. These can be installed with `sudo apt install <package>`.
    - Install `pyjq`: `pip install pyjq` 
2. Make a [New York Times Developer](https://developer.nytimes.com/) account and create an API key that can access the [Article Search API](https://developer.nytimes.com/docs/articlesearch-product/1/overview). 
    - This key as a string should be used as an input to any function in `obtaining.py` that calls for an API key. 
3. Make a free [Google Cloud account](https://cloud.google.com/) and make an API key that can access the [Natural Language API](https://cloud.google.com/natural-language). These steps are necessary to use `processing.py`.
    - In `processing.py`, uncomment line 10 (`import os`). Uncomment lines 21 and 22 as well.
    - In `processing.py` on line 19, add a variable `PATH_<YOUR NAME>` that has a string for your path to your Google Cloud API key in the first line of a text file. 
    - Change line 21 to use your API variable: `with open(os.path.abspath(PATH_<YOUR_NAME>), "r") as f:`. 
4. If running a code block in computational essay, make sure to uncomment any lines of code as well as read directions for adding API keys.

## Generating Plots
You should not need to do anything besides run the computational essay to generate plots. The plot generating functions can be found in `visualization.py`. If you would like to create a new plot, check the docstrings for specifics.

![](https://developer.nytimes.com/files/poweredby_nytimes_200c.png?v=1583354208354)