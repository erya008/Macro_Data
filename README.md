# Nowcasting-Python

The repository contains Python code that is translated from a Matlab code which produces a dynamic factor model. The Matlab code and the model
belong to the [Federal Reserve Bank of New York](https://github.com/FRBNY-TimeSeriesAnalysis/Nowcasting),
 developed by [Eric Qian](https://github.com/eric-qian) and
[Brandyn Bok](https://github.com/brandynbok). Please visit their [repository](https://github.com/FRBNY-TimeSeriesAnalysis/Nowcasting) for further details.

The Matlab code being translated implements the nowcasting framework described in "[Macroeconomic Nowcasting and Forecasting with Big Data](https://www.newyorkfed.org/research/staff_reports/sr830.html)" by Brandyn Bok, Daniele Caratelli, Domenico Giannone, Argia M. Sbordone, and Andrea Tambalotti, *Staff Reports 830*, Federal Reserve Bank of New York (prepared for Volume 10 of the *Annual Review of Economics*).

## File and folder description

* `data/` : example US data downloaded from [FRED](https://fred.stlouisfed.org/)
* `Functions/` : functions for loading data, estimating model, and updating predictions
* `example_DFM.py` : example script to estimate a dynamic factor model (DFM) for a panel of monthly and quarterly series
* `example_Nowcast.py` : example script to produce a nowcast or forecast for a target variable, e.g., real GDP growth
* `ResDFM.pickle` : example DFM estimation output
* `Spec_US_example.xls` : example model specification for the US

## NOTICE:
This repository is not associated Federal Reserve Bank of New York. 
I am not well versed in dynamic factor modeling but the reason I created this repository was to challenge myself and I thought it would be cool to convert a model from matlab to python. So feel free to use it for academic purposes but make sure you give proper credit to [Eric Qian](https://github.com/eric-qian) and
[Brandyn Bok](https://github.com/brandynbok). 

The repository is in its early stages and requires further improvements such as optimizing functions and writing clearer syntax with proper formatting. I'm not sure when I will get to this as I moved away from time series and started focusing on deep learning. My apologies for any inconviences. Feel free to post any technical issues that you encountered and I'll try my best to respond promptly.

Thanks,

MK
