def read_df(filename=None):
    import sys
    import pandas as pd

    if filename:
        csv = filename
    elif len(sys.argv)>1:
        csv = sys.argv[1]
    else:
        csv = input("Name of csv data file to be fitted:")
    dataframe = pd.read_csv(csv, index_col=[0])
    return dataframe

def choose_xy(dataframe):
    print(f"dataframe read in has the following columns.")
    for i, col_name in enumerate(dataframe.columns):
        print(f"{i}:{col_name}")

    x = dataframe.columns[int(input("Please choose the x value column by inputting the corresponding index."))]
    print(f"You have chosen x={x}")
    y = dataframe.columns[int(input("Please choose the y value column by inputting the corresponding index."))]
    print(f"You have chosen y={y}")
    return x, y

def fit_interactively_and_show(dataframe, x, y, w=None, PLOTLY=True):
    """Note that this returns the fitted coefficients p in desceneding powers,
    i.e. following numpy convention."""
    from pprint import pprint
    import numpy as np
    p = np.polyfit( dataframe[x],
                    dataframe[y],
                    int(input("degrees of the polynomial to be fitted")),
                    w=w,
                    )# rank, singular_vals, rcond all are irrelevant diagnostic information
    print("The coefficients of the polynomial fit, in increasing powers, is as follows:")
    pprint(p[::-1])
    expression_str = "y =" + " + ".join([f"{c} * x^{i}" for i, c in enumerate(p[::-1])])
    print("i.e.", expression_str)

    fit_equation = np.poly1d(p)
    yfit = fit_equation(dataframe[x])
    residuals = dataframe[y] - yfit

    if PLOTLY:
        import plotly.express as px
        dataframe["yfit"] = yfit
        dataframe["residuals"] = residuals
        fig = px.scatter(dataframe, x=x, y="residuals", title=f"Residual plot after fitting")
        fig.show()

    else:
        import matplotlib.pyplot as plt
        deviation_bars = np.vstack([residuals, np.zeros_like(yfit)])
        plt.title("Residual plot")
        plt.xlabel(x)
        plt.ylabel(y)
        plt.plot([min(dataframe[x]), max(dataframe[x])], [0, 0], color='black') # plot the y=0 trend line.
        plt.plot(np.vstack([dataframe[x], dataframe[x]]), deviation_bars, color="C0")
        plt.scatter(dataframe[x], residuals, marker='x', color='black')
        plt.show()
    return fit_equation, residuals

if __name__=="__main__":
    dataframe = read_df()
    x, y = choose_xy(dataframe)
    selected_df = dataframe
    # selected_df = dataframe[dataframe["distance"]=='0']
    fit_interactively_and_show(selected_df, x, y, PLOTLY=False)