from pybamm_diffsol import PybammDiffsol, Pybamm2Diffsl
import pybamm
import numpy as np


def test_solve():
    model = PybammDiffsol(
        """
        in = [r, k]
        r { 1 } k { 1 }
        u_i { y = 0.1 }
        F_i { (r * y) * (1 - (y / k)) }
    """
    )
    t_eval = np.array([0.0, 1.0])
    t_interp = np.linspace(0.0, 1.0, 100)
    k = 1.0
    r = 1.0
    y0 = 0.1
    y = model.solve(np.array([r, k]), t_interp, t_eval)
    soln = k / (1.0 + (k - y0) * np.exp(-r * t_interp) / y0)
    np.testing.assert_allclose(y[0], soln, rtol=1e-5)


def test_spm_solve():
    outputs = ["Voltage [V]"]
    inputs = ["Current function [A]"]
    model_str = Pybamm2Diffsl(pybamm.lithium_ion.SPM()).to_str(inputs, outputs)
    model = PybammDiffsol(model_str)
    t_eval = np.array([0.0, 3600.0])
    t_interp = np.linspace(0.0, 3600.0, 100)
    params = np.array([1.0])
    y = model.solve(params, t_interp, t_eval)

    spm = pybamm.lithium_ion.SPM()
    params = spm.default_parameter_values
    params["Current function [A]"] = "[input]"
    geometry = spm.default_geometry
    params.process_model(spm)
    params.process_geometry(geometry)
    mesh = pybamm.Mesh(geometry, spm.default_submesh_types, spm.default_var_pts)
    disc = pybamm.Discretisation(mesh, spm.default_spatial_methods)
    disc.process_model(spm)
    solver = pybamm.IDAKLUSolver()
    sol = solver.solve(
        spm, t_eval=t_eval, t_interp=t_interp, inputs={"Current function [A]": 1.0}
    )

    np.testing.assert_allclose(y[0], sol[outputs[0]].data[:-1], rtol=1e-5)
