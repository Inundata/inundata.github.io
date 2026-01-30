---
title: "Model specification"
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

### 1. Model

For the WTI nominal price forecasting, I specify the model below.

$$
y_{t} = \beta_{1}y_{t-1} + \beta_{2}y_{t-2} + \beta_{3}y_{t-3} + \beta_{4}y_{t-4} + f(X_{t-1}) + \epsilon_{t}
$$

where $$y_{t} = WTI_{t} / CPI_{t-1}$$

I assumed that I could not get the recent CPI at the point of forecasting.

The reason why I used four lags for forecasting, there was an evidence that the residuals are serially correlated.

### 2. XGBoost parameter

I've changed many parameters to find the most appropriate parameter for the oil price forecasting so far.

Up to now, I decided the parameter as follows.

. `n_estimators = 20` <br>
. `subsample` = $$\sqrt{n}$$ <br>
. `num_parallel_tree = 170` <br>
. `tree_method = exact` <br>
. `colsample_bynode = 1` <br>
. `random_state = 42` <br>

The above model specification could be changed in the future.

### Note

1. Changed the code(Change to use $$CPI_{t-1}$$ from $$CPI_{t}$$) <br/>
   → For the one-step ahead forecast, `num_parallel_tree = 100` was better than `170` when other parameters were not changed.
