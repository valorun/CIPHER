from cipher.core.actions import SpeechAction, CUSTOM_ACTIONS
from cipher.core.action_parameters import StringParameter
from datetime import datetime
from meteofrance_api import MeteoFranceClient

class GetWeatherAction(SpeechAction):
    display_name = 'Météo'

    @staticmethod
    def get_parameters():
        return [StringParameter('location', 'Ville/lieu', ''),
                    StringParameter('date', 'Date', 'La date au format YYYY-MM-DD')]

    @staticmethod
    def check_parameters(location: str, date: str):
        if not isinstance(location, str):
            return False, "The location must be a string."
        if date is not None and not isinstance(date, str):
            return False, "The date must be a string."
        return True, None

    @staticmethod
    def execute(location: str, date: str):
        valid, message = GetWeatherAction.check_parameters(location, date)
        print(location)
        print(date)
        if not valid:
            return
        client = MeteoFranceClient()

        # Search a location from name.
        list_places = client.search_places(location)
        if len(list_places) == 0:
            SpeechAction.execute("Désolé, je ne connais pas cette ville.")
            return
        my_place = list_places[0]

        # Fetch weather forecast for the location
        raw_forecast = client.get_forecast_for_place(my_place).daily_forecast

        # Formatted forecast with dates as keys
        forecast = {}
        for i in range(len(raw_forecast)):
            date = datetime.fromtimestamp(raw_forecast[i]['dt']).strftime('%Y-%m-%d')
            forecast[date] = raw_forecast[i]['weather12H']['desc']

        if date is None or date == '':
            date = datetime.now().strftime('%Y-%m-%d')
        else:
            date = date.split(' ')[0]

        if date not in forecast:
            SpeechAction.execute("Désolé, je ne sais pas.")
            return
        
        SpeechAction.execute(f"Demain, à {location}, le temps sera {forecast[date]}")

CUSTOM_ACTIONS['weather'] = GetWeatherAction