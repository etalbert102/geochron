""" Visualization of time hexes """
import pandas as pd
import plotly.express as px

def top_locations(timehex:pd.DataFrame):
    timehex_dropped = timehex.drop(columns=['interval', 'start_time', 'end_time'])
    timehex_sum = timehex_dropped.sum()
    s_top10 = timehex_sum.sort_values(ascending=False).head(10)
    df_top10 = s_top10.to_frame().reset_index()
    df_top10.columns = ['Geohash', 'Number of Time Periods Observed']  # rename column
    fig = px.bar(df_top10, x='Geohash', y='Number of Time Periods Observed', title='Top 10 Locations')


    return fig
