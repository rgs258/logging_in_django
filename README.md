# Logging and Exception Handling in Django
## The Django Polls app with Logging Examples

Here you'll find some examples of how to use logging, added to the Django Polls app.

This repo was created for a session at DjangoCon US 2019 and my slides from the session are included in the root of the repo.

Please feel free to reach out with any questions :)

## Slide 40 - Getting to Django’s Exception Handler
Here are the notes from slide #40, if you're interested :)
We end up at Django’s exception handler on every request because of a middleware trick

1.  WSGI __init__:           runs        load_middleware
2.  load_middleware:         assigns     convert_exception_to_response      as the     _middleware_chain
3.  WSGI __call__:           calls       get_response
4.  get_response             assigns     _middleware_chain                  as the     response
