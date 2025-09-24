
import unittest
import numpy as np
import matplotlib.pyplot as plt

import PIC # Our evolving ES PIC library we want to test

class TestPICPieces(unittest.TestCase):

    def test_V_Bandedsolve(self):

        dx = 0.01
        N = int(1/dx)
        x = np.linspace(0.0, 1.0, N+1)
        rho = np.ones_like(x)

        # Call the numerical solver
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


    def test_V_Bandedsolve_Dirichlet(self):

        dx = 0.01
        N = int(1/dx)
        x = np.linspace(0.0, 1.0, N+1)
        rho = 10.0*np.ones_like(x)

        # Call the numerical solver
        V = PIC.solveBanded(dx, rho, bc="dirichlet", left_side=1.0, right_side=5.0, eps0=1.0)

        # Compare to the known exact solution
        exact = lambda x : -5.0*x*x+9.0*x+1.0
        phi_e = exact(x)
        error_norm = np.linalg.norm((V-phi_e))
        #print("Error norm: "+str(error_norm))

        # Test that the solver produced a solution that agrees with the
        # exact solution to within (default) tolerance

        self.assertTrue(np.allclose(V, phi_e))


    def test_V_Bandedsolve_Periodic(self):

        dx = 0.01
        N = int(1/dx)
        x = np.linspace(0.0, 1.0, N+1)
        exact = lambda x : np.sin(2.0*np.pi*x)
        mms_rhs = lambda x : -4.0*np.pi*np.pi*np.sin(2.0*np.pi*x)
        # Need to negate per ES formulation
        rho = -mms_rhs(x)

        # Call the numerical solver
        V = PIC.solveBanded(dx, rho, bc="dirichlet", left_side=1.0, right_side=1.0, eps0=1.0)
        #print("V:",V)

        # Compare to the known exact solution - includes shift repated to BCs
        phi_e = 1.0+exact(x)
        #print("Exact:",phi_e)
        error_norm = np.linalg.norm((V-phi_e))
        #print("Error norm: "+str(error_norm))

        # Test that the solver produced a solution that agrees with the
        # exact solution to within (default) tolerance

        self.assertTrue(np.allclose(V, phi_e, atol=0.001))


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
        self.assertTrue(np.array_equal(PIC.get_elem_id(x, pos_vec), np.array(elem_arr)))


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

        # Test some expected attributes from the particle objects
        self.assertEqual(fake_e.mass, 1.0)
        self.assertEqual(fake_e.charge, -1.0)
        self.assertEqual(super_heavy_ion.mass, 1.0e20)
        self.assertEqual(super_heavy_ion.charge, 1.0)


    def test_load_particles(self):

        # Create a particle instance
        test_particle = PIC.Particle("e-", { 'charge': -1.0, 'mass': 9.109548628456E-31, 'weight': 1.e6 })
        test_particle.weight = 1.e10 # assign a representative computational particle weight

        T_spec = 800.0

        # This produces a lot of computational particles, eg ~20 million and so is an indicator of performance
        PIC.particle_loader(-0.1, 0.1, 1.e18, test_particle, Temp=T_spec, K_B = 1.380649e-23)

        # Compute the temperature and compare to what we wanted
        avg_velx = np.mean(test_particle.velx)
        avg_vely = np.mean(test_particle.vely)
        avg_velz = np.mean(test_particle.velz)
        avg_T = test_particle.mass*(  np.dot((avg_velx-test_particle.velx), (avg_velx-test_particle.velx))
                                    + np.dot((avg_vely-test_particle.vely), (avg_vely-test_particle.vely))
                                    + np.dot((avg_velz-test_particle.velz), (avg_velz-test_particle.velz)) )
        avg_T = avg_T/(3.0*1.380649e-23*test_particle.pos.shape[0])
        #print("avg_T: "+str(avg_T))
        self.assertTrue(np.isclose(avg_T, T_spec, rtol=1.0e-3))


        # Optionally plot the distributions
        if False:
            n, bins, patches = plt.hist(test_particle.pos, 50, density=True) #, facecolor='g', alpha=0.75)
            plt.xlabel('pos')
            plt.ylabel('Probability')
            plt.title('Histogram')
            plt.show()

            n, bins, patches = plt.hist(test_particle.velx, 50, density=True) #, facecolor='g', alpha=0.75)
            plt.xlabel('vel')
            plt.ylabel('Probability')
            plt.title('Histogram')
            plt.show()

            print("computational particles: ",test_particle.pos.shape)
            print("Pos  (min, mean, max): ",np.min(test_particle.pos), np.mean(test_particle.pos), np.max(test_particle.pos))
            print("Velx (min, mean, max): ",np.min(test_particle.velx), np.mean(test_particle.velx), np.max(test_particle.velx))
            print("Vely (min, mean, max): ",np.min(test_particle.vely), np.mean(test_particle.vely), np.max(test_particle.vely))
            print("Velz (min, mean, max): ",np.min(test_particle.velz), np.mean(test_particle.velz), np.max(test_particle.velz))


    def test_particle_outflux(self):

        test_particles = PIC.Particle("fake", { 'charge': 1.0, 'mass': 1.0, 'weight': 1.0 })

        test_particles.pos   = np.linspace(-10.0, 10.0, 21)
        test_particles.velx  = 2.0*test_particles.pos
        test_particles.vely  = 3.0*test_particles.pos
        test_particles.velz  = 4.0*test_particles.pos
        test_particles.field = 5.0*test_particles.pos

        new_particles = PIC.apply_outflux_bc(test_particles, -4.5, 4.5)

        # Test expected behavior after removing out-of-bounds particles
        baseline = np.linspace(-4.0, 4.0, 9)
        self.assertEqual(new_particles.pos.shape[0], 9)
        self.assertTrue(np.allclose(    baseline, new_particles.pos  ), 'Filtered particle pos values are not correct.')
        self.assertTrue(np.allclose(2.0*baseline, new_particles.velx ), 'Filtered particle velx values are not correct.')
        self.assertTrue(np.allclose(3.0*baseline, new_particles.vely ), 'Filtered particle vely values are not correct.')
        self.assertTrue(np.allclose(4.0*baseline, new_particles.velz ), 'Filtered particle velz values are not correct.')
        self.assertTrue(np.allclose(5.0*baseline, new_particles.field), 'Filtered particle field values are not correct.')


    def test_particle_periodic(self):

        test_particles = PIC.Particle("fake", { 'charge': 1.0, 'mass': 1.0, 'weight': 1.0 })

        x_left  = -0.5
        x_right =  1.0
        test_particles.pos   = np.array([x_left+2.234*(x_right-x_left), x_right-5.15*(x_right-x_left)])
        test_particles.velx  = 2.0*test_particles.pos
        test_particles.vely  = 3.0*test_particles.pos
        test_particles.velz  = 4.0*test_particles.pos
        test_particles.field = 5.0*test_particles.pos

        new_particles = PIC.apply_periodic_bc(test_particles, x_left, x_right)

        # Test expected behavior after removing out-of-bounds particles
        baseline = np.array([x_left+0.234*(x_right-x_left), x_right-0.15*(x_right-x_left)])
        self.assertTrue(np.allclose(baseline, new_particles.pos), 'Filtered particle pos values are not correct.')
        self.assertTrue(np.allclose(test_particles.velx , new_particles.velx ), 'Filtered particle velx values are not correct.')
        self.assertTrue(np.allclose(test_particles.vely , new_particles.vely ), 'Filtered particle vely values are not correct.')
        self.assertTrue(np.allclose(test_particles.velz , new_particles.velz ), 'Filtered particle velz values are not correct.')
        self.assertTrue(np.allclose(test_particles.field, new_particles.field), 'Filtered particle field values are not correct.')




if __name__=='__main__':
    unittest.main()
