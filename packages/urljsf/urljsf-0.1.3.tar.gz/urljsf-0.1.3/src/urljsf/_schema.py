"""Generated schema for ``urljsf``"""
# Copyright (C) urljsf contributors.
# Distributed under the terms of the Modified BSD License.

from __future__ import annotations

import sys

if sys.version_info >= (3, 11):  # pragma: no cover
    from typing import Any, Literal, Required, TypeAlias, TypedDict, Union
else:  # pragma: no cover
    from typing import Any, Literal, TypedDict, Union

    from typing_extensions import Required, TypeAlias


ASchema = Union["_AnySchemaLocation", "AnInlineObject"]
"""
A Schema.

A schema-like object referenced by URL, or inline as an object

Aggregation type: oneOf
Subtype: "_AnySchemaLocation", "AnInlineObject"
"""


AnInlineObject = dict[str, Any]
"""
An Inline Object.

A literal object
"""


class AnyForm(TypedDict, total=False):
    """Any Form.

    a definition of a form
    """

    form_data: ASchema
    """
    A Schema.

    A schema-like object referenced by URL, or inline as an object

    Aggregation type: oneOf
    Subtype: "_AnySchemaLocation", "AnInlineObject"
    """

    order: int | float
    """
    the order in which to show a form, lowest (or omitted) first, with a tiebreaker on name

    """

    props: _Props | _AnyFormPropsOneof1
    """
    JSON-compatible subset of `rjsf` component properties for this form


    Aggregation type: oneOf
    """

    schema: ASchema
    """
    A Schema.

    A schema-like object referenced by URL, or inline as an object

    Aggregation type: oneOf
    Subtype: "_AnySchemaLocation", "AnInlineObject"
    """

    ui_schema: ASchema
    """
    A Schema.

    A schema-like object referenced by URL, or inline as an object

    Aggregation type: oneOf
    Subtype: "_AnySchemaLocation", "AnInlineObject"
    """


FileFormat = Literal["json", "toml", "yaml"]
"""
File Format.

a format that can be serialized or deserialized
"""
FILEFORMAT_JSON: Literal["json"] = "json"
"""The values for the 'File Format' enum"""
FILEFORMAT_TOML: Literal["toml"] = "toml"
"""The values for the 'File Format' enum"""
FILEFORMAT_YAML: Literal["yaml"] = "yaml"
"""The values for the 'File Format' enum"""


# | urljsf.
# |
# | A schema for building forms for building URLs for building...
Urljsf = TypedDict(
    "Urljsf",
    {
        # | an optional identifier for this instance of the `urljsf` schema
        # |
        # |
        # | format: uri-reference
        "$id": str,
        # | an optional identifier for the `urljsf` schema that constrains this: this
        # | can be used by non-`urljsf` tools to validate and provide more insight while
        # | authoring.
        # |
        # |
        # | format: uri-reference
        "$schema": str,
        # | `nunjucks` templates keyed by the label displayed to a form user: any evaluating
        # | to a non-whitespace string will be considered _failing_.
        "checks": "_Checks",
        # | forms used to build and populate a URL
        # |
        # | Required property
        "forms": Required["_Forms"],
        # | isolate each form on the page in an `iframe`
        "iframe": bool,
        # | additional simple CSS to apply to an `iframe` element (implies `iframe`)
        # |
        "iframe_style": str,
        # | don't try to add a link to bootstrap if missing.
        # |
        # | default: False
        "no_bootstrap": bool,
        # | options for the `nunjucks` environment
        "nunjucks": "_UrljsfNunjucks",
        # | CSS rules, or nested selector objects containing more rules
        "style": "_Styles",
        # | [nunjucks](https://mozilla.github.io/nunjucks/templating.html) strings
        # | (or lists of strings) that control how strings are built from forms.
        # | See documentation for further customizations.
        # |
        # |
        # | WARNING: Normally the types should be a mix of each other instead of Union.
        # | See: https://github.com/camptocamp/jsonschema-gentypes/issues/7
        # |
        # | Required property
        "templates": Required["_Templates"],
    },
    total=False,
)


_AnyFormPropsOneof1 = str
""" format: #/definitions/any-schema-location """


_AnySchemaLocation = str
"""
a path to a JSON schema, serialized as JSON, TOML, or (simple) YAML. The URN-like
`py:module.submodule:member` may be used to reference an importable module
`dict` or `str` member, or function that returns one, and will be expanded into
a JSON object or URL.

format: uri-reference
minLength: 1
"""


_AnyStyle = Union[str, dict[str, Any]]
"""
A CSS rule, or a nested selector object containing more rules

Aggregation type: oneOf
"""


_AnyTemplate = Union["_AnyTemplateAnyof0", "_AnyTemplateAnyof1"]
""" Aggregation type: anyOf """


_AnyTemplateAnyof0 = str
""" a `nunjucks` template as a simple string """


_AnyTemplateAnyof1 = list[str]
"""
    a template as a list of strings that will be concatenated before being rendered


minItems: 1
"""


_Checks = dict[str, "_AnyTemplate"]
"""
`nunjucks` templates keyed by the label displayed to a form user: any evaluating
to a non-whitespace string will be considered _failing_.
"""


_Forms = dict[str, "AnyForm"]
""" forms used to build and populate a URL """


class _Props(TypedDict, total=False):
    """JSON-compatible default values for `rjsf` [Form.props][props].

    [props]: https://rjsf-team.github.io/react-jsonschema-form/docs/api-reference/form-props
    """

    acceptCharset: str
    """ The value of this prop will be passed to the `accept-charset` HTML attribute on the form """

    action: str
    """
    The value of this prop will be passed to the `action` HTML attribute on the form

    NOTE: this just renders the `action` attribute in the HTML markup. There is no real network request being sent to this `action` on submit. Instead, react-jsonschema-form catches the submit event with `event.preventDefault()` and then calls the `onSubmit` function, where you could send a request programmatically with `fetch` or similar.
    """

    autoComplete: str
    """ The value of this prop will be passed to the `autocomplete` HTML attribute on the form """

    className: str
    """ The value of this prop will be passed to the `class` HTML attribute on the form """

    disabled: bool
    """ It's possible to disable the whole form by setting the `disabled` prop. The `disabled` prop is then forwarded down to each field of the form. If you just want to disable some fields, see the `ui:disabled` parameter in `uiSchema` """

    enctype: str
    """ The value of this prop will be passed to the `enctype` HTML attribute on the form """

    extraErrorsBlockSubmit: bool
    """ If set to true, causes the `extraErrors` to become blocking when the form is submitted """

    focusOnFirstError: bool
    """ If set to true, then the first field with an error will receive the focus when the form is submitted with errors """

    formContext: dict[str, Any]
    """ globals for custom UI """

    formData: dict[str, Any]
    """ The data for the form, used to prefill a form with existing data """

    id: str
    """ The value of this prop will be passed to the `id` HTML attribute on the form """

    idPrefix: str
    """ To avoid collisions with existing ids in the DOM, it is possible to change the prefix used for ids; Default is `root` """

    idSeparator: str
    """ To avoid using a path separator that is present in field names, it is possible to change the separator used for ids (Default is `_`) """

    liveOmit: bool
    """ If `omitExtraData` and `liveOmit` are both set to true, then extra form data values that are not in any form field will be removed whenever `onChange` is called. Set to `false` by default """

    liveValidate: bool
    """ If set to true, the form will perform validation and show any validation errors whenever the form data is changed, rather than just on submit """

    method: str
    """ The value of this prop will be passed to the `method` HTML attribute on the form """

    name: str
    """ The value of this prop will be passed to the `name` HTML attribute on the form """

    noHtml5Validate: bool
    """ If set to true, turns off HTML5 validation on the form; Set to `false` by default """

    omitExtraData: bool
    """ If set to true, then extra form data values that are not in any form field will be removed whenever `onSubmit` is called. Set to `false` by default. """

    readonly: bool
    """ It's possible to make the whole form read-only by setting the `readonly` prop. The `readonly` prop is then forwarded down to each field of the form. If you just want to make some fields read-only, see the `ui:readonly` parameter in `uiSchema` """

    schema: dict[str, Any]
    """ The JSON schema object for the form """

    showErrorList: _PropsShowerrorlist
    """ When this prop is set to `top` or 'bottom', a list of errors (or the custom error list defined in the `ErrorList`) will also show. When set to false, only inline input validation errors will be shown. Set to `top` by default """

    tagName: str
    """ It's possible to change the default `form` tag name to a different HTML tag, which can be helpful if you are nesting forms. However, native browser form behaviour, such as submitting when the `Enter` key is pressed, may no longer work """

    target: str
    """ The value of this prop will be passed to the `target` HTML attribute on the form """

    uiSchema: _Uischema
    """

    WARNING: Normally the types should be a mix of each other instead of Union.
    See: https://github.com/camptocamp/jsonschema-gentypes/issues/7
    """


_PropsShowerrorlist = Literal[False, "top", "bottom"]
""" When this prop is set to `top` or 'bottom', a list of errors (or the custom error list defined in the `ErrorList`) will also show. When set to false, only inline input validation errors will be shown. Set to `top` by default """
_PROPSSHOWERRORLIST_FALSE: Literal[False] = False
"""The values for the 'When this prop is set to `top` or 'bottom', a list of errors (or the custom error list defined in the `ErrorList`) will also show. When set to false, only inline input validation errors will be shown. Set to `top` by default' enum"""
_PROPSSHOWERRORLIST_TOP: Literal["top"] = "top"
"""The values for the 'When this prop is set to `top` or 'bottom', a list of errors (or the custom error list defined in the `ErrorList`) will also show. When set to false, only inline input validation errors will be shown. Set to `top` by default' enum"""
_PROPSSHOWERRORLIST_BOTTOM: Literal["bottom"] = "bottom"
"""The values for the 'When this prop is set to `top` or 'bottom', a list of errors (or the custom error list defined in the `ErrorList`) will also show. When set to false, only inline input validation errors will be shown. Set to `top` by default' enum"""


_Styles = dict[str, "_AnyStyle"]
""" CSS rules, or nested selector objects containing more rules """


_Templates = Union[dict[str, "_AnyTemplate"], "_TemplatesTyped"]
"""
[nunjucks](https://mozilla.github.io/nunjucks/templating.html) strings
(or lists of strings) that control how strings are built from forms.
See documentation for further customizations.


WARNING: Normally the types should be a mix of each other instead of Union.
See: https://github.com/camptocamp/jsonschema-gentypes/issues/7
"""


class _TemplatesTyped(TypedDict, total=False):
    download_filename: _AnyTemplate
    """ Aggregation type: anyOf """

    submit_button: _AnyTemplate
    """ Aggregation type: anyOf """

    submit_target: _AnyTemplate
    """ Aggregation type: anyOf """

    url: _AnyTemplate
    """ Aggregation type: anyOf """


_URLJSF_NO_BOOTSTRAP_DEFAULT = False
""" Default value of the field path 'urljsf no_bootstrap' """


_Uischema = Union[dict[str, "_UischemaAdditionalproperties"], "_UischemaTyped"]
"""

WARNING: Normally the types should be a mix of each other instead of Union.
See: https://github.com/camptocamp/jsonschema-gentypes/issues/7
"""


_UischemaAdditionalproperties = Union[
    "_Uischema", Union[str, Union[int, float], dict[str, Any], list[Any], bool, None]
]
""" Aggregation type: anyOf """


_UischemaTyped = TypedDict(
    "_UischemaTyped",
    {
        # |
        # | WARNING: Normally the types should be a mix of each other instead of Union.
        # | See: https://github.com/camptocamp/jsonschema-gentypes/issues/7
        "items": "_Uischema",
        # | Allows RJSF to override the default field implementation by specifying either the name of a field that is used to look up an implementation from the `fields` list or an actual one-off `Field` component implementation itself
        "ui:field": str,
        "ui:fieldReplacesAnyOrOneOf": bool,
        # | An object that contains all the potential UI options in a single object
        "ui:options": "_UischemaUiColonOptions",
        "ui:rootFieldId": str,
    },
    total=False,
)


# | An object that contains all the potential UI options in a single object
_UischemaUiColonOptions = TypedDict(
    "_UischemaUiColonOptions",
    {
        # | We know that for title, it will be a string, if it is provided
        "title": str,
        # | We know that for description, it will be a string, if it is provided
        "description": str,
        # | Any classnames that the user wants to be applied to a field in the ui
        "classNames": str,
        # | Flag, if set to `true`, will mark all child widgets from a given field as disabled
        "disabled": bool,
        # | The default value to use when an input for a field is empty
        # |
        # | Aggregation type: anyOf
        "emptyValue": "_UischemaUiColonOptionsEmptyvalue",
        # | Will disable any of the enum options specified in the array (by value)
        "enumDisabled": list[Union[str, Union[int, float], bool]],
        # | Allows a user to provide a list of labels for enum values in the schema
        # |
        # | Aggregation type: anyOf
        "enumNames": "_UischemaUiColonOptionsEnumnames",
        # | Flag, if set to `true`, will cause the `FileWidget` to show a preview (with download for non-image files)
        "filePreview": bool,
        # | Used to add text next to a field to guide the end user in filling it in
        "help": str,
        # | Flag, if set to `true`, will hide the default error display for the given field AND all of its child fields in the hierarchy
        "hideError": bool,
        # | Flag, if set to `true`, will mark a list of checkboxes as displayed all on one line instead of one per row
        "inline": bool,
        # | Used to change the input type (for example, `tel` or `email`) for an <input>
        "inputType": str,
        # | This property allows you to reorder the properties that are shown for a particular object
        # |
        # | Aggregation type: anyOf
        "order": "_UischemaUiColonOptionsOrder",
        # | We know that for placeholder, it will be a string, if it is provided
        "placeholder": str,
        # | Flag, if set to `true`, will mark all child widgets from a given field as read-only
        "readonly": bool,
        # | Provides a means to set the initial height of a textarea widget
        "rows": Union[int, float],
        "style": dict[str, Any],
        # | custom overrides for urlsjf grid
        "urljsf:grid": "_UischemaUiColonOptionsUrljsfColonGrid",
        "widget": str,
    },
    total=False,
)


_UischemaUiColonOptionsEmptyvalue = Union[
    bool,
    Union[int, float],
    str,
    dict[str, Any],
    "_UischemaUiColonOptionsEmptyvalueAnyof",
    None,
]
"""
The default value to use when an input for a field is empty

Aggregation type: anyOf
"""


_UischemaUiColonOptionsEmptyvalueAnyof: TypeAlias = None
"""
items:
  {}
"""


_UischemaUiColonOptionsEnumnames = Union[
    bool,
    Union[int, float],
    str,
    "_UischemaUiColonOptionsEnumnamesAnyof",
    list[Union[str, Union[int, float], dict[str, Any], list[Any], bool, None]],
    None,
]
"""
Allows a user to provide a list of labels for enum values in the schema

Aggregation type: anyOf
"""


_UischemaUiColonOptionsEnumnamesAnyof: TypeAlias = None
"""
items:
  type: string
"""


_UischemaUiColonOptionsOrder = Union[
    bool,
    Union[int, float],
    str,
    "_UischemaUiColonOptionsOrderAnyof",
    list[Union[str, Union[int, float], dict[str, Any], list[Any], bool, None]],
    None,
]
"""
This property allows you to reorder the properties that are shown for a particular object

Aggregation type: anyOf
"""


_UischemaUiColonOptionsOrderAnyof: TypeAlias = None
"""
items:
  type: string
"""


class _UischemaUiColonOptionsUrljsfColonGrid(TypedDict, total=False):
    """custom overrides for urlsjf grid"""

    addButton: list[str]
    children: dict[str, list[str]]
    default: list[str]


class _UrljsfNunjucks(TypedDict, total=False):
    """options for the `nunjucks` environment"""

    filters: list[_UrljsfNunjucksFiltersItem]
    """
    filters to ensure in `nunjucks` templates

    uniqueItems: True
    """


_UrljsfNunjucksFiltersItem = Union["FileFormat"]
""" Aggregation type: oneOf """
