import os
import mimetypes
import io
import re
from datetime import datetime, date
from itertools import zip_longest
from typing import Union
from time import sleep

import numpy as np
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

from speedtab.enums import MergeType, BorderStyle, HorizontalAlignment, VerticalAlignment, WrapStrategy, ShareRole, \
    ChartType, StackedType, LegendPosition, AxisPosition, BooleanConditionTypes, BorderSides, ClearSpecific
from speedtab.formats import Color, Border, Number, BaseNumberFormat, Text

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.file']
SHIFT_DIM = {
    'startRowIndex': 0,
    'startColumnIndex': 0,
    'endRowIndex': 1,
    'endColumnIndex': 1,
}

BORDER_SIDES_MAP = {
    'T': BorderSides.TOP,
    'B': BorderSides.BOTTOM,
    'L': BorderSides.LEFT,
    'R': BorderSides.RIGHT,
    'H': BorderSides.HORIZONTAL,
    'V': BorderSides.VERTICAL,
    'I': BorderSides.INNER,
    'O': BorderSides.OUTER,
    'A': BorderSides.ALL,
}

TYPE_ORDER = {b: i for b, i in zip(('clear', 'format', 'chart', 'data'), (0, 0, 0, 1))}

DIMENSION = {
    'ROWS': 'ROWS',
    'COLUMNS': 'COLUMNS',
    0: 'ROWS',
    1: 'COLUMNS'
}


def apply(iterable, f):
    if isinstance(iterable, list):
        return [apply(w, f) for w in iterable]
    else:
        return f(iterable)


def col_num_to_string(n, start_from_0=True):
    string = ''
    if not isinstance(n, int):
        return string
    n += int(start_from_0)
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string


def create_token(input_cred, output_token: str = 'token.json'):
    """A convenience function that creates token for accessing Google Sheets API. The token will be generated in the
    current directory.

    :param input_cred: A path to the json file containing Google credentials.
    :param output_token: A name for the token, defaults to 'token.json'.
    """
    flow = InstalledAppFlow.from_client_secrets_file(input_cred, SCOPES)
    creds = flow.run_local_server(port=0)
    with open(output_token, 'w') as token:
        token.write(creds.to_json())


def datetime_to_xls(input_date):
    if isinstance(input_date, datetime):
        return (input_date - datetime(1899, 12, 30)).total_seconds() / 86400
    elif isinstance(input_date, date):
        return (input_date - date(1899, 12, 30)).days
    else:
        return input_date


def depth(l):
    if isinstance(l, (list, tuple)):
        return max(map(depth, l)) + 1
    else:
        return 0


def get_col_num(col):
    n = 0
    for position, character in zip(range(len(col) - 1, -1, -1), col):
        n += 26 ** position * (ord(character) - 64)
    return n - 1


def num_to_string(n):
    if isinstance(n, int):
        return str(n + 1)
    else:
        return ''


def parse_range(input_range):
    if isinstance(input_range, str):
        input_range = input_range.split(':') + [''] if len(input_range.split(':')) == 1 else input_range.split(':')
        cells = sum(tuple(sheet_cell_to_index(x) for x in input_range), ())
    else:
        cells = input_range + (None,) * 4

    if cells[0] is None:
        cells = (0,) + cells[1:]
    return cells


def parse_url(url: str):
    if not isinstance(url, str):
        return url

    if re.search(r"^(?:https://)?(?:docs|drive)\.google\.com/", url):
        return re.search(r'/(?:d|folders)/([^/?]+)(?:\?|/|$)', url)[1]
    else:
        return url
def sheet_cell_to_index(cell):
    letter = re.search(r'[A-Z]+', cell)
    num = re.search(r'[0-9]+', cell)
    return int(num.group()) - 1 if num else num, get_col_num(letter.group()) if letter else letter


class BooleanCondition:
    def __init__(self, condition_type: BooleanConditionTypes, value=None):
        self.type = condition_type
        self.value = value

    def boolean_condition(self):  # TODO: describe this
        """_summary_

        :return: _description_
        """
        if self.type in (BooleanConditionTypes.BLANK, BooleanConditionTypes.NOT_BLANK,
                         BooleanConditionTypes.IS_NOT_EMPTY,
                         BooleanConditionTypes.IS_EMPTY, BooleanConditionTypes.TEXT_IS_URL,
                         BooleanConditionTypes.TEXT_IS_EMAIL, BooleanConditionTypes.DATE_IS_VALID):
            return {
                'condition': {
                    'type': self.type
                }}
        else:
            return {
                'condition': {
                    'type': self.type,
                    'values': [
                        {'userEnteredValue': self.value}
                    ]}}

def execute_task(task, auto_retry_after = None):
    try:
        return task.execute()
    except HttpError as error:
        if auto_retry_after:
            print(f'An error occurred: {error}')
            print(f'Next attempt in {auto_retry_after} seconds')
            sleep(auto_retry_after)
            return task.execute()
        else:
            raise error


class Task:
    def __init__(self, task_type, position, sheetId, task, work_zone):
        self.task_type = task_type
        self.position = position
        self.sheetId = sheetId
        self.task = task
        self.work_zone = work_zone
    def __str__(self):
        return f'''
            type: {self.task_type};
            position: {self.position};
            sheetId: {self.sheetId};
            work_zone: {self.work_zone};
            task: {self.task};
        '''

class SpreadSheet:
    """A representation of a Google Spreadsheet. For a user, methods for this class include sheet manipulation (adding, deleting,
    accessing sheets) as well as exporting a spreadsheet to an external file.
    """

    def __init__(self, spreadsheet_id, token_path, credentials, connect_v4, connect_v3, value_input_option, user):
        self.spreadsheet_id = spreadsheet_id
        self.token_path = token_path
        self.credentials = credentials
        self.connect_v4 = connect_v4
        self.connect_v3 = connect_v3
        self.user = user
        self.auto_retry_after = user.auto_retry_after
        self.value_input_option = value_input_option
        self._get_metadata()
        self._task_queue = []

    def _get_metadata(self):

        self.metadata = execute_task(self.connect_v4.spreadsheets().get(spreadsheetId=self.spreadsheet_id), self.auto_retry_after)

        self.sheets = dict(
            [(properties.get('title'), {
                'max_column': properties.get('gridProperties').get('columnCount'),
                'max_row': properties.get('gridProperties').get('rowCount'),
                'sheetId': properties.get('sheetId'),
                'position': properties.get('index'),
                'charts': [chart.get('chartId') for chart in charts],
                'conditional_formats': len(conditional_formats),
            }) for properties, charts, conditional_formats in
             [(sheet.get('properties'), sheet.get('charts', []), sheet.get('conditionalFormats', [])) for sheet in
              self.metadata.get('sheets')]]
        )

    def _regroup_tasks(self):
        groups = []
        for sheetId in [x.get('sheetId') for x in self.sheets.values()]:
            current_id_tasks = [x for x in self._task_queue if x.sheetId == sheetId]
            clear_ids = [i for i, x in enumerate(current_id_tasks) if x.task_type == 'clear']
            group_ids = sorted(tuple(set([0] + [j for i, j in zip([-2] + clear_ids, clear_ids) if j - i != 1]
                                         + [len(current_id_tasks)])))
            splinted_tasks = [current_id_tasks[i:j] for i, j in zip(group_ids, group_ids[1:])]

            merged_group = []
            shift = []
            for elem in splinted_tasks:
                if not any(d.task_type == 'data' for d in elem):
                    shift += elem
                else:
                    merged_group.append(elem + shift)
                    shift = []
            if shift:
                merged_group.append(shift)

            groups.append(merged_group)

        full_groups = [sorted(sum(x, []), key=lambda x: (TYPE_ORDER[x.task_type], x.position)) for x in
                       zip_longest(*groups, fillvalue=[])]

        curr_size = {}
        new_size = {}
        for sheet in self.sheets.values():
            curr_size[sheet.get('sheetId')] = [sheet.get('max_row'), sheet.get('max_column')]
            new_size[sheet.get('sheetId')] = [sheet.get('max_row'), sheet.get('max_column')]

        for group in full_groups:
            for task in group:
                if task.task_type == 'clear' and 'updateSheetProperties' in task.task.keys():
                    vals = task.task.get('updateSheetProperties').get('properties').get('gridProperties')
                    new_size[task.sheetId] = [vals.get('rowCount'), vals.get('columnCount')]
                elif task.task_type == 'clear' and 'appendDimension' in task.task.keys():
                    vals = task.task.get('appendDimension')
                    if vals.get('dimension') == 'ROWS':
                        new_size[task.sheetId][0] = max(curr_size[task.get('sheetId')][0] + vals.get('length'),
                                                        new_size[task.sheetId][0])
                    if vals.get('dimension') == 'COLUMNS':
                        new_size[task.sheetId][1] = max(curr_size[task.get('sheetId')][1] + vals.get('length'),
                                                        new_size[task.sheetId][1])
                else:
                    new_size[task.sheetId] = [
                        max(new_size[task.sheetId][0],
                            task.work_zone.get('startRowIndex', 0) if task.work_zone.get('startRowIndex',
                                                                                         0) is not None else 0,
                            task.work_zone.get('endRowIndex', 0) if task.work_zone.get('endRowIndex',
                                                                                       0) is not None else 0
                            ),
                        max(new_size[task.sheetId][1],
                            task.work_zone.get('startColumnIndex', 0) if task.work_zone.get('startColumnIndex',
                                                                                            0) is not None else 0,
                            task.work_zone.get('endColumnIndex', 0) if task.work_zone.get('endColumnIndex',
                                                                                          0) is not None else 0
                            )
                    ]

            for key, (rows, columns) in new_size.items():
                if new_size[key] != curr_size[key]:
                    self._set_sheet_size(rows, columns, key, group)

        return [sorted(group, key=lambda x: (TYPE_ORDER[x.task_type], x.position)) for group in full_groups]

    def _set_sheet_size(self, rows: int, columns: int, sheet_id, group):
        group.append(Task('format', -1, sheet_id, {
            'updateSheetProperties': {
                'properties': {
                    'gridProperties': {
                        'rowCount': rows + 1,
                        'columnCount': columns + 1,
                    },
                    'sheetId': sheet_id,
                },
                'fields': 'gridProperties.rowCount, gridProperties.columnCount',
            }}, None))

    def set_title(self, title: str):
        """Changes title of the spreadsheet.

        :param title: A new name of spreadsheet.
        :return: A SpreadSheet object with.
        """

        self._task_queue.append(Task('format', len(self._task_queue), list(self.sheets.values())[0].get('sheetId'), {
            'updateSpreadsheetProperties': {
                'properties': {
                    'title': title
                },
                'fields': 'title'
            }}, {}))
        return self

    def copy_spreadsheet(self, new_title: str = None):
        self.user.copy_spreadsheet(file_id=self.spreadsheet_id, new_title=new_title)

    def delete_file(self):
        self.user.delete_file(file_id=self.spreadsheet_id)

    def move_from_trash(self, trashed: bool = False):
        self.user.move_from_trash(file_id=self.spreadsheet_id, trashed=trashed)

    def move_to_trash(self, trashed: bool = True):
        self.user.move_to_trash(file_id=self.spreadsheet_id, trashed=trashed)

    def rename_file(self, name: str):
        self.user.rename_file(file_id=self.spreadsheet_id, name=name)

    def move_to_folder(self, folder_id: str):
        self.user.move_to_folder(file_id=self.spreadsheet_id, folder_id=folder_id)

    def share_file_with_user(self, user_email: str, role: ShareRole):
        self.user.share_file_with_user(file_id=self.spreadsheet_id, user_email=user_email, role=role)

    def share_with_domain(self, domain: str, role: ShareRole):
        self.user.share_with_domain(file_id=self.spreadsheet_id, domain=domain, role=role)

    def add_sheets(self, sheets: list):
        """Adds sheets to a spreadsheet.

        :param sheets: A list of new sheets' names.
        :return: A SpreadSheet object with new sheets added.
        """
        execute_task(self.connect_v4.spreadsheets().batchUpdate(**{
                'spreadsheetId': self.spreadsheet_id,
                'body': {
                    'requests': [{
                        'addSheet': {
                            'properties': {
                                'title': title,
                                'gridProperties': {
                                    'rowCount': 100,
                                    'columnCount': 26,
                                }}}} for title in sheets]
                }}), self.auto_retry_after)

        self._get_metadata()
        return self

    def delete_sheets(self, sheets):
        """Deletes sheets from a spreadsheet.

        :param sheets: A list with names of the sheets to be deleted.
        :return: A Spreadsheet object.
        """
        for sheet in sheets:
            self._task_queue.append(Task('format', len(self._task_queue), self.sheets.get(sheet).get('sheetId'), {
                'deleteSheet': {
                    'sheetId': self.sheets.get(sheet).get('sheetId')}}, {}))
        return self

    def exec(self):
        batch_update_chart_list = []
        for group in self._regroup_tasks():
            batch_update_data_list = []
            batch_update_list = []
            for task in group:
                if task.task_type == 'data':
                    batch_update_data_list.append(task.task)
                elif task.task_type == 'chart':
                    batch_update_chart_list.append(task.task)
                else:
                    batch_update_list.append(task.task)

            if batch_update_list:
                execute_task(self.connect_v4.spreadsheets().batchUpdate(**{
                    'spreadsheetId': self.spreadsheet_id,
                    'body': {
                        'requests': batch_update_list
                    }}), self.auto_retry_after)

            if batch_update_data_list:
                execute_task(self.connect_v4.spreadsheets().values().batchUpdate(**{
                    'spreadsheetId': self.spreadsheet_id,
                    'body': {
                        'valueInputOption': self.value_input_option,
                        'data': batch_update_data_list,
                    }}), self.auto_retry_after)
        if batch_update_chart_list:
            execute_task(self.connect_v4.spreadsheets().batchUpdate(**{
                'spreadsheetId': self.spreadsheet_id,
                'body': {
                    'requests': batch_update_chart_list
                }}), self.auto_retry_after)

    def export_as_csv(self, output: str):
        """Writes a spreadsheet to a csv file.

        :param output: A file's name with .csv extension.
        """
        try:
            request = self.connect_v3.files().export_media(fileId=self.spreadsheet_id, mimeType='text/csv')

            fh = io.FileIO(output, mode='w')

            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print('Download %d%%.' % int(status.progress() * 100))

        except HttpError as error:
            print(f'An error occurred: {error}')
    def export_as_excel(self, output: str):
        """Writes a spreadsheet to an Excel file.

        :param output: A file's name with a particular Excel extension (e.g. "MyTable.xlsx")
        """
        try:
            request = self.connect_v3.files().export_media(fileId=self.spreadsheet_id,
                                                           mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

            fh = io.FileIO(output, mode='w')

            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print('Download %d%%.' % int(status.progress() * 100))

        except HttpError as error:
            print(f'An error occurred: {error}')

    def export_as_pdf(self, output: str):
        """Writes a spreadsheet to a pdf file.

        :param output: A file's name with .pdf extension.
        """
        try:
            request = self.connect_v3.files().export_media(fileId=self.spreadsheet_id, mimeType='application/pdf')

            fh = io.FileIO(output, mode='w')

            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print('Download %d%%.' % int(status.progress() * 100))

        except HttpError as error:
            print(f'An error occurred: {error}')

    def export_as_zip(self, output: str):
        """Writes a spreadsheet to a zipped file.

        :param output: A file's name with .zip extension.
        """
        try:
            request = self.connect_v3.files().export_media(fileId=self.spreadsheet_id, mimeType='application/zip')

            fh = io.FileIO(output, mode='w')

            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print('Download %d%%.' % int(status.progress() * 100))

        except HttpError as error:
            print(f'An error occurred: {error}')

    def sheet(self, sheet_name: str):
        """Accesses a sheet in a given spreadsheet by name.

        :param sheet_name: Sheet's name
        :return: A Sheet object.
        """
        return Sheet(sheet_name, self.sheets.get(sheet_name).get('sheetId'), self._task_queue, self.sheets, self)

    def sheets_list(self):
        """Returns a list of the existing sheets in a spreadsheet.

        :return: A list with sheets' names.
        """
        return list(self.sheets.keys())



class Range:
    """A representation of a selected range in a Sheet. This class contains numerous methods for interaction with a sheet
    from formatting cells and inputting values to adding charts and changing cells' sizes.
    """

    def __init__(self, sheet_id, _task_queue, work_zone, start_data_cell, base, data_cell):
        self.sheet_id = sheet_id
        self._task_queue = _task_queue
        self.work_zone = work_zone
        self.start_data_cell = start_data_cell
        self.base = base
        self.auto_retry_after = base.auto_retry_after
        self.data_cell = data_cell

    def _increment_task(self):
        return len(self._task_queue)

    def add_chart(self,
                  columns,
                  target_axis: Union[AxisPosition, list] = AxisPosition.LEFT_AXIS,
                  index_column: int = 0,
                  chart_type: ChartType = ChartType.LINE,
                  stacked_type: StackedType = StackedType.NONE,
                  title: str = None,
                  legend_position: LegendPosition = LegendPosition.BOTTOM_LEGEND,
                  x_axis_name: str = None,
                  y_left_axis_name: str = None,
                  y_right_axis_name: str = None,
                  y_left_axis_min: float = None,
                  y_right_axis_min: float = None,
                  y_left_axis_max: float = None,
                  y_right_axis_max: float = None,
                  x_scale: int = 1,
                  y_scale: int = 1,
                  offset_x_pixels: int = 0,
                  offset_y_pixels: int = 0,
                  header_count: int = 1,
                  nrows: int = None,
                  reverse_axis_order: bool = False,
                  data_sheet_name: str = None,
                  data_start: Union[tuple, str] = (0, 0),
                  ):
        """Adds chart to a sheet.

        :param columns: A column from which the data for the chart will be taken. Requires an index from data_start param.
        E.g. columns=[1] would mean to select the second column from a given dataset.
        :param target_axis: Defines axis (left only, right only or mixed if you input list), defaults to AxisPosition.LEFT_AXIS.
        :param index_column: Defines from where in the selected dataset the index will be taken for the chart, defaults to 0.
        :param chart_type: A type of chart to use (for combo charts see .add_combo_chart() method).
        A list of available options can be found in the ChartType object, defaults to ChartType.LINE (basic line chart).
        :param stacked_type: Whether to create a stacked chart. A list of available options can be found
        in the StackedType object, defaults to StackedType.NONE.
        :param title: Chart's title, defaults to None.
        :param legend_position: Where to place the legend. A list of available options can be found
        in the LegendPosition object, defaults to LegendPosition.BOTTOM_LEGEND.
        :param x_axis_name: x-axis title, defaults to None.
        :param y_left_axis_name: Left y-axis title, defaults to None.
        :param y_right_axis_name: Right y-axis title, defaults to None.
        :param y_left_axis_min: Sets a minimum value on the y-axis situated on the left, defaults to None.
        :param y_right_axis_min: Sets a minimum value on the y-axis situated on the right, defaults to None.
        :param y_left_axis_max: Sets a maximum value on the y-axis situated on the left, defaults to None.
        :param y_right_axis_max: Sets a maximum value on the y-axis situated on the right, defaults to None.
        :param x_scale: Defines chart size on the x scale, defaults to 1.
        :param y_scale: Defines chart size on the y scale, defaults to 1.
        :param offset_x_pixels: Shifts chart position on the cell from default upper left position upwards or downwards in pixels, defaults to 0.
        :param offset_y_pixels: Shifts chart position on the cell from default upper left position to the left or right in pixels, defaults to 0.
        :param header_count: _description_, defaults to 1. #TODO: describe this
        :param nrows: Sets top n rows to take data from, defaults to None.
        :param reverse_axis_order: Defines x axis order.
        :param data_sheet_name: The name of the sheet from where to take data for the chart, defaults to None.
        :param data_start: A starting position for data that is taken for a chart, defaults to (0, 0).
        :raises ValueError: In case if you want to set mixed axis make sure that amount of columns same as amount of axis.
        :return: A SpreadSheet object.
        """

        data_start_cell = parse_range(data_start)
        target_axis = [target_axis] if not isinstance(target_axis, (list, tuple)) else target_axis

        if len(target_axis) == 1:
            pass
        elif 1 < len(target_axis) != len(columns):
            raise ValueError('Amount of target_axis must be one or equal to the amount of columns in a chart')

        series = [{
            'series': {
                'sourceRange': {
                    'sources': [
                        {
                            'sheetId': self.sheet_id if not data_sheet_name else self.base.sheets.get(
                                data_sheet_name).get('sheetId'),
                            'startRowIndex': data_start_cell[0],
                            'endRowIndex': data_start_cell[0] + nrows + 1 if nrows is not None else None,
                            'startColumnIndex': data_start_cell[1] + column,
                            'endColumnIndex': data_start_cell[1] + column + 1,
                        }
                    ]
                }
            },
            'targetAxis': axis
        } for column, axis in zip_longest(columns, target_axis, fillvalue=target_axis[0])]

        self._task_queue.append(Task('chart', self._increment_task(), self.sheet_id, {
            'addChart': {
                'chart': {
                    'spec': {
                        'title': title,
                        'basicChart': {
                            'chartType': chart_type,
                            'stackedType': stacked_type,
                            'legendPosition': legend_position,
                            'axis': [
                                {
                                    'position': 'BOTTOM_AXIS',
                                    'title': x_axis_name,
                                },
                                {
                                    'position': AxisPosition.LEFT_AXIS,
                                    'title': y_left_axis_name,
                                    'viewWindowOptions': {
                                        'viewWindowMode': 'EXPLICIT',
                                        'viewWindowMin': y_left_axis_min,
                                        'viewWindowMax': y_left_axis_max,
                                    },
                                },
                                {
                                    'position': AxisPosition.RIGHT_AXIS,
                                    'title': y_right_axis_name,
                                    'viewWindowOptions': {
                                        'viewWindowMode': 'EXPLICIT',
                                        'viewWindowMin': y_right_axis_min,
                                        'viewWindowMax': y_right_axis_max,
                                    },
                                },
                            ],
                            'domains': [
                                {
                                    'domain': {
                                        'sourceRange': {
                                            'sources': [
                                                {
                                                    'sheetId': self.sheet_id if not data_sheet_name else self.base.sheets.get(
                                                        data_sheet_name).get('sheetId'),
                                                    'startRowIndex': data_start_cell[0],
                                                    'endRowIndex': data_start_cell[
                                                                       0] + nrows + 1 if nrows is not None else None,
                                                    'startColumnIndex': data_start_cell[1] + index_column,
                                                    'endColumnIndex': data_start_cell[1] + index_column + 1,
                                                }
                                            ]
                                        }
                                    },
                                    'reversed': reverse_axis_order,
                                }
                            ],
                            'series': [*series],
                            'headerCount': header_count,
                        }
                    },
                    'position': {
                        'overlayPosition': {
                            'anchorCell': {
                                'sheetId': self.sheet_id,
                                'rowIndex': self.work_zone.get('startRowIndex'),
                                'columnIndex': self.work_zone.get('startColumnIndex'),
                            },
                            'offsetXPixels': offset_x_pixels,
                            'offsetYPixels': offset_y_pixels,
                            'widthPixels': 800 * x_scale,
                            'heightPixels': 400 * y_scale,
                        }
                    }}}}, self.work_zone))

        return self

    def add_combo_chart(self,
                        left_columns,
                        right_columns,
                        chart_type_left: ChartType = ChartType.COLUMN,
                        chart_type_right: ChartType = ChartType.LINE,
                        index_column: int = 0,
                        stacked_type: StackedType = StackedType.NONE,
                        title: str = None,
                        legend_position: LegendPosition = LegendPosition.BOTTOM_LEGEND,
                        x_axis_name: str = None,
                        y_axis_name_left: str = None,
                        y_axis_name_right: str = None,
                        y_axis_fmt_left: str = None,
                        y_axis_fmt_right: str = None,
                        y_axis_min_left: float = None,
                        y_axis_min_right: float = None,
                        y_axis_max_left: float = None,
                        y_axis_max_right: float = None,
                        x_scale: int = 1,
                        y_scale: int = 1,
                        offset_x_pixels: int = 0,
                        offset_y_pixels: int = 0,
                        header_count: int = 1,
                        nrows: int = None,
                        reverse_axis_order: bool = False,
                        data_sheet_name: str = None,
                        data_start: Union[tuple, str] = (0, 0),
                        ):
        """Adds combo chart.

        :param left_columns: A column from which the data for the left y-axis will be taken. Requires an index from data_start param.
        E.g. columns=[1] would mean to select the second column from a given dataset for the left y-axis.
        :param right_columns: A column from which the data for the right y-axis will be taken. Requires an index from data_start param.
        E.g. columns=[1] would mean selecting the second column from a given dataset for the right x-axis.
        :param chart_type_left: A type of chart to use on the left axis, defaults to ChartType.COLUMN.
        :param chart_type_right: A type of chart to use on the right axis, defaults to ChartType.LINE.
        :param index_column: Defines from where in the selected dataset the index will be taken for the chart, defaults to 0.
        :param stacked_type: Whether to create a stacked chart. A list of available options can be found
        in the StackedType object, defaults to StackedType.NONE.
        :param title: Chart's title, defaults to None.
        :param legend_position: Where to place the legend. A list of available options can be found
        in the LegendPosition object, defaults to LegendPosition.BOTTOM_LEGEND.
        :param x_axis_name: x-axis title, defaults to None.
        :param y_axis_name_left: Left y-axis title, defaults to None.
        :param y_axis_name_right: Right y-axis title, defaults to None.
        :param y_axis_fmt_left: a string with Google custom number formatting (e.g. '#,##0.00' for 1,234.56) for the left axis, defaults to None.
        :param y_axis_fmt_right: a string with Google custom number formatting (e.g. '#,##0.00' for 1,234.56) for the right axis, defaults to None.
        :param y_axis_min_left: Sets a minimum value on the y-axis situated on the left, defaults to None.
        :param y_axis_min_right: Sets a minimum value on the y-axis situated on the right, defaults to None.
        :param y_axis_max_left: Sets a maximum value on the y-axis situated on the left, defaults to None.
        :param y_axis_max_right: Sets a maximum value on the y-axis situated on the right, defaults to None.
        :param x_scale: Defines chart size on the x scale, defaults to 1.
        :param y_scale: Defines chart size on the y scale, defaults to 1.
        :param offset_x_pixels: Shifts chart position on the cell from default upper left position upwards or downwards in pixels, defaults to 0
        :param offset_y_pixels: Shifts chart position on the cell from default upper left position to the left or right in pixels, defaults to 0
        :param header_count: _description_, defaults to 1. #TODO: explain this param
        :param nrows: Sets top n rows to take data from, defaults to None.
        :param reverse_axis_order: Defines x axis order.
        :param data_sheet_name: The name of the sheet from where to take data for the chart, defaults to None.
        :param data_start: A starting position for data that is taken for a chart, defaults to (0, 0).
        :return: A SpreadSheet object.
        """

        data_start_cell = parse_range(data_start)
        series = [{
            'series': {
                'sourceRange': {
                    'sources': [
                        {
                            'sheetId': self.sheet_id if not data_sheet_name else self.base.sheets.get(
                                data_sheet_name).get('sheetId'),
                            'startRowIndex': data_start_cell[0],
                            'endRowIndex': data_start_cell[0] + nrows + 1 if nrows is not None else None,
                            'startColumnIndex': data_start_cell[1] + column,
                            'endColumnIndex': data_start_cell[1] + column + 1,
                        }
                    ]
                }
            },
            'targetAxis': 'LEFT_AXIS',
            'type': chart_type_left,
        } for column in left_columns] + [{
            'series': {
                'sourceRange': {
                    'sources': [
                        {
                            'sheetId': self.sheet_id if not data_sheet_name else self.base.sheets.get(
                                data_sheet_name).get('sheetId'),
                            'startRowIndex': data_start_cell[0],
                            'endRowIndex': data_start_cell[0] + nrows + 1 if nrows is not None else None,
                            'startColumnIndex': data_start_cell[1] + column,
                            'endColumnIndex': data_start_cell[1] + column + 1,
                        }
                    ]
                }
            },
            'targetAxis': 'RIGHT_AXIS',
            'type': chart_type_right,
        } for column in right_columns]

        self._task_queue.append(Task('chart', self._increment_task(), self.sheet_id, {
            'addChart': {
                'chart': {
                    'spec': {
                        'title': title,
                        'basicChart': {
                            'chartType': 'COMBO',
                            'stackedType': stacked_type,
                            'legendPosition': legend_position,
                            'axis': [
                                {
                                    'position': 'BOTTOM_AXIS',
                                    'title': x_axis_name,
                                },
                                {
                                    'position': 'LEFT_AXIS',
                                    'title': y_axis_name_left,
                                    'format': y_axis_fmt_left,
                                    'viewWindowOptions': {
                                        'viewWindowMin': y_axis_min_left,
                                        'viewWindowMax': y_axis_max_left,
                                    },
                                },
                                {
                                    'position': 'RIGHT_AXIS',
                                    'title': y_axis_name_right,
                                    'format': y_axis_fmt_right,
                                    'viewWindowOptions': {
                                        'viewWindowMin': y_axis_min_right,
                                        'viewWindowMax': y_axis_max_right,
                                    },
                                },
                            ],
                            'domains': [
                                {
                                    'domain': {
                                        'sourceRange': {
                                            'sources': [
                                                {
                                                    'sheetId': self.sheet_id if not data_sheet_name else self.base.sheets.get(
                                                        data_sheet_name).get('sheetId'),
                                                    'startRowIndex': data_start_cell[0],
                                                    'endRowIndex': data_start_cell[
                                                                       0] + nrows + 1 if nrows is not None else None,
                                                    'startColumnIndex': data_start_cell[1] + index_column,
                                                    'endColumnIndex': data_start_cell[1] + index_column + 1,
                                                }
                                            ]
                                        }
                                    },
                                    'reversed': reverse_axis_order,
                                }
                            ],
                            'series': [*series],
                            'headerCount': header_count,
                        }
                    },
                    'position': {
                        'overlayPosition': {
                            'anchorCell': {
                                'sheetId': self.sheet_id,
                                'rowIndex': self.work_zone.get('startRowIndex'),
                                'columnIndex': self.work_zone.get('startColumnIndex'),
                            },
                            'offsetXPixels': offset_x_pixels,
                            'offsetYPixels': offset_y_pixels,
                            'widthPixels': 800 * x_scale,
                            'heightPixels': 400 * y_scale,
                        }
                    }}}}, self.work_zone))
        return self

    def auto_size(self, axis: Union[str, int] = 1):
        """Autosizes rows (axis=0) or columns (axis=1) in a selected range or sheet.

        WARNING! This method may work incorrectly. The source of the error in its behavior is yet to be established.
        In case it does not autosize, please, resort to a .set_size() method to set a specific size of the cells.
        Otherwise, use .reset_size() to restore default sizes.

        :param axis: An axis to autosize, defaults to 1 (column).
        :return: A SpreadSheet object.
        """
        axis = axis.upper() if isinstance(axis, str) else DIMENSION.get(axis)
        self._task_queue.append(Task('chart', self._increment_task(), self.sheet_id, {
            'autoResizeDimensions': {
                'dimensions': {
                    'sheetId': self.sheet_id,
                    'dimension': axis,
                    'startIndex': self.work_zone.get('startRowIndex') if axis == 'ROWS' else self.work_zone.get(
                        'startColumnIndex'),
                    'endIndex': self.work_zone.get('endRowIndex') if axis == 'ROWS' else self.work_zone.get(
                        'endColumnIndex')
                }}}, self.work_zone))
        return self

    def clear(self,
              values: bool = True,
              all_formats: bool = True,
              specific: Union[str, list] = ClearSpecific.NONE,
              ):
        """Clears all the values and formatting on a given range (but leaves merged cells and charts).

        :param values: Whether to clear the values, defaults to True.
        :param all_formats: Whether to clear formatting, defaults to True.
        :param specific: Whether to clear specific items in the spreadsheet. For an exhaustive list of possible options,
        check out ClearSpecific class.
        :return: A Sheet object.
        """
        if specific is None:
            field = []
        elif isinstance(specific, str):
            field = [specific]
        else:
            field = specific

        if all_formats:
            field.append('userEnteredFormat')
        if values:
            field.append('userEnteredValue')

        if field:
            self._task_queue.append(Task('clear', self._increment_task(), self.sheet_id, {
                'updateCells': {
                    'range': self.work_zone,
                    'fields': ', '.join(field),
                }}, self.work_zone))

        return self

    def delete_axis(self, axis: Union[str, int] = 1): #TODO: Need to test
        """When applied to a range ('A1:B5'), deleted all rows and columns regardless of the axis parameter.
        When applied to a row range ('5:5'), deletes the whole row.
        When applied to a cell with a row axis ('B1', axis=0), returns HTTPError.
        When applied to a column range ('B:B'), deletes the whole column.
        When applied to a cell with column axis ('B1', axis=1), 'cuts out' all the columns of the sheet
        up to the one before the column in a selected range (in the case of 'B1', it will leave only A column available).
        To extend the sheet after the latter deletion, use .extend_sheet() method.

        :param axis: Which axis to delete, defaults to 1.
        :return: A SpreadSheet object.
        """
        axis = axis.upper() if isinstance(axis, str) else DIMENSION.get(axis)
        self._task_queue.append(Task('clear', self._increment_task(), self.sheet_id, {
            'deleteDimension': {
                'range': {
                    'sheetId': self.sheet_id,
                    'dimension': axis,
                    'startIndex': self.work_zone.get('startRowIndex') if axis == 'ROWS' else self.work_zone.get(
                        'startColumnIndex'),
                    'endIndex': self.work_zone.get('endRowIndex') if axis == 'ROWS' else self.work_zone.get(
                        'endColumnIndex')
                }}}, self.work_zone))

        return self

    def extend_sheet(self, rows: int = None, cols: int = None):
        """Extends a sheet across rows/columns.

        :param rows: The number of rows to add, defaults to None.
        :param cols: The number of columns to add, defaults to None.
        :return: A SpreadSheet object.
        """
        if cols:
            self._task_queue.append(Task('format', self._increment_task(), self.sheet_id, {
                'appendDimension': {
                    'sheetId': self.sheet_id,
                    'dimension': 'COLUMNS',
                    'length': cols,
                }}, self.work_zone))
        if rows:
            self._task_queue.append(Task('format', self._increment_task(), self.sheet_id, {
                'appendDimension': {
                    'sheetId': self.sheet_id,
                    'dimension': 'ROWS',
                    'length': rows,
                }}, self.work_zone))

        return self

    def hide_axis(self, axis: Union[str, int] = 1, hide: bool = True):  # TODO: catch the bug (see warning)
        """Hide rows or columns from the selected range.

        WARNING! This method may work incorrectly. The source of the error in its behaviour is yet to be established.
        In case it does not hide axes, please, unhide them manually. If the unhide button is unavailable, run the method
        with the hide parameter set to True.

        :param axis: Which axis to hide, defaults to 1.
        :param hide: Whether to hide sheet, defaults to True.

        :return: A SpreadSheet object.
        """
        axis = axis.upper() if isinstance(axis, str) else DIMENSION.get(axis)

        self._task_queue.append(Task('format', self._increment_task(), self.sheet_id, {
            'updateDimensionProperties': {
                'range': {
                    'sheetId': self.sheet_id,
                    'dimension': axis,
                    'startIndex': self.work_zone.get('startRowIndex') if axis == 'ROWS' else self.work_zone.get(
                        'startColumnIndex'),
                    'endIndex': self.work_zone.get('endRowIndex') if axis == 'ROWS' else self.work_zone.get(
                        'endColumnIndex')
                },
                'properties': {
                    'hiddenByUser': hide,
                },
                'fields': 'hiddenByUser',
            }}, self.work_zone))

        return self

    def hide_grid_lines(self, hide_grid=True):
        """Hides grid lines on a sheet.

        :param hide_grid: Whether to hide grid lines, defaults to True
        :return: A SpreadSheet object.
        """
        self._task_queue.append(Task('format', self._increment_task(), self.sheet_id, {
            'updateSheetProperties': {
                'properties': {
                    'sheetId': self.sheet_id,
                    'gridProperties': {
                        'hideGridlines': hide_grid,
                    },
                },
                'fields': 'gridProperties.hideGridlines',
            }
        }, self.work_zone))
        return self

    def hide_sheet(self, hide=True):
        """Hides sheets.

        :param hide: Whether to hide sheet, defaults to True.
        :return: A Sheet object.
        """
        self._task_queue.append(Task('format', self._increment_task(), self.sheet_id, {
            'updateSheetProperties': {
                'properties': {
                    'sheetId': self.sheet_id,
                    'hidden': hide
                },
                'fields': 'hidden'
            }}, self.work_zone))
        return self

    def insert_empty(self, axis: Union[str, int] = 0,
                     inherit_from_before: bool = True):  # TODO: describe inherit_from_before param.
        """Adds rows and columns to the selected range.

        :param axis: Which axis to insert, defaults to 0.
        :param inherit_from_before: Inherit selected columns, defaults to True.
        :return: A Spreadsheet object.
        """
        axis = axis.upper() if isinstance(axis, str) else DIMENSION.get(axis)
        self._task_queue.append(Task('clear', self._increment_task(), self.sheet_id, {
            'insertDimension': {
                'range': {
                    'sheetId': self.sheet_id,
                    'dimension': axis,
                    'startIndex': self.work_zone.get('startRowIndex') if axis == 'ROWS' else self.work_zone.get(
                        'startColumnIndex'),
                    'endIndex': self.work_zone.get('endRowIndex') if axis == 'ROWS' else self.work_zone.get(
                        'endColumnIndex')
                }, 'inheritFromBefore': inherit_from_before
            }}, self.work_zone))

        return self

    def merge_cells(self, merge_type: MergeType = MergeType.MERGE_ALL):
        """Merges selected cells.

        :param merge_type: Whether to merge rows or columns or both. Can be specified in MergeType class, defaults to MergeType.MERGE_ALL.
        :return: A Spreadsheet object.
        """
        self._task_queue.append(Task('format', self._increment_task(), self.sheet_id, {
            'mergeCells': {
                'mergeType': merge_type,
                'range': self.work_zone
            }}, self.work_zone))
        return self

    def put_copied_cells(self, copied_data):
        """Copies data into the current cells.

        :param copied_data: Use method read_cell_details to collect data.
        :return: a SpreadSheet object.
        """

        self._task_queue.append(Task('format', self._increment_task(), self.sheet_id, {
            'updateCells': {
                'range': {
                    'sheetId': self.sheet_id,
                    'startRowIndex': self.work_zone.get('startRowIndex'),
                    'endRowIndex': self.work_zone.get('endRowIndex'),
                    'startColumnIndex': self.work_zone.get('startColumnIndex'),
                    'endColumnIndex': self.work_zone.get('endColumnIndex')
                },
                'fields': 'userEnteredFormat, userEnteredValue',
                'rows': copied_data
            }}, self.work_zone))
        return self

    def read_cell_details(self):
        """Copies all details about the cell to copy it with .put_copied_cells() method.

        :return: A list of dictionaries with cells' parameters.
        """
        return execute_task((self.base.connect_v4.spreadsheets()
                .get(spreadsheetId=self.base.spreadsheet_id,
                     ranges=[self.data_cell],
                     includeGridData=True
                     )), self.auto_retry_after)['sheets'][0]['data'][0].get('rowData', [])


    def read_dataframe(self, header_lines: int = 1):
        """Takes a cell range as an input, reads cell values and turns them in a pandas DataFrame.

        :param header_lines: A range must have a header. The method supports multi-index header rows (not columns!), defaults to 0.
        :return: A pandas DataFrame object.
        """
        rows = self.read_values()
        if header_lines is None or header_lines == 0:
            return pd.DataFrame(data=rows, columns=None)
        elif header_lines == 1:
            return pd.DataFrame(data=rows[header_lines:], columns=rows[0])
        else:
            return pd.DataFrame(data=rows[header_lines:], columns=rows[0:header_lines])

    def read_values(self, formated_values: bool = True):
        """Takes a cell range as an input, and returns a list of lists (per row in the selected range).
        By default, inner lists will contain values in a string format as it preserves the formatting. For instance,
        if the column number is in the dollar format, it will return "$49.09" instead of a float 49.09. To get the
        actual values set formatted_values to False.

        :param formated_values: Whether to save the formatting as in the column, defaults to True.
        :return: A list of lists containing the values from the sheet.
        """
        return execute_task((self.base.connect_v4.spreadsheets().values()
                .get(spreadsheetId=self.base.spreadsheet_id,
                     range=self.data_cell,
                     valueRenderOption='FORMATTED_VALUE' if formated_values else 'UNFORMATTED_VALUE')),
                            self.auto_retry_after).get('values', [])

    def reset_size(self):
        """Resets the size of a cell.

        :return: A Spreadsheet object.
        """
        return self.set_size(axis=1, size=100).set_size(axis=0, size=21)

    def set_background_color(self, color: Color = Color((255, 255, 255)), condition: BooleanCondition = None):
        """Sets cell's background color.

        :param color: Background color in Color format.
        :param condition: Whether to use conditional formatting, defaults to None.
        """

        if condition:
            self._task_queue.append(Task('format', self._increment_task(), self.sheet_id, {
                'addConditionalFormatRule': {
                    'rule': {
                        'ranges': [self.work_zone],
                        'booleanRule': {
                            **condition.boolean_condition(),
                            'format': {
                                'backgroundColor': color.color
                            },
                        }
                    },
                    'index': 0
                }}, self.work_zone))
        else:
            self._task_queue.append(Task('format', self._increment_task(), self.sheet_id, {
                'repeatCell': {
                    'range': self.work_zone,
                    'cell': {
                        'userEnteredFormat': {
                            'backgroundColor': color.color
                        }},
                    'fields': 'userEnteredFormat(backgroundColor)',
                }}, self.work_zone))

        return self

    def set_borders(self,
                    border_style: BorderStyle = BorderStyle.SOLID,
                    border_width: int = 1,
                    color: Color = Color((0, 0, 0)),
                    border_sides: Union[list, str] = BorderSides.ALL,
                    ):
        """Sets cell's borders.

        :param border_style: Border style to use (see BorderStyle class for available options), defaults to BorderStyle.SOLID.
        :param border_width: Choose the width of the border, defaults to 1.
        :param color: Set the color of the borders, defaults to Color((0, 0, 0)).
        :param border_sides: Which border sides to show (see BorderSides class for available options), defaults to BorderSides.ALL_BORDERS.
        :return: A Sheet object.
        """
        if isinstance(border_sides, str):
            border_sides = [BORDER_SIDES_MAP.get(x) for x in border_sides.upper() if x in BORDER_SIDES_MAP.keys()]
        if depth(border_sides) == 2:
            border_sides = set(sum(border_sides, ()))
        elif depth(border_sides) == 1:
            border_sides = set(border_sides)

        self._task_queue.append(Task('format', self._increment_task(), self.sheet_id, {
            'updateBorders': {
                'range': self.work_zone,
                **dict((x, Border(border_style, border_width, color).__dict__) for x in border_sides),
            }}, self.work_zone))
        return self

    def set_freeze_cell(self):
        """Sets a lower right point of a cell to be a freezing point.

        :return: A SpreadSheet object with a freezed view.
        """
        self._task_queue.append(Task('format', self._increment_task(), self.sheet_id, {
            'updateSheetProperties': {
                'properties': {
                    'gridProperties': {
                        'frozenRowCount': self.work_zone.get('startRowIndex'),
                        'frozenColumnCount': self.work_zone.get('startColumnIndex')},
                    'sheetId': self.sheet_id
                },
                'fields': 'gridProperties.frozenRowCount, gridProperties.frozenColumnCount'
            }
        }, self.work_zone))
        return self

    def set_num_format(self, default_format: BaseNumberFormat = Number):
        """Sets cells' number formatting.

        :param default_format: one of the available number formats provided in the ReadyFormats class, defaults to Number.
        :return: A Spreadsheet object.
        """
        if isinstance(default_format, Text):
            task_type = 'clear'
        else:
            task_type = 'format'
        self._task_queue.append(Task(task_type, self._increment_task(), self.sheet_id, {
            'repeatCell': {
                'range': self.work_zone,
                **default_format.__dict__,
            }}, self.work_zone))
        return self

    def set_sheet_size(self, rows: int, columns: int):
        """Sets sheet size.

        :param rows: a number of rows in a sheet.
        :param columns: a number of columns in a sheet.
        :return: A SpreadSheet object.
        """
        self._task_queue.append(Task('clear', self._increment_task(), self.sheet_id, {
            'updateSheetProperties': {
                'properties': {
                    'gridProperties': {
                        'rowCount': rows,
                        'columnCount': columns,
                    },
                    'sheetId': self.sheet_id,
                },
                'fields': 'gridProperties.rowCount, gridProperties.columnCount',
            }}, self.work_zone))

        return self

    def set_size(self, size: int = None, axis: Union[str, int] = 1):
        """Sets cell's size. In Google Sheets, the default cell width is 100 pixels, and the default cell height is 21 pixels.

        :param size: size of a selected axis in pixels, defaults to None.
        :param axis: an axis to change, 0 — for a row, 1 — for a column, defaults to 1.
        :return: A SpreadSheet object.
        """
        axis = axis.upper() if isinstance(axis, str) else DIMENSION.get(axis)
        self._task_queue.append(Task('format', self._increment_task(), self.sheet_id, {
            'updateDimensionProperties': {
                'range': {
                    'sheetId': self.sheet_id,
                    'dimension': axis,
                    'startIndex': self.work_zone.get('startRowIndex') if axis == 'ROWS' else self.work_zone.get(
                        'startColumnIndex'),
                    'endIndex': self.work_zone.get('endRowIndex') if axis == 'ROWS' else self.work_zone.get(
                        'endColumnIndex'),
                },
                'properties': {
                    'pixelSize': size,
                },
                'fields': 'pixelSize',
            }}, self.work_zone))
        return self

    def set_text_format(self, horizontal_alignment: HorizontalAlignment = None,
                        vertical_alignment: VerticalAlignment = None,
                        wrap_strategy: WrapStrategy = None,
                        font_size: int = None,
                        bold: bool = None,
                        italic: bool = None,
                        strikethrough: bool = None,
                        underline: bool = None,
                        font: str = None,
                        text_color: Color = None):
        """Sets cells' text formatting.

        :param horizontal_alignment: defines the style of horizontal alignment (see HorizontalAlignment class
        for available options), defaults to None.
        :param vertical_alignment: defines the style of vertical alignment (see VerticalAlignment class
        for available options), defaults to None.
        :param wrap_strategy: defines wrap strategy (see WrapStrategy class for available options), defaults to None.
        :param font_size: sets font size, defaults to None.
        :param bold: whether to make text bold, defaults to None.
        :param italic: whether to make text in italics, defaults to None.
        :param strikethrough: whether to apply strikethrough to the text, defaults to None.
        :param underline: whether to underline the text, defaults to None.
        :param font: font name (e.g. 'Times New Roman'), defaults to None.
        :param text_color: a Color object to paint words, defaults to None.
        :return: A SpreadSheet object.
        """
        list_of_inputs = ', '.join(
            [f'textFormat.{s}' for s, x in
             zip(('fontFamily', 'fontSize', 'bold', 'italic', 'strikethrough', 'underline', 'foregroundColor'),
                 (font, font_size, bold, italic, strikethrough, underline, text_color)) if x is not None]
            + [s for s, x in zip(('horizontalAlignment', 'verticalAlignment', 'wrapStrategy'),
                                 (horizontal_alignment, vertical_alignment, wrap_strategy)) if x is not None])

        self._task_queue.append(Task('format', self._increment_task(), self.sheet_id, {
            'repeatCell': {
                'range': self.work_zone,
                'cell': {
                    'userEnteredFormat': {
                        'horizontalAlignment': horizontal_alignment if horizontal_alignment not in (
                        None, False) else None,
                        'verticalAlignment': vertical_alignment if vertical_alignment not in (None, False) else None,
                        'wrapStrategy': wrap_strategy if wrap_strategy not in (None, False) else None,
                        'textFormat': {
                            'foregroundColor': text_color.color if text_color not in (None, False) else None,
                            'fontFamily': font if font not in (None, False) else None,
                            'fontSize': font_size if font_size not in (None, False) else None,
                            'bold': bold if bold not in (None, False) else None,
                            'italic': italic if italic not in (None, False) else None,
                            'strikethrough': strikethrough if strikethrough not in (None, False) else None,
                            'underline': underline if underline not in (None, False) else None,
                        }}},
                'fields': f'userEnteredFormat({list_of_inputs})',
            }}, self.work_zone))
        return self

    def unhide_grid_lines(self, hide_grid=False):
        """Unhides grid lines on a sheet.

        :param hide_grid: Whether to hide grid lines, defaults to False.
        :return: A Sheet object.
        """
        self.hide_grid_lines(hide_grid)

    def unhide_sheet(self, hide=False):
        """Unhides sheets.

        :param hide: Whether to hide sheet, defaults to False.
        :return: A Sheet object.
        """
        self.hide_sheet(hide)

    def unmerge_cells(self):
        """Unmerges cells.

        :return: A SpreadSheet object.
        """
        self._task_queue.append(Task('format', self._increment_task(), self.sheet_id, {
            'unmergeCells': {
                'range': self.work_zone,
            }}, self.work_zone))
        return self

    def write_dataframe(self, df: pd.DataFrame, header=True, index=True):
        """Inserts pandas DataFrame in a sheet.

        :param df: a DataFrame object.
        :param header: whether to reserve the first row in the sheet to headers, defaults to True.
        :param index: whether to reserve the first column for index, defaults to True.
        :return: A SpreadSheet object.
        """
        df = df.copy()

        for column, column_type in zip(df.dtypes.index, df.dtypes.values):
            if isinstance(column_type, pd.CategoricalDtype):
                df[column] = df[column].cat.add_categories('').fillna('').astype(str)
            elif np.dtype('timedelta64[ns]') == column_type:
                df[column] = df[column].astype(str)

        if index:
            if isinstance(df.index, pd.CategoricalIndex) or any(isinstance(x, pd.Interval) for x in df.index.values):
                df.index = df.index.astype(str)
            try:
                df = df.reset_index(col_level=-1)
            except:
                df = pd.merge(df.index.to_frame(index=False), df.reset_index(drop=True), left_index=True,
                              right_index=True)

        if pd.__version__ >= '2.1.0':
            df = df.map(datetime_to_xls)
        else:
            df = df.applymap(datetime_to_xls)

        df = df.replace([np.inf, -np.inf, np.NaN], None).where(pd.notnull(df), None)

        if header:
            if isinstance(df.columns, pd.MultiIndex):
                values = [[str(elem) for elem in level] for level in
                          list(zip(*df.columns.to_list()))] + df.values.tolist()
            else:
                values = [[str(elem) for elem in df.columns.to_list()]] + df.values.tolist()
        else:
            values = df.values.tolist()

        self._task_queue.append(Task('data', self._increment_task(), self.sheet_id, {
            'range': self.start_data_cell,
            'values': values,
            'majorDimension': 'ROWS',
        }, self.work_zone))
        return self

    def write_formula(self, value):
        self._task_queue.append(Task('format', self._increment_task(), self.sheet_id, {
            'repeatCell': {
                'range': self.work_zone,
                'cell': {
                    'userEnteredValue': {
                        'formulaValue': value
                    }
                },
                'fields': 'userEnteredValue'
            }}, self.work_zone))

        return self

    def write_range(self, values: list, axis: Union[str, int] = 0):
        # TODO: add overwrite param (bool). If false, insert available or didn't insert at all.
        """Inserts values in a selected cell range. The default starting point is 'A1' in a selected sheet. Overwrites previously inserted data.

        :param values: a list of values to insert.
        :param axis: along which axis to insert the values, defaults to 0.
        :return: A SpreadSheet object.
        """
        values = list(values) if not isinstance(values, list) else values
        while depth(values) < 2:
            values = [values]
        values = apply(values, datetime_to_xls)
        self._task_queue.append(Task('data', self._increment_task(), self.sheet_id, {
            'range': self.start_data_cell,
            'values': values,
            'majorDimension': DIMENSION.get(axis.upper() if isinstance(axis, str) else axis),
        }, self.work_zone))

        return self


class Sheet(Range):
    """A representation of Google Spreadsheet's sheet."""

    def __init__(self, sheet_name, sheet_id, task_query, sheets, base, cells=(0, 0, None, None)):
        self.base = base
        self.sheet_name = sheet_name
        self.sheet_id = sheet_id
        self._task_queue = task_query
        self.sheets = sheets
        self.auto_retry_after = base.auto_retry_after
        cells = parse_range(cells)

        self.start_data_cell = f'{sheet_name}!{col_num_to_string(cells[1])}{num_to_string(cells[0])}'
        self.data_cell = self.start_data_cell + f':{col_num_to_string(cells[3])}{num_to_string(cells[2]) if cells[2] is not None else self.sheets.get(self.sheet_name).get("max_row")}'
        self.work_zone = dict([(key, val + SHIFT_DIM.get(key) if val is not None else val)
                               for key, val in zip(SHIFT_DIM.keys(), cells)]
                              + [('sheetId', self.sheet_id)])

        # if cells[2] is not None else self.sheets.get(self.sheet_name).get("max_row"))}'

        super().__init__(self.sheet_id, self._task_queue, self.work_zone, self.start_data_cell, self.base,
                         self.data_cell)

    def cell_range(self, input_range):
        """Selects a cell range for an interaction.

        :param input_range: Either a string with Excel range (e.g. 'A1:B3'), or a tuple in a form
        (row_start, column_start, row_end, column_end). In the latter case 'A1:B3' can be implemented as (0, 0, 2, 1).
        :return: A Sheet object with a selected range.
        """
        return Sheet(self.sheet_name, self.sheet_id, self._task_queue, self.sheets, self.base, input_range)

    def delete_all_charts(self):
        """Deletes all charts from a sheet."""
        for chart_id in self.sheets.get(self.sheet_name).get('charts'):
            self._task_queue.append(Task('format', self._increment_task(), self.sheet_id, {
                'deleteEmbeddedObject': {
                    'objectId': chart_id
                }}, self.work_zone))

        return self

    def delete_all_conditionals(self):
        """Deletes all conditional formatting from a sheet."""
        for i in range(self.sheets.get(self.sheet_name).get('conditional_formats') - 1, -1, -1):
            self._task_queue.append(Task('format', self._increment_task(), self.sheet_id, {
                'deleteConditionalFormatRule': {
                    'sheetId': self.sheet_id,
                    'index': i
                }
            }, self.work_zone))

        return self

    def sheet(self, sheet_name: str):
        """Switches to another sheet within an active spreadsheet.

        :param sheet_name: A name of the sheet to switch to.
        :return: Selected Sheet object.
        """
        return Sheet(sheet_name, self.sheets.get(sheet_name).get('sheetId'), self._task_queue, self.sheets, self.base)


class Client:
    """User accesses the Google Sheets via the Client object that uses the token to connect to Google Sheets.
    This results in the following routine:

    >>> import speedtab as st
    >>> with st.Client('token.json') as user:
            user.*action*
    """

    def __init__(self, token_path='token.json', auto_retry_after=45):
        self.token_path = token_path
        self.credentials = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        self.list_of_spreadsheets = []
        self.connect_v4 = self._connect_v4()
        self.connect_v3 = self._connect_v3()
        self.auto_retry_after = auto_retry_after

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.exec()

    def _connect_v3(self):
        return build('drive', 'v3', credentials=self.credentials)

    def _connect_v4(self):
        return build('sheets', 'v4', credentials=self.credentials)

    def copy_spreadsheet(self,
                         spreadsheet: Union[str, SpreadSheet],
                         new_title: str = None,
                         value_input_option: str = 'USER_ENTERED',
                         ):
        """Creates a copy of an existing spreadsheet given spreadsheet id (extracted from URL or present in
        the Spreadsheet object) and a new title. As for now, the new title is necessary for creating a copy.

        :param spreadsheet: Google spreadsheet's URL, or spreadsheet's id that can be extracted from the URL manually extraction (see below), or a
        spreadsheet object (acquired, for instance, by .create_spreadsheet() or .get_spreadsheet() methods).
        :param new_title: A new title for a copy.
        :param value_input_option: 'RAW' or 'USER_ENTERED'. https://developers.google.com/sheets/api/reference/rest/v4/ValueInputOption
        :return: A SpreadSheet object that is used to access the spreadsheet itself.

        :note: (Optional) Spreadsheet's id can be located in its URL:
        https://docs.google.com/spreadsheets/d/[Spreadsheet's id]/edit#gid=123456789

        E.g. in the following URL:
        https://docs.google.com/spreadsheets/d/ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789abcdefghi/edit#gid=123456798
        The id will be: ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789abcdefghi
        """
        if isinstance(spreadsheet, str):
            spreadsheet = parse_url(spreadsheet)
        elif isinstance(spreadsheet, SpreadSheet):
            spreadsheet = spreadsheet.spreadsheet_id

        copied_id = execute_task(self.connect_v3.files()
                                 .copy(fileId=spreadsheet,
                                       body={'name': new_title},
                                       supportsAllDrives=True),
                                 self.auto_retry_after)['id']

        ss = SpreadSheet(copied_id,
                         token_path=self.token_path,
                         credentials=self.credentials,
                         connect_v4=self.connect_v4,
                         connect_v3=self.connect_v3,
                         value_input_option=value_input_option,
                         user=self
                         )
        self.list_of_spreadsheets.append(ss)
        return ss

    def create_folder(self, folder_name: str, parent_id: str = None):
        """Creates a folder in Google Drive.

        :param folder_name: New folder's name
        :param parent_id: If a folder is within another folder, add its id (see below), defaults to None
        :return: Folder's id

        :note: Folder's id is automatically returned by .create_folder() method, automatically extracted from the folder's URL, or can be input directly (see below).

        (Optional) The folder's id can be located in its URL:
        https://drive.google.com/drive/u/1/folders/[Folder's id]/...

        E.g. in the following URL:
        https://drive.google.com/drive/u/1/folders/ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567
        The id will be: ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567
        """
        if isinstance(parent_id, str):
            parent_id = parse_url(parent_id)

        folder_id = execute_task(self.connect_v3.files().create(body={
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id] if parent_id else None,
        }, supportsAllDrives=True), self.auto_retry_after)['id']

        return folder_id

    def create_spreadsheet(self,
                           title: str,
                           sheets: list = None,
                           hide_grid_lines: Union[list, bool] = False,
                           value_input_option: str = 'USER_ENTERED'
                           ):
        """Creates a Google spreadsheet. Several sheets can be created at once by passing a list with
        sheets' names. None value, in this case, creates a single sheet with a default name (that depends on
        the language of the Google Sheets, e.g. in English it would be "Sheet1").

        :param title: Spreadsheet's (not sheet's!) title.
        :param sheets: A list with sheets' names, defaults to None
        :param hide_grid_lines: A Boolean (or a list of Booleans) that specifies whether to show the gridlines for
        a sheet (or a list of sheets), defaults to False
        :param value_input_option: 'RAW' or 'USER_ENTERED'. https://developers.google.com/sheets/api/reference/rest/v4/ValueInputOption
        :raises NameError: If the length of the list with Booleans is not equal to the length of the list of sheets.
        :return: A SpreadSheet object that is used to access the spreadsheet itself.
        """
        if sheets is None:
            sheets = ['Sheet1']

        if isinstance(hide_grid_lines, bool):
            hide_grid_lines = [hide_grid_lines] * len(sheets)

        if len(hide_grid_lines) != len(sheets):
            raise NameError(
                f'Wrong list lengths. Number of tabs: {len(sheets)}, number of grid options: {len(hide_grid_lines)}')

        spreadsheet_id = execute_task(
            self.connect_v4.spreadsheets()
            .create(fields='spreadsheetId',
                    body={
                        'properties': {'title': title},
                        'sheets': [{'properties': {
                            'title': sheet_name,
                            'gridProperties': {'hideGridlines': grid}}}
                            for sheet_name, grid in zip(sheets, hide_grid_lines)]}), self.auto_retry_after).get('spreadsheetId')

        ss = SpreadSheet(spreadsheet_id,
                         token_path=self.token_path,
                         credentials=self.credentials,
                         connect_v4=self.connect_v4,
                         connect_v3=self.connect_v3,
                         value_input_option=value_input_option,
                         user=self)
        self.list_of_spreadsheets.append(ss)
        return ss

    def delete_file(self, file_id: Union[str, SpreadSheet]):
        """Deletes a file permanently (without moving it to a trash).

        :param file_id: File's id (e.g. id of a folder or a spreadsheet).

        (Optional) The folder's id can be located in its URL:
        https://drive.google.com/drive/u/1/folders/[Folder's id]/...

        E.g. in the following URL:
        https://drive.google.com/drive/u/1/folders/ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567
        The id will be: ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567

        :note: (Optional) Spreadsheet's id can be located in its URL:
        https://docs.google.com/spreadsheets/d/[Spreadsheet's id]/edit#gid=123456789

        E.g. in the following URL:
        https://docs.google.com/spreadsheets/d/ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789abcdefghi/edit#gid=123456798
        The id will be: ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789abcdefghi
        """
        if isinstance(file_id, str):
            file_id = parse_url(file_id)
        elif isinstance(file_id, SpreadSheet):
            file_id = file_id.spreadsheet_id

        execute_task(self.connect_v3.files().delete(fileId=file_id, supportsAllDrives=True), self.auto_retry_after)

    def exec(self):
        for st in self.list_of_spreadsheets:
            try:
                st.exec()
            except HttpError as error:
                print(f'An error occurred: {error}')
                if self.auto_retry_after:
                    print(f'Next attempt in {self.auto_retry_after} seconds')
                    sleep(self.auto_retry_after)
                    st.exec()

    def get_spreadsheet(self,
                        spreadsheet_id: str,
                        value_input_option: str = 'USER_ENTERED'):
        """Returns a SpreadSheet object with a corresponding spreadsheet's id.

        :param spreadsheet_id: Spreadsheet's URL or id.
        :param value_input_option: 'RAW' or 'USER_ENTERED'. https://developers.google.com/sheets/api/reference/rest/v4/ValueInputOption
        :return: a SpreadSheet object.

        :note: (Optional) Spreadsheet's id can be located in its URL:
        https://docs.google.com/spreadsheets/d/[Spreadsheet's id]/edit#gid=123456789

        E.g. in the following URL:
        https://docs.google.com/spreadsheets/d/ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789abcdefghi/edit#gid=123456798
        The id will be: ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789abcdefghi
        """
        ss = SpreadSheet(spreadsheet_id=parse_url(spreadsheet_id),
                         token_path=self.token_path,
                         credentials=self.credentials,
                         connect_v4=self.connect_v4,
                         connect_v3=self.connect_v3,
                         value_input_option=value_input_option,
                         user=self)
        self.list_of_spreadsheets.append(ss)
        return ss

    def upload_file(self, path: str, folder_id: str = None):
        (directory, filename) = os.path.split(path)
        (mime, encoding) = mimetypes.guess_type(path)
        if mime is None:
            mime = 'application/octet-stream'

        media_body = MediaFileUpload(path, mimetype=mime, resumable=True)
        body = {
            'name': filename,
            'parents': [parse_url(folder_id)],
        }

        file = execute_task(self.connect_v3.files().create(body=body,
                                              media_body=media_body,
                                              supportsAllDrives=True,
                                              fields="id"), self.auto_retry_after)

        return file.get('id')


    def move_from_trash(self, file_id: Union[str, SpreadSheet], trashed: bool = False):
        """Moves a file from trash.

        :param file_id: File's id (e.g. id of a folder or a spreadsheet).
        :param trashed: set trashed status to the file.

        (Optional) The folder's id can be located in its URL:
        https://drive.google.com/drive/u/1/folders/[Folder's id]/...

        E.g. in the following URL:
        https://drive.google.com/drive/u/1/folders/ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567
        The id will be: ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567

        :note: (Optional) Spreadsheet's id can be located in its URL:
        https://docs.google.com/spreadsheets/d/[Spreadsheet's id]/edit#gid=123456789

        E.g. in the following URL:
        https://docs.google.com/spreadsheets/d/ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789abcdefghi/edit#gid=123456798
        The id will be: ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789abcdefghi
        """
        self.move_to_trash(file_id, trashed)

    def move_to_folder(self, file_id: Union[str, SpreadSheet], folder_id: str):
        """Moves file to a particular folder.

        :param file_id: File's URL on Google Drive (the file's id will be extracted automatically). Alternatively, file's id can also be inserted directly.
        :param folder_id: Folder's id.
        """
        if isinstance(file_id, str):
            file_id = parse_url(file_id)
        elif isinstance(file_id, SpreadSheet):
            file_id = file_id.spreadsheet_id

        previous_parents = ','.join(
            execute_task(self.connect_v3.files().get(
                fileId=file_id,
                fields='parents',
                supportsAllDrives=True,
            ),
                self.auto_retry_after).get('parents'))
        execute_task(self.connect_v3.files().update(fileId=file_id, addParents=parse_url(folder_id),
                                       supportsAllDrives=True,
                                       removeParents=previous_parents, fields='id, parents'),
                     self.auto_retry_after)

    def move_to_trash(self, file_id: Union[str, SpreadSheet], trashed: bool = True):
        """Moves a file to trash.

        :param file_id: File's id (e.g. id of a folder or a spreadsheet).
        :param trashed: set trashed status to the file.

        (Optional) The folder's id can be located in its URL:
        https://drive.google.com/drive/u/1/folders/[Folder's id]/...

        E.g. in the following URL:
        https://drive.google.com/drive/u/1/folders/ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567
        The id will be: ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567

        :note: (Optional) Spreadsheet's id can be located in its URL:
        https://docs.google.com/spreadsheets/d/[Spreadsheet's id]/edit#gid=123456789

        E.g. in the following URL:
        https://docs.google.com/spreadsheets/d/ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789abcdefghi/edit#gid=123456798
        The id will be: ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789abcdefghi
        """
        if isinstance(file_id, str):
            file_id = parse_url(file_id)
        elif isinstance(file_id, SpreadSheet):
            file_id = file_id.spreadsheet_id

        execute_task(self.connect_v3.files().update(fileId=file_id, body={'trashed': trashed}, supportsAllDrives=True),
                     self.auto_retry_after)

    def rename_file(self, file_id: str, name: str):
        """Renames an existing files in Google Drive.

        :param file_id: Folder's id.
        :param name: A new name for the file.

        (Optional) The folder's id can be located in its URL:
        https://drive.google.com/drive/u/1/folders/[Folder's id]/...

        E.g. in the following URL:
        https://drive.google.com/drive/u/1/folders/ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567
        The id will be: ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567

        :note: (Optional) Spreadsheet's id can be located in its URL:
        https://docs.google.com/spreadsheets/d/[Spreadsheet's id]/edit#gid=123456789

        E.g. in the following URL:
        https://docs.google.com/spreadsheets/d/ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789abcdefghi/edit#gid=123456798
        The id will be: ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789abcdefghi
        """
        if isinstance(file_id, str):
            file_id = parse_url(file_id)
        elif isinstance(file_id, SpreadSheet):
            file_id = file_id.spreadsheet_id

        execute_task(self.connect_v3.files().update(body={
            'name': name,
        }, fileId=file_id, supportsAllDrives=True), self.auto_retry_after)

    def search_folder(self,
                      folder_name,
                      current_folder: str = None,
                      mkdir: bool = False,
                      selected_fields: list = None,
                      ):
        """Looks for a folder with a given name. Can be customised to create one if it does not exist.

        :param folder_name: Folder's name.
        :param current_folder: Folder to search in, defaults to None
        :param mkdir: whether to create a new folder if it does not exist, defaults to False
        :param selected_fields: you may request your own list of fields (structure below), defaults to None
            {'id': '*',                     # file's id
            'name': '*',                    # file's name
            'file_type': '*',               # file's type (spreadsheet/image/folder/etc)
            'created_time': '*',            # creation time
            'modified_time': '*',           # last modification time
            'modified_by_me_time': '*'}     # last modification by the user
        :return: If there exists a folder, returns its id. If the folder does not exist and mkdir = True, works as .create_folder() method.
        If the folder is not found and mkdir = False, returns None.
        """
        if isinstance(current_folder, str):
            current_folder = parse_url(current_folder)

        folders = [file for file in self.select_files(current_folder) if
                   file.get('file_type') == 'folder' and file.get('name') == folder_name]

        if folders and selected_fields:
            return [[folder.get(x) for x in selected_fields] for folder in folders]
        elif folders:
            return [folder.get('id') for folder in folders]
        elif mkdir:
            return [self.create_folder(folder_name, current_folder)]
        else:
            return print(f"A folder called '{folder_name}' does not exist. To create one, set mkdir=True")

    def select_files(self, folder_id: str = None, trashed: bool = False):
        """Selects files in a given folder.

        :param folder_id: Folder's id, defaults to None (selects files from the whole Drive).
        :param trashed: Whether to search in the bin, defaults to False.
        :return: A list of dictionaries with the following structure.
            {'id': '*',                     # file's id
            'name': '*',                    # file's name
            'file_type': '*',               # file's type (spreadsheet/image/folder/etc)
            'created_time': '*',            # creation time
            'modified_time': '*',           # last modification time
            'modified_by_me_time': '*'}     # last modification by the user
        """
        if isinstance(folder_id, str):
            folder_id = parse_url(folder_id)

        files = []
        page_token = None
        while True:
            response = execute_task(self.connect_v3.files().list(q=('trashed = true' if trashed else 'trashed = false') + (
                f' and "{folder_id}" in parents' if folder_id else ''),
                                                    spaces='drive',
                                                    fields='nextPageToken, files(id, name, mimeType, createdTime, modifiedTime, modifiedByMeTime)',
                                                    includeItemsFromAllDrives=True,
                                                    supportsAllDrives=True,
                                                    pageToken=page_token,
                                                    ), self.auto_retry_after)

            files.extend([{
                'id': file.get('id'),
                'name': file.get('name'),
                'file_type': file.get('mimeType').split('.')[-1],
                'created_time': file.get('createdTime'),
                'modified_time': file.get('modifiedTime'),
                'modified_by_me_time': file.get('modifiedByMeTime'),
            } for file in response.get('files', [])])
            page_token = response.get('nextPageToken', None)

            if page_token is None:
                break

        return files

    def share_file_with_user(self, file_id: Union[str, SpreadSheet], user_email: str, role: ShareRole):
        """Gives access to a file for a user with a given email.

        :param file_id: File's URL on Google Drive (the file's id will be extracted automatically). Alternatively, the file's id can also be inserted directly.
        :param user_email: User's email.
        :param role: Which level of access new users will have. Available options are 'viewer', 'commenter', and 'editor' (accessed by
        ShareRole.VIEWER, ShareRole.COMMENTER, ShareRole.EDITOR accordingly.
        """

        if isinstance(file_id, str):
            file_id = parse_url(file_id)
        elif isinstance(file_id, SpreadSheet):
            file_id = file_id.spreadsheet_id

        execute_task(self.connect_v3.permissions().create(**{
            'fileId': file_id,
            'body': {
                'type': 'user',
                'role': role,
                'emailAddress': user_email,
            },
            'fields': 'id',
        }), self.auto_retry_after)

    def share_with_domain(self, file_id: Union[str, SpreadSheet], domain: str, role: ShareRole):
        """Gives access to a file for users with a given domain.

        :param file_id: File's URL on Google Drive (the file's id will be extracted automatically). Alternatively, the file's id can also be inserted directly.
        :param domain: Organisation's domain (for instance, in email JohnSmith@coolcompany.com the domain would be 'coolcompany')
        :param role: Which level of access new users will have. Available options are 'viewer', 'commenter', and 'editor' (accessed by
        ShareRole.VIEWER, ShareRole.COMMENTER, ShareRole.EDITOR accordingly).
        """

        if isinstance(file_id, str):
            file_id = parse_url(file_id)
        elif isinstance(file_id, SpreadSheet):
            file_id = file_id.spreadsheet_id

        execute_task(self.connect_v3.permissions().create(**{
            'fileId': file_id,
            'body': {
                'type': 'domain',
                'role': role,
                'domain': domain,
                'allowFileDiscovery': True,
            },
            'fields': 'id',
        }), self.auto_retry_after)
