# randomcontent/__init__.py

from .generators.text_generator import generate_text
from .generators.number_generator import generate_number
from .generators.structured_generator import generate_structured_data
from .generators.identifier_generator import generate_identifier
from .generators.structured_generator import format_data

__all__ = ["generate_text", "generate_number", "generate_structured_data","generate_identifier","format_data"]
