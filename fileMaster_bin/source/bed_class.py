import pandas as pd
from typing import List, Dict
from pydantic import ValidationError, BaseModel
from .table_class import TableFile
from .organism_data import ORGANISM_DICT, Organism
BED_SEP = '\t'
BED_COMMENT = '#'

BED_DETAILS = { 'table_key' : 'bed',
                'sep' : BED_SEP,
                'header' : False,
                'index_col' : None,
                'comment': BED_COMMENT,
}
DEFAULT_COLUMNS = [
    {
        "name": "Chrom",
        "index": 0,
        "dtype": "str",
        "description": "The chromosome of a segment.",
    },
    {
        "name": "Start",
        "index": 1,
        "dtype": "int",
        "description": "The start position of a segment.",
        "check_type": True
    },
    {
        "name": "End",
        "index": 2,
        "dtype": "int",
        "description": "The end position of a segment.",
        "check_type": True
    }
]


def init_column_description(all_parms, extra_columns_description):
    col_description = extra_columns_description
    if 'table_data' in all_parms:
        exist = all_parms['table_data'].pop('columns_description')
        print(exist)
        col_description += exist
    if 'columns_description' in all_parms:
        col_description += all_parms.pop('columns_description')
    return col_description


class BedFile(TableFile):
    def __init__(self,
                    organism: Dict[str, str]=None,
                    extra_columns_description: List[Dict[str,str]] = [],
                    **kwargs):
            """
            Initializes a BEDFile instance.

            Args:
                organism (List[Dict[str, str]]): Organism information for the BED file.
                extra_columns (List[Dict[str,str]], optional): Additional columns for the BED file.
                Defaults to None. (no need for chrom,start,end)
            """
            # avoid duplicated values
            columns_description = kwargs.pop('columns_description', [])
            columns = TableFile.remove_duplicated_columns(columns_description,extra_columns_description,DEFAULT_COLUMNS)
            # default_columns = [col for col in DEFAULT_COLUMNS if col['name'] not in [c['name'] for c in extra_columns_description]]
            # columns = default_columns + extra_columns_description + columns_description
            print(columns)
            bed_details = {k: v for k, v in BED_DETAILS.items() if k not in kwargs}
            super().__init__(
                columns_description=columns,
                shape=None,
                **bed_details,
                **kwargs
            )
            bed_data = kwargs['bed_data'] if 'bed_data' in kwargs else {'organism': organism}
            self.bed_data = self.BedFileData(**bed_data)
            # print("created bed successfully")




    def open_file(self)-> pd.DataFrame:
        """
        Opens the BED file and returns the data.

        Returns:
            Any: The data contained in the BED file.
        """
        bed_df = pd.read_csv(self.file_data.path, 
                             **self.table_data.read_args.model_dump()) # todo: in table class - function that get open args
        return bed_df
    



    @classmethod
    def __get_columns_description(cls,path, sep=BED_SEP):
        columns_description = []
        print("Enter the details of non 'chrom', 'start' 'end':")
        with open(path, 'r') as file:
            header = file.readline().strip().split(sep)[3:]
        for i, col in enumerate(header):
            columns_description.append(super().__get_columns_helper(i, col))
        return columns_description
    

    @classmethod
    def create_documantation(cls, path: str, file_type: str = "bed", to_save: bool = True):
        """
        Creates a documentation for the BED file.

        Args:
            path (str): The path of the documentation file.
            file_type (str, optional): The type of the file. Defaults to "bed".
            to_save (bool, optional): Whether to save the documentation to a file. Defaults to True.
        """
        table = super().create_documantation(path, file_type=file_type, to_save=False)
        organism = input(f"Enter the organism of the BED file: ({','.join(ORGANISM_DICT.keys())})")
        if organism not in ORGANISM_DICT:
            raise ValueError(f"Organism '{organism}' is not in the list of organisms.")
        organism = ORGANISM_DICT[organism]
        bed_file = cls(**table.file_data.dict(), **table.table_data.dict(), organism=organism)


    
    class BedFileData(BaseModel):
        """
        Attributes:
            organism (List[Dict[str, str]]): Organism information for the BED file.
        """
        organism: Organism
        # is_sorted: bool





def main():
    description = "Test"
    source = {
        "sourceType" : "haah",
        "sourcePath" : "haah",
        "sourceName" : "haah",
        "sourceDescription" : "haah"
    }
    extra_columns = [{"name":"id", "index": 3, "dtype": str, "description": "id of the segment"}]
    df = BedFile(path = "/home/dsi/toozig/lab_folder/file_class/tests/seq1.bed",
            description= description,
              organism=HG38_ORGANISM, sources_list=[source], 
                extra_columns_description = extra_columns,
                ).open_file()
    print(df.head())
    

    

if __name__ == "__main__":
    main()