---
title: Develop AI Language and Speech solutions on Azure
permalink: index.html
layout: home
---

This page lists exercises associated with Microsoft skilling content on [Microsoft Learn](https://learn.microsoft.com/training/paths/develop-language-solutions-azure-ai/)

> **Note**: To complete the exercises, you'll need an Azure subscription. If you don't already have one, you can sign up for an [Azure account](https://azure.microsoft.com/free). There's a free trial option for new users that includes credits for the first 30 days.

## Exercises

<hr>

{% assign labs = site.pages | where_exp:"page", "page.url contains '/Instructions/Exercises'" %}
{% for activity in labs  %}
{% comment %}
Skip draft pages so in-progress labs don't appear in the published list.
A page with no status is treated as publishable, so existing exercises are unaffected.
{% endcomment %}
{% assign lab_status = activity.lab.status | default: '' | downcase %}
{% if activity.lab.title and lab_status != 'draft' %}

### [{{ activity.lab.title }}]({{ site.github.url }}{{ activity.url }})

{% if activity.lab.level %}**Level**: {{activity.lab.level}} \| {% endif %}{% if activity.lab.duration %}**Duration**: {{activity.lab.duration}} minutes{% endif %}

{% if activity.lab.description %}
*{{activity.lab.description}}*
{% endif %}
<hr>
{% endif %}
{% endfor %}
