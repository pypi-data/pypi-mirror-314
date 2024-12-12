import requests
import pandas as pd
from PyWrike.gateways import OAuth2Gateway1
from PyWrike import (
    validate_token,
    authenticate_with_oauth2,
    get_space_id_by_name,
    get_all_tasks_in_space,
    get_folder_id_by_path,
    create_folder_by_path,
    get_task_id_by_title,
    create_subtask_in_parent_task,
    create_task_in_folder, 
    cache_subtasks_from_tasks,
    get_responsible_id_by_name_and_email,
    get_tasks_by_folder_id,
    update_task_with_tags,
    create_task
)

def create_update_tasks_main():
    global task_df
    excel_file = input("Enter the path to the Excel file: ")
    try:
        config_df = pd.read_excel(excel_file, sheet_name="Config", header=1)
        task_df = pd.read_excel(excel_file, sheet_name="Tasks")
    except Exception as e:
        print(f"Failed to read Excel file: {e}")
        return

    headings = list(task_df.columns)

    access_token = config_df.at[0, "Token"]
        # Validate the token
    if not validate_token(access_token):
        # If the token is invalid, authenticate using OAuth2 and update the access_token
        wrike = OAuth2Gateway1(excel_filepath=excel_file)
        access_token = wrike._create_auth_info()  # Perform OAuth2 authentication
        print(f"New access token obtained: {access_token}")

    cached_tasks_by_space = {}  # Dictionary to store cached tasks by space

    if task_df.empty:
        print("No task details provided.")
        return

    for _, row in task_df.iterrows():
        space_name = row.get("Space Name", "")
        folder_path = row.get("Folder Path", "")
        parent_task_title = row.get("Parent Task Title", "")
        parent_task_path = row.get("Folder Path", "")

        if not space_name:
            print(f"Space name is missing for task '{row.get('Title', '')}'. Skipping this task.")
            continue

        if not folder_path:
            print(f"Folder path is missing for task '{row.get('Title', '')}'. Skipping this task.")
            continue
        
        space_id = get_space_id_by_name(space_name, access_token)
        if not space_id:
            print(f"Space '{space_name}' does not exist. Skipping this task.")
            continue

        # Check if tasks for this space have already been cached
        if space_name not in cached_tasks_by_space:
            print(f"[DEBUG] Caching all tasks in the space '{space_name}'.")
            cached_tasks_by_space[space_name] = get_all_tasks_in_space(space_id, access_token)
            cache_subtasks_from_tasks(cached_tasks_by_space[space_name], access_token)

        else:
            print(f"[DEBUG] Using cached tasks for space '{space_name}'.")
            

        # Set the cached tasks for the current space
        global cached_tasks
        cached_tasks = cached_tasks_by_space[space_name]
        

        folder_id = get_folder_id_by_path(folder_path, space_id, access_token)
        if not folder_id:
            user_input = input(f"Folder path '{folder_path}' does not exist. Would you like to create it? (yes/no): ").strip().lower()
            if user_input != 'yes':
                print(f"Task '{row.get('Title', '')}' creation skipped.")
                continue
            folder_id = create_folder_by_path(folder_path, space_id, access_token)
            if not folder_id:
                print(f"Failed to create or locate folder path '{folder_path}'. Skipping this task.")
                continue
        
        task_data = {
            "title": row.get("Title", ""),
            "description": row.get("Description", ""),
            "first_names": row.get("FirstName", "").split(',') if pd.notna(row.get("FirstName")) else [],
            "last_names": row.get("LastName", "").split(',') if pd.notna(row.get("LastName")) else [],
            "emails": row.get("Email", "").split(',') if pd.notna(row.get("Email")) else [],
            "importance": row.get("Priority", ""),
            "start_date": row.get("Start Date"),
            "end_date": row.get("End Date")
        }

                # Dynamically add any custom field columns to task_data
        for col_name in row.index:
            if col_name not in task_data:  # If this column is not already part of task_data
                field_value = row.get(col_name, "")
                if pd.notna(field_value):
                    task_data[col_name] = str(field_value).strip() if isinstance(field_value, str) else str(field_value)
                else:
                    task_data[col_name] = ""


        # Check if parent task title is provided (Subtask scenario)
        if pd.notna(parent_task_title):
            if parent_task_path:
                parent_folder_id = get_folder_id_by_path(parent_task_path, space_id, access_token)
                if parent_folder_id:
                    parent_task_id = get_task_id_by_title(parent_task_title, parent_folder_id, access_token)
                    if parent_task_id:
                        print(f"[DEBUG] Creating subtask '{task_data['title']}' under parent task '{parent_task_title}'.")
                        create_subtask_in_parent_task(parent_task_id, space_id, task_data, access_token, cached_tasks)
                    else:
                        print(f"Parent task '{parent_task_title}' not found. Skipping this subtask.")
                else:
                    print(f"Parent task folder path '{parent_task_path}' not found. Skipping this subtask.")
            else:
                print(f"Parent task path is missing for subtask '{row.get('Title', '')}'. Skipping this subtask.")
        else:
            # No parent task title provided, so create a standalone task
            print(f"[DEBUG] Creating standalone task '{task_data['title']}' in folder '{folder_path}'.")
            create_task_in_folder(folder_id, space_id, task_data, access_token, cached_tasks)

if __name__ == '__create_update_tasks_main__':
    create_update_tasks_main()