from pathlib import Path


class Paths:
    ROOT_DIR = Path(__file__).parent.parent
    CVS_DIR = ROOT_DIR.parent / "CVs"