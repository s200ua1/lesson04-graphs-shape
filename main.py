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
    df = pd.read_csv(DATA_URL)

    # 장르가 여러 개이면 첫 번째 장르만 사용
    df["장르"] = (
        df["genre"]
        .fillna("기타")
        .astype(str)
        .str.split("|")
        .str[0]
    )

    # 제작 국가가 여러 개이면 첫 번째 국가만 사용
    df["제작국가"] = (
        df["nation"]
        .fillna("기타")
        .astype(str)
        .str.split("|")
        .str[0]
    )

    # 숫자 데이터 변환
    df["first_scrn"] = pd.to_numeric(
        df["first_scrn"],
        errors="coerce"
    )

    df["first_week_audi"] = pd.to_numeric(
        df["first_week_audi"],
        errors="coerce"
    )

    df["total_audi"] = pd.to_numeric(
        df["total_audi"],
        errors="coerce"
    )

    return df


df = load_data()


# ==================================================
# 1. 장르별 영화 편수 도넛
# ==================================================
st.header("1. 장르별 영화 편수 (도넛)")

genre_count = df["장르"].value_counts().reset_index()
genre_count.columns = ["장르", "편수"]

fig = px.pie(
    genre_count,
    names="장르",
    values="편수",
    hole=0.45
)

fig.update_traces(
    hovertemplate=
    "%{label}<br>"
    "영화 편수: %{value}편<br>"
    "비율: %{percent}"
    "<extra></extra>"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.text_input(
    "이 그래프로 알 수 있는 것",
    key="note1"
)


st.divider()


# ==================================================
# 2. 장르별 영화 총 관객 트리맵
# ==================================================
st.header("2. 장르별 영화 총 관객 트리맵")

트리맵데이터 = df.dropna(
    subset=["장르", "movieNm", "total_audi"]
).copy()

fig = px.treemap(
    트리맵데이터,
    path=["장르", "movieNm"],
    values="total_audi"
)

fig.update_traces(
    hovertemplate=
    "영화명: %{label}<br>"
    "총 관객: %{value:,.0f}명"
    "<extra></extra>"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.text_input(
    "이 그래프로 알 수 있는 것",
    key="note2"
)


st.divider()


# ==================================================
# 3. 총 관객 히스토그램
# ==================================================
st.header("3. 영화별 총 관객 분포")

관객데이터 = df.dropna(
    subset=["total_audi"]
).copy()

fig = px.histogram(
    관객데이터,
    x="total_audi",
    nbins=10,
    labels={
        "total_audi": "총 관객"
    }
)

fig.update_layout(
    xaxis_title="총 관객",
    yaxis_title="영화 편수"
)

fig.update_traces(
    hovertemplate=
    "총 관객: %{x:,.0f}명<br>"
    "영화 편수: %{y}편"
    "<extra></extra>"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# 가장 많은 영화가 들어 있는 구간 계산
최소관객 = 관객데이터["total_audi"].min()
최대관객 = 관객데이터["total_audi"].max()

구간경계 = np.linspace(
    최소관객,
    최대관객,
    11
)

관객데이터["관객구간"] = pd.cut(
    관객데이터["total_audi"],
    bins=구간경계,
    include_lowest=True
)

구간별영화수 = (
    관객데이터["관객구간"]
    .value_counts()
    .sort_index()
)

가장많은구간 = 구간별영화수.idxmax()
가장많은구간영화수 = 구간별영화수.max()

가장많은관객영화 = 관객데이터.loc[
    관객데이터["total_audi"].idxmax()
]

영화이름 = 가장많은관객영화["movieNm"]
총관객수 = 가장많은관객영화["total_audi"]

st.write(
    f"대부분의 영화는 **{가장많은구간.left:,.0f}명~"
    f"{가장많은구간.right:,.0f}명** 구간에 몰려 있으며, "
    f"이 구간에는 **{가장많은구간영화수}편**의 영화가 있습니다."
)

st.write(
    f"총 관객이 가장 많은 영화는 **{영화이름}**으로, "
    f"총 관객은 **{총관객수:,.0f}명**입니다."
)

st.text_input(
    "이 그래프로 알 수 있는 것",
    key="note3"
)


st.divider()


# ==================================================
# 4. 개봉일 스크린수와 총 관객의 관계
# ==================================================
st.header("4. 개봉일 스크린수와 총 관객의 관계")

산점도데이터 = df.dropna(
    subset=[
        "first_scrn",
        "total_audi",
        "movieNm",
        "장르"
    ]
).copy()

fig = px.scatter(
    산점도데이터,
    x="first_scrn",
    y="total_audi",
    color="장르",
    hover_name="movieNm",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객",
        "장르": "장르"
    }
)

fig.update_traces(
    hovertemplate=
    "<b>%{hovertext}</b><br>"
    "개봉일 스크린수: %{x:,.0f}개<br>"
    "총 관객: %{y:,.0f}명"
    "<extra></extra>"
)

fig.update_layout(
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.text_input(
    "이 그래프로 알 수 있는 것",
    key="note4"
)


st.divider()


# ==================================================
# 5. 장르별 총 관객 박스플롯
# ==================================================
st.header("5. 장르별 총 관객 분포 (박스플롯)")

장르별영화수 = df["장르"].value_counts()

많은장르 = 장르별영화수[
    장르별영화수 >= 10
].index

박스플롯데이터 = df[
    df["장르"].isin(많은장르)
].dropna(
    subset=[
        "장르",
        "total_audi",
        "movieNm"
    ]
).copy()

fig = px.box(
    박스플롯데이터,
    x="장르",
    y="total_audi",
    points="outliers",
    labels={
        "장르": "장르",
        "total_audi": "총 관객"
    }
)

fig.update_layout(
    xaxis_title="장르",
    yaxis_title="총 관객"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.text_input(
    "이 그래프로 알 수 있는 것",
    key="note5"
)


st.divider()


# ==================================================
# 6. 첫 주 관객을 점 크기로 표현한 버블 그래프
# ==================================================
st.header("6. 개봉일 스크린수와 총 관객의 관계 (버블 그래프)")

버블데이터 = df.dropna(
    subset=[
        "first_scrn",
        "total_audi",
        "first_week_audi",
        "movieNm",
        "장르"
    ]
).copy()

# 버블 크기로 사용할 값이 0보다 큰 영화만 사용
버블데이터 = 버블데이터[
    버블데이터["first_week_audi"] > 0
].copy()

fig = px.scatter(
    버블데이터,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="장르",
    hover_name="movieNm",
    size_max=50,
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객",
        "first_week_audi": "첫 주 관객",
        "장르": "장르"
    }
)

fig.update_traces(
    hovertemplate=
    "<b>%{hovertext}</b><br>"
    "개봉일 스크린수: %{x:,.0f}개<br>"
    "총 관객: %{y:,.0f}명"
    "<extra></extra>"
)

fig.update_layout(
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.text_input(
    "이 그래프로 알 수 있는 것",
    key="note6"
)


st.divider()


# ==================================================
# 7. 제작 국가 → 장르 선버스트
# ==================================================
st.header("7. 제작 국가와 장르별 영화 편수 (선버스트)")

선버스트데이터 = df.dropna(
    subset=[
        "제작국가",
        "장르"
    ]
).copy()

# 빈 문자열을 기타로 처리
선버스트데이터["제작국가"] = (
    선버스트데이터["제작국가"]
    .replace("", "기타")
)

선버스트데이터["장르"] = (
    선버스트데이터["장르"]
    .replace("", "기타")
)

# 영화 한 편 = 1개로 세기 때문에
# values를 지정하지 않으면 행의 개수가 영화 편수가 됩니다.
fig = px.sunburst(
    선버스트데이터,
    path=["제작국가", "장르"]
)

fig.update_traces(
    hovertemplate=
    "%{label}<br>"
    "영화 편수: %{value}편"
    "<extra></extra>"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.text_input(
    "이 그래프로 알 수 있는 것",
    key="note7"
)


st.divider()


# ==================================================
# 다음 그래프
# ==================================================
st.header("8. (다음 그래프를 여기에 추가)")
