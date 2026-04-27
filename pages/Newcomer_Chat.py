import streamlit as st
from utils.database import (
    get_newcomer, add_mood_checkin, get_mood_history,
    create_session, get_messages, add_message
)
from models.ai import analyze_sentiment, check_alert_triggers
from datetime import datetime

def render_chat():
    """Рендеринг чата для новичка"""
    st.title("💬 Чат с Бадди")
    
    # Инициализация сессии
    if 'newcomer_id' not in st.session_state:
        # Простая аутентификация - ввод ID
        newcomer_id = st.text_input("Введите ваш ID новичка:", placeholder="NB-20260401-0001")
        if newcomer_id:
            newcomer = get_newcomer(newcomer_id)
            if newcomer:
                st.session_state['newcomer_id'] = newcomer_id
                st.session_state['newcomer_name'] = newcomer['name']
                create_session(newcomer_id)
                st.rerun()
            else:
                st.error("Новичок не найден. Обратитесь к HR.")
        return
    
    # Приветствие
    newcomer_id = st.session_state['newcomer_id']
    newcomer_name = st.session_state.get('newcomer_name', 'Новичок')
    
    st.subheader(f"Привет, {newcomer_name}! 👋")
    st.write("Я твой AI-бадди. Задавай вопросы, делись впечатлениями!")
    
    # Чат история
    if 'messages' not in st.session_state:
        st.session_state['messages'] = get_messages(newcomer_id)
    
    # Отображение сообщений
    for msg in reversed(st.session_state['messages'][-20:]):
        with st.chat_message(msg['sender']):
            st.write(msg['message'])
    
    # Ввод сообщения
    if prompt := st.chat_input("Напиши сообщение..."):
        # Добавить сообщение пользователя
        add_message(newcomer_id, prompt, 'user')
        st.session_state['messages'].append({
            'message': prompt,
            'sender': 'user',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        # Анализ сентимента
        sentiment, confidence = analyze_sentiment(prompt)
        triggers = check_alert_triggers(prompt)
        
        if triggers:
            for trigger in triggers:
                add_message(newcomer_id, f"[Система: {trigger}]", 'system')
        
        # Генерация ответа бадди
        bot_response = generate_bot_response(prompt, newcomer_name)
        add_message(newcomer_id, bot_response, 'buddy')
        st.session_state['messages'].append({
            'message': bot_response,
            'sender': 'buddy',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        st.rerun()

def generate_bot_response(user_message, newcomer_name):
    """Генерация ответа от бадди"""
    message_lower = user_message.lower()
    
    # Простые шаблоны ответов (в реальности - AI модель)
    responses = {
        'привет': f"Привет, {newcomer_name}! 👋 Как твой день проходит?",
        'как дела': "У меня всё отлично! А у тебя как? Есть какие-то вопросы или трудности?",
        'что делаешь': "Я здесь, чтобы помочь тебе с адаптацией! Могу ответить на вопросы, поддержать или просто поболтать 😊",
        'трудно': "Понимаю, адаптация может быть сложной! 😊 Давай разберём, что именно вызывает трудности? Я помогу!",
        'вопрос': "Конечно! Задавай свой вопрос, я постараюсь помочь 🤗",
        'спасибо': "Всегда рад помочь! 😊 Если ещё что-то нужно - обращайся!",
        'устал': "Понимаю, первые дни могут быть утомительными! Не забывай делать перерывы. Всё получится! 💪",
        'одиноко': "Понимаю твои чувства 😊 Попробуй познакомиться с коллегами, пригласить на кофе! Команда всегда готова помочь!",
    }
    
    # Поиск совпадений
    for keyword, response in responses.items():
        if keyword in message_lower:
            return response
    
    # Стандартный ответ
    default_responses = [
        f"{newcomer_name}, понимаю! Расскажи подробнее, что тебя беспокоит? 😊",
        "Интересный вопрос! Давай обсудим это подробнее 🤗",
        "Спасибо, что поделился! Я здесь, чтобы поддержать тебя! 💪",
        "Понимаю! Если есть вопросы - спрашивай, помогу чем могу! 😊",
    ]
    
    import random
    return random.choice(default_responses)

def render_mood_checkin():
    """Рендеринга проверки настроения"""
    st.title("😊 Проверка Настроения")
    
    if 'newcomer_id' not in st.session_state:
        st.warning("Сначала войди в чат!")
        return
    
    newcomer_id = st.session_state['newcomer_id']
    
    st.write("Как ты себя чувствуешь сегодня?")
    
    # Шкала настроения
    mood = st.slider(
        "Оцени своё настроение:",
        min_value=1,
        max_value=5,
        value=3,
        step=1
    )
    
    mood_labels = {
        1: "😞 Очень плохо",
        2: "😕 Плохо",
        3: "😐 Нормально",
        4: "🙂 Хорошо",
        5: "😀 Отлично"
    }
    
    st.write(mood_labels[mood])
    
    feedback = st.text_area("Если хочешь, расскажи подробнее:")
    
    if st.button("Отправить"):
        add_mood_checkin(newcomer_id, mood, feedback)
        st.success("Спасибо! Твоё настроение записано! 💖")
        
        # Проверка на алерт
        triggers = check_alert_triggers(feedback, mood)
        if triggers:
            st.warning("Обрати внимание: некоторые фразы могут указывать на трудности.")
    
    st.markdown("---")
    
    # История настроения
    st.subheader("📊 Моя история настроения")
    history = get_mood_history(newcomer_id, days=30)
    
    if history:
        for entry in reversed(history[-10:]):
            st.write(f"**{entry['created_at'][:10]}**: {'⭐' * entry['mood_score']}")
            if entry['feedback']:
                st.write(f"_{entry['feedback']}_")
    else:
        st.info("Пока нет записей о настроении")
