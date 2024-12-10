import asyncio
import csv
import os

from plugin.utils import Plugin


class WhiteboxPluginGpsSimulator(Plugin):
    name = "GPS Simulator"

    def __init__(self):
        self.is_active = False
        self.simulation_task = None
        self.GPSLocation = None
        self.file_path = os.path.join(os.path.dirname(__file__), "gps_simulation.csv")
        self.gps_data = self.read_gps_simulation(self.file_path)

        self.whitebox.register_event_callback("flight_start", self.on_flight_start)
        self.whitebox.register_event_callback("flight_end", self.on_flight_end)

        self.plugin_template = (
            "whitebox_plugin_gps_simulator/whitebox_plugin_gps_simulator.html"
        )
        self.plugin_js = [
            "/static/whitebox_plugin_gps_simulator/whitebox_plugin_gps_simulator.js"
        ]

    async def on_flight_start(self, data):
        self.is_active = True
        if self.simulation_task is None or self.simulation_task.done():
            self.simulation_task = asyncio.create_task(self.simulate_gps())

    async def on_flight_end(self, data):
        self.is_active = False
        if self.simulation_task:
            self.simulation_task.cancel()
            self.simulation_task = None

    def read_gps_simulation(self, file_path):
        gps_data = []

        with open(file_path, mode="r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row

            for row in reader:
                latitude = float(row[0])
                longitude = float(row[1])
                altitude = float(row[2])
                gps_data.append((latitude, longitude, altitude))

        return gps_data

    async def simulate_gps(self):
        step_delay = 1  # seconds

        for step in self.gps_data:
            if not self.is_active:
                break

            lat = step[0]
            lon = step[1]
            alt = step[2]

            await self.whitebox.api.location.emit_location_update(lat, lon, alt)
            await asyncio.sleep(step_delay)


plugin_class = WhiteboxPluginGpsSimulator
