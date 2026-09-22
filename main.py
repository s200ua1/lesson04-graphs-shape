```python
import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

# 데이터 주소
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 개봉일 변환
    df["openDt"] = pd.to_datetime(
        df["openDt"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 여러 장르가 있는 경우 첫 번째 장르만 사용
    df["genre_first"] = (
        df["genre"]
        .fillna("미분류")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    df.loc[df["genre_first"] == "", "genre_first"] = "미분류"

    # 총 관객을 숫자로 변환
    df["total_audi"] = pd.to_numeric(
        df["total_audi"],
        errors="coerce"
    ).fillna(0)

    return df


df = load_data()


# =============================
# 1. 장르별 영화 편수
# =============================
st.header("1. 장르별 영화 편수")

genre_counts = (
    df["genre_first"]
    .value_counts()
    .reset_index()
)

genre_counts.columns = ["장르", "영화 편수"]

fig1 = px.pie(
    genre_counts,
    names="장르",
    values="영화 편수",
    hole=0.45,
    title="장르별 영화 편수"
)

fig1.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    )
)

fig1.update_layout(
    height=550,
    legend_title="장르"
)

st.plotly_chart(fig1, use_container_width=True)

st.text_area(
    "이 그래프로 알 수 있는 것",
    placeholder="장르별 영화 편수의 분포를 보고 알 수 있는 내용을 한 문장으로 적어 보세요.",
    height=80,
    key="graph1_note"
)


# =============================
# 2. 장르별 영화 총 관객 트리맵
# =============================
st.divider()

st.header("2. 장르별 영화 총 관객 트리맵")

fig2 = px.treemap(
    df,
    path=["genre_first", "movieNm"],
    values="total_audi",
    title="장르별 영화 총 관객",
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    height=650
)

st.plotly_chart(fig2, use_container_width=True)

st.text_area(
    "이 그래프로 알 수 있는 것",
    placeholder="장르별로 어떤 영화의 총 관객이 많았는지 트리맵을 보고 한 문장으로 적어 보세요.",
    height=80,
    key="graph2_note"
)
```
