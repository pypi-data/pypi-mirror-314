Usage
=====

.. _installation:

Installation
------------

To use this package, first install it using pip:

.. code-block:: console

   (.venv) $ pip install vbvarsel


How to use this package
----------

After installing the package, it can be imported using standard import syntax:

.. code-block:: python3

    import vbvarsel.vbvarsel
    # from vbvarsel import vbvarsel #alternative import option


The main entry point to the package is :func:`~vbvarsel.vbvarsel.main()`.

This function requires at minimum :func:`~vbvarsel.global_parameters.Hyperparameters` and one of either :func:`~vbvarsel.global_parameters.SimulationParameters` or a user-supplied dataset.
The user-supplied dataset should be only numeric values. An optional parameter, :code:`cols_to_ignore` may be passed, which is a list of column name strings that are to be dropped.
If the data contains any non-numeric values, the process will fail.

Hyperparameters
---------------

The hyperparameters are a collection of parameters that control the clustering algorithm. These values can only be set once on initialisation.
These parameters all have default values, but can be modified upon initialisation.
::
    * threshold - The threshold for simulation convergence. (Default 1e-1)
    * k1 - Maximum number of clusters to simulate for. (Default 5)
    * alpha0 - Prior coefficient count, also known as the concentration parameter for
        Dirichelet prior on the mixture proportions. This field is calculated
        from 1/k1. (Default 0.2)
    * a0 - Degrees of freedom for the Gamma prior on the cluster precision, which
        controls the shape of the Gamma distribution. A higher number results
        in a more peaked distribution. (Default 3)
    * beta0 - Shrinkage parameter of the Gaussian conditional prior on the cluster
        mean. This influences the tightness and spread of the cluster, smaller
        shrinkage leads to tighter clusters. (Default 1e-3)
    * d0 - Shape parameter of the Beta distribution on the probability. A value of
        1 results in a uniform distribution. (Default 1)
    * t_max - Maximum starting annealing temperature. Value of 1 has no annealing.
        (Default 1)
    * max_itr - Maximum number of iterations. (Default 25)
    * max_annealed_itr - Maximum number of iterations for annealing, if applicable. (Default 10)
    * max_models - Maximum number of models to run for averaging (Default 10)