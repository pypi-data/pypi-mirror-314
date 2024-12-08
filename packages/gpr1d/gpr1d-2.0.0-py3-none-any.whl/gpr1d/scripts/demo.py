#!/usr/bin/env python

import os
import sys
import re
import inspect
from operator import itemgetter
from pathlib import Path
import numpy as np

# Required import, only works after using 'pip install'
from gpr1d.core.kernels import RQ_Kernel
from gpr1d.core.routines import GaussianProcessRegression1D


def run_demo():
    '''
    A demonstration script for the classes within the GPR1D module.

    Due to the iterative nature of the optimization method and the
    random nature of the kernel restart function, the results may
    not be exactly the same for consecutive runs of this demo
    script. However, all fits should fall within the fit error
    ranges of each other, unless the optimization algorithm has
    not converged.
    '''

    ### Some basic setup

    plot_save_directory = Path('GPPlots')
    plot_save_directory.mkdir(parents=True, exist_ok=True)
    if not plot_save_directory.is_dir():
        raise IOError(f'Demo save directory, {plot_save_directory}, already exists and is not a directory. Aborting!')


    ### Generating sample data

    # Make basic function data
    x_spread = 0.01
    y_spread = 0.25
    intercept = 3.0
    slope1 = 1.0
    x_values = np.linspace(0.0, 1.0, 21)
    y_values = slope1 * x_values + intercept
    boundary1 = 0.3
    slope2 = 16.0
    boundary1_filter = (x_values >= boundary1)
    y_values[boundary1_filter] = y_values[boundary1_filter] - slope2 * (x_values[boundary1_filter] - boundary1)
    boundary2 = 0.7
    boundary2_filter = (x_values >= boundary2)
    y_values[boundary2_filter] = y_values[boundary2_filter] + (slope2 + slope1) * (x_values[boundary2_filter] - boundary2)

    # Add random error to generated data points
    raw_x_values = x_values + x_spread * np.random.randn(x_values.size)
    raw_y_values = y_values + y_spread * np.random.randn(y_values.size)
    raw_x_errors = np.full(raw_x_values.shape, x_spread)
    raw_y_errors = np.full(raw_y_values.shape, y_spread)
    raw_intercept = raw_y_values[0]



    ### Fitting

    fit_x_values = np.linspace(0.0, 1.0, 100)

    # Define a kernel to fit the data itself
    #     Rational quadratic kernel is usually robust enough for general fitting
    kernel = RQ_Kernel(1.0e0, 1.0e0, 5.0e0)

    # This is only necessary if using kernel restart option on the data fitting
    kernel_hyppar_bounds = np.atleast_2d([[1.0e-1, 1.0e-1, 5.0e0], [1.0e1, 1.0e0, 2.0e1]])

    # Define a kernel to fit the given y-errors, needed for rigourous estimation of fit error including data error
    #     Typically a simple rational quadratic kernel is sufficient given a high regularization parameter (specified later)
    #     Here, the RQ kernel is summed with a noise kernel for extra robustness and to demonstrate how to use operator kernels
    error_kernel = RQ_Kernel(1.0e-1, 1.0e0, 5.0e0)

    # Again, this is only necessary if using kernel restart option on the error fitting
    error_kernel_hyppar_bounds = np.atleast_2d([[1.0e-1, 1.0e-1, 1.0e0, ], [1.0e1, 1.0e0, 1.0e1]])


    # GPR fit using y-errors only as weights
    #     Create class object to store raw data, kernels, and settings
    gpr_object = GaussianProcessRegression1D()

    # Print source location for reference, in case of multiple installations
    location = Path(inspect.getsourcefile(type(gpr_object)))
    print(f'Using GPR1D definition from: {location.parent.resolve()}')

    #     Define the kernel and regularization parameter to be used in the data fitting routine
    gpr_object.set_kernel(
        kernel=kernel,
        kbounds=kernel_hyppar_bounds,
        regpar=1.0
    )

    #     Define the raw data and associated errors to be fitted
    gpr_object.set_raw_data(
        xdata=raw_x_values,
        ydata=raw_y_values,
        yerr=raw_y_errors,
        xerr=raw_x_errors,
        dxdata=[0.0],         # Example of applying derivative constraints
        dydata=[0.0],
        dyerr=[0.0]
    )

    #     Define the search criteria for data fitting routine and error fitting routine
    gpr_object.set_search_parameters(epsilon=1.0e-2)
    gpr_object.set_error_search_parameters(epsilon=1.0e-1)

    #     Default optimizer is gradient ascent / descent - extremely robust but slow
    #     Uncomment any of the following lines to test the recommended optimizers
    #gpr_object.set_search_parameters(epsilon=1.0e-2, method='adam', spars=[1.0e-1, 0.4, 0.8])
    #gpr_object.set_error_search_parameters(epsilon=1.0e-1, method='adam', spars=[1.0e-1, 0.4, 0.8])

    #     Perform the fit with kernel restarts
    gpr_object.GPRFit(fit_x_values, hsgp_flag=False, nrestarts=5)

    #     Grab optimized kernel settings - easy way to minimize data storage requirements for fit reproduction
    (gp_kernel_name, gp_kernel_hyppars, gp_fit_regpar) = gpr_object.get_gp_kernel_details()

    #     Grab fit results
    (fit_y_values, fit_y_errors, fit_dydx_values, fit_dydx_errors) = gpr_object.get_gp_results()

    #     Grab the log-marginal-likelihood of fit
    fit_lml = gpr_object.get_gp_lml()


    # GPR fit rigourously accounting only for y-errors (this is the recommended option)
    #     Procedure is nearly identical to above, except for the addition of an error kernel
    hsgpr_object = GaussianProcessRegression1D()

    #     Define the kernel and regularization parameter to be used in the data fitting routine
    hsgpr_object.set_kernel(
        kernel=kernel,
        kbounds=kernel_hyppar_bounds,
        regpar=1.0
    )

    #     Define the kernel and regularization parameter to be used in the error fitting routine
    hsgpr_object.set_error_kernel(
        kernel=error_kernel,
        kbounds=error_kernel_hyppar_bounds,
        regpar=2.0
    )

    #     Define the raw data and associated errors to be fitted
    hsgpr_object.set_raw_data(
        xdata=raw_x_values,
        ydata=raw_y_values,
        yerr=raw_y_errors,
        xerr=raw_x_errors,
        dxdata=[0.0],           # Example of applying derivative constraints
        dydata=[0.0],
        dyerr=[0.0]
    )

    #     Define the search criteria for data fitting routine and error fitting routine
    hsgpr_object.set_search_parameters(epsilon=1.0e-2)
    hsgpr_object.set_error_search_parameters(epsilon=1.0e-1)

    #     Default optimizer is gradient ascent / descent - extremely robust but slow
    #     Uncomment any of the following lines to test the recommended optimizers
    #hsgpr_object.set_search_parameters(epsilon=1.0e-2, method='adam', spars=[1.0e-1, 0.4, 0.8])
    #hsgpr_object.set_error_search_parameters(epsilon=1.0e-1, method='adam', spars=[1.0e-1, 0.4, 0.8])

    #     Perform the fit with kernel restarts
    hsgpr_object.GPRFit(fit_x_values, hsgp_flag=True, nrestarts=5)

    #     Grab optimized kernel settings - easy way to minimize data storage requirements for fit reproduction
    (hsgp_kernel_name, hsgp_kernel_hyppars, hsgp_fit_regpar) = hsgpr_object.get_gp_kernel_details()
    (hsgp_error_kernel_name, hsgp_error_kernel_hyppars, hsgp_error_fit_regpar) = hsgpr_object.get_gp_error_kernel_details()

    #     Grab fit results
    (hs_fit_y_values, hs_fit_y_errors, hs_fit_dydx_values, hs_fit_dydx_errors) = hsgpr_object.get_gp_results()
    (hs_zfit_y_values, hs_zfit_y_errors, hs_zfit_dydx_values, hs_zfit_dydx_errors) = hsgpr_object.get_gp_results(noise_flag=False)

    #     Grab the log-marginal-likelihood of fit
    hs_fit_lml = hsgpr_object.get_gp_lml()


    # GPR fit rigourously accounting for y-errors AND x-errors
    #     Procedure is nearly identical to above, except for the addition of an extra option
    nigpr_object = GaussianProcessRegression1D()
    nigpr_object.set_kernel(
        kernel=kernel,
        kbounds=kernel_hyppar_bounds,
        regpar=1.0
    )
    nigpr_object.set_error_kernel(
        kernel=error_kernel,
        kbounds=error_kernel_hyppar_bounds,
        regpar=2.0
    )
    nigpr_object.set_raw_data(
        xdata=raw_x_values,
        ydata=raw_y_values,
        yerr=raw_y_errors,
        xerr=raw_x_errors,
        dxdata=[0.0],
        dydata=[0.0],
        dyerr=[0.0]
    )
    nigpr_object.set_search_parameters(epsilon=1.0e-2)
    nigpr_object.set_error_search_parameters(epsilon=1.0e-1)

    #     Uncomment any of the following lines to test the recommended optimizers
    #nigpr_object.set_search_parameters(epsilon=1.0e-2, method='adam', spars=[1.0e-1, 0.4, 0.8])
    #nigpr_object.set_error_search_parameters(epsilon=1.0e-1, method='adam', spars=[1.0e-1, 0.4, 0.8])

    #     Perform the fit with kernel restarts, here is the extra option to account for x-errors in fit
    nigpr_object.GPRFit(fit_x_values, hsgp_flag=True, nigp_flag=True, nrestarts=5)

    # Grab outputs
    (nigp_kernel_name, nigp_kernel_hyppars, nigp_fit_regpar) = nigpr_object.get_gp_kernel_details()
    (nigp_error_kernel_name, nigp_error_kernel_hyppars, nigp_error_fit_regpar) = nigpr_object.get_gp_error_kernel_details()
    (ni_fit_y_values, ni_fit_y_errors, ni_fit_dydx_values, ni_fit_dydx_errors) = nigpr_object.get_gp_results()
    ni_fit_lml = nigpr_object.get_gp_lml()



    ### Sampling distribution (only done with HSGP option)

    num_samples = 10000

    # Samples the fit distribution - smooth noise representation
    sample_array = hsgpr_object.sample_GP(num_samples, actual_noise=False)

    # Calculates the derivatives of the sampled fit distributions
    dfit_x_values = (fit_x_values[1:] + fit_x_values[:-1]) / 2.0
    deriv_array = (sample_array[:, 1:] - sample_array[:, :-1]) / (fit_x_values[1:] - fit_x_values[:-1])

    # Samples the derivative distribution - smooth noise representation
    dsample_array = hsgpr_object.sample_GP_derivative(num_samples, actual_noise=False)

    # Calculates the integrals of the sampled derivative distributions
    ifit_x_values = dfit_x_values.copy()
    integ_array = dsample_array[:, 1] * (ifit_x_values[0] - fit_x_values[0]) # + raw_intercept
    if integ_array.ndim == 1:
        integ_array = np.transpose(np.atleast_2d(integ_array))
    for jj in np.arange(1, dsample_array.shape[1]-1):
        integ = integ_array[:, jj-1] + dsample_array[:, jj] * (ifit_x_values[jj] - ifit_x_values[jj-1])
        if integ.ndim == 1:
            integ = np.transpose(np.atleast_2d(integ))
        integ_array = np.hstack((integ_array, integ))
    # Integrals require renormalization to the fit mean to define the constant of integration that is lost
    orig_mean = np.nanmean(hs_fit_y_values)
    for ii in np.arange(0, num_samples):
        sint_mean = np.nanmean(integ_array[ii, :])
        integ_array[ii, :] = integ_array[ii, :] - sint_mean + orig_mean

    # Samples the fit distribution - true noise representation
    nsample_array = hsgpr_object.sample_GP(num_samples, actual_noise=True)

    # Samples the derivative distribution - true noise representation
    ndsample_array = hsgpr_object.sample_GP_derivative(num_samples, actual_noise=True)

    # Samples the fit distribution - zero noise representation
    zsample_array = hsgpr_object.sample_GP(num_samples, without_noise=True)

    # Calculates the derivatives of the sampled fit distributions - zero noise representation
    zderiv_array = (zsample_array[:, 1:] - zsample_array[:, :-1]) / (fit_x_values[1:] - fit_x_values[:-1])

    # Samples the derivative distribution - zero noise representation
    #    Note that zero noise is only different from smooth noise if an error kernel is used
    zdsample_array = hsgpr_object.sample_GP_derivative(num_samples, without_noise=True)

    # Calculates the integrals of the sampled derivative distributions - zero noise representation
    zinteg_array = zdsample_array[:, 1] * (ifit_x_values[0] - fit_x_values[0]) # + raw_intercept
    if zinteg_array.ndim == 1:
        zinteg_array = np.transpose(np.atleast_2d(zinteg_array))
    for jj in np.arange(1, zdsample_array.shape[1]-1):
        zinteg = zinteg_array[:, jj-1] + zdsample_array[:, jj] * (ifit_x_values[jj] - ifit_x_values[jj-1])
        if zinteg.ndim == 1:
            zinteg = np.transpose(np.atleast_2d(zinteg))
        zinteg_array = np.hstack((zinteg_array, zinteg))
    # Integrals require renormalization to the fit mean to define the constant of integration that is lost
    zorig_mean = np.nanmean(hs_zfit_y_values)
    for ii in np.arange(0, num_samples):
        zsint_mean = np.nanmean(zinteg_array[ii, :])
        zinteg_array[ii, :] = zinteg_array[ii, :] - zsint_mean + zorig_mean

    # Computing statistics of sampled profiles
    sample_mean = np.nanmean(sample_array, axis=0)
    deriv_mean = np.nanmean(deriv_array, axis=0)
    dsample_mean = np.nanmean(dsample_array, axis=0)
    integ_mean = np.nanmean(integ_array, axis=0)
    sample_std = np.nanstd(sample_array, axis=0)
    deriv_std = np.nanstd(deriv_array, axis=0)
    dsample_std = np.nanstd(dsample_array, axis=0)
    integ_std = np.nanstd(integ_array, axis=0)

    # Computing statistics of sampled profiles - zero noise representation
    zsample_mean = np.nanmean(zsample_array, axis=0)
    zderiv_mean = np.nanmean(zderiv_array, axis=0)
    zdsample_mean = np.nanmean(zdsample_array, axis=0)
    zinteg_mean = np.nanmean(zinteg_array, axis=0)
    zsample_std = np.nanstd(zsample_array, axis=0)
    zderiv_std = np.nanstd(zderiv_array, axis=0)
    zdsample_std = np.nanstd(zdsample_array, axis=0)
    zinteg_std = np.nanstd(zinteg_array, axis=0)



    ### Printing

    gp_str = f'\n--- GPR Fit ---\n\n'
    gp_str += f'Kernel name: {gp_kernel_name:30}\n'
    gp_str += f'Regularization parameter: {gp_fit_regpar:17.4f}\n'
    gp_str += f'Optimized kernel hyperparameters:\n'
    for hh in np.arange(0, gp_kernel_hyppars.size):
        gp_str += f'{gp_kernel_hyppars[hh]:15.6e}'
    gp_str += '\n\n'
    gp_str += f'Log-marginal-likelihood: {fit_lml:18.6f}\n'

    print(gp_str)

    hsgp_str = f'\n--- HSGPR Fit ---\n\n'
    hsgp_str += f'Kernel name: {hsgp_kernel_name:30}\n'
    hsgp_str += f'Regularization parameter: {hsgp_fit_regpar:17.4f}\n'
    hsgp_str += f'Optimized kernel hyperparameters:\n'
    for hh in np.arange(0, hsgp_kernel_hyppars.size):
        hsgp_str += f'{hsgp_kernel_hyppars[hh]:15.6e}'
    hsgp_str += f'\n\n'
    hsgp_str += f'Error kernel name: {hsgp_error_kernel_name:24}\n'
    hsgp_str += f'Regularization parameter: {hsgp_error_fit_regpar:17.4f}\n'
    hsgp_str += f'Optimized error kernel hyperparameters:\n'
    for hh in np.arange(0, hsgp_error_kernel_hyppars.size):
        hsgp_str += f'{hsgp_error_kernel_hyppars[hh]:15.6e}'
    hsgp_str += f'\n\n'
    hsgp_str += f'Log-marginal-likelihood: {hs_fit_lml:18.6f}\n'

    print(hsgp_str)

    nigp_str = f'--- NIGPR Fit ---\n\n'
    nigp_str += f'Kernel name: {nigp_kernel_name:30}\n'
    nigp_str += f'Regularization parameter: {nigp_fit_regpar:17.4f}\n'
    nigp_str += f'Optimized kernel hyperparameters:\n'
    for hh in np.arange(0, nigp_kernel_hyppars.size):
        nigp_str += f'{nigp_kernel_hyppars[hh]:15.6e}'
    nigp_str += f'\n\n'
    nigp_str += f'Error kernel name: {nigp_error_kernel_name:24}\n'
    nigp_str += f'Regularization parameter: {nigp_error_fit_regpar:17.4f}\n'
    nigp_str += f'Optimized error kernel hyperparameters:\n'
    for hh in np.arange(0, nigp_error_kernel_hyppars.size):
        nigp_str += f'{nigp_error_kernel_hyppars[hh]:15.6e}'
    nigp_str += f'\n\n'
    nigp_str += f'Log-marginal-likelihood: {ni_fit_lml:18.6f}\n'

    print(nigp_str)



    ### Plotting

    plt = None
    try:
        import matplotlib.pyplot as plt
    except:
        plt = None

    if plt is not None:

        plot_num_samples = 10
        plot_sigma = 2.0

        # Raw data with GPR fit and error, only accounting for y-errors
        save_file = plot_save_directory / 'gp_test.png'
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plot_raw_y_errors = plot_sigma * raw_y_errors
        ax.errorbar(raw_x_values, raw_y_values, yerr=plot_raw_y_errors, ls='', marker='.', color='k')
        ax.plot(fit_x_values, hs_fit_y_values, color='r')
        plot_hs_fit_y_lower = hs_fit_y_values - plot_sigma * hs_fit_y_errors
        plot_hs_fit_y_upper = hs_fit_y_values + plot_sigma * hs_fit_y_errors
        ax.fill_between(fit_x_values, plot_hs_fit_y_lower, plot_hs_fit_y_upper, facecolor='r', edgecolor='None', alpha=0.2)
        ax.set_xlim(0.0, 1.0)
        fig.savefig(save_file)
        plt.close(fig)

        # Derivative of GPR fit and error, only accounting for y-errors
        save_file = plot_save_directory / 'gp_dtest.png'
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(fit_x_values, fit_dydx_values, color='r')
        plot_hs_fit_dydx_lower = hs_fit_dydx_values - plot_sigma * hs_fit_dydx_errors
        plot_hs_fit_dydx_upper = hs_fit_dydx_values + plot_sigma * hs_fit_dydx_errors
        ax.fill_between(fit_x_values, plot_hs_fit_dydx_lower, plot_hs_fit_dydx_upper, facecolor='r', edgecolor='None', alpha=0.2)
        ax.set_xlim(0.0, 1.0)
        fig.savefig(save_file)
        plt.close(fig)

        # Raw data with GPR fit and error, comparison of using y-errors as weights, rigourously accounting for y-errors, and rigourously account for y-errors AND x-errors
        save_file = plot_save_directory / 'gp_options_test.png'
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plot_raw_x_errors = plot_sigma * raw_x_errors
        ax.errorbar(raw_x_values, raw_y_values, xerr=plot_raw_x_errors, yerr=plot_raw_y_errors, ls='', marker='.', color='k')
        ax.plot(fit_x_values, fit_y_values, color='g')
        plot_fit_y_lower = fit_y_values - plot_sigma * fit_y_errors
        plot_fit_y_upper = fit_y_values + plot_sigma * fit_y_errors
        ax.plot(fit_x_values, plot_fit_y_lower, color='g', ls='--')
        ax.plot(fit_x_values, plot_fit_y_upper, color='g', ls='--')
        #ax.fill_between(fit_x_values, plot_fit_y_lower, plot_fit_y_upper, facecolor='g', edgecolor='None', alpha=0.2)
        ax.plot(fit_x_values, hs_fit_y_values, color='r')
        ax.plot(fit_x_values, plot_hs_fit_y_lower, color='r', ls='--')
        ax.plot(fit_x_values, plot_hs_fit_y_upper, color='r', ls='--')
        #ax.fill_between(fit_x_values, plot_hs_fit_y_lower, plot_hs_fit_y_upper, facecolor='r', edgecolor='None', alpha=0.2)
        ax.plot(fit_x_values, ni_fit_y_values, color='b')
        plot_ni_fit_y_lower = ni_fit_y_values - plot_sigma * ni_fit_y_errors
        plot_ni_fit_y_upper = ni_fit_y_values + plot_sigma * ni_fit_y_errors
        ax.plot(fit_x_values, plot_ni_fit_y_lower, color='b', ls='--')
        ax.plot(fit_x_values, plot_ni_fit_y_upper, color='b', ls='--')
        #ax.fill_between(fit_x_values, plot_ni_fit_y_lower, plot_ni_fit_y_upper, facecolor='b', edgecolor='None', alpha=0.2)
        ax.set_xlim(0.0, 1.0)
        fig.savefig(save_file)
        plt.close(fig)

        # Derivative of GPR fit and error, comparison of using y-errors as weights, rigourously accounting for y-errors, and rigourously account for y-errors AND x-errors
        save_file = plot_save_directory / 'gp_options_dtest.png'
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(fit_x_values, fit_dydx_values, color='g')
        plot_fit_dydx_lower = fit_dydx_values - plot_sigma * fit_dydx_errors
        plot_fit_dydx_upper = fit_dydx_values + plot_sigma * fit_dydx_errors
        ax.plot(fit_x_values, plot_fit_dydx_lower, color='g', ls='--')
        ax.plot(fit_x_values, plot_fit_dydx_upper, color='g', ls='--')
        #ax.fill_between(fit_x_values, plot_fit_dydx_lower, plot_fit_dydx_upper, facecolor='g', edgecolor='None', alpha=0.2)
        ax.plot(fit_x_values, hs_fit_dydx_values, color='r')
        ax.plot(fit_x_values, plot_hs_fit_dydx_lower, color='r', ls='--')
        ax.plot(fit_x_values, plot_hs_fit_dydx_upper, color='r', ls='--')
        #ax.fill_between(fit_x_values, plot_hs_fit_dydx_lower, plot_hs_fit_dydx_upper, facecolor='r', edgecolor='None', alpha=0.2)
        ax.plot(fit_x_values, ni_fit_dydx_values, color='b')
        plot_ni_fit_dydx_lower = ni_fit_dydx_values - plot_sigma * ni_fit_dydx_errors
        plot_ni_fit_dydx_upper = ni_fit_dydx_values + plot_sigma * ni_fit_dydx_errors
        ax.plot(fit_x_values, plot_ni_fit_dydx_lower, color='b', ls='--')
        ax.plot(fit_x_values, plot_ni_fit_dydx_upper, color='b', ls='--')
        #ax.fill_between(fit_x_values, plot_ni_fit_dydx_lower, plot_ni_fit_dydx_upper, facecolor='b', edgecolor='None', alpha=0.2)
        ax.set_xlim(0.0, 1.0)
        fig.savefig(save_file)
        plt.close(fig)

        # Sampled fit curves (smooth noise) against GPR fit distribution
        save_file = plot_save_directory / 'sample_gp_test.png'
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.fill_between(fit_x_values, plot_hs_fit_y_lower, plot_hs_fit_y_upper, facecolor='r', edgecolor='None', alpha=0.2)
        for ii in np.arange(0, plot_num_samples):
            ax.plot(fit_x_values, sample_array[ii, :], color='k', alpha=0.5)
        plot_hs_sample_y_lower = sample_mean - plot_sigma * sample_std
        plot_hs_sample_y_upper = sample_mean + plot_sigma * sample_std
        ax.fill_between(fit_x_values, plot_hs_sample_y_lower, plot_hs_sample_y_upper, facecolor='b', edgecolor='None', alpha=0.2)
        ax.set_xlim(0.0, 1.0)
        fig.savefig(save_file)
        plt.close(fig)

        # Derivatives of sampled fit curves (smooth noise) against GPR fit derivative distribution
        save_file = plot_save_directory / 'sample_gp_der_test.png'
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.fill_between(fit_x_values, plot_hs_fit_dydx_lower, plot_hs_fit_dydx_upper, facecolor='r', edgecolor='None', alpha=0.2)
        for ii in np.arange(0, plot_num_samples):
            ax.plot(dfit_x_values, deriv_array[ii, :], color='k', alpha=0.5)
        plot_hs_sample_dydx_lower = deriv_mean - plot_sigma * deriv_std
        plot_hs_sample_dydx_upper = deriv_mean + plot_sigma * deriv_std
        ax.fill_between(dfit_x_values, plot_hs_sample_dydx_lower, plot_hs_sample_dydx_upper, facecolor='b', edgecolor='None', alpha=0.2)
        ax.set_xlim(0.0, 1.0)
        fig.savefig(save_file)
        plt.close(fig)

        # Sampled fit derivative curves (smooth noise) against GPR fit derivative distribution
        save_file = plot_save_directory / 'sample_gp_dtest.png'
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.fill_between(fit_x_values, plot_hs_fit_dydx_lower, plot_hs_fit_dydx_upper, facecolor='r', edgecolor='None', alpha=0.2)
        for ii in np.arange(0, plot_num_samples):
            ax.plot(fit_x_values, dsample_array[ii, :], color='k', alpha=0.5)
        plot_hs_dsample_dydx_lower = dsample_mean - plot_sigma * dsample_std
        plot_hs_dsample_dydx_upper = dsample_mean + plot_sigma * dsample_std
        ax.fill_between(fit_x_values, plot_hs_dsample_dydx_lower, plot_hs_dsample_dydx_upper, facecolor='b', edgecolor='None', alpha=0.2)
        ax.set_xlim(0.0, 1.0)
        fig.savefig(save_file)
        plt.close(fig)

        # Integrals of sampled fit derivative curves (smooth noise) against GPR fit distribution
        save_file = plot_save_directory / 'sample_gp_int_dtest.png'
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.fill_between(fit_x_values, plot_hs_fit_y_lower, plot_hs_fit_y_upper, facecolor='r', edgecolor='None', alpha=0.2)
        for ii in np.arange(0, plot_num_samples):
            ax.plot(ifit_x_values, integ_array[ii, :], color='k', alpha=0.5)
        plot_hs_dsample_y_lower = integ_mean - plot_sigma * integ_std
        plot_hs_dsample_y_upper = integ_mean + plot_sigma * integ_std
        ax.fill_between(ifit_x_values, plot_hs_dsample_y_lower, plot_hs_dsample_y_upper, facecolor='b', edgecolor='None', alpha=0.2)
        ax.set_xlim(0.0, 1.0)
        fig.savefig(save_file)
        plt.close(fig)

        # Sampled fit curves (true noise) against GPR fit distribution
        save_file = plot_save_directory / 'sample_gp_noisy_test.png'
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.fill_between(fit_x_values, plot_hs_fit_y_lower, plot_hs_fit_y_upper, facecolor='r', edgecolor='None', alpha=0.2)
        for ii in np.arange(0, plot_num_samples):
            ax.plot(fit_x_values, nsample_array[ii, :], color='k', alpha=0.5)
        ax.set_xlim(0.0, 1.0)
        fig.savefig(save_file)
        plt.close(fig)

        # Sampled fit derivative curves (true noise) against GPR fit derivative distribution
        save_file = plot_save_directory / 'sample_gp_noisy_dtest.png'
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.fill_between(fit_x_values, plot_hs_fit_dydx_lower, plot_hs_fit_dydx_upper, facecolor='r', edgecolor='None', alpha=0.2)
        for ii in np.arange(0, plot_num_samples):
            ax.plot(fit_x_values, ndsample_array[ii, :], color='k', alpha=0.5)
        ax.set_xlim(0.0, 1.0)
        fig.savefig(save_file)
        plt.close(fig)

        # Sampled fit curves (zero noise) against GPR fit distribution
        save_file = plot_save_directory / 'sample_gp_no_noise_test.png'
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plot_hs_zfit_y_lower = hs_zfit_y_values - plot_sigma * hs_zfit_y_errors
        plot_hs_zfit_y_upper = hs_zfit_y_values + plot_sigma * hs_zfit_y_errors
        ax.fill_between(fit_x_values, plot_hs_zfit_y_lower, plot_hs_zfit_y_upper, facecolor='r', edgecolor='None', alpha=0.2)
        for ii in np.arange(0, plot_num_samples):
            ax.plot(fit_x_values, zsample_array[ii, :], color='k', alpha=0.5)
        plot_hs_zsample_y_lower = zsample_mean - plot_sigma * zsample_std
        plot_hs_zsample_y_upper = zsample_mean + plot_sigma * zsample_std
        ax.fill_between(fit_x_values, plot_hs_sample_y_lower, plot_hs_sample_y_upper, facecolor='b', edgecolor='None', alpha=0.2)
        ax.set_xlim(0.0, 1.0)
        fig.savefig(save_file)
        plt.close(fig)

        # Derivatives of sampled fit curves (zero noise) against GPR fit derivative distribution
        save_file = plot_save_directory / 'sample_gp_der_no_noise_test.png'
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plot_hs_zfit_dydx_lower = hs_zfit_dydx_values - plot_sigma * hs_zfit_dydx_errors
        plot_hs_zfit_dydx_upper = hs_zfit_dydx_values + plot_sigma * hs_zfit_dydx_errors
        ax.fill_between(fit_x_values, plot_hs_zfit_dydx_lower, plot_hs_zfit_dydx_upper, facecolor='r', edgecolor='None', alpha=0.2)
        for ii in np.arange(0, plot_num_samples):
            ax.plot(dfit_x_values, zderiv_array[ii, :], color='k', alpha=0.5)
        plot_hs_zsample_dydx_lower = zderiv_mean - plot_sigma * zderiv_std
        plot_hs_zsample_dydx_upper = zderiv_mean + plot_sigma * zderiv_std
        ax.fill_between(dfit_x_values, plot_hs_zsample_dydx_lower, plot_hs_zsample_dydx_upper, facecolor='b', edgecolor='None', alpha=0.2)
        ax.set_xlim(0.0, 1.0)
        fig.savefig(save_file)
        plt.close(fig)

        # Sampled fit derivative curves (zero noise) against GPR fit derivative distribution
        save_file = plot_save_directory / 'sample_gp_no_noise_dtest.png'
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.fill_between(fit_x_values, plot_hs_zfit_dydx_lower, plot_hs_zfit_dydx_upper, facecolor='r', edgecolor='None', alpha=0.2)
        for ii in np.arange(0, plot_num_samples):
            ax.plot(fit_x_values, zdsample_array[ii, :], color='k', alpha=0.5)
        plot_hs_zdsample_dydx_lower = zdsample_mean - plot_sigma * zdsample_std
        plot_hs_zdsample_dydx_upper = zdsample_mean + plot_sigma * zdsample_std
        ax.fill_between(fit_x_values, plot_hs_zdsample_dydx_lower, plot_hs_zdsample_dydx_upper, facecolor='b', edgecolor='None', alpha=0.2)
        ax.set_xlim(0.0, 1.0)
        fig.savefig(save_file)
        plt.close(fig)

        # Integrals of sampled fit derivative curves (zero noise) against GPR fit distribution
        save_file = plot_save_directory / 'sample_gp_int_no_noise_dtest.png'
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.fill_between(fit_x_values, plot_hs_zfit_y_lower, plot_hs_zfit_y_upper, facecolor='r', edgecolor='None', alpha=0.2)
        for ii in np.arange(0, plot_num_samples):
            ax.plot(ifit_x_values, zinteg_array[ii, :], color='k', alpha=0.5)
        plot_hs_zdsample_y_lower = zinteg_mean - plot_sigma * zinteg_std
        plot_hs_zdsample_y_upper = zinteg_mean + plot_sigma * zinteg_std
        ax.fill_between(ifit_x_values, plot_hs_zdsample_y_lower, plot_hs_zdsample_y_upper, facecolor='b', edgecolor='None', alpha=0.2)
        ax.set_xlim(0.0, 1.0)
        fig.savefig(save_file)
        plt.close(fig)

        print(f'Results of demonstration plotted and saved in directory, {plot_save_directory.resolve()}.\n')

    else:

        print(f'   Module matplotlib not found. Skipping plotting of demonstration results.\n')

    print(f'Demonstration script successfully completed!\n')


def main():

    run_demo()


if __name__ == '__main__':

    main()
