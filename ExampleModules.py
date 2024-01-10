from icecube import icetray, dataclasses
import numpy as np

class ExampleGenerator(icetray.I3Module):
    """
    Example module that generates vector of random 
    numbers and stores them to DAQ frame
    """
    def __init__(self, context):
        """
        This is initialization function, where one defines parameters
        """
        icetray.I3Module.__init__(self, context)
        # Here is example of parameters 
        # the form is AddParameter(name, explanation, default value)
        self.AddParameter("Size", "Size of desired vector", 10)  
        self.AddParameter("Mean", "mean of gaussian", 0.0)
        self.AddParameter("Sigma", "sigma of gaussian", 1.0)
        self.AddParameter("Outname", "Name of output field", "RandomVector")
        self.AddParameter("NEvents", "Number of event frames to produce" , 100)
        self.AddOutBox('OutBox')    

    def Configure(self):
        """
        This function configures the module, for example - get parameters etc.
        """
        self.size = self.GetParameter("Size")
        self.mean = self.GetParameter("Mean")
        self.sigma  = self.GetParameter("Sigma")
        self.nevents = self.GetParameter("NEvents")
        self.outname = self.GetParameter("Outname")
        self.counter = 0
    def DAQ(self, frame):
        """
        This functions actually processes the frame
        """
        # let's do something - genrate random numbers
        numbers = np.random.normal(loc   = self.mean, 
                                   scale = self.sigma, 
                                   size  = self.size)
        # And now - store these random numbers to the frame
        frame[self.outname] = dataclasses.I3VectorDouble(numbers.tolist())
        # after that - we have to push 
        self.PushFrame(frame)
        # since this particular moduele is a generator
        # it has to stop once desired number of events is reached
        self.counter +=1
        if self.counter >= self.nevents:
            self.RequestSuspension()

class AveragingModule(icetray.I3Module):
    """
    Simple module that calculate average as an example 
    """
    def __init__(self, context):
        """
        This is initialization function, where one defines parameters
        """
        icetray.I3Module.__init__(self, context)
        # Here is example of parameters 
        # the form is AddParameter(name, explanation, default value)
        self.AddParameter("Input", "input name", "")  
        self.AddParameter("Output", "output name", "")
        self.AddOutBox('OutBox')   
    def Configure(self):
        """
        This function configures the module, for example - get parameters etc.
        """
        self.input = self.GetParameter("Input")
        self.output = self.GetParameter("Output")
    def DAQ(self, frame):
        """
        Processing of the frame
        """
        frame[self.output] = dataclasses.I3Double(np.mean(frame[self.input]) )
        self.PushFrame(frame)

#
def AveragingFunction(frame, input, output):
    frame[output] = dataclasses.I3Double(np.array(frame[input]).mean())
    # If function returns False, the frame will be dropped from the processing and ignored
    # Often this is how selection is applied
    return(True)
