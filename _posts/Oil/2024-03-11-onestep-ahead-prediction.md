---
title:  "one-step ahead prediction[New]"
show_date: true
comments: true
layout: single
categories:
  - Oil price forecasting
tags:
  - Python
  - XGBoost
toc: true
toc_sticky: true
published: false
---

I've performed a one-step ahead prediction recently again. I made a mistake in setting the `n_estimator` value as 10.

## 1. Parameter settings
- `max_depth` = 6
- `n_estimator(=number of boosting)` = 20
- `no column subsampling`
- `row subsampling(bootstrap in custom_RF)` = $$\sqrt{n}$$
- `num_parallel_tree` = 170

## 2. Forecasting Performance
- Test periods: 2013-09 ~ 2023-11 (2020-03 ~ 2020-05 were excluded.)
- RW RMSE = .0889
- XGBoost; (`n_estimator` = 20 & `num_parallel_tree` = 1 & `subsample` = 1) RMSE = .1302

- Below is the table when `n_estimator` = 20  & `subsample` = $$\sqrt{n}^{-\frac{1}{2}}$$ when `num_parallel_tree` varies,

| RW RMSE | X XGBoost; <br/> `n_estimator=20`  RMSE | Ratio | 
| :-: | :-: | :-: | 
|    100   | .0830 |    93.36%  |
|    120     | .0828 |    92.14% |
|    140     | .0826 |   92.91%  |
|    160     | .0827 |   93.03%  |
|    170     | .0828 |   93.14%  |
|    180     | .0827 |   93.03%  |
|    200     | .0831 |   93.48%  |
|    220     | .0831 |   93.48%  |
|    240     | .0829 |   93.25%  |
|    260     | .0829 |   93.25%  |
|    280     | .0829 |   93.25%  |
|    300     | .0831 |   93.48%  |

- Below plot is the accuumulated result for each `num_parallel_tree`
{% include oil_plotly/RMSE_of_BTRF_num_parallel_tree_change.html %}
