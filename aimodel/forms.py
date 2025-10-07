from django import forms
from .models import K2Model, KeplerModel, TESSModel

class K2Form(forms.ModelForm):
    class Meta:
        model = K2Model
        fields = '__all__'
        widgets = {
            'pl_orbper': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.01, 'min': 0, 'placeholder': 'e.g., 41.688644'}),
            'pl_trandur': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.001, 'min': 0, 'placeholder': 'e.g., 2.3'}),
            'pl_rade': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.1, 'min': 0, 'placeholder': 'e.g., 2.355'}),
            'pl_ratror': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.0001, 'min': 0, 'placeholder': 'e.g., 0.022'}),
            'st_teff': forms.NumberInput(attrs={'class': 'glass-input', 'step': 50, 'min': 0, 'placeholder': 'e.g., 5703.0'}),
            'st_rad': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.01, 'min': 0, 'placeholder': 'e.g., 0.95'}),
            'sy_pmra': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.1, 'placeholder': 'e.g., 36.5'}),
            'sy_pmdec': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.1, 'placeholder': 'e.g., -51.3'}),
            'sy_dist': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.1, 'min': 0, 'placeholder': 'e.g., 179.46'}),
            'sy_gaiamag': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.01, 'placeholder': 'e.g., 10.86'}),
            'sy_tmag': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.01, 'placeholder': 'e.g., 10.40'}),
            'sy_kepmag': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.01, 'placeholder': 'e.g., 11.04'}),
        }

class KeplerForm(forms.ModelForm):
    class Meta:
        model = KeplerModel
        fields = '__all__'
        widgets = {
            'koi_period': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.001, 'min': 0, 'placeholder': 'e.g., 3.45'}),
            'koi_duration': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.0001, 'min': 0, 'placeholder': 'e.g., 2.4'}),
            'koi_depth': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.0001, 'min': 0, 'placeholder': 'e.g., 400.0'}),
            'koi_ror': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.0001, 'min': 0, 'placeholder': 'e.g., 0.02'}),
            'koi_dor': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.01, 'min': 0, 'placeholder': 'e.g., 25.0'}),
            'koi_incl': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.1, 'min': 0, 'max': 90, 'placeholder': 'e.g., 89.5'}),
            'koi_impact': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.01, 'min': 0, 'placeholder': 'e.g., 0.3'}),
            'koi_prad': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.1, 'min': 0, 'placeholder': 'e.g., 1.5'}),
            'koi_sma': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.001, 'min': 0, 'placeholder': 'e.g., 0.05'}),
            'koi_teq': forms.NumberInput(attrs={'class': 'glass-input', 'step': 1, 'min': 0, 'placeholder': 'e.g., 1200.0'}),
            'koi_insol': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.1, 'min': 0, 'placeholder': 'e.g., 1800.0'}),
            'koi_model_snr': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.1, 'min': 0, 'placeholder': 'e.g., 25.0'}),
            'koi_num_transits': forms.NumberInput(attrs={'class': 'glass-input', 'step': 1, 'min': 0, 'placeholder': 'e.g., 15'}),
            'koi_max_sngle_ev': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.0001, 'min': 0, 'placeholder': 'e.g., 100.0'}),
            'koi_steff': forms.NumberInput(attrs={'class': 'glass-input', 'step': 50, 'min': 0, 'placeholder': 'e.g., 5800'}),
            'koi_slogg': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.01, 'placeholder': 'e.g., 4.4'}),
            'koi_smet': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.01, 'placeholder': 'e.g., 0.1'}),
            'koi_srad': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.01, 'min': 0, 'placeholder': 'e.g., 1.0'}),
            'koi_smass': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.001, 'min': 0, 'placeholder': 'e.g., 1.0'}),
            'koi_srho': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.001, 'min': 0, 'placeholder': 'e.g., 1.2'}),
            'koi_kepmag': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.001, 'placeholder': 'e.g., 12.3'}),
            'koi_gmag': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.001, 'placeholder': 'e.g., 13.0'}),
            'koi_rmag': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.001, 'placeholder': 'e.g., 12.8'}),
            'koi_imag': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.001, 'placeholder': 'e.g., 12.7'}),
            'koi_zmag': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.001, 'placeholder': 'e.g., 12.5'}),
            'koi_jmag': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.001, 'placeholder': 'e.g., 11.2'}),
            'koi_hmag': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.001, 'placeholder': 'e.g., 11.0'}),
            'koi_kmag': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.001, 'placeholder': 'e.g., 10.8'}),
        }

class TESSForm(forms.ModelForm):
    class Meta:
        model = TESSModel
        fields = '__all__'
        widgets = {
            'pl_orbper': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.001, 'min': 0, 'placeholder': 'e.g., 12.34'}),
            'pl_trandurh': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.001, 'min': 0, 'placeholder': 'e.g., 3.21'}),
            'pl_trandeperr1': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.0001, 'placeholder': 'e.g., 0.0012'}),
            'pl_trandep': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.0001, 'min': 0, 'placeholder': 'e.g., 0.0021'}),
            'pl_rade': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.1, 'min': 0, 'placeholder': 'e.g., 1.2'}),
            'pl_eqt': forms.NumberInput(attrs={'class': 'glass-input', 'step': 1, 'min': 0, 'placeholder': 'e.g., 800'}),
            'st_teff': forms.NumberInput(attrs={'class': 'glass-input', 'step': 50, 'min': 0, 'placeholder': 'e.g., 5400'}),
            'st_logg': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.01, 'placeholder': 'e.g., 4.5'}),
            'st_rad': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.01, 'min': 0, 'placeholder': 'e.g., 0.9'}),
            'st_tmag': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.001, 'placeholder': 'e.g., 10.8'}),
            'st_dist': forms.NumberInput(attrs={'class': 'glass-input', 'step': 0.1, 'min': 0, 'placeholder': 'e.g., 100.0'}),
        }