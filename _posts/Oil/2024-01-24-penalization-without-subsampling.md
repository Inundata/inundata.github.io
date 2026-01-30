---
title:  "Subsampling? Penalization?"
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

From the [previous post](https://inundata.github.io/oil%20price%20forecasting/about-penalization/), I checked that the penalization parameters were not effective when I set the XGBoost `with subsampling`.

In this post, I changed the XGBoost `with subsampling` to `without subsampling`.

Through this work, I expect that I can understand the `subsampling` parameter more in terms of penalization.

To remind you of your memories, I use these parameters for the XGBoost.

| Name of parameters | Details | Values |
| :-: | :-: | :-: |
|    `n_estimators` | total number of iterations |    20    |
| `num_parallel_tree` | total number of trees in each iteration |  170 |
|    `subsample`     | the ratio of subsampling;<br/> the subsampled data is feeded to each tree |   $$\sqrt{n}^{-\frac{1}{2}}$$ to 1   |
|    `tree_method`     | The method of finding the splitting point;<br/>`exact` means looking all of the values for each feature |   `exact`    |
|    `colsample_bynode`     | Subsampling ratio of the columns for each node(splitting point) |    1    |
|    `random_state`     | For the reproducibility |    42   |


Also, I perform the *one-step ahead prediction* and the target is *the monthly price of WTI nominal*.

**To be brief, as I expected, the penalization parameters were useful if we didn't perform the subsampling. *Thus, in terms of regularization, we can use `subsampling` or `penalization parameters`*.**

I attached the RMSE graph in each case below.<br/>
(For each point, it is the accumulated RMSE up to that date.)

## 1. Lambda
<br>
**[`lambda` ranges from 1 to 20; alpha = 0]**

**1. XGBoost without subsampling**
{% include oil_plotly/RMSE_of_BTRF_lambda_change_NoSubSampling.html %}

<br>

## 2. Alpha
<br>
**[`alpha` ranges from 0 to 19; lambda = 1]**

**1. XGBoost without subsampling**
{% include oil_plotly/RMSE_of_BTRF_alpha_change_NoSubSampling.html %}

<br/>

The below plot is the mean of RMSE for the test period(recent 5 years; except the COVID-19 period).<br/>
For the label `with subsampling`, it means that I did the subsampling in $$\sqrt{n}$$ with `alpha = 0` and `lambda = 1`.

<span>
![image](/assets/oil_result_images/rmse_without_subsampling_5years.png){: .align-center}
</span>
