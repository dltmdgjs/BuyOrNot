from getCoupangReview import Coupang
from analyzeCoupangReview import run_review_analysis

if __name__ == '__main__':
    coupang = Coupang()
    coupang.start()
    run_review_analysis()