---
layout: page
title: posts
permalink: /posts/
---

{% for post in site.posts %}
<div class="post-item">
  <span class="post-item-date">{{ post.date | date: "%b %d, %Y" }}</span>
  <h2 class="post-item-title"><a href="{{ post.url }}">{{ post.title }}</a></h2>
</div>
{% endfor %}
