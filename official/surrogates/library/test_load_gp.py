import numpy as np
import sys
import surrogates
import load_gp
# NOTE: This is a test that should only be run by CTest in the build tree.
# Importing surrogates this way works only in the context of running
# tests in the build tree. In an ordinary dakota install, dakota.surrogates
# should be imported.


morris_gp = surrogates.load("morris.gp.bin", True)
load_gp.print_gp_history(morris_gp)

