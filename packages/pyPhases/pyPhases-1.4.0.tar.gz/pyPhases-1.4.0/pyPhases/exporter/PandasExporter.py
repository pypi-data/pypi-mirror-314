from math import exp
import pandas as pd
from pyPhases.exporter.PickleExporter import PickleExporter
from pyPhases.exporter.DataExporter import DataExporter
from pyPhases.Data import DataNotFound


class PandasExporter(DataExporter):
    
    def __init__(self, options=None):
        super().__init__(options)
        self.df = None
        self.dataHandler = True
    
    def checkType(self, type):
        return type in [pd.DataFrame]
    
    def getDataHandler(self, data):
        self.df = data
        return self

    def read(self, dataId, options={}, **kwargs):
        try:
            self.df = pd.read_pickle(self.getPath(dataId))
        except FileNotFoundError:
            raise DataNotFound(f"Data with id {dataId} not found")

        return self
    
    def write(self, dataId, object: pd.DataFrame, options={}, **kwargs):
        object.to_pickle(self.getPath(dataId))


    def get(self, **kwargs):
        """
        Retrieves a single row (as dict) from the DataFrame based on the provided keyword arguments.
        If no keyword arguments are provided, returns the entire DataFrame.
        """
                
        if self.df is None:
            raise DataNotFound("Data was never read")
        
        if kwargs:
            try:
                row = self.df.loc[(self.df[list(kwargs)] == pd.Series(kwargs)).all(axis=1)]
                if row.empty:
                    raise DataNotFound(f"Data with {kwargs} not found")
                return row
            except IndexError:
                raise DataNotFound(f"Data with {kwargs} not found")
            except KeyError:
                raise DataNotFound(f"Data with {kwargs} not found")
        return self.df