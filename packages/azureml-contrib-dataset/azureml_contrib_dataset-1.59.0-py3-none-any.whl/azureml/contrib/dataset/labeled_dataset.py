# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains functions for labeled datasets that are still under development.
(DEPRECATED) Use the TabularDataset in azureml-core instead.

Labeled datasets are a type of TabularDataset that are created from data labeling projects.
For more information about data labeling projects, please refer to
[Create a data labeling project and export
labels](https://docs.microsoft.com/azure/machine-learning/how-to-create-labeling-projects).

Unlike a regular TabularDataset, a labeled dataset has the ability to be mounted and downloaded.
You can also convert a labeled dataset to a pandas DataFrame using the `to_pandas_dataframe` method or to a
torchvision dataset using the `to_torchvision()` method.

"""

from azureml.data._loggerfactory import track, _LoggerFactory, trace_error


_logger = _LoggerFactory.get_logger(__name__)

trace_error(_logger, "use of deprecated azureml-contrib-dataset, failing import")
raise ImportError("azureml-contrib-dataset is deprecated, please use the TabularDataset in azureml-core instead.")
