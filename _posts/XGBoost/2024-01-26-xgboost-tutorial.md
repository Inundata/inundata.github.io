---
title:  "XGBoost Tutorial"
show_date: true
comments: true
layout: single
categories:
  - Machine learning
tags:
  - Python
  - XGBoost
toc: true
toc_sticky: true
published: false
---

In this post, we will take a moment what is XGBoost and its parameters in Python.
And finally, I'll briefly explain what is our goal to do with the XGBoost.

## 1. Concept of XGBoost

The full idea of XGBoost can be found [here](https://xgboost.readthedocs.io/en/stable/tutorials/model.html), and this is the [paper of the XGboost](https://scholar.google.com/scholar_url?url=https://dl.acm.org/doi/pdf/10.1145/2939672.2939785&hl=ko&sa=X&ei=0PSzZdbLKr6Py9YPupq-2As&scisig=AFWwaeZXiFTAoiBjcjZUzHKYyVQx&oi=scholarr).

The key concept of XGBoost is **"fitting the residual repeatedly".**

The summary of the XGBoost is presented as below.

<h2 align="center">[The sketch of XGBoost]</h2>

![xgboost-intro](/assets/xgboost/xgboost-intro.jpg){: .align-center}

From the above picture, the input of the *t-th* boosting is the *(t-1)-th* boosting's residual.

By getting this as an input, in the *t-th* boosting, it formulates one tree(or forest), and the result is denoted as $$f_{t}$$.

Finally, the *T-th* boosting prediction value is the sum of all of these trees(or forests) and we can denote as 
<br/>
<div align="center">$$\hat{y_{T}} = \sum_{t=1}^Tf_{t}$$</div>
<div align="center">T = total number of boostings</div>
<br/>
For *t-th* boosting, the XGBoost is minimizing the following objective function.
<br/>
<div align="center">$$L^{t}=\sum_{i=1}^n[l(y_{i}, \hat{y_{i}}^{t-1} + f_{t}(x_{i}))] + \Omega(f_{t})$$</div>

To quickly optimize the objective function, it uses the Taylor Series Approximation.
<br/>
<div align="center">$$L^{t}\approx\sum_{i=1}^n[l(y_{i}, \hat{y_{i}}^{t-1}) + g_{i}f_{t}(x_{i}) + \frac{1}{2}h_{i}f_{t}^2(x_{i})] + \Omega(f_{t})$$</div>
<div align="center">$$g_{i} = \frac{\partial{l(y_{i}, \hat{y_{i}}^{t-1})}}{\partial{\hat{y_{i}}^{t-1}}}$$</div>
<div align="center">$$h_{i} = \frac{\partial^2{l(y_{i}, \hat{y_{i}}^{t-1})}}{\partial{(\hat{y_{i}}^{t-1})}^2}$$</div>

$$n$$ is the *total number of observations* and $$\Omega(f_{t})$$ is *the penalization term*.<br/>
For more details, refer to the above XGBoost documentation or the paper.

## 2. Parameters of the XGBoost

In this part, I will explain the XGBoost parameters that you must know in more detail. <br/>
The official Python API reference documentation of the XGBoost is linked below.

- Documentation of the XGBoost: [Click here](https://xgboost.readthedocs.io/en/stable/python/python_api.html)
- Explanation of the default values of XGBoost: [Click here](https://xgboost.readthedocs.io/en/stable/parameter.html)
<br/><br/>

*Note)*
1. XGBoost can do both the *classification* and *regression*, and the parameters are almost the same. Thus, I will explain by referring to the *XGBRegressor*. <br/>
2. Some parameters' default values are not written in the above documentation.

<h3>1. n_estimators</h3>
- This refers to the total number of times to fit the residuals iterately.
- Default value = `100`

<h3>2. max_depth</h3>
- The maximum tree depth for each tree in each boosting.
- Default value = `6`

<h3>3. tree_method</h3>
- The method of finding the splitting point for each feature. There are 4 values for this parameter; `auto`, `exact`, `approx`, and `hist`. <br/>
ⅰ. `auto` : Same as the `hist` method. <br/>
ⅱ. `exact` : Exact greedy algorithm. Splitting all of the candidates. <br/>
ⅲ. `approx` : Create the buckets for each feature and find the split. <br/>
ⅳ. `hist` : same as `approx` but much more faster. <br/>
- Default value = `auto`

- difference between `exact` and `hist`. <br/>
Let say there is a feature with those values;
$$x = [10, 14, 25, 3, 9, 16, 37, 1, 22, 17]$$.
<br/>
In tree algorithm, it sorts the value into ascending order.<br/>
$$x = [1, 3, 9, 10, 14, 16, 17, 22, 25, 37]$$.<br/><br/>
ⅰ. `exact`<br/>
It looks for all values one by one to find the splitting point.<br/>
![exact](/assets/xgboost/exact.png){: .align-center}<br/>
ⅱ. `approx` <br/>
Create the buckets that match with the parameter `max_bin` and put each value into that bucket first. Then, find the splitting points by using the buckets.<br/>
![approx](/assets/xgboost/approx.png){: .align-center}
<br/>
- difference between `approx` and `hist` <br/>
From the [lead maintainer of XGBoost](https://github.com/dmlc/xgboost/issues/1950), `approx` method generates a new set of bins for each boosting, whereas the `hist` method re-uses the bins over multiple boostings.

<h3>4. max_bin</h3>
- For the `hist` or `approx` tree method, it refers to the maximum number of bins per feature.
- It can not be used for the `exact` tree method.
- Default value = `256`

<h3>5. max_leaves</h3>
- The maximum number of leaves; `0` indicates no limit.
- It can not be used for the `exact` tree method.
- Default value = `0`

<h3>6. learning_rate</h3>
- It has the range 0 from 1 and is multiplied to the $$f_{t}$$.<br/>
<div align="center">$$\hat{y_{t}} = \hat{y_{t-1}} + (lr) * f_{t}$$</div>
- Default value = `0.3`

<h3>7. subsample</h3>
- The ratio of row subsampling. The subsampled data is fed to each tree.
- In XGBoost, it performs the [`sampling without replacement`](https://xgboost.readthedocs.io/en/stable/tutorials/rf.html).
- Each tree will have different subsampled data.
- Default value = `1`
- column subsampling is also possible. For details, check the documentation.

<h3>8. num_parallel_tree</h3>
- Total number of trees in each boosting. If this parameter is not specified, each boosting will use only one tree.
- Default value = `1`

<h3>9. reg_alpha</h3>
- The $$L1$$ penalization parameter.
- Default value = `0`

<h3>10. reg_lambda</h3>
- The $$L2$$ penalization parameter.
- Default value = `1`

<h3>Summary</h3>
- The diagram of the above is as follows.
![parameters-summary](/assets/xgboost/parameters-summary.jpg){: .align-center}

## 3. Further Objective

Our further objective is focused on modifying the `max_bin` and the `exact`.<br/>
Currently, `max_bin` and `exact` can’t be used at the same time. In addition, there are some problems with `max_bin` and `exact` parameters.

<h3>1. max_bin</h3>

- If we use this parameter with the `approx`, it does not find the **exact** point to be split.
- For example, let's create the `y` and `x` as follows.

```python
import numpy as np
import xgboost

y = np.r_[np.ones(20), np.ones(80) * 100].reshape(-1, 1)  # Total number of elements with value 1: 20
                                                          # Total number of elements with value 100: 80
x = np.arange(1, 101).reshape(-1, 1) # ranges from 1 to 100 and increases by 1
```

- Then the plotted `y` and `x` will be looked like below.<br/><br/>
![y-and-x](/assets/xgboost/y-and-x.png){: .align-center}

- If someone asks you to find the best splitting point from this picture, you will easily choose the point `x=20`(the red line).<br/><br/>
![y-and-x](/assets/xgboost/y-and-x-split.png){: .align-center}

- However, if we do it with the `xgboost` package by giving the `max_bin` parameter to `2`, it fails.

```python
tree_method = 'approx'
max_bin = 2 # Impose to find only one point
n_estimators = 10
random_state = 42

mdl = xgboost.XGBRegressor(tree_method = tree_method
                        , max_bin = max_bin
                        , n_estimators = n_estimators
                        , random_state = random_state)

mdl.fit(X = x, y = y)
```

- The result from XGBoost is as follows.<br/><br/>
![xgboost-wrong-result](/assets/xgboost/xgboost-wrong-result.png){: .align-center}<br/>
It split at the point where `x < 48`. This result is **not what we expected.**

<h3>2. exact</h3>

- Finding the exact point can be solved by using the `exact` method.
- Applying the `exact` method to the previous example is as follows.

```python
tree_method = 'exact'
# max_bin = 2 # we cannot us this parameter when tree_method is `exact`
n_estimators = 10
random_state = 42

mdl = xgboost.XGBRegressor(tree_method = tree_method
                        # , max_bin = max_bin
                        , n_estimators = n_estimators
                        , random_state = random_state)

mdl.fit(X = x, y = y)
```
![xgboost-right-result](/assets/xgboost/xgboost-right-result.png){: .align-center}<br/>
It split at the point where `x < 20.5`. **This result is what we expected.**

However, we cannot use the `exact` for other problems when we want to get one or two points to be split due to it splitting **all of the points**.

<h3>3. Objective</h3>
- Our objective is to modify the XGBoost code to use `exact` by giving restriction of finding the splitting point.
- By modifying this, we can restrict the splitting point to only one or two even if other points can lower the loss.
- However, the source code is provided in `C/C++`.

