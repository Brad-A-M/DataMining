# DataMining

For the synthetic dataset, kmeans.py returns a data frame in the following form when `generateClusters(max_iterations)` is called..

| polygon   | x              | y              |  cluster  |
| --------- | -------------- | -------------- | --------- |
| polygon # | point1 x-coord | point1 y-coord | cluster # |
| polygon # | point2 x-coord | point2 y-coord | cluster # |
| ...       | ...            | ...            | ...       |

For classification datasets, kmeans.py returns a dataframe in the following form.

| Attribute 1 |  Attribute 2 | ... | class   | cluster   |
| ----------- | ------------ | --- | ------- | --------- |
| value 1     | value 1      | ... | class # | cluster # |
| value 2     | value 2      | ... | class # | cluster # |
| ...         | ...          | ... | ...     | ...       |
