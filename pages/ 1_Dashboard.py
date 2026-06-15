import streamlit as st
from services.auth_service import get_current_user
from services.user_service import get_user_profile
from services.workout_service import get_user_recent_workouts
from services.recovery_service import get_latest_recovery_record, get_muscle_recovery_records
from services.analysis_service import get_latest_analysis_result, get_recommendations_list

st.set_page_config(
    page_title="Dashboard - Exercise MVP",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 대시보드")

# 로그인 확인
user = get_current_user()
if not user:
    st.warning("로그인이 필요합니다.")
    st.stop()

user_id = user.id

try:
    # 사용자 프로필 정보
    user_profile = get_user_profile(user_id)
    
    if user_profile:
        st.write(f"**닉네임:** {user_profile.get('nickname', 'N/A')}")
        st.write(f"**경험 수준:** {user_profile.get('experience_level', 'N/A')}")
        if user_profile.get('goal'):
            st.write(f"**운동 목표:** {user_profile.get('goal')}")
    
    st.divider()
    
    # 상단 요약 카드 영역
    st.subheader("📊 오늘의 요약")
    
    col1, col2, col3 = st.columns(3)
    
    # 최근 운동 정보
    recent_workouts = get_user_recent_workouts(user_id, limit=1)
    
    with col1:
        with st.container(border=True):
            st.write("**최근 운동**")
            if recent_workouts:
                workout = recent_workouts[0]
                st.write(f"날짜: {workout.get('workout_date')}")
                st.write(f"루틴: {workout.get('routines', {}).get('routine_name', 'N/A')}")
            else:
                st.write("아직 기록된 운동이 없습니다.")
    
    # 회복 상태
    latest_recovery = get_latest_recovery_record(user_id)
    
    with col2:
        with st.container(border=True):
            st.write("**회복 상태**")
            if latest_recovery:
                st.write(f"피로도: {latest_recovery.get('overall_fatigue')}/10")
                st.write(f"컨디션: {latest_recovery.get('overall_condition')}/10")
            else:
                st.warning("회복 기록이 없습니다.")
    
    # 분석 결과
    latest_analysis = get_latest_analysis_result(user_id)
    
    with col3:
        with st.container(border=True):
            st.write("**분석 결과**")
            if latest_analysis:
                st.write(f"자극량 점수: {latest_analysis.get('stimulus_score', 'N/A')}")
                st.write(f"효율 점수: {latest_analysis.get('efficiency_score', 'N/A')}")
            else:
                st.info("분석 결과가 없습니다.")
    
    st.divider()
    
    # 중단 영역 - 최근 운동 기록 및 분석
    st.subheader("📈 최근 활동")
    
    tab1, tab2, tab3 = st.tabs(["운동 기록", "회복 기록", "분석 결과"])
    
    with tab1:
        st.write("**최근 운동 세션**")
        recent_workouts = get_user_recent_workouts(user_id, limit=5)
        if recent_workouts:
            for idx, workout in enumerate(recent_workouts, 1):
                with st.container(border=True):
                    st.write(f"{idx}. {workout.get('workout_date')} - {workout.get('routines', {}).get('routine_name', 'N/A')}")
        else:
            st.info("운동 기록이 없습니다.")
    
    with tab2:
        st.write("**최근 회복 기록**")
        latest_recovery = get_latest_recovery_record(user_id)
        if latest_recovery:
            with st.container(border=True):
                st.write(f"**기록 날짜:** {latest_recovery.get('recovery_date')}")
                st.write(f"**전체 피로도:** {latest_recovery.get('overall_fatigue')}/10")
                st.write(f"**전체 컨디션:** {latest_recovery.get('overall_condition')}/10")
                
                if latest_recovery.get('memo'):
                    st.write(f"**메모:** {latest_recovery.get('memo')}")
                
                # 부위별 회복 상태
                recovery_id = latest_recovery.get('id')
                muscle_records = get_muscle_recovery_records(recovery_id)
                
                if muscle_records:
                    st.write("**부위별 회복 상태**")
                    for muscle in muscle_records:
                        muscle_name = muscle.get('muscle_groups', {}).get('muscle_name', 'Unknown')
                        st.write(f"- {muscle_name}: 근육통 {muscle.get('soreness')}/10, 통증 {muscle.get('pain')}/10, 회복 {muscle.get('recovery_status')}/10")
        else:
            st.info("회복 기록이 없습니다.")
    
    with tab3:
        st.write("**최신 분석 결과**")
        latest_analysis = get_latest_analysis_result(user_id)
        if latest_analysis:
            with st.container(border=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("자극량 점수", latest_analysis.get('stimulus_score', 'N/A'))
                with col2:
                    st.metric("효율 점수", latest_analysis.get('efficiency_score', 'N/A'))
                
                if latest_analysis.get('warning_content'):
                    st.warning(f"**경고:** {latest_analysis.get('warning_content')}")
        else:
            st.info("분석 결과가 없습니다.")
    
    st.divider()
    
    # 하단 빠른 이동 영역
    st.subheader("⚡ 빠른 이동")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💪 운동 기록 입력", use_container_width=True):
            st.switch_page("pages/3_Workout_Input.py")
    
    with col2:
        if st.button("🩹 회복 기록 입력", use_container_width=True):
            st.switch_page("pages/4_Recovery_Input.py")
    
    with col3:
        if st.button("📋 루틴 확인", use_container_width=True):
            st.switch_page("pages/5_Routine_View.py")
    
    with col4:
        if st.button("📊 분석 결과 보기", use_container_width=True):
            st.switch_page("pages/6_Analysis_Result.py")

except Exception as e:
    st.error(f"오류가 발생했습니다: {str(e)}")
