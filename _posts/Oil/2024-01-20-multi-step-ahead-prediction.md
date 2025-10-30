---
title: "Multi step ahead prediction"
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

Using the [model](https://inundata.github.io/oil%20price%20forecasting/model-specification/) that I sepcified, I performed the multi-step ahead prediction.

The result as follows.

**[Two step ahead prediction]**

| forecast step |   BTRF |     RW | BTRF/RW |
| :-----------: | -----: | -----: | ------: |
|       1       | 0.0825 | 0.0887 |  0.9302 |
|       2       | 0.1288 | 0.1407 |  0.9158 |

**[Three step ahead prediction]**

| forecast step |   BTRF |     RW | BTRF/RW |
| :-----------: | -----: | -----: | ------: |
|       1       | 0.0823 | 0.0883 |  0.9325 |
|       2       | 0.1296 | 0.1409 |  0.9202 |
|       3       | 0.1621 | 0.1791 |  0.9052 |
