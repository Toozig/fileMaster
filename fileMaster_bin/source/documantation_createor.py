
# # todo - for fixing columns - print table + enumarte of cols name

# from .file_class import  Source
# from .table_class import TableFile, open_file_by_extension, get_file_extension, COLUMN_DESCRIPTION_TEMPLATE, READ_FUNCTION
# import art
# from .PBM_class import PBMFile, DEFAULT_COLUMNS as PBM_DEFAULT_COLUMNS
# import json
# import os
# from .bed_class import BedFile, DEFAULT_COLUMNS as BED_DEFAULT_COLUMNS
# from .organism_data import get_organism_data
# from time import sleep
# SOURCE = 'source'
# PATH = 'path'
# NAME = 'name'

# DEBUG = True

# MISSING_COLUMN_MSG = "Oh honey, it seems we have a data-fashion mismatch! 💃💔\n\
# This is a default column and it must be in the file.\
#  Please fix your file to ensure the descriptions match the fabulous data inside. \n"

# GET_SOURCE_NAME = "Enter the source name ( leave empty to use file name): "
# GET_SOURCE_PATH = "Enter the source path (link to paper / path to source json): "
# GET_SOURCE_TYPE = "Enter the source type (script/ paper): "




# def write_ascii(string, font='tarty1'):
#     art.tprint(string, font=font)
#     sleep(0.2)


# ### Source file functions ####
# def __create_source(path, type,  name):
#     source = {PATH: path, NAME: name, 'file_type': type}
#     return source


# def __create_file_data(path: str,file_type, sources , description):
#     """
#     Creates a file documentation file.
#     Args: path (str): The path of the file documentation file.
#     """

#     file_data = {'path': path, 
#                  'file_type': file_type, 
#                  'description': description,
#                   'sources': sources}
#     return file_data

        

# def create_source_documantation( path: str, to_save: bool=False, description = None, sources = []):
#     """
#     Creates a file documentation file.
#     Args: path (str): The path of the file documentation file.
#     """

    
#     file_data = __create_file_data(path, SOURCE, sources, description)
#     source = Source(**file_data)
#     if to_save:
#         json_name = path.split('.')[0] + '.json'
#         with open(json_name, 'w') as file:
#             json.dump(source.get_data(), file)
#         print(f'File documentation saved to {json_name}')
#     return source

# ### end of source file functions ####
# # considering using the col for later use


# ### Bed file functions ####


# def create_bed_data(path: str, genome, file_type: str = "bed", to_save: bool = False, **kwargs):
#     organims_data = get_organism_data(genome)
#     bed_data = create_table_data(path, file_type, to_save, 
#                                             default_columns = BED_DEFAULT_COLUMNS, **kwargs)
#     bed_data.update({'organism': organims_data})
#     return bed_data


# def create_bed_documantation(path: str, file_type: str = "bed", to_save: bool = False):
#     """
#     Creates a documentation for the BED file.
#     Args:
#         path (str): The path of the documentation file.
#         file_type (str, optional): The type of the file. Defaults to "bed".
#         to_save (bool, optional): Whether to save the documentation to a file. Defaults to True.
#     """

#     bed_data = create_bed_data(path, file_type, to_save)
#     print('bed data before object')
#     print(bed_data)
#     return BedFile(**bed_data) 

# #### end of bed file functions ####
# ### PBM file functions ####


# def __get_sequence_length(table_data):
#     table = TableFile(**table_data)
#     df = table.open_file()
#     seq_len = len(df['pbm_sequence'].iloc[0])
#     return seq_len


# def create_pbm_data(path: str,  array_design, pbm_source, file_type: str = "pbm", to_save: bool = False):
#     description = f"PMB expirment.\nsource: {pbm_source[NAME]}"
#     table_data = create_table_data(path, file_type, to_save, 
#                                             default_columns = PBM_DEFAULT_COLUMNS,
#                                             sources=[pbm_source],
#                                             description=description)
#     seq_len = __get_sequence_length(table_data)
#     table_data.update({'seq_len': seq_len, 'ArrayDesign': array_design})
#     return table_data


# def create_pbm_documantation(path: str, file_type: str = "pbm", to_save: bool = False):
#     """
#     Creates a documentation for the BED file.
#     Args:
#         path (str): The path of the documentation file.
#         file_type (str, optional): The type of the file. Defaults to "bed".
#         to_save (bool, optional): Whether to save the documentation to a file. Defaults to True.
#     """

#     pbm_data = create_pbm_data(path, file_type, to_save)
#     if DEBUG:
#         print('pbm data before object')
#     print(pbm_data)
#     return PBMFile(**pbm_data) 

# #### end of PBM file functions ####


# ##### Table file  functions#####

# def create_table_documantation(path: str,
#                                 file_type: str = "table",
#                                 have_header: bool = None,
#                                 index_col: bool = None,
#                                 comment: str = None,
#                                 default_columns = [],
#                                 ):
#     table_data = create_table_data(path, file_type, have_header, index_col, comment, default_columns)
#     return TableFile(**table_data)
        


# def get_file_key_no_input(path):
#     """
#     In case coudlnt understand the file extension and way to open it
#     """
#     try:
#         file_key = get_file_extension(path)
#     except ValueError:
#         print("\n===============\nCould not detrmine the file type\n")
#         for i, key in enumerate(READ_FUNCTION.keys()):
#             print(f"{i}. {key}")
#         ext_list = list(READ_FUNCTION.keys())
#         for i, ext in enumerate(ext_list):
#                 print(f"{i}. {ext}")
#         print(f"\nChange the extension to one of the  following types ^ ")
#         exit(1)
#     return file_key 


# def __create_table_data(path,header, index_col, comment, columns_description):
#     table_key = get_file_key_no_input(path)
#     table_data = {'table_key': table_key, 
#                   'header': header, 
#                   'index_col': index_col,
#                    'comment': comment,
#                     'columns_description': columns_description}
#     return table_data

# def create_table_data(path: str,
#                     header,
#                     index_col,
#                     comment,
#                     columns_description,
#                     file_type: str = "table",
#                     sources = [],
#                     description = '',
#                     default_columns = []):
#         """
#         create json file for a given table file
#         """
#         file_data = __create_file_data(path=path, 
#                                         file_type = file_type, 
#                                         sources = sources,
#                                         description = description)
        
#         columns_description = columns_description + default_columns
#         table_data = __create_table_data(path, header, index_col, comment, columns_description)
#         table_data.update(file_data)
#         return table_data



# ### end of table file functions ###
# ### source file functions ####
        

# def create_documantation(path: str, to_save: bool = True):
#     print(f"Creating documentation for {path.split('/')[-1]}")
#     keys_list = list(CREATE_TYPE_DICT.keys())
#     for i, key in enumerate(keys_list):
#          print(f'{i} - {key}')
#     file_idx = int('write the index of the file type')
#     return CREATE_TYPE_DICT[keys_list[file_idx]](path=path, to_save=to_save)



# CREATE_TYPE_DICT = {
#      'source' : create_source_documantation,
#      'table' : create_table_documantation,
#      'bed' : create_bed_documantation,
#      'pbm' : create_pbm_documantation
# }



# def main():
#     path = '/home/dsi/toozig/lab_folder/deepBind_training/downloaded_data/DMRT1/GSM1292960_pTH9197_HK_8mer_6759.raw.txt.gz'
#     create_table_documantation(path)

# if __name__ == '__main__':

#     main()