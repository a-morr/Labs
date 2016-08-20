# solutions.py
"""Volume 2A: Fouier I (Discrete Fourier Transform). Solutions file."""


import scipy as sp
from scipy.io import wavfile
from scipy.fftpack import fft
from matplotlib import pyplot as plt


class Signal(object):
    """Class for storing and manipulating a sound wave."""
    def __init__(self, sample_rate, samples):
        self.rate = float(sample_rate)
        self.wave = sp.array(samples, dtype=sp.float32)

    def plot(self):
        # Fix the x axis
        self.dft = fft(self.wave, axis=0)
        time = sp.arange(0,len(self.wave))/self.rate
        cycles = self.rate*sp.arange(1,len(self.dft)+1)/len(self.wave)

        # Make the plots
        plt.subplot(121)
        plt.plot(time, self.wave)
        plt.subplot(122)
        plt.plot(cycles, sp.absolute(self.dft))
        plt.show()

    def export(self, filename):
        # Casting as reals and absolute maximum?
        scaled = sp.real(self.wave)
        scaled = sp.int16(scaled * 32676. / scaled.max())
        wavfile.write(filename, self.rate, scaled)

    def __add__(self, other):
        return Signal(self.rate, self.wave + other.wave)

    def append(self, other):
        self.wave = sp.append(self.wave, other.wave)

def generate_note(frequency, duration):
    """Generate a note with the specified frequency and duration.
    Return the soundwave packaged in an instantiation of the Signal class.
    """
    wave_function = lambda x: sp.sin(2*sp.pi*x*frequency)
    stepsize = 1./44100
    sample_points = sp.arange(0, duration, stepsize)
    samples = wave_function(sample_points)
    return Signal(44100, samples)

def DFT(vec):
    """A naive implementation of the Discrete Fourier Transform.

    Parameters:
        vec (array_like): The 1 x N-1 vector [f(0),f(1),...,f(N-1)].

    Returns:
        c (ndarray): The 1 x N-1 vector of the DFT of 'vec'.
    """

    vec = sp.array(vec, dtype=sp.complex128) # CAST AS COMPLEX
    N = len(vec)
    c = sp.zeros(N, dtype=sp.complex128)
    for k in xrange(N):
        c[k] = sp.sum(sp.exp((-2*sp.pi*1j*k*sp.arange(N))/N)*vec)
        c[k] = (vec * sp.exp(-2*sp.pi*1j*k*sp.arange(N))).sum()
    return c

def generate_chord():
    C = generate_note(523.25, 2)
    E = generate_note(659.25, 2)
    G = generate_note(783.99, 2)
    chord = C + E + G
    chord.export("chord1.wav")
    chord.append(chord + generate_note(587.33,2))
    chord.export("chord2.wav")
    #chord.plot()

# Old Solutions ---------------------------------------------------------------

def prob1(freq=60, length=1):
    """Generates a sine wave, saves it as a .wav file, and uses plot_signal()
        to plot the signal.

    Parameters
    ----------
    freq : integer, optional
        The fequency of the sine wave. Defaults to 60.
    length : integer, optional
        The number of seconds the sine wave lasts. Defaults to 1.

    Returns
    -------
    None
    """

    samplerate = 44100
    stepsize = freq*2*sp.pi/samplerate
    signal = sp.sin(sp.arange(0, stepsize*length*samplerate, stepsize))
    scaled_signal = sp.int16(signal/sp.absolute(signal).max() * 32767)
    wavfile.write('problem1.wav', samplerate, scaled_signal)
    #plot_signal('problem1.wav')

#=============================================================================
# PROBLEM 2 - Naive DFT
#=============================================================================
def prob2(vec, verbose=False):
    """A naive implementation of the Discrete Fourier Transform.

    Parameters
    ----------
    vec : array_like
        The 1 x N-1 vector [f(0),f(1),...,f(N-1)].
    verbose : boolean, optional
        If True, prints out whether or not the DFT was successful,
        comparing with scipy.fft(). Defaults to False.

    Returns
    -------
    c : array_like
        The 1 x N-1 vector of the DFT of 'vec'.
    """

    vec = sp.array(vec, dtype=sp.complex128)
    N = len(vec)
    c = sp.zeros(N, dtype=sp.complex128)
    for k in xrange(N):
        c[k] = 1./N*sp.sum(sp.exp((-2*sp.pi*1j*k*sp.arange(N))/N)*vec)
        #c[k] = (vec * sp.exp(-2*sp.pi*1j*k*sp.arange(N)/N)).sum()
    if verbose:
        if sp.allclose(sp.fft(vec)/float(N), c): print("Success!")
        else: print("Failure!")
    return c

#=============================================================================
# PROBLEM 3
#=============================================================================
def prob3(filename='pianoclip.wav'):
    """Plots the spectrum of a given .wav file, then calculates the location
    and value of the largest spike. For the default value, the exact value is
    742.281519994 Hz (f#5 + 5 cents)

    Parameters
    ----------
    filename: string, optional
        The name of the .wav sound file to be examined.
        Defaults to 'pianoclip.wav'.

    Returns
    -------
    None
    """
    #plot_signal(filename)
    rate, signal = wavfile.read(filename)
    signal = sp.float32(signal)
    #fsignal = sp.absolute(fftw.fft(signal.T).T)
    # Use if scipy_fftpack is unavailable
    fsignal = sp.absolute(fft(signal, axis=0))
    plt.plot(fsignal)
    plt.title("Spectrum of %s"%filename)
    plt.show()
    loc = fsignal[1:].argmax()
    val = fsignal[1:].max()
    print("\nSpike location:\t",loc)
    print("Spike value:\t",val)
    print("Hz:\t\t",float(loc*rate)/signal.shape[0])

#==============================================================================
# Problem 4
#==============================================================================
def prob4(filename='saw.wav', new_rate = 11025, outfile='prob4.wav'):
    """Down-samples a given .wav file to a new rate and saves the resulting
    signal as another .wav file.

    Parameters
    ----------
    filename : string, optional
        The name of the .wav sound file to be down-sampled.
        Defaults to 'saw.wav'.
    new_rate : integer, optional
        The down-sampled rate. Defaults to 11025.
    outfile : string, optional
        The name of the new file. Defaults to prob4.wav.

    Returns
    -------
    None
    """
    old_rate, in_sig = wavfile.read(filename)
    fin = fftw.fft(sp.float32(in_sig))
    # Use if scipy_fftpack is unavailable
    # fin = sp.fft(sp.float32(in_sig))
    nsiz = sp.floor(in_sig.size * new_rate / old_rate)
    nsizh = sp.floor(nsiz / 2)
    fout = sp.zeros(nsiz) + 0j
    fout[0:nsizh] = fin[0:nsizh]
    fout[nsiz-nsizh+1:] = sp.conj(sp.flipud(fout[1:nsizh]))
    out = sp.real(sp.ifft(fout))
    out = sp.int16(out/sp.absolute(out).max() * 32767)
    plot_signal(filename)
    wavfile.write('prob4.wav',new_rate,out)
    print("")
    plot_signal('prob4.wav')

