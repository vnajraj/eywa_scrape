from dataclasses import dataclass, asdict
import json


@dataclass
class Measurement:
    date: str
    hour: int
    station: str
    wind_direction: str
    wind_speed: float
    temperature: float
    humidity: int
    pressure: float
    pressure_tendency: float
    weather: str

    @staticmethod
    def new(date, hour, row):
        hour = int(hour)

        # remove station type indicator
        station = row[0].text.rstrip(" A")

        wind_direction = row[1].text
        wind_speed = None if row[2].text == "-" else float(row[2].text)
        temperature = None if row[3].text == "-" else float(row[3].text)
        humidity = -1 if row[4].text == "-" else int(row[4].text)

        pressure = row[5].text.rstrip("*")
        pressure = None if pressure == "-" else float(pressure)

        pressure_tendency = None if row[6].text == "-" else float(row[6].text)
        weather = row[7].text

        return Measurement(
            date=date,
            hour=hour,
            station=station,
            wind_direction=wind_direction,
            wind_speed=wind_speed,
            temperature=temperature,
            humidity=humidity,
            pressure=pressure,
            pressure_tendency=pressure_tendency,
            weather=weather,
        )

    def to_json(self):
        return json.dumps(asdict(self))

    def to_dict(self):
        return asdict(self)
