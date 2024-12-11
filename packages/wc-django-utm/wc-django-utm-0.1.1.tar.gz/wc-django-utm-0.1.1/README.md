# WebCase UTM tracker

Simple middleware and utils for tracking utm parameters.

## Installation

```sh
pip install wc-django-utm
```

In `settings.py`:

```python
INSTALLED_APPS += [
  'wcd_utm',
]

WCD_UTM = {
  # All the "main" parameters that must be resolved.
  'PARAMETERS': [
    'utm_source', 'utm_medium', 'utm_campaign',
    'utm_term', 'utm_content',

    'gclid', 'aclk', 'msclkid', 'fbclid', 'twclid',
  ]),
  # Additional parameter prefixes. Also used to convert prefixed parameters
  # like "utm_content" into "content".
  'RESOLVABLE_PREFIXES':['utm_'],
  # Whether to unwrap prefixed parameters or not.
  # Example: "utm_content" will be unwrapped into "content".
  # By default - do not.
  'UNWRAP_PREFIXED_PARAMETERS': False,

  # Used to store all different utm parameters sets, that user had during the
  # session.
  'SESSION_STORAGE_KEY': 'utm_params_stored',
  # Latest utm parameters set. The key that you are mostly going to use.
  'SESSION_ACCESS_KEY': 'utm_params',

  # Header to parse UTM parameters from as if it is URL.
  # Use this to pass utm parameters from Android/iOS app, for example.
  'HEADER_ORIGIN_URL': 'HTTP_X_UTM_ORIGIN_URL',
  # Same as previous, but this one should store JSON data instead of plain
  # URL string.
  'HEADER_JSON': 'HTTP_X_UTM_JSON',
}
```

## Usage

Most of the time only the middleware will be used:

```python
MIDDLEWARE = [
  # ...
  'django.contrib.sessions.middleware.SessionMiddleware',
  # MUST be placed after session middleware ^.
  'wcd_utm.middleware.UTMSessionMiddleware',
  # ...
]
```

### In a view

Middleware will store parsed data in a `SESSION_ACCESS_KEY`(`'utm_params'`) key. Parameter values will always be a list of strings:

```python
def some_view(request):
  params = request.session["utm_params"]

  # Values are always lists
  if 'black_friday_sale' in params.get('utm_campaign', []):
    # Then do stuff related to you black friday sale campaign.
    pass

  # ...
```

