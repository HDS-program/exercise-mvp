import streamlit as st
from services.exercise_service import get_all_exercises

st.title("💪 운동 종목 조회")

try:
    exercises = get_all_exercises()
    
    if exercises:
        st.subheader(f"총 {len(exercises)}개의 운동 종목")
        
        # 검색 기능
        search_term = st.text_input("운동 검색", "")
        
        if search_term:
            exercises = [e for e in exercises if search_term.lower() in e.get("exercise_name", "").lower()]
        
        # 운동 목록 표시
        cols = st.columns(1)
        for exercise in exercises:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{exercise.get('exercise_name', 'N/A')}**")
                    if 'description' in exercise:
                        st.caption(exercise['description'])
                with col2:
                    st.write(f"ID: {exercise.get('id', 'N/A')}")
                st.divider()
    else:
        st.info("등록된 운동이 없습니다.")
        
except Exception as e:
    st.error(f"운동 목록을 불러오는 중 오류가 발생했습니다: {str(e)}")
