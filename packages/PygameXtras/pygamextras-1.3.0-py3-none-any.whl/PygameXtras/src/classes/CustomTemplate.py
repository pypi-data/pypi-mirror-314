from .Label import Label
from .Button import Button
from .Entry import Entry


class CustomTemplate:
    def __init__(self, **kwargs):
        self.__kwargs = kwargs

    def get(self, key):
        return self.__kwargs.get(key)

    def label(self, **kwargs) -> Label:
        local_kwargs = self.__kwargs.copy()
        for k, v in kwargs.items():
            local_kwargs[k] = v

        assert "surface" in local_kwargs.keys(), "<surface> has to be set"
        assert "text" in local_kwargs.keys(), "<text> has to be set"
        assert "size" in local_kwargs.keys(), "<size> has to be set"
        assert "xy" in local_kwargs.keys(), "<xy> has to be set"
        assert "anchor" in local_kwargs.keys(), "<anchor> has to be set"

        return Label(
            local_kwargs.pop("surface"),
            local_kwargs.pop("text"),
            local_kwargs.pop("size"),
            local_kwargs.pop("xy"),
            local_kwargs.pop("anchor"),
            **local_kwargs)
    
    def button(self, **kwargs) -> Button:
        local_kwargs = self.__kwargs.copy()
        for k, v in kwargs.items():
            local_kwargs[k] = v

        assert "surface" in local_kwargs.keys(), "<surface> has to be set"
        assert "text" in local_kwargs.keys(), "<text> has to be set"
        assert "size" in local_kwargs.keys(), "<size> has to be set"
        assert "xy" in local_kwargs.keys(), "<xy> has to be set"
        assert "anchor" in local_kwargs.keys(), "<anchor> has to be set"

        return Button(
            local_kwargs.pop("surface"),
            local_kwargs.pop("text"),
            local_kwargs.pop("size"),
            local_kwargs.pop("xy"),
            local_kwargs.pop("anchor"),
            **local_kwargs)
    
    def entry(self, **kwargs) -> Entry:
        local_kwargs = self.__kwargs.copy()
        for k, v in kwargs.items():
            local_kwargs[k] = v

        assert "surface" in local_kwargs.keys(), "<surface> has to be set"
        assert "text" in local_kwargs.keys(), "<text> has to be set"
        assert "size" in local_kwargs.keys(), "<size> has to be set"
        assert "xy" in local_kwargs.keys(), "<xy> has to be set"
        assert "anchor" in local_kwargs.keys(), "<anchor> has to be set"

        return Entry(
            local_kwargs.pop("surface"),
            local_kwargs.pop("text"),
            local_kwargs.pop("size"),
            local_kwargs.pop("xy"),
            local_kwargs.pop("anchor"),
            **local_kwargs)
