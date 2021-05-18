
import unittest
import numpy as np
import matplotlib.pyplot as plt

import PIC # Our evolving ES PIC library we want to test

class TestSolver(unittest.TestCase):

    def test1(self):

        dx = 0.01
        N = int(1/dx)
        x = np.linspace(0.0, 1.0, N+1)
        rho = x*0.0 + 1.0

        # Call the numerical solver
        max_iters = 1000
        phi = PIC.solvePotentialGS(dx, rho, max_iters)

        # Compare to the known exact solution
        exact = lambda x : 0.5*x*(1-x)
        phi_e = exact(x)
        e_norm = np.linalg.norm((phi-phi_e))
        print("Error norm: "+str(e_norm))

        # Plot the two solutions
        fig, ax = plt.subplots()
        ax.plot(x, phi, marker='x', label='FD')
        ax.plot(x, phi_e, label='exact')
        ax.legend()

        ax.set(xlabel='Pos (x)', ylabel='voltage (V)', title='convergence')
        #ax.grid()

        fig.savefig("test.png")
        plt.show()

        # Test that the solver produced a solution that agrees with the
        # exact solution to within (default) tolerance

        self.assertTrue(np.allclose(phi, phi_e))


if __name__=='__main__':
    unittest.main()
