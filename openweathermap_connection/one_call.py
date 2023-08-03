from datetime import datetime

import pyowm
import pandas as pd
import numpy as np

from .connection import OpenWeatherMapConnection

class OpenWeatherMapOneCallConnection(OpenWeatherMapConnection):

    def _connect(self, lat: float, lon: float, dt: float = None, **kwargs) -> pyowm.weatherapi25.one_call.OneCall:
        '''
        When initialized, an API call is made and a OneCall object containing all relevant weather data is returned. 
        '''
        conn = super()._connect(**kwargs)
        self.dt = dt
        if dt:
            return conn.weather_manager().one_call_history(lat, lon, dt, **kwargs)
        else:
            return conn.weather_manager().one_call(lat, lon, **kwargs)
        
    def get_current(self):
        return self._instance.current

    def get_forecast_daily(self): 
        return self._instance.forecast_daily

    def get_forecast_hourly(self):
        return self._instance.forecast_hourly
        
    def get_forecast_minutely(self):
        return self._instance.forecast_minutely
    
    def get_national_weather_alerts(self):
        return self._instance.national_weather_alerts
    
    def get_weather_summary(self):
        current_weather = self.get_current()
        minutely_forecasts = self.get_forecast_minutely()
        hourly_forecasts = self.get_forecast_hourly()
        daily_forecasts = self.get_forecast_daily()

        combined_forecasts = {}
        combined_forecasts[current_weather.reference_time()] = current_weather.to_dict()
        for group in [minutely_forecasts, hourly_forecasts, daily_forecasts]:
            for fcst in group:
                combined_forecasts[fcst.reference_time()] = fcst.to_dict()
        return combined_forecasts

    def get_temperature_df(self):
        summary = self.get_weather_summary()
        temperature_data = {'dt': [], 'temp': [], 'high_temp': [], 'low_temp': []}
        for ts, fcst in summary.items():
            dt = datetime.fromtimestamp(ts)
            if 'temperature' in fcst.keys():
                if 'temp' in fcst['temperature'].keys():
                    temp = fcst['temperature']['temp']
                    temperature_data['dt'].append(dt)
                    temperature_data['temp'].append(temp)
                    temperature_data['high_temp'].append(np.nan)
                    temperature_data['low_temp'].append(np.nan)
                # For timestamps 2+ days in the future, only daily min and max are given
                elif 'max' in fcst['temperature'].keys() and 'min' in fcst['temperature'].keys():
                    high_temp = fcst['temperature']['max']
                    low_temp = fcst['temperature']['min']
                    temperature_data['dt'].append(dt)
                    temperature_data['temp'].append(np.nan)
                    temperature_data['high_temp'].append(high_temp)
                    temperature_data['low_temp'].append(low_temp)
        temperature_df = pd.DataFrame(temperature_data).sort_values(by='dt')
        return temperature_df