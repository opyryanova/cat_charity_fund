from datetime import datetime

from aiogoogle import Aiogoogle
from fastapi import HTTPException, status

from app.core.config import settings
from app.core.constants import (
    COLUMN_COUNT,
    ROW_COUNT,
    DATETIME_FORMAT,
    SHEET_ID,
    SHEET_TITLE,
    REPORT_TITLE,
    MIN_GOOGLE_COLUMNS,
)
from app.models.charity_project import CharityProject


def get_spreadsheet_body(now_datetime: str) -> dict:
    return {
        'properties': {
            'title': f'Отчет QRKot от {now_datetime}',
            'locale': 'ru_RU',
        },
        'sheets': [
            {
                'properties': {
                    'sheetType': 'GRID',
                    'sheetId': SHEET_ID,
                    'title': SHEET_TITLE,
                    'gridProperties': {
                        'rowCount': ROW_COUNT,
                        'columnCount': COLUMN_COUNT,
                    },
                }
            }
        ],
    }


def get_table_header(now_datetime: str) -> list[list[str]]:
    return [
        [REPORT_TITLE],
        [f'Дата и время формирования: {now_datetime}'],
        ['Название проекта', 'Время сбора (дни)', 'Описание'],
    ]


async def create_spreadsheets(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover('sheets', 'v4')
    now_datetime = datetime.now().strftime(DATETIME_FORMAT)
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=get_spreadsheet_body(now_datetime))
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

    rows = get_table_header(now_datetime)

    for project in projects:
        duration_days = (project.close_date - project.create_date).days
        rows.append(
            [project.name, str(duration_days), project.description or '']
        )

    total_rows = len(rows)
    if total_rows > ROW_COUNT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f'Количество строк ({total_rows})'
                f'превышает лимит таблицы ({ROW_COUNT}).'
            )
        )

    if COLUMN_COUNT < MIN_GOOGLE_COLUMNS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f'Значение COLUMN_COUNT ({COLUMN_COUNT}) должно быть'
                f'не меньше {MIN_GOOGLE_COLUMNS}.'
            )
        )

    update_body = {
        'majorDimension': 'ROWS',
        'values': rows,
    }

    range_r1c1 = f'R1C1:R{total_rows}C{MIN_GOOGLE_COLUMNS}'

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=range_r1c1,
            valueInputOption='USER_ENTERED',
            json=update_body,
        )
    )
