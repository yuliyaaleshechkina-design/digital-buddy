import streamlit as st
from utils.database import get_dashboard_summary

def main():
    """Главная страница"""
    st.set_page_config(
        page_title="Цифровой Бадди",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Цифровой Бадди")
    st.markdown("---")
    
    # Выбор роли
    st.header("Выберите вашу роль:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👤 Я Новичок", use_container_width=True, type="primary"):
            st.session_state['role'] = 'newcomer'
            st.switch_page("pages/Newcomer_Chat.py")
    
    with col2:
        if st.button("👔 Я HR", use_container_width=True, type="primary"):
            st.session_state['role'] = 'hr'
            st.switch_page("pages/HR_Dashboard.py")
    
    st.markdown("---")
    
    # Информация о системе
    st.header("📖 О системе")
    
    st.subheader("💬 Что это?")
    st.write("""
    **Цифровой Бадди** — AI-помощник, который помогает новичкам адаптироваться 
    в первые 90 дней работы.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎯 Для новичков")
        st.write("""
        - Чат с AI-бадди
        - Ответы на вопросы
        - Поддержка и советы
        """)
    
    with col2:
        st.markdown("### 📊 Для HR")
        st.write("""
        - Дашборд со статусами
        - Отслеживание настроения
        - Ранние алерты о проблемах
        """)
    
    with col3:
        st.markdown("### 🚀 Преимущества")
        st.write("""
        - Всегда доступен
        - Дружелюбный тон
        - Конфиденциально
        """)
    
    st.markdown("---")
    
    # Быстрая статистика
    summary = get_dashboard_summary()
    st.subheader("📈 Общая статистика")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Активных новичков", summary['total_newcomers'])
    
    with col2:
        st.metric("Активных алертов", summary['active_alerts'])
    
    with col3:
        st.metric("Среднее настроение", f"{summary['avg_mood']}/5")

if __name__ == "__main__":
    main()
