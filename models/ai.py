from transformers import pipeline
import os

# Инициализация модели сентимента (русский язык)
SENTIMENT_MODEL = None

def get_sentiment_model():
    """Загрузить модель сентимента"""
    global SENTIMENT_MODEL
    if SENTIMENT_MODEL is None:
        try:
            # Используем мультиязычную модель
            SENTIMENT_MODEL = pipeline(
                "sentiment-analysis",
                model="bhadresh-savani/bert-base-indonesian-positional-sentiment-analysis",
                return_all_scores=False
            )
        except:
            # Fallback на простую эвристику
            SENTIMENT_MODEL = "fallback"
    return SENTIMENT_MODEL

def analyze_sentiment(text):
    """Анализировать сентимент текста"""
    model = get_sentiment_model()
    
    if model == "fallback":
        return fallback_sentiment(text)
    
    try:
        result = model(text[:512])[0]  # Ограничение длины
        label = result['label'].lower()
        score = result['score']
        
        if 'neg' in label:
            return 'negative', score
        elif 'pos' in label:
            return 'positive', score
        else:
            return 'neutral', score
    except:
        return fallback_sentiment(text)

def fallback_sentiment(text):
    """Простая эвристика для сентимента"""
    text_lower = text.lower()
    
    negative_words = [
        'плохо', 'грустно', 'трудно', 'страшно', 'не понимаю',
        'одиноко', 'хочу уйти', 'бросаю', 'не хочу', 'ужасно',
        'проблема', 'злой', 'разочарован', 'устал', 'не нравится'
    ]
    
    positive_words = [
        'хорошо', 'отлично', 'круто', 'классно', 'рад', 'радостно',
        'понравилось', 'легко', 'увлекательно', 'интересно', 'супер'
    ]
    
    negative_count = sum(1 for word in negative_words if word in text_lower)
    positive_count = sum(1 for word in positive_words if word in text_lower)
    
    if negative_count > positive_count:
        return 'negative', 0.7
    elif positive_count > negative_count:
        return 'positive', 0.7
    else:
        return 'neutral', 0.5

def check_alert_triggers(text, mood_score=None):
    """Проверить триггеры для алертов"""
    triggers = []
    text_lower = text.lower()
    
    # Триггерные слова
    trigger_words = [
        'не понимаю', 'трудно', 'страшно', 'одиноко', 
        'бросаю', 'не хочу', 'хочу уйти', 'плохо'
    ]
    
    for word in trigger_words:
        if word in text_lower:
            triggers.append(f"Триггерное слово: '{word}'")
            break
    
    # Низкое настроение
    if mood_score is not None and mood_score <= 2:
        triggers.append(f"Низкое настроение: {mood_score}/5")
    
    return triggers
