import os
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time

from PublicDataReader import TransactionPrice
from dotenv import load_dotenv

load_dotenv()

from CityCode import get_gungu_info, get_sido_info
from months import generate_months, generate_recent_months, generate_year_months

service_key = os.getenv("PUBLIC_DATA_HUB")
api = TransactionPrice(service_key)

sido_list = get_sido_info()
gungu_list = get_gungu_info(sido_list["cortarNo"][0])


def calculate_gap_ratio(sale_df, jeonse_df):
    """간단한 갭투자 비율 계산"""
    if sale_df is None or jeonse_df is None or len(sale_df) == 0:
        return 0

    # 전세만 추출 (월세 = 0)
    jeonse_only = jeonse_df[jeonse_df["월세금액"] == 0].copy()

    if len(jeonse_only) == 0:
        return 0

    # 매칭키 생성
    def create_key(df):
        return (
            df["법정동"].astype(str)
            + "_"
            + df["단지명"].astype(str)
            + "_"
            + df["층"].astype(str)
            + "_"
            + df["계약년도"].astype(str)
            + "_"
            + df["계약월"].astype(str)
            + "_"
            + df["계약일"].astype(str)
        )

    sale_keys = set(create_key(sale_df))
    jeonse_keys = set(create_key(jeonse_only))

    # 매칭 케이스 찾기
    matched_cases = len(sale_keys & jeonse_keys)

    # 갭투자 비율 계산
    gap_ratio = (matched_cases / len(sale_df)) * 100 if len(sale_df) > 0 else 0

    return gap_ratio


# 월별 구별 갭투자 비율 조회
def month_to_month_gap_ratio(months_list=None):
    """
    월별 구별 갭투자 비율 조회

    Args:
        months_list (list): 조회할 월 리스트 (기본값: 최근 6개월)

    Returns:
        pd.DataFrame: 월별 구별 갭투자 비율 데이터프레임
    """
    if months_list is None:
        months_list = generate_recent_months(6)  # 기본값: 최근 6개월

    results = []

    print("📊 월별 구별 갭투자 비율 조회 시작...")
    print("=" * 60)

    for month in months_list:
        print(f"\n📅 {month} 분석 중...")

        for idx, row in gungu_list.iterrows():
            cortarNo = str(row["cortarNo"])[:5]  # 앞의 5자리만 추출
            cortarName = row["cortarName"]

            try:
                # 매매 데이터 조회
                sale_df = api.get_data(
                    property_type="아파트",
                    trade_type="매매",
                    sigungu_code=cortarNo,
                    year_month=month,
                )

                # 전월세 데이터 조회
                jeonse_df = api.get_data(
                    property_type="아파트",
                    trade_type="전월세",
                    sigungu_code=cortarNo,
                    year_month=month,
                )

                # 갭투자 비율 계산
                gap_ratio = calculate_gap_ratio(sale_df, jeonse_df)

                # 결과 저장
                results.append(
                    {
                        "년월": month,
                        "구명": cortarName,
                        "매매거래수": len(sale_df) if sale_df is not None else 0,
                        "전월세거래수": len(jeonse_df) if jeonse_df is not None else 0,
                        "갭투자비율(%)": round(gap_ratio, 2),
                    }
                )

                if gap_ratio > 0:
                    print(f"  • {cortarName}: {gap_ratio:.1f}%")

                # API 호출 간격 조정
                time.sleep(0.1)

            except Exception as e:
                print(f"  ❌ {cortarName} 오류: {e}")
                results.append(
                    {
                        "년월": month,
                        "구명": cortarName,
                        "매매거래수": 0,
                        "전월세거래수": 0,
                        "갭투자비율(%)": 0,
                    }
                )

    return pd.DataFrame(results)


# 결과 데이터프레임 생성
if __name__ == "__main__":
    # 다양한 사용 예시

    # 1. 최근 6개월 데이터 조회
    # recent_data = month_to_month_gap_ratio()
    # print("\n=== 최근 6개월 갭투자 비율 ===")
    # print(recent_data.head())

    # # 2. 특정 연도 전체 데이터 조회
    # year_2024_months = generate_year_months(2025)
    # year_2024_data = month_to_month_gap_ratio(year_2024_months)
    # print("\n=== 2024년 전체 갭투자 비율 ===")
    # print(year_2024_data.head())

    # 3. 특정 기간 데이터 조회
    period_months = generate_months(2011, 1, 2025, 6)
    period_data = month_to_month_gap_ratio(period_months)
    print("\n=== 2000년 1월 ~ 2025년 6월 갭투자 비율 ===")
    print(period_data.head())

    # CSV 저장
    period_data.to_csv("gap_investment_results.csv", index=False)
    print("\n✅ 결과가 gap_investment_results.csv에 저장되었습니다.")
