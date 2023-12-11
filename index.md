---
title: Azure AI Language Exercises
permalink: index.html
layout: home
---

# Azure AI Language Exercises

The following exercises are designed to support the modules on Microsoft Learn for [Developing natural language solutions](https://learn.microsoft.com/training/paths/develop-language-solutions-azure-ai/).


{% assign labs = site.pages | where_exp:"page", "page.url contains '/Instructions/Exercises'" %}
{% for activity in labs  %}
- [{{ activity.lab.title }}]({{ site.github.url }}{{ activity.url }})
{% endfor %}
