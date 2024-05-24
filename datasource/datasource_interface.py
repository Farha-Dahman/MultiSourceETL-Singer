from abc import ABC, abstractmethod

class DataSourceInterface(ABC):
    @abstractmethod
    def extract_data(self):
        pass
