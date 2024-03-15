
# todo - for fixing columns - print table + enumarte of cols name

from .file_class import  Source
from .table_class import TableFile, open_file_by_extension, get_file_extension, COLUMN_DESCRIPTION_TEMPLATE, READ_FUNCTION
import art
from .PBM_class import PBMFile, DEFAULT_COLUMNS as PBM_DEFAULT_COLUMNS
import json
import os
from .bed_class import BedFile, DEFAULT_COLUMNS as BED_DEFAULT_COLUMNS
from .organism_data import ORGANISM_DICT
from time import sleep
SOURCE = 'source'
PATH = 'path'
NAME = 'name'

DEBUG = True

MISSING_COLUMN_MSG = "Oh honey, it seems we have a data-fashion mismatch! 💃💔\n\
This is a default column and it must be in the file.\
 Please fix your file to ensure the descriptions match the fabulous data inside. \n"

GET_SOURCE_NAME = "Enter the source name ( leave empty to use file name): "
GET_SOURCE_PATH = "Enter the source path (link to paper / path to source json): "
GET_SOURCE_TYPE = "Enter the source type (script/ paper): "

def write_ascii(string, font='tarty1'):
    art.tprint(string, font=font)
    sleep(0.2)



def __create_source(path=None, type=None,  name=None):
    source = {}
    
    print("Enter the details of the file source (script/ paper etc) source:")
    source[PATH] = input(GET_SOURCE_PATH) if path is None else path
    if os.path.exists(source[PATH]):
            Source.from_json(source[PATH])
            return Source
    source[NAME] = input(GET_SOURCE_NAME) if name is None else name
    # source[NAME]  = source[NAME] if source[NAME] else source[PATH].split('/')[-1].split('.')[0]
    source['file_type'] = input(GET_SOURCE_TYPE) if type is None else type
    # source['description'] = input("Enter the source description: ")
    # todo: add dfescription from json
    print(f"source: {source}")
    return source

def __create_file_data(path: str,file_type, sources = [], description = None):
    """
    Creates a file documentation file.
    Args: path (str): The path of the file documentation file.
    """
    file_description = input("Enter description of the file: ") if description is None else description

    print("\n===============\n\n")
    write_ascii(SOURCE)
    more_source =  len(sources) == 0
    if not more_source:
        print(sources)
        more_source = input("Do you want to add a source? (y/n): ").lower() == 'y'
    while more_source:
        sources.append(__create_source())
        more_source = input("Do you want to add another source? (y/n): ").lower() == 'y'
    file_data = {'path': path, 'file_type': file_type, 'description': file_description, 'sources': sources}
    return file_data

        

def create_source_documantation( path: str, to_save: bool=True):
    """
    Creates a file documentation file.
    Args: path (str): The path of the file documentation file.
    """
    file_data = __create_file_data(path, SOURCE)
    source = Source(**file_data)
    if to_save:
        json_name = path.split('.')[0] + '.json'
        with open(json_name, 'w') as file:
            json.dump(source.get_data(), file)
        print(f'File documentation saved to {json_name}')
    return source



# considering using the col for later use

def __get_organism_data():
    print("\n===============\nDarling, let's figure out the fabulous origin of your file!")

    print("Available organisms:")
    for i, key in enumerate(ORGANISM_DICT.keys()):
        print(f"{i}. {key} {__get_organism_emoji(key)}")
    print(f"{len(ORGANISM_DICT)}. Other")

    while True:
        try:
            selected_index = int(input("\nEnter the number corresponding to your chosen organism: "))
            if 0 <= selected_index < len(ORGANISM_DICT):
                selected_key = list(ORGANISM_DICT.keys())[selected_index]

                print(f"\nFile origin identified as")
                write_ascii(selected_key)
                print("You're making data glamorous, darling!")
                return ORGANISM_DICT[selected_key]
            elif selected_index == len(ORGANISM_DICT):
                # Handle the "Other" option here
                organism = input("Enter the organism (e.g., mouse, human): ")
                genome_version = input("Enter the genome version (e.g., hg38, mm10): ")
                custom_origin = {"organism": organism, "genome_version": genome_version}
                print(f"\nCustom file origin identified: {custom_origin}")
                return custom_origin
            else:
                print("Oh honey, that's not on the list. Choose a valid number from the fabulous options.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def __get_organism_emoji(organism_key):
    emoji_dict = {
        "mm10": "🐭🧬",
        "hg38": "👤🧬",
    }
    return emoji_dict.get(organism_key, "🌈")


### Bed file functions ####

def create_bed_data(path: str, file_type: str = "bed", to_save: bool = False):
    organims_data = __get_organism_data()
    bed_data = create_table_data(path, file_type, to_save, 
                                            default_columns = BED_DEFAULT_COLUMNS)
    bed_data.update({'organism': organims_data})
    return bed_data


def create_bed_documantation(path: str, file_type: str = "bed", to_save: bool = False):
    """
    Creates a documentation for the BED file.
    Args:
        path (str): The path of the documentation file.
        file_type (str, optional): The type of the file. Defaults to "bed".
        to_save (bool, optional): Whether to save the documentation to a file. Defaults to True.
    """

    bed_data = create_bed_data(path, file_type, to_save)
    print('bed data before object')
    print(bed_data)
    return BedFile(**bed_data) 

#### end of bed file functions ####
### PBM file functions ####

def __get_array_design():
    array_design = ''
    while array_design not in ['ME', 'HK']:
        array_design = input("Enter the array design (ME/HK): ").upper()
        if array_design not in ['ME', 'HK']:
            print("Oh honey, that's not on the list. Choose a valid array design.")
    return array_design


def __create_PBM_source():
    source_id = input("Enter the source id (e.g PMID, GEO ID): ")
    source_path = input("BONUS Enter the source path (link to paper / site.): ")
    pbm_source = __create_source(path=source_path, type='paper', name=source_id)
    return pbm_source


def __get_sequence_length(table_data):
    table = TableFile(**table_data)
    df = table.open_file()
    seq_len = len(df['pbm_sequence'].iloc[0])
    return seq_len


def create_pbm_data(path: str, file_type: str = "pbm", to_save: bool = False):
    array_design = __get_array_design()
    pbm_source = __create_PBM_source()
    description = f"PMB expirment source: {pbm_source[NAME]}"
    table_data = create_table_data(path, file_type, to_save, 
                                            default_columns = PBM_DEFAULT_COLUMNS,
                                            sources=[pbm_source],
                                            description=description)
    seq_len = __get_sequence_length(table_data)
    table_data.update({'seq_len': seq_len, 'ArrayDesign': array_design})
    return table_data


def create_pbm_documantation(path: str, file_type: str = "pbm", to_save: bool = False):
    """
    Creates a documentation for the BED file.
    Args:
        path (str): The path of the documentation file.
        file_type (str, optional): The type of the file. Defaults to "bed".
        to_save (bool, optional): Whether to save the documentation to a file. Defaults to True.
    """

    pbm_data = create_pbm_data(path, file_type, to_save)
    if DEBUG:
        print('pbm data before object')
    print(pbm_data)
    return PBMFile(**pbm_data) 

#### end of PBM file functions ####


##### Table file  functions#####

def create_table_documantation(path: str,
                                file_type: str = "table",
                                have_header: bool = None,
                                index_col: bool = None,
                                comment: str = None,
                                default_columns = []):
    table_data = create_table_data(path, file_type, have_header, index_col, comment, default_columns)
    return TableFile(**table_data)
        

def __create_table_data(path: str,
                    file_key: str,
                    have_header: bool = None,
                    index_col: bool = None,
                    comment: str = None,
                    default_columns = []):
        print("\n===============\n")
        write_ascii('table')
        print("\n===============\n")
        df = open_file_by_extension(path, header = None,
                                     index_col = False,
                                       comment = None, table_key = file_key)
        print('this are the first lines of the file-')
        print(df.head().to_markdown())
        if have_header is None:
            have_header = input("\n===============\nDoes the table have a header? (y/n) ").lower() == 'y'
        header = 0 if have_header else None
        if index_col is None:
            index_col = input("\n===============\nIs one of the columns is the index? (y/n) ").lower() == 'y'
        if index_col:
            index_col = int(input("\n===============\nEnter the index column number: "))
        if comment is None:
            comment = input("\n===============\nWhat is the comment character? (e.g '#', leave empty if not relevant) ")
            comment = None if comment == '' else comment
        columns_description = __get_columns_description(path, header, index_col, comment, default_columns)

        table_data= {'table_key': file_key, 'header': header, 'index_col': index_col, 'comment': comment,
                      'columns_description': columns_description}
        return table_data


def __get_columns_helper(i, col, name=None):
    cur_column = COLUMN_DESCRIPTION_TEMPLATE.copy()
    cur_column[NAME] = input("Name: ") if name is None else name
    cur_column['index'] = i
    # check_type = input("Check type? (y/n) ").lower() == 'y'
    cur_column['description'] = input("Description: ")
    # cur_column['dtype'] =  input("data_ype: ") if check_type else None
    # cur_column['check_type'] = check_type
    return cur_column

def __fix_default_columns(df,columns,index):
    '''
    If a default column is not in the right index,
    the function will fix it.
    '''    
    column = columns[index]
    print(f"\n===============\nDarling, let's fix the default column - {column['name']}!")
    print(f"here are the first 5 lines of the file-")
    for i, name in df.iloc[0].items():
        print(i,':',name)
    print(df.head().to_string())
    correct_index = -1
    while not 0 <= correct_index < len(df.columns):
        correct_index = input(f"\n===============\nWhat is the correct index of the column '{column['name']}'?\n Leave empty if the column is not in the file\n")
        if correct_index == '':
            print(MISSING_COLUMN_MSG)
            exit(1)
        try:
            correct_index = int(correct_index)
        except ValueError:
            print("Sweetheart, your input is as chaotic as a disco ball in a tornado! Please grace me with a valid number, won't you? 💃✨")
            correct_index = -1
    column['index'] = correct_index
    print("Congratulations! Now lets go back to where we were! 🌈✨")
    return column
        
    # check if the input is valid 



def __verify_with_idx_col(df, columns):
    relevant_df = df[[df.columns[i['index']] for i in columns]]
    print(relevant_df.head().to_string())
    resutls = []
    for i in range(len(columns)):
        column = columns[i]
        print(f"Name: {column['name']}\nIndex: {column['index']}\n\
DType: {column['dtype']}\nDescription: {column['description']}")
        user_input = input(f"\n===============\nDoes the description match the data inside the file? (y/n): ")
        if user_input.lower() != 'y':
            print(MISSING_COLUMN_MSG)
            column = __fix_default_columns(df,columns,i)
        resutls.append(column)

    return resutls

def __verify_no_idx_col(df, columns):
    result  = []
    for i in range(len(columns)):
        fixed_col = __fix_default_columns(df,columns,i)
        result.append(fixed_col)
    return result


def __verify_columns_description(df, columns):
    """
     checks if the descriptions of file columns 
     match the data inside.
    """
    print("\n===============\nDarling, let's verify the fabulous descriptions of your columns!")
    idx_col = [col for col in columns if col['index'] is not None]
    verified_idx = __verify_with_idx_col(df, idx_col)
    no_idx_col = [col for col in columns if col['index'] is None]
    verified_no_idx = __verify_no_idx_col(df, no_idx_col)

    # todo: check there is no contradiction between the two lists
    result = verified_idx + verified_no_idx

    print("\nCongratulations, your file is as fabulous as you are! 🌈✨")
    return result


def __get_columns_description(path,  header = None, index_col = None, comment = None, default_columns = []):
    """
    This function verifies the default columns and gets the description of the rest of the columns
    """
    columns_description = []
    print("\n===============\n")
    write_ascii("col-description")
    print("Enter the details of each column")
    df = open_file_by_extension(path, header , index_col, comment)
    # check the default columns of the file
    if len(default_columns):
        default_columns = __verify_columns_description(df, default_columns)
    default_col_index = [col['index'] for col in default_columns]
    col_index = list(range(len(df.columns)))
    col_index = [i for i in col_index if i not in default_col_index]
    col_details = df.columns.tolist() if header is not None else df.iloc[0].tolist()
    for i in col_index:
        col = col_details[i]
        print(f"Enter the details of column {i} '{col}':")
        columns_description.append(__get_columns_helper(i ,
                                                         col, name = col if header is not None else None))

    return columns_description + default_columns
    

def create_table_data(path: str,
                    file_type: str = "table",
                    have_header: bool = None,
                    index_col: bool = None,
                    comment: str = None,
                    default_columns = [],
                    sources = [],
                    description = None):
        """
        create json file for a given table file
        """
        table_data = __create_file_data(path=path, 
                                        file_type = file_type, 
                                        sources = sources,
                                        description = description)
        
        try:
             file_key = get_file_extension(path)
        except ValueError:
            file_key =  __get_table_file_type(path)
        table_data.update(__create_table_data(path, file_key, have_header, index_col, comment, default_columns))
        return table_data



def __get_table_file_type(path):
    """
    In case coudlnt understand the file extension and way to open it
    """
    print("\n===============\nCould not detrmine the file type\n")
    for i, key in enumerate(READ_FUNCTION.keys()):
        print(f"{i}. {key}")
    ext_list = list(READ_FUNCTION.keys())
    for i, ext in enumerate(ext_list):
            print(f"{i}. {ext}")
    file_key = input(f"\n=================\nEnter the file -{path.split('/'[-1])} type index: ")
    file_key = ext_list[int(file_key)] 
    return file_key 

### end of table file functions ###
### source file functions ####
        

def create_documantation(path: str, to_save: bool = True):
    print(f"Creating documentation for {path.split('/')[-1]}")
    keys_list = list(CREATE_TYPE_DICT.keys())
    for i, key in enumerate(keys_list):
         print(f'{i} - {key}')
    file_idx = int('write the index of the file type')
    return CREATE_TYPE_DICT[keys_list[file_idx]](path=path, to_save=to_save)



CREATE_TYPE_DICT = {
     'source' : create_source_documantation,
     'table' : create_table_documantation,
     'bed' : create_bed_documantation,
     'pbm' : create_pbm_documantation
}



def main():
    path = '/home/dsi/toozig/lab_folder/deepBind_training/downloaded_data/DMRT1/GSM1292960_pTH9197_HK_8mer_6759.raw.txt.gz'
    create_table_documantation(path)

if __name__ == '__main__':

    main()