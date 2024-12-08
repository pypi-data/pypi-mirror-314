######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.38                                                                                #
# Generated on 2024-12-08T03:54:57.945080                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.cards.card_modules.card
    import metaflow.plugins.cards.card_modules.basic

from .card import MetaflowCard as MetaflowCard
from .card import MetaflowCardComponent as MetaflowCardComponent
from .convert_to_native_type import TaskToDict as TaskToDict

ABS_DIR_PATH: str

RENDER_TEMPLATE_PATH: str

JS_PATH: str

CSS_PATH: str

def transform_flow_graph(step_info):
    ...

def read_file(path):
    ...

class DefaultComponent(metaflow.plugins.cards.card_modules.card.MetaflowCardComponent, metaclass=type):
    """
    The `DefaultCard` and the `BlankCard` use a JS framework that build the HTML dynamically from JSON.
    The `DefaultComponent` is the base component that helps build the JSON when `render` is called.
    
    The underlying JS framework consists of various types of objects.
    These can be found in: "metaflow/plugins/cards/ui/types.ts".
    The `type` attribute in a `DefaultComponent` corresponds to the type of component in the Javascript framework.
    """
    def __init__(self, title = None, subtitle = None):
        ...
    def render(self):
        ...
    ...

class TitleComponent(metaflow.plugins.cards.card_modules.card.MetaflowCardComponent, metaclass=type):
    def __init__(self, text = None):
        ...
    def render(self):
        ...
    ...

class SubTitleComponent(metaflow.plugins.cards.card_modules.card.MetaflowCardComponent, metaclass=type):
    def __init__(self, text = None):
        ...
    def render(self):
        ...
    ...

class SectionComponent(DefaultComponent, metaclass=type):
    def __init__(self, title = None, subtitle = None, columns = None, contents = []):
        ...
    @classmethod
    def render_subcomponents(cls, component_array, additional_allowed_types = [str, dict], allow_unknowns = False):
        ...
    def render(self):
        ...
    ...

class ImageComponent(DefaultComponent, metaclass=type):
    def __init__(self, src = None, label = None, title = None, subtitle = None):
        ...
    def render(self):
        ...
    ...

class TableComponent(DefaultComponent, metaclass=type):
    def __init__(self, title = None, subtitle = None, headers = [], data = [[]], vertical = False):
        ...
    @classmethod
    def validate(cls, headers, data):
        ...
    def render(self):
        ...
    ...

class DagComponent(DefaultComponent, metaclass=type):
    def __init__(self, title = None, subtitle = None, data = {}):
        ...
    def render(self):
        ...
    ...

class TextComponent(DefaultComponent, metaclass=type):
    def __init__(self, text = None):
        ...
    def render(self):
        ...
    ...

class LogComponent(DefaultComponent, metaclass=type):
    def __init__(self, data = None):
        ...
    def render(self):
        ...
    ...

class HTMLComponent(DefaultComponent, metaclass=type):
    def __init__(self, data = None):
        ...
    def render(self):
        ...
    ...

class PageComponent(DefaultComponent, metaclass=type):
    def __init__(self, title = None, subtitle = None, contents = []):
        ...
    def render(self):
        ...
    ...

class ErrorComponent(metaflow.plugins.cards.card_modules.card.MetaflowCardComponent, metaclass=type):
    def __init__(self, headline, error_message):
        ...
    def render(self):
        ...
    ...

class SerializationErrorComponent(ErrorComponent, metaclass=type):
    def __init__(self, component_name, error_message):
        ...
    ...

class ArtifactsComponent(DefaultComponent, metaclass=type):
    def __init__(self, title = None, subtitle = None, data = {}):
        ...
    def render(self):
        ...
    ...

class MarkdownComponent(DefaultComponent, metaclass=type):
    def __init__(self, text = None):
        ...
    def render(self):
        ...
    ...

class TaskInfoComponent(metaflow.plugins.cards.card_modules.card.MetaflowCardComponent, metaclass=type):
    """
    Properties
        page_content : a list of MetaflowCardComponents going as task info
        final_component: the dictionary returned by the `render` function of this class.
    """
    def __init__(self, task, page_title = 'Task Info', only_repr = True, graph = None, components = [], runtime = False):
        ...
    def render(self):
        """
        Returns:
            a dictionary of form:
                dict(metadata = {},components= [])
        """
        ...
    ...

class ErrorCard(metaflow.plugins.cards.card_modules.card.MetaflowCard, metaclass=type):
    def __init__(self, options = {}, components = [], graph = None):
        ...
    def reload_content_token(self, task, data):
        """
        The reload token will change when the component array has changed in the Metaflow card.
        The change in the component array is signified by the change in the component_update_ts.
        """
        ...
    def render(self, task, stack_trace = None):
        ...
    ...

class DefaultCardJSON(metaflow.plugins.cards.card_modules.card.MetaflowCard, metaclass=type):
    def __init__(self, options = {'only_repr': True}, components = [], graph = None):
        ...
    def render(self, task):
        ...
    ...

class DefaultCard(metaflow.plugins.cards.card_modules.card.MetaflowCard, metaclass=type):
    def __init__(self, options = {'only_repr': True}, components = [], graph = None):
        ...
    def render(self, task, runtime = False):
        ...
    def render_runtime(self, task, data):
        ...
    def refresh(self, task, data):
        ...
    def reload_content_token(self, task, data):
        """
        The reload token will change when the component array has changed in the Metaflow card.
        The change in the component array is signified by the change in the component_update_ts.
        """
        ...
    ...

class BlankCard(metaflow.plugins.cards.card_modules.card.MetaflowCard, metaclass=type):
    def __init__(self, options = {'title': ''}, components = [], graph = None):
        ...
    def render(self, task, components = [], runtime = False):
        ...
    def render_runtime(self, task, data):
        ...
    def refresh(self, task, data):
        ...
    def reload_content_token(self, task, data):
        """
        The reload token will change when the component array has changed in the Metaflow card.
        The change in the component array is signified by the change in the component_update_ts.
        """
        ...
    ...

class TaskSpecCard(metaflow.plugins.cards.card_modules.card.MetaflowCard, metaclass=type):
    def render(self, task):
        ...
    ...

