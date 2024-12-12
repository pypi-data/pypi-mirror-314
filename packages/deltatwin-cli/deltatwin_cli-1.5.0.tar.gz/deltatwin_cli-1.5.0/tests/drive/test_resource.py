import json
import os
import unittest

from click.testing import CliRunner

from delta.cli import delta_cli


class TestDriveResource(unittest.TestCase):
    service_url = 'https://delta_api'
    resource_dir = os.path.join(os.path.dirname(__file__), '../resources')

    @classmethod
    def setUpClass(cls) -> None:
        with open(os.path.join(cls.resource_dir,
                               'drive/manifest_example.json')) as exp:
            with open('manifest.json', 'w') as f:
                json.dump(json.loads(exp.read()), f)

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.exists("manifest.json"):
            os.remove("manifest.json")

    def test_resources(self):
        runner = CliRunner()

        result = runner.invoke(
            delta_cli,
            ["drive", "resource", "list"],
            catch_exceptions=False
        )
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(
            delta_cli,
            ["drive", "resource", "list", "-f", "json"],
            catch_exceptions=False
        )

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(json.loads("[]"), json.loads(result.output))

        result = runner.invoke(
            delta_cli,
            ["drive", "resource", "add",
             os.path.join(self.resource_dir, 'login.json'),
             'log.json'],
            catch_exceptions=False
        )
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(
            delta_cli,
            ["drive", "resource", "list", "-f", "json"],
            catch_exceptions=False
        )

        self.assertEqual(result.exit_code, 0)

        data = [{
            "name": "log.json",
            "source_url": os.path.join(self.resource_dir, 'login.json')
        }]

        self.assertEqual(data, json.loads(result.output))

        result = runner.invoke(
            delta_cli,
            ["drive", "resource", "delete", 'log.json'],
            catch_exceptions=False
        )
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(
            delta_cli,
            ["drive", "resource", "list", "-f", "json"],
            catch_exceptions=False
        )

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(json.loads("[]"), json.loads(result.output))
