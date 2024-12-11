This package computes the Lafler-Kinman statistic $\Theta$ for time-series data, incorporating the uncertainties of the flux/magnitude measurements.

## Installation

To install the package, run the following command:


pip install lk-stat-package




## Usage

### Importing the Package

Use the following line of code to import the package:


from lk_stat_package import lk_stat


### Computing the Lafler-Kinman Statistic

To compute the Lafler-Kinman statistic, use the `lk_stat` function as shown below:


theta = lk_stat(periods, magnitude, magnitude_err, time)


**Parameters:**
- periods: Array of trial periods.
- mag: Array of observed magnitudes.
- magerr: Array of magnitude uncertainties.
- Time: Array of observation times.

**Returns:**
- theta: The Lafler-Kinman statistic for each trial period.

Feel free to contact the author for any questions or contributions!


