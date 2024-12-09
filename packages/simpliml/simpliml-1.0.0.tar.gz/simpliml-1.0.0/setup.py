import setuptools, os, datetime, license

pckName = "simpliml"
version = "1.0.0"
python_requires=">=3.9,<=3.12"
author = "Dharmaraj D"
status = "Development Status :: 1 - Planning"
author_email = "rajaddr@gmail.com"
licenseType="MIT"
description = "Machine Learning, Artificial Intelligence, Mathematics"
url = "https://github.com/rajaddr/simpliml"
keywords='Forecast Time Series Machine Learning Deep Learning Artificial Intelligence Mathematics'

print(os.getcwd())
with open('LICENSE', 'w') as f:
    f.write(license.find(licenseType).render(name=author, email=author_email))

with open('about.py', 'w') as f:
    f.write("""import json

version_json = '''{
    "__date__": "%s",
    "__author__": "%s",
    "__version__": "%s",
    "__email__": "%s",
    "__description__": "%s",
    "__keywords__": "%s",
    "__url__": "%s",
    "__license__": "%s",
    "__status__": "%s"
}'''

def get_about():
    return json.loads(version_json)
"""%(datetime.datetime.now(),author, version, author_email, description, keywords, url, licenseType, status.split()[-1]))

with open('README.md', 'w') as f:
    f.write("""<div align="center">

![SimpliML](https://i.ibb.co/KWCTBQP/NameSml.png) 

[![Python](https://img.shields.io/static/v1?label=Python&labelColor=007676&message={0}&color=01C0C0&style=flat&logoColor=01C0C0&logo=python)](https://pypi.org/project/simpliml/)
[![Version](https://img.shields.io/static/v1?label=Version&labelColor=007676&message={1}&color=01C0C0&style=flat)](https://pypi.org/project/simpliml/)
[![Package Status](https://img.shields.io/static/v1?label=Status&labelColor=007676&message={2}&color=01C0C0&style=flat)](https://pypi.org/project/simpliml/)
[![License](https://img.shields.io/static/v1?label=License&labelColor=007676&message={3}&color=01C0C0&style=flat)](https://github.com/rajaddr/simpliml/blob/master/LICENSE)
<hr>
</div>

## Project description
**SimpliML** is a versatile machine learning library designed to be a one-stop solution for the entire data lifecycle. Whether you're preparing raw data or deploying advanced predictive models, *SimpliML* simplifies every step of the machine learning process.  

## Key Features  

- **Data Cleansing and Cleaning**  
  Simplify the preprocessing of raw data to ensure accurate and reliable model performance.  

- **Data Analysis**  
  Explore and analyze data with powerful, easy-to-use tools to uncover actionable insights.  

- **Model Execution and Prediction**  
  Train, validate, and deploy machine learning models seamlessly for accurate and efficient predictions.  

- **Forecasting and Optimization**  
  Perform precise forecasting and optimize your decision-making processes with ease.  

## Why Choose SimpliML?  

***SimpliML*** is designed for data scientists, ML engineers, and enthusiasts who need a reliable, efficient, and easy-to-use toolkit for managing the entire machine learning workflow.  

Get started today and unlock the full potential of your data with **SimpliML**!  

## Links
- Binary installers : [Python Package Index (PyPI)](https://pypi.org/project/simpliml)
- Source code repository : [GIT](https://github.com/rajaddr/simpliml) 
- Issue tracker : [Issue](https://github.com/rajaddr/simpliml/issues) 
- Changelog : [Changelog](https://github.com/rajaddr/simpliml/blob/master/CHANGELOG.md) 

## Installation
```sh
# or PyPI
pip install simpliml
```

## Dependencies
![Pandas](https://img.shields.io/static/v1?label=Pandas&labelColor=007676&message=>=2.2.3&color=01C0C0&style=flat&logoColor=01C0C0&logo=pandas)
![NumPy](https://img.shields.io/static/v1?label=NumPy&labelColor=007676&message=>=1.26.2&color=01C0C0&style=flat&logoColor=01C0C0&logo=NumPy)
![SciPy](https://img.shields.io/static/v1?label=SciPy&labelColor=007676&message=>=1.14.1&color=01C0C0&style=flat&logoColor=01C0C0&logo=SciPy)
![scikit-learn](https://img.shields.io/static/v1?label=scikit-learn&labelColor=007676&message=>=1.5.2&color=01C0C0&style=flat&logoColor=01C0C0&logo=scikit-learn)
![Torch](https://img.shields.io/static/v1?label=Torch&labelColor=007676&message=>=2.5.1&color=01C0C0&style=flat&logoColor=01C0C0&logo=PyTorch)
![Statsmodels](https://img.shields.io/static/v1?label=statsmodels&labelColor=007676&message=>=0.14.4&color=01C0C0&style=flat&logoColor=01C0C0&logo=)
![Altair](https://img.shields.io/static/v1?label=Altair&labelColor=007676&message=>=5.5.0&color=01C0C0&style=flat&logoColor=01C0C0&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMgAAADICAYAAACtWK6eAAAACXBIWXMAAAWJAAAFiQFtaJ36AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAATSSURBVHgB7d07biRVGIbhv7rtYCSCjiEZESELS70BpFoAiM4IcUDOElgTK6iAjIRVkLCBkXxR4ZYbZHnaM+2u27k8T+zMelWnXJ+rIgAAAAAAAAAAAAAAAAAAAAAAAABIWhMcddtdbd/98+dfkZmHn77wOx3RKjhq1ax/DaonkNe1QfUEcsRtd33TR7wPqieQI5omfg4IgXzkQ/fN+3C84kAgL6zi4ibgQCAvrJvG8Yr/CeSZu+7b1s05zwnkmcbVgxcEcrC/OX+8etwEPCOQg3VctgEvCOSgaXrTEj4ikPjv2UezDXhBII8um8vfAo4QyJM24IjqAzFM5FOqD6Rp4seAV1QdyGGYuAt4RdWBePbB51QdyKoJf73ik6oNxDCRU1QbiGEip6gykL7bbno355ygykDu4mEfxybgM6oMxEsZOFV1gXgpA29RXSCGibxFjUesNuBEVQVy313vPPvgLaoKpHdzzhtVE4hhIueoJhDDRM5RTSCGiZyjikAMEzlXFYEYJnKu4gMxTGSI4gMxTGSI4gMxTGSIogMxTGSoogMxTGSo0o9YbcAAxQZimMgYyr2CeGMiIygyEF+LYixFBmKYyFiKDMQwkbEUF8htd7V1c85Yigtk1ax9a5DRlHjEagNGchEFKflrUd9/uT7tB//40Ecifv/uXROZK+oKYpjI2IoJxDCRKRQTyCoubgJGVkwga/9WywSKCMRLGZhKEYF4KQNTyT4Qw0SmlH0gholMKftAmqY3LWEyWQeyHyY+JrINmEjWgRgmMrXcj1htwISyDaTkYSLpyDYQw0TmkGUghonMJctADBOZS5aBGCYyl+wCMUxkTtkFYpjInLIKxDCRuWUViGEic8sqEMNE5pZNIE/PPgwTmVc2gfhaFEvI6YjVBswsi0AME1lKFoE0vhbFQpIP5DBM3AUsIPlAPPtgSckH4mtRLCnpQAwTWVrSgRgmsrRkA+m77aZ3c87Ckg3kLh72cWwCFpRsIF7KQAqSDMRLGUhFkoEYJpKKVI9YbUACkgvkvrveefZBKpILpHdzTkKSCsQwkdQkFYhhIqlJKhDDRFKTTCCGiaQomUAME0lREoEYJpKqJAIxTCRVSQRimEiqFg/EMJGUXcTC9sPEPsjJL19fnvZzf98n86v94auLJs6QwhGrDUjUooEYJpK6Za8g3phI4hYLxNeiyMFigRgmkoPFAjFMJAeLBHLbXW3dnJODRQJZNWvfGiQLSx2x2oAMzB6Ir0WRk9kDMUwkJ7MGYphIbmYNZBUXNwEZmTWQtX+rJTOzBeKlDORotkC8lIEczRKIYSK5miUQw0RyNUsgTdOblpClyQPZDxMfE9kGZGjyQAwTydkcR6w2IFOTBmKYSO4mDcQwkdxNFohhIiWYLBDDREowWSCGiZRgkkAMEynFJIEYJlKK0QMxTKQkowdimEhJRg/EMJGSjBrI07MPw0TKMWog+69FBRRk7CNWG1CQ0QIxTKREowXS+FoUBRolkMMwcRdQmFEC8eyDUo0SiK9FUarBgRgmUrLBgRgmUrJBgfTddtO7OadggwK5i4d9HJuAQg0KxEsZKN3ZgXgpAzU4OxDDRGow5IjVBhTurEDuu+udZx8AAAAAAAAAAAAAAAAAAAAAAAAAwOL+BcH67Bny8ncOAAAAAElFTkSuQmCC)
![Matplotlib](https://img.shields.io/static/v1?label=Matplotlib&labelColor=007676&message=>=3.9.3&color=01C0C0&style=flat&logoColor=01C0C0&logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMjgiIGhlaWdodD0iMTI4IiBzdHJva2U9IiM3NzciIGZpbGwtb3BhY2l0eT0iLjgiPgo8cGF0aCBmaWxsPSIjRkZGIiBkPSJtNjMsMWE2Myw2MyAwIDEsMCAyLDB6bTAsMTRhNDksNDkgMCAxLDAgMiwwem0wLDE0YTM1LDM1IDAgMSwwCjIsMHptMCwxNGEyMSwyMSAwIDEsMCAyLDB6bTAsMTRhNyw3IDAgMSwwIDIsMHptNjQsN0gxbTEwOC00NS05MCw5MG05MCwwLTkwLTkwbTQ1LTE4djEyNiIvPgo8cGF0aCBmaWxsPSIjRjYwIiBkPSJtNTAsOC0yMCwxMCA2OCw5MiAxMC0xMEw2NCw2NHoiLz4KPHBhdGggZmlsbD0iI0ZDMCIgZD0ibTE3LDUwdjI4TDY0LDY0eiIvPgo8cGF0aCBmaWxsPSIjN0Y3IiBkPSJtNjQsNjQgNiwzNUg1OHoiLz4KPHBhdGggZmlsbD0iI0NGMyIgZD0ibTY0LDY0IDEzLTQwIDksNXoiLz4KPHBhdGggZmlsbD0iIzA0RiIgZD0ibTY0LDY0IDE0LTYgMSw0emwtMjYsMTMgMyw0eiIvPgo8L3N2Zz4=)
![Seaborn](https://img.shields.io/static/v1?label=seaborn&labelColor=007676&message=>=0.13.2&color=01C0C0&style=flat&logoColor=01C0C0&logo=)
![pmdarima](https://img.shields.io/static/v1?label=pmdarima&labelColor=007676&message=>=2.0.4&color=01C0C0&style=flat&logoColor=01C0C0&logo=)

## Usage

## 1) Time Series
- **Pre-built Models:** Includes popular time series forecasting models like ARIMA, SARIMA, torch, and more.
- **Seamless Integration:** Load data, preprocess, and run forecasting models in one place.
- **Automatic Forecasting:** Automatically generates forecasts for future time steps once a model is selected.
- **Visualization:** Built-in tools for visualizing both historical data and forecasted values.
- **Customizable:** Fine-tune model parameters to suit your specific use case.
- **Extensive Documentation:** Detailed guides and examples to help you get started.


#### Import SimpliML Time Series
```python
import pandas as pd
import simpliml.timeseriesforecast as tsf
```

#### Build Time Series Data
```python
sourceDF = pd.read_csv("") # Any Input data read
dataDF, futureDF = tsf.generateTSData(sourceDF, format='%Y-%m', freq='MS', periods=30)
```
Parameters:-
- format : str, optional 
  - Please refer [strftime-and-strptime-behavior](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior)
- freq : str, optional
  - Please refer [timeseries-offset-aliases](https://pandas.pydata.org/docs/user_guide/timeseries.html#timeseries-offset-aliases)
- periods : int, optional
  - Forcasting time period

#### Analysis Data
```python
tsf.analysisData(dataDF) # This will work only in interactive computational environment like Jupyter Notebook/lab/hub ..etc 
```

#### Build Model and forcast
```python
mdlResult = tsf.runModel(dataDF, futureDF, seasonal=12, modelApproach = 'FAST', testSize=80)  # Single Process Thread
(OR)
mdlResult = tsf.runThreadModel(dataDF, futureDF, seasonal=12, modelApproach = 'FAST', testSize=80) # Single Process Multiple Thread (Thread : CPU Count * 2)
(OR)
mdlResult = tsf.runProcessModel(dataDF, futureDF, seasonal=12, modelApproach = 'FAST', testSize=80) # Multiple Process (Process : CPU Count / 4) # Advise to use only in Windows  
```
Parameters:-
- seasonal : int, optional
  - The number of periods in a complete seasonal cycle, 
  - Example 
    -  1 : Yearly data
    -  2 : Half-yearly data
    -  4 : Quarterly data 
    -  7 : Daily data with a weekly cycle
    - 52 : Weekly Data
- modelApproach : ["BEST", "FAST"], optional
  - BEST : Best model build with multiple permutation and combination
  - FAST : Fast model build with limited permutation and combination
- testSize : int, optional
  - Test Size by defult 80:20 rule


#### Model Result Analysis
```python
mdlOutPut = tsf.modelResult(dataDF, mdlResult, modelApproach='Best') 
```
Parameters:-
- modelApproach : str, optional
  - BEST MAPE analysis report and can pass the model name, get the analysis report

""".format(python_requires, version, status.split()[-1], licenseType))



package_dir = {pckName: pckName}
packages = []
scripts = []
for dirname, dirnames, filenames in os.walk(pckName):
    if '__init__.py' in filenames:
        packages.append(dirname.replace('/', '.'))

for dirname, dirnames, filenames in os.walk(pckName):
    for filename in filenames:
        if filename.endswith('.py'):
            scripts.append(os.path.join(dirname, filename))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_requires = list(filter(None, [i.strip() for i in open("C:\\Users\\raja_\\OneDrive\\Projects\\pipTSF\\requirements.txt", "r", encoding="utf-8").readlines()]))

setuptools.setup(
    name=pckName,
    version=version,
    author=author,
    author_email=author_email,
    setup_requires=["datetime", "license", "setuptools"],
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=url,
    keywords = keywords,
    project_urls={
        "Issue Tracker": url + "/issues",
        "Changelog": url + "/blob/master/CHANGELOG.md"
    },
    classifiers=[
        status,
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        license.find(licenseType).python,
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"

    ],
    package_dir=package_dir,
    packages=packages,
    scripts=scripts,
    python_requires=python_requires,
    install_requires=install_requires,
)


# https://elmah.io/tools/base64-image-encoder/