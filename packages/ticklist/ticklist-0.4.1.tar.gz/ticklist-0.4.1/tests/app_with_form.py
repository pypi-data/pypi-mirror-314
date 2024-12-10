from typing import Collection, Type

from pydantic import BaseModel
from textual.app import App

from ticklist import form
from ticklist.annotation_iterators import ANNOTATION_ITERATORS
from ticklist.types import NO_VALUE, AnnotationIterator


class MyApp(App):
    """An app for testing purposes."""

    CSS_PATH = "app_with_form.tcss"

    def __init__(
        self,
        model_type: Type[BaseModel],
        value: BaseModel | None = None,
        annotation_iterators: Collection[AnnotationIterator] | None = None,
        with_model_info: bool = True,
    ):
        self._model_type = model_type
        self._value = value if value else NO_VALUE

        self._annotation_iterators = (
            annotation_iterators if annotation_iterators else ANNOTATION_ITERATORS
        )
        self._with_model_info = with_model_info
        super().__init__()

    def on_mount(self):
        self.push_screen(
            form.Form(
                self._model_type,
                self._value,
                self._annotation_iterators,
                model_info=self._with_model_info,
            )
        )
