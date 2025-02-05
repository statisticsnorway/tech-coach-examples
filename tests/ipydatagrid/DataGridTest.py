# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#   kernelspec:
#     display_name: tech-coach-stat
#     language: python
#     name: tech-coach-stat
# ---

# %% [markdown]
# # ipydatagrid

# %%
from ipydatagrid import DataGrid, TextRenderer, BarRenderer, Expr, ImageRenderer

# %%
from json import load
import pandas as pd

with open("./cars.json") as fobj:
    data = load(fobj)
df = pd.DataFrame(data["data"]).set_index("index")
df = df[sorted(df.columns)]

# %% [markdown]
# ## Custom cell renderers
#
# Custom cell renderers can be defined for the entire grid or column-wise.
#
# Two types of cell renderers are currently available: `TextRenderer` and `BarRenderer`.
#
# Most of the `TextRenderer`/`BarRenderer` attributes (`background_color`, `text_color` etc.) can either be a __value__, a __bqplot scale__ or a __`VegaExpr`__ or __`Expr`__ instance.
#
#
# ### Vega expressions
# The `VegaExpr` class allows you to define an attribute value as a result of a Vega-expression (see https://vega.github.io/vega/docs/expressions/). _e.g._ `background_color = VegaExpr("value < 150 ? 'red' : 'green'")`.
#   
# You can look at the vega-expression documentation for more information about available constants and functions. In the scope of the expression are also available: `value`: cell value, `x` and `y`: cell position in pixel, `width` and `height` of the cell, `row` and `column`: cell position.
#
# ### Python expressions
# If you prefer writing those expressions in Python, we provide an `Expr` class which takes a Python expression as input string or a Python function, and generates the equivalent vega-expression for you using [py2vega](https://github.com/QuantStack/py2vega).

# %%
from bqplot import LinearScale, ColorScale, OrdinalColorScale, OrdinalScale
from py2vega.functions.color import rgb


def horsepower_coloring(cell):
    if cell.value < 100:
        return "red"
    elif cell.value < 150:
        return "orange"
    else:
        return "green"


def weight_coloring(cell):
    scaled_value = 1 if cell.value > 4500 else cell.value / 4500
    color_value = scaled_value * 255

    return rgb(color_value, 0, 0)


renderers = {
    "Acceleration": BarRenderer(
        horizontal_alignment="center",
        bar_color=ColorScale(min=0, max=20, scheme="viridis"),
        bar_value=LinearScale(min=0, max=20),
    ),
    "Cylinders": TextRenderer(
        background_color=Expr('"grey" if cell.row % 2 else default_value')
    ),
    "Displacement": TextRenderer(
        text_color=ColorScale(min=97, max=455),
        font=Expr(
            "'16px sans-serif' if cell.value > 400 else '12px sans-serif'"
        ),
    ),
    "Horsepower": TextRenderer(
        text_color="black", background_color=Expr(horsepower_coloring)
    ),
    "Miles_per_Gallon": TextRenderer(
        background_color=Expr('"grey" if cell.value is None else default_value')
    ),
    "Name": TextRenderer(
        background_color=Expr(
            'rgb(0, 100, 255) if "chevrolet" in cell.value or "ford" in cell.value else default_value'
        )
    ),
    "Origin": TextRenderer(
        text_color="black",
        background_color=OrdinalColorScale(domain=["USA", "Japan", "Europe"]),
        horizontal_alignment=Expr(
            "'right' if cell.value in ['USA', 'Japan'] else 'left'"
        ),
    ),
    "Weight_in_lbs": TextRenderer(
        text_color="black", background_color=Expr(weight_coloring)
    ),
    "Year": TextRenderer(text_color="black", background_color="green"),
    "Image": ImageRenderer(),
}

datagrid = DataGrid(
    df, base_row_size=124, base_column_size=250, renderers=renderers
)
datagrid

# %%
renderers[
    "Name"
].background_color.value = '"green" if "pontiac" in cell.value or "citroen" in cell.value else default_value'

# %%
renderers["Year"].background_color = "yellow"

# %%
datagrid.transform(
    [
        {
            "type": "filter",
            "operator": "=",
            "column": "Origin",
            "value": "Europe",
        },
        {"type": "sort", "column": "Horsepower", "desc": True},
    ]
)

# %%
datagrid.revert()

# %%
datagrid.transform(
    [
        {"type": "filter", "operator": "=", "column": "Origin", "value": "USA"},
        {"type": "filter", "operator": "<", "column": "Horsepower", "value": 130},
        {"type": "sort", "column": "Acceleration"},
    ]
)

# %% [markdown]
# # Performance test: A million cells with ipydatagrid

# %%
from random import uniform


def create_random_data(n_rows=100, n_columns=100):
    data = {"data": [], "schema": {}}

    data["data"] = [
        [uniform(0, 1) for c in range(n_columns)] for r in range(n_rows)
    ]
    data["schema"]["fields"] = [
        {"name": str(c), type: "number"} for c in range(n_columns)
    ]

    return data


def update_random_data(old_data):
    data = {"data": [], "schema": {}}

    n_columns = len(old_data["data"])
    n_rows = len(old_data["data"][0])

    data["data"] = [
        [uniform(-0.1, 0.1) + old_data["data"][r][c] for c in range(n_columns)]
        for r in range(n_rows)
    ]
    data["schema"]["fields"] = [
        {"name": str(c), type: "number"} for c in range(n_columns)
    ]

    return data


# %%
from py2vega.constants import SQRT1_2

huge_data = create_random_data(1000, 1000)


def renderer_function(cell, default_value):
    return "#fc8403" if cell.value < SQRT1_2 else default_value


conditional_expression = Expr(renderer_function)

default_renderer = TextRenderer(
    background_color=conditional_expression, format=".3f"
)

huge_df = pd.DataFrame(huge_data["data"])

conditional_huge_datagrid = DataGrid(huge_df, default_renderer=default_renderer)
conditional_huge_datagrid

# %%
from ipywidgets import FloatSlider, Dropdown, ColorPicker, HBox, VBox

operator_dropdown = Dropdown(options=["<", ">"], value="<")
reference_slider = FloatSlider(value=0.5, min=0, max=1)
output_colorpicker = ColorPicker(value="#fc8403")


def on_change(*args, **kwargs):
    conditional_expression.value = "'{color}' if cell.value {operator} {reference} else default_value".format(
        operator=operator_dropdown.value,
        reference=reference_slider.value,
        color=output_colorpicker.value,
    )


operator_dropdown.observe(on_change, "value")
reference_slider.observe(on_change, "value")
output_colorpicker.observe(on_change, "value")

hbox = HBox((operator_dropdown, reference_slider, output_colorpicker))
VBox([conditional_huge_datagrid, hbox])

# %% [markdown]
# ## Bar renderer

# %%
from bqplot import LinearScale, ColorScale
from ipydatagrid import DataGrid, BarRenderer

linear_scale = LinearScale(min=0, max=1)
color_scale = ColorScale(min=0, max=1)
bar_renderer = BarRenderer(
    bar_color=color_scale,
    bar_value=linear_scale,
    bar_horizontal_alignment="center",
    show_text=False,
)

huge_df2 = pd.DataFrame(create_random_data()["data"])

huge_datagrid = DataGrid(huge_df2, default_renderer=bar_renderer)

# %%
huge_datagrid

# %%
from ipywidgets import FloatSlider, link

slider = FloatSlider(
    description="Scale: ", value=linear_scale.max, min=0, max=1, step=0.01
)
link((color_scale, "min"), (slider, "value"))
link((linear_scale, "min"), (slider, "value"))

slider

# %%
color_scale.scheme = "magma"
