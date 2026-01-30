---
title: "Machine learning: sklearn의 사용법, 그리고 이외 기타 유용한 것들"
show_date: true
comments: true
layout: single
categories:
  - Machine learning
tags:
  - Python
  - Sklearn
toc: true
toc_sticky: true
published: false
---

머신러닝을 이용하다보면, Scaling, 모델 예측 성능 평가 등 다양한 것을 하여야 한다. <br/>
그동안 Sklearn의 pipeline에 대한 글이 검색되는 경우 무엇인지 잘몰랐었는데, 공부를 해보니 이를 적극적으로 활용해봐야겠다는 생각이 든다. <br/>

따라서 이와 관련한 내용을 간단하게 정리하며, 나중에 필요할 때 해당 method를 찾아서 사용해보는 식으로 하면 될 것 같다.

### 1. np.number

- `sklearn`을 이용해서 scaling을 진행할 때, 숫자인 데이터에 대해서만 scaling을 진행할 수 있다.
- 숫자 데이터를 포함하고 있는 열을 쉽게 선택할 수 있는 방법을 새로이 알게되었는데, 이는 `np.number`이다.
- 사용법

```python
# housing : pd.DataFrame
# 숫자 datatype만 포함하는 열을 선택한다고 하면,
housing_num = housing.select_dtypes(include = [np.number])
```

### 2. from sklearn.utils.validation import check_array, check_is_fitted

- 나중에 사용자 지정 class를 만들때 알아두면 좋은 method인 것으로 보임.
- `check_array` : 해당 data type이 array인지 아닌지 체크를 함.
- `check_is_fitted` : `*.fit()` 메소드가 적용이 되었는지 아닌지를 확인할 수 있는 방법.
- 참고로, `fit` 메소드를 사용자가 직접 정의할 때, `y`를 사용하지 않더라도 지정해줘야함. 자세한 내용은 아래 사용법을 통해서 확인하기.
- 사용법

```python
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_array, check_is_fitted

class StandardScalerClone(BaseEstimator, TransformerMixin):
    def __init__(self, with_mean=True):  # *args나 **kwargs를 사용하지 않습니다!
        self.with_mean = with_mean

    def fit(self, X, y=None):  # 사용하지 않더라도 y를 넣어 주어야 합니다
        X = check_array(X)  # X가 부동소수점 배열인지 확인합니다
        self.mean_ = X.mean(axis=0)
        self.scale_ = X.std(axis=0)
        self.n_features_in_ = X.shape[1]  # 모든 추정기는 fit()에서 이를 저장합니다.
        return self  # 항상 self를 반환합니다!

    def transform(self, X):
        check_is_fitted(self)  # (훈련으로) 학습된 속성이 있는지 확인합니다
        X = check_array(X)
        assert self.n_features_in_ == X.shape[1]
        if self.with_mean:
            X = X - self.mean_
        return X / self.scale_
```

### 3. from sklearn.preprocessing import OneHotEncoder의 \*.get_feature_names_out() attribute

- dummy variable을 생성하는 OneHotEncoder를 사용하면 array로 바꿔버리기 때문에, 다시 dataframe으로 지정해주고 column name을 지정해주어야하는 불편한 점이 존재했었음.
- 근데 이 attribute를 사용하면 쉽게 지정할 수 있음.
- 사용법

```python
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

housing_cat = pd.DataFrame({"ocean_proximity" : ['<1H OCEAN', 'INLAND', 'ISLAND', 'NEAR BAY', 'NEAR OCEAN']})

cat_encoder = OneHotEncoder(sparse_output = False)
housing_cat_1hot = cat_encoder.fit_transform(housing_cat)
print(housing_cat_1hot) # spare_output = False로 지정한 경우, array로 나옴
# [[1. 0. 0. 0. 0.]
# [0. 1. 0. 0. 0.]
# [0. 0. 1. 0. 0.]
# [0. 0. 0. 1. 0.]
# [0. 0. 0. 0. 1.]]
print(cat_encoder.feature_names_in_) # 어떤 feature가 들어가서 fit이 되었는지 확인 할 수 있음.
# ['ocean_proximity']
print(cat_encoder.get_feature_names_out())
# ['ocean_proximity_<1H OCEAN' 'ocean_proximity_INLAND'
# 'ocean_proximity_ISLAND' 'ocean_proximity_NEAR BAY'
# 'ocean_proximity_NEAR OCEAN'] → (기존 column_name)_(value)의 형식으로 column이 만들어짐.
```

### 4. from sklearn.preprocessing import OrdinalEncoder

- 범주형 데이터(ex: "나쁨", "보통", "좋음")가 존재하는 column의 경우 이를 범주형 숫자로 바꿔버리는 Encoder

### 5. from sklearn.pipeline import Pipeline, make_pipeline

- Machine learning을 사용할 때, 이 방법을 사용하면 매우 편해질 것으로 예상됨.
- 전처리부터 시작해서, 모델을 학습하는 과정까지를 하나의 pipeline으로 두어서 쉽게 관리할 수 있게 됨.
- 사용법 1(`Pipeline`)

```python
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

num_pipeline = Pipeline([
    ("impute", SimpleImputer(strategy="median")), # 비어있는 값에 대해서 어떻게 값을 메꿀지를 지정해주는 SimpleImputer 메소드, "median", "mean", "most_frequent", "constant" 등의 방법이 존재하므로 자세한건 document를 참고
    ("standardize", StandardScaler()), # 표준화를 진행
])

# Pipeline은 ("변환기 이름", "변환함수") 이 두가지를 인자로 받아감.

from sklearn import set_config

set_config(display = "diagram")
num_pipeline # 이렇게 하면 그림으로 나타나, 쉽게 pipeline을 확인할 수 있다.
```

![pipe-line](/assets/machine-learning/pipeline1.png){: .align-center}

- 사용법 2(`make_pipeline`)

```python
from sklearn.pipeline import make_pipeline

num_pipeline = make_pipeline(SimpleImputer(strategy="median"), StandardScaler())

# make_pipeline은 Pipeline과 다르게 "변환기 이름"을 지정해주지 않아도 된다.
```

### 6. from sklearn.preprocessing import FunctionTransformer

- 가지고 있는 데이터로부터 새로운 feature를 추가할 때, 사용자 지정의 transformer가 필요하다. 이때 사용할 수 있는게 `FunctionTransformer`이다.
- 사용법은 `FunctionTransformer([하고 싶은 함수], kw_args = [하고싶은 함수의 keyword parameters])`이다.
- 사용법

```python
sf_coords = 37.7749, -122.41
sf_transformer = FunctionTransformer(rbf_kernel,
                                     kw_args=dict(Y=[sf_coords], gamma=0.1))
sf_simil = sf_transformer.transform(housing[["latitude", "longitude"]])
```

### 7. from sklearn.compose import ColumnTransformer

- Machine learning 전처리의 어려운 점은 어떠한 column을 전처리하는지 지정하는 것이다.
- 하지만 `pipeline`과 함께라면 쉽게 column에 대해서 지정할 수 있고, 반복적으로 진행할 수 있다.
- 사용법

```python
def column_ratio(X):
    return X[:, [0]] / X[:, [1]]

def ratio_name(function_transformer, feature_names_in):
    return ["ratio"]  # get_feature_names_out에 사용

def ratio_pipeline():
    return make_pipeline(
        SimpleImputer(strategy="median"),
        FunctionTransformer(column_ratio, feature_names_out=ratio_name),
        StandardScaler())

from sklearn.cluster import KMeans

class ClusterSimilarity(BaseEstimator, TransformerMixin):
    def __init__(self, n_clusters=10, gamma=1.0, random_state=None):
        self.n_clusters = n_clusters
        self.gamma = gamma
        self.random_state = random_state

    def fit(self, X, y=None, sample_weight=None):
        # 사이킷런 1.2버전에서 최상의 결과를 찾기 위해 반복하는 횟수를 지정하는 `n_init` 매개변수 값에 `'auto'`가 추가되었습니다.
        # `n_init='auto'`로 지정하면 초기화 방법을 지정하는 `init='random'`일 때 10, `init='k-means++'`일 때 1이 됩니다.
        # 사이킷런 1.4버전에서 `n_init`의 기본값이 10에서 `'auto'`로 바뀝니다. 경고를 피하기 위해 `n_init=10`으로 지정합니다.
        self.kmeans_ = KMeans(self.n_clusters, n_init=10, random_state=self.random_state)
        self.kmeans_.fit(X, sample_weight=sample_weight)
        return self  # 항상 self를 반환합니다!

    def transform(self, X):
        return rbf_kernel(X, self.kmeans_.cluster_centers_, gamma=self.gamma)

    def get_feature_names_out(self, names=None):
        return [f"클러스터 {i} 유사도" for i in range(self.n_clusters)]

log_pipeline = make_pipeline(
    SimpleImputer(strategy="median"),
    FunctionTransformer(np.log, feature_names_out="one-to-one"),
    StandardScaler())
cluster_simil = ClusterSimilarity(n_clusters=10, gamma=1., random_state=42)
default_num_pipeline = make_pipeline(SimpleImputer(strategy="median"),
                                     StandardScaler())
preprocessing = ColumnTransformer([
        ("bedrooms", ratio_pipeline(), ["total_bedrooms", "total_rooms"]),
        ("rooms_per_house", ratio_pipeline(), ["total_rooms", "households"]),
        ("people_per_house", ratio_pipeline(), ["population", "households"]),
        ("log", log_pipeline, ["total_bedrooms", "total_rooms", "population",
                               "households", "median_income"]),
        ("geo", cluster_simil, ["latitude", "longitude"]),
        ("cat", cat_pipeline, make_column_selector(dtype_include=object)),
    ],
    remainder=default_num_pipeline)  # 남은 특성: housing_median_age
```

### 8. 전처리 pipeline과 머신러닝 방법론을 하나의 pipeline으로 잇는 방법

- pipeline의 강력한 점은 machine learning의 방법론과 합쳐서 사용할 수 있다는 점인데, 이를 통해서 machine learning 작업을 수월히 할 수 있을 것으로 기대됨.
- 사용법

```python
from sklearn.tree import DecisionTreeRegressor

tree_reg = make_pipeline(preprocessing, DecisionTreeRegressor(random_state=42)) # preprocessing은 7번에 있는 preprocessing을 의미함.
                                                                                # 이코드는 preprocessing을 한 뒤에 DecisionTreeRegressor를 진행하라는 뜻임.
tree_reg.fit(housing, housing_labels) # preprocessing → DecisionTreeRegressor를 실제로 진행.
```

![pipe-line-collapsed](/assets/machine-learning/pipeline-ml-method-collapse.png){: .align-center}

### 9. from sklearn.model_selection import cross_val_score

- machine learning에서는 cross validation을 하는 경우가 다반사임. 따라서 위의 method를 잘알아두면 좋음.
- 사용법

```python
from sklearn.model_selection import cross_val_score

tree_rmses = -cross_val_score(tree_reg, housing, housing_labels,
                              scoring="neg_root_mean_squared_error", cv=10) #neg_root_mean_squared_error를 해서 앞에 (-)를 붙인 것에 주의

pd.Series(tree_rmses).describe() # fold들에 대한 결과를 요약해서 반환함.
# count       10.000000
# mean     66868.027288
# std       2060.966425
# min      63649.536493
# 25%      65338.078316
# 50%      66801.953094
# 75%      68229.934454
# max      70094.778246
# dtype: float64
```

### 10. pipeline과 gridsearch

- pipeline이 있으면 gridsearch도 쉽게 할 수 있음.
- 사용법

```python
from sklearn.model_selection import GridSearchCV

full_pipeline = Pipeline([
    ("preprocessing", preprocessing),
    ("random_forest", RandomForestRegressor(random_state=42)),
])
param_grid = [
    {'preprocessing__geo__n_clusters': [5, 8, 10], # preprocessing__(언더바 2개): full_pipeline변수에서 "preprocess"을 찾아가게 해서,
                                                # 여기서 preprocessing pipeline을 찾아들어간 뒤에, geo__(언더바 2개)라는 transformer를 찾아 들어간 뒤에, 여기서 keyword변수인 n_cluster를 바꾸겠다는 뜻임.
     'random_forest__max_features': [4, 6, 8]},
    {'preprocessing__geo__n_clusters': [10, 15],
     'random_forest__max_features': [6, 8, 10]},
]
grid_search = GridSearchCV(full_pipeline, param_grid, cv=3,
                           scoring='neg_root_mean_squared_error')
grid_search.fit(housing, housing_labels)
```

자세한 내용은 search와 documentation을 통해서 익숙해지도록 하자.
