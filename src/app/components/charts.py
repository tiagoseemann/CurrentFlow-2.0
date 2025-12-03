"""
Professional chart components using Plotly.

This module provides reusable, interactive chart components optimized for
energy analytics and time series data visualization.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Optional, List


# Professional color palette
COLORS = {
    'primary': '#1f77b4',      # Blue
    'secondary': '#ff7f0e',    # Orange
    'success': '#2ca02c',      # Green
    'danger': '#d62728',       # Red
    'warning': '#ff9800',      # Yellow
    'info': '#17a2b8',         # Cyan
}

REGION_COLORS = {
    'Norte': '#2ecc71',
    'Nordeste': '#e74c3c',
    'Sudeste/Centro-Oeste': '#3498db',
    'Sul': '#f39c12',
}


def create_dual_axis_chart(
    df: pd.DataFrame,
    x_col: str,
    y1_col: str,
    y2_col: str,
    y1_label: str = "Series 1",
    y2_label: str = "Series 2",
    title: str = "Dual Axis Chart",
    height: int = 500
) -> go.Figure:
    """
    Create a dual-axis line chart (e.g., Load + Temperature).

    Args:
        df: DataFrame with data
        x_col: Column for x-axis (usually date)
        y1_col: Column for left y-axis
        y2_col: Column for right y-axis
        y1_label: Label for left axis
        y2_label: Label for right axis
        title: Chart title
        height: Chart height in pixels

    Returns:
        Plotly Figure object

    Example:
        >>> fig = create_dual_axis_chart(
        ...     df=data,
        ...     x_col='date',
        ...     y1_col='val_cargaenergiamwmed',
        ...     y2_col='temp_mean',
        ...     y1_label='Energy Load (MW)',
        ...     y2_label='Temperature (°C)'
        ... )
    """
    fig = go.Figure()

    # Left axis (y1)
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[y1_col],
        name=y1_label,
        line=dict(color=COLORS['primary'], width=2),
        yaxis='y1'
    ))

    # Right axis (y2)
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[y2_col],
        name=y2_label,
        line=dict(color=COLORS['danger'], width=2),
        yaxis='y2'
    ))

    # Layout with dual axes
    fig.update_layout(
        title=title,
        xaxis=dict(title=x_col.title()),
        yaxis=dict(
            title=dict(text=y1_label, font=dict(color=COLORS['primary'])),
            tickfont=dict(color=COLORS['primary'])
        ),
        yaxis2=dict(
            title=dict(text=y2_label, font=dict(color=COLORS['danger'])),
            tickfont=dict(color=COLORS['danger']),
            overlaying='y',
            side='right'
        ),
        hovermode='x unified',
        height=height,
        template='plotly_white'
    )

    return fig


def create_time_series_with_bands(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    mean_col: Optional[str] = None,
    std_col: Optional[str] = None,
    title: str = "Time Series with Confidence Bands",
    y_label: str = "Value",
    height: int = 500
) -> go.Figure:
    """
    Create time series with confidence bands (±1σ, ±2σ).

    Args:
        df: DataFrame with data
        x_col: Date column
        y_col: Value column
        mean_col: Column with mean (optional, calculated if None)
        std_col: Column with std (optional, calculated if None)
        title: Chart title
        y_label: Y-axis label
        height: Chart height

    Returns:
        Plotly Figure

    Example:
        >>> fig = create_time_series_with_bands(
        ...     df=data,
        ...     x_col='date',
        ...     y_col='val_cargaenergiamwmed',
        ...     title='Energy Load with Confidence Bands'
        ... )
    """
    fig = go.Figure()

    # Calculate mean and std if not provided
    if mean_col is None:
        mean = df[y_col].mean()
    else:
        mean = df[mean_col].mean()

    if std_col is None:
        std = df[y_col].std()
    else:
        std = df[std_col].mean()

    # ±2σ band (lighter)
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=[mean + 2*std] * len(df),
        fill=None,
        mode='lines',
        line=dict(color='rgba(0,0,0,0)'),
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=[mean - 2*std] * len(df),
        fill='tonexty',
        mode='lines',
        line=dict(color='rgba(0,0,0,0)'),
        fillcolor='rgba(68, 68, 68, 0.1)',
        name='±2σ'
    ))

    # ±1σ band (darker)
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=[mean + std] * len(df),
        fill=None,
        mode='lines',
        line=dict(color='rgba(0,0,0,0)'),
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=[mean - std] * len(df),
        fill='tonexty',
        mode='lines',
        line=dict(color='rgba(0,0,0,0)'),
        fillcolor='rgba(68, 68, 68, 0.2)',
        name='±1σ'
    ))

    # Mean line
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=[mean] * len(df),
        mode='lines',
        line=dict(color='gray', dash='dash'),
        name='Mean'
    ))

    # Actual data
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[y_col],
        mode='lines',
        line=dict(color=COLORS['primary'], width=2),
        name=y_label
    ))

    fig.update_layout(
        title=title,
        xaxis_title=x_col.title(),
        yaxis_title=y_label,
        hovermode='x unified',
        height=height,
        template='plotly_white'
    )

    return fig


def create_regional_comparison(
    df: pd.DataFrame,
    region_col: str,
    value_col: str,
    title: str = "Regional Comparison",
    chart_type: str = "bar"
) -> go.Figure:
    """
    Create regional comparison chart (bar or box plot).

    Args:
        df: DataFrame with data
        region_col: Column with region names
        value_col: Column with values to compare
        title: Chart title
        chart_type: 'bar' or 'box'

    Returns:
        Plotly Figure

    Example:
        >>> fig = create_regional_comparison(
        ...     df=data,
        ...     region_col='region',
        ...     value_col='val_cargaenergiamwmed',
        ...     chart_type='box'
        ... )
    """
    if chart_type == "bar":
        # Calculate mean by region
        regional_mean = df.groupby(region_col)[value_col].mean().reset_index()
        regional_mean = regional_mean.sort_values(value_col, ascending=False)

        fig = go.Figure(data=[
            go.Bar(
                x=regional_mean[region_col],
                y=regional_mean[value_col],
                marker_color=[REGION_COLORS.get(r, COLORS['primary'])
                             for r in regional_mean[region_col]],
                text=regional_mean[value_col].round(1),
                textposition='outside'
            )
        ])

    else:  # box plot
        fig = go.Figure()
        for region in df[region_col].unique():
            region_data = df[df[region_col] == region][value_col]
            fig.add_trace(go.Box(
                y=region_data,
                name=region,
                marker_color=REGION_COLORS.get(region, COLORS['primary'])
            ))

    fig.update_layout(
        title=title,
        xaxis_title="Region",
        yaxis_title=value_col.replace('_', ' ').title(),
        template='plotly_white',
        height=500
    )

    return fig


def create_correlation_heatmap(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    title: str = "Correlation Heatmap"
) -> go.Figure:
    """
    Create correlation heatmap for numerical columns.

    Args:
        df: DataFrame
        columns: List of columns to include (None = all numeric)
        title: Chart title

    Returns:
        Plotly Figure

    Example:
        >>> fig = create_correlation_heatmap(
        ...     df=data,
        ...     columns=['val_cargaenergiamwmed', 'temp_mean', 'radiation_mean']
        ... )
    """
    if columns is None:
        corr_df = df.select_dtypes(include='number').corr()
    else:
        corr_df = df[columns].corr()

    fig = go.Figure(data=go.Heatmap(
        z=corr_df.values,
        x=corr_df.columns,
        y=corr_df.columns,
        colorscale='RdBu',
        zmid=0,
        text=corr_df.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))

    fig.update_layout(
        title=title,
        xaxis_title="",
        yaxis_title="",
        height=600,
        template='plotly_white'
    )

    return fig


def create_anomaly_scatter(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    anomaly_col: str = 'is_anomaly',
    title: str = "Anomaly Detection"
) -> go.Figure:
    """
    Create scatter plot highlighting anomalies.

    Args:
        df: DataFrame
        x_col: X-axis column
        y_col: Y-axis column
        anomaly_col: Binary column indicating anomalies
        title: Chart title

    Returns:
        Plotly Figure
    """
    # Normal points
    normal = df[df[anomaly_col] == 0]
    anomalies = df[df[anomaly_col] == 1]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=normal[x_col],
        y=normal[y_col],
        mode='markers',
        name='Normal',
        marker=dict(color=COLORS['primary'], size=6, opacity=0.6)
    ))

    fig.add_trace(go.Scatter(
        x=anomalies[x_col],
        y=anomalies[y_col],
        mode='markers',
        name='Anomaly',
        marker=dict(
            color=COLORS['danger'],
            size=12,
            symbol='x',
            line=dict(width=2)
        )
    ))

    fig.update_layout(
        title=title,
        xaxis_title=x_col.replace('_', ' ').title(),
        yaxis_title=y_col.replace('_', ' ').title(),
        hovermode='closest',
        template='plotly_white',
        height=500
    )

    return fig


def create_time_series_with_moving_avg(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    windows: List[int] = [7, 30],
    title: str = "Time Series with Moving Averages",
    y_label: str = "Value",
    height: int = 500
) -> go.Figure:
    """
    Create time series with multiple moving averages.

    Args:
        df: DataFrame with data
        x_col: Date column
        y_col: Value column
        windows: List of window sizes for moving averages (default: 7 and 30 days)
        title: Chart title
        y_label: Y-axis label
        height: Chart height

    Returns:
        Plotly Figure

    Example:
        >>> fig = create_time_series_with_moving_avg(
        ...     df=data,
        ...     x_col='date',
        ...     y_col='val_cargaenergiamwmed',
        ...     windows=[7, 30],
        ...     title='Energy Load with Moving Averages'
        ... )
    """
    fig = go.Figure()

    # Original data (lighter)
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[y_col],
        mode='lines',
        name='Original',
        line=dict(color=COLORS['primary'], width=1, dash='dot'),
        opacity=0.5
    ))

    # Moving averages
    colors = [COLORS['warning'], COLORS['danger'], COLORS['success']]
    for i, window in enumerate(windows):
        ma = df[y_col].rolling(window=window, center=False).mean()
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=ma,
            mode='lines',
            name=f'{window}-day MA',
            line=dict(color=colors[i % len(colors)], width=2)
        ))

    fig.update_layout(
        title=title,
        xaxis_title=x_col.title(),
        yaxis_title=y_label,
        hovermode='x unified',
        height=height,
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig


def create_seasonal_analysis(
    df: pd.DataFrame,
    date_col: str,
    value_col: str,
    title: str = "Seasonal Analysis",
    height: int = 500
) -> go.Figure:
    """
    Create seasonal analysis chart showing patterns by season.

    Args:
        df: DataFrame with data
        date_col: Date column
        value_col: Value column
        title: Chart title
        height: Chart height

    Returns:
        Plotly Figure

    Example:
        >>> fig = create_seasonal_analysis(
        ...     df=data,
        ...     date_col='date',
        ...     value_col='val_cargaenergiamwmed'
        ... )
    """
    # Add season column
    df_copy = df.copy()
    df_copy[date_col] = pd.to_datetime(df_copy[date_col])
    df_copy['month'] = df_copy[date_col].dt.month

    # Define seasons (Southern Hemisphere)
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Summer'
        elif month in [3, 4, 5]:
            return 'Fall'
        elif month in [6, 7, 8]:
            return 'Winter'
        else:
            return 'Spring'

    df_copy['season'] = df_copy['month'].apply(get_season)

    # Calculate statistics by season
    seasonal_stats = df_copy.groupby('season')[value_col].agg(['mean', 'std']).reset_index()

    # Order seasons
    season_order = ['Summer', 'Fall', 'Winter', 'Spring']
    seasonal_stats['season'] = pd.Categorical(
        seasonal_stats['season'],
        categories=season_order,
        ordered=True
    )
    seasonal_stats = seasonal_stats.sort_values('season')

    # Create box plot by season
    fig = go.Figure()

    season_colors = {
        'Summer': '#f39c12',
        'Fall': '#e67e22',
        'Winter': '#3498db',
        'Spring': '#2ecc71'
    }

    for season in season_order:
        season_data = df_copy[df_copy['season'] == season][value_col]
        fig.add_trace(go.Box(
            y=season_data,
            name=season,
            marker_color=season_colors.get(season, COLORS['primary']),
            boxmean='sd'
        ))

    fig.update_layout(
        title=title,
        xaxis_title="Season",
        yaxis_title=value_col.replace('_', ' ').title(),
        template='plotly_white',
        height=height,
        showlegend=False
    )

    return fig


def create_monthly_heatmap(
    df: pd.DataFrame,
    date_col: str,
    value_col: str,
    title: str = "Monthly Patterns Heatmap"
) -> go.Figure:
    """
    Create heatmap showing monthly patterns (day vs month).

    Args:
        df: DataFrame with data
        date_col: Date column
        value_col: Value column to aggregate
        title: Chart title

    Returns:
        Plotly Figure

    Example:
        >>> fig = create_monthly_heatmap(
        ...     df=data,
        ...     date_col='date',
        ...     value_col='val_cargaenergiamwmed'
        ... )
    """
    df_copy = df.copy()
    df_copy[date_col] = pd.to_datetime(df_copy[date_col])
    df_copy['month'] = df_copy[date_col].dt.month
    df_copy['day'] = df_copy[date_col].dt.day

    # Create pivot table
    heatmap_data = df_copy.pivot_table(
        values=value_col,
        index='day',
        columns='month',
        aggfunc='mean'
    )

    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=[month_names[i-1] for i in heatmap_data.columns],
        y=heatmap_data.index,
        colorscale='RdYlBu_r',
        colorbar=dict(title=value_col.replace('_', ' ').title()),
        hovertemplate='Month: %{x}<br>Day: %{y}<br>Value: %{z:.1f}<extra></extra>'
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Month",
        yaxis_title="Day of Month",
        template='plotly_white',
        height=600
    )

    return fig
