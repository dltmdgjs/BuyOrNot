![header](https://capsule-render.vercel.app/api?type=waving&color=timeGradient&height=200&section=header&text=BuyOrNot?&fontSize=40)

# Buy Or Not? - 구매 의사 결정 

- Buy Or Not? 프로그램은 우리나라 인기 쇼핑몰 사이트인 쿠팡(Coupang)의 제품 리뷰를 크롤링하여, gpt모델을 사용해 구매 의사를 돕는 프로그램입니다.
- 프로그램을 실행하여 제품의 url을 넣어보세요. gpt가 대신 결정해줄 겁니다.

## 프로그램 실행 화면
- (vscode의 터미널 창을 통해 실행한 화면입니다.)

### 실행 첫 화면(제품 url 입력)
<img width="1092" alt="img0" src="https://github.com/user-attachments/assets/c641ab3c-8e19-4ae0-ae4b-ad9551001ce5">

### 리뷰 크롤링 화면
<img width="1089" alt="img1" src="https://github.com/user-attachments/assets/1122a2a2-aff7-4a40-a7d4-95e22a8852c7">
<img width="1091" alt="img2" src="https://github.com/user-attachments/assets/6e9c563d-f2a8-4199-ab66-a5f6bbab06f6">  
- url 입력 후 제품 페이지 내 리뷰를 가져옴

### GPT 모델 평가
<img width="561" alt="img3" src="https://github.com/user-attachments/assets/b11866fa-c51a-49bc-b5a7-985bb54434b4">


### 생성된 엑셀 파일
<img width="739" alt="img4" src="https://github.com/user-attachments/assets/496b64de-8a67-4a1d-a0a1-710e22a1a441">  
- gpt 모델로 분석한 결과는 엑셀 파일로 저장되며, 각 리뷰에 대한 긍정 및 부정 평가가 담김.

### 리뷰 크롤링 (요청 시간 만료)
<img width="1097" alt="img5" src="https://github.com/user-attachments/assets/8e1a4cc9-1254-4aba-922d-ab8aea7f3e44">  
- time out으로 인해 실패한 화면




## GPT API 키

### 1. OPENAI API 사이트에 로그인 후 API 키 발급
[OPENAI API](https://openai.com/index/openai-api/)
- (주의!) 애플 아이디로 로그인 할 경우 '나의 이메일 가리기' 사용 중이라면, 추후 로그인 시 인증 메일 수신 불가 문제가 발생하여 로그인하지 못하니 다른 계정으로 계정 생성할 것! (저도 이 문제를 알고 싶지 않았습니다..)
- (주의!) API 키를 발급 받으면 복사해서 안전한 곳에 저장할 것! (키는 한번만 보여줍니다.)
- (참고) API 발급은 무료이지만, 사용을 위해선 결제 필요.

### 2. 프로젝트에 openai 라이브러리 설치

```
pip install openai python-dotenv
```

### 3. .env 파일에 API 키 저장
```
OPENAI_API_KEY="your_openai_api_key"
```

### 4. GPT 모델 연동 및 리뷰 분석 코드 작성

```
import openai
import pandas as pd
import os
from dotenv import load_dotenv

# .env 파일에서 API 키 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# GPT 모델을 사용하여 리뷰 분석 함수
def analyze_review(review_text):
    try:
        response = openai.Completion.create(
            # 모델 선택
            model="text-davinci-003",
            # 명령어 입력
            prompt=f"다음 리뷰의 감정을 분석해주세요: '{review_text}'\n감정: ",
            max_tokens=10
        )
        sentiment = response['choices'][0]['text'].strip()
        return sentiment
    except Exception as e:
        print("API 요청 중 오류 발생:", e)
        return None
...
...
...
```
- .env 파일로부터 api키를 불러와 저장
- max_tokens 값을 증가시켜 gpt의 답변 길이를 늘릴 수 있음.

## 크롤링 코드
[JaehyoJJAng](https://github.com/JaehyoJJAng/Coupang-Review-Crawling/tree/main)
- 리뷰 크롤링은 위를 참조 및 변경하였음.

### 주요 변경 사항
1. 크롤링할 대상 축소 (리뷰요소만 크롤링 및 최대 크롤링 개수를 10개로 설정.)
2. 딜레이 시간을 랜덤하게 하도록 변경 (쿠팡의 반복적인 요청 거절로 인한 변경.)
3. 저장할 엑셀 파일명 변경.

## References
[text](https://github.com/JaehyoJJAng/Coupang-Review-Crawling/tree/main)

## License
MIT License

## 기타(참고사항)
- API 키도 같이 업로드 하고 싶었으나, 개인 계정을 통해 비용을 지불하고 사용하는 것이므로 유출 방지를 위해 gitignore 하였습니다.
- 많은 수의 리뷰를 분석하면 신뢰성이 높아질 수 있지만, 쿠팡 측에서 계속해서 다양한 방법으로 요청을 차단하고 있고, 그렇게 하는 이유가 있다고 생각하였기 때문에 소량(10개)만 크롤링하였습니다.
