from matplotlib import pyplot as plt
from matplotlib.axes import Axes
import seaborn as sns
import seaborn.objects as so
import pandas as pd
from typing import Literal


def draw_components_and_line_chart(df: pd.DataFrame, 
                                   total_line_label: str | None = None, 
                                   component_design: Literal["bar","area"] = "bar",
                                   ax: Axes | None = None,
                                   legend_position: str | int = "upper left",
                                   move_legend_kwargs: dict = {},
                                   alpha: float = 0.3,
                                   total_line_linewidth: int = 3,
                                   ) -> tuple | None:
    """
    Generates a component chart using Seaborn for the dataframe provided.
    The dataframe needs to have all columns properly labelled, and both
    the main index and the column index need to have names, otherwise a runtime 
    warning will be generated.

    Args:
        df (pd.Dataframe): the original dataframe.
        total_line_label (str | None, optional): the label to give to the total line
            or None if a total line is not desired. Defaults to None.
        component_design (Literal[&quot;bar&quot;,&quot;area&quot;], optional): 
            the component to represent the data. "bar" generates
            a stacked bar chart and "area" generates a stacked area chart. 
            Defaults to "bar".
        ax (Axes | None, optional): the axes over which to draw the chart or  
            None if a new figure and axes are required. Defaults to None.
        legend_position (str | int): the legend position according to Seaborn
            documentation of ``move_legend``. Defaults to upper left. 
        move_legend_kwargs (dict, optional): the keyword arguments position for the 
            legend, according to Seaborn documentation of ``move_legend``. 
            Defaults to empty dictionary.
        total_line_linewidth (int, optional): the linewidth for the total line. 
            Defaults to 3 and ignored if there is no total_line_label.
        alpha (float, optional): the alpha (transparency) for the area chart. 
            Defaults to 0.3.


    Raises:
        RuntimeWarning: possible runtime warnings about colums and index names 
            being missing. Sensible defaults will be generated.            
            
    Returns:
        tuple | None: returns (fig, ax) if ax is not provided in input, else None.

    """
    if df.columns.name is None:
        raise RuntimeWarning("df.columns does not have a name, it will be auto-generated. Remove this warning by explicitly setting df.columns.name to something meaningful")
    if isinstance(df.index, pd.MultiIndex):
        if df.index.names is None:
            raise RuntimeWarning("df.index does not have level names, they will be auto-generated. Remove this warning by explicitly setting df.index.names to something meaningful")
    else:
        if df.index.name is None:
            raise RuntimeWarning("df.index does not have a name, it will be auto-generated. Remove this warning by explicitly setting df.index.name to something meaningful")

    # prepare the data
    dfs = df.stack()
    dfs.name = "values"
    dfc = dfs.reset_index()
    dfc_pos = dfc.loc[dfc["values"] >= 0.]
    dfc_neg = dfc.loc[dfc["values"] < 0.]
    x = dfs.index.names[0]
    y = dfs.name
    hue = dfs.index.names[1]

    # choose the component design
    if component_design == "bar":
        component = so.Bar(edgewidth=0, alpha=alpha)
    elif component_design == "area":
        component = so.Area(edgewidth=0, alpha=alpha)

    # prepare the chart adding positive and negative values 
    # separately and if required the total line
    pl = (
        so
        .Plot(data=dfc_pos, x=x, y=y, color=hue)
        .add(component, so.Stack())
        .add(component, so.Stack(), data=dfc_neg, x=x, y=y, color=hue)
        .label(x=x, y="")
    )

    if total_line_label is not None:
        total_data = df.sum(axis=1)
        total_data.name = total_line_label
        total_data_df = total_data.to_frame()
        total_data_df.columns.name = hue
        total_data_dfs = total_data_df.stack()
        total_data_dfs.name = y
        total_data_dfc = total_data_dfs.reset_index()
        pl = pl.add(so.Line(linewidth=total_line_linewidth), data=total_data_dfc)

    # create a new figure if needed
    if ax is None:
        fig = plt.figure(figsize=(10,5));
        ax = fig.subplots();
        if total_line_label is not None:
            fig.suptitle(total_line_label + " - decomposition");
        provide_return = True
    else:
        provide_return = False

    # display the plot
    pl.on(ax).plot()
    legend = fig.legends.pop()
    ax.legend(legend.legend_handles, [t.get_text() for t in legend.texts])
    sns.move_legend(ax, legend_position, **move_legend_kwargs)

    # return the new figure details if needed
    if provide_return:
        return fig, ax