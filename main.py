import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. 앱 제목
st.title("한국에서 출발하는 비행기 티켓 가격 분석 및 예측 ✈️")

# 2. 가상 데이터 생성
# 2024년 날짜 범위 생성
dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="W")

# 환율 설정 (예시: 1 USD = 1300 KRW)
exchange_rate = 1300

# 도시별 가상 티켓 가격 데이터 (정규분포 기반 가상의 가격)
np.random.seed(42)  # 결과 재현을 위한 시드 고정
ticket_prices = {
    "Tokyo": np.random.normal(300, 50, len(dates)) * exchange_rate,
    "Osaka": np.random.normal(280, 45, len(dates)) * exchange_rate,
    "New York": np.random.normal(900, 100, len(dates)) * exchange_rate,
    "London": np.random.normal(850, 90, len(dates)) * exchange_rate
}

# 데이터프레임 생성
data = pd.DataFrame({
    "Date": dates,
    "Tokyo": ticket_prices["Tokyo"],
    "Osaka": ticket_prices["Osaka"],
    "New York": ticket_prices["New York"],
    "London": ticket_prices["London"]
})

# 3. 도시 선택 (UI는 한글로 표시)
city_kor = st.selectbox("도시를 선택하세요", ["도쿄", "오사카", "뉴욕", "런던"])
city_map = {"도쿄": "Tokyo", "오사카": "Osaka", "뉴욕": "New York", "런던": "London"}
city = city_map[city_kor]

# 선택한 도시에 해당하는 데이터 필터링
city_data = data[["Date", city]].rename(columns={city: "Price"})

# 4. 가격 변동 그래프 (그래프 제목과 레이블은 영어로 표시)
st.subheader(f"{city_kor} 행 티켓 가격 변동")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(city_data["Date"], city_data["Price"], marker='o', linestyle='-', color='blue', alpha=0.7)
ax.set_xlabel("Date", fontsize=12)
ax.set_ylabel("Price (KRW)", fontsize=12)
ax.set_title(f"{city} Ticket Price Trend in 2024", fontsize=14)
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.5)
st.pyplot(fig)

# 5. 가장 저렴한 시기 예측 (UI는 한글로 표시)
min_price_row = city_data.loc[city_data["Price"].idxmin()]
st.subheader("가장 저렴한 시기 예측")
st.write(f"{city_kor} 행 티켓 가격이 가장 저렴한 시기는 **{min_price_row['Date'].strftime('%Y-%m-%d')}**로, 가격은 **₩{min_price_row['Price']:.0f}** 입니다.")

# 6. 월별 평균 가격 막대 그래프 (그래프 제목과 레이블은 영어로 표시)
st.subheader(f"{city_kor} 행 월별 평균 가격")
city_data['Month'] = city_data['Date'].dt.month
monthly_avg = city_data.groupby("Month")["Price"].mean()

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(monthly_avg.index, monthly_avg.values, color='skyblue', edgecolor='black', alpha=0.7)
ax.set_xlabel("Month", fontsize=12)
ax.set_ylabel("Average Price (KRW)", fontsize=12)
ax.set_title(f"Monthly Average Ticket Price to {city} in 2024", fontsize=14)
plt.xticks(monthly_avg.index)
plt.grid(True, axis='y', linestyle='--', alpha=0.5)
st.pyplot(fig)
