import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from kfp_config import DEFAULT_KFP_ENDPOINT, get_kfp_endpoint


class KfpEndpointTests(unittest.TestCase):
    def test_defaults_to_local_port_forward(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(get_kfp_endpoint(), DEFAULT_KFP_ENDPOINT)

    def test_uses_configured_endpoint_without_trailing_slash(self):
        with patch.dict(os.environ, {"KFP_ENDPOINT": "http://ml-pipeline:8888/"}):
            self.assertEqual(get_kfp_endpoint(), "http://ml-pipeline:8888")


if __name__ == "__main__":
    unittest.main()