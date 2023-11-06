from io import BufferedRandom

from cerberus import Validator, TypeDefinition

werkzeug_file_type = TypeDefinition('werkzeug_file', (BufferedRandom,), ())

Validator.types_mapping['werkzeug_file'] = werkzeug_file_type
