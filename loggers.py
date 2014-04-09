import datetime
import math
import requests

class Logger(object):
    def __init__(self, driver):
        self.screen_name = driver

    def lap(self, lap):
        pass

    def delta(self, delta):
        pass

    def position(self, x, y):
        pass

class RacingLeagueCharts(Logger):
    def __init__(self, driver, status_bar):
        super(RacingLeagueCharts, self).__init__(driver)
        self.session_id = 0
        self.status_bar = status_bar
        self.session_url = 'https://racingleaguecharts.com/sessions/register'
        self.lap_url = 'https://racingleaguecharts.com/laps'

    def request_session(self, packet):
        payload = { "driver": self.screen_name, "track": packet.track_length, "type": packet.session_type }
        r = requests.post(self.session_url, data=payload, verify=False)
        if r.status_code == 200:
            self.session_id = r.json()['session_id']
            self.status_bar.SetStatusText('Session id: {0}'.format(self.session_id))
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
