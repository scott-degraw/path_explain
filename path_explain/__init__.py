"""
A module for explaining the output of gradient-based
models using path attributions.
"""
__version__ = '1.0'

from .explainers.path_explainer_torch import PathExplainerTorch
from .plot.scatter import scatter_plot
from .plot.summary import summary_plot
from .plot.text import text_plot, matrix_interaction_plot, bar_interaction_plot
