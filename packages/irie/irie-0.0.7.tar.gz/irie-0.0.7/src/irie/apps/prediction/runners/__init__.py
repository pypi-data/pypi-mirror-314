from pathlib import Path
from typing import NewType
from abc import abstractmethod
RunID = NewType("RunID", int)

MetricType = NewType("MetricType", str)

class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class Runner:
    def __init__(self, conf: dict):

        if isinstance(conf, dict):
            # Create from dict when posted from API; this
            # is used to create a new PredictorModel
            self.name: str   = conf["name"]
            self.description = conf.get("description", "")
            self.conf        = conf["config"]
            self.metrics     = conf["metrics"]
            self.entry_point = conf["entry_point"]
            self.active = conf.get("active", True)
        else:
            # Create from PredictorModel when loaded from database.
            # This is done when running analysis
            self.name: str = conf.name
            self.description = "" # conf.description
            self.conf = conf.config
            self.entry_point = conf.entry_point
            self.metrics = conf.metrics
            self.active = conf.active
            try:
                self.model_file = Path(conf.config_file.path).resolve()
            except ValueError as e:
                print(e)

            self.out_dir = Path(__file__).parents[0]/"Predictions"
            self.runs = {}

    @abstractmethod
    def newPrediction(self, event)->RunID: ...

    @abstractmethod
    def runPrediction(self, run_id)->bool: ...

    def getMetricList(self)->list:
        return self.metrics

    def activateMetric(self, type, rid=None)->bool:
        return False

    @abstractmethod
    def getMetricData(self, run: RunID, metric: MetricType)->dict: ...
