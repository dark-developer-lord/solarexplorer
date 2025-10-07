from django.db import models

class K2Model(models.Model):
    pl_orbper = models.FloatField(verbose_name="Orbital Period (days)")
    pl_trandur = models.FloatField(verbose_name="Transit Duration (days)")
    pl_rade = models.FloatField(verbose_name="Planet Radius (Earth radii)")
    pl_ratror = models.FloatField(verbose_name="Planet to Star Radius Ratio")  # Изменил на pl_ratror
    st_teff = models.FloatField(verbose_name="Stellar Effective Temperature (K)")
    st_rad = models.FloatField(verbose_name="Stellar Radius (Solar radii)")
    sy_pmra = models.FloatField(verbose_name="Proper Motion RA (mas/yr)")  # Добавил
    sy_pmdec = models.FloatField(verbose_name="Proper Motion Dec (mas/yr)")  # Добавил
    sy_dist = models.FloatField(verbose_name="Distance (pc)")  # Добавил
    sy_gaiamag = models.FloatField(verbose_name="Gaia Magnitude")  # Добавил
    sy_tmag = models.FloatField(verbose_name="TESS Magnitude")  # Добавил
    sy_kepmag = models.FloatField(verbose_name="Kepler Magnitude")  # Добавил

    class Meta:
        verbose_name = "K2 Mission Data"
        verbose_name_plural = "K2 Mission Data"

    def __str__(self):
        return f"K2 - Period: {self.pl_orbper} days"

class KeplerModel(models.Model):
    koi_period = models.FloatField(verbose_name="Orbital Period (days)")
    koi_duration = models.FloatField(verbose_name="Transit Duration (hours)")
    koi_depth = models.FloatField(verbose_name="Transit Depth (ppm)")
    koi_ror = models.FloatField(verbose_name="Planet-Star Radius Ratio")
    koi_dor = models.FloatField(verbose_name="Planet-Star Distance Ratio")
    koi_incl = models.FloatField(verbose_name="Inclination (degrees)")
    koi_impact = models.FloatField(verbose_name="Impact Parameter")
    koi_prad = models.FloatField(verbose_name="Planet Radius (Earth radii)")
    koi_sma = models.FloatField(verbose_name="Semi-Major Axis (AU)")
    koi_teq = models.FloatField(verbose_name="Equilibrium Temperature (K)")
    koi_insol = models.FloatField(verbose_name="Insolation Flux (Earth units)")
    koi_model_snr = models.FloatField(verbose_name="Model Signal-to-Noise Ratio")
    koi_num_transits = models.IntegerField(verbose_name="Number of Transits")
    koi_max_sngle_ev = models.FloatField(verbose_name="Maximum Single Event Statistic")
    koi_steff = models.FloatField(verbose_name="Stellar Effective Temperature (K)")
    koi_slogg = models.FloatField(verbose_name="Stellar Surface Gravity (log10(cm/s²))")
    koi_smet = models.FloatField(verbose_name="Stellar Metallicity")
    koi_srad = models.FloatField(verbose_name="Stellar Radius (Solar radii)")
    koi_smass = models.FloatField(verbose_name="Stellar Mass (Solar masses)")
    koi_srho = models.FloatField(verbose_name="Stellar Density (g/cm³)")
    koi_kepmag = models.FloatField(verbose_name="Kepler Magnitude")
    koi_gmag = models.FloatField(verbose_name="Gaia G Magnitude")
    koi_rmag = models.FloatField(verbose_name="SDSS r Magnitude")
    koi_imag = models.FloatField(verbose_name="SDSS i Magnitude")
    koi_zmag = models.FloatField(verbose_name="SDSS z Magnitude")
    koi_jmag = models.FloatField(verbose_name="2MASS J Magnitude")
    koi_hmag = models.FloatField(verbose_name="2MASS H Magnitude")
    koi_kmag = models.FloatField(verbose_name="2MASS K Magnitude")

    class Meta:
        verbose_name = "Kepler Mission Data"
        verbose_name_plural = "Kepler Mission Data"

    def __str__(self):
        return f"Kepler - Period: {self.koi_period} days"

class TESSModel(models.Model):
    pl_orbper = models.FloatField(verbose_name="Orbital Period (days)")
    pl_trandurh = models.FloatField(verbose_name="Transit Duration (hours)")
    pl_trandeperr1 = models.FloatField(verbose_name="Transit Depth Error")
    pl_trandep = models.FloatField(verbose_name="Transit Depth")
    pl_rade = models.FloatField(verbose_name="Planet Radius (Earth radii)")
    pl_eqt = models.FloatField(verbose_name="Equilibrium Temperature (K)")
    st_teff = models.FloatField(verbose_name="Stellar Effective Temperature (K)")
    st_logg = models.FloatField(verbose_name="Stellar Surface Gravity (log10(cm/s²))")
    st_rad = models.FloatField(verbose_name="Stellar Radius (Solar radii)")
    st_tmag = models.FloatField(verbose_name="TESS Magnitude")
    st_dist = models.FloatField(verbose_name="Distance to Star (pc)")

    class Meta:
        verbose_name = "TESS Mission Data"
        verbose_name_plural = "TESS Mission Data"

    def __str__(self):
        return f"TESS - Period: {self.pl_orbper} days"

class DF(models.Model):
    mission = models.CharField(max_length=10)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Data Frame"
        verbose_name_plural = "Data Frames"
        
    def __str__(self):
        return f"{self.mission} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"