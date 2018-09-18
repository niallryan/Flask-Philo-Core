from .test_views import (
    SimpleView, SimpleCorsView

)


URLS = (
    ('/', SimpleView, 'home'),
    ('/cors-api/test-cors', SimpleCorsView, 'cors'),
)
