---
title: Azure AI Language Exercises
permalink: index.html
layout: home
---

# Azure AI Language Exercises

The following exercises are designed to provide you with a hands-on learning experience in which you'll explore common tasks that developers do when building natural language solutions on Azure. 

> **Note**: To complete the exercises, you'll need an Azure subscription. If you don't already have one, you can sign up for an [Azure account](https://azure.microsoft.com/free). There's a free trial option for new users that includes credits for the first 30 days.

## Exercises

{% assign labs = site.pages | where_exp:"page", "page.url contains '/Instructions/Labs'" %}
{% for activity in labs  %}
<hr>

### [{{ activity.lab.title }}]({{ site.github.url }}{{ activity.url }})

{{activity.lab.description}}

{% endfor %}

<hr>

> **Note**: While you can complete these exercises on their own, they're designed to complement modules on [Microsoft Learn](https://learn.microsoft.com/training/paths/develop-language-solutions-azure-ai/); in which you'll find a deeper dive into some of the underlying concepts on which these exercises are based. 
