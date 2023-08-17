# Подключаем библиотеки
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials


class Table:
    def open_table(self):
        if not self.is_open_table:
            self.is_open_table = True

            driveService = apiclient.discovery.build('drive', 'v3',
                                                     http=self.httpAuth)
            # Выбираем работу с Google Drive и 3 версию API

            access = driveService.permissions().create(
                fileId=self.spreadsheetId,
                body={'type': 'user', 'role': 'writer', 'emailAddress': 'andreevnikita529@gmail.com'},
                # Открываем доступ на редактирование
                fields='id'
            ).execute()

    def __init__(self):
        self.is_open_table = False
        self.CREDENTIALS_FILE = 'trader-in-table-2e38c4d420a7.json'
        # Имя файла с закрытым ключом, вы должны подставить свое

        # Читаем ключи из файла
        sp_ipa = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.CREDENTIALS_FILE, sp_ipa)

        self.httpAuth = self.credentials.authorize(httplib2.Http())  # Авторизуемся в систем
        self.service = apiclient.discovery.build('sheets', 'v4', http=self.httpAuth)
        # Выбираем работу с таблицами и 4 версию API

    def new_table(self):
        spreadsheet = self.service.spreadsheets().create(body={
            'properties': {'title': 'Первый тестовый документ', 'locale': 'ru_RU'},
            'sheets': [{'properties': {'sheetType': 'GRID',
                                       'sheetId': 0,
                                       'title': 'Лист номер один',
                                       'gridProperties': {'rowCount': 3000, 'columnCount': 15}}}]
        }).execute()
        self.spreadsheetId = spreadsheet['spreadsheetId']  # сохраняем идентификатор файла
        print('https://docs.google.com/spreadsheets/d/' + self.spreadsheetId)

    def write_in_table(self, sp: list, span):
        print(sp, span)
        results = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheetId, body={
            "valueInputOption": "USER_ENTERED",
            # Данные воспринимаются, как вводимые пользователем (считается значение формул)
            "data": [
                {"range": f"Лист номер один!{span}",
                 "majorDimension": "ROWS",  # Сначала заполнять строки, затем столбцы
                 "values": sp}
            ]
        }).execute()

    @staticmethod
    def int_to_stra(inti):
        return 'Z' * (inti // (ord('Z') - ord('A') + 1)) + chr(inti % (ord('Z') - ord('A') + 1) + ord('A') + 1)
