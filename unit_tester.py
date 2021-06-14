
import unittest
import numpy as np
import matplotlib.pyplot as plt

import PIC # Our evolving ES PIC library we want to test

class TestSolver(unittest.TestCase):

    def _test_V_solve(self):

        dx = 0.01
        N = int(1/dx)
        x = np.linspace(0.0, 1.0, N+1)
        rho = x*0.0 + 1.0

        # Call the numerical solver
        max_iters = 1000
        V = PIC.solvePotentialGS(dx, rho, max_iters)

        # Compare to the known exact solution
        exact = lambda x : 0.5*x*(1-x)
        phi_e = exact(x)
        #error_norm = np.linalg.norm((V-phi_e))
        #print("Error norm: "+str(error_norm))

        # Plot the two solutions
        fig, ax = plt.subplots()
        ax.plot(x, V, marker='x', label='FD')
        ax.plot(x, phi_e, label='exact')
        ax.legend()

        ax.set(xlabel='Pos (x)', ylabel='voltage (V)', title='convergence')
        #ax.grid()

        fig.savefig("test.png")
        #plt.show()

        # Test that the solver produced a solution that agrees with the
        # exact solution to within (default) tolerance

        self.assertTrue(np.allclose(V, phi_e))


    def test_dVdx(self):

        dx = 0.01
        N = int(1/dx)
        x = np.linspace(0.0, 1.0, N+1)

        # Create an exact V field (polynomial) that we will numerically differentiate
        exactV = lambda x : 0.5*x*(1-x)
        V = exactV(x)

        # And create the field of exact gradient values
        exactG = lambda x : 0.5 - x
        exactGrad = exactG(x)

        # Call the numerical gradient using first-order approximation for domain boundaries
        use_second_order = False
        gradV = PIC.computeGrad(dx, V, second_order=False)

        # Compute the error and check that it is within tolerance but also outside a tighter tolerance
        error_norm = np.linalg.norm((gradV-exactGrad))
        #print("Error norm: "+str(error_norm))
        self.assertTrue(error_norm < 1.e-2)
        self.assertFalse(error_norm < 1.e-3)


        # Now call the numerical gradient using second-order approximation for domain boundaries
        use_second_order = True
        gradV = PIC.computeGrad(dx, V, second_order=True)

        # Compute the error and check that it is very close to machine precision
        error_norm = np.linalg.norm((gradV-exactGrad))
        #print("Error norm: "+str(error_norm))
        self.assertTrue(error_norm < 1.e-14)


    def test_elem_id(self):

        dx = 0.01
        N = int(1/dx)

        # Introduce a shift in order to test meshes that don't have 0.0 as the left end-point
        shift = 0.15

        x = np.linspace(0.0, 1.0, N+1) - shift

        # Test left end-point
        self.assertEqual(PIC.get_elem_id(x, -shift), 0)
        # Test right location of first element
        self.assertEqual(PIC.get_elem_id(x, -shift+dx), 1)

        # Test left location of last element
        self.assertEqual(PIC.get_elem_id(x, x[-1]-dx), N-2)
        # Test right end-point
        self.assertEqual(PIC.get_elem_id(x, x[-1]), N-1)

        # Test an interior point
        pos = 42*dx +0.5*dx - shift
        self.assertEqual(PIC.get_elem_id(x, pos), 42)

        # Test a collection of interior points
        elem_arr = [31, 87, 42]
        pos_vec = np.array(elem_arr)*dx + 0.5*dx - shift
        self.assertEqual(PIC.get_elem_id(x, pos_vec).tolist(), elem_arr)


    def test_charge_scatter(self):

        dx = 0.01
        N = int(1/dx)
        mesh = np.linspace(0.0, 1.0, N+1)

        # Fake particle charge and macroparticle weight for testing purposes
        charge = np.array([1.5])
        particle_wt = 2.0

        # Place a charge at a certain location
        pos = np.array( [ 0.4125 ] )

        # We should get an array of charge on the left and right nodes of the element
        #    ... that this point lies within.  So calculate what the result should be:
        elem_id = PIC.get_elem_id(mesh, pos[0])
        left_x = mesh[elem_id]
        right_x = mesh[elem_id+1]
        weight_right = (pos[0]-left_x)/(right_x-left_x)
        weight_left = 1.0 - weight_right

        # The function we want to test
        scat_chg = PIC.charge_scatter(mesh, pos, particle_wt, charge)

        # Correctness checks for the two nodes
        self.assertEqual(scat_chg[elem_id]  , weight_left *charge[0]*particle_wt)
        self.assertEqual(scat_chg[elem_id+1], weight_right*charge[0]*particle_wt)


    def test_field_gather(self):

        dx = 0.01
        N = int(1/dx)
        mesh = np.linspace(0.0, 1.0, N+1)

        # Place a charge at a certain location
        pos = np.array( [ 0.4125 ] )

        # Linear field should give us an exact gather value (because we interpolate linearly)
        mock_field = lambda x : -2.0 + 4.0*x
        E_field = mock_field(mesh)

        # The function we want to test
        gathered_field = PIC.field_gather(mesh, pos, E_field)

        # Correctness check
        self.assertEqual(gathered_field[0], mock_field(pos[0]))


if __name__=='__main__':
    unittest.main()
