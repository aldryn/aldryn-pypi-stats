from aldryn_client import forms


class PositiveIntegerField(forms.NumberField):
    def clean(self, value):
        value = super(PositiveIntegerField, self).clean(value)
        try:
            val = int(value)
            assert val > 0
            return value
        except:
            raise forms.ValidationError('Please provide a positive integer')


class Form(forms.BaseForm):
    cache_duration = PositiveIntegerField('Cache duration (in whole seconds)',
        required=False, initial=3600)

    def to_settings(self, data, settings):
        settings['ALDRYN_PYPI_STATS_CACHE_DURATION'] = data.get(
            'cache_duration', '')
        return settings
