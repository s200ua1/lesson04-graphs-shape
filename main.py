# --------------------------------------------------
# 그래프 2. 장르별 영화 총 관객 트리맵
# --------------------------------------------------
st.header("2. 장르별 영화 총 관객 트리맵")

# total_audi를 숫자로 변환합니다
df["total_audi"] = pd.to_numeric(df["total_audi"], errors="coerce")

fig = px.treemap(
    df,
    path=["장르", "movieNm"],
    values="total_audi",
)

# 칸에 마우스를 올리면 영화명과 총 관객이 보이게 합니다
fig.update_traces(
    hovertemplate="영화명: %{label}<br>총 관객: %{value:,.0f}명<extra></extra>"
)

st.plotly_chart(fig, width="stretch")


# '이 그래프로 알 수 있는 것' 한 문장을 적는 자리
st.text_input("이 그래프로 알 수 있는 것", key="note2")


st.divider()


# 앞으로 그래프를 계속 추가할 구역
st.header("3. (다음 그래프를 여기에 추가)")
