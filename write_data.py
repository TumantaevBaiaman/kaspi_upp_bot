import io
import xlsxwriter


def get_report_file(data):
    workbook = xlsxwriter.Workbook("new_sku_data.xlsx")
    worksheet = workbook.add_worksheet()

    head_style = workbook.add_format(
        {
            'bold': True, 'border': 2, 'align': 'center',
        }
    )

    content_style = workbook.add_format(
        {
            'bold': False, 'border': 2, 'align': 'center',
        }
    )

    columns = [
        'SKU',
        'name',
        'price',
    ]

    worksheet.set_column('A:A', 25)
    worksheet.set_column('B:B', 100)
    worksheet.set_column('C:C', 25)

    for index, value in enumerate(columns):
        worksheet.write(0, index, value, head_style)

    for i, value in enumerate(data, start=1):
        worksheet.write(i, 0, value[0], content_style)
        worksheet.write(i, 1, value[2], content_style)
        worksheet.write(i, 2, float(value[1].replace(",", ".")), content_style)

    workbook.close()