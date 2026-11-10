import streamlit as st
import plotly.express as px
import pandas as pd

from report_data import file

st.set_page_config(
    page_title="Manufacturing Reprot",
    layout="wide"
)

st.title("Manufacturing Production Report")

uploaded_file = st.sidebar.file_uploader(
    "Upload your excel file",
    type=["xlsx","csv"]
)


if "data" not in st.session_state:
    st.session_state.data = None

if uploaded_file is not None:
    st.session_state.data = pd.read_excel(uploaded_file)

    report = file(st.session_state.data)
    st.sidebar.subheader("Dashboard Navigation")
    dashboard = st.sidebar.radio(
        "Select Dashboard",
        ["Production","Sales","Operations"]
    )


    st.sidebar.success("Excel file uploaded successfully")

    st.subheader("Raw Data")
    st.dataframe(report.f_path,height=300)

    tab1,tab2,tab3,tab4 = st.tabs([
        "Department","Shift","Sales Channel"," "
    ])
    if dashboard =="Production":
        with tab1:
            st.subheader("Department-wise Production")

            department_data = report.department_groupby()

            fig1 = px.bar(
                department_data,
                x="Department",
                y="Total_production",
                color="Department",
                text="Total_production",
                title="Department-wise Production"
            )
            fig1.update_traces(textposition="outside")
            st.plotly_chart(fig1,use_container_width=True)
            st.dataframe(department_data)

        with tab2:
            st.subheader("Shift-wise Production")
            shift_data = report.shift_groupby()

            fig2 = px.bar(
                shift_data,
                x="Shift",
                y="Total_Production",
                color="Shift",
                text="Total_Production",
                title="Department-wise Production"
            )
            fig2.update_traces(textposition="outside")
            st.plotly_chart(fig2,use_container_width=True)
            st.dataframe(shift_data)

        with tab3:
            sales_channel = report.sales_channel_groupby()
            fig = px.bar(
                sales_channel,
                x="Sales_Channel",
                y="total_production",
                color="total_production",
                text="total_production",
                title="Sales Channel-wise Production"
            )
            fig.update_traces(textposition = "outside")
            st.plotly_chart(fig,use_container_width=True)


    elif dashboard == "Sales":
        with tab3:
            st.subheader("Sales Dashboard")
            sales_channel = report.sales_channel_groupby()
            st.dataframe(sales_channel)
            fig = px.bar(
                sales_channel,
                x="Sales_Channel",
                y="total_sales",    
                color="total_sales",
                text="total_sales",
                title="Sales Channel-wise Sales"
            )
            fig.update_traces(textposition = "outside")
            st.plotly_chart(fig,use_container_width=True)


else:
    st.sidebar.info("Please upload an excel file to view the report")
