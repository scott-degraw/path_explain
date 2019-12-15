"""
Defines a function to plot individual feature-level importances
across a dataset.
"""
import pandas as pd
import numpy as np
import altair as alt
import matplotlib as mpl
import matplotlib.pyplot as plt
from . import colors

def _get_bounds(arr):
    """
    A helper function to clip an array.
    Args:
        arr: A numpy array
    """
    vmin = np.nanpercentile(arr, 5)
    vmax = np.nanpercentile(arr, 95)
    if vmin == vmax:
        vmin = np.nanpercentile(arr, 1)
        vmax = np.nanpercentile(arr, 99)
        if vmin == vmax:
            vmin = np.min(arr)
            vmax = np.max(arr)
    return vmin, vmax

def scatter_plot(attributions,
                 feature_values,
                 feature_index,
                 interactions=None,
                 color_by=None,
                 feature_names=None,
                 scale_x_ind=False,
                 scale_y_ind=False,
                 figsize=5,
                 dpi=150,
                 **kwargs):
    """
    Function to draw an interactive scatter plot of
    attribution values. Since this is built on top
    of altair, this function works best when the
    number of points is small (< 5000).

    Args:
        attributions: A matrix of attributions.
                      Should be of shape [batch_size, feature_dims].
        feature_values: A matrix of feature values.
                        Should the same shape as the attributions.
        feature_index: The index of the feature to plot. If this is an integer,
                       indexes into attributions[:, feature_index]. If this is
                       a string, indexes into
                       attributions[:, where(features_names) == feature_index].
        interactions:  Either a matrix of the same shape as attributions representing
                       the interaction between feature_index and all other features,
                       or a matrix that can be indexed as
                       interactions[:, feature_index, color_by], which
                       provides the interaction between feature_index and color_by.
        color_by: An index of a feature to color the plot by. Follows the
                  same syntax as feature_index.
        feature_names: An optional list of length attributions.shape[1]. Each
                       entry should be a string representing the name of a feature.
        scale_x_ind: Set to True to scale the x axes of each plot independently.
                     Defaults to False.
        scale_y_ind: Set to True to scale the y axes of each plot independently.
                     Defaults to False.
        figsize: Figure size in matplotlib units. Each figure will be square.
        dpi: Resolution of each plot.
        kwargs: passed to matplotlib.pyplot.scatter
    """
    if not isinstance(feature_index, int):
        if feature_names is None:
            raise ValueError('Provided argument feature_index {} was '.format(feature_index) + \
                             'not an integer but feature_names was not specified.')
        feature_index = feature_names.index(feature_index)
    if color_by and not isinstance(color_by, int):
        if feature_names is None:
            raise ValueError('Provided argument color_by {} was '.format(color_by) + \
                             'not an integer but feature_names was not specified.')
        color_by = feature_names.index(color_by)

    if feature_names is None:
        feature_names = ['Feature {}'.format(i) for i in range(attributions.shape[1])]

    x_name = 'Value of {}'.format(feature_names[feature_index])
    y_name = 'Attribution to {}'.format(feature_names[feature_index])
    data_df = pd.DataFrame({
        x_name: feature_values[:, feature_index],
        y_name: attributions[:, feature_index]
    })

    color_name = None
    if color_by is not None:
        color_name = 'Value of {}'.format(feature_names[color_by])
        color_column = feature_values[:, color_by]
        vmin, vmax = _get_bounds(color_column)
        color_column = np.clip(color_column, vmin, vmax)

        data_df[color_name] = color_column

    chart = alt.Chart(data_df).mark_point(filled=True, size=20).encode(
        x=alt.X(x_name + ':Q'),
        y=alt.Y(y_name + ':Q')
    )

    if color_by is not None:
        chart = chart.encode(
            color=alt.Color(color_name + ':Q', scale=alt.Scale(scheme='goldgreen'))
        )

    if interactions is not None:
        if color_by is None:
            raise ValueError('Provided interactions but argument ' + \
                             'color_by was not specified')
        if interactions.shape == attributions.shape:
            interaction_column = 2.0 * interactions[:, color_by]
        else:
            interaction_column = interactions[:, feature_index, color_by] + \
                                 interactions[:, color_by, feature_index]

        inter_name = 'Interaction between {} and {}'.format(feature_names[feature_index],
                                                            feature_names[color_by])
        main_name = 'Main effect of {} '.format(feature_names[feature_index])
        inter_df = pd.DataFrame({
            x_name: feature_values[:, feature_index],
            color_name: color_column,
            inter_name: interaction_column,
            main_name:  attributions[:, feature_index] - interaction_column
        })
        # TODO: WHY DO WE MULTIPLY BY TWO ABOVE? THINK ABOUT
        # WHY WE SHOULD SUBTRACT BY BOTH i,j entry and j,i
        # IN TERMS OF COMPLETENESS -

    if color_by is not None:
        fig, axs = plt.subplots(1, 3, figsize=(3 * figsize + 1, figsize), dpi=dpi)
    else:
        fig, axis = plt.subplots(1, 1, figsize=(figsize, figsize), dpi=dpi)
        axs = [axis]

    x_limits, y_limits = _get_shared_limits(data_df[x_name], data_df[y_name],
                                            scale_x_ind, scale_y_ind)

    _single_scatter(axs[0], data_df, x_name, y_name, color_name, x_limits, y_limits, **kwargs)
    if color_by is not None:
        _single_scatter(axs[1], inter_df, x_name, inter_name,
                        color_name, x_limits, y_limits, **kwargs)
        _single_scatter(axs[2], inter_df, x_name, main_name,
                        color_name, x_limits, y_limits, **kwargs)
        _color_bar(fig, vmin, vmax, color_name, **kwargs)

    fig.suptitle('Attributions to {}'.format(feature_names[feature_index]), fontsize=18)

    return fig, axs

def _get_shared_limits(data_x, data_y, scale_x_ind, scale_y_ind):
    """
    Helper function to get shared plot limits
    """
    x_limits = None
    if not scale_x_ind:
        x_limits = [np.min(data_x), np.max(data_x)]
        x_range = x_limits[1] - x_limits[0]
        x_limits[0] -= x_range * 0.05
        x_limits[1] += x_range * 0.05

    y_limits = None
    if not scale_y_ind:
        y_limits = [np.min(data_y), np.max(data_y)]
        y_range = y_limits[1] - y_limits[0]
        y_limits[0] -= y_range * 0.05
        y_limits[1] += y_range * 0.05
    return x_limits, y_limits

def _color_bar(fig, vmin, vmax, color_name,
               ticks=True,
               label_size=14,
               **kwargs):
    """
    Helper function. Creates the color bar.
    """
    if 'cmap' not in kwargs:
        kwargs['cmap'] = colors.green_gold()

    fig.subplots_adjust(right=0.88)
    cbar_ax = fig.add_axes([0.9, 0.15, 0.01, 0.7])
    color_bar = fig.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(vmin=vmin,
                                                                             vmax=vmax),
                                                   cmap=kwargs['cmap']),
                             cax=cbar_ax,
                             orientation='vertical')
    color_bar.outline.set_visible(False)
    if ticks:
        cbar_ax.tick_params(length=6, labelsize=12)
        labelpad = 20
    else:
        vrange = vmax - vmin
        color_bar.set_ticks([vmin + vrange * 0.02, vmax - vrange * 0.02])
        cbar_ax.tick_params(size=0)
        cbar_ax.set_yticklabels(['Low', 'High'], fontsize=label_size)
        labelpad = 0
    color_bar.set_label(color_name, fontsize=label_size, rotation=270, labelpad=labelpad)

def _single_scatter(axis, data, x_name, y_name, color_name=None,
                    x_limits=None, y_limits=None, **kwargs):
    """
    Helper function. Generates a scatter plot with some custom
    settings.
    """
    axis.spines['right'].set_linewidth(0.2)
    axis.spines['top'].set_linewidth(0.2)
    axis.spines['left'].set_linewidth(0.5)
    axis.spines['bottom'].set_linewidth(0.5)

    if 's' not in kwargs:
        kwargs['s'] = 7
    if 'cmap' not in kwargs:
        kwargs['cmap'] = colors.green_gold()

    if color_name is not None:
        axis.scatter(x=data[x_name], y=data[y_name], c=data[color_name], **kwargs)
    else:
        axis.scatter(x=data[x_name], y=data[y_name], **kwargs)

    axis.grid(linewidth=0.5)
    axis.set_axisbelow(True)
    axis.tick_params(length=6, labelsize=12)
    axis.set_xlabel(x_name, fontsize=14)
    axis.set_ylabel(y_name, fontsize=14)

    if x_limits is not None:
        axis.set_xlim(x_limits)
    if y_limits is not None:
        axis.set_ylim(y_limits)
