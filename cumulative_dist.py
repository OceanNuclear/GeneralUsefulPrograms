from numpy import array as ary
import numpy as np
from matplotlib import pyplot as plt

def cumulative_dist_plot(unordered_vector, *args, **kwargs):
    new_list = ary(unordered_vector)[np.isfinite(unordered_vector)]
    sorted_list = np.sort(new_list)
    plt.step(sorted_list, np.linspace(0, 1, len(sorted_list)), *args, **kwargs)
    plt.title('Cumulative distribution of fraction of values less than x')
    plt.xlabel('x')
    return sorted_list