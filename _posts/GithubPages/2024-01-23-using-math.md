---
title: "Using LaTex in Minimal mistakes"
show_date: true
comments: true
layout: single
categories:
  - Github pages
tags:
  - Github pages
toc: true
toc_sticky: true
published: false
---

We have to set up several things to use LaTex in Minimal Mistakes Jekyll.

I referenced [this page](https://singyuan.github.io/posts/mathjax/add_tex/)

### 1. Set Markdown Engine to Kramdown

Change the engine of `kramdown` as follows

{% highlight javascript %}
markdown: karmdown
{% endhighlight %}

### 2. Copy the original `script.html`

Copy over `minimal-mistakes/_includes/scripts.html` and paste to our `_includes/scripts.html.`

Most of you will have the vanilla one if you don't change the `script.html`, so don't worry about it.

### 3. Modify `head.html`

Append the following content to `head.html.`

{% highlight javascript %}

<!-- Mathjax Support -->
<script type="text/javascript" async
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-MML-AM_CHTML">
</script>

{% endhighlight %}

### 4. Test the Latex

use `$$...$$` for the math equation

{% highlight javascript %}

$$
y_{t} = X_{t}\beta
$$

{% endhighlight %}

It will show now as

$$
y_{t} = X_{t}\beta
$$

Enjoy the LaTex.
