# ha-atenedgar

[![Linting](https://github.com/NitorCreations/ha-atenedgar/actions/workflows/ruff.yaml/badge.svg)](https://github.com/NitorCreations/ha-atenedgar/actions/workflows/ruff.yaml)
[![Tests](https://github.com/NitorCreations/ha-atenedgar/actions/workflows/unittest.yaml/badge.svg)](https://github.com/NitorCreations/ha-atenedgar/actions/workflows/unittest.yaml)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=NitorCreations&repository=ha-atenedgar&category=integration)

Home Assistant integration for the [Aten VS482](https://www.aten.com/global/en/products/professional-audiovideo/video-switches/vs482/) 
HDMI switch via an [EDGAR](https://en.papouch.com/edgar-poe-ethernet-serial-device-server-p3300/) serial device server

## Features

* input selection

## Quirks

The serial interface doesn't provide a method for querying the currently selected input, so the source selection in 
Home Assistant is opportunistic.

## Tests

```bash
python3 -m unittest discover -s tests/ -v
```
