import os
import shutil
from typing import Dict, Tuple, Union

import numpy as np
import pandas as pd
from compas_python_utils.cosmic_integration.binned_cosmic_integrator.detection_matrix import (
    DetectionMatrix,
)

from ..likelihood import ln_likelihood
from ..logger import logger
from ..observation import Observation, load_observation
from .star_formation_paramters import DEFAULT_SF_PARAMETERS


class McZGrid(DetectionMatrix):
    """
    Represents a detection matrix in (m_c, z) space.

    This class is a wrapper around the DetectionMatrix class, with some extra functionality.

    :param compas_path: The path to the COMPAS hdf5 file
    :param cosmological_parameters: The cosmological parameters to use (dict)
    :param rate_matrix: The detection rate matrix
    :param chirp_mass_bins: The chirp mass bins
    :param redshift_bins: The redshift bins
    :param n_systems: The number of systems in the COMPAS file
    :param n_bbh: The number of BBH systems in the COMPAS file
    :param outdir: The output directory to save the detection matrix to
    :param bootstrapped_rate_matrices: The bootstrapped rate matrices


    Important methods:
    - sample_observations
    - prob_of_mcz

    """

    @classmethod
    def from_dict(cls, data: Dict) -> "McZGrid":
        """Create a mcz_grid object from a dictionary"""
        obj_types = [
            "compas_path",
            "cosmological_parameters",
            "n_systems",
            "n_bbh",
        ]
        for key in data:
            if key in obj_types:
                data[key] = data[key].item()
        det_matrix = cls(
            compas_path=data["compas_path"],
            cosmological_parameters=data["cosmological_parameters"],
            rate_matrix=data["rate_matrix"],
            chirp_mass_bins=data["chirp_mass_bins"],
            redshift_bins=data["redshift_bins"],
            n_systems=data["n_systems"],
            n_bbh=data["n_bbh"],
            outdir=data.get("outdir", "."),
            bootstrapped_rate_matrices=data.get(
                "bootstrapped_rate_matrices", None
            ),
        )
        logger.debug(f"Loaded cached det_matrix with: {det_matrix.param_str}")
        return det_matrix

    def save(self, fname="") -> None:
        """Save the mcz_grid object to a npz file, return the filename"""
        super().save()
        if fname != "":
            shutil.move(self.default_fname, fname)

    def get_matrix_bin_idx(self, mc: float, z: float) -> Tuple[int, int]:
        mc_bin = np.argmin(np.abs(self.chirp_mass_bins - mc))
        z_bin = np.argmin(np.abs(self.redshift_bins - z))
        return mc_bin, z_bin

    def prob_of_mcz(self, mc: float, z: float, duration: float = 1.0) -> float:
        mc_bin, z_bin = self.get_matrix_bin_idx(mc, z)
        if self.n_detections(duration) == 0:
            return 0
        return self.rate_matrix[mc_bin, z_bin] / self.n_detections(duration)

    def get_prob_grid(self, duration: float = 1.0) -> np.ndarray:
        if self.n_detections(duration) == 0:
            return np.zeros_like(self.rate_matrix)
        return self.rate_matrix / self.n_detections(duration)

    def get_bootstrapped_grid(self, i: int) -> "McZGrid":
        """Creates a new Uni using the ith bootstrapped rate matrix"""
        assert (
            i < self.n_bootstraps
        ), f"i={i} is larger than the number of bootstraps {self.n_bootstraps}"
        return McZGrid(
            compas_path=self.compas_path,
            cosmological_parameters=self.cosmological_parameters,
            rate_matrix=self.bootstrapped_rate_matrices[i],
            chirp_mass_bins=self.chirp_mass_bins,
            redshift_bins=self.redshift_bins,
            n_systems=self.n_systems,
            n_bbh=self.n_bbh,
            outdir=self.outdir,
        )

    def n_detections(self, duration: float = 1.0) -> float:
        """Calculate the number of detections in a given duration (in years)"""
        return np.nansum(self.rate_matrix) * duration

    def get_lnl(
        self,
        mcz_obs: Observation,
    ) -> Tuple[float, float]:
        """Get Lnl+/-unc from the mcz_obs"""
        lnl = ln_likelihood(
            obs=mcz_obs,
            model=self,
        )
        bootstrapped_lnls = []
        for i in range(self.n_bootstraps):
            bootstrap_mcz_grid = self.get_bootstrapped_grid(i)
            bootstrapped_lnls.append(
                ln_likelihood(
                    obs=mcz_obs,
                    model=bootstrap_mcz_grid,
                )
            )
        return lnl, np.std(np.array(bootstrapped_lnls))

    def __dict__(self) -> Dict:
        return self.to_dict()

    def __repr__(self) -> str:
        return f"<mcz_grid: [{self.n_systems} systems], {self.param_str}, [{self.compas_path}]>"

    @property
    def param_str(self):
        return "_".join(
            [f"{k}_{v:.10f}" for k, v in self.cosmological_parameters.items()]
        )

    @property
    def label(self) -> str:
        return McZGrid.get_label(
            self.compas_path, self.cosmological_parameters
        )

    @property
    def default_fname(self) -> str:
        return McZGrid.get_default_fname(
            self.outdir, self.compas_path, self.cosmological_parameters
        )

    @staticmethod
    def get_label(
        compas_path: str, cosmological_parameters: Dict[str, float]
    ) -> str:
        compas_fname = os.path.basename(compas_path).split(".")[0]
        p_str = McZGrid.param_dict_to_str(cosmological_parameters)
        return f"mczgrid_{compas_fname}_{p_str}"

    @staticmethod
    def get_default_fname(
        outdir: str,
        compas_path: str,
        cosmological_parameters: Dict[str, float],
    ):
        l = McZGrid.get_label(compas_path, cosmological_parameters)
        return f"{outdir}/{l}.h5"

    @staticmethod
    def param_dict_to_str(param_dict: Dict[str, float]) -> str:
        return "_".join([f"{k}_{v:.4f}" for k, v in param_dict.items()])

    @property
    def n_bootstraps(self) -> int:
        if self.bootstrapped_rate_matrices is None:
            return 0
        return len(self.bootstrapped_rate_matrices)

    @classmethod
    def generate_n_save(
        cls,
        compas_h5_path: str,
        sf_sample: Dict = None,
        save_plots: bool = False,
        outdir=None,
        fname="",
        n_bootstraps=0,
        clean=False,
        **kwargs,
    ) -> "McZGrid":
        """Generate a detection matrix for a given set of star formation parameters
        :param compas_h5_path:
        :param sf_sample: Dict of star formation parameters
        :param save_plots: Bool to save plots
        :param outdir: outdir for plots + mcz_grid
        :param fname: mcgrid-fname (if empty, will not save)
        :param n_bootstraps: N
        :return:
        """

        if sf_sample is None:
            sf_sample = DEFAULT_SF_PARAMETERS
            logger.warning(
                f"sf_sample not provided, using default: {sf_sample}"
            )

        if not clean:
            fnames = [
                fname,
                cls.get_default_fname(outdir, compas_h5_path, sf_sample),
            ]
            for f in fnames:
                if os.path.isfile(f):
                    logger.warning(
                        f"Skipping {f} generation as it already exists"
                    )
                    return cls.from_h5(f)
        if fname != "" and not fname.endswith(".h5"):
            logger.error(f"fname must end with .h5, got {fname}")

        if sf_sample is None:
            sf_sample = DEFAULT_SF_PARAMETERS

        params = dict(
            aSF=sf_sample.get("aSF", DEFAULT_SF_PARAMETERS["aSF"]),
            dSF=sf_sample.get("dSF", DEFAULT_SF_PARAMETERS["dSF"]),
            mu_z=sf_sample.get("mu_z", DEFAULT_SF_PARAMETERS["mu_z"]),
            sigma_0=sf_sample.get("sigma_0", DEFAULT_SF_PARAMETERS["sigma_0"]),
        )
        logger.info(f"Generating McZ grid: {params}")

        mcz_grid = cls.from_compas_output(
            compas_path=compas_h5_path,
            cosmological_parameters=params,
            max_detectable_redshift=0.6,
            redshift_bins=np.linspace(0, 0.6, 100),
            chirp_mass_bins=np.linspace(3, 40, 50),
            outdir=outdir,
            save_plots=save_plots,
            n_bootstrapped_matrices=n_bootstraps,
        )
        if isinstance(fname, str):
            mcz_grid.save(fname=fname)
        return mcz_grid

    @classmethod
    def lnl(
        cls,
        sf_sample: Dict,
        mcz_obs: Union[Observation, str, Dict],
        compas_h5_path: str,
        **kwargs,
    ) -> Tuple[float, float]:
        """Return the LnL(sf_sample|mcz_obs)+/-unc

        Also saves the Lnl+/-unc and params to a csv file

        :param mcz_obs: The observed mcz values
        :param args: Arguments to pass to generate_n_save
        :return: The LnL value
        """
        if "outdir" in kwargs:
            os.makedirs(kwargs["outdir"], exist_ok=True)

        if isinstance(mcz_obs, str):
            mcz_obs = load_observation(mcz_obs)
        elif isinstance(mcz_obs, dict):
            mcz_obs = Observation.from_dict(mcz_obs)

        model = cls.generate_n_save(
            compas_h5_path=compas_h5_path,
            sf_sample=sf_sample,
            **kwargs,
        )

        lnl, unc = model.get_lnl(mcz_obs=mcz_obs)
        _save_lnl_dict_to_csv(
            lnl,
            unc,
            model=model,
            fname=kwargs.get("fname", ""),
        )
        return lnl, unc

    @property
    def n_mc_bins(self) -> int:
        return len(self.chirp_mass_bins)

    @property
    def n_z_bins(self) -> int:
        return len(self.redshift_bins)


def _save_lnl_dict_to_csv(lnl, unc, model: McZGrid, fname: str) -> None:
    """Save the lnl and unc to a csv file"""
    data = dict(
        lnl=lnl,
        unc=unc,
        **model.cosmological_parameters,
    )
    # save lnl data to csv
    lnl_fname = f"{model.outdir}/{model.label}_lnl.csv"
    if fname != "":
        lnl_fname = fname.replace(".h5", "_lnl.csv")

    df = pd.DataFrame(data, index=[0])
    df.to_csv(lnl_fname, index=False)
