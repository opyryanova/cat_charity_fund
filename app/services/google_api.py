from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.constants import COLUMN_COUNT, ROW_COUNT
from app.models.charity_project import CharityProject


DATETIME_FORMAT = '%Y/%m/%d %H:%M:%S'


async def create_spreadsheets(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {
            'title': 'Отчет QRKot',
            'locale': 'ru_RU',
        },
        'sheets': [
            {
                'properties': {
                    'sheetType': 'GRID',
                    'sheetId': 0,
                    'title': 'Отчет',
                    'gridProperties': {
                        'rowCount': ROW_COUNT,
                        'columnCount': COLUMN_COUNT,
                    },
                }
            }
        ],
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
    spreadsheetid: str,
    wrapper_services: Aiogoogle,
) -> None:
    drive_service = await wrapper_services.discover('drive', 'v3')
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email,
    }
    await wrapper_services.as_service_account(
        drive_service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id',
        )
    )


async def update_spreadsheets_value(
    spreadsheetid: str,
    projects: list[CharityProject],
    wrapper_services: Aiogoogle,
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    now_datetime = datetime.now().strftime(DATETIME_FORMAT)

    table_values: list[list[str]] = [
        ['Отчет по закрытым проектам QRKot'],
        [f'Дата и время формирования: {now_datetime}'],
        ['Название проекта', 'Время сбора (дни)', 'Описание'],
    ]

    for project in projects:
        duration = project.close_date - project.create_date
        days = duration.days
        table_values.append(
            [project.name, str(days), project.description]
        )

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values,
    }

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f'A1:C{len(table_values)}',
            valueInputOption='USER_ENTERED',
            json=update_body,
        )
    )
