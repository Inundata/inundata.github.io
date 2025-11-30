---
title: "251201 Random Forest Simulation (1)"
show_date: true
comments: true
layout: single
categories:
  - RF
tags:
  - RF
toc: true
toc_sticky: true
published: true
mathjax: true
use_math: true
---

### Impact of noise and &sigma; (2d)

![2D Impact](/assets/rf_sim/251130_2d_impact_noise_and_sigma.png){: .align-center width="100%"}

---

<h5>여쭤볼 사항</h5>
<ol> 
  <li> &sigma;가 커짐에도 RRMSE의 값이 커지지 않는 이유: 샘플 수가 많아서 &sigma;의 효과를 상쇄하기 때문?</li>
  <li> Random Forest는 기본적으로 $$y_{i}$$의 평균을 내는 것으로 생각할 수 있으며, RandomForest의 예측치 $\hat{f}(x)$는 다음과 같이 쓸 수 있음 .$$\hat{f}(x) = \frac{1}{k} \sum_{i=1}^{k} y_i$$ </li>
</ol>
