from abc import ABC, abstractmethod
from pydantic import BaseModel

class DeepBindData(BaseModel):
    protein_name: str
    source_organism: str
    cite_source: str	

class DeepbindInterface():
    @abstractmethod
    def get_db_data(self) -> DeepBindData:
        """
        get the cite source of the file
        """
        pass

    def get_protein(self) -> str:
        """
        get the protein name
        """
        data = self.get_db_data()
        return data.protein_name

    def get_organism(self) -> str:
        """
        get the organism name
        """
        data = self.get_db_data()
        return data.source_organism	

    def get_cite_source(self) -> str:
        """
        get the cite source of the file
        """
        data = self.get_db_data()
        return data.cite_source

    @abstractmethod
    def get_experiment_details(self) -> dict:
        """
        get the experiment details
        """
        pass