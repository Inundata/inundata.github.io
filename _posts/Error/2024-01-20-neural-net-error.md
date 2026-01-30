---
title: "Neural Net Reproduce 에러"
show_date: true
comments: true
layout: single
categories:
  - Machine learning
tags:
  - Python
  - Error
toc: true
toc_sticky: true
toc_label: "목차"
published: false
---

얼마 전 Vanilla Neural Network를 짤 일이 있어서 짜본 다음에, reproducibility를 회사와 집 모두에서 확인하여 마음 놓고 있었다.

그리고 해당 코드를 제3자에게 제공을 한 적이 있었는데, reproduce가 되지 않는 것을 확인하였다.

며칠을 고생한 끝에 해결하긴 했는데, 아직 그 원인은 명확히 밝혀내지 못하고 있으며 혹시나 하여 이를 기록으로 남긴다([stackoverflow에 남긴 자문자답의 글](https://stackoverflow.com/questions/77843222/same-seed-number-package-versions-python-version-but-different-neural-net-re)).

### 파이썬 패키지 버전 및 초기 셋팅

<br>
사용하고 있는 Python 및 관련한 package 버전은 다음과 같다.

> > > python = 3.9.2 <br>
> > > keras=2.12.0<br> tensorflow=2.12.0<br>
> > > pandas=1.5.3<br> numpy=1.23.5<br>
> > > statsmodels=0.13.5 scikit-learn=1.2.2<br>

당시에 짰던 코드는 다음과 같다.
<br>

```python
reset_seeds(42) # For reproducibility
model = Sequential()
model.add(Dense(64, input_shape = (train_X_arr.shape[1], ), activation = 'sigmoid'))
model.add(Dense(16, activation = 'tanh'))
model.add(Dense(1, activation = 'sigmoid'))
model.compile(loss = 'mae')
```

그리고 위의 코드에서 정의한 `reset_seeds`는 다음과 같다.
<br>

```python
def reset_seeds(seed):
    import numpy as np
    import random
    import os
    import tensorflow as tf

    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    random.seed(seed)
    tf.random.set_seed(seed)
```

### 초기 가중치의 합

<br>
위와 같이 한 뒤에, 회사/집의 데스크탑과 노트북의 초기 weight의 sum을 확인한 결과, 둘의 결과는 모두 동일한 것으로 나왔다.

**회사와 집의 초기 가중치의 합 (Before training)**

> > > [-9.959677, 0.0, -5.590966, 0.0, -1.1521256, 0.0]

**노트북의 초기 가중치의 합 (Before training)**

> > > [-9.959677, 0.0, -5.590966, 0.0, -1.1521256, 0.0]

그리고 아래와 같이 간단한 학습을 각각 진행하였다.

```python
hist = model.fit(x = train_X_arr, y = train_y_arr, batch_size = 1, epochs = 1, verbose = 2, shuffle = False)
```

학습을 한 뒤, 초기 가중치의 합을 다시 구해본 결과 아래와 같았다.

**회사와 집의 초기 가중치의 합 (Before training)**

> > > [-159.85245, -5.7658424, 57.23868, 0.47032726, 0.13733912, -0.25829855]

**노트북의 초기 가중치의 합 (Before training)**

> > > [-168.1607, -6.258976, 50.797672, 0.42788112, 0.15801406, -0.26924044]

seed까지 맞췄는데도 가중치의 합이 달라, 며칠을 검색해보고 다양한 에러 사례를 찾아보았지만 정확히 부합하는게 없었다.

그런데 이상하게도 코드를 아래와 같이 바꾸니, reproduce가 되는 것을 확인하였다.

### Reproducibility Error 수정

<br>
**Original One**
```python
reset_seeds(42) 
model = Sequential()
model.add(Dense(64, input_shape = (train_X_arr.shape[1], ), activation = 'sigmoid'))
model.add(Dense(16, activation = 'tanh'))
model.add(Dense(1, activation = 'sigmoid'))
model.compile(loss = 'mae')
```

**New One**

```python
reset_seeds(42)
model = Sequential()
model.add(Dense(64, input_shape = (train_X_arr.shape[1], ), activation = 'sigmoid'))
model.add(Dense(16, activation = 'tanh'))
model.add(Dense(1, activation = 'sigmoid'))
model.compile(optimizer = 'adam', loss = 'mae') # Only this line changed
```

이와 같이 바꾸니 가중치의 합이 동일하게 나오는 것을 확인하였는데, 아직도 이게 어떻게 작동을 하고 있는지 명확히 밝혀내진 못하고 있다.

후일 이것의 원인을 밝혀내는 것을 목표로 하고 있다.

참고로 데스크탑과 노트북 모두 운영체제는 Windows를 사용하고 있으나, 차이점은 CPU가 각각 AMD랑 Intel이라는건데...여기서 차이가 기인하는 것인지는 확실치 않다.
