import requests
import json
import pandas as pd
from PyWrike.gateways import OAuth2Gateway1
from PyWrike import (
    validate_token,
    read_config_from_excel,
    authenticate_with_oauth2,
    get_wrike_space_id,
    get_space_details,
    create_new_space,
    get_folders_in_space,
    get_custom_fields,
    map_custom_fields,
    get_titles_hierarchy,
    create_folders_recursively
)


def new_space_main():
    # Prompt for the Excel file path
    excel_path = input("Please enter the path to the Excel file with configuration: ")
    
    # Read the configuration from the Excel sheet
    config = read_config_from_excel(excel_path)
    
    access_token = config.get('Token')
    space_name = config.get('Space to extract data from')
    new_space_title = config.get('New Space Title')

        # Validate the token
    if not validate_token(access_token):
        # If the token is invalid, authenticate using OAuth2 and update the access_token
        wrike = OAuth2Gateway1(excel_filepath=excel_path)
        access_token = wrike._create_auth_info()  # Perform OAuth2 authentication
        print(f"New access token obtained: {access_token}")
    
    if not access_token or not space_name or not new_space_title:
        print("Error: Missing necessary configuration details.")
        return
    
    space_id = get_wrike_space_id(space_name, access_token)
    if not space_id:
        print(f"No Wrike space found with the name '{space_name}'.")
        return
    
    original_space = get_space_details(space_id, access_token)
    if not original_space:
        print(f"Could not fetch details for the space '{space_name}'.")
        return
    
    new_space = create_new_space(original_space, new_space_title, access_token)
    if not new_space:
        print(f"Could not create a new space with the title '{new_space_title}'.")
        return
    
    folders = get_folders_in_space(space_id, access_token)
    if not folders:
        print(f"No folders found in the space '{space_name}'.")
        return

   # Fetch and map custom fields
    original_custom_fields = get_custom_fields(access_token)
    custom_field_mapping = map_custom_fields(original_custom_fields, original_space['id'], new_space['id'], access_token)

    all_paths = []
    for folder in folders:
        if "scope" in folder and folder["scope"] == "WsFolder":
            paths = get_titles_hierarchy(folder["id"], folders)
            all_paths.extend(paths)
    
    new_root_folder_id = new_space['id']
    new_paths_info = create_folders_recursively(all_paths, new_root_folder_id, space_name, new_space_title, access_token, folders, custom_field_mapping)
    
if __name__ == "__new_space_main__":
    new_space_main()
   