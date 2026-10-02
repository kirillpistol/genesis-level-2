"""Two manual package identities for testing bindings. No trained sector models."""
import hashlib
import json
from pathlib import Path
from .numeric import Numeric

REGISTRY={'sector-a.numeric':Numeric,'sector-b.numeric':Numeric}

def package_digest():
    root=Path(__file__).resolve().parent
    # Exact reviewed source bundle; real packages must include weights/assets too.
    hashes={name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in ('numeric.py','bindings_demo.py')}
    raw=json.dumps(hashes,sort_keys=True,separators=(',',':')).encode()
    return hashlib.sha256(raw).hexdigest()

PACKAGE_SPECS={name:dict(algorithm_version=Numeric.version,model_version='demo-aggregates/1',
                        input_contract=sector+'.numeric/1',package_sha256=package_digest())
               for name,sector in [('sector-a.numeric','sector-a'),('sector-b.numeric','sector-b')]}
