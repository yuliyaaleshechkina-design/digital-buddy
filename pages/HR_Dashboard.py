import streamlit as st
from utils import database
import plotly.express as px
import pandas as pd
from datetime import datetime

def render_dashboard():
    """Рендеринг HR дашборда"""
    st.title("📊 HR Дашборд")
    
    try:
        # Сводка
        summary = database.get_dashboard_summary()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("👥 Новичков", summary['total_newcomers'])
        with col2:
            st.metric("🚨 Активных алертов", summary['active_alerts'])
        with col3:
            st.metric("😊 Среднее настроение", summary['avg_mood'], delta_color="normal")
        
        st.markdown("---")
        
        # Список новичков
        st.subheader("📋 Список новичков")
        newcomers = database.get_all_newcomers()
        
        if newcomers:
            df = pd.DataFrame([
                {
                    "Имя": n['name'],
                    "Должность": n['position'],
                    "Отдел": n['department'],
                    "Дата выхода": n['start_date'],
                    "Ментор": n['mentor_name'] or '-'
                }
                for n in newcomers
            ])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Пока нет активных новичков. Добавь первого через 'Добавить новичка'!")
        
        st.markdown("---")
        
        # График настроения (пример)
        st.subheader("📈 Тренд настроения")
        
        if newcomers:
            sample_data = {
                'Дата': [datetime.now().strftime('%Y-%m-%d') for _ in range(5)],
                'Настроение': [4, 4.2, 3.8, 4.1, 4.3]
            }
            fig = px.line(
                sample_data, 
                x='Дата', 
                y='Настроение',
                title='Среднее настроение по компании',
                markers=True
            )
            fig.update_yaxes(range=[0, 5])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Нет данных о настроении")
        
        st.markdown("---")
        
        # Алерты
        st.subheader("🚨 Активные алерты")
        alerts = database.get_active_alerts()
        
        if alerts:
            for alert in alerts:
                with st.container():
                    st.error(f"**{alert['newcomer_name']}** - {alert['reason']}")
                    if st.button(f"Разрешить #{alert['id']}", key=f"resolve_{alert['id']}"):
                        database.resolve_alert(alert['id'])
                        st.rerun()
        else:
            st.success("Нет активных алертов! 🎉")
            
    except Exception as e:
        st.error(f"Ошибка: {str(e)}")
        st.info("Попробуй обновить страницу или проверь консоль")
