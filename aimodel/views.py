# aimodel/views.py
import json
import logging
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie

logger = logging.getLogger(__name__)

@ensure_csrf_cookie
def exoplanet_predictor(request):
    """Главная страница предсказания экзопланет"""
    from .forms import KeplerForm, TESSForm, K2Form
    
    kepler_form = KeplerForm()
    tess_form = TESSForm()
    k2_form = K2Form()
    
    context = {
        'kepler_form': kepler_form,
        'tess_form': tess_form,
        'k2_form': k2_form,
    }
    return render(request, 'hackathon/exoplanet_predictor.html', context)

@csrf_exempt
def predict_exoplanet_api(request):
    """API для предсказания экзопланет"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            mission = data.get('mission')
            sample_data = data.get('sample_data')
            level = data.get('level', 1)
            
            print(f"Received request: mission={mission}, level={level}")
            
            # Валидация
            if not mission or not sample_data:
                return JsonResponse({'error': 'Missing mission or sample data'}, status=400)
            
            # Импортируем здесь чтобы избежать циклических импортов
            from .transform_to_log import predict_exoplanet
            
            # Предсказание
            result = predict_exoplanet(sample_data, mission=mission, level=level)
            
            # Определяем статус и рекомендации
            planet_prob = result['planet_prob']
            if planet_prob > 0.7:
                status = "HIGH PLANET PROBABILITY"
                recommendation = "✅ Strong exoplanet candidate"
                status_class = "success"
            elif planet_prob > 0.5:
                status = "LIKELY PLANET"
                recommendation = "⚠️ Requires additional verification"
                status_class = "warning"
            else:
                status = "LOW PLANET PROBABILITY"
                recommendation = "❌ Possible false positive"
                status_class = "error"
            
            # Создаем DataFrame с результатами
            df_data = []
            
            # Добавляем основные результаты
            df_data.append({
                'Parameter': 'Planet Probability',
                'Value': f"{result['planet_prob']:.4f}",
                'Type': 'Result'
            })
            df_data.append({
                'Parameter': 'Non-Planet Probability', 
                'Value': f"{result['non_planet_prob']:.4f}",
                'Type': 'Result'
            })
            
            # Добавляем входные параметры
            for key, value in sample_data.items():
                df_data.append({
                    'Parameter': key,
                    'Value': str(value),
                    'Type': 'Input Parameter'
                })
            
            df = pd.DataFrame(df_data)
            
            response_data = {
                "mission": mission.upper(),
                "level": level,
                "planet_prob": float(result['planet_prob']),
                "non_planet_prob": float(result['non_planet_prob']),
                "status": status,
                "recommendation": recommendation,
                "status_class": status_class,
                "dataframe_html": df.to_html(classes='table table-striped', index=False, escape=False)
            }
            
            return JsonResponse(response_data)
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            import traceback
            traceback.print_exc()  # Печатаем полный traceback в консоль
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Only POST requests allowed'}, status=405)