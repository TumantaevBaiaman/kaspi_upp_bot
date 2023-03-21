import asyncio
import time

import gspread
from oauth2client.service_account import ServiceAccountCredentials as sac
import pandas as pd

from write_data import get_report_file

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials_path = 'test.json'

credentials = sac.from_json_keyfile_name(credentials_path, scope)
client = gspread.authorize(credentials)


async def gsheet2df(spreadsheet_name, sheet_num):

    sheet = client.open(spreadsheet_name).get_worksheet(sheet_num).get_all_records(numericise_ignore=['all'])
    df = pd.DataFrame.from_dict(sheet)
    return sheet


async def add_data_sheets(spreadsheet_name, sheet_num, data):

    sheet = client.open(spreadsheet_name).get_worksheet(sheet_num)
    for i in data:
        new_row = [None, None, str(i["Название товара "]), int(i["Штрихкод"])]
        try:
            sheet.append_row(new_row)
        except:
            pass


async def update_price_by_sku(sheet, all_record, sku, new_price):

    for row_num, record in enumerate(all_record):
        if record['SKU'] == sku:
            try:
                sheet.update_cell(row_num + 2, 4, new_price)
                return
            except:
                return


async def load_data(sheet_name):
    handle = await gsheet2df(sheet_name, 0)
    return handle


async def update_data(sheet, all_record, sku, new_price):
    handle = await update_price_by_sku(sheet, all_record, sku, new_price)
    return handle


async def read_sheets():
    sheet_names = ["Названия Каспи-Umag", "Склад_export_1678877246390"]
    tasks = []
    for sheet_name in sheet_names:
        task = asyncio.create_task(load_data(sheet_name))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results


async def new_data_price(name_excel: list, price_excel: list) -> dict:
    new_data = {}

    sku_name = {i["SKU"]: str(i["Штрихкод"]) for i in name_excel if i["SKU"] != ""}
    price_name = {str(i["Штрихкод"]): i["Закупочная цена"] for i in price_excel}

    for key, value in sku_name.items():
        if value in price_name:
            new_data[key] = [price_name[value], value]
    return new_data


async def add_new_data(name_excel: list, price_excel: list) -> list:
    new_data = []

    data = [i["Штрихкод"] for i in name_excel]

    for i in price_excel:
        if i["Штрихкод"] not in data:
            new_data.append(i)
    await add_data_sheets("Названия Каспи-Umag", 0, new_data)


async def update(data: dict):
    sheet = client.open("ExcelFormatTemplate").get_worksheet(0)
    all_records = sheet.get_all_records()
    sku_data_all = [i['SKU'] for i in all_records]
    tasks = []
    data_excel_new_sku = []
    for key, value in data.items():
        if key in sku_data_all:
            task = asyncio.create_task(update_data(sheet, all_records, key, float(value[0].replace(",", "."))))
            tasks.append(task)
        else:
            data_excel_new_sku.append([key, *value])
    await asyncio.gather(*tasks)

    if data_excel_new_sku == []:
        return False
    else:
        get_report_file(data_excel_new_sku)
        return True
