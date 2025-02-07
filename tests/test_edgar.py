import unittest

from custom_components.atenedgar.edgar import parse_settings_xml


class EdgarTestCase(unittest.TestCase):
    def test_parse_settings_xml(self):
        with open("tests/resources/edgar_settings.xml", "rb") as settings_file:
            settings_xml = settings_file.read().decode("iso-8859-2")
            settings = parse_settings_xml(settings_xml)

            self.assertEqual("10.211.0.112", settings.ip)
            self.assertEqual("Edgar ETH", settings.type)
            self.assertEqual("00:80:A3:E6:2E:75", settings.mac)
            self.assertEqual("1.5", settings.fw)


if __name__ == "__main__":
    unittest.main()
