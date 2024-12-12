import os

import numpy as np
import pytest

from lnl_computer.cosmic_integration.mcz_grid import McZGrid
from lnl_computer.mock_data import MockData
from lnl_computer.observation import Observation
from lnl_computer.observation.mock_observation import MockObservation

PLOT = False


def test_mcz_grid_gen_n_save(mock_data: MockData, tmp_path):
    # GENERATE AND SAVE GRID
    grd = McZGrid.from_compas_output(
        mock_data.compas_filename,
        cosmological_parameters=dict(aSF=0.01, dSF=4.70, mu_z=-0.23),
        n_bootstrapped_matrices=2,
        chirp_mass_bins=np.linspace(3, 40, 50),
        redshift_bins=np.linspace(0, 0.6, 100),
    )
    tmp_fn = os.path.join(tmp_path, "mcz_grid.h5")
    grd.save(fname=tmp_fn)


def test_mcz_grid_generation_skip(mock_data: MockData, caplog, tmp_path):
    # TRY TO RE-GENERATE (but will be skipped)
    McZGrid.generate_n_save(
        mock_data.compas_filename,
        dict(aSF=0.01, dSF=4.70, mu_z=-0.23, sigma_0=0.0),
        n_bootstraps=2,
        outdir=tmp_path,
        fname=mock_data.mcz_grid_filename,
    )
    assert f"Skipping {mock_data.mcz_grid_filename} generation" in caplog.text


def test_load_mcz_grid_n_plot(mock_data: MockData, tmp_path):
    new_uni = McZGrid.from_h5(mock_data.mcz_grid_filename)
    new_uni.plot().savefig(os.path.join(tmp_path, "mcz_grid.png"))


def test_obs_gen_n_save(mock_data: MockData, tmp_path):
    obs = MockObservation.from_mcz_grid(mock_data.mcz_grid, duration=1)
    obs.save(os.path.join(tmp_path, "mock_obs.npz"))
    obs = Observation.load(os.path.join(tmp_path, "mock_obs.npz"))
    obs.plot(fname=os.path.join(tmp_path, "mock_obs.png"))
