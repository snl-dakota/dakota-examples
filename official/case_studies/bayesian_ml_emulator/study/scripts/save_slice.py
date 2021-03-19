#### import the simple module from the paraview
from paraview.simple import *
import sys, getopt, signal

def sig_handler(signum, frame):
  print("Segfault")
  return None 

def extract_and_save_slice(input_pvd_file, output_path, RD=27.0, hub_height=32.1, location_RD=5, RD_factor_y=2, RD_factor_z=1, y_bound=50, z_lower=10, z_upper=70):
  signal.signal(signal.SIGSEGV, sig_handler)
  # full path to input pvd file
  # output folder for results (slice_data.csv)
  # slice x-location given in terms of rotor diameters (RD)
  # multiple parameters to control to size of the slice:
  # RD_factor_y: factor around y=0 to define size of y, usage: slice_ylims = [-RD_factor_y*RD, RD_factor_y*RD]
  # RD_factor_z: factor to define size of z, usage: slice_zlims = [1, RD_factor_z*RD]
  # y_bound: absolute bound to define size of y, usage: slice_ylims = [-y_bound, y_bound]
  # z_lower, z_upper: absolute bounds to define size of z: usage: slice_zlims = [z_lower, z_upper]

  slice_ylims = [-55, 55] #[-y_bound, y_bound] #[-RD_factor_y*RD, RD_factor_y*RD]
  slice_zlims = [0, 100]  #[z_lower, z_upper] #[1, RD_factor_z*RD] #[hub_height - RD_factor_z*RD, hub_height + RD_factor_z*RD]

  # derived quantities
  slice_xloc = 135.0 #location_RD*RD

  # create a new 'PVD Reader'
  velocitypvd = PVDReader(FileName=input_pvd_file)
  velocitypvd.PointArrays = ['velocity']

  # create a new 'Calculator'
  calculator1 = Calculator(Input=velocitypvd)

  # Properties modified on calculator1
  calculator1.ResultArrayName = 'coords'
  calculator1.Function = 'coords'

  # create a new 'Resample To Image'
  resampleToImage1 = ResampleToImage(Input=calculator1)

  # Properties modified on resampleToImage1
  resampleToImage1.UseInputBounds = 0
  resampleToImage1.SamplingDimensions = [1, 177, 161] #[1, 101, 101]
  resampleToImage1.SamplingBounds = [slice_xloc, slice_xloc, slice_ylims[0], \
                                     slice_ylims[1], slice_zlims[0], slice_zlims[1]]

  # save data
  SaveData(output_path + "slice_data.csv", proxy=resampleToImage1, Precision=12,
      UseScientificNotation=1)

########################################################################

def main(argv):

  run_dir = ''
  try:
    opts, args = getopt.getopt(argv,"hi:",["run_folder=", "RD=", "hub_height=", "RD_factor_y=", "RD_factor_z=", "location_RD=", "y_bound=", "z_lower=", "z_upper="])
  except getopt.GetoptError:
    print('save_slice.py -i <run_folder>')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('save_slice.py -i <run_folder> --RD=<rotor diameter> --hub_height=<height of rotor> --RD_factor_y=<y_section: [-RD_factor_y*RD, RD_factor_y*RD]> --RD_factor_z=<z_section: [hub_height-RD_factor_z*RD, hub_height+RD_factor_z*RD]> --location_RD=<x location of slice, i.e. location_RD*RD> --y_bound=<absolue y section: [-y_bound, y_bound], --z_lower/z_upper=<absolute z section: [z_lower, z_upper]')
      sys.exit()
    elif opt in ("-i", "--run_folder"):
      run_dir = arg
    elif opt in ("--RD"):
      RD = float(arg)
    elif opt in ("--hub_height"):
      hub_height = float(arg)
    elif opt in ("--RD_factor_y"):
      RD_factor_y = float(arg)
    elif opt in ("--RD_factor_z"):
      RD_factor_z = float(arg)
    elif opt in ("--location_RD"):
      location_RD = float(arg)
    elif opt in ("--y_bound"):
      y_bound = float(arg)
    elif opt in ("--z_lower"):
      z_lower = float(arg)
    elif opt in ("--z_upper"):
      z_upper = float(arg)

  # edit these variables
  path_prefix = run_dir + '/output/single_turbine'
  input_pvd_file = path_prefix + '/solutions/velocity.pvd'
  output_path = path_prefix + '/slice/'
  #input_pvd_file = "/Users/dtseidl/projects/fy19/wind/single/output_fine/3D_Box/solutions/velocity.pvd"

  #print("Input: ", input_pvd_file)
  #print("Output: ", output_path)
  #try:
  extract_and_save_slice(input_pvd_file, output_path, RD, hub_height, location_RD, RD_factor_y, RD_factor_z, y_bound, z_lower, z_upper)
  #except Exception as inst:
   #print "The exception is " + str(inst)

if __name__ == "__main__":
  main(sys.argv[1:])
