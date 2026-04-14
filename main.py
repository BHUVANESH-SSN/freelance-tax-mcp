import sys
import os
from pathlib import Path

# Ensure src is in the python path
src_path = str(Path(__file__).parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Disable verbose HTTP logging from httpx/httptools
import logging
logging.getLogger("httpx").setLevel(logging.WARNING)

from freelance_tax_mcp.server import main

if __name__ == "__main__":
    main()
