import streamlit as st
from services.auth_service import get_current_user
from services.analysis_service import get_recommendations_list

st.set_page_config(
    page_title="Recommendation - Exercise MVP",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 추천 결과 조회")

# 로그인 확인
user = get_current_user()
if not user:
    st.warning("로그인이 필요합니다.")
    st.stop()

user_id = user.id

try:
    st.subheader("분석 결과 기반 추천 운동")
    
    recommendations = get_recommendations_list(user_id, limit=10)
    
    if recommendations:
        st.write(f"**총 {len(recommendations)}개의 추천 운동**")
        st.divider()
        
        for idx, rec in enumerate(recommendations, 1):
            with st.container(border=True):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"### {idx}. {rec.get('exercises', {}).get('exercise_name', 'Unknown')}")
                    
                    st.write("**추천 이유**")
                    st.write(rec.get('reason', 'N/A'))
                    
                    st.write("**예상 효과**")
                    st.write(rec.get('expected_effect', 'N/A'))
                    
                    # 대상 근육 부위
                    target_muscles = rec.get('muscle_groups', {})
                    if target_muscles:
                        st.write(f"**대상 근육:** {target_muscles.get('muscle_name', 'N/A')}")
                
                with col2:
                    st.write("**상세 정보**")
                    st.write(f"ID: {rec.get('id')}")
                    st.write(f"생성: {rec.get('created_at', 'N/A')[:10]}")
                    
                    # 추천 채택/거절 버튼 (향후 구현)
                    if st.button("👍 추천 수락", key=f"accept_{rec.get('id')}"):
                        st.success("추천을 수락했습니다!")
                    
                    if st.button("👎 추천 거절", key=f"reject_{rec.get('id')}"):
                        st.info("추천을 거절했습니다.")
    
    else:
        st.info("아직 추천 결과가 없습니다.")
        st.write("운동 기록, 회복 기록, 분석 결과가 있을 때 추천이 생성됩니다.")
        
        st.divider()
        st.write("**다음 단계:**")
        st.write("1. 💪 운동 기록 입력")
        st.write("2. 🩹 회복 기록 입력")
        st.write("3. 📊 분석 결과 생성")
        st.write("4. 🎯 추천 결과 확인")

except Exception as e:
    st.error(f"오류가 발생했습니다: {str(e)}")
