from homeassistant import config_entries
from homeassistant.helpers import config_entry_flow
import voluptuous as vol

DEFAULT_INTERVAL = 15

class NeoomFlowHandler(config_entries.ConfigFlow, domain="neoom"):
    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            # Zeige das Formular für die Konfiguration des Intervalls an
            return self.async_show_form(
                step_id="interval",
                data_schema=vol.Schema({
                    "api_key": str,
                    "site_id": str,
                    "update_interval": vol.Coerce(int, default=DEFAULT_INTERVAL),
                }),
            )

        # Zeige das Formular für die Benutzereingabe an
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                "api_key": str,
                "site_id": str,
            }),
        )

    async def async_step_interval(self, user_input=None):
        """Handle the interval configuration step."""
        if user_input is not None:
            # Speichere die bestätigten Daten und das Intervall
            return self.async_create_entry(title="Neoom Integration", data=user_input)

        # Zeige das Intervallformular an
        return self.async_show_form(
            step_id="interval",
            data_schema=vol.Schema({
                "api_key": str,
                "site_id": str,
                "update_interval": vol.Coerce(int, default=DEFAULT_INTERVAL),
            }),
        )
