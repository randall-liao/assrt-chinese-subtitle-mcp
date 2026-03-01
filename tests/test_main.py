import sys
from pathlib import Path

# Add src to the Python path to allow tests to import from it easily without a package install
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import main


def test_main():
    assert main() == "Hello from assrt-chinese-subtitle-mcp!"
