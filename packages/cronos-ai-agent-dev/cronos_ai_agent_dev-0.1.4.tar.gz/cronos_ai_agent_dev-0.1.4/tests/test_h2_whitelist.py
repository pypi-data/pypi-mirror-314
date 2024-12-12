import unittest
from src.cronos_ai_agent_dev.functions.h2_whitelist_function import H2Whitelist


class TestH2Whitelist(unittest.TestCase):
    def setUp(self):
        self.h2_whitelist = H2Whitelist()

    def test_name_property(self):
        self.assertEqual(self.h2_whitelist.name, "get_h2_whitelist_tokens")

    def test_spec_property(self):
        spec = self.h2_whitelist.spec
        self.assertEqual(spec["type"], "function")
        self.assertEqual(spec["function"]["name"], "get_h2_whitelist_tokens")
        self.assertTrue("description" in spec["function"])

    def test_execute_success(self):
        result = self.h2_whitelist.execute({}, "", [])

        # Check if the request was successful
        self.assertTrue(result["success"])

        # Check if the response contains expected formatting
        response = result["response"]
        self.assertIn("Available tokens on Cronos zkEVM:", response)
        self.assertIn("Address:", response)
        self.assertIn("Decimals:", response)
        self.assertIn("Explorer:", response)


if __name__ == "__main__":
    unittest.main()
