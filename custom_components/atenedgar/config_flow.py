from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow

from custom_components.atenedgar import Edgar
from custom_components.atenedgar.const import CONF_HOST, CONF_NAME, CONF_PORT, DOMAIN

STEP_USERDATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT, default=80): int,
        vol.Required(CONF_NAME): str,
    }
)


class AtenEdgarConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Handle a flow initialized by the user."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Verify that the Edgar serial server is reachable
            edgar = Edgar(user_input["host"], user_input["port"])

            if not await edgar.is_reachable():
                errors["base"] = "cannot_connect"
            else:
                title = user_input["name"]
                return self.async_create_entry(title=title, data=user_input)

        return self.async_show_form(step_id="user", data_schema=STEP_USERDATA_SCHEMA, errors=errors)
