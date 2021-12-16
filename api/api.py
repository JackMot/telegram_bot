import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'config/credentials.json'
# ID Google Sheets документа (можно взять из его URL)
spreadsheet_id = '1Fzhkd4fhKD8ux-Ocv5oXXix_e7wd--7Yweorum8YkI0'

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)


def add_data_to_sheet(data):
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": "A2:B999",
                 "majorDimension": "ROWS",
                 "values": data}
            ]
        }
    ).execute()


# Пример чтения таблицы 
def read_sheet(list_name: str, range_of_list: str):
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f"'{list_name}'!" + f'{range_of_list}',  # 'A1:E10'
        majorDimension='ROWS'
    ).execute()
    return values


# пришло такое значение ['test 16', 'This is C3']
def add_data(request: list, sheet: str):
    row_data = read_sheet(sheet, 'A1:B999')
    data = row_data.get('values')[1:]
    # print(data)

    for item in data:
        if item[0] == request[0]:
            item[1] = request[1]
            # print(data)
            add_data_to_sheet(data)
            return True

    data.append(request)
    # print(data)
    add_data_to_sheet(data)
    return True


# Пример создания листа
def create_list_sheet(year: str):
    results = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=
        {
            "requests": [
                {
                    "addSheet": {
                        "properties": {
                            "title": "Студенты",
                            "gridProperties": {
                                "rowCount": 40,
                                "columnCount": 12
                            }
                        }
                    }
                }
            ]
        }).execute()
