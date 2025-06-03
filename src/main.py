import os
from cleanData import cleanData

def getValidFile():
    while True:
        # Get the file path from the user
        filePath = input("Enter the path to the dataset (must be .xlsx, .csv, or .json): ")

        # Check if the file extension is valid
        if filePath.endswith(('.xlsx', '.csv', '.json')):
            # Check if the file actually exists
            if os.path.isfile(filePath):
                return filePath
            else:
                print("The file does not exist. Please enter a valid file path.")
        else:
            print("Invalid file type. Please enter a .xlsx, .csv, or .json file.")

def main():
    # Get the valid file from the user
    filePath = getValidFile()

    # Pass the valid file to the cleanData module for processing
    cleanData(filePath)

if __name__ == "__main__":
    main()
