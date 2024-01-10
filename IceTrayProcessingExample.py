#!/usr/bin/env python3
import os, sys 
from optparse import OptionParser

usage = "usage: %prog [options]"
parser = OptionParser(usage)
parser.add_option("-n", "--nevents",type=int, default=1,
                  dest="NEVENTS", help="Number of events to produce")
parser.add_option("-o", "--outfile", type=str,default="output.i3.bz2",
                  dest="OUTFILE", help = "Name of outfile ")

(options,args) = parser.parse_args()
if len(args) != 0:
        message = "Got undefined options:"
        for a in args:
                message += a
                message += " "
        parser.error(message)
# creating tray
from icecube import icetray, dataio
tray = icetray.I3Tray()
tray.AddModule("I3InfiniteSource","streams",
                Stream=icetray.I3Frame.DAQ,
               )
### loading example generation module and adding to "chain"
from ExampleModules import ExampleGenerator
tray.AddModule(ExampleGenerator, 
               Size=1000, 
               Mean=0.0, 
               Sigma = 10.0, 
               Outname ="RandomVector",
               Nevents = options.NEVENTS)
# And here is the "processing module"
from ExampleModules import AveragingModule
tray.AddModule(AveragingModule, 
               Input="RandomVector",
               Output ="AverageFromModule"
               )
# And processing module defined as simple python function
from ExampleModules import AveragingFunction
tray.AddModule(AveragingFunction, 
               Input="RandomVector",
               Output ="AverageFromFunction", 
               Streams = [icetray.I3Frame.DAQ]
               )
### Module that writes the output
tray.AddModule("I3Writer","writer",
    Filename = options.OUTFILE,
    Streams = [icetray.I3Frame.DAQ],
    )

tray.Execute()
print("Done")
