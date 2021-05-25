
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


if __name__=='__main__':
    unittest.main()
