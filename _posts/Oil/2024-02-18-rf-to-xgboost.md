---
title:  "Random Forest with Boosting"
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

In this post, I do the `Random Forest with boosting`(hereinafter `custom_RF`) by modifying the package of `sklearn.ensemble.RandomForestRegressor`.

The purpose is to verify that `XGBoost` does some other thing inside of their package except of **boosting**.

If the performances are not different between `XGBoost` and `custom_RF`, then we can assume that `XGBoost` is not different from the `Random Forest with boosting`.

## 1. Forecasting settings

- Training period: 2013-08 ~ 2023-10
- Forecasting period: 2013-09 ~ 2023-11
- Total number of periods: 120 periods(except for the COVID-19 period(2020-3 ~ 2020-5))
- One-step ahead forecast
- Expanding window

## 2. Parameter settings
- `max_depth` = 6
- `n_estimators(=number of boosting)` = 20
- `no column subsampling`
- `row column subsampling(bootstrap in custom_RF)` = $$\sqrt{n}$$
- For parameters not mentioned here, `XGBoost` and `custom_RF` were set equally.

## 3. Forecasting performance

- Used the `RMSE` for measuring the performance.
- Varied the `num_parallel_tree(=number of trees for each boosting)` and measured the performance.
- Random walk RMSE = `0.0889`

<h4> a. XGBoost </h4>

| num_parallel_tree | RMSE | (RMSE of XGBoost) / (RMSE of RW) |
| :-: | -: | -: |
|    100   | .0828 |    93.1%  |
|    120     | .0835 |    93.9% |
|    140     | .0833 |   93.7%  |
|    160     | .0833 |    93.7%  |
|    170     | .0833 |    93.7% |
|    180     | .0834 |    93.8% |
|    200     | .0835 |    93.9%  |
|    220     | .0835 |    93.9%  |
|    240     | .0836 |    94.0%  |
|    260     | .0836 |    94.0%  |
|    280     | .0835 |    93.9%  |
|    300     | .0837 |    94.2%  |

- The performance was the best when `num_parallel_tree = 100`

<h4> b. custom_RF </h4>

| num_parallel_tree | RMSE | (RMSE of custom_RF) / (RMSE of RW) |
| :-: | -: | -: | 
|    100     | .0854 |    96.1% |
|    120     | .0852 |    95.8% |
|    140     | .0842 |    94.7% |
|    160     | .0821 |    92.4% |
|    170     | .0817 |    91.9% |
|    180     | .0816 |    91.8% |
|    200     | .0824 |    92.7% |
|    220     | .0820 |    92.2% |
|    240     | .0831 |    93.5% |
|    260     | .0818 |    92.0% |
|    280     | .0825 |    92.8% |
|    300     | .0831 |    93.5% |

- The performance was the best when `num_parallel_tree = 180`.
- With `num_parallel_tree = 180`, the performance was better than `XGBoost`.
- The ratios fluctuated more than the `XGBoost`.

## 4. Forecasting performance plot(accumulated)

<h4> a. XGBoost </h4>

{% include oil_plotly/xgboost-rmse-to-wti-nominal.html %}{:, .align-center}

<h4> b. custom_RF </h4>

{% include oil_plotly/rf-xgboost-rmse-to-wti-nominal.html %}{:, .align-center}
