django-smilies
=============

Smilies :) for django :cool:

Install
-------

    $ pip install -e git://github.com/numerodix/django-smilies.git#egg=django-smilies

Then add:

```python
INSTALLED_APPS = (
    ..
    'smilies',
    ..
)
```

How to use
----------

```html
{% load show_smilies %}

<p>{{ article.text|show_smilies }}</p>
```
