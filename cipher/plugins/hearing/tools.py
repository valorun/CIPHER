from datetime import datetime
from meteofrance_api import MeteoFranceClient

def get_datetime() -> str:
    """
    Get the current time and date.
    """
    now = datetime.now()
    return f"Il est {now.hour} heure {now.minute} et nous sommes le {now.strftime('%d/%m/%Y')}"

def get_weather(location: str, date: str = None) -> str:
    """
    Get the weather forecast for a specific location and date.
    
    Args:
        location (str): Name of the city or place
        date (str, optional): Optional date in YYYY-MM-DD format
    """
    if not isinstance(location, str):
        return "Erreur : The location must be a string."
    if date is not None and not isinstance(date, str):
        return "Erreur : The date must be a string."
    
    client = MeteoFranceClient()

    # Search a location from name.
    list_places = client.search_places(location)
    if len(list_places) == 0:
        return f"Désolé, je ne connais pas la ville {location}."
    my_place = list_places[0]

    # Fetch weather forecast for the location
    raw_forecast = client.get_forecast_for_place(my_place).daily_forecast

    # Formatted forecast with dates as keys
    forecast = {}
    for i in range(len(raw_forecast)):
        d = datetime.fromtimestamp(raw_forecast[i]['dt']).strftime('%Y-%m-%d')
        forecast[d] = raw_forecast[i]['weather12H']['desc']

    if date is None or date == '':
        date = datetime.now().strftime('%Y-%m-%d')
    else:
        date = date.split(' ')[0]

    if date not in forecast:
        return f"Désolé, je n'ai pas de prévisions pour la date {date}."
    
    return f"Prévision pour {location} le {date} : {forecast[date]}"

AVAILABLE_TOOLS = [get_datetime, get_weather]
