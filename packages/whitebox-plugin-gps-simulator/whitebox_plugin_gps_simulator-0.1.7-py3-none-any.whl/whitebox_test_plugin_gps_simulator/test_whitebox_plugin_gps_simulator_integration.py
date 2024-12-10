import json
import asyncio

from django.test import TransactionTestCase
from django.urls import reverse
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter

from whitebox.routing import websocket_urlpatterns
from plugin.manager import plugin_manager
from whitebox.api import API


class TestWhiteboxPluginGpsSimulatorIntegration(TransactionTestCase):
    def setUp(self) -> None:
        self.plugin = next(
            (
                x
                for x in plugin_manager.plugins
                if x.__class__.__name__ == "WhiteboxPluginGpsSimulator"
            ),
            None,
        )
        self.application = URLRouter(websocket_urlpatterns)
        return super().setUp()

    def test_plugin_loaded(self):
        self.assertIsNotNone(self.plugin)

    async def test_websocket_flight_start_triggers_simulation(self):
        communicator = WebsocketCommunicator(self.application, "/ws/flight/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        await communicator.send_json_to({"type": "flight_start"})
        response = await communicator.receive_json_from()
        self.assertEqual(response["type"], "message")
        self.assertEqual(response["message"], "Flight started")
        self.assertTrue(self.plugin.is_active)
        self.assertIsNotNone(self.plugin.simulation_task)

        await asyncio.sleep(1)

        response = await communicator.receive_json_from()
        self.assertEqual(response["type"], "location_update")
        self.assertIn("latitude", response)
        self.assertIn("longitude", response)
        self.assertIn("altitude", response)

        await communicator.disconnect()

    async def test_websocket_flight_end_stops_simulation(self):
        communicator = WebsocketCommunicator(self.application, "/ws/flight/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        await communicator.send_json_to({"type": "flight_start"})
        await asyncio.sleep(1)

        self.assertTrue(self.plugin.is_active)
        self.assertIsNotNone(self.plugin.simulation_task)

        await communicator.send_json_to({"type": "flight_end"})
        await asyncio.sleep(1)

        self.assertFalse(self.plugin.is_active)
        self.assertIsNone(self.plugin.simulation_task)

        await communicator.disconnect()

    async def test_location_updates_stored_in_database(self):
        communicator = WebsocketCommunicator(self.application, "/ws/flight/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        await communicator.send_json_to({"type": "flight_start"})
        await asyncio.sleep(1)

        await communicator.send_json_to({"type": "flight_end"})
        await asyncio.sleep(1)

        await communicator.disconnect()

        api = API()
        latest_location = await api.location.get_latest_location()
        self.assertIsNotNone(latest_location)

    def test_plugin_template_and_static_files(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "whitebox_plugin_gps_simulator/whitebox_plugin_gps_simulator.html",
            response.context["templates"],
        )
        self.assertIn(
            "/static/whitebox_plugin_gps_simulator/whitebox_plugin_gps_simulator.js",
            response.context["js_files"],
        )
