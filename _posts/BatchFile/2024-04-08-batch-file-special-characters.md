---
title: "Batch File - 특수문자가 경로에 있는 경우 설정하는 방법에 대하여"
show_date: true
comments: true
layout: single
categories:
  - etc
tags:
toc: true
toc_sticky: false
published: false
---

파이썬 파일을 \*.bat(배치파일)로 만들어서 사용하는 경우가 종종 있는데, 이때 경로에 특수문자가 있으면 실행이 되지 않는 문제가 있다. <br/>

이는 batch file이 utf-8을 못읽어서 발생하는 문제인 것으로 보인다. <br/>

[해당 링크](https://superuser.com/questions/1676567/how-to-use-special-characters-from-bat-file-in-windows)를 참조하여 \*.bat파일을 다음과 같이 바꾸니 되었다. <br/>

```
chcp 65001 >nul # 이거를 최상단에 추가
```
