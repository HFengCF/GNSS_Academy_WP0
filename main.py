import sys, os

def main():
    
    Scen_path = sys.argv[1]

    folder_output = Scen_path + 'OUT'

    if not os.path.exists(folder_output):
        os.makedirs(folder_output)