lingress
========

The Lingress project is an initiative aimed at developing a streamlined
pipeline for the analysis of Nuclear Magnetic Resonance (NMR) datasets,
utilizing a univariate linear regression model. This package encompasses
the execution of linear regression analysis via the Ordinary Least
Squares (OLS) method and provides visual interpretations of the
resultant data. Notably, it includes the p-values of all NMR peaks in
its analytical scope.

Functionally, this program strives to fit a model of metabolic profiles
through the application of linear regression. Its design and
capabilities present a robust tool for in-depth and nuanced data
analysis in the realm of metabolic studies.

**How to install**
------------------

.. code:: bash

   pip install lingress

**UI Peak Picking**
-------------------

.. code:: python

   #Example data
   import numpy as np
   from lingress import pickie_peak
   import pandas as pd


   df = pd.read_csv("https://raw.githubusercontent.com/aeiwz/example_data/main/dataset/Example_NMR_data.csv")
   spectra = df.iloc[:,1:]
   ppm = spectra.columns.astype(float).to_list()


   #defind plot data and run UI
   pickie_peak(spectra=spectra, ppm=ppm).run_ui()

.. figure:: ./src/img/UI_peak_picking.png
   :alt: img1

   img1

**Linear Regression model**
---------------------------

.. code:: python

   import pandas as pd
   from lingress import lin_regression


   df = pd.read_csv("https://raw.githubusercontent.com/aeiwz/example_data/main/dataset/Example_NMR_data.csv")
   X = df.iloc[:,1:]
   ppm = spectra.columns.astype(float).to_list()
   y = df['Group']


   mod = lin_regression(x=X, target=y, label=y, features_name=ppm, adj_method='fdr_bh')
   mod.create_dataset()
   mod.fit_model()

.. code:: python

   mod.spec_uniplot()

.. figure:: ./src/img/spec_uniplot.png
   :alt: spec uniplot

   spec uniplot

.. code:: python

   mod.volcano_plot()

.. figure:: ./src/img/volcano.png
   :alt: volcano

   volcano

.. code:: python

   mod.resampling(n_jobs=-1, n_boots=100, adj_method='fdr_bh')

::

   [Parallel(n_jobs=-1)]: Using backend LokyBackend with 8 concurrent workers.
   [Parallel(n_jobs=-1)]: Done   6 tasks      | elapsed:    3.7s
   [Parallel(n_jobs=-1)]: Done  60 tasks      | elapsed:    6.7s
   [Parallel(n_jobs=-1)]: Done 150 tasks      | elapsed:   11.2s
   [Parallel(n_jobs=-1)]: Done 276 tasks      | elapsed:   17.8s
   ...
   [Parallel(n_jobs=-1)]: Done 6486 tasks      | elapsed:  5.6min
   [Parallel(n_jobs=-1)]: Done 7188 tasks      | elapsed:  6.1min
   [Parallel(n_jobs=-1)]: Done 7211 out of 7211 | elapsed:  6.1min finished

