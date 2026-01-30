---
title:  "Neural Network with PCA"
show_date: true
comments: true
layout: single
categories:
  - Oil price forecasting
tags:
  - Python
  - Neural Network
toc: true
toc_sticky: true
published: false
---

In this post, I will show some results of forecasting WTI nominal price using the neural network.
The difference from the before is that I use the **PCA** before pushing input data into the input layer.

## 1. Assumptions toward this work
I made two assumptions for these works, <br/>
<h4> a. Data Transformation harms to find the common variation in the X. </h4>
- As the data transformation was conducted, most of the data was converted into the quasi white noise. Therefore, I suppose that data transformation is not desirable in this problem.
- To verify this, I ran two different neural network models. One model uses factors as input data that is extracted from the *transformed data*, and the other one uses input data that is extracted from the *untransformed data*. 
- For the untransformed data, Logs were taken only for variables by referring to FRED-MD's paper.

<h4> b. Using the input that have strong signals will return the stable predictions. </h4>
- From my experience, the neural network model prediction values were quite varied even if I used enough epochs.
- So, I suppose that reducing the dimension of the input data and using the variables that have strong signals will give stable predictions.

## 2. Reason of using PCA to the input data($$X$$)
Due to the weak relationship between the $$y$$ and $$X$$ in forecasting oil price, the neural network model failed to learn the relationship between $$y$$ and $$x$$. <br/>
The neural network was successful in LLM(Large Language Model) where the signal is solid between the $$y$$ and $$X$$. However, as you know, the oil price has a large variance in its nature and, finding the important $$X$$ is hard. <br/>

Thus, I supposed that finding the input data which have the strong signal is the most important thing before training the model, so I accompanied the idea of PCA into this problem.

## 3. Explained Variance check
- The red horizontal line is .95 and the blue horizontal line is .6.

<h4> a. Transformed data </h4>
![transformed-data-EV-path](/assets/neural.network/EVPath_DataTransformation_O.png){: .align-center}

- For the 95% explained variance, almost 60 factors are required.
- For the 60% explained variance, 14 factors are required.

<h4> b. Transformed data </h4>
![untransformed-data-EV-path](/assets/neural.network/EVPath_DataTransformation_X.png){: .align-center}

- For the 95% explained variance, almost 15 factors are required.
- For the 60% explained variance, 2 factors are required.

## 4. The model structure
- For the comparsion, I used three models: <br/>
**a. Neural network model; using factors from transformed data** <br/>
**b. Neural network model; using factors from untransformed data**<br/>
**c. Neural network model; using all of the input data**<br/>

- The parially linear is accompained to all of those models, and the benchmark model is random walk.
- I used the batch size: 128, and the order of activation function is ReLU-ReLU-tanh for the hidden layers.

- The model details are below; <br/>
**a. Neural network model; using factors from transformed data**<br/>
![neural-network-model-using-factors-from-transformed-data](/assets/neural.network/neural-network-model-using-factors-from-transformed-data.png){: .align-center}

**b. Neural network model; using factors from untransformed data**<br/>
![neural-network-model-using-factors-from-untransformed-data](/assets/neural.network/neural-network-model-using-factors-from-untransformed-data.png){: .align-center}

**c. Neural network model; using all of the input data**<br/>
![neural-network-model-using-all-input-data](/assets/neural.network/neural-network-model-using-all-input-data.png){: .align-center}


## 5. Prediction value path and training loss path
- I focused only on the prediction value path and the training loss path. I am not going to talk about the performance of these models.
- As my assumption, using the input data has strong signals returned the stable prediction value (look at the blue and orange color line). <br/>
The interesting point is that the prediction value from the model C(the green line) have a sudden jump. This happens when the training loss sparks suddenly. <br/>In my conjecture, this phenomenon happens when the model gets out from a local minimum and gets back into the other local minimum.
- The one more interesting point is that, after a certain numbers of epoch is passed most of the prediction value from the model A and model C converges to the random walk value. <br/>

<h4> **2013-9 ~ 2013-12** </h4>
![prediction-values-path-full1](/assets/neural.network/prediction-values-path-full1.png){: .align-center}

<h4> **2014-1 ~ 2014-4** </h4>
![prediction-values-path-full2](/assets/neural.network/prediction-values-path-full2.png){: .align-center}

<h4> **2014 -5 ~ 2014-8** </h4>
![prediction-values-path-full3](/assets/neural.network/prediction-values-path-full3.png){: .align-center}

- Picture without neural network

<h4> **2013-9 ~ 2013-12** </h4>
![prediction-values-path-full1-no-neural-network](/assets/neural.network/prediction-values-path-full1-no-neural-network.png){: .align-center}

<h4> **2014-1 ~ 2014-4** </h4>
![prediction-values-path-full2-no-neural-network](/assets/neural.network/prediction-values-path-full2-no-neural-network.png){: .align-center}

<h4> **2014 -5 ~ 2014-8** </h4>
![prediction-values-path-full3-no-neural-network](/assets/neural.network/prediction-values-path-full3-no-neural-network.png){: .align-center}


## 6. Further Objective

- In my guess, we have to do a non-linear transformation to the linear outputs. In my conjecture, we can avoid that the prediction value converges to the random walk values.
- Finding the appropriate numbers of factors are needed, and for extracting factors we have to decide which one is more appropriate between using the transformed data or untransformed data.