"""
Reusable metric components for the dashboard.

This module provides professional KPI cards and metric displays
following best practices for data visualization.
"""

import streamlit as st
from typing import Optional, Union


def display_kpi_card(
    label: str,
    value: Union[int, float],
    delta: Optional[Union[int, float]] = None,
    delta_label: Optional[str] = None,
    format_str: str = "{:,.2f}",
    help_text: Optional[str] = None
) -> None:
    """
    Display a KPI card with optional delta indicator.

    Args:
        label: KPI name/label
        value: Current value
        delta: Change from previous period (optional)
        delta_label: Label for delta (e.g., "vs last month")
        format_str: Python format string for value display
        help_text: Tooltip text explaining the metric

    Example:
        >>> display_kpi_card(
        ...     label="Average Load",
        ...     value=25000.5,
        ...     delta=1250.3,
        ...     delta_label="vs last month",
        ...     format_str="{:,.1f} MW"
        ... )
    """
    formatted_value = format_str.format(value)

    if delta is not None:
        delta_pct = (delta / value) * 100 if value != 0 else 0
        delta_text = f"{delta:+.1f} ({delta_pct:+.1f}%)"
        if delta_label:
            delta_text += f" {delta_label}"
    else:
        delta_text = None

    st.metric(
        label=label,
        value=formatted_value,
        delta=delta_text,
        help=help_text
    )


def display_kpi_row(metrics: list[dict]) -> None:
    """
    Display a row of KPI cards.

    Args:
        metrics: List of metric dictionaries with keys:
                 'label', 'value', 'delta' (optional), 'format' (optional)

    Example:
        >>> metrics = [
        ...     {'label': 'Total Load', 'value': 50000, 'format': '{:,.0f} MW'},
        ...     {'label': 'Avg Temp', 'value': 24.5, 'format': '{:.1f}°C'},
        ... ]
        >>> display_kpi_row(metrics)
    """
    cols = st.columns(len(metrics))

    for col, metric in zip(cols, metrics):
        with col:
            display_kpi_card(
                label=metric['label'],
                value=metric['value'],
                delta=metric.get('delta'),
                format_str=metric.get('format', '{:,.2f}'),
                help_text=metric.get('help')
            )


def display_stat_summary(
    title: str,
    mean: float,
    median: float,
    std: float,
    min_val: float,
    max_val: float,
    unit: str = ""
) -> None:
    """
    Display statistical summary in an expandable section.

    Args:
        title: Title of the summary
        mean: Mean value
        median: Median value
        std: Standard deviation
        min_val: Minimum value
        max_val: Maximum value
        unit: Unit of measurement (e.g., "MW", "°C")

    Example:
        >>> display_stat_summary(
        ...     title="Energy Load Statistics",
        ...     mean=25000, median=24500, std=3000,
        ...     min_val=15000, max_val=35000,
        ...     unit="MW"
        ... )
    """
    with st.expander(f"📊 {title}"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Mean", f"{mean:,.1f} {unit}")
            st.metric("Std Dev", f"{std:,.1f} {unit}")

        with col2:
            st.metric("Median", f"{median:,.1f} {unit}")
            st.metric("Range", f"{max_val - min_val:,.1f} {unit}")

        with col3:
            st.metric("Min", f"{min_val:,.1f} {unit}")
            st.metric("Max", f"{max_val:,.1f} {unit}")
