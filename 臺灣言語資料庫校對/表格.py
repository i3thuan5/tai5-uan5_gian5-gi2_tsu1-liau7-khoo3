from django.forms import ModelForm
from django.forms import Textarea
from django.forms import Select

from 臺灣言語資料庫.模型 import 文字
from django.forms.widgets import TextInput, HiddenInput

class 文字校對表格(ModelForm):
	class Meta:
		model = 文字
		fields = ['流水號','型體', '音標', ]
		labels = {
        }
		help_texts = {
        }
		error_messages = {
        }
		widgets = {
			'':HiddenInput(),
			'型體': TextInput(attrs={'class':'校對'}),
			'音標': TextInput(attrs={'class':'校對'}),
		}
		