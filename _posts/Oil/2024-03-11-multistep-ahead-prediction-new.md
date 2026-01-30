---
title:  "Multi-step ahead prediction[New]"
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

I've performed a multi-step ahead prediction, due to changing some code, and updated the result.

## 1. Forecasting setting

For the multi-step ahead prediction, I used the model below,

$$y_{t+1} = \beta_{1}y_{t} + \beta_{2}y_{t-1} + \beta_{3}y_{t-2} + \beta_{4}y_{t-3} + f(X_{t}) + \epsilon_{t+1}$$
$$y_{t+2} = \beta_{1}y_{t+1} + \beta_{2}y_{t} + \beta_{3}y_{t-1} + \beta_{4}y_{t-2} + f(X_{t}) + \epsilon_{t+2}$$ 
$$y_{t+3} = \beta_{1}y_{t+2} + \beta_{2}y_{t+1} + \beta_{3}y_{t} + \beta_{4}y_{t-1} + f(X_{t}) + \epsilon_{t+3}$$ 

<br/>

for the forecasting,

$$\hat{y}_{t+1} = \hat{\beta}_{1}y_{t} + \hat{\beta_{2}}y_{t-1} + \hat{\beta_{3}}y_{t-2} + \hat{\beta_{4}}y_{t-3} + \hat{f}(X_{t})$$
$$\hat{y}_{t+2} = \hat{\beta}_{1}\hat{y}_{t+1|t} + \hat{\beta}_{2}y_{t} + \hat{\beta}_{3}y_{t-1} + \hat{\beta}_{4}y_{t-2} + \hat{f}(X_{t})$$
$$\hat{y}_{t+3} = \hat{\beta}_{1}\hat{y}_{t+2|t} + \hat{\beta}_{2}\hat{y}_{t+1|t} + \hat{\beta}_{3}y_{t} + \hat{\beta}_{4}y_{t-1} + \hat{f}(X_{t})$$


- Training period: 2013-06 ~ 2023-08
- Forecasting period: 2013-07 ~ 2023-11
- Total number of periods: 120 periods(except for the COVID-19 period(2020-3 ~ 2020-5))
- Three-step ahead forecast
- Expanding window

## 2. Parameter settings
- `max_depth` = 6
- `n_estimators(=number of boosting)` = 20
- `no column subsampling`
- `row subsampling(bootstrap in custom_RF)` = $$\sqrt{n}$$
- `num_parallel_tree` = 170

## 3. Forecasting Performance

| forecasting step | RMSE | (RMSE of XGBoost) / (RMSE of RW) |
| :-: | -: | -: |
|    1   | .0829 |    93.5%  |
|    2     | .1305 |    92.8% |
|    3     | .1625 |   90.8%  |

<br/>

The accumulated RMSE for each forecasting steps are below.

![multi-step-ahead-forecast-xgboost](/assets/oil_result_images/three-step-ahead-forecast.png){: .align-center}

