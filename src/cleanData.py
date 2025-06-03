import pandas as pd
import os

def cleanData(filePath):

    if filePath.endswith(".csv"):
        data = pd.read_csv(filePath)
    elif filePath.endswith('.xlsx'):
        data = pd.read_excel(filePath)
    elif filePath.endswith('.json'):
        data = pd.read_json(filePath)

    # Remove duplicate entries
    data = data.drop_duplicates()

    # Remove unnecessary column
    data = data.drop(columns = "Not_Useful_Column")

    # Remove invalid charaters in last name column
    data["Last_Name"] = data["Last_Name"].str.strip("._/")

    # Clean formatting of phone number
    data["Phone_Number"] = data["Phone_Number"].astype(str)
    data["Phone_Number"] = data["Phone_Number"].str.replace('[^a-zA-Z0-9]','', regex=True)
    data["Phone_Number"] = data["Phone_Number"].apply(lambda x: x[0:3] + '-' + x[3:6] + '-' + x[6:10])
    data["Phone_Number"] = data["Phone_Number"].str.replace('nan--','', regex=True)
    data["Phone_Number"] = data["Phone_Number"].str.replace('Na--','', regex=True)
    data["Phone_Number"] = data["Phone_Number"].str.replace('--','', regex=True)

    # Split adress column to make more readable
    data[["Street_Adress", "State", "Zip_Code"]] = data["Address"].str.split(',',n=2, expand=True)

    # Format Yes and No to Y and N
    data["Paying Customer"] = data["Paying Customer"].str.replace('Yes', 'Y')
    data["Paying Customer"] = data["Paying Customer"].str.replace('No', 'N')
    data["Do_Not_Contact"] = data["Do_Not_Contact"].str.replace('Yes', 'Y')
    data["Do_Not_Contact"] = data["Do_Not_Contact"].str.replace('No', 'N')

    # Fill N/a, None, NaN with blank space 
    data = data.fillna('')

    # Drop the people that have selected 'Yes' for Do Not Contact
    for x in data.index:
        if data.loc[x, "Do_Not_Contact"] == 'Y':
            data.drop(x, inplace=True)

    # Drop the people that have not entered a phone number
    for x in data.index:
        if data.loc[x, "Phone_Number"] == '':
            data.drop(x, inplace=True)

    # Fix the indexing after dropping rows
    data = data.reset_index(drop=True)


    cleanedData = data

    # Generate new file path with "Cleaned" added to the original file name
    fileDir, fileName = os.path.split(filePath) 
    base_name, ext = os.path.splitext(fileName)  
    newFileName = f"{base_name}_Cleaned{ext}"
    newFilePath = os.path.join(fileDir, newFileName)
    
    # Save cleaned data to the new file
    if filePath.endswith(".csv"):
        data.to_csv(newFilePath, index=False)
    elif filePath.endswith(".xlsx"):
        data.to_excel(newFilePath, index=False)
    elif filePath.endswith(".json"):
        data.to_json(newFilePath, orient="records", lines=True)

    print(f"Cleaned data saved to {newFilePath}")
    
    return cleanedData  



