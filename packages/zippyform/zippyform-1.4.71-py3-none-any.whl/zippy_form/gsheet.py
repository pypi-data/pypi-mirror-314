from django.conf import settings

import gspread
import re
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from zippy_form.models import GoogleCredentials

from zippy_form.utils import FORM_TYPE, GSHEET_TYPES

gsheet_perm_type = "user"
gsheet_role = "writer"


def gsheet_init():
    """
    Gsheet - Initialize
    """
    try:
        # Check if form submission is allowed to sync on Gsheet
        sync_form_submission_to_gsheet = settings.ZF_GSHEET_SYNC_FORM_SUBMISSION
    except:
        sync_form_submission_to_gsheet = False

    if sync_form_submission_to_gsheet:
        try:
            # Check if user provided Gsheet credentials in settings file
            gsheet_credentials = settings.ZF_GSHEET_CREDENTIALS
        except:
            gsheet_credentials = None

        if gsheet_credentials:
            try:
                # Check if user provided Gsheet credentials in settings file are valid
                credentials = ServiceAccountCredentials.from_json_keyfile_dict(gsheet_credentials)

                # Authenticate with Google Sheets API
                gc = gspread.authorize(credentials)

                return gc
            except:
                pass

    return None


def create_gsheet_map_form(form, fields, gsheet_type, delete_sync_fields, existing_gsheet_url, form_gsheet_mapping_history, spreadsheet=None):
    """
    Create Gsheet & map to form
    """
    gc = gsheet_init()
    if gc:
        # Name of the Google Sheet to create
        sheet_name = str(form.id)
        try:
            # Create Gsheet
            if form.account.admin_email:
                if existing_gsheet_url:
                    spreadsheet_url = existing_gsheet_url
                else:
                    spreadsheet = gc.create(sheet_name)
                    spreadsheet_url = spreadsheet.url
                add_field_labels_to_gsheet(fields, form, gsheet_type, spreadsheet_url, spreadsheet, delete_sync_fields, existing_gsheet_url)
                if not existing_gsheet_url:
                    spreadsheet.share(form.account.admin_email, perm_type=gsheet_perm_type, role=gsheet_role)

                # Save Gsheet URL to the form
                if spreadsheet_url:
                    form.gsheet_url = spreadsheet_url
                    form.save()
                    form_gsheet_mapping_history.zf_gsheet_url = spreadsheet_url
                    form_gsheet_mapping_history.save()
        except gspread.exceptions.APIError as e:
            print(str(e))
        except Exception as e:
            print("str", str(e))


def create_spreadsheet_in_user_google_account(request, form, fields, gsheet_type, delete_sync_fields, existing_gsheet_url, form_gsheet_mapping_history, spreadsheet=None):
    """
    Create Spreadsheet on user google account & share to user - Gsheet Type 2
    """
    account_id = request.headers['ZF-SECRET-KEY']
    remove_multiple_fields_from_gsheet(delete_sync_fields, form, gsheet_type, existing_gsheet_url)
    try:
        if existing_gsheet_url:
            spreadsheet_url = existing_gsheet_url
        else:
            credentials = get_credential_object(account_id)

            # Build service objects
            sheets_service = build('sheets', 'v4', credentials=credentials)
            drive_service = build('drive', 'v3', credentials=credentials)
            people_service = build('people', 'v1', credentials=credentials)

            spreadsheet = {
                'properties': {
                    'title': str(form.id)
                }
            }
            spreadsheet = sheets_service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
            spreadsheet_id = spreadsheet.get('spreadsheetId')
            spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
        gsheet_url = spreadsheet_url
        add_field_labels_to_gsheet(fields, form, gsheet_type, gsheet_url, spreadsheet, delete_sync_fields, existing_gsheet_url)

        # Get OAuth user email
        if not existing_gsheet_url:
            profile = people_service.people().get(resourceName='people/me', personFields='emailAddresses').execute()
            user_email = profile['emailAddresses'][0]['value']

            # Share the spreadsheet with the user's email
            permission = {
                'type': 'user',
                'role': 'writer',
                'emailAddress': user_email
            }
            drive_service.permissions().create(
                fileId=spreadsheet_id,
                body=permission,
                fields='id',
            ).execute()
        form.gsheet_url = spreadsheet_url
        form.gsheet_type = GSHEET_TYPES[1][0]
        form.save()
        form_gsheet_mapping_history.custom_gsheet_url = spreadsheet_url
        form_gsheet_mapping_history.save()
        response_data = {
            'spreadsheet_url': spreadsheet_url,
            'message': f"Spreadsheet created and shared with {user_email} successfully"
        }
        return response_data

    except GoogleCredentials.DoesNotExist:
        return {"status": 'error', "msg": "Google credentials not found for the account"}

    except Exception as e:
        return str(e)


def remove_multiple_fields_from_gsheet(field_labels, form,gsheet_type, existing_gsheet_url):
    """
    Remove multiple fields from Gsheet
    """
    gsheet_url = existing_gsheet_url
    if gsheet_url:
        if gsheet_type == GSHEET_TYPES[1][0]:
            try:
                credentials = get_credential_object(form.account.id)  # Ensure you're using the correct credentials
                gc = gspread.authorize(credentials)
                spreadsheet = gc.open_by_url(gsheet_url)
            except Exception as e:
                spreadsheet = None
        else:
            spreadsheet = open_gsheet(form)
        if spreadsheet:
            # Select the worksheet where you want to send data (by default, the first sheet)
            worksheet = spreadsheet.get_worksheet(0)

            # Find indices of columns with the specified labels
            column_indices = []
            for label in field_labels:
                try:
                    cell = worksheet.find(label)
                    column_indices.append(cell.col)
                except Exception as e:
                    print(f"Failed to find column with label {label}: {e}")

            # Sort indices in descending order to avoid index shifting issues when deleting columns
            column_indices.sort(reverse=True)

            # Delete the columns
            for column_index in column_indices:
                try:
                    worksheet.delete_columns(column_index)
                except Exception as e:
                    print(f"Failed to delete column {column_index}: {e}")


def get_credential_object(account_id):
    """
    Get "User Google Credentials" From DB & return "Google Credentials"
    """
    try:
        google_credentials = GoogleCredentials.objects.get(account__id=account_id)
        credentials_data = google_credentials.credentials
        token = credentials_data.get('token')
        refresh_token = credentials_data.get('refresh_token')
        token_uri = credentials_data.get('token_uri')
        client_id = credentials_data.get('client_id')
        client_secret = credentials_data.get('client_secret')
        scopes = credentials_data.get('scopes')

        # Create Credentials object
        credentials = Credentials(
            token=token,
            refresh_token=refresh_token,
            token_uri=token_uri,
            client_id=client_id,
            client_secret=client_secret,
            scopes=scopes
        )

        return credentials
    except Exception as e:
        print(str(e))


def open_gsheet(form):
    """
    Open Gsheet
    """
    spreadsheet = None

    gc = gsheet_init()
    if gc:
        try:
            # Try to open the Google Sheet by its url
            spreadsheet = gc.open_by_url(form.gsheet_url)
        except gspread.exceptions.SpreadsheetNotFound as e:
            # If the sheet doesn't exist
            spreadsheet = None

    return spreadsheet


def add_field_labels_to_gsheet(fields, form, gsheet_type, gsheet_url, spreadsheet=None,
                               delete_sync_fields=[], existing_gsheet_url=None):
    """
    Add fields labels to Gsheet
    """
    remove_multiple_fields_from_gsheet(delete_sync_fields, form, gsheet_type, existing_gsheet_url)
    form_type = form.type

    # Extract worksheet ID directly from the gsheet_url
    if gsheet_type == GSHEET_TYPES[2][0]:
        try:
            # Use regular expression to find the 'gid' parameter in the URL
            match = re.search(r'gid=(\d+)', gsheet_url)
            if match:
                worksheet_id = int(match.group(1))
            else:
                raise ValueError("No valid worksheet ID found in the URL")
        except Exception as e:
            print(f"Failed to extract worksheet ID: {e}")
            return

    if gsheet_url:
        if gsheet_type in [GSHEET_TYPES[1][0], GSHEET_TYPES[2][0]]:
            try:
                credentials = get_credential_object(form.account.id)  # Ensure you're using the correct credentials
                gc = gspread.authorize(credentials)
                spreadsheet = gc.open_by_url(gsheet_url)
            except Exception as e:
                print(f"Failed to open spreadsheet: {e}")
                spreadsheet = None
        print(gsheet_type, spreadsheet, "check...")
        if gsheet_type == GSHEET_TYPES[0][0] and spreadsheet is None:
            gc = gsheet_init()
            if gc:
                try:
                    # Try to open the Google Sheet by its url
                    spreadsheet = gc.open_by_url(gsheet_url)
                except gspread.exceptions.SpreadsheetNotFound as e:
                    # If the sheet doesn't exist
                    spreadsheet = None

    if spreadsheet:
        try:
            print(spreadsheet)
            # Select the worksheet where you want to send data (by default, the first sheet)
            if gsheet_type in [GSHEET_TYPES[0][0], GSHEET_TYPES[1][0]]:
                worksheet = spreadsheet.get_worksheet(0)
            else:
                worksheets = spreadsheet.worksheets()
                for ws in worksheets:
                    if ws.id == worksheet_id:
                        worksheet = ws
                        break

            # Define the row index where you want to add the column
            heading_label_row_index = 1

            # ---- Heading Label ---- #
            # Get the current headers from the worksheet
            current_headers = worksheet.row_values(heading_label_row_index)
            current_headers_set = set(current_headers)  # Convert to set for quick lookup
            current_headers_count = len(current_headers)

            # Insert new columns
            if current_headers_count == 0:
                # If no headers present
                start_column = 0

                if form_type == FORM_TYPE[0][0]:
                    new_column_values = ['Submission ID', 'Status', "Last Activity"]
                else:
                    new_column_values = ['Submission ID', 'Status', "Last Activity", "Payment Type", "Payment Mode",
                                         'Total Amount Paid']

                worksheet.format('A1:ZZZ1', {'textFormat': {'bold': True}})
            else:
                # If headers already present, skip existing fields
                start_column = current_headers_count

                new_column_values = []
                required_fields = ['Submission ID', 'Status', "Last Activity"]

                # Only add the required fields if they are not already present
                for field in required_fields:
                    if field not in current_headers_set:
                        new_column_values.append(field)

                if gsheet_type == GSHEET_TYPES[2][0]:
                    if form_type != FORM_TYPE[0][0]:
                        additional_fields = ["Payment Type", "Payment Mode", 'Total Amount Paid']
                        for field in additional_fields:
                            if field not in current_headers_set:
                                new_column_values.append(field)

            # Form the fields & save to "new_column_values"
            for field in fields:
                if field['label'] not in current_headers_set:
                    new_column_values.append(field['label'])

            for i, value in enumerate(new_column_values, start=start_column):
                worksheet.update_cell(heading_label_row_index, i + 1, value)
        except Exception as e:
            print(str(e), "Error Message....")


def update_field_label_in_gsheet(old_field_label, new_field_label, form):
    """
    Update field label in Gsheet
    """
    gsheet_url = form.gsheet_url

    if gsheet_url:
        if form.gsheet_type == GSHEET_TYPES[1][0]:
            try:
                credentials = get_credential_object(form.account.id)  # Ensure you're using the correct credentials
                gc = gspread.authorize(credentials)
                spreadsheet = gc.open_by_url(gsheet_url)
            except Exception as e:
                print(f"Failed to open spreadsheet: {e}")
                spreadsheet = None
        else:
            spreadsheet = open_gsheet(form)

        if spreadsheet:
            # Select the worksheet where you want to send data (by default, the first sheet)
            worksheet = spreadsheet.get_worksheet(0)

            current_headers = worksheet.row_values(1)

            if old_field_label in current_headers:
                index = current_headers.index(old_field_label)
                current_headers[index] = new_field_label

                worksheet.update('A1:ZZZ1', [current_headers])


def remove_field_from_gsheet(field_label, form):
    """
    Remove field from Gsheet
    """
    gsheet_url = form.gsheet_url
    if gsheet_url:
        if form.gsheet_type == GSHEET_TYPES[1][0] or GSHEET_TYPES[2][0] :
            try:
                credentials = get_credential_object(form.account.id)  # Ensure you're using the correct credentials
                gc = gspread.authorize(credentials)
                spreadsheet = gc.open_by_url(gsheet_url)
            except Exception as e:
                print(f"Failed to open spreadsheet: {e}")
                spreadsheet = None
        else:
            spreadsheet = open_gsheet(form)
        if spreadsheet:
            # Select the worksheet where you want to send data (by default, the first sheet)
            worksheet = spreadsheet.get_worksheet(0)

            # Find the index of the columns with the specified label name
            column_index = worksheet.find(field_label).col

            # Delete the Columns
            worksheet.delete_columns(column_index)


def send_form_data_to_gsheet(method, form, form_submission_id, form_submission_data, gsheet_type, gsheet_mapping_field_list):
    """
    Send form data to Gsheet - Gsheet Type 1, Gsheet Type 2, Gsheet Type 3
    """
    gsheet_url = form.gsheet_url
    if gsheet_url:
        if gsheet_type in [GSHEET_TYPES[1][0], GSHEET_TYPES[2][0]]:
            try:
                credentials = get_credential_object(form.account.id)  # Ensure you're using the correct credentials
                gc = gspread.authorize(credentials)
                spreadsheet = gc.open_by_url(gsheet_url)
                if gsheet_type == GSHEET_TYPES[2][0]:
                    # Gsheet Type 3
                    send_form_data_to_existing_gsheet_create(method, form, form_submission_id, form_submission_data, gsheet_type,
                                                      gsheet_mapping_field_list,spreadsheet)
                    spreadsheet = None

            except Exception as e:
                print(f"Failed to open spreadsheet: {e}")
                spreadsheet = None

        else:
            spreadsheet = open_gsheet(form)
        if spreadsheet:
            # Select the worksheet where you want to send data (by default, the first sheet)
            worksheet = spreadsheet.get_worksheet(0)

            # Get the header row from the worksheet
            header_row_values = worksheet.row_values(1)
            if header_row_values:
                # If it has Header Row
                if method == "save":
                    form_submission_data['Submission ID'] = form_submission_id

                    new_row = [form_submission_data.get(header, "") for header in header_row_values]
                    worksheet.append_row(new_row)
                else:
                    # Get all the submission id from column 1
                    submission_id_column_values = worksheet.col_values(1)

                    if form_submission_id in submission_id_column_values:
                        # Get row index which we need to update
                        row_index = submission_id_column_values.index(form_submission_id) + 1
                        for key, value in form_submission_data.items():
                            worksheet.update_cell(row_index, header_row_values.index(key) + 1, value)


def send_form_data_to_existing_gsheet_create(method, form, form_submission_id, form_submission_data, gsheet_type,
                                             gsheet_mapping_field_list, spreadsheet):
    """
    Send form data to Gsheet - Gsheet Type 3
    """
    import re

    gsheet_url = form.gsheet_url
    match = re.search(r"gid=(\d+)", gsheet_url)
    if match:
        worksheet_id = int(match.group(1))
    else:
        print("Invalid Google Sheet URL: 'gid' not found")
        return

    worksheets = spreadsheet.worksheets()

    for ws in worksheets:
        if ws.id == worksheet_id:
            worksheet = ws
            break
    else:
        print("Worksheet not found")
        return

    # Define static headers based on form type
    if form.type == FORM_TYPE[0][0]:
        static_headers = ['Submission ID', 'Status', "Last Activity"]
    else:
        static_headers = ['Submission ID', 'Status', "Last Activity", "Payment Type", "Payment Mode",
                          'Total Amount Paid']

    try:
        if worksheet:
            gsheet_headers = worksheet.row_values(1)
            mapped_columns = {}

            # Map dynamic fields
            for gsheet_mapping_field_dict in gsheet_mapping_field_list:
                gsheet_field_name = gsheet_mapping_field_dict['gsheet_column_name']
                field_name = gsheet_mapping_field_dict['field_name']
                if gsheet_field_name in gsheet_headers:
                    column_index = gsheet_headers.index(gsheet_field_name) + 1
                    mapped_columns[field_name] = column_index

            # Map static headers if they are present in the sheet
            for static_header in static_headers:
                if static_header in gsheet_headers:
                    column_index = gsheet_headers.index(static_header) + 1
                    mapped_columns[static_header] = column_index

            if method == 'save':
                next_row = len(worksheet.col_values(1)) + 1

                # Check if there are any values in the next row's columns
                while True:
                    row_values = worksheet.row_values(next_row)
                    if not any(row_values):  # If all values in the next row are empty
                        break
                    next_row += 1

                form_submission_data['Submission ID'] = form_submission_id
                for form_field, column_index in mapped_columns.items():
                    form_submission_data_field = form_submission_data.get(form_field, None)
                    if form_submission_data_field is not None:
                        worksheet.update_cell(next_row, column_index, form_submission_data_field)

            else:
                # Update an existing row based on form_submission_id
                cell = worksheet.find(form_submission_id)
                if not cell:
                    return
                row_number = cell.row
                for form_field, column_index in mapped_columns.items():
                    form_submission_data_field = form_submission_data.get(form_field, None)
                    if form_submission_data_field is not None:
                        worksheet.update_cell(row_number, column_index, form_submission_data_field)

    except Exception as e:
        print(str(e), "Error Message....")

def remove_form_data_from_gsheet(form, form_submission_id):
    """
    Remove form data from Gsheet
    """
    gsheet_url = form.gsheet_url
    worksheet_id = int(gsheet_url.split('=')[1])
    gsheet_type = form.gsheet_type
    if gsheet_url:
        if gsheet_type in [GSHEET_TYPES[1][0], GSHEET_TYPES[2][0]]:
            try:
                credentials = get_credential_object(form.account.id)  # Ensure you're using the correct credentials
                gc = gspread.authorize(credentials)
                spreadsheet = gc.open_by_url(gsheet_url)
            except Exception as e:
                print(f"Failed to open spreadsheet: {e}")
                spreadsheet = None

        else:
            spreadsheet = open_gsheet(form)

        if spreadsheet:

            if gsheet_type == [GSHEET_TYPES[0][0], GSHEET_TYPES[1][0]]:
                # Select the worksheet where you want to send data (by default, the first sheet)
                worksheet = spreadsheet.get_worksheet(0)
            else:
                worksheets = spreadsheet.worksheets()
                for ws in worksheets:
                    if ws.id == worksheet_id:
                        worksheet = ws
                        break
            # Find the index of the row with the specified Submission ID
            cell = worksheet.find(str(form_submission_id))

            # Delete the row
            worksheet.delete_row(cell.row)
