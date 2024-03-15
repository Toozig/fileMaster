import os
import random
from source.documantation_createor import *
import art
import sys 

FILE_PATH_IDX = 1

FILE_TYPE_DICT= {
    'table': 'For table file, e.g. .csv, .tsv (bed files are table as well, and also vcf 🤯)',
    'bed': 'Specific for bed files, have same functionality as table files... and even more 🤯',
    'pbm': 'For PBM expirement result',
    'source': 'Minimal information about the file. This won\'t\
 give the full functionality of the file package. Don\'t be lazy 😤.',
}

def print_ascii_art():
    # ASCII art for cool header
    ascii_art = """
oooooooooooo  o8o  oooo            ooo        ooooo                        .                                oooooooooo.   ooooooooo   .oooo.     .oooo.        
`888'     `8  `"'  `888            `88.       .888'                      .o8                                `888'   `Y8b d\"\"\"\"\"\"\"8' .dP""Y88b  .dP""Y88b       
 888         oooo   888   .ooooo.   888b     d'888   .oooo.    .oooo.o .o888oo  .ooooo.  oooo d8b            888     888       .8'        ]8P'       ]8P'      
 888oooo8    `888   888  d88' `88b  8 Y88. .P  888  `P  )88b  d88(  "8   888   d88' `88b `888""8P            888oooo888'      .8'       <88b.      .d8P'       
 888    "     888   888  888ooo888  8  `888'   888   .oP"888  `"Y88b.    888   888ooo888  888                888    `88b     .8'         `88b.   .dP'          
 888          888   888  888    .o  8    Y     888  d8(  888  o.  )88b   888 . 888    .o  888                888    .88P    .8'     o.   .88P  .oP     .o      
o888o        o888o o888o `Y8bod8P' o8o        o888o `Y888""8o 8""888P'   "888" `Y8bod8P' d888b              o888bood8P'    .8'      `8bd88P'   8888888888      
                                                                                                                                                               
                                                                                                                                                               
                                                                                                                                                                                                                                                                     
    """
    print(ascii_art)

def welcome_message():
    print(f"\n🤖 Welcome to FileMaster 432 - The not-so-Ultimate-but-what-we-have Server File\
 Organizer! 🤖")
    print("I am Your Organized-Evaluation-Leveraging [YO-EL]. \n"
          "I might not be the most enthusiastic navigator, but I'll help you through the digital\
 cosmos (e.g. DSI server and Dropbox).")
    # print("Just like the Hitchhiker's Guide to the Galaxy, but for your server files!")
    print("Hold tight, and let's get ready for some organized chaos! 🚀📂")



def check_and_print_file(file_path):
    path = os.path.realpath(file_path)
    print(path)
    if os.path.exists(path):
        print("\nFile exists! 😲 Amazeballs!")
        return False
    else:
        print("\nFile not found. 😠 Ugh, seriously?!")
        return True

def ask_for_file_type():
    print("\nPlease choose the file type:")
    available_types= [i for i in list(FILE_TYPE_DICT.keys()) if i in CREATE_TYPE_DICT.keys()]
    for index, key in enumerate(available_types):
        print(f"{index}. {key} - {FILE_TYPE_DICT[key]}")
    print("\n===============\nIf you think the file is not any of the above, please choose 'Generic Source'.")
    print("Or you can just write a new file type 😇")
    print("(Choose generic source if you are not sure about the file type 🫠 )\n")

    while True:
        try:
            file_type_index = int(input("Enter the number of the file type: "))
            if file_type_index in range(len(available_types)):
                return available_types[file_type_index]
            else:
                print("Invalid input. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def generate_insult(username):
    adjective = random.choice(["Fierce", "Fabulous", "Sassy", "Daring"])
    noun = random.choice(["tech-savvy", "data-challenged", "algorithm-averse", "keyboard-warrior"])
    verb = random.choice(["struggling", "stumbling", "tripping", "grasping"])
    return f"Well, well, well! Look who's attempting to organize files!\n {username}, you {adjective} {noun}.\n\
 Your file-naming skills are like a {verb} robot on a dance floor. 💅🌈\n\n"


if __name__ == "__main__":

    os.system('cls' if os.name == 'nt' else 'clear')
    # print_ascii_art()
    art.tprint("FileMaster 432", font="colossal")
    welcome_message()
    username = "Gonen lab user"

    try:
        
        # Get file path from the user
        file_path = sys.argv[1]

        # Check and print the status
        while check_and_print_file(file_path):
            file_path = input("Enter the file path to check (Ctrl+C to exit): \n")

        # Ask for file type information
        file_type = ask_for_file_type()
        print("\n\n===============\nYou have classified the file as:\n")
        write_ascii(file_type)
        file_doc = CREATE_TYPE_DICT[file_type](file_path)
        save_path = file_doc.save_json()
        print(f"\n===============\nFile saved as {save_path}.")

    except KeyboardInterrupt:
        print("\nSo long, and thanks for all the files! Goodbye! 🐡🦈\n")