from django.newforms.widgets import Widget
from django.conf import settings
from django.utils.safestring import mark_safe
from django.newforms.util import flatatt

class TransCharWidget(Widget):
	def value_to_dict(self, value):
		if isinstance(value, dict):
			value_dict = value
		else:
			if value:
				value_dict = eval(value)
				if not isintance(value_dict, dict):
					value_dict = {}
			else:
				value_dict = {}
		return value_dict

	def get_input(self, name, value, lang, attrs):
		value_html = ''
		if value:
			value_html = ' value="%s"' % value
		return '<input name="%s_%s"%s/>' % (name, lang, value_html)
		
	def render(self, name, value, attrs=None):
		value_dict = self.value_to_dict(value)
		output = []
		for lang_code, lang_name in settings.LANGUAGES:
			value_for_lang = ''
			if value_dict.has_key(lang_code):
				value_for_lang = value_dict[lang_code]
			output.append('<li style="list-style-type: none">%s: %s</li>' % (lang_name, self.get_input(name, value_for_lang, lang_code, attrs)))
		return mark_safe(u'<ul id="id_%s">%s</ul>' % (name, u''.join(output)))
	
	def value_from_datadict(self, data, files, name):
		output = {}
		for lang_code, lang_name in settings.LANGUAGES:
			output[lang_code] = data.get('%s_%s' % (name, lang_code))
		return output

class TransTextWidget(TransCharWidget):
	def __init__(self, attrs=None):
		self.attrs = {'cols': '40', 'rows': '10'}
		if attrs:
			self.attrs.update(attrs)

	def get_input(self, name, value, lang, attrs):
		#final_attrs = self.build_attrs(attrs, name=name)
		return '<textarea name="%s_%s"%s>%s</textarea>' % (name, lang, flatatt(self.attrs), value)

