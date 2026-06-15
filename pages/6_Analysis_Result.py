import streamlit as st
from services.auth_service import get_current_user
from services.analysis_service import get_latest_analysis_result, get_analysis_history

st.set_page_config(
    page_title="Analysis Result - Exercise MVP",
    page_icon="📊",
    layout="wide"
)

st.title("📊 분석 결과 조회")

# 로그인 확인
user = get_current_user()
if not user:
    st.warning("로그인이 필요합니다.")
    st.stop()

user_id = user.id

try:
    # 최신 분석 결과
    st.subheader("최신 분석 결과")
    
    latest_analysis = get_latest_analysis_result(user_id)
    
    if latest_analysis:
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("자극량 점수", latest_analysis.get('stimulus_score', 'N/A'))
        
        with col2:
            st.metric("운동 효율 점수", latest_analysis.get('efficiency_score', 'N/A'))
        
        st.divider()
        
        # 상세 정보
        st.write("**분석 상세 정보**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**세션 ID:** {latest_analysis.get('session_id')}")
        
        with col2:
            st.write(f"**생성 날짜:** {latest_analysis.get('created_at', 'N/A')}")
        
        # 경고 정보
        if latest_analysis.get('warning_content'):
            st.warning(f"**손해 운동 경고:** {latest_analysis.get('warning_content')}")
        else:
            st.success("**상태:** 경고 없음 ✅")
        
        st.divider()
        
        # 분석 이력
        st.subheader("분석 결과 이력")
        
        analysis_history = get_analysis_history(user_id, limit=10)
        
        if analysis_history:
            for idx, analysis in enumerate(analysis_history, 1):
                with st.container(border=True):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**#{idx}**")
                        st.write(f"날짜: {analysis.get('created_at', 'N/A')[:10]}")
                    
                    with col2:
                        st.write(f"자극량: {analysis.get('stimulus_score', 'N/A')}")
                        st.write(f"효율: {analysis.get('efficiency_score', 'N/A')}")
                    
                    with col3:
                        if analysis.get('warning_content'):
                            st.write(f"⚠️ {analysis.get('warning_content')[:50]}")
                        else:
                            st.write("✅ 정상")
        else:
            st.info("분석 결과 이력이 없습니다.")
    
    else:
        st.info("아직 분석 결과가 없습니다.")
        st.write("운동 기록과 회복 기록을 입력하면 분석 결과가 생성됩니다.")

except Exception as e:
    st.error(f"오류가 발생했습니다: {str(e)}")
