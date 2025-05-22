---
title: "One step ahead prediction"
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

Using the [model](https://inundata.github.io/oil%20price%20forecasting/model-specification/) that I sepcified and using other models, I performed the one-step ahead prediction.

The result as follows.

| Number of lags | RMSE to WTI_nominal | Improvement by adding one more lags |          Duartion |
| :------------: | ------------------: | ----------------------------------: | ----------------: |
|       1        |               .0851 |                                   - | 2013/08 ~ 2023/10 |
|       2        |               .0835 |                              -.0017 | 2013/08 ~ 2023/10 |
|       3        |               .0832 |                              -.0003 | 2013/08 ~ 2023/10 |
|       4        |               .0820 |                              -.0012 | 2013/08 ~ 2023/10 |
|       5        |               .0829 |                              +.0009 | 2013/08 ~ 2023/10 |
|       6        |               .0842 |                              +.0018 | 2013/08 ~ 2023/10 |

Note) The RMSE of Random walk was `.0884` for the same period.
