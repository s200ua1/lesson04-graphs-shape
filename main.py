# --------------------------------------------------
# 그래프 6. 첫 주 관객을 크기로 넣은 버블 그래프
# --------------------------------------------------
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

# 첫 주 관객을 숫자형으로 변환합니다
버블데이터["first_week_audi"] = pd.to_numeric(
    버블데이터["first_week_audi"],
    errors="coerce"
)

버블데이터 = 버블데이터.dropna(
    subset=["first_week_audi"]
)

fig = px.scatter(
    버블데이터,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="장르",
    hover_name="movieNm",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객",
        "first_week_audi": "첫 주 관객",
        "장르": "장르"
    },
    size_max=50
)

# 점에 마우스를 올리면 영화명과 주요 정보가 보이게 합니다
fig.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>"
                  "개봉일 스크린수: %{x:,.0f}개<br>"
                  "총 관객: %{y:,.0f}명<br>"
                  "첫 주 관객: %{marker.size:,.0f}명"
                  "<extra></extra>"
)

fig.update_layout(
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객"
)

st.plotly_chart(fig, use_container_width=True)


st.text_input("이 그래프로 알 수 있는 것", key="note6")


st.divider()


# 앞으로 그래프를 계속 추가할 구역
st.header("7. (다음 그래프를 여기에 추가)")
