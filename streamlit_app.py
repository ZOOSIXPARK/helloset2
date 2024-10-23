import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from scipy import stats

# 페이지 설정
st.set_page_config(layout="wide", page_title="고객 종합 대시보드")

# 공통 차트 스타일 설정
CHART_THEME = 'seaborn'
COLOR_PALETTE = px.colors.qualitative.Set3
TEMPLATE = 'plotly_white'

def prepare_heatmap_data(df, row_col, col_col):
    # 크로스탭 생성
    cross_tab = pd.crosstab(df[row_col], df[col_col])
    # 값을 float 타입으로 변환
    cross_tab = cross_tab.astype(float)
    return cross_tab

def get_chart_layout(title='', legend_position='default'):
    layout = dict(
        title=title,
        template=TEMPLATE,
        title_x=0.3,
        font=dict(family="Malgun Gothic", size=12),
        margin=dict(t=50, l=50, r=50, b=50),
        showlegend=True
    )
    
    if legend_position == 'default':
        layout['legend'] = dict(
            orientation="v",  # 수직 방향
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02
        )
    elif legend_position == 'bottom':
        layout['legend'] = dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    
    return layout

# 데이터 로드
@st.cache_data
def load_data():
    data = pd.read_csv('random_dataset.csv')
    return data

data = load_data()

# Streamlit 앱 시작
st.title('고객 분석 종합 대시보드')

# KPI 섹션 스타일
st.markdown("""
<style>
    .kpi-container {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        margin: 1rem 0;
    }
    .kpi-card {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin: 10px;
        flex: 1;
        min-width: 200px;
        text-align: center;
        transition: transform 0.3s ease;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
    }
    .kpi-title {
        font-size: 18px;
        color: #333;
        margin-bottom: 10px;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: bold;
        color: #2c3e50;
    }
    .kpi-icon {
        font-size: 24px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# KPI 데이터 계산
total_customers = len(data)
avg_total_value = data['총평가금액'].mean()
max_total_value = data['총평가금액'].max()
min_total_value = data['총평가금액'].min()
aggressive_investors_ratio = (data['투자성향'] == '5:공격투자형').mean()
avg_etf_stocks = data['ETF종목수'].mean()
min_etf_stocks = data['ETF종목수'].min()
max_etf_stocks = data['ETF종목수'].max()

# 각 투자성향별 고객 수 계산
investor_counts = data['투자성향'].value_counts()
max_investor_type = investor_counts.idxmax()
min_investor_type = investor_counts.idxmin()

# 각 연령대별 고객 수 계산
age_group_counts = data['연령대'].value_counts()
max_age_group = age_group_counts.idxmax()
min_age_group = age_group_counts.idxmin()

# 각 지역별 고객 수 계산
region_counts = data['지역명'].value_counts()
max_region = region_counts.idxmax()
min_region = region_counts.idxmin()

# KPI 카드 생성
st.markdown("<h2 style='text-align: left;'>주요 고객 지표 (KPI)</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: left; font-size: 25px;'>분석일자 : 2024/09/30</p>", unsafe_allow_html=True)

kpi_html = f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-icon">👥</div>
        <div class="kpi-title">총 고객 수</div>
        <div class="kpi-value">{total_customers:,}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">💰</div>
        <div class="kpi-title">평균 총평가금액</div>
        <div class="kpi-value">₩{avg_total_value:,.0f}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">📈</div>
        <div class="kpi-title">최대 총평가금액</div>
        <div class="kpi-value">₩{max_total_value:,.0f}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">📉</div>
        <div class="kpi-title">최소 총평가금액</div>
        <div class="kpi-value">₩{min_total_value:,.0f}</div>
    </div>
</div>
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-icon">📊</div>
        <div class="kpi-title">최다 투자성향</div>
        <div class="kpi-value">{max_investor_type}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">📉</div>
        <div class="kpi-title">최소 투자성향</div>
        <div class="kpi-value">{min_investor_type}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">🧓</div>
        <div class="kpi-title">최다 연령대</div>
        <div class="kpi-value">{max_age_group}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">👶</div>
        <div class="kpi-title">최소 연령대</div>
        <div class="kpi-value">{min_age_group}</div>
    </div>
</div>
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-icon">📍</div>
        <div class="kpi-title">최다 거주지역</div>
        <div class="kpi-value">{max_region}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">🗺️</div>
        <div class="kpi-title">최소 거주지역</div>
        <div class="kpi-value">{min_region}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">📈</div>
        <div class="kpi-title">최대 ETF 보유수</div>
        <div class="kpi-value">{max_etf_stocks}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">📉</div>
        <div class="kpi-title">최소 ETF 보유수</div>
        <div class="kpi-value">{min_etf_stocks}</div>
    </div>
</div>
"""

st.markdown(kpi_html, unsafe_allow_html=True)
# 고객 상세 분석
st.header('고객 상세 분석')

# 탭 생성
tabs = st.tabs(['투자성향 분석', '연령대 분석', '지역 분석', '자산 분석'])

# 투자성향 분석의 파이 차트 부분 수정
with tabs[0]:
    st.subheader('투자성향 분석')
    col1, col2 = st.columns(2)
    
    with col1:
        # 투자성향 분포 (파이 차트)
        investment_style = data['투자성향'].value_counts()
        fig_style = px.pie(
            values=investment_style.values,
            names=investment_style.index,
            color_discrete_sequence=COLOR_PALETTE,
            title='투자성향 분포'
        )
        fig_style.update_layout(**get_chart_layout('투자성향 분포', 'bottom'))
        st.plotly_chart(fig_style, use_container_width=True)
        
        # 나머지 차트들은 기본 legend 위치 사용
        style_asset_avg = data.groupby('투자성향')['총평가금액'].mean().sort_values(ascending=False)
        fig_style_asset = px.bar(
            x=style_asset_avg.index,
            y=style_asset_avg.values,
            title='투자성향별 평균 자산',
            labels={
                'x': '투자성향',
                'y': '평균 총평가금액 (원)'
            },
            color=style_asset_avg.index,
            color_discrete_sequence=COLOR_PALETTE
        )
        fig_style_asset.update_layout(**get_chart_layout('투자성향별 평균 자산'))
        fig_style_asset.update_traces(texttemplate='₩%{y:,.0f}', textposition='outside')
        st.plotly_chart(fig_style_asset, use_container_width=True)
    
    with col2:
        # 투자성향별 안전자산 비율 분포
        fig_style_safe = px.box(
            data,
            x='투자성향',
            y='안전자산비율',
            title='투자성향별 안전자산 비율 분포',
            labels={
                'x': '투자성향',
                'y': '안전자산비율 (%)'
            },
            color='투자성향',
            color_discrete_sequence=COLOR_PALETTE
        )
        fig_style_safe.update_layout(
            title='투자성향별 안전자산 비율 분포',
            template=TEMPLATE,
            title_x=0.3,
            font=dict(family="Malgun Gothic", size=12),
            margin=dict(t=50, l=50, r=50, b=50),
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.02
            )
        )
        st.plotly_chart(fig_style_safe, use_container_width=True)
        
        # 투자성향별 ETF 보유 현황
        style_etf_avg = data.groupby('투자성향')['ETF종목수'].mean().sort_values(ascending=False)
        fig_style_etf = px.bar(
            x=style_etf_avg.index,
            y=style_etf_avg.values,
            title='투자성향별 평균 ETF 보유수',
            labels={
                'x': '투자성향',
                'y': '평균 ETF 보유 종목수'
            },
            color=style_etf_avg.index,
            color_discrete_sequence=COLOR_PALETTE
        )
        fig_style_etf.update_layout(**get_chart_layout('투자성향별 평균 ETF 보유수'))
        fig_style_etf.update_traces(texttemplate='%{y:.1f}개', textposition='outside')
        st.plotly_chart(fig_style_etf, use_container_width=True)

with tabs[1]:
    st.subheader('연령대 분석')
    col1, col2 = st.columns(2)
    
    with col1:
        # 연령대별 평균 자산 규모
        age_asset_avg = data.groupby('연령대')['총평가금액'].mean().sort_values(ascending=False)
        fig_age_asset = px.bar(
            x=age_asset_avg.index,
            y=age_asset_avg.values,
            title='연령대별 평균 자산',
            labels={
                'x': '연령대',
                'y': '평균 총평가금액 (원)'
            },
            color=age_asset_avg.index,
            color_discrete_sequence=COLOR_PALETTE
        )
        fig_age_asset.update_layout(**get_chart_layout('연령대별 평균 자산'))
        fig_age_asset.update_traces(texttemplate='₩%{y:,.0f}', textposition='outside')
        st.plotly_chart(fig_age_asset, use_container_width=True)
        
        # 연령대별 투자성향 분포 (히트맵)
        # 연령대별 투자성향 분포 (히트맵) 수정
        age_style_dist = prepare_heatmap_data(data, '연령대', '투자성향')
        fig_age_style = px.imshow(
            age_style_dist.values,  # numpy array로 변환
            x=age_style_dist.columns,  # x축 레이블
            y=age_style_dist.index,    # y축 레이블
            title='연령대별 투자성향 분포',
            labels=dict(x='투자성향', y='연령대', color='고객 수'),
            color_continuous_scale='YlOrRd',
            aspect='auto'
        )
        fig_age_style.update_layout(**get_chart_layout('연령대별 투자성향 분포'))
        fig_age_style.update_traces(text=age_style_dist.values.astype(int), 
                          texttemplate='%{text}명')
        st.plotly_chart(fig_age_style, use_container_width=True)
    
    with col2:
        # 연령대별 안전자산 비율 분포
        fig_age_safe = px.box(
            data,
            x='연령대',
            y='안전자산비율',
            title='연령대별 안전자산 비율 분포',
            labels={
                'x': '연령대',
                'y': '안전자산비율 (%)'
            },
            color='연령대',
            color_discrete_sequence=COLOR_PALETTE
        )
        fig_age_safe.update_layout(**get_chart_layout('연령대별 안전자산 비율 분포'))
        st.plotly_chart(fig_age_safe, use_container_width=True)
        
        # 연령대별 ETF 보유 현황
        age_etf_avg = data.groupby('연령대')['ETF종목수'].mean().sort_values(ascending=False)
        fig_age_etf = px.bar(
            x=age_etf_avg.index,
            y=age_etf_avg.values,
            title='연령대별 평균 ETF 보유수',
            labels={
                'x': '연령대',
                'y': '평균 ETF 보유 종목수'
            },
            color=age_etf_avg.index,
            color_discrete_sequence=COLOR_PALETTE
        )
        fig_age_etf.update_layout(**get_chart_layout('연령대별 평균 ETF 보유수'))
        fig_age_etf.update_traces(texttemplate='%{y:.1f}개', textposition='outside')
        st.plotly_chart(fig_age_etf, use_container_width=True)
with tabs[2]:
    st.subheader('지역별 분석')
    col1, col2 = st.columns(2)
    
    with col1:
        # 지역별 투자자 수
        region_investors = data['지역명'].value_counts()
        fig_region = px.bar(
            x=region_investors.index,
            y=region_investors.values,
            title='지역별 투자자 분포',
            labels={
                'x': '지역명',
                'y': '투자자 수 (명)'
            },
            color=region_investors.index,
            color_discrete_sequence=COLOR_PALETTE
        )
        fig_region.update_layout(**get_chart_layout('지역별 투자자 분포'))
        fig_region.update_traces(texttemplate='%{y:,}명', textposition='outside')
        st.plotly_chart(fig_region, use_container_width=True)
        
        region_age = prepare_heatmap_data(data, '지역명', '연령대')
        fig_region_age = px.imshow(
            region_age.values,
            x=region_age.columns,
            y=region_age.index,
            title='지역별 연령대 분포',
            labels=dict(x='연령대', y='지역명', color='고객 수'),
            color_continuous_scale='YlOrRd',
            aspect='auto'
        )
        fig_region_age.update_layout(**get_chart_layout('지역별 연령대 분포'))
        fig_region_age.update_traces(text=region_age.values.astype(int), 
                                   texttemplate='%{text}명')
        st.plotly_chart(fig_region_age, use_container_width=True)
    
    with col2:
        # 지역별 평균 자산
        region_asset_avg = data.groupby('지역명')['총평가금액'].mean().sort_values(ascending=False)
        fig_region_asset = px.bar(
            x=region_asset_avg.index,
            y=region_asset_avg.values,
            title='지역별 평균 자산',
            labels={
                'x': '지역명',
                'y': '평균 총평가금액 (원)'
            },
            color=region_asset_avg.index,
            color_discrete_sequence=COLOR_PALETTE
        )
        fig_region_asset.update_layout(**get_chart_layout('지역별 평균 자산'))
        fig_region_asset.update_traces(texttemplate='₩%{y:,.0f}', textposition='outside')
        st.plotly_chart(fig_region_asset, use_container_width=True)
        
        # 지역별 투자성향 분포 (히트맵) 수정
        region_style = prepare_heatmap_data(data, '지역명', '투자성향')
        fig_region_style = px.imshow(
            region_style.values,
            x=region_style.columns,
            y=region_style.index,
            title='지역별 투자성향 분포',
            labels=dict(x='투자성향', y='지역명', color='고객 수'),
            color_continuous_scale='YlOrRd',
            aspect='auto'
        )
        fig_region_style.update_layout(**get_chart_layout('지역별 투자성향 분포'))
        fig_region_style.update_traces(text=region_style.values.astype(int), 
                             texttemplate='%{text}명')
        st.plotly_chart(fig_region_style, use_container_width=True)

with tabs[3]:
    st.subheader('자산 규모별 분석')
    col1, col2 = st.columns(2)
    
    with col1:
        # 자산규모별 투자자 분포
        asset_size = data['자산규모'].value_counts()
        fig_asset = px.pie(
            values=asset_size.values,
            names=asset_size.index,
            title='자산규모별 투자자 분포',
            color_discrete_sequence=COLOR_PALETTE
        )
        fig_asset.update_layout(**get_chart_layout('자산규모별 투자자 분포', 'bottom'))
        fig_asset.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='%{label}<br>고객 수: %{value:,}명<br>비율: %{percent}'
        )
        st.plotly_chart(fig_asset, use_container_width=True)
    
    with col2:
        # 자산규모별 안전자산 비율 분포
        fig_asset_safe = px.box(
            data,
            x='자산규모',
            y='안전자산비율',
            title='자산규모별 안전자산 비율 분포',
            labels={
                'x': '자산규모',
                'y': '안전자산비율 (%)'
            },
            color='자산규모',
            color_discrete_sequence=COLOR_PALETTE
        )
        fig_asset_safe.update_layout(**get_chart_layout('자산규모별 안전자산 비율 분포'))
        st.plotly_chart(fig_asset_safe, use_container_width=True)
        
        # 자산규모별 투자성향 분포 (히트맵) 수정
        asset_style = prepare_heatmap_data(data, '자산규모', '투자성향')
        fig_asset_style = px.imshow(
            asset_style.values,
            x=asset_style.columns,
            y=asset_style.index,
            title='자산규모별 투자성향 분포',
            labels=dict(x='투자성향', y='자산규모', color='고객 수'),
            color_continuous_scale='YlOrRd',
            aspect='auto'
        )
        fig_asset_style.update_layout(**get_chart_layout('자산규모별 투자성향 분포'))
        fig_asset_style.update_traces(text=asset_style.values.astype(int), 
                            texttemplate='%{text}명')
        st.plotly_chart(fig_asset_style, use_container_width=True)
# 고급 분석 섹션
st.header('고급 분석')
col1, col2 = st.columns(2)

with col1:
    # ETF 종목수와 총평가금액의 상관관계
    marker_sizes = np.log10(data['총평가금액'].clip(lower=1)) * 5
    fig_scatter = px.scatter(
        data,
        x='ETF종목수',
        y='총평가금액',
        color='투자성향',
        size=marker_sizes,
        hover_data=['연령대', '지역명'],
        title='ETF 종목수와 총평가금액의 관계',
        labels={
            'ETF종목수': 'ETF 보유 종목수',
            '총평가금액': '총평가금액 (원)',
            '투자성향': '투자성향',
            '연령대': '연령대',
            '지역명': '지역명'
        },
        color_discrete_sequence=COLOR_PALETTE
    )
    fig_scatter.update_layout(
        **get_chart_layout('ETF 종목수와 총평가금액의 관계'),
        hovermode='closest'
    )
    # 금액 포맷 설정
    fig_scatter.update_layout(
        yaxis=dict(
            tickformat=',.0f',
            tickprefix='₩'
        )
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    # 안전자산비율과 총평가금액의 관계
    fig_safe = px.box(
        data,
        x='안전자산비율',
        y='총평가금액',
        color='투자성향',
        title='안전자산비율과 총평가금액의 관계',
        labels={
            '안전자산비율': '안전자산비율 (%)',
            '총평가금액': '총평가금액 (원)',
            '투자성향': '투자성향'
        },
        color_discrete_sequence=COLOR_PALETTE
    )
    fig_safe.update_layout(
        **get_chart_layout('안전자산비율과 총평가금액의 관계')
    )
    # 금액 포맷 설정
    fig_safe.update_layout(
        yaxis=dict(
            tickformat=',.0f',
            tickprefix='₩'
        )
    )
    st.plotly_chart(fig_safe, use_container_width=True)

# 통계적 분석
st.header('통계적 분석')

# 데이터 타입 변환을 위한 전처리
numeric_data = data.copy()
numeric_data['총평가금액'] = pd.to_numeric(numeric_data['총평가금액'], errors='coerce')
numeric_data['ETF종목수'] = pd.to_numeric(numeric_data['ETF종목수'], errors='coerce')
# 안전자산비율에서 % 기호 제거 후 숫자로 변환
numeric_data['안전자산비율'] = pd.to_numeric(numeric_data['안전자산비율'].str.rstrip('%'), errors='coerce')

# 상관관계 분석을 위한 주요 변수 정의
analysis_vars = ['ETF종목수', '총평가금액', '안전자산비율']

# 상관관계 분석 결과를 저장할 리스트
correlation_results = []

# 모든 가능한 변수 쌍에 대해 상관관계 분석 수행
for i in range(len(analysis_vars)):
    for j in range(i+1, len(analysis_vars)):
        var1 = analysis_vars[i]
        var2 = analysis_vars[j]
        
        # 결측치 제거 후 상관관계 계산
        valid_data = numeric_data[[var1, var2]].dropna()
        if len(valid_data) > 0:
            correlation, p_value = stats.pearsonr(valid_data[var1], valid_data[var2])
            
            correlation_results.append({
                '분석 항목': f'{var1}와(과) {var2}',
                '상관계수': correlation,
                'P-value': p_value,
                '해석': '강한 상관관계' if abs(correlation) > 0.5 
                       else '중간 상관관계' if abs(correlation) > 0.3 
                       else '약한 상관관계',
                '데이터 수': len(valid_data)
            })

# 상관관계 분석 결과를 데이터프레임으로 변환
corr_df = pd.DataFrame(correlation_results)
corr_df['상관계수'] = corr_df['상관계수'].round(4)
corr_df['P-value'] = corr_df['P-value'].round(4)

# 스타일이 적용된 테이블로 표시
st.write("### 변수 간 상관관계 분석")
st.markdown("""
<style>
    .correlation-table {
        font-size: 16px;
        width: 100%;
        text-align: left;
        border-collapse: collapse;
    }
    .correlation-table th {
        background-color: #f0f2f6;
        padding: 12px;
        border: 1px solid #ddd;
    }
    .correlation-table td {
        padding: 12px;
        border: 1px solid #ddd;
    }
    .correlation-table tr:hover {
        background-color: #f5f5f5;
    }
</style>
""", unsafe_allow_html=True)

# HTML 테이블 생성
table_html = "<table class='correlation-table'>"
table_html += "<tr><th>분석 항목</th><th>상관계수</th><th>P-value</th><th>해석</th><th>데이터 수</th></tr>"
for _, row in corr_df.iterrows():
    table_html += f"<tr>"
    table_html += f"<td>{row['분석 항목']}</td>"
    table_html += f"<td>{row['상관계수']}</td>"
    table_html += f"<td>{row['P-value']}</td>"
    table_html += f"<td>{row['해석']}</td>"
    table_html += f"<td>{row['데이터 수']:,}</td>"
    table_html += "</tr>"
table_html += "</table>"

st.markdown(table_html, unsafe_allow_html=True)

# 분석 인사이트 부분 수정
st.subheader('주요 분석 인사이트')

# 각종 통계 계산 (numeric_data 사용)
avg_etf_by_age = numeric_data.groupby('연령대')['ETF종목수'].mean()
max_etf_age = avg_etf_by_age.idxmax()
max_etf_age_value = avg_etf_by_age.max()

avg_asset_by_age = numeric_data.groupby('연령대')['총평가금액'].mean()
max_asset_age = avg_asset_by_age.idxmax()
max_asset_age_value = avg_asset_by_age.max()

# 상관관계 결과를 쉽게 찾기 위한 dictionary 생성
corr_dict = {f"{row['분석 항목']}": row for _, row in corr_df.iterrows()}

st.markdown(f"""
#### 1. 투자 행태 분석
- 가장 많은 고객이 선택한 투자성향은 **{max_investor_type}**입니다.
- 평균적으로 고객들은 **{avg_etf_stocks:.1f}개**의 ETF를 보유하고 있습니다.
- **{max_etf_age}** 연령대가 가장 많은 평균 **{max_etf_age_value:.1f}개**의 ETF를 보유하고 있습니다.

#### 2. 자산 분포 분석
- 전체 고객의 평균 총평가금액은 **₩{avg_total_value:,.0f}**입니다.
- 가장 높은 평균 자산을 보유한 연령대는 **{max_asset_age}**로, 평균 **₩{max_asset_age_value:,.0f}**입니다.

#### 3. 상관관계 분석 결과
""")

# 각 상관관계에 대한 세부 분석 표시
for _, row in corr_df.iterrows():
    significance = "통계적으로 유의미함" if row['P-value'] < 0.05 else "통계적으로 유의미하지 않음"
    direction = "양의" if row['상관계수'] > 0 else "음의"
    strength = row['해석'].replace('상관관계', '')
    
    st.markdown(f"""
    - **{row['분석 항목']}**:
        - {direction} {strength}상관성을 보임 (상관계수: {row['상관계수']})
        - {significance} (P-value: {row['P-value']})
        - 분석에 사용된 데이터: {row['데이터 수']:,}개
        
        {'높은 값의 변수가 서로 양의 방향으로 움직이는 경향이 있습니다.' if row['상관계수'] > 0 else '한 변수가 증가할 때 다른 변수는 감소하는 경향이 있습니다.'}
    """)

# 전반적인 분석 요약
st.markdown("""
#### 4. 종합 분석 요약
1. **투자 성향과 자산 관리**
   - 투자성향별로 뚜렷한 자산 운용 패턴이 관찰됩니다.
   - ETF 투자와 자산 규모 사이의 관계가 확인됩니다.

2. **연령대별 특성**
   - 연령대에 따라 투자 스타일의 차이가 나타납니다.
   - 각 연령대별로 선호하는 투자 방식이 구분됩니다.

3. **안전자산 선호도**
   - 안전자산 비율은 투자성향과 총자산 규모에 따라 다양한 분포를 보입니다.
   - 연령대가 높아질수록 안전자산 선호도가 증가하는 경향이 있습니다.
""")

# 시각화 가이드 추가
st.sidebar.markdown("""
### 📊 데이터 시각화 가이드
- 모든 금액은 원화(₩)로 표시
- 비율은 백분율(%)로 표시
- 상관계수 범위: -1 ~ +1
- P-value < 0.05: 통계적으로 유의미
""")