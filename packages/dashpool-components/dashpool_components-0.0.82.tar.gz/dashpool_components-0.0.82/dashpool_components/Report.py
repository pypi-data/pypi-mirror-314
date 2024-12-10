# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Report(Component):
    """A Report component.
Component to show a  Report

Keyword arguments:

- id (string; required):
    Unique ID to identify this component in Dash callbacks."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dashpool_components'
    _type = 'Report'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, **kwargs):
        self._prop_names = ['id']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Report, self).__init__(**args)
