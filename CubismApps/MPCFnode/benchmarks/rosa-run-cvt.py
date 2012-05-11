import sys
import re
import os

#this is my shit
import runcvt

print 'usage: python rosa-run-cvt.py gcc <desired-time-in-minutes> <path-to-IC>'

if len(sys.argv) > 4:
	print('Error: passing more arguments than allowed. Aborting now.')
	sys.exit("Aborting because of errors!")
	
print "Args are:"
for x in sys.argv: print x
	
stage = "gcc"
if len(sys.argv) > 1:
	if re.search("gcc", sys.argv[1]) == None:
		print('No match for the first argument')
		sys.exit("Aborting because of errors!")
	else:
		stage = sys.argv[1]

tdesired_seconds = 5.*60
if len(sys.argv) >= 3:
	tdesired_seconds = float(sys.argv[2])*60;
	
path_to_ic = "."
if len(sys.argv) >= 4:
	path_to_ic = str(sys.argv[3]);
	
getnodedata = os.popen('hostname ; date \'+-%y-%m-%d-%H_%M_%S\'')
nodedata = ("result-" + getnodedata.readline() + getnodedata.readline()).replace('\n', '')
common = " source /opt/modules/default/init/bash ;  \
< module load PrgEnv-gnu ; \
< export LD_LIBRARY_PATH=/apps/rosa/intel/composerxe-2011.3.174/tbb/lib/intel64/cc4.1.0_libc2.4_kernel2.6.16.21/:/users/petrosk/hdf5-1.8.8_icc_serial/lib/:/users/petrosk/VTK/lib/vtk-5.8/:$LD_LIBRARY_PATH; \
< export OMP_NUM_THREADS=32 ;  "

threads = [32, 2];
runargs = " -ncores 16  -dumpperiod 100000000 -saveperiod 100000000 -ascii 0 -awk 0 -bubx 0.2 -buby 0.5 -bubz 0 -cfl 0.6 -g1 1.4 -g2 1.667 -gr 0 \
-mach 1.2 -mollfactor 2 -pc1 0 -pc2 0 -rad 0.05 -reinit 0 -reinitfreq 1000 -report 5 -restart 1 -shockpos 0.1 \
-sim cvt -sten 0 -sumrho 3 -tend 2.0 -verb 1 -vp 0 -re 1000 -nu1 1.941574781e-4 -fpath " + path_to_ic

threads_per_node = 8

if re.search("gcc", stage) != None:
	runcvt.run(runargs, tdesired_seconds, "33.6", "60.", common + " module load gcc/4.6.1; ", "./rosa-cvt-exec-gcc461/", nodedata+"-gcc461", "", threads, threads_per_node)

#for the moment not supported	
#if re.search("icc", stage) != None:
#	runcvt.run(runargs, tdesired_seconds, "844.8", "96.", common + " module load intel/12; ", "./brutus-exec-icc12/", nodedata+"-icc12", "", threads, threads_per_node)
