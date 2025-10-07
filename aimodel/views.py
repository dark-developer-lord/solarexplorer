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
            
            logger.info(f"Received prediction request: mission={mission}, level={level}")
            logger.debug(f"Sample data: {sample_data}")
            
            # Валидация
            if not mission or not sample_data:
                return JsonResponse({'error': 'Missing mission or sample data'}, status=400)
            
            # Проверка допустимых миссий
            if mission not in ['k2', 'kepler', 'tess']:
                return JsonResponse({'error': 'Invalid mission. Must be: k2, kepler, or tess'}, status=400)
            
            # Проверка уровня модели
            if level not in [1, 2]:
                return JsonResponse({'error': 'Invalid level. Must be: 1 or 2'}, status=400)
            
            # Импортируем здесь чтобы избежать циклических импортов
            from .transform_to_log import predict_exoplanet
            
            try:
                # Предсказание
                result = predict_exoplanet(sample_data, mission=mission, level=level)
                
                # Определяем статус и рекомендации
                planet_prob = result['planet_prob']
                if planet_prob > 0.7:
                    status = "HIGH PLANET PROBABILITY"
                    recommendation = "✅ Strong exoplanet candidate - further observation recommended"
                    status_class = "success"
                    icon = "🪐"
                elif planet_prob > 0.5:
                    status = "LIKELY PLANET"
                    recommendation = "⚠️ Promising candidate - additional verification needed"
                    status_class = "warning"
                    icon = "🌍"
                else:
                    status = "LOW PLANET PROBABILITY"
                    recommendation = "❌ Likely false positive - consider alternative explanations"
                    status_class = "error"
                    icon = "⭐"
                
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
                        'Value': f"{float(value):.6f}" if isinstance(value, (int, float)) else str(value),
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
                    "icon": icon,
                    "dataframe_html": df.to_html(classes='result-table', index=False, escape=False)
                }
                
                logger.info(f"Prediction successful: {mission} level {level} - planet_prob: {result['planet_prob']:.4f}")
                return JsonResponse(response_data)
                
            except FileNotFoundError as e:
                logger.error(f"Model file not found: {str(e)}")
                return JsonResponse({'error': f'Model file not found: {str(e)}'}, status=500)
            except Exception as e:
                logger.error(f"Prediction error in ML model: {str(e)}")
                return JsonResponse({'error': f'ML model error: {str(e)}'}, status=500)
            
        except json.JSONDecodeError:
            logger.error("Invalid JSON in request")
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            logger.error(f"Request processing error: {str(e)}")
            import traceback
            traceback.print_exc()
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Only POST requests allowed'}, status=405)