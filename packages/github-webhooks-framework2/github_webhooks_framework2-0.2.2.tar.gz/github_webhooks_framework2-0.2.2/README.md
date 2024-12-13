# Python GitHub Webhooks Framework

**NOTE:** Forked from [github_webhooks](https://github.com/karech/github-webhooks) as I needed to access more things:

- query params from incoming webhooks for identification
- `background_tasks` to handle long running webhook actions.

Simple and lightweight micro framework for quick integration with [GitHub
webhooks][1].  
It's based on [FastAPI][3] and [pydantic][4], nothing more!  
Async and mypy friendly.

[![Run CI](https://github.com/morriz/github-webhooks/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/morriz/github-webhooks/actions/workflows/ci.yml)  
[![PyPI](https://img.shields.io/pypi/v/github-webhooks-framework2.svg)][2]

## Installation

Just add `github-webhooks-framework2` package.  
Example:

- `pip install github-webhooks-framework2`
- `poetry add github-webhooks-framework2`

## Example

Create file `example.py` and copy next code:

```python
import uvicorn
from pydantic import BaseModel

from github_webhooks import create_app
from github_webhooks.schemas import WebhookCommonPayload


# WebhookCommonPayload is based on pydantic.BaseModel
class PullRequestPayload(WebhookCommonPayload):
    class Pull(BaseModel):
        title: str
        url: str

    action: str
    pull_request: Pull


# Initialize Webhook App
app = create_app()


# Register webhook handler:
#   `pull_request` - name of an event to handle
#   `PullRequestPayload` - webhook payload will be parsed into this model
@app.hooks.register('pull_request', PullRequestPayload)
async def handler(payload: PullRequestPayload) -> None:
    print(f'New pull request {payload.pull_request.title}')
    print(f'  link: {payload.pull_request.url}')
    print(f'  author: {payload.sender.login}')


if __name__ == '__main__':
    # start uvicorn server
    uvicorn.run(app)
```

### Let's have detailed overview.

We start by defining payload [Model][5] to parse incoming [Pull Request Body][6].

```python
class PullRequestPayload(WebhookCommonPayload):
    class Pull(BaseModel):
        title: str
        url: str

    action: str
    pull_request: Pull
```

In this example we only want to get `action`, `pull_request.title` and `pull_request.url` from payload.  
By subclassing `WebhookCommonPayload` model will automatically get `sender`, `repository` and `organization` fields.

Next - we are creating ASGI app (based on FastAPI app)

```python
app = create_app()
```

Optionally we can provide here `secret_token` [Github Webhook secret][7]

```python
app = create_app(secret_token='super-secret-token')
```

And time to define our handler

```python
@app.hooks.register('pull_request', PullRequestPayload)
async def handler(payload: PullRequestPayload) -> None:
    print(f'New pull request {payload.pull_request.title}')
    print(f'  link: {payload.pull_request.url}')
    print(f'  author: {payload.sender.login}')
```

We are using here `@app.hooks.register` deco, which accepts 2 arguments:

- `event: str` - name of webhook event
- `payload_cls: pydantic.BaseModel` - pydantic model class to parse request, subclassed from `pydantic.BaseModel`
  or `WebhookCommonPayload`.

And our handler function may include the following (named) params:

```python
async def handler(payload: PullRequestPayload, headers: WebhookHeaders, query_params: QueryParams, background_tasks: BackgroundTasks) -> Optional[str]:
    # `headers` will be WebhookHeaders model with Github Webhook headers parsed.
    ...
```

An example setup can be found in `example/server.py`.

## References:

[1]: https://developer.github.com/webhooks/
[2]: https://pypi.python.org/pypi/github-webhooks-framework
[3]: https://fastapi.tiangolo.com/
[4]: https://pydantic-docs.helpmanual.io/
[5]: https://pydantic-docs.helpmanual.io/usage/models/
[6]: https://docs.github.com/en/developers/webhooks-and-events/webhooks/webhook-events-and-payloads#pull_request
[7]: https://docs.github.com/en/developers/webhooks-and-events/webhooks/securing-your-webhooks

## Development

1. Install local venv: `python -m venv .venv`
2. Activate: `. .venv/bin/activate`
3. Install deps with `pip install -r requirements.txt -r requirements-test.txt`
4. When done with packages: `./freeze-requirements.sh`
