"""ROBERT"""
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from robo.db import get_engine
from web.pages.base import BasePage


saa_codes = [
    "이자수익_대체투자_기타/사모투자_PD-인수금융",
    "이자수익_해외채권_구조화채권_구조화채권",
    "이자수익_해외채권_Sovereign/Financial_Sovereign",
    "이자수익_해외채권_Sovereign/Financial_Financial",
    "이자수익_해외채권_Sovereign/Financial_Quasi-Sovereign/Muni",
    "이자수익_해외채권_회사채/사모사채_회사채",
    "이자수익_해외채권_회사채/사모사채_사모사채",
    "이자수익_대체투자_인프라_신재생",
    "이자수익_대체투자_인프라_발전",
    "이자수익_대체투자_인프라_기타-SOC",
    "이자수익_대체투자_인프라_BTOBOT",
    "이자수익_대체투자_인프라_BTL",
    "이자수익_대체투자_부동산_부동산담보",
    "이자수익_대체투자_부동산_부동산PF",
    "이자수익_대체투자_기타/사모투자_상품투자",
    "이자수익_대체투자_기타/사모투자_기타-사모투자",
    "이자수익_국내채권_회사채/사모사채_회사채",
    "이자수익_국내채권_회사채/사모사채_사모사채",
    "이자수익_국내채권_특수/금융채_금융채",
    "이자수익_국내채권_구조화채권_구조화채권",
    "이자수익_국내채권_채권형 수익증권_기타",
    "이자수익_국내채권_매자닌_기타",
    "수익추구_주식_상장/주식형 수익증권_기타",
    "수익추구_주식_비상장/PEF_기타",
    "ALM_유동성_단기자금_기타",
    "ALM_국내채권_국고채_기타",
    "기타_기타_기타_기타",
]


as_of_date = "기준일자"
inception_date = "발행일"
maturity_date = "만기일자"
last_coupon_date = "직전이자일"

position_id = "포지션ID"
asset_classification = "자산구분명"
security_classification = "유가증권분류명"
performance_classification = "실적분류코드"
portfolio_type = "포트폴리오 이름"
asset_class_1 = "자산군1명"
asset_class_2 = "자산군2명"
asset_class_3 = "자산군3명"
asset_class_4 = "자산군4명"
fixed_income_classification = "채권분류명"

applied_yield = "적용 수익률"
face_yield = "액면이자율"

interest_periods = "이자주기"

book_value = "장부금액(원화)"
face_value = "액면 금액(원화)"
fair_value = "공정가치(원화)"

product_type = "상품유형명"
product_name = "종목명"
account_name = "운용펀드명"
id_isin = "국제표준코드"


@st.cache_data()
def read_bs() -> pd.DataFrame:
    data = pd.read_sql(
        sql="SELECT * FROM balance_sheet",
        con=get_engine(),
        parse_dates=[as_of_date, inception_date, maturity_date, last_coupon_date],
    )
    return data


@st.cache_data()
def read_cf() -> pd.DataFrame:
    data = pd.read_sql(
        sql="SELECT * FROM bs_cashflow",
        con=get_engine(),
        parse_dates=["date"],
    )
    return data


def get_frequency() -> str:
    return str(st.selectbox(label="Frequency", options=["D", "M", "Q", "Y"], index=3))


def get_start() -> str:
    return str(st.date_input(label="Start", value=pd.Timestamp("now")))


def get_end() -> str:
    return str(
        st.date_input(
            label="Start", value=pd.Timestamp("now") + pd.DateOffset(years=30)
        )
    )


class Manager(BasePage):
    def load_page(self):
        bs_data = read_bs()
        bs_data.insert(loc=0, column="Check", value=True)

        col1, col2 = st.columns(2)
        with col1:
            portfolio_type_options = bs_data[portfolio_type].unique()
            selected_portfolio_type = st.multiselect(
                label="Portflio Type",
                options=portfolio_type_options,
                default=portfolio_type_options,
            )
            bs_data = bs_data[
                bs_data[portfolio_type].isin(values=selected_portfolio_type)
            ]
        with col2:
            product_type_options = bs_data[product_type].unique()
            selected_portfolio_type = st.multiselect(
                label="Product Type",
                options=product_type_options,
                default=product_type_options,
            )
            bs_data = bs_data[
                bs_data[product_type].isin(values=selected_portfolio_type)
            ]

        col1, col2, col3 = st.columns(3)

        with col1:
            cfstart = get_start()

        with col2:
            cfend = get_end()

        with col3:
            frequency = get_frequency()

        with st.expander(label="See raw data", expanded=False):
            info_container = st.container()
            edited_df = st.data_editor(bs_data)  # 👈 An editable dataframe
            final_df = edited_df[edited_df["Check"]]
            with info_container:
                st.info(f"Number of raw data cheked: {len(final_df)}/{len(edited_df)}")

        total_fair_value_data = final_df.groupby(by=product_type)[fair_value].sum()
        total_fair_value_data = total_fair_value_data[total_fair_value_data != 0]

        col1, col2 = st.columns([1, 2])
        with col1:
            if not bs_data.empty:
                self.h4("Current Asset Allocation:")
                fig = go.Figure(
                    data=[
                        go.Pie(
                            labels=total_fair_value_data.index,
                            values=total_fair_value_data.values,
                        )
                    ]
                )
                self.plotly(fig, height=600)

        cf_data = read_cf()
        cf_data["cashflow_amount"] /= 100_000_000
        cf_data = cf_data[cf_data["position_id"].isin(final_df[position_id])]

        if not cf_data.empty:
            with col2:
                self.h4("Future Cash Flow:")
                include_matuirty = st.checkbox(label="Include Principal", value=True)
                if not include_matuirty:
                    cf_data = cf_data[cf_data["cashflow_type"] != "principal"]

                cf_data = (
                    cf_data.groupby(by=["date", "product_type"])["cashflow_amount"]
                    .sum()
                    .unstack()
                )
                cf_data.replace(0, np.nan, inplace=True)

                cf_data = (
                    cf_data.resample(frequency)
                    .sum()
                    .loc[cfstart:cfend]
                    .dropna(how="all")
                )

                self.note("단위: 억", align="right")
                ttcf = cf_data.sum(axis=1)
                fig = go.Figure()
                fig.add_trace(trace=go.Bar(x=ttcf.index, y=ttcf.values, name="Total"))
                fig.update_layout(barmode="stack", yaxis_tickformat=".2f")
                self.plotly(fig, height=200)
                fig = go.Figure()
                fig.update_traces([])
                for x in cf_data:
                    cf = cf_data[x].dropna()
                    fig.add_trace(trace=go.Bar(x=cf.index, y=cf.values, name=x))
                fig.update_layout(barmode="stack", yaxis_tickformat=".2f")
                self.plotly(fig, height=400)
        st.warning("SAA mapping 후 .... 비중확인 기능 개발 예정")

        st.write(bs_data["saa_code"].unique())

        self.upload_excel()

    def read_excel(self, file) -> pd.DataFrame:
        try:
            return pd.read_excel(file)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return pd.DataFrame()

    def upload_excel(self) -> None:
        with st.expander("Upload New Data"):
            uploaded_file = st.file_uploader("Upload Balance Sheet", type=["xlsx"])

            if uploaded_file is not None:
                with st.spinner(text="Uploading in progress..."):
                    bs_data = self.read_excel(uploaded_file)

                    # Assuming all the column names exist in the DataFrame and have appropriate data
                    columns_to_concat = [
                        asset_classification,
                        product_type,
                        security_classification,
                        performance_classification,
                        asset_class_2,
                        asset_class_3,
                        asset_class_4,
                        fixed_income_classification,
                    ]

                    for column in columns_to_concat:
                        bs_data[column] = bs_data[column].fillna("")

                    bs_data["saa_code"] = (
                        bs_data[columns_to_concat]
                        .astype(str)
                        .apply(lambda row: "".join(row), axis=1)
                    )

                    # Handle missing values
                    bs_data["saa_code"] = bs_data["saa_code"].fillna(
                        ""
                    )  # Fill missing values with an empty string

                    st.write(bs_data)

                    if bs_data is not None:
                        bs_data.to_sql(
                            name="balance_sheet",
                            con=get_engine(),
                            if_exists="replace",
                            index=False,
                        )
                        st.cache_data.clear()
                        try:
                            saa_map = pd.read_sql(
                                sql="SELECT * FROM saa_mapping", con=get_engine()
                            )
                        except:
                            saa_map = pd.DataFrame(columns=["saa_code", "saa_custom"])

                        add_map = []
                        for saa_c in bs_data["saa_code"].unique():
                            if saa_c not in saa_map["saa_code"]:
                                add_map.append(
                                    {
                                        "saa_code": saa_c,
                                        "saa_custom": None,
                                    }
                                )

                        saa_map = pd.concat([saa_map, pd.DataFrame(add_map)])

                        saa_map.to_sql(
                            name="saa_map",
                            con=get_engine(),
                            if_exists="replace",
                            index=False,
                        )

                        cashflows = []
                        for _, bs_row in bs_data.iterrows():
                            if bs_row[product_type] in [
                                "외환 (FX)",
                                "통화 스왑(CRS)",
                                "채권선도",
                            ]:
                                continue

                            start = (
                                bs_row[last_coupon_date]
                                if pd.isna(bs_row[last_coupon_date])
                                else bs_row[as_of_date]
                                if pd.isna(bs_row[inception_date])
                                else bs_row[inception_date]
                            )
                            end = (
                                pd.Timestamp("now") + pd.DateOffset(years=10)
                                if pd.isna(bs_row[maturity_date])
                                else bs_row[maturity_date]
                            )
                            end = min(
                                end, pd.Timestamp("now") + pd.DateOffset(years=50)
                            )

                            periods = (
                                3
                                if bs_row[product_type] == "수익증권"
                                else 0
                                if bs_row[product_type] == "할인채"
                                else int(bs_row[interest_periods])
                            )

                            interest = int(bs_row[face_value] * bs_row[face_yield])
                            if interest == 0:
                                interest = int(
                                    bs_row[book_value] * bs_row[applied_yield]
                                )
                            interest = int(interest / 12 * periods / 100)
                            if (
                                interest != 0
                                and not pd.isna(start)
                                and not pd.isna(end)
                            ):
                                for date in pd.date_range(
                                    start=start,
                                    end=end,
                                    freq=pd.DateOffset(months=periods),
                                ):
                                    if date < pd.Timestamp("now"):
                                        continue

                                    cashflows.append(
                                        {
                                            "position_id": bs_row[position_id],
                                            "product_type": bs_row[product_type],
                                            "date": date,
                                            "cashflow_type": "interest",
                                            "cashflow_amount": interest,
                                        }
                                    )
                            if end is not None:
                                if end > pd.Timestamp("now"):
                                    cashflows.append(
                                        {
                                            "position_id": bs_row[position_id],
                                            "product_type": bs_row[product_type],
                                            "date": end,
                                            "cashflow_type": "principal",
                                            "cashflow_amount": bs_row[face_value]
                                            or bs_row[book_value],
                                        }
                                    )

                        cashflows = pd.DataFrame(cashflows)

                        cashflows.to_sql(
                            name="bs_cashflow",
                            con=get_engine(),
                            if_exists="replace",
                            index=False,
                        )
