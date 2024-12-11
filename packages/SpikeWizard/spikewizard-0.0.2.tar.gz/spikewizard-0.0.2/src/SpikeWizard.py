import scipy.signal as signal
import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.ndimage import gaussian_filter1d
import inspect
from typing import Callable
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

class SpikeFinder:
    
    def __init__(self, data, mode = 'auto', filter = True, function : str | Callable = "gaussian", **kwargs):
        """
        __init__ _summary_

        Parameters
        ----------
        data : _type_
            _description_
        mode : str, optional
            _description_, by default 'auto'
        filter : bool, optional
            _description_, by default True
        function : str | Callable, optional
            _description_, by default "gaussian"
        """        
        self.data = data
        self.kwargs = kwargs
        self.mode = mode
        self.kwrags = kwargs
        self.function = function

        self.status_check()
        self.filter = filter
        self.__dict__.update(kwargs)
        
        if mode == 'auto':
            self.find_heights()
            self.find_widths()
        self.spikes = self.find_spikes()
    
    def status_check(self):
        
        mode = self.mode
        kwargs = self.kwargs

        VALID_STATUS = {'auto', 'manual'}
        VALID_FUNCTION = ['gaussian', 'Lorentzian']
        
        if mode not in VALID_STATUS:
            raise ValueError("results: status must be one of %r." % VALID_STATUS)
        
        if bool(kwargs) and mode == 'auto':
            raise ValueError("results: mode auto does not accept any keyword arguments.")
        
        if not bool(kwargs) and mode == 'manual':
            raise ValueError("results: mode manual requires keyword arguments, based on the scipy.signal.find_n_peaks documentation.")
        if self.function not in VALID_FUNCTION and not callable(self.function):
            raise ValueError("results: function must be one of %r." % VALID_FUNCTION)
        
        if callable(self.function) and set(['mean_position', 'width', 'amplitude']).issubset(inspect.signature(self.function).parameters.keys()):
            raise ValueError("results: function must be a callable with width and height .")
            
    def find_heights(self):
        
        self.heights = np.std(self.data) 
    
    def find_widths(self) :
        if self.filter:
            self.data_filtered = gaussian_filter1d(self.data, self.data.std() * 10)
        x = np.arange(len(self.data))
        y_spl = UnivariateSpline(x,self.data_filtered,s= 2,k=3)
        
        mask = y_spl.derivative(n=2)(x)  < 0
        
        mask2 = mask[1:] != mask[:-1] #find the edges of the mask
        
        widths_spline = np.arange(len(x) - 1)[mask2][1:] - np.arange(len(x) - 1)[mask2][:-1]
        self.widths = (np.min(widths_spline)/2, np.max(widths_spline) * 2)

    def find_spikes(self):
        # Find the indices of the spikes
        return signal.find_peaks(self.data_filtered, height=self.heights, width = self.widths)
    
    @property
    def spike_indices(self):
        return self.spikes[0]
    
    @property
    def spike_properties(self):
        return self.spikes[1]
    
    def get_spike_count(self):
        return len(self.spike_indices)
    
    def get_spike_rate(self):
        return self.get_spike_count() / (len(self.data) / 1000)
    
    def get_spike_amplitudes(self):
        return self.data[self.spike_indices]
    
    def get_spike_waveforms(self):
        #TODO: Use the left and right bases to get the waveforms
        waveforms = []
        for idx in self.spike_indices:
            window_size = self.spike_properties['widths'][idx]
            start = idx - window_size
            end = idx + window_size
            if start < 0 or end >= len(self.data):
                continue
            waveforms.append(self.data[start:end])
        return np.array(waveforms)

class Fitter(SpikeFinder) :
    
    def __init__(self, data, mode='auto', filter=True, function: str | Callable = "gaussian", **kwargs):
        """
        __init__ _summary_

        Parameters
        ----------
        data : _type_
            _description_
        mode : str, optional
            _description_, by default 'auto'
        filter : bool, optional
            _description_, by default True
        function : str | Callable, optional
            _description_, by default "gaussian"
        """        
        super().__init__(data, mode, filter, function, **kwargs) 
        self.available_function = {'gaussian': self.gaussian, 'Lorentzian': self.Lorentzian, 'custom': self.function}
        if function is not callable : 
            self.function = self.available_function[function]
            
      
        
    def gaussian(self, x, a, x0, sigma):
        return a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))
    
    def Lorentzian(self, x, a, x0, gamma):
        return a * gamma ** 2 / ((x - x0) ** 2 + gamma ** 2)
    
    @property
    def fit(self, **kwargs):
        
        def func(x, *params):
        
            y = np.zeros_like(x, dtype=float)
            
            for i in range(0, len(params), 3):
                
                A = params[i]
                x0 = params[i + 1]
                typical_width = params[i+2]
                y += self.function(x, A, x0, typical_width)
                
            return y
        
        initial_positions = self.spike_indices
        initial_amplitudes, initial_widths = self.spike_properties['peak_heights'], self.spike_properties['widths']
        
        position_unc = self.spike_properties['right_bases'] - self.spike_properties['left_bases']
        
        #TODO: Tackle the uncertainty in the width and amplitude
        
        initial_params = np.ravel([[initial_amplitudes[i],initial_positions[i], initial_widths[i]] for i in range(len(initial_amplitudes))])
        bounds_inf = np.ravel([[initial_amplitudes[i] / 2, initial_positions[i]-position_unc[i], initial_widths[i]/2] for i in range(len(initial_amplitudes))])
        bounds_sup = np.ravel([[initial_amplitudes[i] * 2, initial_positions[i]+position_unc[i], initial_widths[i]*2] for i in range(len(initial_amplitudes))])
        
        self.params, self.cov = curve_fit(func, np.arange(len(self.data)), self.data,p0 = initial_params, maxfev=10000, bounds= [bounds_inf, bounds_sup])
        
        return func(np.arange(len(self.data)), *self.params)

    def plot_fit(self, ax : bool | plt.Axes = False, **kwargs):
        
        #TODO: Add the possibility to customize the plot with kwargs
        if not ax:
            
            fig, ax = plt.subplots()
            
            ax.plot(self.data, lw = .3, label = 'raw')
            ax.plot(self.data_filtered, label = 'filtered_data')
            ax.plot(self.spike_indices, self.data[self.spike_indices], 'o', label='spikes')
            ax.plot(self.fit, label='Fit') 
            ax.legend()
        
        else : 
                
            ax.plot(self.data, lw = .3, label = 'raw')
            ax.plot(self.data_filtered, label = 'filtered_data')
            ax.plot(self.spike_indices, self.data[self.spike_indices], 'o', label='spikes')
            ax.plot(self.fit, label='Fit')
            for i in range(0, len(self.params), 3):
                ax.plot(np.arange(len(self.data)), self.function(np.arange(len(self.data)), *self.params[i:i+3]), label = f'Fit {i//3}', lw = .9, ls = ':') 
            ax.legend()
            ax.xaxis.set_visible(False)
            ax2 = ax.inset_axes([0, -.3, 1, 0.25], sharex=ax)
            ax2.set_title('Residuals')
            ax2.semilogy(self.data  - self.fit, alpha = 0.5, lw = 0, marker = 'o', markersize = 2)
            ax2.xaxis.set_visible(False)
            
        return ax