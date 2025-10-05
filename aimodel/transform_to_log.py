# aimodel/ml_predictor.py
import os
import numpy as np
import pandas as pd
import joblib
from django.conf import settings

def transform_features(sample_dict: dict, mission: str) -> pd.DataFrame:
    """Преобразование фичей для конкретной миссии"""
    df = pd.DataFrame([sample_dict])
    mission = mission.lower()

    try:
        if mission == "k2":
            # K2 трансформации
            if 'pl_orbper' in df.columns: df["log_pl_orbper"] = np.log1p(df["pl_orbper"])
            if 'pl_trandur' in df.columns: df["log_pl_trandur"] = np.log1p(df["pl_trandur"])
            if 'pl_rade' in df.columns: df["log_pl_rade"] = np.log1p(df["pl_rade"])
            if 'pl_ratror' in df.columns: df["log_pl_ratror"] = np.log1p(df["pl_ratror"])
            if 'sy_dist' in df.columns: df["log_sy_dist"] = np.log1p(df["sy_dist"])
            if 'sy_pmra' in df.columns: df["log_abs_sy_pmra"] = np.log1p(df["sy_pmra"].abs())
            if 'sy_pmdec' in df.columns: df["log_abs_sy_pmdec"] = np.log1p(df["sy_pmdec"].abs())

            cols = [
                'pl_orbper', 'pl_trandur', 'pl_rade', 'pl_ratror',
                'st_teff', 'st_rad', 'sy_pmra', 'sy_pmdec', 'sy_dist',
                'sy_gaiamag', 'sy_tmag', 'sy_kepmag',
                'log_pl_orbper', 'log_pl_trandur', 'log_pl_rade',
                'log_pl_ratror', 'log_sy_dist', 'log_abs_sy_pmra',
                'log_abs_sy_pmdec'
            ]
            # Возвращаем только существующие колонки
            existing_cols = [col for col in cols if col in df.columns]
            return df.reindex(columns=existing_cols, fill_value=0.0)

        elif mission == "kepler":
            # Kepler трансформации
            if 'koi_period' in df.columns: df["log_koi_period"] = np.log1p(df["koi_period"])
            if 'koi_depth' in df.columns: df["log_koi_depth"] = np.log1p(df["koi_depth"])
            if 'koi_dor' in df.columns: df["log_koi_dor"] = np.log1p(df["koi_dor"])
            if 'koi_ror' in df.columns: df["log_koi_ror"] = np.log1p(df["koi_ror"])
            if 'koi_prad' in df.columns: df["log_koi_prad"] = np.log1p(df["koi_prad"])
            if 'koi_model_snr' in df.columns: df["log_koi_model_snr"] = np.log1p(df["koi_model_snr"])
            if 'koi_max_sngle_ev' in df.columns: df["log_koi_max_sngle_ev"] = np.log1p(df["koi_max_sngle_ev"])
            if 'koi_num_transits' in df.columns: df["log_koi_num_transits"] = np.log1p(df["koi_num_transits"])

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
            existing_cols = [col for col in cols if col in df.columns]
            return df.reindex(columns=existing_cols, fill_value=0.0)

        elif mission in ["tess", "tes"]:
            # TESS трансформации
            if 'pl_orbper' in df.columns: df["log_pl_orbper"] = np.log1p(df["pl_orbper"])
            if 'pl_trandeperr1' in df.columns: df["log_pl_trandeperr1"] = np.log1p(df["pl_trandeperr1"].abs())
            if 'st_teff' in df.columns: df["log_st_teff"] = np.log1p(df["st_teff"])
            if 'st_logg' in df.columns: df["log_st_logg"] = np.log1p(df["st_logg"])

            cols = [
                'pl_orbper', 'pl_trandurh', 'pl_trandeperr1', 'pl_trandep',
                'pl_rade', 'pl_eqt', 'st_teff', 'st_logg', 'st_rad',
                'st_tmag', 'st_dist', 'log_pl_orbper', 'log_pl_trandeperr1',
                'log_st_teff', 'log_st_logg'
            ]
            existing_cols = [col for col in cols if col in df.columns]
            return df.reindex(columns=existing_cols, fill_value=0.0)

        else:
            raise ValueError(f"Unknown mission: {mission}")
    except Exception as e:
        raise ValueError(f"Feature transformation error: {str(e)}")

def find_model_files(base_dir, mission, level):
    """Находит файлы моделей и скейлеров с различными расширениями"""
    mission_dir = os.path.join(base_dir, mission)
    
    if not os.path.exists(mission_dir):
        raise FileNotFoundError(f"Mission directory not found: {mission_dir}")
    
    print(f"Looking in directory: {mission_dir}")
    print(f"Files in directory: {os.listdir(mission_dir)}")
    
    # Возможные шаблоны имен файлов
    model_patterns = [
        f"{mission}_level{level}_model.com",  # Ваш оригинальный формат
        f"{mission}_level{level}_model.pkl",
        f"{mission}_model_lvl{level}.pkl",
        f"{mission}_model_lvl{level}.com",
        f"{mission}_model{level}.pkl",
        f"{mission}_model{level}.com",
    ]
    
    scaler_patterns = [
        f"{mission}_scaler_lvl{level}.pk1",  # Ваш оригинальный формат
        f"{mission}_scaler_lvl{level}.pkl",
        f"{mission}_scaler{level}.pkl",
        f"{mission}_scaler{level}.pk1",
    ]
    
    model_path = None
    scaler_path = None
    
    # Ищем файл модели
    for pattern in model_patterns:
        potential_path = os.path.join(mission_dir, pattern)
        if os.path.exists(potential_path):
            model_path = potential_path
            print(f"Found model: {model_path}")
            break
    
    # Ищем файл скейлера
    for pattern in scaler_patterns:
        potential_path = os.path.join(mission_dir, pattern)
        if os.path.exists(potential_path):
            scaler_path = potential_path
            print(f"Found scaler: {scaler_path}")
            break
    
    if not model_path:
        raise FileNotFoundError(f"Model file not found for {mission} level {level}. Checked patterns: {model_patterns}")
    
    if not scaler_path:
        raise FileNotFoundError(f"Scaler file not found for {mission} level {level}. Checked patterns: {scaler_patterns}")
    
    return model_path, scaler_path

def predict_exoplanet(sample_dict: dict, mission: str, level: int, base_dir=None) -> dict:
    """Основная функция предсказания"""
    if base_dir is None:
        base_dir = os.path.join(settings.BASE_DIR, 'models_pkl')
        
    mission = mission.lower()
    
    try:
        # Исправляем имена файлов в соответствии с вашей структурой
        if mission == "tes":
            mission = "tess"
        
        print(f"Starting prediction for {mission}, level {level}")
        print(f"Base directory: {base_dir}")
        
        # Находим файлы моделей
        model_path, scaler_path = find_model_files(base_dir, mission, level)
        
        # Загружаем скейлер и модель
        print(f"Loading scaler from: {scaler_path}")
        scaler = joblib.load(scaler_path)
        print("Scaler loaded successfully")
        
        print(f"Loading model from: {model_path}")
        model = joblib.load(model_path)
        print("Model loaded successfully")

        # Преобразуем и масштабируем данные
        print("Transforming features...")
        X = transform_features(sample_dict, mission)
        print("Features transformed successfully")
        
        print("Scaling data...")
        X_scaled = pd.DataFrame(scaler.transform(X.fillna(0)), columns=X.columns)
        print("Data scaled successfully")

        # Делаем предсказание
        print("Making prediction...")
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(X_scaled)[0]
            print(f"Prediction probabilities: {proba}")
        else:
            # Если нет predict_proba, создаем фиктивные вероятности
            prediction = model.predict(X_scaled)[0]
            proba = [0.3, 0.7] if prediction == 1 else [0.7, 0.3]
            print(f"Direct prediction: {prediction}, probabilities: {proba}")

        result = {
            "mission": mission,
            "planet_prob": float(proba[1]),
            "non_planet_prob": float(proba[0])
        }
        
        print(f"Prediction completed: {result}")
        return result
        
    except Exception as e:
        print(f"Error in predict_exoplanet: {str(e)}")
        import traceback
        traceback.print_exc()
        raise Exception(f"Prediction error: {str(e)}")