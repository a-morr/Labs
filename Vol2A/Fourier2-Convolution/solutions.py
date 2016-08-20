# solutions.py
"""Filtering and Convolution solutions file."""

import scipy as sp
from scipy.io import wavfile
from matplotlib import pyplot as plt


# Problem 1: Implement this function.
def clean_signal(outfile='prob1.wav'):
    """Clean the 'Noisysignal2.wav' file. Plot the resulting sound
    wave and write the resulting sound to the specified outfile.
    """

    rate,data = wavfile.read('Noisysignal2.wav')
    fsig = sp.fft(data,axis = 0)
    f = sp.absolute(fsig)
    plt.plot(f[0:f.shape[0]/2])
    for j in xrange(14020,50001):
        fsig[j]=0
        fsig[-j]=0

    newsig=sp.ifft(fsig)
    f = sp.absolute(fsig)
    plt.figure()
    plt.plot(f[0:f.shape[0]/2])
    plt.show()
    plt.close()
    newsig = sp.ifft(fsig).astype(float)
    scaled = sp.int16(newsig/sp.absolute(newsig).max() * 32767)
    wavfile.write(outfile,rate,scaled)


# Problem 2 is not required. Use balloon.wav for problem 3.


# Problem 3: Implement this function
def convolve(source='chopin.wav', pulse='balloon.wav', outfile='prob3.wav'):
    """Convolve the specified source file with the specified pulse file,
    then write the resulting sound wave to the specified outfile.
    """
    '''
    rate1,sig1 = wavfile.read(source)
    n = sig1.shape[0]
    rate2,sig2 = wavfile.read(pulse)
    m = sig2.shape[0]
    sig1 = sp.append(sig1,sp.zeros((m,2)))
    sig2 = sp.append(sig2,sp.zeros((n,2)))
    f1 = sp.fft(sig1)
    f2 = sp.fft(sig2)
    out = sp.ifft((f1*f2))
    out = sp.real(out)
    scaled = sp.int16(out/sp.absolute(out).max() * 32767)
    wavfile.write(outfile, rate1, scaled)
    '''

    # Read in the files
    rate1, signal  = wavfile.read(source)
    rate2, impulse = wavfile.read(pulse)
    
    # pad signal with zeros
    sig = sp.zeros((signal.shape[0]+impulse.shape[0],2))
    sig[:len(signal)] = signal
    imp = sp.zeros_like(sig)
    imp[:len(impulse)] = impulse
    
    # fourier transforms (we HAVE to have a warning box about the axis=0 stuff)
    f1 = sp.fft(sig, axis=0)
    f2 = sp.fft(imp, axis=0)
    out = sp.ifft(f1*f2, axis=0)
    
    # prepping output and writing file
    out = sp.real(out)
    scaled = sp.int16(out/sp.absolute(out).max() * 32767)
    wavfile.write(outfile, rate1, scaled)


# Problem 4: Implement this function.
def white_noise(outfile='prob4.wav'):
    """Generate some white noise, write it to the specified outfile,
    and plot the spectrum (DFT) of the signal.
    """
    samplerate = 22050
    # Create 10 seconds of mono white noise
    noise = sp.int16(sp.random.randint(-32767,32767,samplerate*10)) 
    wavfile.write(outfile,22050,noise)
    f = sp.fft(sp.float32(noise))
    plt.plot(sp.absolute(f))
    plt.show()


# Problem 5 (removed for now)
def prob5():
    rate, sig = wavfile.read('tada.wav')
    sig = sp.float32(sig)
    noise = sp.float32(sp.random.randint(-32767,32767,sig.shape))
    out = sp.ifft(sp.fft(sig)*sp.fft(noise))
    out = sp.real(out)
    out = sp.int16(out/sp.absolute(out).max() * 32767)
    wavfile.write('white-conv.wav',rate,out)


# END OF SOLUTIONS ============================================================

from os import system
from sys import stdout

# Test script
def test(student_module):
    """Test script. Import the student's solutions file as a module.
    
    10 points for problem 1
    20 points for problem 3
    10 points for problem 4
    
    Inputs:
        student_module: the imported module for the student's file.
    
    Returns:
        score (int): the student's score, out of 40.
        feedback (str): a printout of test results for the student.
    """
    tester = _testDriver()
    tester.test_all(student_module)
    return tester.score, tester.feedback

def _autoclose(func):
    """function decorator for closing figures automatically."""
    def wrapper(*args, **kwargs):
        plt.ion()
        result = func(*args, **kwargs)
        plt.close('all')
        plt.ioff()
        return result
    return wrapper

class _testDriver(object):
    """Class for testing a student's work. See test.__doc__ for more info."""

    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize the feedback attribute."""
        self.feedback = ""

    # Main routine -----------------------------------------------------------
    def test_all(self, student_module, total=40):
        """Grade the provided module on each problem and compile feedback."""
        # Reset feedback and score.
        self.feedback = ""
        self.score = 0

        def test_one(problem, number, value):
            """Test a single problem, checking for errors."""
            try:
                self.feedback += "\n\nProblem %d (%d points):"%(number, value)
                points = problem(student_module)
                self.score += points
                self.feedback += "\nScore += %d"%points
            except BaseException as e:
                self.feedback += "\n%s: %s"%(self._errType(e),e)

        # Grade each problem.
        test_one(self.problem1, 1, 10)  # Problem 1: 10 points.
        test_one(self.problem3, 2, 20)  # Problem 3: 20 points.
        test_one(self.problem4, 3, 10)  # Problem 4: 10 points.

        # Report final score.
        percentage = (100. * self.score) / total
        self.feedback += "\n\nTotal score: %d/%d = %s%%"%(
                                    self.score, total, percentage)
        if   percentage >=  98: self.feedback += "\n\nExcellent!"
        elif percentage >=  90: self.feedback += "\n\nGreat job!"

        # Add comments (optionally).
        print(self.feedback)
        comments = str(raw_input("Comments: "))
        if len(comments) > 0:
            self.feedback += '\n\n\nComments:\n\t%s'%comments

    # Helper Functions --------------------------------------------------------
    @staticmethod
    def _errType(error):
        """Get just the name of the exception 'error' in string format."""
        if isinstance(error, BaseException):
            return str(type(error)).lstrip("<type 'exceptions.").rstrip("'>")
        else:
            return str(error)

    def _grade(self, points, message=None):
        """Manually grade a problem worth 'points'. Return the score."""
        credit = -1
        while credit > points or credit < 0:
            try:
                credit = int(input("Score out of %d: "%points))
            except:
                credit = -1
        if credit != points:
            # Add comments (optionally),
            comments = raw_input("Comments: ")
            if len(comments) > 0:
                self.feedback += "\n%s"%comments
            # Or add a predetermined error message.
            elif message is not None:
                self.feedback += "\n%s"%message
        return credit

    # Problems ----------------------------------------------------------------
    @_autoclose
    def problem1(self, s):
        """Test clean_signal(). 10 points."""
        if not hasattr(s, "clean_signal"):
            raise NotImplementedError("Problem 1 Incomplete")

        print("\nCleaned plot\t\t"),
        s.clean_signal("prob1.wav")
        points  = self._grade(5, "Incorrect plot of cleaned signal")
        print("Cleaned sound\t\t"),; stdout.flush()
        system("afplay prob1.wav")
        points += self._grade(5, "Signal wasn't cleaned adequately")
        system("rm prob1.wav")
        return points

    def problem3(self, s):
        """Test convolve(). 20 points."""
        if not hasattr(s, "convolve"):
            raise NotImplementedError("Problem 1 Incomplete")

        print("\nRunning convolve()..."),; stdout.flush()
        s.convolve(outfile="prob3.wav")
        print("done.")
        system("afplay prob3.wav")
        points = self._grade(20, "Signal wasn't convolved adequately")
        system("rm prob3.wav")
        return points

    @_autoclose
    def problem4(self, s):
    	"""Test white_noise(). 10 points."""
        if not hasattr(s, "white_noise"):
            raise NotImplementedError("Problem 4 Incomplete")

        print("\nwhitenoise DFT\t\t"),
        s.white_noise("prob4.wav")
        points = self._grade(5, "Incorrect DFT plot")
        print("whitenoise sound\t"),; stdout.flush()
        system("afplay prob4.wav")
        points += self._grade(5, "Incorrect whitenoise")
        system("rm prob4.wav")
        return points
