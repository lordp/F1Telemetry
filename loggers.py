import datetime
import math
import gspread

class Logger(object):
    def __init__(self):
        #Should also load this from a file...
        self.screen_name = "Physfix"

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
        self.username = "USERNAME"
        self.password = "PASSWORD"
        self.spreadsheet_name = "F1 telemetry template"
        self.laps_worksheet_name = "Laps"

        #Now connect to Google Docs
        #TODO: catch exceptions here and everywhere for that matter...
        self.google_docs = gspread.login(self.username, self.password)
        self.spreadsheet = self.google_docs.open(self.spreadsheet_name)
        self.laps = self.spreadsheet.worksheet(self.laps_worksheet_name)
        self.column = self._find_my_column(self.laps)

        #read
        self.row = 2

    def _find_my_column(self, worksheet):
        row = worksheet.row_valugit addes(1)
        if self.screen_name in row:
            return row.index(self.screen_name) + 1

        #TODO: there is a race here if there is more than one client
        column = len(row) + 2
        self.laps.update_cell(1, column, self.screen_name)
        return column

    def lap(self, lap):
        print self.row, lap.lap_time

        #TODO: replace this with something nicer
        sec = lap.lap_time
        msec = (sec - math.floor(sec)) * 1000
        print "msec", msec
        nice_time = datetime.timedelta(seconds=sec)
        print str(nice_time)
        self.laps.update_cell(self.row, self.column, str(nice_time))
        self.row += 1

if __name__ == '__main__':
    g=GoogleDocs()
    x=LapTest()
    g.lap(x)