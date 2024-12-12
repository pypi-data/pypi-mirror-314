import requests
import pandas as pd
from PyWrike.gateways import OAuth2Gateway1
from PyWrike import (
    validate_token,
    authenticate_with_oauth2,
    get_space_id_by_name,
    get_folder_id_by_path,
    create_folder_in_space,
    get_all_tasks_in_folder,
    get_task_detail,
    create_task_folder,
    get_task_id_by_titles,
    get_custom_fields,
    map_custom_fields_propagate
)

def propagate_tasks_main():
    # Ask the user to input the path of the Excel file
    excel_file = input("Please enter the full path to the Excel file: ")

    # Load the access token from the 'Config' sheet
    config_df = pd.read_excel(excel_file, sheet_name='Config', header=1)
    access_token = config_df.at[0, 'Token']

    # Validate the token
    if not validate_token(access_token):
        # If the token is invalid, authenticate using OAuth2 and update the access_token
        wrike = OAuth2Gateway1(excel_filepath=excel_file)
        access_token = wrike._create_auth_info()  # Perform OAuth2 authentication
        print(f"New access token obtained: {access_token}")

    # Load the propagation details from the file
    propagate_df = pd.read_excel(excel_file, sheet_name='Propagate')

    # Iterate over the rows in the 'Propagate' sheet
    for index, row in propagate_df.iterrows():
        source_space_name = row['Space Name']
        source_path = row['Source Path']
        task_title = row['Task Title']
        dest_space_name = row["Destination Space Name"]

        # Check if 'Destination Path' is valid (non-NaN)
        if pd.isna(row['Destination Path']):
            print(f"Skipping row {index} due to missing 'Destination Path'.")
            continue

        destination_path = row['Destination Path'].strip()
        
        # Check for destination space in the Destination Path
        dest_space_name = row.get('Destination Space Name', source_space_name)  # Use the same space if no destination space provided
        
        # Get the space IDs for both source and destination spaces
        source_space_id = get_space_id_by_name(source_space_name, access_token)
        dest_space_id = get_space_id_by_name(dest_space_name, access_token)
    
        # Fetch and map custom fields
        original_custom_fields = get_custom_fields(access_token)
        custom_field_mapping = map_custom_fields_propagate(original_custom_fields, source_space_id, dest_space_id, access_token)

        
        # Retrieve the source folder ID
        source_folder_id = get_folder_id_by_path(source_path, source_space_id, access_token)
        if not source_folder_id:
            continue

        # Retrieve or create the destination folder in the destination space
        destination_folder_id = get_folder_id_by_path(destination_path, dest_space_id, access_token)
        if not destination_folder_id:
            # Create the destination folder if it doesn't exist
            destination_folder_name = destination_path.split('\\')[-1]
            parent_folder_path = '\\'.join(destination_path.split('\\')[:-1])
            parent_folder_id = get_folder_id_by_path(parent_folder_path, dest_space_id, access_token)
            if not parent_folder_id:
                print(f"Parent folder for '{destination_folder_name}' not found in destination space. Skipping.")
                continue
            destination_folder_id = create_folder_in_space(destination_folder_name, parent_folder_id, access_token)

        if pd.isna(task_title):
            # Create subfolder and replicate the tasks
            new_subfolder_id = create_folder_in_space(source_path.split('\\')[-1], destination_folder_id, access_token)
            tasks = get_all_tasks_in_folder(source_folder_id, access_token)
            for task in tasks:
                task_id = task['id']
                
                # Retrieve full details for the task
                task_details = get_task_detail(task_id, access_token)
                # Map custom fields for the task
                mapped_custom_fields = []
                for field in task_details.get('customFields', []):
                    field_id = field['id']
                    if field_id in custom_field_mapping:
                        mapped_custom_fields.append({
                            'id': custom_field_mapping[field_id],
                            'value': field['value']
                        })
                
                # Create the task in the new subfolder with all details
                create_task_folder(new_subfolder_id, task_details, access_token, mapped_custom_fields)

        else:
            # Create a new task instead of updating an existing one
            task_id = get_task_id_by_titles(source_folder_id, task_title, access_token)
            if task_id:
                task_details = get_task_detail(task_id, access_token)
                # Map custom fields for the task
                mapped_custom_fields = []
                for field in task_details.get('customFields', []):
                    field_id = field['id']
                    if field_id in custom_field_mapping:
                        mapped_custom_fields.append({
                            'id': custom_field_mapping[field_id],
                            'value': field['value']
                        })
                create_task_folder(destination_folder_id, task_details, access_token, mapped_custom_fields)

                



