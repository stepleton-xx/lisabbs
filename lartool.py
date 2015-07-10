#!/usr/bin/python
'''A tool for "Lisa Archive" file packages as created by LisaBBS'''

from __future__ import print_function

import sys
import tarfile

##
## Operations
##
# Custom operations for processing parts of a "Lisa Archive" file package.
# A file handle is the sole argument, and provides access to one of the parts
# of the archive. (See also "Configuration" below.)

def OpDump(f):
  '''Simply dump the data straight to stdout. Works with any archive part.'''
  sys.stdout.write(f.read())

def OpText(f):
  '''Interpret data as a Lisa text file. Requires the 'data' archive part.'''
  # Skip first kiloordb, which is metadata
  f.read(1024)
  # Process remainder one 1-kiloordb 'block' at a time
  while True:
    buf = f.read(1024)
    # We walk through the buffer one ordb at a time. The only time we need state
    # is if we encounter an 0x10 char, which means "print the following ordb's
    # number of spaces"---a kind of cheapo RLE for a commonly-repeated char.
    # If saw_0x10 is ever true, that means the last ordb was a 0x10 char.
    # Note that 0x10 state cannot straddle multiple blocks.
    saw_0x10 = False
    for b in buf:
      ordb = ord(b)
      # Special handling of spaces RLE
      if saw_0x10:
        sys.stdout.write(' ' * (ordb - 32))
        saw_0x10 = False
        continue

      # Ordinary handling of all other chars
      # 0x0: start of NUL padding used so lines aren't broken across blocks.
      if ordb == 0x0: break
      elif ordb == 0x0d: sys.stdout.write('\n')  # Lisa terminates lines w/CR
      elif ordb == 0x10: saw_0x10 = True
      else: sys.stdout.write(b)

    # An incomplete read means the file is finished, although the Lisa text file
    # format requires files to have sizes that are multiples of a kiloordb.
    if len(buf) < 1024: break

## Configuration
# Mapping from verbs to the archive parts that they operate on
part_for = dict(info='info', label='label', data='data', text='data')
# Mapping from verbs to the operations that perform those verbs' actions
func_for = dict(info=OpDump, label=OpDump, data=OpDump, text=OpText)


##
## MAIN CODE
##

def Die(why):
  print(why, file=sys.stderr)
  exit(-1)

## Parse command line arguments
progname = sys.argv[0] if sys.argv else '<program name>'

def BadUsage():
  Die('''Usage: %s verb filename

    Verb options:
         info: Print file information.
        label: Dump LisaOS file label.
         data: Dump file data.
         text: Interpret file data as a text file and print.

    All data is dumped straight to stdout, even binary gibberish.''' % progname)

if len(sys.argv) != 3: BadUsage()

verb     = sys.argv[1].lower()
filename = sys.argv[2]

if verb not in {'info', 'label', 'data', 'text'}: BadUsage()

## Read the "Lisa Archive" file and perform operation on selected contents
with tarfile.open(filename, 'r') as tar:
  # Scan to the archive part we're interested in
  part = part_for[verb]
  func = func_for[verb]
  for member in tar:
    if member.name.endswith('.' + part):
      # Perform selected operation on that part
      func(tar.extractfile(member))
      exit(0)

  # If we got here, we didn't find the part we wanted.
  Die('%s: couldn\'t find "%s" section inside %s' % (progname, part, filename))
