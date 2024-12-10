import os
import logging

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from playwright.sync_api import sync_playwright


logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
logging.getLogger("django.request").setLevel(logging.ERROR)
logging.getLogger("django.server").setLevel(logging.ERROR)


class TestWhiteboxPluginGpsSimulatorBrowser(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)
        cls.context = cls.browser.new_context()
        cls.page = cls.context.new_page()

    @classmethod
    def tearDownClass(cls):
        cls.page.close()
        cls.context.close()
        cls.browser.close()
        cls.playwright.stop()
        super().tearDownClass()

    def setUp(self):
        self.page.goto(f"{self.live_server_url}{reverse('index')}")

    def test_gps_simulator_loaded(self):
        div = self.page.query_selector("#whitebox-plugin-gps-simulator")
        self.assertIsNotNone(div)

    def test_gps_simulator_update_reflected_on_stats(self):
        self.page.wait_for_selector("#whitebox-plugin-gps-simulator")

        function_exists = self.page.evaluate(
            "typeof window.updateCurrentLocation === 'function'"
        )
        self.assertTrue(function_exists)

        self.page.evaluate("window.updateCurrentLocation(1.1, 2.2, 3.3, 0);")

        latitude = self.page.query_selector("#latitude").inner_text()
        longitude = self.page.query_selector("#longitude").inner_text()
        altitude = self.page.query_selector("#altitude").inner_text()
        gps_timestamp = self.page.query_selector("#gps-timestamp").inner_text()

        self.assertEqual(latitude, "1.1")
        self.assertEqual(longitude, "2.2")
        self.assertEqual(altitude, "3.3")
        self.assertEqual(gps_timestamp, "0")
