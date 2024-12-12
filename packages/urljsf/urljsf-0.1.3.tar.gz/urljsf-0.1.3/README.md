# `urljsf`

|            docs             |                                          install                                           |                build                 |
| :-------------------------: | :----------------------------------------------------------------------------------------: | :----------------------------------: |
| [![docs][docs-badge]][docs] | [![install from pypi][pypi-badge]][pypi] [![install from conda-forge][conda-badge]][conda] | [![build][workflow-badge]][workflow] |

> Build statically-hostable, interactive HTML forms for making web requests
>
> _Powered by [`react-json-schema-form`][rjsf] and
> [`react-`][react-bootstrap][`bootstrap`][bootstrap]._

[bootstrap]: https://github.com/twbs/bootstrap
[json-schema]: https://json-schema.org
[rjsf]: https://github.com/rjsf-team/react-jsonschema-form
[react-bootstrap]: https://github.com/react-bootstrap/react-bootstrap
[ui-schema]:
  https://rjsf-team.github.io/react-jsonschema-form/docs/api-reference/uiSchema/
[docs]: https://urljsf.rtfd.org
[docs-badge]: https://readthedocs.org/projects/urljsf/badge/?version=latest
[conda-badge]: https://img.shields.io/conda/vn/conda-forge/urljsf
[conda]: https://anaconda.org/conda-forge/urljsf
[pypi-badge]: https://img.shields.io/pypi/v/urljsf
[pypi]: https://pypi.org/project/urljsf
[workflow-badge]:
  https://github.com/deathbeds/urljsf/actions/workflows/ci.yml/badge.svg?branch=main
[workflow]:
  https://github.com/deathbeds/urljsf/actions/workflows/ci.yml?query=branch%3Amain

**Visitors** to a `urljsf`-built page see:

- one or more interactive HTML forms...
  - defined by and validated against a JSON [Schema][json-schema], optionally with...
  - deep customizable [user interface][ui-schema]
  - pre-filled data
  - custom validation checks

Once the data is _validated_, the user sees a button which gets a URL, which can be:

- downloaded as a file
- opened in a new browser window
- copy and pasted
- submitted to an HTTP endpoint, either by opening a new window, or directly.
- open native applications like email

`urljsf` **doesn't** ship a server, so that part is up to you!

**Site builders** write TOML, JSON, YAML or python, then can use `urljsf` as:

- a drop-in-and-pray [`script`](#js-script)
- a standalone [CLI tool](#command-line)
- a [`sphinx`](#sphinx) or [`mkdocs`](#mkdocs) extension

... to create JavaScript/HTML forms that helps **visitors** provide good data for:

- pull requests
- issues
- galleries
- surveys
- on-demand build services
- precise test descriptions
- linter rules

## Install

[contrib]: https://github.com/deathbeds/urljsf/blob/main/CONTRIBUTING.md

### From PyPI

`urljsf` is distributed on [PyPI][pypi], with several optional extras to help ensure
tested versions are available:

```bash
pip install urljsf
# ... or    urljsf[sphinx]   for sphinx
# ... or    urljsf[mkdocs]   for mkdocs and pymdown-extensions
# ... or    urljsf[yaml]     for build time YAML parsing

# or...
uv install urljsf
# etc.
```

### From conda-forge

`urljsf` is also distributed on [`conda-forge`][conda], with similar extras:

```bash
pixi add urljsf
# ... or urljsf-with-sphinx
# ... or urljsf-with-mkdocs
# ... or urljsf-with-yaml

# or...
micromamba install -c conda-forge urljsf
# or...
mamba install -c conda-forge urljsf
# or...
conda install -c conda-forge urljsf
# etc.
```

### Development

See the [contributing guide][contrib] for a development install.

## Usage

`urljsf` work with some [JSON schema](#json-schema) constrained files as a:

- (not-recommended) hot-linked [`script`](#js-script)
- a standalone [site generator](#command-line) for simple sites
- a plugin for the [`sphinx`](#sphinx) and [`mkdocs`](#mkdocs) documentation systems

### JSON Schema

A `urljsf` is built from a number of JSON schema-constrained files. Writing these in
plain JSON is tedious, so TOML and YAML are also supported inputs for any of the methods
below. Learn more on the [schema documentation][schema-docs].

[schema-docs]: https://urljsf.rtfd.org/en/latest/use/schema.html

### JS Script

A very simple, but limited, usage is an `.html` file that links to `urljsf` and
`bootstrap` resources on the internet.

```html
<script type="application/vnd.deathbeds.urljsf.v0+toml">
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
</script>
<script
  type="module"
  src="https://deathbeds.github.io/urljsf/_static/index.js"
></script>
```

This technique has _many_ limitations, and is **not recommended**.

Some ways to improve:

- download a GitHub release and unpack it, serving the files next to it
- ensure bootstrap is loaded _before_ the script, with a `link` tag in a `head`.
- on the `script` element, use a `src` to point to a valid `urljsf` definition
- use the [CLI](#command-line) or a documentation extension for [`sphinx`](#sphinx) or
  [`mkdocs`](#mkdocs)

### Command Line

The `urljsf` command line generates a ready-to-serve, standalone site with all required
static assets. Written in `python`, it can reuse the extensive JSON schema support in
the python ecosystem, such as `msgspec` or `pydantic`.

```bash
prsf --help
```

`urljsf` requires at least a definition file, but offers many command line options: see
the [documentation][cli-docs] for more.

[cli-docs]: https://urljsf.rtfd.org/en/latest/use/cli.html

### Sphinx

After [installing](#install) with the `[sphinx]` extra, add `urljsf.sphinxext` to
`conf.py`:

```py
# conf.py
extensions = [
  # ... other extensions
  "urljsf.sphinxext",
]
```

Then use the `urljsf` directive in source files:

```rst
.. urljsf:  # a relative path to a description as a TOML, YAML, or JSON file or python
  :toml:
  # a form definition in TOML
```

See the [documentation][sphinx-docs] for more about configuring `urljsf.sphinxext`, the
`urljsf` directive, and more advanced use cases.

[sphinx-docs]: https://urljsf.rtfd.org/en/latest/use/sphinx.html

### Mkdocs

After [installing](#install) with the `[mkdocs]` extra, add `urljsf` to `mkdocs.yml`:

```yaml
# mkdocs.yml
plugins:
  - urljsf
```

Then use the `urljsf` fenced code block in source files:

````markdown
```urljsf {path=path/to/defnition.toml}

```
````

See the [documentation][mkdocs-docs] for more about configuring `urljsf`, the `urljsf`
fence, and more advanced use cases.

[mkdocs-docs]: https://urljsf.rtfd.org/en/latest/use/mkdocs.html

## Limitations

- `react-json-schema-form` cannot represent all possible data structures, such as
  writing a _new_ JSON schema _in_ JSON schema, or many features added after Draft 7
- the generated scripts _won't_ work when served from `file://` due to browser CORS
  headers requirements for `type="module"` scripts
- the [`sphinx`](#sphinx) integration is only tested with the `html` builder, the basic
  `alabaster` theme, and [`pydata-sphinx-theme`][pdst] (by way of `urljsf`'s own
  [documentation][sphinx-docs])
- the [`mkdocs`](#mkdocs) integration is only tested with the default theme

[pdst]: https://github.com/pydata/pydata-sphinx-theme

## Open Source

`urljsf` itself is licensed under the `BSD-3-Clause` license. You can do whatever you
want with it, but if you change it a lot, it's not the maintainers' problem.

`urljsf` distributes third-party JavaScript and CSS in various forms, licensed under the
`MIT`, `BSD-3-Clause`, and `ISC` licenses.
