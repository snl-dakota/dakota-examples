
import unittest
import numpy as np
import matplotlib.pyplot as plt

import PIC # Our evolving ES PIC library we want to test

class TestPICPieces(unittest.TestCase):

    def test_V_Bandedsolve(self):

        dx = 0.01
        N = int(1/dx)
        x = np.linspace(0.0, 1.0, N+1)
        rho = x*0.0 + 1.0

        # Call the numerical solver
        max_iters = 1000
        V = PIC.solveBanded(dx, rho, eps0=1.0)
        #print(V)

        # Compare to the known exact solution
        exact = lambda x : 0.5*x*(1-x)
        phi_e = exact(x)
        error_norm = np.linalg.norm((V-phi_e))
        #print("Error norm: "+str(error_norm))

        # Plot the two solutions ... or don't based on hard-coded boolean
        if False:
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


    def test_read_parameters(self):

        params = PIC.read_parameters("test_params.json")

        # Test the presence of some expected (required?) parameters
        dt = params['simulation']['dt']
        self.assertEqual(0.01, dt)
        xmin = params['simulation']['xmin']
        self.assertEqual(-1.0, xmin)
        xmax = params['simulation']['xmax']
        self.assertEqual(1.0, xmax)
        N = params['simulation']['num_elems']
        self.assertEqual(100, N)


    def test_parse_particle_types(self):

        params = PIC.read_parameters("test_params.json")

        # Parse some particle types
        particles = PIC.parse_particle_types(params)

        # This is a pythonic way of getting the particle objects out of the array of
        # ... particles by name without concern for their order in the array
        fake_e          = [_ for _ in particles if _.type == "fake_e-"][0]
        super_heavy_ion = [_ for _ in particles if _.type == "super_heavy_ion"][0]

        # Test some expected atributes from the particle objects
        self.assertEqual(fake_e.mass, 1.0)
        self.assertEqual(fake_e.charge, -1.0)
        self.assertEqual(super_heavy_ion.mass, 1.0e20)
        self.assertEqual(super_heavy_ion.charge, 1.0)


    def test_load_particles(self):

        # Create a particle instance
        test_particle = PIC.Particle("e-", { 'charge': -1.0, 'mass': 9.109548628456E-31 })
        test_particle.weight = 1.e10 # assign a representative computational particle weight

        PIC.particle_loader(-0.1, 0.1, 1.e18, test_particle, Temp=800.0, K_B = 1.380649e-23)

        if False:
            # Do some pplots to see how the pos and vel distributions look
            n, bins, patches = plt.hist(test_particle.pos, 50, density=True) #, facecolor='g', alpha=0.75)
            plt.xlabel('pos')
            plt.ylabel('Probability')
            plt.title('Histogram')
            plt.show()

            n, bins, patches = plt.hist(test_particle.vel, 50, density=True) #, facecolor='g', alpha=0.75)
            plt.xlabel('vel')
            plt.ylabel('Probability')
            plt.title('Histogram')
            plt.show()

            print(test_particle.pos.shape)
            print(np.mean(test_particle.pos))
            print(np.mean(test_particle.vel))
            print((np.dot(test_particle.vel, test_particle.vel)*test_particle.mass*test_particle.weight/(1.380649e-23*1.e18)))



if __name__=='__main__':
    unittest.main()
