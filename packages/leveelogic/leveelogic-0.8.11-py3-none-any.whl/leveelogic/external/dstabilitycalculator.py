from typing import List, Union, Dict, Tuple
from pydantic import BaseModel
from enum import IntEnum
import threading
import subprocess
from dotenv import load_dotenv
import os
from pathlib import Path
from uuid import uuid1
import logging

from ..objects.levee import Levee
from .dgeolib import DStabilityModel
from geolib.models.dstability.internal import (
    BishopBruteForceResult,
    SpencerGeneticAlgorithmResult,
    UpliftVanParticleSwarmResult,
)


class CalculationResult(BaseModel):
    error: str = ""


class DStabilityCalculationResult(CalculationResult):
    safety_factor: float = 0.0
    slipplane: List[Tuple[float, float]] = []


class CalculationModel(BaseModel):
    levee: Levee
    name: str
    filename: str = ""
    result: DStabilityCalculationResult = None


def calculate(exe: str, model: CalculationModel):
    # model.levee.to_stix(model.filename)
    try:
        subprocess.call([exe, model.filename])
    except Exception as e:
        model.result.error = f"Got a calculation error; '{e}'"
        return

    try:
        ds = DStabilityModel.from_stix(model.filename)
        slipplane = []
        if type(ds.output[0]) in [
            BishopBruteForceResult,
            SpencerGeneticAlgorithmResult,
            UpliftVanParticleSwarmResult,
        ]:
            slipplane = [(p.X, p.Z) for p in ds.output[0].Points]
        model.result = DStabilityCalculationResult(
            safety_factor=ds.output[0].FactorOfSafety, slipplane=slipplane
        )

        return
    except Exception as e:
        model.result = DStabilityCalculationResult(
            error=f"Got calculation result error '{e}'"
        )


class DStabilityCalculator(BaseModel):
    calculation_models: List[CalculationModel] = []
    logfile: Union[Path, str] = None
    remove_files_afterwards: bool = True

    def export_files(self, output_path: Union[Path, str]):
        for cm in self.calculation_models:
            cm.model.serialize(Path(output_path) / f"{cm.name}.stix")

    def clear(self, unset_logfile=False):
        self.calculation_models = []
        if unset_logfile:
            self.logfile = None

    def get_model_by_name(self, model_name: str):
        for cm in self.calculation_models:
            if cm.name == model_name:
                return cm
        raise ValueError(f"No model with name '{model_name}'")

    def get_model_result_dict(self):
        return {
            cm.name: cm.result.safety_factor
            for cm in self.calculation_models
            if cm.result.safety_factor is not None
        }

    def add_models(self, models: List[Levee], names: List[str]):
        if len(models) != len(names):
            raise ValueError(
                f"Got {len(models)} model(s) and {len(names)} name(s), this should be the same amount"
            )
        for i in range(len(models)):
            self.add_model(models[i], names[i])

    def add_model(self, levee: Levee, name: str):
        # adding the first model (the model type is NONE) which also defines which type of calculator this will be
        self.calculation_models.append(CalculationModel(levee=levee, name=name))

    def remove_files(self):
        for cm in self.calculation_models:
            os.remove(cm.filename)

    def calculate(self):
        if self.logfile is not None:
            logging.basicConfig(
                filename=str(self.logfile),
                filemode="w",
                format="%(asctime)s %(levelname)s %(message)s",
                datefmt="%H:%M:%S",
                level=logging.INFO,
            )

        try:
            load_dotenv("leveelogic.env")

            DSTABILITY_CONSOLE_EXE = os.getenv("DSTABILITY_CONSOLE_EXE")
            CALCULATIONS_FOLDER = os.getenv("CALCULATIONS_FOLDER")

            assert Path(DSTABILITY_CONSOLE_EXE).exists()
            assert Path(CALCULATIONS_FOLDER).exists()
        except Exception as e:
            if self.remove_files_afterwards:
                self.remove_files()
            raise ValueError(f"Error setting up calculation environment, '{e}'")

        threads = []
        for calculation_model in self.calculation_models:
            calculation_model.filename = str(
                Path(CALCULATIONS_FOLDER) / f"{str(uuid1())}.stix"
            )
            calculation_model.levee.to_stix(calculation_model.filename)

            threads.append(
                threading.Thread(
                    target=calculate,
                    args=[DSTABILITY_CONSOLE_EXE, calculation_model],
                )
            )

            if self.logfile is not None:
                logging.debug(
                    f"Added model '{calculation_model.name}' to the calculations as file '{calculation_model.filename}'"
                )

        logging.debug(f"Starting {len(threads)} calculation(s)")
        for t in threads:
            t.start()

        for t in threads:
            t.join()
        logging.debug(f"Finished {len(threads)} calculation(s)")
        if self.remove_files_afterwards:
            self.remove_files()
