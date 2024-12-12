# this a test

```urljsf {format=toml}
[forms.url.schema]
title = "pick an xkcd"
description = "this will redirect to `xkcd.com`"
type = "object"
required = ["xkcd"]
properties.xkcd = {type="integer", minimum=1, maximum=2997}

[forms.url.ui_schema.xkcd."ui:options"]
widget = "range"

[templates]
url = "https://xkcd.com/{{ data.url.xkcd }}"
submit_button = "see xkcd #{{ data.url.xkcd }}"
```
