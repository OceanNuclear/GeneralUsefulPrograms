import numpy as np
import pandas as pd
from pprint import pprint
import sys
import matplotlib.pyplot as plt
SEABORN_STYLE = False


def verify_data_shape(numpy_array):
    """Verify the numpy array received is a 2D array with 2 or 3 columns"""
    assert (
        np.ndim(numpy_array) == 2
    ), "Must have a 2D array (multiple data points, each with x,y, [y_err])"
    assert 2 <= np.shape(numpy_array)[1] <= 3, "Must have 2 or 3 columns"
    return


def fit_data_numpy(order, x, y, err=None):
    """fit the data to a polynomial of specified order, optionally weighted by error.

    Parameters
    ----------
    order : int, order of the fitted polynomial that we want.
    x : np.array, the x values of the samples.
    y : np.array, the y values of the samples.
    err : np.array, the standard deviation of the y values of the samples.

    Returns
    -------
    coefficients : The list of coefficients, associated to descending powers of x.
    pcov: Covariance matrix of the coefficients.
          To obtain the resulting standard deviations associated with each coefficient,
          take the square root of the main diagonal,
           i.e. np.sqrt(np.diag(pcov)).
    residuals: the difference between the thingy and the thingy.
    Note
    ----
    We DON'T need a fancy, non-deterministic optimization algorithm
        (which scopy.optimize.curve_fit is capable of) or provide any initial guess values.
        We can obtain the result directly using matrix inversion.

    Error (err) is entered into the w parameter of np.polyfit as 1/err,
    as denoted by the documentation.
    If you want proof that w=1/err is the correct value, start at
        https://github.com/numpy/numpy/commit/5c4aac16b54284a59bc5af34e731be7299cbb1d1
        which points to the issue #5261
        https://github.com/numpy/numpy/issues/5261
        that gives a nice explanation at just the right level of abstraction.

    The covariance matrix (pcov) is given by lhs.T.dot(lhs).
    """
    if err is not None:
        coefficients, pcov = np.polyfit(x, y, deg=order, w=1 / err, cov="unscaled")
    else:
        coefficients, pcov = np.polyfit(x, y, deg=order, cov="unscaled")
    return coefficients, pcov


def calculate_chi2(residuals, data_error):
    """Calculates the total chi2."""
    standard_scores = residuals / data_error
    return (standard_scores ** 2).sum()


def format_polynomial(degree, pretty_display_format):
    """Return the n-th degree polynomial as a text equation.
    E.g.if degree=2, then return 'y=a*x^2 + b*x + c'
        if degree=0, return 'a'.
    pretty_display_format allows matplotlib to superscript properly.
    """
    ord_of_a = ord("a")

    terms_as_text = []
    # we want to count DOWN (descending),
    # from the largest degree to the smallest degree.
    degree_list = list(range(degree))
    for term_num, deg in enumerate(degree_list[::-1]):
        # coefficient_alphabet = 'a', 'b', 'c', ...
        coefficient_alphabet = chr(ord_of_a + term_num)
        # separate handling for deg = 1 and 0.
        if deg > 1:
            if pretty_display_format:
                terms_as_text.append(
                    f"{coefficient_alphabet}" + r"$x^{" + f"{deg}" + r"}$"
                )
            else:  # terminal display format
                terms_as_text.append("{}*x^{}".format(coefficient_alphabet, deg))
        elif deg == 1:
            if pretty_display_format:
                terms_as_text.append(r"{}$x$".format(coefficient_alphabet))
            else:
                terms_as_text.append("{}*x".format(coefficient_alphabet))
        else:
            terms_as_text.append("{}".format(coefficient_alphabet))
    return "y = " + " + ".join(terms_as_text)


def format_coefficient_values(coefficients, std_devs, pretty_display_format):
    """Print the coefficient with std, separated by linebreaks.
    For example,
                coefficients=1.0, 2.0, 3.9
                with error 0.1, 0.2, 0.3 will be formatted to
               'a = 1.000 +/- 0.100
                b = 2.000 +/- 0.200
                c = 3.000 +/- 0.300'
    pretty_display_format optimizes for printing onto the plot by matplotlib
        (The ± becomes value)
    If pretty_display_format is enabled, then
        it'll round to the format 4.6e, and
        '+/-' would be replaced by the ± sign with $$ around it.
    This allows matplotlib to
        display the numbers without cluttering the plot, and
        display the +/- sign properly.
    """
    ord_of_a = ord("a")
    terms_as_text = []

    for term_num, (p, sigma_p) in enumerate(zip(coefficients, std_devs)):
        char = chr(ord_of_a + term_num)
        if pretty_display_format:
            terms_as_text.append(
                "{} = {:4.6e}".format(char, p) + r" $\pm$ " + "{:4.6e}".format(sigma_p)
            )
        else:  # terminal display format
            terms_as_text.append("{} = {} ± {}".format(char, p, sigma_p))
    return ",\n".join(terms_as_text)


def format_reduced_chi2(reduced_chi2, pretty_display_format):
    if pretty_display_format:
        return r"Reduced $\chi^2$ = " + "{:.2f}".format(reduced_chi2)
    else:
        return f"Reduced chi^2 = {reduced_chi2}"


def construct_displayed_equation(coefficients, coef_errors, display_on_plot=True):
    """Turn the coefficients into readable, meaningful strings; such that they can be displayed
    either as texts in the plot or as texts on the terminal."""
    polynomial_equation = format_polynomial(len(coefficients), display_on_plot)
    coefficient_and_error_text = format_coefficient_values(
        coefficients, coef_errors, display_on_plot
    )
    output_text = (
        "Fitted to " + polynomial_equation + ", where\n\n" + coefficient_and_error_text
    )
    return output_text


def format_covariance(covariance_matrix):
    """Print covariance information."""
    m = len(covariance_matrix)
    coef_chars = [chr(ord("a") + i) for i in range(m)]

    # listing the variances, cov(x_i,x_j) when i==j.
    output_text = []
    for i in range(m):
        c = coef_chars[i]
        output_text.append(f"cov({c}, {c}) = var({c}) = σ({c})^2")

    # listing the covariances, cov(x_i,x_j) when i!=j
    indices_loop = np.triu_indices(m, 1)
    for i, j in zip(indices_loop[0], indices_loop[1]):
        output_text.append(
            f"cov({coef_chars[i]}, {coef_chars[j]}) = {covariance_matrix[i][j]}"
        )
    return ",\n".join(output_text)


def fit_order_name(n):
    named_fits = {
        0: "fit to constant",
        1: "linear fit",
        2: "quadratic fit",
        3: "cubic fit",
        4: "quartic fit",
        5: "quintic fit",
    }
    if n in named_fits:
        return named_fits[n]
    else:
        return f"{n}" + r"${}^{th}$ order fit"

if __name__=="__main__":
    if len(sys.argv)>1:
        fname = sys.argv[1]
    else:
        fname = input("Please type in the file path to the csv file containing the data:")
    df = pd.read_csv(fname, index_col=None, comment='#')
    print("Found the following data:")
    print(df)
    chosen_columns = df.columns[:3]
    print(f"The titles of these {len(chosen_columns)} columns are parsed as:", chosen_columns.tolist())
    verify_data_shape(df[chosen_columns].to_numpy())
    print("Interpreting the the columns as:")
    pprint({c:ax for ax, c in zip(['x', 'y', 'error-on-y'], chosen_columns)}, sort_dicts=False) # zip will ignore the 'error-on-y' if len(df.columns)==3
    # input("Press enter to continue to fitting and plotting...")
    if len(chosen_columns)==3:
        x, y, err = df[chosen_columns].to_numpy().T
    elif len(chosen_columns)==2:
        x, y = df[chosen_columns].to_numpy().T
        err = None
    else:
        raise TypeError("Wrong shape of df. Programmer's error: this is supposed to be caught by verify_data_shape!")
    fit_order_input = input("Please enter the order of polynomial fit that you'd like to fit this data to (Leave blank if no fit) :")
    if fit_order_input=="":
        fit_order = None
    else:
        fit_order = int(fit_order_input)

    if fit_order is not None:
        # Polynomial fitting DOESN'T need guesses!
        try:
            coefficients, pcov = fit_data_numpy(fit_order, x, y, err)
        except Exception as fitting_error:
            # gracefully exit the program if there's an error with fitting. Give useful debug information.
            if isinstance(fitting_error, np.linalg.LinAlgError):
                # catch the specific case of "having too few data points".
                print("This error message below probably means you have too few data for such a high order of fit.")
                raise fitting_error
            elif isinstance(fitting_error, SystemError):  # possible
                print("Fitting failed.\nPossibly due to having too-small sigma's/ invalid values in the file.")
                raise fitting_error
            else:  # catch every other error that happens during fitting.
                print("Numpy fitting error.")
                raise fitting_error
            sys.exit()

        # Step 2.5: calculate the chi2
        fitted_equation = np.poly1d(coefficients)
        yfit = fitted_equation(x)
        residuals = yfit - y

        reduced_chi2 = None
        if err is not None:
            try:
                total_chi2 = calculate_chi2(residuals, err)
            except Exception as chi2_calculation_error:
                print("Possible cause of error: an unphysically small sigma was used in one of the datapoints?")
                raise chi2_calculation_error
                sys.exit()

            DoF = len(x) - (fit_order + 1)
            if DoF > 0:
                reduced_chi2 = total_chi2 / DoF
            elif DoF == 0:
                raise ValueError("Too few data points: Number of data points = number of fitting parameters, which is fully determined fitting.")
            else:
                raise ValueError("Too few data points: Number of data points < number of fitting parameters, which is a underdetermined fitting operation. You're using the wrong program.")

        # Step 3: print fitting results.
        std_devs = np.sqrt(np.diag(pcov))
        print(
            construct_displayed_equation(coefficients, std_devs, display_on_plot=False)
        )
        # print("R^2 measures what fraction of the observed variance in y is explained by the model.")
        # print(f"R^2={R2}")
        if err is not None:
            print(f"chi^2 = {total_chi2}")
            if DoF > 0:
                print(f"number of degrees of freedom = {DoF}")
                # print(f"chi^2/DoF = {reduced_chi2}")
                print(format_reduced_chi2(reduced_chi2, False))
        # error-related fitting information information
        print("_" * 50)
        print("Covariance information (You rarely need this):")
        print(format_covariance(pcov))

    # Step 4: plot fitting results.
    plot_title = input("Please type the title of the plot:")
    if SEABORN_STYLE:
        plt.style.use("seaborn")
        plt.rcParams.update({"lines.markeredgewidth": 1})
    if err is None:
        plt.scatter(x, y, marker="x", label="data points")
        # plt.scatter(x, y, marker='x', label="data points")
    else:
        plt.errorbar(
            x, y, yerr=err, fmt="x", markersize=8, capsize=4, label="data points"
        )
    if fit_order is None:
        text_in_box = ""
    else:
        text_in_box = construct_displayed_equation(
            coefficients, std_devs, display_on_plot=True
        )

    if fit_order is not None:
        xs = np.linspace(min(x), max(x), 500)
        ys = fitted_equation(xs)
        plt.plot(xs, ys, color="black", label=fit_order_name(fit_order))
        if err is not None and DoF > 0:
            text_in_box += "\n\n" + format_reduced_chi2(reduced_chi2, True)
    bbox_props = dict(boxstyle="square,pad=0.7", fc="w", ec="k", lw=1)
    plt.annotate(
        text_in_box,
        xy=(25, 500),
        xycoords="figure pixels",
        horizontalalignment="left",
        verticalalignment="top",
        size=9,
        bbox=bbox_props,
    )
    plt.subplots_adjust(left=0.4)
    plt.grid(True)
    plt.title(plot_title)
    plt.xlabel(chosen_columns[0])
    plt.ylabel(chosen_columns[1])
    plt.legend()
    # My design philosophy is that programs aren't supposed to have hidden behaviours,
    #   i.e. if you didn't explicitly tell my program to save the plot, it WON'T save the plot.
    # Therefore I've remvoed the savefig() line.
    # Students MUST press the save icon to save their plot.
    plt.show()
