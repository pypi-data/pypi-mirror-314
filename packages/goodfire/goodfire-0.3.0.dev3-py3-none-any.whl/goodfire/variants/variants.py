from dataclasses import dataclass
import json
from collections import OrderedDict
from typing import Callable, Literal, Optional, Union
import uuid

from ..api.chat.interfaces import ChatMessage
from typing_extensions import TypedDict

from ..controller.controller import ConditionalGroup, Controller
from ..features.features import Feature, FeatureGroup
from ..exceptions import InferenceAbortedException

SUPPORTED_MODELS = Literal[
    "meta-llama/Meta-Llama-3-8B-Instruct", "meta-llama/Meta-Llama-3.1-70B-Instruct"
]


ScopeCallable = Callable[["NestedScope"], "NestedScope"]
HandlerCallable = Callable[["InferenceContext"], "InferenceContext"]


class FeatureDelta(TypedDict):
    mode: Literal["nudge", "pin"]
    value: Union[float]


class FeatureEdits:
    """A collection of feature modifications with ordered tracking.

    This class manages a set of feature edits using an OrderedDict to maintain
    the order in which edits were applied.
    """

    def __init__(self):
        self._edits: OrderedDict[Feature, FeatureDelta] = OrderedDict()

    def __getitem__(self, feature: Feature) -> FeatureDelta:
        return self._edits[feature]

    def __setitem__(self, feature: Feature, delta: FeatureDelta):
        self._edits[feature] = delta

    def __delitem__(self, feature: Feature):
        self._edits.pop(feature, None)

    def __iter__(self):
        return iter(list(self._edits.items()))

    def __len__(self):
        return len(self._edits)


class Variant:
    """A class representing a variant of a base model with feature modifications.

    This class allows for creating variants of a base model by applying
    feature modifications through either nudging or pinning values.

    Args:
        base_model (str): Identifier of the base model to create variants from

    Attributes:
        base_model (str): The base model identifier
        edits (FeatureEdits): Collection of feature modifications
    """

    def __init__(self, base_model: SUPPORTED_MODELS):
        self.base_model = base_model
        self.edits: FeatureEdits = FeatureEdits()
        self.scopes: list[NestedScope] = []
        self._handlers: dict[str, HandlerCallable] = {}

    def set(
        self,
        feature: Union[Feature, FeatureGroup],
        value: Union[float, None],
        mode: Literal["nudge", "pin"] = "nudge",
    ):
        """Set or modify feature values in the variant.

        Args:
            feature (Union[Feature, FeatureGroup]): Feature(s) to modify
            value (Union[float, None]): Value to apply:
                - float: For numerical adjustments
                - None: To clear the modification

            mode (Literal["nudge", "pin"], optional): Modification mode:
                - "nudge": Bias the feature strength
                - "pin": Set the feature strength to a fixed value

                Defaults to "pin".
        """
        if value is None:
            self.clear(feature)
            return

        if isinstance(feature, Feature):
            self.edits[feature] = {
                "mode": mode,
                "value": value,
            }
        else:
            for f in feature:
                self.edits[f] = {"mode": mode, "value": value}

    def clear(self, feature: Union[Feature, FeatureGroup]):
        """Remove modifications for specified feature(s).

        Args:
            feature (Union[Feature, FeatureGroup]): Feature(s) to clear modifications for
        """
        if isinstance(feature, Feature):
            del self.edits[feature]
        else:
            for f in feature:
                del self.edits[f]

    def reset(self):
        """Remove all feature modifications."""
        self.edits = FeatureEdits()
        self.scopes = []

    def __repr__(self):
        return str(self)

    def __str__(self):
        edits = "{"
        for feature, edit in self.edits:
            edits += f"\n      {feature}: {edit},"
        edits += "\n   }"

        return f"Variant(\n   base_model={self.base_model},\n   edits={edits}\n)"

    @classmethod
    def from_json(cls, variant_json: Union[str, dict]):
        if isinstance(variant_json, str):
            variant_json = json.loads(variant_json)

        variant = Variant(variant_json["base_model"])
        for edit in variant_json["edits"]:
            feature = Feature(
                uuid=edit["feature_id"],
                label=edit["feature_label"],
                max_activation_strength=edit["max_activation_strength"],
                index_in_sae=edit["index_in_sae"],
            )
            variant.set(feature, edit["value"], edit["mode"])

        for scope in variant_json["scopes"]:
            variant.scopes.append(NestedScope.from_json(scope))

        return variant

    def json(self):
        """Convert the variant to a JSON-compatible dictionary.

        Returns:
            dict: Dictionary containing base model and feature configurations
        """
        return {
            "base_model": self.base_model,
            "edits": [
                {
                    "feature_id": str(feature.uuid),
                    "feature_label": feature.label,
                    "max_activation_strength": feature.max_activation_strength,
                    "index_in_sae": feature.index_in_sae,
                    "mode": edit["mode"],
                    "value": edit["value"],
                }
                for feature, edit in self.edits
            ],
            "scopes": [scope.json() for scope in self.scopes],
        }

    def set_when(
        self,
        condition: ConditionalGroup,
        values: dict[Union[Feature, FeatureGroup], float],
    ) -> None:
        scope = NestedScope(condition, self)

        for feature, value in values.items():
            scope.set(feature, value)

        self.scopes.append(scope)

    def abort_when(self, condition: ConditionalGroup) -> None:
        def _abort_handler(context: InferenceContext) -> None:
            raise InferenceAbortedException(
                f"Aborted inference due to conditional check:\n {condition}"
            )

        self.handle_when(condition, _abort_handler)

    def handle_when(
        self, condition: ConditionalGroup, handler: HandlerCallable
    ) -> None:
        event_name = str(uuid.uuid4())
        self._handlers[event_name] = handler
        scope = NestedScope(condition, self, event_name=event_name)
        self.scopes.append(scope)

    @property
    def controller(self) -> Controller:
        """Get a controller instance with the variant's modifications applied.

        Returns:
            Controller: Controller instance with feature modifications
        """
        controller = Controller()

        for feature, edit in self.edits:
            if edit["mode"] == "nudge":
                controller[feature] += edit["value"]
            else:
                controller[feature] = edit["value"]

        for scope in self.scopes:
            with controller.when(scope.condition) as ctl_scope:
                if scope.event_name:
                    ctl_scope.interrupt(scope.event_name)
                    continue

                for feature, edit in scope._nested_variant.edits:
                    if edit["mode"] == "nudge":
                        controller[feature] += edit["value"]
                    else:
                        controller[feature] = edit["value"]

        return controller


class NestedScope:
    def __init__(
        self,
        condition: ConditionalGroup,
        base_variant: Variant,
        event_name: Optional[str] = None,
    ):
        self.event_name: Optional[str] = event_name
        self.condition = condition
        self._nested_variant = Variant(base_variant.base_model)

        self.set = self._nested_variant.set
        self.clear = self._nested_variant.clear
        self.reset = self._nested_variant.reset

    def json(self):
        return {
            "condition": self.condition,
            "nested_variant": self._nested_variant.json(),
        }

    @classmethod
    def from_json(cls, nested_scope_json: Union[str, dict]):
        if isinstance(nested_scope_json, str):
            nested_scope_json = json.loads(nested_scope_json)

        scope = NestedScope(
            condition=ConditionalGroup.from_json(nested_scope_json["condition"]),
            base_variant=Variant(nested_scope_json["base_model"]),
        )
        scope._nested_variant = Variant.from_json(nested_scope_json["nested_variant"])
        return scope


@dataclass
class InferenceContext:
    prompt: list[ChatMessage]
    response_so_far: str
