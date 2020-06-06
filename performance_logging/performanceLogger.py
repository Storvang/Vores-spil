import xlsxwriter
import os

frame_times = []
update_times = []
render_times = []


def write_to_file():
    with xlsxwriter.Workbook(os.path.join('performance_logging', 'performance log.xlsx')) as workbook:
        worksheet = workbook.add_worksheet()

        worksheet.write('A1', 'frame times')
        worksheet.write('B1', 'update times')
        worksheet.write('C1', 'render times')

        worksheet.write_column('A2', frame_times)
        worksheet.write_column('B2', update_times)
        worksheet.write_column('C2', render_times)

        chart = workbook.add_chart({'type': 'line'})
        chart.add_series({'name': 'frame time',
                          'values': '=Sheet1!$A$2:$A$' + str(len(frame_times) + 1)})
        chart.add_series({'name': 'update time',
                          'values': '=Sheet1!$B$2:$B$' + str(len(update_times) + 1)})
        chart.add_series({'name': 'render time',
                          'values': '=Sheet1!$C$2:$C$' + str(len(render_times) + 1)})

        worksheet.insert_chart('E2', chart)
