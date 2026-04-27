import streamlit as st
from utils.database import get_all_newcomers, add_newcomer, init_db

def render_add_newcomer():
    """Рендеринг страницы добавления новичка"""
    st.title("➕ Добавить Новичка")
    
    st.write("Добавьте нового сотрудника в систему адаптации")
    
    with st.form("newcomer_form"):
        name = st.text_input("Имя и фамилия *")
        position = st.text_input("Должность *")
        department = st.text_input("Отдел *")
        start_date = st.date_input("Дата выхода *")
        mentor = st.text_input("Имя ментора (опционально)")
        
        submitted = st.form_submit_button("Добавить")
        
        if submitted:
            if name and position and department and start_date:
                newcomer_id = add_newcomer(
                    name=name,
                    position=position,
                    department=department,
                    start_date=start_date.strftime('%Y-%m-%d'),
                    mentor_name=mentor
                )
                
                if newcomer_id:
                    st.success(f"✅ Новичок добавлен! ID: {newcomer_id}")
                    st.info(f"Покажи этот ID новичку для доступа к чату")
                else:
                    st.error("❌ Ошибка: возможно, такой новичок уже добавлен")
            else:
                st.error("❌ Пожалуйста, заполните все обязательные поля *")
    
    st.markdown("---")
    
    # Показ последних добавленных
    st.subheader("📋 Последние добавленные")
    newcomers = get_all_newcomers()[:5]
    
    if newcomers:
        for n in newcomers:
            st.write(f"**{n['name']}** - {n['position']} ({n['department']})")
            st.write(f"  ID: {n['newcomer_id']} | Дата: {n['start_date']}")
            st.write("---")
    else:
        st.info("Пока нет добавленных новичков")
