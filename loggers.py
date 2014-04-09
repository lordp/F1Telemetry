import datetime
import math
import ConfigParser
import gspread
import requests

class Logger(object):
    def __init__(self):
        #Should also load this from a file...
        self.config = ConfigParser.ConfigParser()
        self.config.read('config.ini')
        self.screen_name = self.config.get("logger", "screen_name")

    def lap(self, lap):
        pass

    def delta(self, delta):
        pass

    def position(self, x, y):
        pass

class LapTest(object):
    lap_time = 100.324

class GoogleDocs(Logger):
    def __init__(self):
        super(GoogleDocs, self).__init__()
        #TODO: think of a better way of configuring this! Perhaps INI file?
        self.username = self.config.get("logger", "username")
        self.password = self.config.get("logger", "password")
        self.spreadsheet_name = self.config.get("logger", "sheet_name")
        self.laps_worksheet_name = self.config.get("logger", "laps_worksheet")

        #Now connect to Google Docs
        #TODO: catch exceptions here and everywhere for that matter...
        self.google_docs = gspread.login(self.username, self.password)
        self.spreadsheet = self.google_docs.open(self.spreadsheet_name)
        self.laps = self.spreadsheet.worksheet(self.laps_worksheet_name)
        self.column = self._find_my_column(self.laps)

        #read
        self.row = 4

    def _find_my_column(self, worksheet):
        row = worksheet.row_values(1)
        if self.screen_name in row:
            return row.index(self.screen_name) + 1

        #TODO: there is a race here if there is more than one client
        column = len(row) + 1
        self.laps.update_cell(1, column, self.screen_name)
        return column

    def lap(self, lap):
        print self.row, lap.lap_time

        self.laps.update_cell(self.row, self.column, lap.lap_time)
        self.row += 1

class RacingLeagueCharts(Logger):
    def __init__(self):
        super(RacingLeagueCharts, self).__init__()
        self.session_id = 0
        self.session_url = 'https://racingleaguecharts.com/sessions/register'
        self.lap_url = 'https://racingleaguecharts.com/laps'

    def request_session(self, packet):
        payload = { "driver": self.screen_name, "track": packet.track_length, "type": packet.session_type }
        r = requests.post(self.session_url, data=payload, verify=False)
        if r.status_code == 200:
            self.session_id = r.json()['session_id']
            print self.session_id
            return True
        return False

    def send_sector(self, sector):
        print sector.sector_number, sector.sector_time

    def lap(self, lap):
        payload = { "session_id": self.session_id, "lap_number": lap.lap_number, "sector_1": lap.sector_1, "sector_2": lap.sector_2, "total": lap.lap_time }
        r = requests.post(self.lap_url, data=payload, verify=False)
        if r.status_code == 200:
            return True
        return False

if __name__ == '__main__':
    #g=GoogleDocs()
    r = RacingLeagueCharts()
    x=LapTest()
    #g.lap(x)
    r.lap(x)
