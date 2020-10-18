# DataMining
## HW2 ![Python package](https://github.com/Brad-A-M/DataMining/workflows/Python%20package/badge.svg)
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
