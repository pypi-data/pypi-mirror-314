from matplotlib import pyplot as plt
from typing import Literal
from matplotlib.axes import Axes
import seaborn as sns
import seaborn.objects as so
import pandas as pd

def draw_line_and_shade_chart(df_or_series: pd.DataFrame | pd.Series,
                              shading: pd.Series,
                              v_h: Literal["vertical","horizontal"] = "vertical",
                              ax: Axes | None = None,
                              linewidth: int = 1,
                              alpha: float = 0.3,
                              legend_position: str | int = "upper left",
                              move_legend_kwargs: dict = {},
                              ) -> tuple | None:
    """
    Generates a line chart using Seaborn for the dataframe or series provided.
    The dataframe needs to have all columns properly labelled and the series
    needs to be named; the index need to have a name, otherwise a runtime 
    warning will be generated.

    Args:
        df_or_series (pd.DataFrame | pd.Series): the original dataframe.
        shading (pd.Series): a boolean series, generally but not always 
            with the same index as the first argument that highlights where 
            the shading needs to be for the vertical shading
            This however is not a requirement as the index is used to just 
            place the shading in the correct location. 
        v_h (Literal[&quot;vertical&quot;,&quot;horizontal&quot;], optional): 
            whether to produce the shading vertical (classical approach if the 
            index is of dates) or the other way around. Defaults to "vertical".
        ax (Axes | None, optional): the axes over which to draw the chart or  
            None if a new figure and axes are required. Defaults to None.
        linewidth (int, optional): the linewidth for the charts. Defaults to 1.
        alpha (float, optional): the alpha (transparency) for the shadings. 
            Defaults to 0.3.
        legend_position (str | int): the legend position according to Seaborn
            documentation of ``move_legend``. Defaults to upper left. 
        move_legend_kwargs (dict, optional): the keyword arguments position for the 
            legend, according to Seaborn documentation of ``move_legend``. 
            Defaults to empty dictionary.


    Raises:
        RuntimeWarning: possible runtime warnings about colums and index names 
            being missing. Sensible defaults will be generated.            

    Returns:
        tuple | None: returns (fig, ax) if ax is not provided in input, else None.
    """
    
    if isinstance(df_or_series, pd.Series):
        df = df_or_series.to_dataframe()
        df.columns.name = df_or_series.name
    else:
        df = df_or_series

    if df.columns.name is None:
        raise RuntimeWarning("df.columns does not have a name, it will be auto-generated. Remove this warning by explicitly setting df.columns.name to something meaningful")
    if df.index.name is None:
        raise RuntimeWarning("df.index does not have a name, it will be auto-generated. Remove this warning by explicitly setting df.index.name to something meaningful")
    
    # prepare the data
    dfs = df.stack()
    dfs.name = "values"
    dfc = dfs.reset_index()

    
    x = dfs.index.names[0]
    y = dfs.name
    hue = dfs.index.names[1]
    # prepare the chart
    pl = (
        so
        .Plot(data=dfc, x=x, y=y, color=hue)
        .add(so.Line(linewidth=linewidth))
        .label(x=x, y="")
    )

    if ax is None:
        fig = plt.figure(figsize=(10,5));
        ax = fig.subplots();
        provide_return = True
    else:
        fig = ax.get_figure()
        provide_return = False
    
    still_valid = ~shading.shift(-1).isna()
    breaks = (shading != shading.shift(-1))
    shade_start = shading.loc[breaks & (shading == False) & still_valid].index.to_numpy()
    shade_end = shading.loc[breaks & (shading == True) & still_valid].index.to_numpy()
    assert(len(shade_start)==len(shade_end))

    if v_h == "vertical":
        shade_func = ax.axvspan
    else:
        shade_func = ax.axhspan
    
    for i, s in enumerate(shade_start):
        shade_func(s, shade_end[i], alpha=alpha, color='grey', edgecolor=None, zorder=1)

    # display the plot
    pl.on(ax).plot()
    legend = fig.legends.pop()
    ax.legend(legend.legend_handles, [t.get_text() for t in legend.texts])
    sns.move_legend(ax, legend_position, **move_legend_kwargs)

    # return the new figure details if needed
    if provide_return:
        return fig, ax    
