from bs4 import BeautifulSoup as bs
# from pathlib import Path
from openpyxl import Workbook
# from fake_useragent import UserAgent
from requests.exceptions import RequestException
import time, os, re
import requests as rq
import math, sys
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# 크롬 웹 드라이버
class ChromeDriver:
    def __init__(self) -> None:
        self.set_options()
        self.set_driver()

    def set_options(self) -> None:
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("lang=ko_KR")
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        self.options.add_argument("--log-level=3")
        self.options.add_experimental_option("detach", True)
        self.options.add_experimental_option("excludeSwitches", ["enable-logging"])

    def set_driver(self) -> None:
        self.driver = webdriver.Chrome(options=self.options)




# 쿠팡 리뷰 크롤링.
class Coupang:

    @staticmethod
    def get_product_code(url: str) -> str:
        prod_code: str = url.split("products/")[-1].split("?")[0]
        return prod_code

    # 클래스 생성 후 초기값 설정.
    def __init__(self) -> None:
        self.base_review_url: str = "https://www.coupang.com/vp/product/reviews"
        self.sd = SaveData()
        self.retries = 10
        # 웹 드라이버 헤더 정보(사이트 차단 방지)
        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ko,en;q=0.9,en-US;q=0.8",
            "cookie": "_fbp=fb.1.1709172148924.2042270649; gd1=Y; delivery_toggle=false; srp_delivery_toggle=true; _gcl_au=1.1.1542987164.1726856649; PCID=17272706554699560993959; MARKETID=17272706554699560993959; x-coupang-accept-language=ko-KR; sid=862268b00c90426e990014e6fbf5c7af26562a56; x-coupang-target-market=KR; cf_clearance=r2sQqITwCPo3MoS9IP6Z9PK4HOLYe1ynNWfrauGIufY-1731223910-1.2.1.1-fypmZTk0lIfn8iYHCzX2XZYxGZEjRk5aIM8Eii0PfOgdkWkQ7p.i_AWtifLRou_srPIcGIptzj4pekqm_g.hlWFiPqvRBw5GBlCMFvse9WCy6W0v_ozxtn8yT6Vr8DbALzOVn8umBYJtTVWW_VWJ0sSF5ug8m4hneemnDDLUXeVC9nPEvAQsAEch31CaIy13EZ41WCvs1x.d.G8MTeFLJaGmlJ6fF0pyCtS_JBBdyvloE70.0hQSLZUgN_aKtinLmBEYV9111WtEiy6b_X9rAsmkNfUKmyOZhQrZ0bitPJJTBaL.KOe19sw8rjNSjvLBQWEZjA2sG7ClWr.HeG0VxG3IqSRL.TWBAYgmdBOoJ.DgKkMRXtYr2YEr10JrdaLa5zDHJ5OT6L5Wuc.9bbe2oA; session-id=324aeca3-d8cd-4c45-a6f1-10621d390140; bm_sz=8B4246C44D36EDFC15E70A22536E45B1~YAAQJWHKF+ekeyOTAQAAPjaxUxkwWm66AyB3nnLpzE+aqPPDqugGLbLVDwLT9ONfw/LKyaD3+dznGh6zbEG/dCvrZD1RRuDPnnzoG7/UU37+DKGnwz5/PLTfprF2G0d6ZY0C+EGijaUw1Y0oSODTWswOBXdyBJpub9W/60oWnJocJP0qICJhLVaM95fhCv8+CTHMUMm7I9n/cz5LPTopwEG0gi9WXF5vTH0mKJVpgeB0Rmf4L0ICd0wAO6pl5fnpzzVoQ80k7hgHbUJxpwooF/QNUS6CxRM4s+4lnvWFlDC1w2bsBr66WBlq2+WKXJio1R4kZovl+jl2Dmm9n0AFNKF1KSe7dbBLbWP2i2uLBgiyIS4TFKcwm0NwumkF0Z34PbTTBKjHO1mqtwiAP4P/bu3/vg1UkkSn5qXCQShEN6nMpmEf2YlIQ3ViXNayXFH15pss1AL1AVzufLYgjmkYRNxbNrhB6ZMREQWOfzxjroVvmSkYk+yb8JYNoRxhHZZXvR8spplD3mSsK7aRYyss1qshf3KVx2D9jw==~3753010~4474160;",
            "priority": "u=1, i",
            "sec-ch-ua": '"Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        }
        self.ch = ChromeDriver()

    # 상품 정보 가져오기.
    def get_product_info(self, prod_code: str) -> tuple:
        url = f"https://www.coupang.com/vp/products/{prod_code}"
        self.ch.driver.get(url=url)
        WebDriverWait(self.ch.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
        )
        page_source: str = self.ch.driver.page_source
        soup = bs(page_source, "html.parser")
        return (int(re.sub("[^0-9]", "", soup.select("span.count")[0].text.strip())))

    
    def start(self, url) -> None:
        self.sd.create_directory()
        URL: str = url
        self.headers["Referer"] = URL
        prod_code: str = self.get_product_code(url=URL)

        # 상품 정보 추출
        review_count = self.get_product_info(prod_code=prod_code)
        if review_count > 10:
            review_pages = 2
        else:
            review_pages: int = self.calculate_total_pages(review_count)

        # Set payload
        payloads = [
            {
                "productId": prod_code,
                "page": page,
                "size": 5,
                "sortBy": "ORDER_SCORE_ASC",
                "ratings": "",
                "q": "",
                "viRoleCode": 2,
                "ratingSummary": True,
            }
            for page in range(1, review_pages + 1)
        ]

        # 데이터 추출
        for payload in payloads:
            self.fetch(payload=payload)

    def fetch(self, payload: list[dict]) -> None:
        now_page: str = payload["page"]
        print(f"\n[INFO] Start crawling page {now_page} ...\n")
        attempt: int = 0
        while attempt < self.retries:
            try:
                with rq.Session() as session:
                    with session.get(
                        url=self.base_review_url,
                        headers=self.headers,
                        params=payload,
                        timeout=10,
                    ) as resp:
                        resp.raise_for_status()
                        html = resp.text
                        soup = bs(html, "html.parser")

                        # Article Boxes
                        article_lenth = len(
                            soup.select("article.sdp-review__article__list")
                        )

                        for idx in range(article_lenth):
                            dict_data: dict[str, str | int] = dict()
                            articles = soup.select("article.sdp-review__article__list")

                            # 리뷰 내용
                            review_content = articles[idx].select_one("div.sdp-review__article__list__review > div")
                            if review_content == None:
                                review_content = "" # 등록된 리뷰 내용이 없습니다.
                            else:
                                review_content = re.sub("[\n\t]", "", review_content.text.strip())

                            # 저장.
                            dict_data["review_content"] = review_content
                            self.sd.save(datas=dict_data)
                            print(dict_data, "\n")
                        time.sleep(1)
                        return
            except RequestException as e:
                attempt += 1
                print(f"Attempt {attempt}/{self.retries} failed: {e}")
                if attempt < self.retries:
                    time.sleep(random.uniform(2, 5))
                else:
                    print(f"최대 요청 만료! 다시 실행하세요.")
                    sys.exit()
                    

   
    def input_review_url(self) -> str:
        review_url: str = input("URL 주소를 입력해주세요 : ")
        return review_url

    def calculate_total_pages(self, review_counts: int) -> int:
        reviews_per_page: int = 5
        return int(math.ceil(review_counts / reviews_per_page))


# 엑셀파일로 크롤링 결과 저장.
class SaveData:
    def __init__(self) -> None:
        self.wb: Workbook = Workbook()
        self.ws = self.wb.active
        self.ws.append(["리뷰 내용"])
        self.row: int = 2
        self.dir_name: str = "Coupang-reviews"
        self.create_directory()

    def create_directory(self) -> None:
        if not os.path.exists(self.dir_name):
            os.makedirs(self.dir_name)

    def save(self, datas: dict[str, str | int]) -> None:
        file_name: str = os.path.join(self.dir_name, "crawled_reviews.xlsx")
        self.ws[f"A{self.row}"] = datas["review_content"]
        self.row += 1
        self.wb.save(filename=file_name)

    def __del__(self) -> None:
        self.wb.close()

