echo off

rem  This simulator script example requires Python on the PATH.
rem  It can be installed with, e.g., a Windows installer, via Cygwin, or MSYS.

rem Configure full path to Dakota bin folder, which is needed to run dprepro
set dakota_install=c:\dakota\6.13\

rem  --------------
rem  PRE-PROCESSING
rem  --------------
rem  Incorporate the parameters from Dakota into the template, writing ros.in


python3 %dakota_intall%\bin\dprepro.py %1% ros.template ros.in


rem  --------
rem  ANALYSIS
rem  --------

python3 rosenbrock_bb.py


rem  ---------------
rem  POST-PROCESSING
rem  ---------------

rem  Extract function value and gradient from the simulation output
rem  (in this case Dakota ignores gradient if not needed)
rem  with examples of unix utilities (grep/sed), Perl, and Python

rem  Example with grep/sed installed via MSYS

rem grep 'Function value' ros.out | c:\msys\1.0\bin\sed s/^.................// >results.tmp
rem grep -i "Function g" ros.out | c:\msys\1.0\bin\sed s/^....................//  >> results.tmp

rem perl -n -e "if (/Function value = (.*)/) { print \"$1\n\" }" ros.out > results.tmp
rem perl -n -e "if (/Function gradient = (.*)/) { print $1 }" ros.out >> results.tmp

python3 -c "import sys; r = sys.stdin.readlines(); print(r[14].split('=')[1], end='')" < ros.out > results.tmp
python3 -c "import sys; r = sys.stdin.readlines(); print(r[15].split('=')[1], end='')" < ros.out >> results.tmp

ren results.tmp %2%
