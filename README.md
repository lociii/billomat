[![Travis CI build status](https://travis-ci.org/lociii/billomat.svg)](https://travis-ci.org/lociii/billomat)

Python client for the [billomat.com](http://www.billomat.com) [API](http://www.billomat.com/en/api/)
=====================================================================================================

The syntax of the client is inspired by the great [Django ORM](https://docs.djangoproject.com/en/dev/topics/db/queries/).

Example usage
--------------

```python
from billomat import models
from billomat.base import Client

Client.api_name = 'apiname'
Client.api_key = 'apikey'

# set optional app-id and -secret
Client.app_id = 'app_id'
Client.app_secret = 'app_secret'

articles = models.Article.objects.all()
for article in articles:
    print unicode(article.title)
articles = articles.filter(title='Awesome')
for article in articles:
    print unicode(article.title)

article = models.Article.objects.get(article_number=2)
article.title = u'This is an awesome article'
article.save()

article = models.Article.objects.create(
    title=u'This is an awesome article',
)
article.delete()
```

Django support
---------------
Automatic client configuration by django config is supported

```python
BILLOMAT_API_NAME = 'aaa'
BILLOMAT_API_KEY = 'bbb'
BILLOMAT_APP_ID = 'ccc'
BILLOMAT_APP_SECRET = 'ddd'
```

The client sends 3 django signals:

- billomatclient_request, send before the request
- billomatclient_response, send after the request containing the response
- billomatclient_error, send after a request error containing the exception

Each signal sends a request_id which is a unique identifier (uuid4) for each request to track the status along the signal flow.

License
--------
[MIT](https://github.com/lociii/billomat/blob/master/LICENSE.md)
