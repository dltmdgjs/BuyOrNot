import streamlit as st
from analyzeCoupangReview import run_review_analysis
from getCoupangReview import Coupang

# Streamlit 애플리케이션 제목
st.title("Buy or Not")

# URL 입력 필드
url = st.text_input("상품 URL을 입력하세요:")

# 분석 시작 버튼
if st.button("분석 시작"):
    if url:
        st.info("리뷰를 크롤링하고 분석 중입니다. 잠시만 기다려주세요...")

        try:
            # 크롤링 실행
            coupang = Coupang()
            coupang.start(url)

            # 분석 실행 및 GPT 결과 출력
            gpt_response = run_review_analysis()  # run_review_analysis에서 show_reason_with_gpt 호출 포함
            if gpt_response:
                st.success("최종 구매 결정 및 이유")
                st.info(gpt_response)
            else:
                st.error("분석 결과를 가져오는 데 실패했습니다.")

        except Exception as e:
            st.error(f"오류 발생: {e}")
    else:
        st.error("상품 URL을 입력하세요!")