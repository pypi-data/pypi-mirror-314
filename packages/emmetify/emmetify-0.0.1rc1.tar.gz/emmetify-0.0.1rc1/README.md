# Emmetify

Emmetify is a tool that allows you to save LLM tokens by converting tree structured data like HTML to the Emmet notation.

## What is Emmet?

Emmet is a tool known well by many frontend developers for speeding up HTML coding using abbreviations.
In Emmetify we are using it in the opposite way, we convert HTML to Emmet notation to save LLM tokens.

## Why?

LLM agents can navigate on the web using raw HTML, they can prepare XPath or CSS selectors to extract the data they need or go deeper into the page by clicking on the links which they choose.

But HTML is expensive to process with LLMs, so we can save tokens by converting HTML to Emmet notation.
Which is way cheaper in tokens to process but because it's age (10 years) it's well known by all large language models so they can understand it and navigate on it.

## Install

```bash
pip install emmetify
```

## Usage

### Basic usage

```python
from emmetify import Emmetifier
import requests

emmetifier = Emmetifier()
html = requests.get("https://example.com").text
emmet = emmetifier.emmetify(html)
print(emmet)
```

### With HTML simplification
Allow to skip unimportant HTML tags and prioritize HTML attributes to use only the most important ones.
eg. 

```html
<link rel="stylesheet" href="style.css">
<div id="main" class="container" style="color: red;" data-test="ignore">Example</div>
```

will be converted to

```
div#main.container{Example}
```

Which is way shorter to process with LLMs. But still contains all the necessary information to navigate on the page.

#### Usage:
```python
from emmetify import Emmetifier
import requests
import openai

emmetifier = Emmetifier(config={"html": {"skip_tags": True, "prioritize_attributes": True}})
html = requests.get("https://example.com").text
result = emmetifier.emmetify(html)["result"]
print(result)

llm = openai.OpenAI()
prompt = f"Get list of xpath selectors for all the links on the following page: {result}"
response = llm.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": emmet}],
)
```

## Supported formats
- [x] HTML
- [ ] XML
- [ ] JSON
