from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.translation import get_language
from django.conf import settings

register = Library()

def transdb(value):
	current_lang = get_language()
	default_lang = settings.LANGUAGE_CODE
	value_dict = eval(value)
	if value_dict:
		if value_dict.has_key(current_lang):
			return value_dict[current_lang]
		elif value_dict.has_key(default_lang):
			return value_dict[default_lang]
		else:
			return ''
	else:
		return ''
transdb.is_safe = True
transdb = stringfilter(transdb)

register.filter(transdb)
