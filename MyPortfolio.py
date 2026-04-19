# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.19.10",
#     "pandas>=2.3.3",
#     "plotly>=6.5.1",
#     "numpy>=2.0.0",
# ]
# ///




import marimo




__generated_with = "0.19.11"
app = marimo.App()








@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import plotly.express as px
    import numpy as np
    return mo, pd, px, np








@app.cell
def _(mo):
    mo.md(
        """
---
## 🎓 Personal Portfolio Webpage




Combine everything learned so far into a multi-tabbed webpage featuring an interactive chart and dashboard.
"""
    )








@app.cell
def _(pd):
    df_final = pd.DataFrame(
        {
            "Name": [
                "Apple", "Microsoft", "Amazon", "Google", "Tesla",
                "Meta", "JPMorgan", "Coca-Cola", "Nike", "Intel"
            ],
            "Sector_Key": [
                "Technology", "Technology", "Consumer", "Technology", "Automotive",
                "Technology", "Finance", "Consumer", "Consumer", "Technology"
            ],
            "Z_Score_lag": [3.4, 3.8, 2.7, 3.5, 2.1, 3.0, 2.6, 3.2, 2.8, 2.3],
            "AvgCost_of_Debt": [0.021, 0.018, 0.029, 0.022, 0.041, 0.027, 0.035, 0.024, 0.031, 0.038],
            "Market_Cap_B": [2800, 3000, 1800, 2000, 800, 1200, 500, 260, 180, 170],
        }
    )




    df_final["Debt_Cost_Percent"] = df_final["AvgCost_of_Debt"] * 100
    return df_final








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
        stop=3000,
        step=100,
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
        fig_portfolio = px.scatter(
            title="No data found for the selected filters. Adjust your selections."
        )
        summary = pd.DataFrame(
            {"Message": ["No descriptive statistics available for the current filters."]}
        )
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




        fig_portfolio.add_vline(x=1.81, line_dash="dash", line_color="red")
        fig_portfolio.add_vline(x=2.99, line_dash="dash", line_color="green")




        if len(filtered_portfolio) > 2:
            x = filtered_portfolio["Z_Score_lag"].astype(float)
            y = filtered_portfolio["Debt_Cost_Percent"].astype(float)
            slope, intercept = np.polyfit(x, y, 1)
            x_line = np.linspace(x.min(), x.max(), 100)
            y_line = intercept + slope * x_line
            line_trace = px.line(x=x_line, y=y_line).data[0]
            fig_portfolio.add_trace(line_trace)




        summary = (
            filtered_portfolio[
                ["Z_Score_lag", "Debt_Cost_Percent", "Market_Cap_B"]
            ]
            .describe()
            .round(2)
            .reset_index()
        )




    chart_element = mo.ui.plotly(fig_portfolio)
    stats_table = mo.ui.table(summary, label="Descriptive Statistics")
    return chart_element, stats_table








@app.cell
def _(mo):
    tab_cv = mo.md(
        """
### 👋 About Me




**Name:** Malachi Olagbaju  
**Course:** BSc Accounting & Finance (2025 – Present), Bayes Business School  




**Summary:**  
I am a first year accounting and finance student fascinated by how data analytics, AI, and financial systems interact in real-world decision-making.




**Core Skills:**  
- 🐍 Python Programming  
- 📊 Financial Model Design  
- 🧠 Analytical and Critical Thinking  
- 🗂️ Data Visualisation and Storytelling  
- 💼 Business Reporting and Presentation
"""
    )




    tab_personal = mo.md(
    """
## 🌍 Personal Interests

Outside of academics, I enjoy travelling and exploring new places, which has helped me develop a broader global perspective.

Some of the cities I have visited include:
- 🇪🇸 Tenerife (2021)
- 🇭🇺 Budapest (2022)
- 🇫🇷 Paris (2023)
- 🇺🇸 Dallas (2024)

Through these experiences, I have developed a strong interest in:
- 🌐 Global business environments  
- 📊 Understanding economic differences between countries  
- 🧠 Applying analytical thinking to real-world situations  

These interests complement my academic studies in Accounting & Finance, particularly in areas such as financial analysis, international markets, and data-driven decision making.
"""
)




    return tab_cv, tab_personal








@app.cell
def _(cap_slider, chart_element, mo, sector_dropdown, stats_table, tab_cv, tab_personal):

    tab_data_content = mo.vstack(
        [
            mo.md(
                """
## 📊 Passion Project: Credit Risk Analysis

This project explores the relationship between company risk and borrowing costs.

Using sample company data, I:
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

    app_tabs = mo.ui.tabs(
        {
            "📄 About Me": tab_cv,
            "📊 Passion Projects": tab_data_content,
            "✈️ Personal Interests": tab_personal,
        }
    )

    # 🔴 THIS LINE IS THE KEY FIX
    mo.output.replace(
        mo.vstack(
            [
                mo.md("# **Malachi Olagbaju**"),
                app_tabs,
            ]
        )
    )








if __name__ == "__main__":
    app.run()