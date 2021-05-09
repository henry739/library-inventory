import json
import logging

from jsonschema import validate

logger = logging.Logger(__name__)


class SchemaValidator:
    """
    Encapsulates a single lazily loaded JSON schema.
    """

    def __init__(self, schema_filename):
        self.schema_filename = schema_filename
        self._schema = None

    def get_schema(self):
        if self._schema is not None:
            return self._schema

        try:
            with open(self.schema_filename, "r") as schema_file:
                self._schema = json.load(schema_file)
                return self._schema

        except FileNotFoundError:
            logger.exception(f"Unable to load schema file at: {self.schema_filename}")
            raise

        except json.JSONDecodeError:
            logger.exception(f"Invalid JSON schema file at: {self.schema_filename}")
            raise

    def validate(self, instance):
        validate(instance, self.get_schema())
