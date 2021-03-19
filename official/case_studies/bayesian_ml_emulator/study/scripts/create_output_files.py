import sys, os, getopt
from shutil import copyfile
import numpy as np
import csv

def main(argv):
    
    models = ['coarse']
    nb_runs = 20
    stochastic_dimension = 6
    nb_lines = 101*101
    coords = np.zeros( (nb_lines, 2) ) #Should be same for coarse, medium, fine

    for model_idx, model in enumerate(models):
        xi_array = np.zeros( (nb_runs, stochastic_dimension) )
        uofxi_array = np.zeros( (nb_lines, nb_runs) )
        if model_idx == 0:
            result_file_name = './MCStudy_' + model + '/run_' + str(1) + '/result_xvelocity.txt'
            with open(result_file_name) as result_file:
                line_ctr = 0
                for line in result_file:
                    elements = line.split()
                    coords[line_ctr, :] = elements[1:3] #x is const, we don't need it
                    line_ctr += 1
                    assert(line_ctr <= nb_lines)

        for cur_run in range(1, nb_runs+1):
            xi_file_name = './MCStudy_' + model + '/run_' + str(cur_run) + '/params.in.' + str(cur_run)
            with open(xi_file_name,'r') as new_file:
                for line in new_file:
                    if 'HH_vel' in line and not 'DVV' in line:
                        elements = line.split()
                        xi_array[cur_run-1, 0] = float(elements[0])
                    elif 'power' in line and not 'DVV' in line:
                        elements = line.split()
                        xi_array[cur_run-1, 1] = float(elements[0])
                    elif 'wind_angle' in line and not 'DVV' in line:
                        elements = line.split()
                        xi_array[cur_run-1, 2] = float(elements[0])
                    elif 'eff_thickness' in line and not 'DVV' in line:
                        elements = line.split()
                        xi_array[cur_run-1, 3] = elements[0]
                    elif 'axial_induction_factor' in line and not 'DVV' in line:
                        elements = line.split()
                        xi_array[cur_run-1, 4] = elements[0]
                    elif 'lmax' in line and not 'DVV' in line:
                        elements = line.split()
                        xi_array[cur_run-1, 5] = elements[0]
                    elif 'model' in line and not 'DVV' in line:
                        elements = line.split()
                        model_from_input = elements[0] 
            new_file.close()

            assert(model_from_input == model)

            result_file_name = './MCStudy_' + model + '/run_' + str(cur_run) + '/result_xvelocity.txt'
            with open(result_file_name) as result_file:
                line_ctr = 0
                for line in result_file:
                    elements = line.split()
                    uofxi_array[line_ctr, cur_run-1] = elements[3] #u velocity
                    line_ctr += 1
                    assert(line_ctr <= nb_lines)
            result_file.close()

        #Do something with slice data and write to ./results_casenb file
        print("Create result files")

        result_coordsUofXis_file_name = 'result_coordsUofXis_' + model + '.txt'
        with open(result_coordsUofXis_file_name, 'w') as result_coordsUofXis:
            result_coordsUofXis.write("#File structure: X_i, Y_i, U(X_i, Y_i, Xi_0), ..., U(X_i, Y_i, Xi_N)\n")
            for coords_idx, coords_line in enumerate(coords):
                result_coordsUofXis.write(" ".join([str(coord) for coord in coords_line]) + " ")
                result_coordsUofXis.write(" ".join([str(uofxi_array[coords_idx, i]) for i in range(nb_runs)]))
                result_coordsUofXis.write("\n")
        result_coordsUofXis.close()

        result_xisUofCoords_file_name = 'result_xisUofCoords_' + model + '.txt'
        with open(result_xisUofCoords_file_name, 'w') as result_xisUofCoords:
            result_xisUofCoords.write("#File structure: Xi_i(1:6), U(X_0, Y_0, Xi_i), ..., U(X_101x101, Y_101x101, Xi_i)\n")
            for xi_idx, xi_line in enumerate(xi_array):
                result_xisUofCoords.write(" ".join([str(xi) for xi in xi_line]) + " ")
                result_xisUofCoords.write(" ".join([str(uofxi) for uofxi in uofxi_array[:, xi_idx]]) + " " )
                result_xisUofCoords.write("\n")
        result_xisUofCoords.close()
        print("Done")


if __name__ == "__main__":
   main(sys.argv[1:])
