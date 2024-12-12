# textom/__init__.py
import textom.textom as textom

# Dynamically import all submodules and expose their contents
__all__ = []
for name in dir(textom):
    if not name.startswith("_"):  # Skip private attributes
        globals()[name] = getattr(textom, name)
        __all__.append(name)

# Optional: Set package metadata
__version__ = "0.1.1"
__author__ = "Moritz Frewein"
__email__ = "textom@fresnel.fr"