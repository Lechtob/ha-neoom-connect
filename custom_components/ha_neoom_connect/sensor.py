from __future__ import annotations
import logging

import aiohttp
import voluptuous as vol

from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv


from .const import DOMAIN