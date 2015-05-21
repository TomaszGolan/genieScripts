#!/usr/bin/env python

import os                          # load OS interface
import sys                         # load system function
from lxml import etree             # load xml parser
from optparse import OptionParser  # load command line parser

def openConfigFile():
  # open UserPhysicsOptions.xml file
  global configFile # path to the file
  try: # first try $GENIE/config
    configFile = os.environ.get ("GENIE") + "/config/UserPhysicsOptions.xml"
    print "\nProcessing", configFile, "\n"
  except: # if $GENIE is not define use current directory
    configFile = os.environ.get ("PWD") + "/UserPhysicsOptions.xml"
    print "\n$GENIE is not defined, processing", configFile, "\n"

  global xmlTree
  try:  # try to open xml file
    xmlTree = etree.parse (configFile,
                           parser = etree.XMLParser (remove_comments = False))
  except:
    print "ERROR:", configFile, "could not be opened\n"
    sys.exit(1)

  return xmlTree.getroot() # return root element of xml tree

def optionList (limit):
  # list available parameters in UserPhysicsOptions.xml
  # limit -> how many parameters should be printed at the same time (0 - all)
  counter = 0
  for p in parameters: # loop over parameters
    print "[", p.attrib['type'].strip(), "]",
    print p.attrib['name'].strip(), "=", p.text.strip()
    counter += 1
    if counter == limit:
      counter = 0
      if raw_input ("\n[enter to continue, q to stop]: ") == 'q': break
      else: print

  sys.exit (0)

def processArguments (arguments = sys.argv[1:]):
  # create userOptions dictionary based on command line arguments
  # stop if there are no arguments or #arguments is odd
  if len (arguments) == 0 or len (arguments) % 2 != 0: usage()
  userOptions = {} # user options dictionary {"parameter": "value", ...}
  # loop over arguments (p - parameter, v - value)
  for p, v in zip(arguments[0::2], arguments[1::2]):
    # parameter must start with '--', value can not
    if v.startswith("--") or not p.startswith("--"): usage()
    if p == '--list': # if user called list
      try: N = int(v) # try to use v as no of lines to print
      except: N = 20  # if failed - print 20 lines by default
      optionList (N)  # print lines with N-length steps
    userOptions[p[2:]] = v # fill dictionary (skip '--')

  return userOptions

def setupParameters():
  # change parameters in UserPhysicsOptions.xml
  for p in parameters:  # loop over parameters
    pName = p.attrib['name'].strip()  # parameter name
    if pName in userOptions:  # check if user changed this parameter
      print pName, "=", p.text.strip(), "->", userOptions[pName]
      p.text = userOptions[pName] # change value
      del userOptions[pName]      # remove key from dictionary

def checkArguments():
  # check is some user options were not used
  if len (userOptions):
    print "WARNING: UserPhysicsOptions.xml does not have:",
    for o in userOptions: print o,
    print "\n"
    
def usage():
  print "\nUsage:\t" + "\033[1m" + "./setUserPhysicsOptions.py",
  print "--parameter1 value1 --parameter2 value2 ..." + "\033[0m"
  print "\nNote: do not use '=' (some parameters names contains '=')\n"
  print "Use " + "\033[1m" + "./setUserPhysicsOptions.py --list N",
  print "\033[0m" + "to see the list of available parameters. N is the number",
  print "of parameters printed at the same time (0 - print all)\n"
  sys.exit(0)

#MAIN PROGRAM
    
if __name__ == "__main__":
  # create global list of parameters from UserPhysicsOptions.xml file
  global parameters; parameters = openConfigFile().iter(tag='param')
  # get dictionary from command line arguments
  global userOptions; userOptions = processArguments ()
  # apply user changes
  setupParameters()
  # save UserPhysicsOptions.xml file
  try:
    xmlTree.write (configFile)
    print "\n", configFile, "saved\n"
  except:
    print "\n", configFile, "could not be saved\n"
  # check if some arguments were not used
  checkArguments()
