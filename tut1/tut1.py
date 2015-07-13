'''
Python script for Casper Tutorial 1
Author: Tyrone van Balla (SKA Africa), July 2015
Updated for 2016 CASPER Workshop. Updated Tutorial 1 for use on ROACH2 and to use casperfpga library
'''

import casperfpga, time, struct, sys, logging, socket

# set default fpg file
fpgfile = 'tut1_updated_2015.fpg'

def exit_fail():
	print 'FAILURE DETECTED. Log entries:\n'
	exit()

def exit_clean():
    try:
        for f in fpgas: f.stop()
    except: pass
    exit()

# get command line arguments
if __name__ == '__main__':
    from optparse import OptionParser

    p = OptionParser()
    p.set_usage('tut1_updated.py <ROACH_HOSTNAME_or_IP> [options]')
    p.set_description(__doc__)
    p.add_option('-f', '--fpgfile', dest='fpg', type='str', default=fpgfile,
        help='Specify the fpg file to load')  
    opts, args = p.parse_args(sys.argv[1:])

    if args==[]:
        print 'Please specify a ROACH board. \nExiting.'
        exit()
    else:
        roach2 = args[0]
    if opts.fpg != '':
        fpgfile = opts.fpg

# instantiate fpga object
print('Connecting to server %s... '%(roach2)),
fpga = casperfpga.katcp_fpga.KatcpFpga(roach2)
time.sleep(1)

if fpga.is_connected():
	print 'ok\n'
else:
 	print 'ERROR connecting to server %s.\n'%(roach2)
 	exit_fail()

# upload fpg file to ROACH2 and program
print '---------------------------' 
print 'Programming FPGA...',
sys.stdout.flush()
fpga.upload_to_ram_and_program(fpgfile)
time.sleep(10)
print 'ok'

# get variables to assign to registers to be used in adder
print '---------------------------' 
print 'Enter values for adder: \n'
var_a = int(raw_input("Enter a value for a: "))
var_b = int(raw_input("Enter a value for b: "))
print '\n'    
print 'Assigning values to registers. . . .',
try:
	fpga.write_int('a', var_a)
	fpga.write_int('b', var_b)
except:
	print "ERROR writing values to registers"
	exit_fail()

print 'ok\n'
print '---------------------------'
print 'Reading value from sum_a_b: output from adder: ',
try:
	print fpga.read_int('sum_a_b')
except:
	print "ERROR reading from register"
	exit_fail()
print 'Read adder output ok'
print '---------------------------\n'

counter_en = raw_input("Enable counter? (y/n): ")
if counter_en == 'y':
	print "Enabling counter . . .",
	fpga.write_int('counter_ctrl', 1)
	print 'ok'
else:
	print "Demo completed. . . exiting...."
	exit_clean()

try:
	print "Outputting counter values periodically... press Ctrl+C to stop (only press it once!)"
	
	while True:
		print "\nCounter value: ",
		print fpga.read_int('counter_value')
		time.sleep(2)

except KeyboardInterrupt:
    print "\nStopping . . . . ",
    
print 'ok\n'
print '---------------------------\n'

counter_reset = raw_input("Reset counter? (y/n): ")
if counter_reset == 'y':
	print "Resetting counter . . .",
	fpga.write_int('counter_ctrl', 2)
	print 'ok\n'
else:
	print "Demo completed. . . exiting...."
	exit_clean()

print "New counter value: ",
print fpga.read_int('counter_value')

print "\n\nDemo completed . . . exiting. . . ."
exit_clean()