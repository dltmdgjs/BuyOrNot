import openai
import pandas as pd
import os
from dotenv import load_dotenv



# GPT 모델을 사용한 감정 분석
def analyze_review_with_gpt(review_text, api_key):
    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "리뷰 분석을 돕는 역할을 해주세요."},
                {"role": "user", "content": f"이 리뷰의 감정을 분석해주세요, 대답 형식은 다음과 같이 해주세요. [긍정/부정/중립 중 1개] : [짧은 이유 한 문장)]. 다음은 분석할 리뷰입니다 : '{review_text}'"}
            ],
            max_tokens=50
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"API 요청 중 오류 발생: {e}")
        return "분석 오류"

# 감정 분석 결과 분류
def determine_sentiment_category(analysis):
    if "긍정" in analysis:
        return "긍정"
    elif "부정" in analysis:
        return "부정"
    else:
        return "중립"

# 긍정 리뷰 비율 계산 및 구매 결정
def make_purchase_decision(sentiment_counts):
    positive_reviews = sentiment_counts.get("긍정", 0)
    negative_reviews = sentiment_counts.get("부정", 0)
    total_reviews = positive_reviews + negative_reviews

    if total_reviews == 0:
        return "리뷰 데이터 부족으로 결정할 수 없습니다."
    positive_ratio = positive_reviews / total_reviews
    return "구매 추천" if positive_ratio > 0.8 else "비추천"

# GPT 모델로 이유 요약 출력
def show_reason_with_gpt(final_decision, df, api_key):
    # 이유 요약 및 출력.
    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "리뷰 분석을 돕는 역할을 해주세요."},
                {"role": "user", "content": f"다음은 최종 구매 결정과 분석결과들입니다. 최종 구매 결정이 '추천'이면 긍정인 분석결과들을 50자 이내로 한 줄로 요약해주고, 최종 구매 결정이 '비추천'이면 부정인 분석결과들을 50이내 한 줄로 요약해주세요. 최종 구매 결정 : {final_decision}, 분석결과들 : '{df['리뷰 분석']}', 출력 시 다른말은 덧붙이지 말고 요약된 이유만 출력"}
            ],
            max_tokens=100
        )
        print(f"이유 : {response['choices'][0]['message']['content']}")
        return f"이유 : {response['choices'][0]['message']['content']}"
    except Exception as e:
        print(f"API 요청 중 오류 발생: {e}")
        return "분석 오류"

# 분석 결과를 엑셀로 저장
def save_analysis_to_excel(df, output_path):
    try:
        df.to_excel(output_path, index=False)
        print(f"분석 결과가 '{output_path}'에 저장되었습니다.")
    except Exception as e:
        print(f"엑셀 저장 중 오류 발생: {e}")

# 전체 분석 실행 함수
def run_review_analysis():

    #gpt api key 불러오기
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("API 키를 로드할 수 없습니다. .env 파일을 확인해주세요.")
        return
    
    # 리뷰 파일 불러오기
    excel_file = "Coupang-reviews/crawled_reviews.xlsx"
    if not excel_file:
        print("엑셀 파일 경로를 확인해주세요.")
        return
    try:
        df = pd.read_excel(excel_file)
        print("리뷰 데이터를 성공적으로 로드했습니다.")
    except Exception as e:
        print(f"엑셀 파일 로드 중 오류 발생: {e}")
        return

    # 감정 분석 수행
    print("gpt 모델로 분석 중...")
    df['리뷰 분석'] = df['리뷰 내용'].apply(lambda review: analyze_review_with_gpt(review, api_key))
    df['분석 결과'] = df['리뷰 분석'].apply(determine_sentiment_category)

    # 최종 구매 결정 계산 및 출력
    sentiment_counts = df['분석 결과'].value_counts()
    final_decision = make_purchase_decision(sentiment_counts)
    print("최종 구매 결정:", final_decision)

    # 이유 요약 및 출력.
    reason = show_reason_with_gpt(final_decision, df, api_key)

    # 결과를 저장할 디렉토리 생성
    if not os.path.exists('Reviews-analysis'):
        os.makedirs('Reviews-analysis')

    # 결과 저장
    output_file = "Reviews-analysis/analyzed_reviews.xlsx"
    save_analysis_to_excel(df, output_file)

    return "최종 구매 결정 : " + final_decision + ", \n" + reason

