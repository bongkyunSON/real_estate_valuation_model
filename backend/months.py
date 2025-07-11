from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def generate_months(start_year=2000, start_month=1, end_year=None, end_month=None):
    """
    동적으로 년월 리스트를 생성하는 함수

    Args:
        start_year (int): 시작 연도 (기본값: 2000)
        start_month (int): 시작 월 (기본값: 1)
        end_year (int): 종료 연도 (기본값: 현재 연도)
        end_month (int): 종료 월 (기본값: 현재 월)

    Returns:
        list: "YYYYMM" 형태의 문자열 리스트
    """
    if end_year is None:
        end_year = datetime.now().year
    if end_month is None:
        end_month = datetime.now().month

    months = []
    current_date = datetime(start_year, start_month, 1)
    end_date = datetime(end_year, end_month, 1)

    while current_date <= end_date:
        months.append(current_date.strftime("%Y%m"))
        current_date += relativedelta(months=1)

    return months


def generate_recent_months(months_count=6):
    """
    최근 N개월의 년월 리스트를 생성

    Args:
        months_count (int): 최근 몇 개월인지 (기본값: 6)

    Returns:
        list: "YYYYMM" 형태의 문자열 리스트
    """
    months = []
    current_date = datetime.now().replace(day=1)

    for i in range(months_count):
        months.append(current_date.strftime("%Y%m"))
        current_date -= relativedelta(months=1)

    return list(reversed(months))


def generate_year_months(year):
    """
    특정 연도의 모든 월을 생성

    Args:
        year (int): 연도

    Returns:
        list: "YYYYMM" 형태의 문자열 리스트
    """
    return [f"{year}{month:02d}" for month in range(1, 13)]


# 호환성을 위한 기본 months 리스트 (필요시 사용)
months = generate_months(2000, 1, 2025, 6)

# 실제 사용 예시들
if __name__ == "__main__":
    # 전체 기간 (2000년 1월 ~ 현재)
    all_months = generate_months()
    print(f"전체 기간: {len(all_months)}개월")
    print(f"최근 5개: {all_months[-5:]}")

    # 최근 6개월만
    recent_months = generate_recent_months(6)
    print(f"최근 6개월: {recent_months}")

    # 2024년 전체
    year_2024 = generate_year_months(2024)
    print(f"2024년 전체: {year_2024}")

    # 특정 기간
    period_months = generate_months(2023, 1, 2024, 12)
    print(f"2023-2024 기간: {len(period_months)}개월")
