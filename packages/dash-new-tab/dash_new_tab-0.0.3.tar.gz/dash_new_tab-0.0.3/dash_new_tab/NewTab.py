# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class NewTab(Component):
    """A NewTab component.


Keyword arguments:

- id (string; required):
    The ID of this component, used to identify dash components  in
    callbacks. The ID needs to be unique across all of the  components
    in an app.

- href (string; optional):
    The URL to open in a new tab.

- n_opens (number; default 0):
    The number of times a new tab has been opened. Meant to be
    incremented manually by a callback to trigger opening of a new
    tab."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_new_tab'
    _type = 'NewTab'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, href=Component.UNDEFINED, n_opens=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'href', 'n_opens']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'href', 'n_opens']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(NewTab, self).__init__(**args)
