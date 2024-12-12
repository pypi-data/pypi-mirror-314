import sys
import os
import re
import webbrowser

import pygal
from pygal.style import Style

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))

from collection.collection import MovieCollection
from analysis.data_preprocessing import report_basic_stats
from analysis.data_preprocessing import calculate_top_directors
from analysis.data_preprocessing import stacked_bar_preprocess


# common style
custom_style = Style(title_font_size=20, label_font_size=14, major_label_font_size=14)


def plot_basic_stats(
    user_collection: MovieCollection,
    collection_name: str = None,
    for_dashboard: bool = False,
):
    """
    Generate an HTML visualization for the provided statistics and movie posters.

    Args:
        user_collection (MovieCollection): The user's collection.
        collection_name (str): The name of the collection (optional).
        for_dashboard (bool): Flag indicating whether the visualization is for a dashboard.

    Returns:
         str: The path to the generated HTML file.
    """

    template_file = os.getenv("STATS_TEMPLATE")
    output_file = os.getenv("STATS_OUTPUT_HTML")

    # Load user collection data with movies
    stats = report_basic_stats(user_collection, collection_name)

    # Load the HTML template
    with open(template_file, "r") as file:
        html_template = file.read()

    # Create SVG charts for rate distribution
    bar_chart = pygal.Bar(
        style=custom_style,
        title="Rate Distribution",
        show_legend=True,
        tooltip_border_radius=10,
    )
    for rate, count in stats["rate_distribution"].items():
        bar_chart.add(f"Rate {rate}", count)
    rate_chart_svg = bar_chart.render().decode("utf-8")

    # Create SVG charts for movies watched per year
    year_chart = pygal.Bar(
        style=custom_style,
        title="Movies Watched Per Year",
        show_legend=True,
        tooltip_border_radius=10,
    )
    for year, count in stats["movies_per_year"].items():
        year_chart.add(str(year), count)
    year_chart_svg = year_chart.render().decode("utf-8")

    # Diplay Top Rated Movies
    top_rated_html = """
    <div class="grid-container">
    """
    for _, movie in stats["top_rated_movies"].iterrows():
        top_rated_html += f"""
        <div class="grid-item">
            <img src="{movie['Poster_Link']}" alt="Poster of {movie['movie_title']}" class="poster">
            <p class="movie-title"><strong>{movie['movie_title']}</strong></p>
        </div>
        """
    top_rated_html += "</div>"

    # Diplay Lowest Rated Movies
    lowest_rated_html = """
    <div class="grid-container">
    """
    for _, movie in stats["lowest_rated_movie"].iterrows():
        lowest_rated_html += f"""
        <div class="grid-item">
            <img src="{movie['Poster_Link']}" alt="Poster of {movie['movie_title']}" class="poster">
            <p class="movie-title"><strong>{movie['movie_title']}</strong></p>
        </div>
        """
    lowest_rated_html += "</div>"

    if for_dashboard:
        # Return data for dashboard
        return {
            "user_id": stats["user_id"],
            "rate_chart_svg": rate_chart_svg,
            "year_chart_svg": year_chart_svg,
            "top_rated_html": top_rated_html,
            "lowest_rated_html": lowest_rated_html,
        }

    # Replace placeholders in the template
    html_content = html_template.replace("{{user_id}}", stats["user_id"])
    html_content = html_content.replace("{{rate_chart_svg}}", rate_chart_svg)
    html_content = html_content.replace("{{year_chart_svg}}", year_chart_svg)
    html_content = html_content.replace("{{top_rated_movies}}", top_rated_html)
    html_content = html_content.replace("{{lowest_rated_movie}}", lowest_rated_html)

    # Save the final HTML to file
    with open(output_file, "w") as file:
        file.write(html_content)

    webbrowser.open(f"file://{os.path.abspath(output_file)}")
    return f"Report saved to '{output_file}'."


def plot_top_directors(
    user_collection: MovieCollection,
    collection_name: str = None,
    for_dashboard: bool = False,
):
    """
    Visualize the top 5 directors with their movies and average ratings using a bar chart.

    Args:
        user_collection (MovieCollection): The user's collection.
        collection_name (str): The name of the collection (optional).
        for_dashboard (bool): Flag indicating whether the visualization is for a dashboard.

    Returns:
         str: The path to the generated SVG file.
    """

    top_directors = calculate_top_directors(user_collection, collection_name)

    output_file = os.getenv("TOP_DIRECTORS_OUTPUT_FILE")

    # Create a bar chart for Top Directors
    director_chart = pygal.Bar(
        title="Top 5 Directors with Average Ratings",
        width=600,
        height=600,
        margin_bottom=200,
        style=custom_style,
        x_label_rotation=30,
        show_legend=True,
        legend_at_bottom=True,
    )

    # Add data to the chart
    for _, row in top_directors.iterrows():
        director_chart.add(
            row["Director"],  # Legend will display the director's name
            [
                {
                    "value": row["movie_count"],
                    "label": f"Avg Rating: {row['avg_rating']:.2f}",
                }
            ],
        )
    # Render the chart as SVG (raw data)
    svg_data = director_chart.render()

    # Add custom text below the chart
    additional_text = """
    <text x="0" y="420" font-size="12" fill="black">Director Details:</text>
    """
    line_height = 20  # Line height for spacing between rows
    y_start = 440  # Starting y-coordinate for the first text line
    for i, row in top_directors.iterrows():
        additional_text += f'<text x="20" y="{y_start + i * line_height}" font-size="10" fill="black">{row["Director"]}: {row["movies"]}</text>'

    # Find the position to insert the custom text
    svg_data = svg_data.decode("utf-8")  # Decode bytes to string
    insert_position = svg_data.find("</svg>")  # Find the end of the SVG
    svg_data = svg_data[:insert_position] + additional_text + svg_data[insert_position:]

    if for_dashboard:
        # Return data for dashboard
        return svg_data

    # Save the SVG chart
    with open(output_file, "w") as f:
        f.write(svg_data)

    webbrowser.open(f"file://{os.path.abspath(output_file)}")
    return f"Top Directors saved to '{output_file}'."


def plot_stacked_bar(
    user_collection: MovieCollection,
    collection_name: str,
    period,
    year=None,
    for_dashboard: bool = False,
):
    """
    Visualize genre trends over time using a stacked bar chart.

    Args:
        user_collection (MovieCollection): The user's collection.
        collection_name (str): The name of the collection (optional).
        period (str): The period criterion ('month' or 'year').
        year (int): The specific year to filter the data (optional).
        for_dashboard (bool): Flag indicating whether the visualization is for a dashboard.

    Returns:
         str: The path to the generated SVG file.
    """

    pivot_table = stacked_bar_preprocess(user_collection, collection_name, period, year)
    output_file = os.getenv("TREND_OUTPUT_FILE")

    chart = pygal.StackedBar(
        style=custom_style, x_label_rotation=45, truncate_label=15, show_legend=True
    )
    chart.title = f"Percentage Genre of Movie Watched per {period}"
    if year:
        chart.title += f" in {year}"

    chart.x_labels = pivot_table.index.astype(str)  # use period labels as strings

    # add each genre to the chart
    for genre in pivot_table.columns:
        chart.add(genre, pivot_table[genre].tolist())

    if for_dashboard:
        # Return data for dashboard
        return chart.render().decode("utf-8")

    # render the chart to file or display in the notebook
    chart.render_to_file(output_file)

    webbrowser.open(f"file://{os.path.abspath(output_file)}")
    return f"Trend chart saved to '{output_file}'."


def display_dashboard(
    user_collection: MovieCollection, collection_name: str, period: str, year=None
):
    """
    Combine all visualizations into a single HTML dashboard and display it in the browser.

    Args:
        user_collection (MovieCollection): The user's collection.
        collection_name (str): The name of the collection (optional).
        period (str): The period criterion ('month' or 'year').
        year (int): The specific year to filter the data (optional).

    Returns:
         str: The path to the generated HTML file.
    """
    template_file = os.getenv("DASHBOARD_TEMPLATE")
    output_file = os.getenv("DASHBOARD_OUTPUT_HTML")

    # Generate visualizations for dashboard
    basic_stats = plot_basic_stats(user_collection, collection_name, for_dashboard=True)
    top_directors_svg = plot_top_directors(
        user_collection, collection_name, for_dashboard=True
    )
    stacked_bar_svg = plot_stacked_bar(
        user_collection, collection_name, period, year, for_dashboard=True
    )

    # Load the HTML template
    with open(template_file, "r") as file:
        html_template = file.read()

    # Replace placeholders in the template
    html_content = html_template.replace("{{user_id}}", basic_stats["user_id"])
    html_content = html_content.replace(
        "{{rate_chart_svg}}", basic_stats["rate_chart_svg"]
    )
    html_content = html_content.replace(
        "{{year_chart_svg}}", basic_stats["year_chart_svg"]
    )
    html_content = html_content.replace(
        "{{top_rated_movies}}", basic_stats["top_rated_html"]
    )
    html_content = html_content.replace(
        "{{lowest_rated_movie}}", basic_stats["lowest_rated_html"]
    )
    html_content = html_content.replace("{{director_chart_svg}}", top_directors_svg)
    html_content = html_content.replace("{{trend_chart_svg}}", stacked_bar_svg)

    # Save the combined HTML
    with open(output_file, "w") as file:
        file.write(html_content)

    webbrowser.open(f"file://{os.path.abspath(output_file)}")
    return f"Dashboard saved to '{output_file}'."
