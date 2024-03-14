from typing import List, Tuple, Optional
from pydantic import ValidationError, BaseModel, field_validator
from .file_class import File
import pandas as pd



COLUMN_DESCRIPTION_TEMPLATE = {
    "name": "Column Name",
    "index": 0,
    "dtype": 'str', # optional
    "description": "Description of the column.",
    "check_type": False # optional if false
}

READ_FUNCTION = {
    'csv': lambda path, header, index_col, comment: pd.read_csv(path, header=header, index_col=index_col, comment=comment),
    'tsv': lambda path, header, index_col, comment: pd.read_csv(path, header=header, sep='\t', index_col=index_col, comment=comment),
    'txt': lambda path, header, index_col, comment: pd.read_csv(path, header=header, sep='\t', index_col=index_col, comment=comment),
    'xls': lambda path, header, index_col, comment: pd.read_excel(path, header=header, index_col=index_col, comment=comment),
    'xlsx': lambda path, header, index_col, comment: pd.read_excel(path, header=header, index_col=index_col, comment=comment),
    'json': lambda path, header, index_col, comment: pd.read_json(path, index_col=index_col, comment=comment),
    'parquet': lambda path, header, index_col, comment: pd.read_parquet(path, index_col=index_col, comment=comment),
    'feather': lambda path, header, index_col, comment: pd.read_feather(path, index_col=index_col, comment=comment),
    'h5': lambda path, header, index_col, comment: pd.read_hdf(path, index_col=index_col, comment=comment),
    'hdf5': lambda path, header, index_col, comment: pd.read_hdf(path, index_col=index_col, comment=comment),
    'bed': lambda path, header, index_col, comment: pd.read_csv(path, header=header, sep='\t', index_col=None, comment="#"),
}




def get_file_extension(file_path: str) -> str:
    function_keys = [i for i in READ_FUNCTION.keys() if i in file_path.split('/')[-1]]
    if len(function_keys) == 0:
        raise ValueError(f"Unsupported file extension: {file_path.split('/')[-1]}")
    return function_keys[0]


def open_file_by_extension(file_path, header, index_col, comment,table_key = None) -> pd.DataFrame:
    table_key = table_key if table_key is not None else get_file_extension(file_path)
    return READ_FUNCTION[table_key](path=file_path,header=header,index_col=index_col, comment=comment)
	


class ColumnsDescriptionItem(BaseModel):
    name: str
    index: int
    description: str


class TableReadArgs(BaseModel):
    table_key: str 
    header: Optional[int] = None
    index_col: Optional[int] = None
    comment: Optional[str] = None

    @field_validator('header')
    @classmethod
    def set_default_header(cls, value):
        """
        Validator to set the default header value if not provided.

        Args:
            value (str): The header value provided.

        Returns:
            str: The header value or 'infer' if not provided.
        """
        return value if value is not None else 'infer'

class TableFileData(BaseModel):
    """
    Represents a generic table file with common functionalities.

    Attributes:
        header (str): Header of the table file.
        index_col (str): Name of the column to be used as an index.
        sep (str): Separator used in the table file.
        columns_description (List[dict[str,str]]): List of dictionaries specifying column details.
        comment (str): Character indicating comments in the table file.
        shape (Tuple[int, int]): Tuple representing the shape (number of rows and columns_description) of the table.
        dtypes (list): List of data types for columns_description in the table.
    """
    read_args: TableReadArgs
    columns_description: List[ColumnsDescriptionItem]
    shape: Optional[List[int]] = None

class TableFile(File):
    _class_data_key = 'table_data'
    table_data: TableFileData


    def __init__(self, columns_description: List[dict[str, str]] =None, table_key: str = None,
                 header=None, index_col=None, comment: str = None, shape: List[int] = None, read_args= {},
                  **kwargs):
            """
            Initializes a TableFile instance.

            Args:
                path (str): The file path of the table file.
                description (str): Description of the table file.
                source (dict): Source information for the table file.
                sep (str): Separator used in the table file. Used to open the file
                columns_description (List[dict[str,str]]): List of dictionaries specifying column details.
                date (str, optional): The date and time when the table file log was created. Defaults to None.
                header (optional): Pandas read_csv header parameter. Defaults to 'infer'.
                index_col  (optional): Pandas read_csv index_col parameter. Defaults to None.
                comment  (str, optional): Pandas read_csv comment parameter. Defaults to None.
                shape (Tuple[int, int], optional): Tuple representing the shape (number of rows and columns_description) of the table. Defaults to None.
            
            """
            # print("=======Table======")
            # for k,v in kwargs.items():
            #     print(k,':',v)
            # print("=============")
            super().__init__(**kwargs)
            if 'table_data' in kwargs:
                table_data = kwargs['table_data']
                # columns_description = table_data.pop('columns_description')
            else:
                if len(read_args) : 
                    open_args = TableReadArgs(**read_args)
                else:
                    open_args = TableReadArgs(header = header,
                                        index_col = index_col,
                                        table_key = table_key,
                                        comment = comment)
                table_data = {'columns_description': columns_description, 'shape': shape, 'read_args' : open_args}
            # print("---TableData---")
            # for k,v in table_data.items():
            #     print(k,v)  
            # print("doing table data")
            self.table_data = TableFileData(**table_data)
            # print("created table successfully")


    def open_file(self) -> pd.DataFrame:
        """
        Opens the table file and returns a pandas DataFrame with specified parameters.

        Returns:
            pd.DataFrame: The DataFrame representing the table.
        """
        df = open_file_by_extension(file_path=self.get_path() ,**self.table_data.read_args.dict())
        return df

    @classmethod
    def __remove_duplicates_dicts(cls,lst):
        result = []
        seen = set()
        for d in lst:
            # Convert each dictionary to a frozenset to make it hashable
            frozen_dict = frozenset(d.items())
            if frozen_dict in seen:
                continue
            seen.add(frozen_dict)
            result.append(d)
        return result
    

    @classmethod
    def remove_duplicated_columns(cls,columns_description =[],
                                default_columns=[],
                                 
                                file_exta_cols=[]):

        if len(file_exta_cols):
            def_cols1 = [col for col in default_columns if col['name'] not in [c['name'] for c in file_exta_cols]]
            columns_description_f = [col for col in columns_description if col['name'] not in [c['name'] for c in file_exta_cols]]
        else:
            def_cols1 = default_columns
            columns_description_f = columns_description
        if len(columns_description):
            def_cols1 = [col for col in def_cols1 if col['name'] not in [c['name'] for c in columns_description]]

        columns = file_exta_cols + def_cols1 + columns_description_f
        return cls.__remove_duplicates_dicts(columns)

    # def __getattr__(self, attr): 
    #         if attr in self.__dict__:
    #             return self.__dict__[attr]
    #         # Delegate attribute access to the underlying DataFrame
    #         try:
    #             print('tryin to get', attr)
    #             return getattr(self.open_file(), attr)
    #         except AttributeError:
    #             raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")





