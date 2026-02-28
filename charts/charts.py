import altair as alt
import pandas as pd

def base_theme():
    return {
        "config": {
            "view": {"stroke": None},
            "axis": {"labelFontSize": 12, "titleFontSize": 14},
            "legend": {"labelFontSize": 12, "titleFontSize": 14},
        }
    }

def chart_hook_temp_over_time(df: pd.DataFrame) -> alt.Chart:
    return (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("temp_max:Q", title="Daily max temp (°C)"),
            tooltip=[alt.Tooltip("date:T"), alt.Tooltip("temp_max:Q", format=".1f")],
        )
        .properties(height=320)
    )

def chart_context_seasonality(df: pd.DataFrame) -> alt.Chart:
    month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    return (
        alt.Chart(df)
        .mark_boxplot()
        .encode(
            x=alt.X("month_name:N", title="Month", sort=month_order),
            y=alt.Y("temp_max:Q", title="Daily max temp (°C)"),
        )
        .properties(height=320)
    )

def chart_surprise_extremes(df: pd.DataFrame) -> alt.Chart:
    q = float(df["temp_max"].quantile(0.99))
    df2 = df.copy()
    df2["extreme"] = df2["temp_max"] >= q

    base = (
        alt.Chart(df2)
        .mark_point(filled=True, size=35)
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("temp_max:Q", title="Daily max temp (°C)"),
            color=alt.condition("datum.extreme", alt.value("red"), alt.value("lightgray")),
            tooltip=[alt.Tooltip("date:T"), alt.Tooltip("temp_max:Q", format=".1f")],
        )
        .properties(height=320)
    )

    rule = alt.Chart(pd.DataFrame({"q": [q]})).mark_rule(strokeDash=[6, 4]).encode(y="q:Q")
    return base + rule

def chart_explain_precip_vs_temp(df: pd.DataFrame) -> alt.Chart:
    return (
        alt.Chart(df)
        .mark_point(opacity=0.45)
        .encode(
            x=alt.X("precipitation:Q", title="Precipitation (in)"),
            y=alt.Y("temp_max:Q", title="Daily max temp (°C)"),
            tooltip=[
                "date:T",
                alt.Tooltip("precipitation:Q", format=".2f"),
                alt.Tooltip("temp_max:Q", format=".1f"),
            ],
        )
        .properties(height=320)
    )

def chart_dashboard(df: pd.DataFrame) -> alt.Chart:
    weather_types = sorted(df["weather"].unique())

    w_select = alt.selection_point(
        fields=["weather"],
        bind=alt.binding_select(options=weather_types, name="Weather: "),
    )
    brush = alt.selection_interval(encodings=["x"], name="Time window")

    line = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("temp_max:Q", title="Daily max temp (°C)"),
            color=alt.Color("weather:N", title="Weather"),
            tooltip=["date:T", "weather:N", alt.Tooltip("temp_max:Q", format=".1f")],
        )
        .add_params(w_select, brush)
        .transform_filter(w_select)
        .properties(height=260)
    )

    hist = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("temp_max:Q", bin=alt.Bin(maxbins=30), title="Daily max temp (°C)"),
            y=alt.Y("count():Q", title="Days"),
            tooltip=[alt.Tooltip("count():Q", title="Days")],
        )
        .transform_filter(w_select)
        .transform_filter(brush)
        .properties(height=260)
    )

    return alt.vconcat(line, hist).resolve_scale(color="independent")



def static_viz(df:pd.DataFrame) -> alt.Chart:
    monthly = df.groupby("month_name", as_index = False)['precipitation'].sum()
    month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    static_chart = alt.Chart(monthly, title = alt.TitleParams(text = "Total Precipitation by Month Across All Years", fontSize = 20)
                             ).mark_bar().encode(
    x = alt.X('month_name:N', title = 'Month', sort = month_order, axis = alt.Axis(labelFontSize = 12, titleFontSize = 15)),
    y = alt.Y('precipitation:Q', title = 'Precipitation',  axis = alt.Axis(labelFontSize =12, titleFontSize = 15)),
    tooltip = ['month_name','precipitation']).properties(height = 700, width = 900)

    return static_chart


def interactive_viz(df:pd.DataFrame) -> alt.Chart:
    brush = alt.selection_interval() 

    dot_chart = alt.Chart(df, title = alt.TitleParams(text = "Scatterplot of Precipitation vs. Wind", fontSize = 20)).mark_circle().encode(
    x = alt.X('wind:Q', title = 'Wind', axis = alt.Axis(labelFontSize = 12, titleFontSize = 15)),
    y = alt.Y('precipitation:Q', title = 'Precipitation',  axis = alt.Axis(labelFontSize =12, titleFontSize = 15)),
    color = alt.Color('weather:N', title = 'Weather Type', legend = alt.Legend(labelFontSize = 12, titleFontSize = 15)),
    tooltip = ['wind','precipitation']).add_params(brush).properties(height = 700, width = 900)

    bar_chart = alt.Chart(df, title = alt.TitleParams(text = "Aggregated Number of Days by Weather Type", fontSize = 20)).mark_bar().transform_filter(brush).encode(
    x = alt.X("weather:N", title = 'Weather Type',  axis = alt.Axis(labelFontSize = 12, titleFontSize = 15)),
    y = alt.Y("count()", title = 'Number of Days', axis = alt.Axis(labelFontSize =12, titleFontSize = 15)),
    color = alt.Color('weather:N')).properties(height = 700, width = 900)

    return dot_chart & bar_chart


