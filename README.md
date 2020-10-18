# DataMining
## HW2 ![Python package](https://github.com/Brad-A-M/DataMining/workflows/Python%20package/badge.svg)

Required packages for this application can be installed with the pip. Run `pip install -r requirements.txt` to install.

Note: if you have `pip` configured as your python 2 package manager, you may have to use `pip3` instead as this application requires python 3.

For the synthetic datasets, db scan and kmeans return a dataframe in the form.

| polygon   | x              | y              |  cluster  |
| --------- | -------------- | -------------- | --------- |
| polygon # | point1 x-coord | point1 y-coord | cluster # |
| polygon # | point2 x-coord | point2 y-coord | cluster # |
| ...       | ...            | ...            | ...       |

For classification datasets, db scan and kmeans return a dataframe in the following form.

| Attribute 1 |  Attribute 2 | ... | class   | cluster   |
| ----------- | ------------ | --- | ------- | --------- |
| value 1     | value 1      | ... | class # | cluster # |
| value 2     | value 2      | ... | class # | cluster # |
| ...         | ...          | ... | ...     | ...       |

Algorithm assessment

| Algorithm | Assessment Metric     | Dataset                                      | Score  |
| k-means   | Silhoutte Coefficient | Synthetic, 5 polys, 5 pts each, 10 noise pts | 0.3588 |
| DB Scan   | Silhoutte Coefficient | Synthetic, 5 polys, 5 pts each, 10 noise pts | 0.3915 |
| k-means   | Purity                | Segmentation, UCI Machine Learning Repo      | 0.6476 |
| DB Scan   | Purity                | Segmentation, UCI Machine Learning Repo      | 0.9904 |