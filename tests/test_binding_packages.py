import hashlib
import json
from pathlib import Path
import unittest
from level2_algorithms import bindings_demo
class PackageTests(unittest.TestCase):
    def test_actual_source_bundle_and_distinct_contracts(self):
        root=Path(bindings_demo.__file__).parent
        hashes={name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in ('numeric.py','bindings_demo.py')}
        expected=hashlib.sha256(json.dumps(hashes,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        self.assertEqual(bindings_demo.package_digest(),expected)
        a,b=(bindings_demo.PACKAGE_SPECS[name] for name in ('sector-a.numeric','sector-b.numeric'))
        self.assertEqual(a['package_sha256'],expected)
        self.assertNotEqual(a['input_contract'],b['input_contract'])
        self.assertEqual(a['algorithm_version'],bindings_demo.REGISTRY['sector-a.numeric'].version)
