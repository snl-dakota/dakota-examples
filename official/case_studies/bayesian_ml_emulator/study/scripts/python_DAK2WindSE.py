import sys, os, getopt
from shutil import copyfile
import numpy as np
import csv

#This is the main run script which sets up the case folder, runs windse in the folder
#postprocesses the output to a slice, reads the slice and create a result file
#--paramfile: the current parameterfile params.in.i
#--resultfile: the current resultfile results.out.i
def main(argv):
    
    try:
        opts, args = getopt.getopt(argv,"hi:p:r:",["ipath=", "paramfile=", "resultfile="])
    except getopt.GetoptError:
        print("parse_input.py -p <paramfile>")
        sys.exit(2)
    for opt, arg in opts:
        #print "loop", opt, arg
        if opt == '-h':
            print("parse_input.py -p <paramfile>")
            sys.exit()
        elif opt in ("-p", "--paramfile"):
            #print "param:", arg
            paramfile = arg
        elif opt in ("-r", "--resultfile"):
            #print "param:", arg
            resultfile = arg

    param_split = paramfile.split('.')
    case_nb = int(param_split[-1])

    print('====== START', case_nb, '======')
    lmax = -1
    y_bound = -1
    z_lower = -1
    z_upper = -1
    #Get parameters from params.in.<case_nb>
    with open(paramfile,'r') as new_file:
        for line in new_file:
            if 'HH_vel' in line and not 'DVV' in line:
                elements = line.split()
                HH_vel = float(elements[0])
            elif 'power' in line and not 'DVV' in line:
                elements = line.split()
                power = float(elements[0])
            elif 'wind_angle' in line and not 'DVV' in line:
                elements = line.split()
                wind_angle = float(elements[0])
            elif 'eff_thickness' in line and not 'DVV' in line:
                elements = line.split()
                eff_thickness = elements[0]
            elif 'axial_induction_factor' in line and not 'DVV' in line:
                elements = line.split()
                axial_induction_factor = elements[0]
            elif 'lmax' in line and not 'DVV' in line:
                elements = line.split()
                lmax = elements[0]
            elif 'model' in line and not 'DVV' in line:
                elements = line.split()
                model = elements[0]
            elif 'y_bound' in line and not 'DVV' in line:
                elements = line.split()
                y_bound  = int(elements[0])
            elif 'z_lower' in line and not 'DVV' in line:
                elements = line.split()
                z_lower = int(elements[0])
            elif 'z_upper' in line and not 'DVV' in line:
                elements = line.split()
                z_upper = int(elements[0])
            elif 'grid_x' in line and not 'DVV' in line:
                elements = line.split()
                grid_x = int(elements[0])
            elif 'grid_y' in line and not 'DVV' in line:
                elements = line.split()
                grid_y = int(elements[0])
            elif 'grid_z' in line and not 'DVV' in line:
                elements = line.split()
                grid_z = int(elements[0])
            elif 'grid_refine' in line and not 'DVV' in line:
                elements = line.split()
                grid_refine = int(elements[0])

    assert(grid_x > 0 and grid_y > 0 and grid_z > 0)
    assert(y_bound > 0 and y_bound <= 135)
    assert(z_lower >= 0 and z_lower < z_upper and z_upper <= 120)
    assert(grid_refine >= 0 and grid_refine <= 4)

    print("#Model: ", model)
    print("#Uncertain parameters: HH_vel, power, wind_angle, eff_thickness, axial_induction_factor, lmax")
    print(HH_vel, power, wind_angle, eff_thickness, axial_induction_factor, lmax)
    print('======')

    #Hub parameters, could also add that to input file
    RD = 27.0 #Given
    hub_height = 32.1 #Given
    location_RD = 5 #x location of slice
    RD_factor_y = 2 #NOT USED: Slice dimension in y: Multiple of RD around y of hub, i.e. y = [-RD_factor_y*RD, RD_factor_y*RD]
    RD_factor_z = 3 #NOT USED: Slice dimension in z: Multiple of RD around z of hub, i.e. z = [hub_height - RD_factor_z*RD, hub_height + RD_factor_z*RD]

    #Create run directory
    print('Initialize run directory')
    run_dir = './run_' + str(case_nb)
    try:
        os.mkdir(run_dir)
    except OSError:
        print ("Creation of the run directory %s failed" % run_dir)
    try:
        os.mkdir(run_dir + '/turbine_data')
    except OSError:
        print ("Creation of the ./run_i/turbine_data directory %s failed" % run_dir + '/turbine_data')
    
    copyfile("./" + paramfile, run_dir + "/" + paramfile)

    #Do something based on model, not used right now
    #if model == 'fine':
    #elif model == 'medium':
    #elif model == 'coarse':
    #else:
    #   raise NotImplementedError

    #Create turbine_data file
    turbine_data_file_name = run_dir + '/turbine_data/wind_farm.txt'
    turbine_data_file = open(turbine_data_file_name, 'w')
    turbine_data_file.write('#\tx\ty\tHH\tYaw\tDiameter\tThickness\tAxial_Induction\n')
    turbine_data_file.write('0\t0\t32.1\t0.0\t27.0\t' + str(eff_thickness) + '\t' + str(axial_induction_factor) + '\n')
    turbine_data_file.close()

    #Create specific input file single_turbine.yaml via sed
    copyfile('./single_turbine.yaml', run_dir + '/single_turbine.yaml')
    os.system('./sed_input_file.sh ' + str(case_nb) + " "+ str(HH_vel) + " " + str(power) + " " + str(wind_angle) + " " + str(lmax) + " " + str(grid_refine) \
                                     + " " + str(grid_x) + " " + str(grid_y) + " " + str(grid_z))
    print('Done')

    #Run WindSE
    print('Run WindSE')
    os.system('./exe_windse.sh ' + str(case_nb))
    #Cleanup unnecessary WindSE
    os.system('./remove_unnecessary_folders.sh ' + str(case_nb))
    print('Done')

    print('Create Slice')
    try:
        #Create slice folder
        os.mkdir(run_dir + '/output/single_turbine/slice')
    except OSError:
        print ("Creation of the run directory %s failed" % run_dir)

    #Create slice
    #TODO: here you might have to change the pvpython call
    os.system('/projects/viz/paraview/bin/pvpython save_slice.py -i' + run_dir \
              + ' --RD=' + str(RD) + ' --hub_height=' + str(hub_height) + ' --RD_factor_y=' + str(RD_factor_y) \
              + ' --RD_factor_z=' + str(RD_factor_z) + ' --location_RD=' + str(location_RD) + ' --y_bound=' + str(y_bound) + ' --z_lower=' + str(z_lower) + ' --z_upper=' + str(z_upper))
    print('Done')

    #Read slice data into an array
    print("Read slice...")
    slice_file_name = run_dir + '/output/single_turbine/slice/slice_data.csv'
    nb_lines = 161*177 #101*101
    slice_coords = np.zeros( (nb_lines, 3) )
    slice_velocity = np.zeros( (nb_lines , 3) )
    with open(slice_file_name, newline='') as slice_csv:
        file_reader = csv.reader(slice_csv, delimiter=',')
        file_reader.__next__()
        for row_idx, row in enumerate(file_reader):
            slice_coords[row_idx, :] = row[0:3]
            slice_velocity[row_idx, :] = row[3:6]
    print("Done")

    #NOT USED: Write results data for all velocities to text file
    #print("Create result files")
    #result_xvelocity_file_name = run_dir + '/result_xvelocity.txt'
    #with open(result_xvelocity_file_name, 'w') as result_xvelocity:
    #    for coord_idx, coords in enumerate(slice_coords):
    #        if(coords[1] >= -y_bound and coords[1] <= y_bound and coords[2] >= z_lower and coords[2] <= z_upper):
    #            result_xvelocity.write(" ".join([str(coord) for coord in coords]) + " ")
    #            result_xvelocity.write(" ".join([str(slice_velocity[coord_idx, i]) for i in range(3)]))
    #            result_xvelocity.write("\n")
    #result_xvelocity.close()
    #print("Done")

    print("Create result dakota file")
    result_file_name = "./" + resultfile
    with open(result_file_name, 'w') as result_file:
        for line_velocity_idx, line_velocity in enumerate(slice_velocity):
            if(slice_coords[line_velocity_idx, 1] >= -y_bound and slice_coords[line_velocity_idx, 1] <= y_bound \
               and slice_coords[line_velocity_idx, 2] >= 29.5 and slice_coords[line_velocity_idx, 2] <= z_upper):
                result_file.write(str(line_velocity[0]))
                result_file.write("\n")
        for line_velocity_idx, line_velocity in enumerate(slice_velocity):
            if(slice_coords[line_velocity_idx, 1] >= -y_bound and slice_coords[line_velocity_idx, 1] <= y_bound \
               and slice_coords[line_velocity_idx, 2] >= 29.5 and slice_coords[line_velocity_idx, 2] <= z_upper):
                result_file.write(str(line_velocity[1]))
                result_file.write("\n")
        for line_velocity_idx, line_velocity in enumerate(slice_velocity):
            if(slice_coords[line_velocity_idx, 1] >= -y_bound and slice_coords[line_velocity_idx, 1] <= y_bound \
               and slice_coords[line_velocity_idx, 2] >= 29.5 and slice_coords[line_velocity_idx, 2] <= z_upper):
                result_file.write(str(line_velocity[2]))
                result_file.write("\n")
    result_file.close()
    print("Done")
    print('====== END', case_nb, '======')


if __name__ == "__main__":
   main(sys.argv[1:])
