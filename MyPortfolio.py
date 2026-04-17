# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.19.10",
#     "pandas>=2.3.3",
#     "plotly>=6.5.1",
#     "pyarrow>=22.0.0",
#     "pyzmq>=27.1.0",
#     "numpy>=2.0.0",
# ]
# ///

import marimo

__generated_with = "0.19.11"
app = marimo.App()


@app.cell
def _(mo):
    mo.md(
        r"""
---
## 🎓 Personal Portfolio Webpage
Combine everything learned so far (e.g., data loading, preparation, and visualization) into a multi-tabbed webpage featuring an interactive chart and dashboard.
"""
    )
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import plotly.express as px
    import numpy as np
    return mo, np, pd, px


@app.cell
def _(pd):
    csv_url = "https://gist.githubusercontent.com/DrAYim/80393243abdbb4bfe3b45fef58e8d3c8/raw/ed5cfd9f210bf80cb59a5f420bf8f2b88a9c2dcd/sp500_ZScore_AvgCostofDebt.csv"

    df_final = pd.read_csv(csv_url)
    df_final = df_final.dropna(subset=["AvgCost_of_Debt", "Z_Score_lag", "Sector_Key"])
    df_final = df_final[df_final["AvgCost_of_Debt"] < 5]
    df_final["Debt_Cost_Percent"] = df_final["AvgCost_of_Debt"] * 100
    df_final["Market_Cap_B"] = df_final["Market_Cap"] / 1e9

    return (df_final,)


@app.cell
def _(df_final, mo):
    all_sectors = sorted(df_final["Sector_Key"].unique().tolist())

    sector_dropdown = mo.ui.multiselect(
        options=all_sectors,
        value=all_sectors[:3],
        label="Filter by Sector",
    )

    cap_slider = mo.ui.slider(
        start=0,
        stop=200,
        step=10,
        value=0,
        label="Min Market Cap ($ Billions)",
    )

    return cap_slider, sector_dropdown


@app.cell
def _(cap_slider, df_final, sector_dropdown):
    filtered_portfolio = df_final[
        (df_final["Sector_Key"].isin(sector_dropdown.value))
        & (df_final["Market_Cap_B"] >= cap_slider.value)
    ]

    count = len(filtered_portfolio)
    return count, filtered_portfolio


@app.cell
def _(count, filtered_portfolio, mo, np, pd, px):
    if count == 0:
        empty_fig = px.scatter(
            title="No data found for the selected filters. Adjust your selections."
        )
        chart_element = mo.ui.plotly(empty_fig)

        empty_stats = pd.DataFrame(
            {"Message": ["No descriptive statistics available for the current filters."]}
        )
        stats_table = mo.ui.table(empty_stats, label="Descriptive Statistics")

    else:
        fig_portfolio = px.scatter(
            filtered_portfolio,
            x="Z_Score_lag",
            y="Debt_Cost_Percent",
            color="Sector_Key",
            size="Market_Cap_B",
            hover_name="Name",
            title=f"Cost of Debt vs. Z-Score ({count} observations)",
            labels={
                "Z_Score_lag": "Altman Z-Score (lagged)",
                "Debt_Cost_Percent": "Avg. Cost of Debt (%)",
            },
            template="presentation",
            width=900,
            height=600,
        )

        fig_portfolio.add_vline(
            x=1.81,
            line_dash="dash",
            line_color="red",
            annotation=dict(
                text="Distress Threshold (Z-Score = 1.81)",
                font=dict(color="red"),
                x=1.5,
                xref="x",
                y=1.07,
                yref="paper",
                showarrow=False,
                yanchor="top",
            ),
        )

        fig_portfolio.add_vline(
            x=2.99,
            line_dash="dash",
            line_color="green",
            annotation=dict(
                text="Safe Threshold (Z-Score = 2.99)",
                font=dict(color="green"),
                x=3.10,
                xref="x",
                y=1.02,
                yref="paper",
                showarrow=False,
                yanchor="top",
            ),
        )

        if len(filtered_portfolio) > 2:
            x = filtered_portfolio["Z_Score_lag"].astype(float)
            y = filtered_portfolio["Debt_Cost_Percent"].astype(float)

            slope, intercept = np.polyfit(x, y, 1)
            x_line = np.linspace(x.min(), x.max(), 100)
            y_line = intercept + slope * x_line
            r2 = np.corrcoef(x, y)[0, 1] ** 2

            line_trace = px.line(x=x_line, y=y_line).data[0]
            fig_portfolio.add_trace(line_trace)
            fig_portfolio.add_annotation(
                text=f"Regression line – R² = {r2:.2f}",
                xref="paper",
                yref="paper",
                x=0.02,
                y=0.95,
                showarrow=False,
                font=dict(color="black"),
            )

        chart_element = mo.ui.plotly(fig_portfolio)

        summary = (
            filtered_portfolio[
                ["Z_Score_lag", "Debt_Cost_Percent", "Market_Cap_B"]
            ]
            .describe()
            .round(2)
            .reset_index()
        )
        stats_table = mo.ui.table(summary, label="Descriptive Statistics")

    travel_data = pd.DataFrame(
        {
            "City": ["London", "New York", "Tokyo", "Sydney", "Paris"],
            "Lat": [51.5, 40.7, 35.6, -33.8, 48.8],
            "Lon": [-0.1, -74.0, 139.6, 151.2, 2.3],
            "Visit_Year_str": ["2022", "2023", "2024", "2021", "2023"],
        }
    )

    years = sorted(travel_data["Visit_Year_str"].unique(), key=int)

    fig_travel = px.scatter_geo(
        travel_data,
        lat="Lat",
        lon="Lon",
        hover_name="City",
        color="Visit_Year_str",
        category_orders={"Visit_Year_str": years},
        color_discrete_sequence=px.colors.qualitative.Plotly,
        projection="natural earth",
        title="My Travel Footprint",
        labels={"Visit_Year_str": "Visit Year"},
    )

    fig_travel.update_traces(marker=dict(size=12))

    return chart_element, fig_travel, stats_table


@app.cell
def _(cap_slider, chart_element, fig_travel, mo, sector_dropdown, stats_table):
    tab_cv = mo.md(
        """
### 👋 About Me

**Name:** Malachi Olagbaju  
**Course:** BSc Accounting & Finance (2025 – Present), Bayes Business School

**Summary:**  
I am a first year accounting and finance student fascinated by how data analytics, AI, and financial systems interact in real-world decision-making.

**Core Skills:**  
- 🐍 Python Programming (pandas, plotly, marimo)  
- 📊 Financial Model Design  
- 🧠 Analytical and Critical Thinking  
- 🗂️ Data Visualisation & Storytelling  
- 💼 Business Reporting & Presentation
"""
    )

    tab_data_content = mo.vstack(
        [
            mo.md(
                """
## 📊 Passion Project: Credit Risk Analysis

This project explores the relationship between company risk and borrowing costs.

Using real financial data, I:
- Analysed company credit risk using the Altman Z-score
- Compared risk against cost of debt
- Built an interactive dashboard using Python and Plotly
"""
            ),
            mo.callout(
                mo.md(
                    "Use the filters below to explore the relationship between borrowing costs and credit risk."
                ),
                kind="info",
            ),
            mo.hstack([sector_dropdown, cap_slider], justify="center", gap=2),
            chart_element,
            stats_table,
        ]
    )

    tab_personal = mo.vstack(
        [
            mo.md(
                """
## 🌍 Personal Interests

Outside of academics, I enjoy travelling and exploring new places.

On the map I have highlighted some of the cities that I have visited, showing my interest in global cultures and experiences.
"""
            ),
            mo.ui.plotly(fig_travel),
        ]
    )

    return tab_cv, tab_data_content, tab_personal


@app.cell
def _(mo, tab_cv, tab_data_content, tab_personal):
    app_tabs = mo.ui.tabs(
        {
            "📄 About Me": tab_cv,
            "📊 Passion Projects": tab_data_content,
            "✈️ Personal Interests": tab_personal,
        }
    )

    deployment_note = mo.callout(
        mo.md(
            "**Deployment:** Exported using `marimo export html-wasm` and hosted on GitHub Pages."
        ),
        kind="success",
    )

    mo.vstack(
        [
            mo.md("# **Malachi Olagbaju**"),
            deployment_note,
            app_tabs,
        ]
    )
    return


if __name__ == "__main__":
    app.run()