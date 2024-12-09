
import humps
import collections

class Case:
	CAMEL = 1
	SNAKE = 2
	PASCAL = 3


_transforms = {
	Case.CAMEL: humps.camelize,
	Case.SNAKE: lambda x : humps.decamelize(humps.camelize(x)),
	Case.PASCAL: humps.pascalize,
}


_sequences = tuple([tuple, list])
_mappings = tuple([collections.abc.Mapping])

def register_mapping_class(cls):
	global _mappings

	new_mappings = set(_mappings)
	new_mappings.add(cls)
	_mappings = tuple(new_mappings)


def _create_case_mapping(fields, output_case):
	method = _transforms[output_case]
	mapping = dict()

	for field in fields:
		mapped_field = method(field)
		mapping[mapped_field] = field

	return mapping


def translate_case(value, desired_case):
	if isinstance(value, _sequences):
		result = list()

		for item in value:
			translated = translate_case(item, desired_case)
			result.append(translated)

		return result

	if not isinstance(value, _mappings):
		return value

	source_mapping = value
	mapping = _create_case_mapping(value.keys(),
		desired_case)

	converted_dict = dict()
	for output_key, input_key in mapping.items():
		input_content = source_mapping[input_key]

		if isinstance(input_content, _sequences):
			translated_values = list()

			for item in input_content:
				translated = translate_case(item, desired_case)
				translated_values.append(translated)

			input_content = translated_values

		if isinstance(input_content, _mappings):
			input_content = translate_case(input_content,
				desired_case)

		converted_dict[output_key] = input_content

	return converted_dict

#-------------------------------------------------------------------------------

_complex_types = (
	*_mappings,
	*_sequences
)

class _convert_mapping:
	def __init__(self, mapping):
		complex_values = dict()
		sane = dict()

		for key, value in mapping.items():
			dst = complex_values if isinstance(value, _complex_types) else sane
			dst[key] = value

		for key, value in complex_values.items():
			sane[key] = convert_to_object(value)

		self.__dict__.update(sane)


def convert_to_object(value):
	if isinstance(value, collections.abc.Mapping):
		return _convert_mapping(value)

	if isinstance(value, list):

		return [
			convert_to_object(element)
			for element in value
		]

	return value


def assemble_dicts(*bases, include_nones=True, **named):
	result = dict()

	for entry in bases:
		for key, value in entry.items():
			if value is not None or include_nones:
				result[key] = value

	for field, entry in named.items():
		if isinstance(entry, _sequences):
			scoped = list()

			for item in entry:
				if isinstance(item, _mappings):
					assembled = assemble_dicts(item)
					scoped.append(assembled)

				else:
					scoped.append(item)

			result[field] = scoped

		elif isinstance(entry, _mappings):
			scoped = dict()

			for key, value in entry.items():
				if value is not None:
					scoped[key] = value

			result[field] = scoped

		else:
			result[field] = entry

	mapped = translate_case(result, Case.CAMEL)
	return mapped

#-------------------------------------------------------------------------------

__all__ = [
	"Case",
	"register_mapping_class",
	"translate_case",
	"convert_to_object",
	"assemble_dicts"
]

