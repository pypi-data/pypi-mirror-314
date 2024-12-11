import pytz
from datetime import datetime

class DateTimeHelpers:
    @classmethod
    def convert_to_datetime(date_str):
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    @classmethod
    def convert_to_date(date_str):
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    @classmethod
    def convert_to_time(time_str):
        return datetime.strptime(time_str, '%H:%M:%S').time()
    @classmethod
    def convert_to_string(date_time):
        return date_time.strftime('%Y-%m-%d %H:%M:%S')
    @classmethod
    def convert_to_date_string(date_time):
        return date_time.strftime('%Y-%m-%d')
    @classmethod
    def convert_to_time_string(date_time):
        return date_time.strftime('%H:%M:%S')
    @classmethod
    def get_current_date_time():
        return datetime.now()
    @classmethod
    def get_current_date():
        return datetime.now().date()
    @classmethod
    def get_current_time():
        return datetime.now().time()
    @classmethod
    def convert_to_utc(date_time):
        return date_time.astimezone(pytz.utc)
    @classmethod
    def convert_to_local(date_time):
        return date_time.astimezone(pytz.timezone('America/New_York')) 