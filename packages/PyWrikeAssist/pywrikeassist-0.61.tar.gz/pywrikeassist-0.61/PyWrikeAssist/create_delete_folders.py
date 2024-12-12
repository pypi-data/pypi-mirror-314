import pandas as pd
import numpy as np
import requests
from PyWrike.gateways import OAuth2Gateway1
from PyWrike import (
    validate_token,
    authenticate_with_oauth2,
    get_folder_id_by_name,
    get_subfolder_id_by_name,
    create_wrike_project,
    create_wrike_folder,
    delete_wrike_folder,
    delete_wrike_project,
    get_responsible_id_by_name_and_email
)

def create_delete_folders_main():
    # Prompt user for Excel file path
    excel_file = input("Enter the path to the Excel file: ")

    try:
        # Load data from the Excel sheets
        config_df = pd.read_excel(excel_file, sheet_name="Config", header=1)
        project_df = pd.read_excel(excel_file, sheet_name="Projects")
        print("Excel file loaded successfully.")
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # Retrieve configuration data
    access_token = config_df.at[0, "Token"]
    folder_path = config_df.at[0, "Project Folder Path"]

    # Validate or refresh access token
    if not validate_token(access_token):
        client_id = config_df.at[0, "Client ID"]
        client_secret = config_df.at[0, "Client Secret"]
        redirect_url = config_df.at[0, "Redirect URL"]
        access_token = authenticate_with_oauth2(client_id, client_secret, redirect_url)

    parent_folder_id = get_folder_id_by_name(folder_path, access_token)
    if not parent_folder_id:
        print("Parent folder ID not found. Please check the folder path in the configuration.")
        return
    else:
        print(f"Parent folder ID: {parent_folder_id}")

    # Process deletion rows
    for _, row in project_df.iterrows():
        delete_project_title = row.get("Delete Project Title")
        delete_folders = row.get("Delete Folders")

        # If deletion fields are populated, handle deletion
        if pd.notna(delete_project_title):
            project_id = get_subfolder_id_by_name(parent_folder_id, delete_project_title.strip(), access_token)
            if project_id:
                if pd.notna(delete_folders):
                    print(f"Deleting folder '{delete_folders.strip()}' from project '{delete_project_title.strip()}'")
                    delete_wrike_folder(access_token, project_id, delete_folders.strip())
                else:
                    print(f"Deleting project '{delete_project_title.strip()}' itself.")
                    delete_wrike_project(access_token, parent_folder_id, delete_project_title.strip())
            else:
                print(f"Project '{delete_project_title.strip()}' not found, skipping deletion.")

    # Process creation rows
    for _, row in project_df.iterrows():
        project_name = row.get("Create Project Title")
        folder_name = row.get("Create Folders")
        first_name = row.get("First Name")
        last_name = row.get("Last Name")
        email = row.get("Email")
        start_date = row.get("Start Date")
        end_date = row.get("End Date")

        # Skip rows without project creation details
        if pd.isna(project_name):
            continue

        # Convert timestamps to strings
        start_date = start_date.strftime('%Y-%m-%d') if pd.notnull(start_date) else None
        end_date = end_date.strftime('%Y-%m-%d') if pd.notnull(end_date) else None

        # Check if the project or standalone folder already exists
        project_id = get_subfolder_id_by_name(parent_folder_id, project_name, access_token)
        if not project_id:
            print(f"Project '{project_name}' not found. Creating it.")
            if pd.isna(first_name) and pd.isna(last_name) and pd.isna(email) and not start_date and not end_date:
                project_id = create_wrike_folder(access_token, parent_folder_id, project_name)
            else:
                responsible_id = get_responsible_id_by_name_and_email(first_name, last_name, email, access_token)
                if responsible_id:
                    project_id = create_wrike_project(
                        access_token, parent_folder_id, project_name, responsible_id, start_date, end_date
                    )
        else:
            print(f"Project '{project_name}' found with ID: {project_id}")

        # If the project or folder exists or was created successfully, create subfolders
        if project_id and pd.notna(folder_name):
            existing_subfolder_id = get_subfolder_id_by_name(project_id, folder_name, access_token)
            if not existing_subfolder_id:
                print(f"Creating subfolder '{folder_name}' in project/folder '{project_name}'")
                create_wrike_folder(access_token, project_id, folder_name)
            else:
                print(f"Subfolder '{folder_name}' already exists in '{project_name}' with ID: {existing_subfolder_id}")


if __name__ == "__main__":
    create_delete_folders_main()