import requests
import decimal
import datetime

class RacingLeagueCharts:
    def __init__(self, parent):
        self.session_id = 0
        self.parent = parent
        self.log = []

        self.session_url = 'https://racingleaguecharts.com/sessions/register'
        self.lap_url = 'https://racingleaguecharts.com/laps'

    def add_log_entry(self, msg):
        self.log.append('[{0}]: {1}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), msg))

    def request_session(self, packet):
        if self.parent.config['local_enabled']:
            return True
        self.add_log_entry('New session requested')
        track_length = decimal.Decimal(packet.track_length)
        payload = {"driver": self.parent.config['name'],
                   "track": round(track_length, 3),
                   "type": packet.session_type,
                   "race": self.parent.race_id}
        r = requests.post(self.session_url, data=payload, verify=False)
        if r.status_code == 200:
            self.session_id = r.json()['session_id']
            self.parent.session_id.SetLabel('Session: {0}'.format(self.session_id))
            self.add_log_entry("Session id: {0}".format(self.session_id))
            return True
        return False

    @staticmethod
    def send_sector(sector):
        print sector.sector_number, sector.sector_time

    def lap(self, lap):
        raw_times, formatted_times = self.format_lap_times(lap)
        self.add_log_entry("Lap: {0:02d} {1} {2} {3} {4}".format(
            int(lap.lap_number), formatted_times['total'],
            formatted_times['s1'], formatted_times['s2'],
            formatted_times['s3'])
        )
        self.parent.last_lap.SetLabel('Last Lap: {0}'.format(formatted_times['total']))
        if self.parent.config['local_enabled']:
            return True
        payload = {
            "session_id": self.session_id, "lap_number": lap.lap_number,
            "sector_1": raw_times['s1'], "sector_2": raw_times['s2'], "sector_3": raw_times['s3'],
            "total": raw_times['total'], "speed": lap.top_speed, "fuel": lap.current_fuel, "position": lap.position
        }
        r = requests.post(self.lap_url, data=payload, verify=False)
        if r.status_code == 200:
            return True
        return False

    @staticmethod
    def format_time(seconds):
        m, s = divmod(seconds, 60)
        if m > 0:
            return '{0:.0f}:{1:06.3f}'.format(m, s)
        else:
            return '{0:06.3f}'.format(s)

    def format_lap_times(self, lap):
        if lap.sector_1:
            s1 = round(decimal.Decimal(lap.sector_1), 3)
        else:
            s1 = 0

        if lap.sector_2:
            s2 = round(decimal.Decimal(lap.sector_2), 3)
        else:
            s2 = 0

        if lap.lap_time:
            total = round(decimal.Decimal(lap.lap_time), 3)
            s3 = round(decimal.Decimal(total - s2 - s1), 3)
        else:
            total = 0
            s3 = 0

        fs1 = self.format_time(s1)
        fs2 = self.format_time(s2)
        fs3 = self.format_time(s3)
        fst = self.format_time(total)

        return [{"s1": s1, "s2": s2, "s3": s3, "total": total}, {"s1": fs1, "s2": fs2, "s3": fs3, "total": fst}]
