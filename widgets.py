from django.newforms.widgets import Widget
from django.conf import settings
from django.utils.safestring import mark_safe

class TransDbWidget(Widget):
	def render(self, name, value, attrs=None):
		output = []
		for lang_code, lang_name in settings.LANGUAGES:
			value_str = ''
			if value and value.has_key(lang_code):
				value_str = ' value="%s"' % value[lang_code]
			output.append('<li style="list-style-type: none">%s: <input name="%s_%s" type="text"%s/></li>' % (lang_name, name, lang_code, value_str))
		return mark_safe(u'<ul id="id_%s">%s</ul>' % (name, u''.join(output)))
	
	def value_from_datadict(self, data, files, name):
		output = {}
		for lang_code, lang_name in settings.LANGUAGES:
			output[lang_code] = data.get('%s_%s' % (name, lang_code))
		return output

