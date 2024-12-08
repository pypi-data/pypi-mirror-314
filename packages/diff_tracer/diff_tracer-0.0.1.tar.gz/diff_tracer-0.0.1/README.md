<h1 align="center">DIFF TRACER</h1>
<p align="center">
  A FastAPI utility designed to compare two API responses, making it easier to validate behavior and ensure accuracy during refactoring.
  <br/><br/>
  <a href="https://github.com/betofigueiredo/diff_tracer/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge&labelColor=363a4f&color=a6da95"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Made%20with-Python-blue?style=for-the-badge&labelColor=363a4f&color=346FA0"></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/Made%20with-FastAPI-blue?style=for-the-badge&labelColor=363a4f&color=009485"></a>
  <br/><br/>
  <img src="https://github.com/user-attachments/assets/53b3f1cd-f5a8-43de-9b9d-3a3dfbad064c" alt="Preview" width="100%"/>
</p>

> [!WARNING]
> Please keep in mind that Diff Tracer is still under active development

<br />

## Installation

```zsh
❯ pip install diff_tracer
```

<br />

## Basic Usage

To compare two results:

```python
from diff_tracer import compare_async

@app.get("/")
async def get_data():
    return await compare_async(
        current_fn=lambda: currentUseCase(), # current function in production
        new_fn=lambda: newUseCase(), # new refactored function
        percentage=80, # percentage of requests to compare, good to control expensive endpoints
    )
```

Active the dashboard endpoint in your main file:

```python
from fastapi import FastAPI
from diff_tracer import init_web_view


app = FastAPI()


init_web_view(app=app, security_token="362a9b3f302542deb3184671bbc3e7da")
```

Access http://localhost:{PORT}/diff-tracer-view/362a9b3f302542deb3184671bbc3e7da to view the dashboard.

Check a full working example on `./diff_tracer/fastapi_example.py`
<br /><br />

## Why

I used this aproach while working on a major endpoint refactor at my current company. The endpoint was critical but lacked comprehensive tests, making it challenging to ensure the refactored function behaved identically to the original. While I wrote some tests, I wanted an extra layer of confidence before deploying to production.
<br /><br />

## Known issues

- The dashboard endpoint is not secure. You can set a token to make it harder to access, but it's still not secure.
- The files are saved local on your API, so everytime you make a new deploy they will be erased.
  <br /><br />

## Contributing

For local development just install the libraries and start the FastAPI example file:

```zsh
❯ poetry install
❯ poetry run task start_api
```

Access http://localhost:8000/users to simulate requests.

Access http://localhost:8000/diff-tracer-view/1234 to view de dashboard. 1234 is the default token.

To run the tests:

```zsh
❯ poetry run task test
```

<br />

## Thanks to

The code that makes the comparison is from Google Diff, Match and Patch Library written by Neil Fraser Copyright (c) 2006 Google Inc. http://code.google.com/p/google-diff-match-patch/
