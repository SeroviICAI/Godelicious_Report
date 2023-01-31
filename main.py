from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.express as px
import random

# Fixing dtypes of some troublesome columns...
dtypes = {'holiday_type': object, 'locale': object,
          'locale_name': object, 'description': object,
          'transferred': object}

# Reading csv files and concatenating dataframes...
dataframe_1 = pd.read_csv("godelicious_1.csv", dtype=dtypes)
dataframe_2 = pd.read_csv("godelicious_2.csv", dtype=dtypes)
dataframe = pd.concat([dataframe_1, dataframe_2], axis=0)

# External CSS stylesheets
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
    dbc.themes.BOOTSTRAP,
]

# Figure of average sales per week day
dataframe_week_days = dataframe.groupby(by="day_of_week", as_index=False)["sales"].mean()
dataframe_week_days.rename(columns={"sales": "avg_sales"}, inplace=True)
fig = px.pie(dataframe_week_days,
             names="day_of_week",
             values="avg_sales",
             width=354,
             height=350,
             template="ggplot2")

piechart_days = html.Div(
    children=[
        html.H4(
            children='Average sales per day of the week',
            className='figure-text',
        ),
        dcc.Graph(
            id='piechart-days',
            figure=fig
        )
    ],
    className="figure"
)

# Figure of average sales per week
dataframe_weeks_year = dataframe.groupby(by=["week", "year"], as_index=False)["sales"].sum()
dataframe_weeks = dataframe_weeks_year.groupby(by="week", as_index=False)["sales"].mean()
dataframe_weeks.rename(columns={"sales": "avg_sales"}, inplace=True)
dataframe_weeks["max_sales"] = dataframe_weeks_year.groupby(by="week")["sales"].max()
dataframe_weeks.sort_values(by="week", ascending=True, inplace=True)
fig = px.line(dataframe_weeks,
              x="week",
              y=["avg_sales", "max_sales"],
              width=1024,
              height=350,
              template="ggplot2")

fig.add_shape(
    type="line",
    line_color="salmon",
    line_width=3,
    opacity=1,
    line_dash="dot",
    xref="paper",
    x0=0,
    x1=1,
    y0=dataframe_weeks['avg_sales'].mean(),
    y1=dataframe_weeks['avg_sales'].mean(),
    yref="y"
)

linechart_weeks = html.Div(
    children=[
        html.H4(
            children='Average sales per week',
            className='figure-text',
        ),
        dcc.Graph(
            id='linechart-weeks',
            figure=fig
        )
    ],
    className="figure"
)

# Figure of average sales per month
dataframe_months_year = dataframe.groupby(by=["month", "year"], as_index=False)["sales"].sum()
dataframe_months = dataframe_months_year.groupby(by="month", as_index=False)["sales"].mean()
dataframe_months.rename(columns={"sales": "avg_sales"}, inplace=True)
dataframe_months["max_sales"] = dataframe_months_year.groupby(by="month")["sales"].max()
dataframe_months.sort_values(by="month", ascending=True, ignore_index=True, inplace=True)
fig = px.line(dataframe_months,
              x="month",
              y=["avg_sales", "max_sales"],
              width=670,
              height=350,
              template="ggplot2")

fig.add_shape(
    type="line",
    line_color="salmon",
    line_width=3,
    opacity=1,
    line_dash="dot",
    xref="paper",
    x0=0,
    x1=1,
    y0=dataframe_months['avg_sales'].mean(),
    y1=dataframe_months['avg_sales'].mean(),
    yref="y"
)

linechart_months = html.Div(
    children=[
        html.H4(
            children='Average sales per month',
            className='figure-text',
        ),
        dcc.Graph(
            id='linechart-months',
            figure=fig
        )
    ],
    className="figure"
)

# Top ten most sold product families
dataframe_products = dataframe.groupby(by=["family"], as_index=False)["sales"].sum()
dataframe_products.sort_values(by="sales", ascending=True, ignore_index=True, inplace=True)

fig = px.bar(dataframe_products[-10:],
             x="sales",
             y="family",
             color="sales",
             color_continuous_scale='Viridis',
             template='ggplot2',
             orientation='h',
             height=600,
             width=1024)

barchart_products = html.Div(
    children=[
        html.H4(
            children='Top 10 most sold Product Categories',
            className='figure-text',
        ),
        dcc.Graph(
            id='barchart-products',
            figure=fig
        ),
    ],
    className="figure"
)

dataframe_products.sort_values(by="sales", ascending=False, ignore_index=True, inplace=True)

# Product Categories with the most profit obtained with promotions
dataframe_prom_bool = dataframe.copy()
dataframe_prom_bool["onpromotion"] = dataframe_prom_bool["onpromotion"].apply(bool)
dataframe_prom_prod = dataframe_prom_bool[dataframe_prom_bool["onpromotion"] == True].groupby(by=["family"],
                                                                                              as_index=False
                                                                                              )["sales"].sum()
dataframe_prom_prod.sort_values(by="sales", ascending=True, ignore_index=True, inplace=True)

fig = px.bar(dataframe_prom_prod[-10:],
             x="sales",
             y="family",
             color="sales",
             color_continuous_scale='Magma',
             template='ggplot2',
             orientation='h',
             height=600,
             width=1024)

barchart_prom = html.Div(
    children=[
        html.H4(
            children='Top 10 Product Categories with the most profit obtained with promotions',
            className='figure-text',
        ),
        dcc.Graph(
            id='barchart-prom',
            figure=fig
        )
    ],
    className="figure"
)

# Figure of sales per store type
dataframe_store_types = dataframe.groupby(by="store_type", as_index=False)["sales"].sum()
fig = px.pie(dataframe_store_types,
             names="store_type",
             values="sales",
             width=1024,
             height=600,
             template="ggplot2")

piechart_stores = html.Div(
    children=[
        html.H4(
            children='Where does the most profit come from? (Store types)',
            className='figure-text',
        ),
        dcc.Graph(
            id='piechart-stores',
            figure=fig
        )
    ],
    className="figure"
)

# APP
app = Dash(__name__,
           suppress_callback_exceptions=True,
           external_stylesheets=external_stylesheets)
app.title = "Godelicious: Delicacies in one GO!"

# Tabs content
tab_1 = html.Div(
    children=[
        html.Div(
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(
                            dbc.Card(
                                children=[
                                    dbc.CardHeader("Number of store-clients collected"),
                                    dbc.CardBody(
                                        [
                                            html.H5("Store-clients", className="card-title"),
                                            html.P(
                                                str(dataframe['store_nbr'].nunique()) + " stores",

                                            ),
                                        ],
                                    ),
                                ],
                                color="primary",
                                outline=True
                            ),
                        ),
                        dbc.Col(
                            dbc.Card(
                                children=[
                                    dbc.CardHeader("Number of product categories sold"),
                                    dbc.CardBody(
                                        [
                                            html.H5("Product categories", className="card-title"),
                                            html.P(
                                                str(dataframe['family'].nunique()) + " categories",

                                            ),
                                        ],
                                    ),
                                ],
                                color="secondary",
                                outline=True
                            ),
                        ),
                        dbc.Col(
                            dbc.Card(
                                children=[
                                    dbc.CardHeader("Number of years of collected data"),
                                    dbc.CardBody(
                                        [
                                            html.H5("Years", className="card-title"),
                                            html.P(
                                                str(dataframe['year'].nunique()) + " years",

                                            ),
                                        ],
                                    ),
                                ],
                                color="warning",
                                outline=True
                            ),
                        ),
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    children=[
                        dbc.Col(
                            dbc.Card(
                                children=[
                                    dbc.CardHeader("Number of states where the company is active"),
                                    dbc.CardBody(
                                        [
                                            html.H5("States", className="card-title"),
                                            html.P(
                                                str(dataframe['state'].nunique()) + " states",

                                            ),
                                        ],
                                    ),
                                ],
                                color="warning",
                                outline=True
                            ),
                        ),
                        dbc.Col(
                            dbc.Card(
                                children=[
                                    dbc.CardHeader("Number of cities where the company is active"),
                                    dbc.CardBody(
                                        [
                                            html.H5("Cities", className="card-title"),
                                            html.P(
                                                str(dataframe['city'].nunique()) + " cities",

                                            ),
                                        ],
                                    ),
                                ],
                                color="success",
                                outline=True
                            ),
                        ),
                        dbc.Col(
                            dbc.Card(
                                children=[
                                    dbc.CardHeader("Number of months of collected data"),
                                    dbc.CardBody(
                                        [
                                            html.H5("Months", className="card-title"),
                                            html.P(
                                                str(len(dataframe.groupby(by=["month", "year"]))) + " months",

                                            ),
                                        ],
                                    ),
                                ],
                                color="danger",
                                outline=True
                            ),
                        ),
                    ],
                    className="mb-4",
                ),
            ],
            className="card-box"
        ),
        html.Div(
            children=[
                piechart_days,
                linechart_months,
                linechart_weeks,
                barchart_products,
                barchart_prom,
                piechart_stores,
            ],
            className="figure-box"
        ),
    ]
)

tab_2 = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Store:", className="menu-title"),
                        dcc.Dropdown(
                            id="store-filter",
                            options=[
                                {"label": store_nbr, "value": store_nbr}
                                for store_nbr in np.sort(dataframe["store_nbr"].unique())
                            ],
                            value=1,
                            clearable=False,
                            className="dropdown",
                        ),
                    ],
                    className="menu"
                ),
            ]
        ),
        html.Div(
            children=[
                html.Div(
                    id="store-cards",
                    className="card-box",
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.H4(
                                    children='Top 10 most sold Product Categories',
                                    className="figure-text",
                                ),
                                dcc.Graph(
                                    id="barchart-store-sales",
                                ),
                            ],
                            className="figure"
                        ),
                        html.Div(
                            children=[
                                html.H4(
                                    children='What are the most sold product categories?',
                                    className="figure-text",
                                ),
                                dcc.Graph(
                                    id="piechart-store-products",
                                ),
                            ],
                            className="figure"
                        ),
                    ],
                    className="figure-box"
                ),
            ],
        ),
    ],
)

tab_3 = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="State:", className="menu-title"),
                        dcc.Dropdown(
                            id="state-filter",
                            options=[
                                {"label": state, "value": state}
                                for state in np.sort(dataframe["state"].unique())
                            ],
                            value=dataframe.iloc[0]["state"],
                            clearable=False,
                            className="dropdown",
                        ),
                    ],
                    className="menu"
                ),
            ]
        ),
        html.Div(
            children=[
                html.Div(
                    id="state-cards",
                    className="card-box"
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.H4(
                                    children="Most profitable shops in region",
                                    className="figure-text",
                                ),
                                dcc.Graph(
                                    id="barchart-state-sales",
                                ),
                            ],
                            className="figure"
                        ),
                    ],
                    className="figure-box"
                ),
            ],
        ),
    ],
)

tab_4 = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="State:", className="menu-title"),
                        dcc.Dropdown(
                            id="product-filter",
                            options=[
                                {"label": stype, "value": stype}
                                for stype in np.sort(dataframe["family"].unique())
                            ],
                            value=dataframe.iloc[0]["family"],
                            clearable=False,
                            className="dropdown",
                        ),
                    ],
                    className="menu"
                ),
            ],
        ),
        html.Div(
            children=[
                html.Div(
                    id="product-cards",
                    className="card-box"
                ),
                html.Div(
                    children=[
html.Div(
                            children=[
                                html.H4(
                                    children="Top 10 cities where the product was most successful",
                                    className="figure-text",
                                ),
                                dcc.Graph(
                                    id="barchart-product-city",
                                ),
                            ],
                            className="figure"
                        ),
                    ],
                    className="figure-box"
                ),
            ],
        ),
    ],
)

app.layout = html.Div([
    dcc.Tabs(
        id="tabs-styled-with-inline",
        children=[
            dcc.Tab(label='Sheet 1', value='sheet-1', className="tab", selected_className="custom-tab"),
            dcc.Tab(label='Sheet 2', value='sheet-2', className="tab", selected_className="custom-tab"),
            dcc.Tab(label='Sheet 3', value='sheet-3', className="tab", selected_className="custom-tab"),
            dcc.Tab(label='Sheet 4', value='sheet-4', className="tab", selected_className="custom-tab"),
        ],
        value='sheet-1',
        parent_className='custom-tabs',
    ),
    html.Div(
        children=[
            html.Div(
                children=[
                    html.P(children="📊", className="header-emoji"),
                    html.H1(
                        children="Godelicious Dashboard", className="header-title"
                    ),
                    html.P(
                        children="Analyze and visualize the main Godelicious KPIs in a"
                                 " dashboard made with Dash.",
                        className="header-description",
                    ),
                ],
                className="header",
            ),
        ],
    ),
    html.Div(id='tabs-content-inline')
],
)


# Sheet 2 I/O
@app.callback(
    [Output("store-cards", "children"),
     Output("barchart-store-sales", "figure"),
     Output("piechart-store-products", "figure")],
    Input("store-filter", "value")
)
def update_charts_sheet_2(store):
    mask = dataframe_prom_bool[dataframe_prom_bool["store_nbr"] == store]
    mask_sales_year = mask.groupby(by=["year", "onpromotion"], as_index=False)["sales"].sum()

    cards = dbc.Row(
        children=[
            dbc.Col(
                dbc.Card(
                    children=[
                        dbc.CardHeader("Total number of sold product categories"),
                        dbc.CardBody(
                            [
                                html.H5("Product categories", className="card-title"),
                                html.P(
                                    str(mask[mask["sales"] != 0]["family"].nunique()) + " products",

                                ),
                            ]
                        )
                    ],
                    color=random.choice(["warning", "secondary", "primary", "success", "danger"]),
                    outline=True
                )
            ),
            dbc.Col(
                dbc.Card(
                    children=[
                        dbc.CardHeader("Total number of sales made"),
                        dbc.CardBody(
                            [
                                html.H5("Sales", className="card-title"),
                                html.P(
                                    str(mask['sales'].sum()) + " sales",

                                ),
                            ]
                        )
                    ],
                    color=random.choice(["warning", "secondary", "primary", "success", "danger"]),
                    outline=True
                )
            ),
            dbc.Col(
                dbc.Card(
                    children=[
                        dbc.CardHeader("Store type of the selected store"),
                        dbc.CardBody(
                            [
                                html.H5("Type", className="card-title"),
                                html.P(
                                    mask.iloc[0]["store_type"] + " type",

                                ),
                            ]
                        )
                    ],
                    color=random.choice(["warning", "secondary", "primary", "success", "danger"]),
                    outline=True
                )
            ),
        ]
    )

    figure_1 = px.bar(mask_sales_year,
                      x="year",
                      y="sales",
                      color="onpromotion",
                      template='ggplot2',
                      orientation='v',
                      height=600,
                      width=1024)

    figure_2 = px.pie(mask[mask["sales"] != 0],
                      names="family",
                      values="sales",
                      template='ggplot2',
                      height=600,
                      width=1024)
    figure_2.update_traces(textposition='inside')
    figure_2.update_layout(uniformtext_minsize=15, uniformtext_mode='hide')
    return cards, figure_1, figure_2


# Sheet 3 I/O
@app.callback(
    [Output("state-cards", "children"),
     Output("barchart-state-sales", "figure")],
    Input("state-filter", "value")
)
def update_charts_sheet_3(state):
    mask = dataframe[dataframe["state"] == state]

    mask_categories = mask.groupby(by="family", as_index=False)["sales"].sum()
    mask_categories.sort_values(by="sales", ascending=False, inplace=True)

    mask_stores = mask.groupby(by="store_nbr", as_index=False)["sales"].sum()
    mask_stores["store_nbr"] = mask_stores["store_nbr"].apply(str)
    mask_stores.sort_values(by="sales", ascending=True, inplace=True)

    cards = dbc.Row(
        children=[
            dbc.Col(
                dbc.Card(
                    children=[
                        dbc.CardHeader("Most profitable product category in the region"),
                        dbc.CardBody(
                            [
                                html.H5("Best product category", className="card-title"),
                                html.P(
                                    str(mask_categories.iloc[0]["family"]),

                                ),
                            ]
                        )
                    ],
                    color=random.choice(["warning", "secondary", "primary", "success", "danger"]),
                    outline=True
                )
            ),
            dbc.Col(
                dbc.Card(
                    children=[
                        dbc.CardHeader("Total number of sales made"),
                        dbc.CardBody(
                            [
                                html.H5("Sales", className="card-title"),
                                html.P(
                                    str(mask['sales'].sum()) + " sales",

                                ),
                            ]
                        )
                    ],
                    color=random.choice(["warning", "secondary", "primary", "success", "danger"]),
                    outline=True
                )
            ),
            dbc.Col(
                dbc.Card(
                    children=[
                        dbc.CardHeader("Most common type of store in the selected region"),
                        dbc.CardBody(
                            [
                                html.H5("Store type (most common)", className="card-title"),
                                html.P(
                                    mask["store_type"].mode() + " type",

                                ),
                            ]
                        )
                    ],
                    color=random.choice(["warning", "secondary", "primary", "success", "danger"]),
                    outline=True
                )
            ),
        ]
    )

    figure_1 = px.bar(mask_stores[-5:],
                      x="sales",
                      y="store_nbr",
                      template='ggplot2',
                      orientation='h',
                      height=600,
                      width=1024)
    return cards, figure_1


# Sheet 4 I/O
@app.callback(
    [Output("product-cards", "children"),
     Output("barchart-product-city", "figure")],
    Input("product-filter", "value")
)
def update_charts_sheet_4(family):
    place_int = int(dataframe_products[dataframe_products["family"] == family].index[0]) + 1
    # Convert to ordinal
    place = "%d%s" % (place_int, "tsnrhtdd"[(place_int//10 % 10 != 1)*(place_int % 10 < 4)*place_int % 10::4])

    mask = dataframe[dataframe["family"] == family]

    mask_cities = mask.groupby(by="city", as_index=False)["sales"].sum()
    mask_cities.sort_values(by="sales", ascending=True, inplace=True)

    mask_states = mask.groupby(by="state", as_index=False)["sales"].sum()
    mask_states.sort_values(by="sales", ascending=True, inplace=True)

    cards = dbc.Row(
        children=[
            dbc.Col(
                dbc.Card(
                    children=[
                        dbc.CardHeader("State in which the product was the most sold"),
                        dbc.CardBody(
                            [
                                html.H5("State (most successful)", className="card-title"),
                                html.P(
                                    str(mask_states.iloc[-1]["state"]),
                                ),
                            ]
                        )
                    ],
                    color=random.choice(["warning", "secondary", "primary", "success", "danger"]),
                    outline=True
                )
            ),
            dbc.Col(
                dbc.Card(
                    children=[
                        dbc.CardHeader("Total number of sales made"),
                        dbc.CardBody(
                            [
                                html.H5("Sales", className="card-title"),
                                html.P(
                                    str(mask['sales'].sum()) + " sales",

                                ),
                            ]
                        )
                    ],
                    color=random.choice(["warning", "secondary", "primary", "success", "danger"]),
                    outline=True
                )
            ),
            dbc.Col(
                dbc.Card(
                    children=[
                        dbc.CardHeader("Place on the ranking of most profitable product"),
                        dbc.CardBody(
                            [
                                html.H5("Ranking categories", className="card-title"),
                                html.P(
                                    place + ' place'
                                ),
                            ]
                        )
                    ],
                    color=random.choice(["warning", "secondary", "primary", "success", "danger"]),
                    outline=True
                )
            ),
        ]
    )

    figure_1 = px.bar(mask_cities[-10:],
                      x="sales",
                      y="city",
                      template='ggplot2',
                      orientation='h',
                      height=600,
                      width=1024)
    figure_1.update_traces(marker_color='#73af48')
    return cards, figure_1


# Tabs I/O
@app.callback(
    Output('tabs-content-inline', 'children'),
    Input('tabs-styled-with-inline', 'value')
)
def render_content(tab):
    if tab == 'sheet-1':
        return tab_1
    elif tab == 'sheet-2':
        return tab_2
    elif tab == 'sheet-3':
        return tab_3
    elif tab == 'sheet-4':
        return tab_4


if __name__ == "__main__":
    app.run_server(debug=True)
