import json
from ..common_service import BaseEMCRestCaseAdmin


class TestDiscoveryhannelController(BaseEMCRestCaseAdmin):

    def setUp(self):
        super().setUp()

    def test_route_search_without_lang(self):
        url = "/api/discovery-channel"

        response = self.http_get(url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.reason, "OK")

        content = json.loads(response.content.decode("utf-8"))

        self.assertIn('discovery_channels', content)
        self.assertEqual(len(content['discovery_channels']), 10)

        channels = [d["name"] for d in content['discovery_channels']]
        ids = [d["id"] for d in content['discovery_channels']]

        # Default lang is catalan
        self.assertIn(
            "Fires / Xerrades",
            channels
        )

        # check order by sequence
        sequences = [dc.sequence for dc in self.env["discovery.channel"].browse(ids)]
        self.assertEqual(sequences, sorted(sequences))

    def test_route_search_with_lang_es(self):
        url = "/api/discovery-channel"

        response = self.http_get(
            url,
            headers={
                'Accept-Language': 'es'
            }
        )

        self.assertEquals(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        channels = [d["name"] for d in content['discovery_channels']]

        self.assertIn(
            "Ferias / Charlas",
            channels
        )

    def test_route_search_with_lang_ca(self):
        url = "/api/discovery-channel"

        response = self.http_get(
            url,
            headers={
                'Accept-Language': 'ca'
            }
        )

        self.assertEquals(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        channels = [d["name"] for d in content['discovery_channels']]

        self.assertIn(
            "Fires / Xerrades",
            channels
        )
