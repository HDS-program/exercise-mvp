import streamlit as st
from services.auth_service import get_current_user
from services.routine_service import get_user_routines, get_routine_items

st.title("📋 루틴 조회")

# 로그인 확인
user = get_current_user()
if not user:
    st.warning("로그인이 필요합니다.")
    st.stop()

try:
    user_id = user.id
    routines = get_user_routines(user_id)
    
    if routines:
        st.subheader(f"총 {len(routines)}개의 루틴")
        
        # 루틴 선택
        routine_names = [r.get("routine_name", "Unknown") for r in routines]
        selected_routine_name = st.selectbox("루틴 선택", routine_names)
        
        # 선택된 루틴 정보
        selected_routine = next(
            (r for r in routines if r.get("routine_name") == selected_routine_name),
            None
        )
        
        if selected_routine:
            routine_id = selected_routine.get("id")
            st.write(f"**루틴명:** {selected_routine.get('routine_name')}")
            st.write(f"**활성화:** {'활성' if selected_routine.get('is_active') else '비활성'}")
            
            # 루틴 항목 조회
            st.subheader("포함된 운동")
            routine_items = get_routine_items(routine_id)
            
            if routine_items:
                for idx, item in enumerate(routine_items, 1):
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.write(f"**{idx}. {item.get('exercises', {}).get('exercise_name', 'N/A')}**")
                    with col2:
                        st.write(f"세트: {item.get('target_sets')}")
                    with col3:
                        st.write(f"반복: {item.get('target_reps')}")
                    with col4:
                        st.write(f"중량: {item.get('target_weight')}kg")
                    st.divider()
            else:
                st.info("이 루틴에 포함된 운동이 없습니다.")
    else:
        st.info("등록된 루틴이 없습니다.")
        
except Exception as e:
    st.error(f"루틴 정보를 불러오는 중 오류가 발생했습니다: {str(e)}")
