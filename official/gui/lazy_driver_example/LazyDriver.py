import os.path
import psutil
import shutil
import subprocess
import sys
import dakota.interfacing as di

###########################

# Arguments and constants

parameters_file = sys.argv[1]
results_file = sys.argv[2]
collecting_results_file = "." + results_file

pid_file_name = ".pid"
ignore_file = ".ignore"
invalid_pid = -1

###########################

# Run-time specified fields

this_driver_filename = "LazyDriver.py"
driver_cmd = ["python" , "-m" , "DakotaDriver" ]
expected_params = ["w", "t", "L", "p", "E", "X", "Y"]
expected_results = ["mass" , "stress" , "displacement" ]
fail_value = "NaN"
expected_evals = []

###########################

# Functions

def annotate_working_dir():
    dakrunfile_path = "../.dakrun" 
    if not os.path.exists(dakrunfile_path):
        dakrunfile = open(dakrunfile_path, "w")
        dakrunfile.write("fail="+fail_value+"\n")
        dakrunfile.write("parameters_file="+parameters_file+"\n")
        dakrunfile.write("results_file="+results_file+"\n")
        dakrunfile.write("analysis_driver="+this_driver_filename)
        dakrunfile.close()

def delete_results_file(results_file):
    if os.path.exists(results_file): 
        os.remove(results_file)
        
def file_contains_results(results_file):
    with open(results_file) as results:
        for line in results:
            if fail_value in line:
                return False
    return True        

def write_fail_results(results_file, results):
    delete_results_file(results_file)
    resultsfile = open(results_file, "w")
    for r in results:
        resultsfile.write(fail_value + " " + r + "\n")
    resultsfile.close()
    
def validate_parameters(expected_params, actual_params_obj):
    for d, v in actual_params_obj.items():
        if d not in expected_params and len(expected_params) > 0:
            raise RuntimeError("Parameter label " + d + " was not expected")
            
def validate_and_extract_result_labels(expected_results, actual_results_obj):
    actual_results = []
    for d, v in actual_results_obj.items():
        if d not in expected_results and len(expected_results) > 0:
            raise RuntimeError("Result label " + d + " was not expected")
        else:
            actual_results.append(d)
    return actual_results

###########################

# Main

annotate_working_dir()

actual_params_obj, actual_results_obj = di.read_parameters_file()
actual_eval_num = actual_params_obj.eval_num

validate_parameters(expected_params, actual_params_obj)
actual_results = validate_and_extract_result_labels(expected_results, actual_results_obj)

driver_cmd.append(parameters_file)
driver_cmd.append(collecting_results_file)

if not os.path.exists(ignore_file):    
    if len(expected_evals) == 0 or actual_eval_num in expected_evals:
        if not os.path.exists(pid_file_name):    
            write_fail_results(results_file, actual_results)
            
            proc = subprocess.Popen(driver_cmd, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
            pid_ = proc.pid 
            
            pidfile = open(".pid", "w")
            pidfile.write(str(pid_))
            pidfile.close()
    
        else:
            pid_ = invalid_pid
            with open(pid_file_name,"r") as pidfile:
                pid_ = int(pidfile.read())
    
            if os.path.exists(collecting_results_file) and file_contains_results(collecting_results_file):
                # Process finished and results can be collected
                delete_results_file(results_file)
                shutil.copy(collecting_results_file, results_file)
            elif pid_ != invalid_pid and psutil.pid_exists(pid_):
                # Process is still running
                write_fail_results(results_file, actual_results)
    
    elif not os.path.exists(results_file):
        write_fail_results(results_file, actual_results)
        
elif not os.path.exists(results_file):
    write_fail_results(results_file, actual_results)
