import streamlit as st
from datetime import datetime
from services.auth_service import get_current_user
from services.recovery_service import (
    get_sessions_without_recovery,
    create_recovery_record,
    create_muscle_recovery_record,
    check_recovery_exists
)
from services.exercise_service import get_muscle_groups
from services.workout_service import get_user_recent_workouts

st.title("🩹 회복 기록 입력")

# 로그인 확인
user = get_current_user()
if not user:
    st.warning("로그인이 필요합니다.")
    st.stop()

user_id = user.id

try:
    # 회복 기록이 필요한 운동 세션 조회
    st.subheader("1️⃣ 회복 기록 대상 운동 선택")
    
    sessions_without_recovery = get_sessions_without_recovery(user_id)
    
    if not sessions_without_recovery:
        st.info("회복 기록을 입력할 운동 기록이 없습니다.")
        st.stop()
    
    # 세션 선택
    session_options = {
        f"{s.get('workout_date')} - {s.get('routines', {}).get('routine_name', 'Unknown')}": s.get('id')
        for s in sessions_without_recovery
    }
    
    selected_session_label = st.selectbox("운동 선택", list(session_options.keys()))
    selected_session_id = session_options[selected_session_label]
    
    # 회복 기록 날짜
    st.subheader("2️⃣ 회복 상태 기록")
    col1, col2 = st.columns(2)
    
    with col1:
        recovery_date = st.date_input("회복 기록 날짜", datetime.now())
    
    with col2:
        st.write("")  # 간격
    
    # 전체 피로도 및 컨디션
    col1, col2 = st.columns(2)
    
    with col1:
        overall_fatigue = st.slider("전체 피로도 (1-10)", 1, 10, 5)
    
    with col2:
        overall_condition = st.slider("전체 컨디션 (1-10)", 1, 10, 5)
    
    # 부위별 회복 상태
    st.subheader("3️⃣ 부위별 회복 상태")
    
    muscle_groups = get_muscle_groups()
    if not muscle_groups:
        st.error("근육 부위 데이터를 불러올 수 없습니다.")
        st.stop()
    
    muscle_recovery_data = {}
    for muscle in muscle_groups:
        muscle_id = muscle.get("id")
        muscle_name = muscle.get("muscle_name", "Unknown")
        
        st.write(f"**{muscle_name}**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            soreness = st.slider(
                f"{muscle_name} 근육통 (0-10)",
                0, 10, 3,
                key=f"soreness_{muscle_id}"
            )
        
        with col2:
            pain = st.slider(
                f"{muscle_name} 통증 (0-10)",
                0, 10, 0,
                key=f"pain_{muscle_id}"
            )
        
        with col3:
            recovery_status = st.slider(
                f"{muscle_name} 회복 정도 (0-10)",
                0, 10, 5,
                key=f"recovery_{muscle_id}"
            )
        
        muscle_recovery_data[muscle_id] = {
            "soreness": soreness,
            "pain": pain,
            "recovery_status": recovery_status
        }
        st.divider()
    
    # 메모
    st.subheader("4️⃣ 메모")
    memo = st.text_area("회복 상태에 대한 메모 (선택사항)", "")
    
    # 저장 버튼
    if st.button("회복 기록 저장", type="primary"):
        try:
            # 회복 기록 생성
            recovery_result = create_recovery_record(
                session_id=selected_session_id,
                recovery_date=str(recovery_date),
                overall_fatigue=overall_fatigue,
                overall_condition=overall_condition,
                memo=memo
            )
            
            if not recovery_result['success']:
                st.error(f"회복 기록 생성 실패: {recovery_result['error']}")
                st.stop()
            
            recovery_id = recovery_result['data']['id']
            
            # 부위별 회복 기록 생성
            for muscle_id, data in muscle_recovery_data.items():
                muscle_result = create_muscle_recovery_record(
                    recovery_id=recovery_id,
                    muscle_id=muscle_id,
                    soreness=data['soreness'],
                    pain=data['pain'],
                    recovery_status=data['recovery_status']
                )
                
                if not muscle_result['success']:
                    st.warning(f"부위별 회복 기록 저장 실패: {muscle_result['error']}")
            
            st.success("✅ 회복 기록이 저장되었습니다!")
            st.balloons()
            
        except Exception as e:
            st.error(f"회복 기록 저장 중 오류가 발생했습니다: {str(e)}")

except Exception as e:
    st.error(f"오류가 발생했습니다: {str(e)}")
