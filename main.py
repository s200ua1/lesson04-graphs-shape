import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")


DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data():
    # 1년간 박스오피스 10위권에 든 영화 216편의 요약표를 불러옵니다
    df = pd.read_csv(DATA_URL)

    # 장르가 여러 개(|)로 적힌 영화는 첫 번째 장르만 씁니다
    df["장르"] = df["genre"].fillna("기타").astype(str).str.split("|").str[0]

    # 총 관객을 숫자로 변환합니다
    df["total_audi"] = pd.to_numeric(df["total_audi"], errors="coerce")

    return df


df = load_data()


# --------------------------------------------------
# 그래프 1. 장르별 영화 편수 도넛
# --------------------------------------------------
st.header("1. 장르별 영화 편수 (도넛)")

genre_count = df["장르"].value_counts().reset_index()
genre_count.columns = ["장르", "편수"]


fig = px.pie(
    genre_count,
    names="장르",
    values="편수",
    hole=0.45
)

# 조각에 마우스를 올리면 편수와 비율이 보이게 합니다
fig.update_traces(
    hovertemplate="%{label}<br>영화 편수: %{value}편<br>비율: %{percent}<extra></extra>"
)

st.plotly_chart(fig, use_container_width=True)


# '이 그래프로 알 수 있는 것' 한 문장을 적는 자리
st.text_input("이 그래프로 알 수 있는 것", key="note1")


st.divider()


# --------------------------------------------------
# 그래프 2. 장르 안에 영화가 들어 있는 트리맵
# --------------------------------------------------
st.header("2. 장르별 영화 총 관객 트리맵")

fig = px.treemap(
    df,
    path=["장르", "movieNm"],
    values="total_audi"
)

# 영화 칸에 마우스를 올리면 영화명과 총 관객이 보이게 합니다
fig.update_traces(
    hovertemplate="영화명: %{label}<br>총 관객: %{value:,.0f}명<extra></extra>"
)

st.plotly_chart(fig, use_container_width=True)


# '이 그래프로 알 수 있는 것' 한 문장을 적는 자리
st.text_input("이 그래프로 알 수 있는 것", key="note2")


st.divider()


# --------------------------------------------------
# 그래프 3. 총 관객 히스토그램
# --------------------------------------------------
st.header("3. 영화별 총 관객 분포")

# 결측치를 제외합니다
관객데이터 = df.dropna(subset=["total_audi"]).copy()

# 히스토그램을 그립니다
fig = px.histogram(
    관객데이터,
    x="total_audi",
    nbins=10,
    labels={
        "total_audi": "총 관객",
        "count": "영화 편수"
    }
)

fig.update_layout(
    xaxis_title="총 관객",
    yaxis_title="영화 편수"
)

fig.update_traces(
    hovertemplate="총 관객 구간: %{x}<br>영화 편수: %{y}편<extra></extra>"
)

st.plotly_chart(fig, use_container_width=True)


# 가장 많은 영화가 몰려 있는 구간을 계산합니다
최소관객 = 관객데이터["total_audi"].min()
최대관객 = 관객데이터["total_audi"].max()

구간경계 = np.linspace(최소관객, 최대관객, 11)

관객데이터["관객구간"] = pd.cut(
    관객데이터["total_audi"],
    bins=구간경계,
    include_lowest=True
)

구간별영화수 = 관객데이터["관객구간"].value_counts().sort_index()

가장많은구간 = 구간별영화수.idxmax()
가장많은구간영화수 = 구간별영화수.max()

# 총 관객이 가장 많은 영화를 찾습니다
가장많은관객영화 = 관객데이터.loc[
    관객데이터["total_audi"].idxmax()
]

영화이름 = 가장많은관객영화["movieNm"]
총관객수 = 가장많은관객영화["total_audi"]


# 그래프 아래에 해석 문구를 보여 줍니다
st.write(
    f"대부분의 영화는 **{가장많은구간.left:,.0f}명~"
    f"{가장많은구간.right:,.0f}명** 구간에 몰려 있으며, "
    f"이 구간에는 **{가장많은구간영화수}편**의 영화가 있습니다."
)

st.write(
    f"총 관객이 가장 많은 영화는 **{영화이름}**으로, "
    f"총 관객은 **{총관객수:,.0f}명**입니다."
)


# '이 그래프로 알 수 있는 것' 한 문장을 적는 자리
st.text_input("이 그래프로 알 수 있는 것", key="note3")


st.divider()


# 앞으로 그래프를 계속 추가할 구역
st.header("4. (다음 그래프를 여기에 추가)")
