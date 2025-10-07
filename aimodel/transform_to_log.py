import os
import numpy as np
import pandas as pd
import joblib


# === 1. Feature transformation ===
def transform_features(sample_dict: dict, mission: str) -> pd.DataFrame:
    df = pd.DataFrame([sample_dict])
    mission = mission.lower()

    # === K2 ===
    if mission == "k2":
        df["log_pl_orbper"] = np.log1p(df["pl_orbper"])
        df["log_pl_trandur"] = np.log1p(df["pl_trandur"])
        df["log_pl_rade"] = np.log1p(df["pl_rade"])
        df["log_pl_ratror"] = np.log1p(df["pl_ratror"])
        df["log_sy_dist"] = np.log1p(df["sy_dist"])
        df["log_abs_sy_pmra"] = np.log1p(df["sy_pmra"].abs())
        df["log_abs_sy_pmdec"] = np.log1p(df["sy_pmdec"].abs())

        cols = [
            'pl_orbper', 'pl_trandur', 'pl_rade', 'pl_ratror',
            'st_teff', 'st_rad', 'sy_pmra', 'sy_pmdec', 'sy_dist',
            'sy_gaiamag', 'sy_tmag', 'sy_kepmag',
            'log_pl_orbper', 'log_pl_trandur', 'log_pl_rade',
            'log_pl_ratror', 'log_sy_dist', 'log_abs_sy_pmra',
            'log_abs_sy_pmdec'
        ]
        return df.reindex(columns=cols, fill_value=np.nan)

    # === Kepler ===
    elif mission == "kepler":
        df["log_koi_period"] = np.log1p(df["koi_period"])
        df["log_koi_depth"] = np.log1p(df["koi_depth"])
        df["log_koi_dor"] = np.log1p(df["koi_dor"])
        df["log_koi_ror"] = np.log1p(df["koi_ror"])
        df["log_koi_prad"] = np.log1p(df["koi_prad"])
        df["log_koi_model_snr"] = np.log1p(df["koi_model_snr"])
        df["log_koi_max_sngle_ev"] = np.log1p(df["koi_max_sngle_ev"])
        df["log_koi_num_transits"] = np.log1p(df["koi_num_transits"])

        cols = [
            'koi_period', 'koi_duration', 'koi_depth', 'koi_ror', 'koi_dor',
            'koi_incl', 'koi_impact', 'koi_prad', 'koi_sma', 'koi_teq',
            'koi_insol', 'koi_model_snr', 'koi_num_transits', 'koi_max_sngle_ev',
            'koi_steff', 'koi_slogg', 'koi_smet', 'koi_srad', 'koi_smass',
            'koi_srho', 'koi_kepmag', 'koi_gmag', 'koi_rmag', 'koi_imag',
            'koi_zmag', 'koi_jmag', 'koi_hmag', 'koi_kmag',
            'log_koi_period', 'log_koi_depth', 'log_koi_dor',
            'log_koi_ror', 'log_koi_prad', 'log_koi_model_snr',
            'log_koi_max_sngle_ev', 'log_koi_num_transits'
        ]
        return df.reindex(columns=cols, fill_value=np.nan)

    # === TESS ===
    elif mission in ["tess", "tes"]:
        df["log_pl_orbper"] = np.log1p(df["pl_orbper"])
        df["log_pl_trandeperr1"] = np.log1p(df["pl_trandeperr1"].abs())
        df["log_st_teff"] = np.log1p(df["st_teff"])
        df["log_st_logg"] = np.log1p(df["st_logg"])

        cols = [
            'pl_orbper', 'pl_trandurh', 'pl_trandeperr1', 'pl_trandep',
            'pl_rade', 'pl_eqt', 'st_teff', 'st_logg', 'st_rad',
            'st_tmag', 'st_dist', 'log_pl_orbper', 'log_pl_trandeperr1',
            'log_st_teff', 'log_st_logg'
        ]
        return df.reindex(columns=cols, fill_value=np.nan)

    else:
        raise ValueError(f"Неизвестная миссия: {mission}")


# === 2. Трансформация + стандартизация ===
def transform_and_scale(sample_dict: dict, mission: str, level: int, base_dir="models_pkl") -> pd.DataFrame:
    mission = mission.lower()
    prefix = "tess" if mission == "tes" else mission

    scaler_path = os.path.join(base_dir, mission, f"{prefix}_scaler_lvl{level}.pkl")
    if not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Скейлер не найден: {scaler_path}")

    X = transform_features(sample_dict, prefix)
    scaler = joblib.load(scaler_path)

    X_scaled = pd.DataFrame(
        scaler.transform(X.fillna(0)),
        columns=X.columns
    )
    return X_scaled


# === 3. Полный пайплайн: трансформация → стандартизация → предсказание ===
def predict_exoplanet(sample_dict: dict, mission: str, level: int, base_dir="models_pkl") -> dict:
    mission = mission.lower()
    prefix = "tess" if mission == "tes" else mission

    model_path = os.path.join(base_dir, mission, f"{prefix}_model_lvl{level}.cbm")
    scaler_path = os.path.join(base_dir, mission, f"{prefix}_scaler_lvl{level}.pkl")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Модель не найдена: {model_path}")
    if not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Скейлер не найден: {scaler_path}")

    X_scaled = transform_and_scale(sample_dict, mission, level, base_dir)
    model = joblib.load(model_path)
    proba = model.predict_proba(X_scaled)[0]

    result = {
        "mission": mission,
        "planet_prob": float(proba[1]),
        "non_planet_prob": float(proba[0])
    }

    print(f"\n🪐 Миссия: {mission.upper()} | Уровень: {level}")
    print(f"Вероятность планеты: {result['planet_prob']:.4f}")
    print(f"Вероятность не-планеты: {result['non_planet_prob']:.4f}")
    return result


# === Пример запуска для всех миссий ===
if __name__ == "__main__":
    samples = {
        "k2": {
            "pl_orbper": 41.688644,
            "pl_trandur": 2.3,
            "pl_rade": 2.355,
            "pl_ratror": 0.022,
            "st_teff": 5703.0,
            "st_rad": 0.95,
            "sy_pmra": 36.5,
            "sy_pmdec": -51.3,
            "sy_dist": 179.46,
            "sy_gaiamag": 10.86,
            "sy_tmag": 10.40,
            "sy_kepmag": 11.04,
        },

        "kepler": {
            "koi_period": 3.45,
            "koi_duration": 2.4,
            "koi_depth": 400.0,
            "koi_ror": 0.02,
            "koi_dor": 25.0,
            "koi_incl": 89.5,
            "koi_impact": 0.3,
            "koi_prad": 1.5,
            "koi_sma": 0.05,
            "koi_teq": 1200.0,
            "koi_insol": 1800.0,
            "koi_model_snr": 25.0,
            "koi_num_transits": 15,
            "koi_max_sngle_ev": 100.0,
            "koi_steff": 5800,
            "koi_slogg": 4.4,
            "koi_smet": 0.1,
            "koi_srad": 1.0,
            "koi_smass": 1.0,
            "koi_srho": 1.2,
            "koi_kepmag": 12.3,
            "koi_gmag": 13.0,
            "koi_rmag": 12.8,
            "koi_imag": 12.7,
            "koi_zmag": 12.5,
            "koi_jmag": 11.2,
            "koi_hmag": 11.0,
            "koi_kmag": 10.8,
        },

        "tess": {
            "pl_orbper": 12.34,
            "pl_trandurh": 3.21,
            "pl_trandeperr1": 0.0012,
            "pl_trandep": 0.0021,
            "pl_rade": 1.2,
            "pl_eqt": 800,
            "st_teff": 5400,
            "st_logg": 4.5,
            "st_rad": 0.9,
            "st_tmag": 10.8,
            "st_dist": 100.0,
        }
    }

    results = []
    for mission, sample in samples.items():
        result = predict_exoplanet(sample, mission=mission, level=1)
        results.append(result)

    df = pd.DataFrame(results)
    print("\n===Сводная таблица ===")
    print(df.to_string(index=False))
