import requests
import json
import pandas as pd
import os
from PyWrike.gateways import OAuth2Gateway1
from PyWrike import (
    validate_token,
    authenticate_with_oauth2,
    get_all_spaces,
    get_space_id_from_name,
    get_all_folders_json,
    save_to_json
)

# Main function to execute the export
def wrike_export_json_main():
    # Load configuration and delete task details from Excel file
    excel_file = input("Enter the path to the Excel file: ")
    if not os.path.isfile(excel_file):
        print("File does not exist. Please check the path.")
        exit()
    
    try:
        config_df = pd.read_excel(excel_file, sheet_name="Config", header=1)
    except Exception as e:
        print(f"Failed to read Excel file: {e}")
        exit()

    # Extract token and space name from the Config sheet
    wrike_api_token = config_df.at[0, "Token"]
    space_name = config_df.at[0, "Space to extract data from"]

    # Validate token
    if not validate_token(wrike_api_token):
        client_id = config_df.at[0, "Client ID"]
        client_secret = config_df.at[0, "Client Secret"]
        redirect_url = config_df.at[0, "Redirect URI"]
        wrike_api_token = authenticate_with_oauth2(client_id, client_secret, redirect_url)

    # Get spaces and the ID for the specified space
    spaces_response = get_all_spaces(wrike_api_token)
    workspace_id = get_space_id_from_name(space_name, spaces_response)

    if not workspace_id:
        print(f"Space with name '{space_name}' not found.")
        exit()

    workspace_data = get_all_folders_json(workspace_id, wrike_api_token)
    save_to_json(workspace_data, space_name)

# Execute main function if file is run as a script
if __name__ == "__main__":
    wrike_export_json_main()
