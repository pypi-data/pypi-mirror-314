# SpikeWizard: Automated Spike Fitting for Raw Signal Analysis

## Introduction:

SpikeWizard is an advanced Python package designed to automate the process of fitting spikes in raw signals. It offers a comprehensive framework for analyzing signals containing spikes of various types and fitting them to a specified function. SpikeWizard harnesses cutting-edge algorithms and techniques to identify and fit multiple spikes within a signal seamlessly, eliminating the need for manual intervention in setting initial conditions.

## Demo

![example](https://raw.githubusercontent.com/Chatr0uge/SpikeWizard/main/images/image.png)

## Installation

```bash
pip install SpikeWizard
```

## Key Features:

1. Automated Spike Identification: SpikeWizard employs sophisticated algorithms from **scipy** to automatically detect spikes within raw signal data. These algorithms are robust and adaptable, capable of handling various signal characteristics and noise levels. Typical from a signal noise ration varying between : $0 \to 0.3$, which is quite reasonable for experimental data.

2. Flexible Function Types: The package supports fitting spikes to a wide range of function types, providing flexibility to accommodate different signal profiles and experimental requirements. Users can specify the desired function type based on their data characteristics and analysis objectives.

3. Multi-Spike Fitting: SpikeWizard excels at fitting multiple spikes within the same signal simultaneously. This feature enhances efficiency by enabling users to analyze complex signals containing multiple spike occurrences without the need for iterative processing.

4. Automatic Initial Condition Determination: SpikeWizard automatically determines initial conditions for spike fitting, eliminating the manual effort typically required to set initial parameters. This streamlines the analysis process and reduces user intervention.

5. Customizable Parameters: While SpikeWizard automates many aspects of spike fitting, it also offers users the flexibility to customize fitting parameters according to their specific requirements. This includes options to adjust algorithm parameters, function properties, and fitting constraints. This Customization handles **find_peaks** parameters from **scipy.signal**

6. Visualization Tools: The package provides visualization tools to facilitate comprehensive analysis and interpretation of fitted spikes. Users can visualize the original signal overlaid with fitted spikes, along with diagnostic plots to assess the quality of fitting and evaluate model performance.

## Usage Example:

```python
from SpikeWizard import Fitter

# Load raw signal data
raw_signal = ...

# Specify function type for spike fitting
def function(x, amp, x_0, typical_width) : ...

# Fit spikes automatically with SpikeWizard
fitter = Fitter(raw_signal, function_type)
fitted_spikes = Fitter.fit

# Visualize original signal and fitted spikes
Fitter.plot_fit()
```

## Documentation

For the moment there are only two predefined function implemented in SpikeWizard, both are commonly used in physics and chemical fields, which is the main audience of this package. The first function is a simple gaussian, and the other am amplitude dependant Lorentzian.

- $\mathcal{G}(x) = a \exp(-\frac{(x - \mu)^2}{2 \sigma^2})$
- $\mathcal{L}(x) = a  \frac{\Gamma^2}{((x - x0)^2 + \Gamma^2)}$

However, the user is free to implement his own spike function as long as its main arguments are **amplitude**, **width**, **position**, it will be well handled by the package

## Conclusion:

SpikeWizard revolutionizes spike fitting in raw signal analysis by offering a powerful and automated solution that caters to diverse research needs. Its ability to handle various spike types, fit multiple spikes simultaneously, and determine initial conditions automatically makes it an invaluable tool for researchers and practitioners in fields such as neuroscience, signal processing, and beyond. With SpikeWizard, analyzing spike data becomes more efficient, accurate, and accessible, empowering users to extract meaningful insights from their signals effortlessly.

## Collaboration

# TODO :

- use left and right bases to compute the waveforms
- develop mathematically the spline decomposition and special case
- Uncertainties on widths and amplitudes
- Benchmarks on various number of spikes, SNR
- Fix the Spline decomposition parameter
- Fix The Filtering parameters
- ~~Implement residuals analysis~~
