import requests
import logging
from datetime import datetime, timedelta

from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=15)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Setup the Neoom sensor platform."""

    # Hier können Sie Konfigurationsparameter abrufen, falls erforderlich
    api_key = config.get("api_key")
    site_id = config.get("site_id")

    # Überprüfen Sie, ob erforderliche Konfigurationen vorhanden sind
    if api_key is None or site_id is None:
        _LOGGER.error("API key or site ID not provided in configuration")
        return False

    # Erstellen Sie eine Instanz Ihrer Sensoren
    sensors = [
        NeoomSensor(api_key, site_id, "power_consumption", "Power Consumption", "W"),
        NeoomSensor(api_key, site_id, "power_consumption_calc", "Calculated Power Consumption", "W"),
        NeoomSensor(api_key, site_id, "power_production", "Power Production", "W"),
        NeoomSensor(api_key, site_id, "power_storage", "Power Storage", "W"),
        NeoomSensor(api_key, site_id, "power_grid", "Power Grid", "W"),
        NeoomSensor(api_key, site_id, "power_charging_stations", "Power Charging Stations", "W"),
        NeoomSensor(api_key, site_id, "power_heating", "Power Heating", "W"),
        NeoomSensor(api_key, site_id, "power_appliances", "Power Appliances", "W"),
        NeoomSensor(api_key, site_id, "state_of_charge", "State of Charge", "%"),
        NeoomSensor(api_key, site_id, "self_sufficiency", "Self Sufficiency", "%"),
    ]

    # Fügen Sie die Sensoren zur Plattform hinzu
    add_entities(sensors, True)

class NeoomSensor(Entity):
    """Representation of a Neoom sensor."""

    def __init__(self, api_key, site_id, sensor_type, name, unit_of_measurement):
        """Initialize the sensor."""
        self._api_key = api_key
        self._site_id = site_id
        self._sensor_type = sensor_type
        self._name = name
        self._unit_of_measurement = unit_of_measurement
        self._state = None
        self._last_updated = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Neoom {self._name}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    @property
    def last_updated(self):
        """Return the last update time of the sensor."""
        return self._last_updated

    def update(self):
        """Fetch the latest data from the Neoom API."""
        url = f"https://api.ntuity.io/v1/sites/{self._site_id}/energy-flow/latest"

        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self._api_key}"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            if self._sensor_type in data:
                self._state = data[self._sensor_type]["value"]
                self._last_updated = datetime.strptime(data[self._sensor_type]["time"], "%Y-%m-%dT%H:%M:%S.%fZ")
            else:
                _LOGGER.warning(f"Sensor type '{self._sensor_type}' not found in API response.")
                self._state = None
        except requests.exceptions.RequestException as err:
            _LOGGER.error(f"Error fetching data from Neoom API: {err}")
            self._state = None
