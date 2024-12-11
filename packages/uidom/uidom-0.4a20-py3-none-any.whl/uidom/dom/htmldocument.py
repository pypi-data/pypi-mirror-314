# Copyright (c) 2022 uidom
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from dataclasses import dataclass, field

from uidom.dom.htmlelement import XTemplate
from uidom.dom.src import component
from uidom.dom.src.dom_tag import dom_tag
from uidom.dom.src.main import extension

__all__ = [
    # "Head", 
    # "Body", 
    "HtmlDocument"
    ]

class Head(component.Component):
    def render(self, *args, **kwargs):
        self.add(kwargs)
        self.add(*args)
        return self

class Body(component.Component):
    def render(self, *args, **kwargs):
        self.add(kwargs)
        self.add(*args)
        return self


@dataclass(eq=False)
class HtmlDocument(component.Component):
    csrf_field = "X-CSRF-TOKEN"
    ensure_csrf_token: bool = field(default=True, init=False)

    def __init__(self, *args, **kwargs):
        self.ensure_csrf_token = kwargs.pop("ensure_csrf_token", self.ensure_csrf_token)
        self.document = self
        super(HtmlDocument, self).__init__(*args, **kwargs)
        self._entry = self.body
        self._old_entry = None
    
    def __pre_render__(self, *args, **kwargs):
        # self._may_shift_Head_to_head()
        # self._may_shift_Body_to_body()
        self._may_add_xelement_to_xelement_placeholder(search_element=self.body)
        if title := self.body.get("title"):
            title = title[0]
            title_parent: dom_tag = title.parent
            if title_parent is not None:
                title_parent.remove(title)
                self.head.add(title)

        if not self.head.get("meta", charset="utf-8"):
            charset = self.html_tags.meta(charset="utf-8")
            self.head.add(charset)

        if not self.head.get("meta", name="viewport"):
            viewport_meta = self.html_tags.meta(
                name="viewport",
                content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, minimal-ui",
            )
            self.head.add(viewport_meta)

    def __enter__(self):
        super().__enter__()
        self._old_entry = self._entry
        self._entry = self._entry_with_context
        return self

    def __exit__(self, type, value, traceback):
        super().__exit__(type, value, traceback)
        self._entry = self._old_entry

    def _may_shift_Head_to_head(self):
        if head_node_list := self.body.get(tag=Head):
            # we expect only one Head element per Document
            # still for some reason if there are multiple
            # Heads in child components we handle them here
            if head_node_list:
                for head_node in head_node_list:
                    head_parent: dom_tag = head_node.parent
                    if head_parent is not None:
                        if head_parent is self.head:
                            continue
                        else:
                            head_parent.remove(head_node)
                            self.head.add(head_node)

    def _may_shift_Body_to_body(self):
        if body_node_list := self.body.get(tag=Body):
            # we expect only one Body element per Document
            # still for some reason if there are multiple
            # Body in child components we handle them here
            if body_node_list:
                for body_node in body_node_list:
                    body_parent: dom_tag = body_node.parent
                    if body_parent is not None:
                        if body_parent is self._Body_placeholder:
                            continue
                        else:
                            body_parent.remove(body_node)
                            self._Body_placeholder.add(body_node)

    def _may_add_xelement_to_xelement_placeholder(self, search_element: dom_tag):
        if xtemplate_node_list := search_element.get(XTemplate):
            # we expect many XTemplate element per Document.
            # we added XTemplate.xelement attribute to XTemplate
            # as a helper attribute to extract xelements so that we
            # can add them dynamically
            for xtemplate_node in xtemplate_node_list:
                xelement = getattr(xtemplate_node, "xelement", None)
                if xelement is not None:
                    parent = getattr(xelement, "parent", None)
                    if parent is self._xelemet_placeholder:
                        # in this case we have already added xelement to the placeholder
                        continue
                    else:
                        if parent is not None:
                            # here the xelement is not in the placeholder
                            parent.remove(xelement)
                        self._xelemet_placeholder.add(xelement)
                    self._may_add_xelement_to_xelement_placeholder(search_element=xelement)

    def __checks__(self, element):
        if self.ensure_csrf_token:
            token_element = element.get(name=self.csrf_field)
            if not token_element:
                raise AttributeError(
                    f"{self.__class__.__qualname__} {self.csrf_field} must be set"
                )
            if len(token_element) > 1:
                raise AssertionError(
                    f"{self.__class__.__qualname__} {self.csrf_field} set at multiple places"
                )
        return element

    def render(
        self, *args, head=None, body=None, common_head=None, common_body=None, **kwargs
    ):
        common_head = (
            [common_head] if not isinstance(common_head, list) else common_head
        )
        common_body = (
            [common_body] if not isinstance(common_body, list) else common_body
        )
        head = [head] if not isinstance(head, list) else head
        body = [body] if not isinstance(body, list) else body

        doc = self.html_tags.DocType("html")
        with self.html_tags.html() as self.html:
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # ^Head Section
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            with self.html_tags.head() as self.head:
                if any(head):
                    for _head_file in head:
                        if isinstance(_head_file, dom_tag):
                            self.head.add(_head_file)
                        elif isinstance(_head_file, str):
                            self.head.add(self.html_tags.link(href=_head_file))
                        elif isinstance(_head_file, dict):
                            self.head.add(self.html_tags.link(**_head_file))

                if any(common_head):
                    _ = [
                        self.head.add(_hd)
                        for _hd in common_head
                        if isinstance(_hd, dom_tag)
                    ]
            
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # $Head Section
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # ^Body Section
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            self._entry_with_context = extension.PlaceholderTag()
            self._Body_placeholder = extension.PlaceholderTag()
            self._xelemet_placeholder = extension.PlaceholderTag()
            with self.html_tags.body(
                self._entry_with_context, *args, **kwargs
            ) as self.body:
                if any(body):
                    for _body_file in body:
                        if isinstance(_body_file, dom_tag):
                            self.body.add(_body_file)
                        elif isinstance(_body_file, str):
                            self.body.add(self.html_tags.script(src=_body_file))
                        elif isinstance(_body_file, dict):
                            self.body.add(self.html_tags.script(**_body_file))

                # Body Tag Placeholder added here so that we can add elements to body
                # via Body Component
                self.body.add(self._Body_placeholder)

                # here we add xelement placeholder to body so that we can add
                # xelements definitions under it.
                self.body.add(self._xelemet_placeholder)

                if any(common_body):
                    _ = [
                        self.body.add(_bd)
                        for _bd in common_body
                        if isinstance(_bd, dom_tag)
                    ]
            
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # $Body Section
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        
        return doc, self.html

    def _render(self, sb, indent_level=1, indent_str="  ", pretty=True, xhtml=False):
        # This is creating some errors in app/_counter.py _Counter class 
        # need to look at this more thoroughly.
        # the following code doesnt works properly if 
        #
        # self._may_shift_Head_to_head()
        # self._may_shift_Body_to_body()
        #
        # are uncommented. The code follows as here...
        # from dataclasses import dataclass
        # from uidom.dom import div, Component, uniqueid, button
        # from estore.document import document

        # __all__ =  ["_Counter"]


        # class _Counter(Component):
        #     routes = ["get", "increment", "decrement"]

        #     def render(self, count):
        #         _id = next(uniqueid)
        #         with div(id=f"id_{_id}", className="inline-flex bg-slate-600 rounded-md p-2") as counter:
        #             button("-", hx_get=f"/counter/decrement?count={count}", hx_target=f"#id_{_id}", hx_swap="outerHTML")
        #             div(count, className="flex px-3 py-2")
        #             button("+", hx_get=f"/counter/increment?count={count}",  hx_target=f"#id_{_id}",  hx_swap="outerHTML")
        #         return counter

        #     @staticmethod
        #     def get(count: int):
        #         return document(_Counter(count=count))

        #     @staticmethod
        #     def decrement(count: int):
        #         if count > 0:
        #             return _Counter(count=count-1)
        #         return _Counter(count=count)

        #     @staticmethod
        #     def increment(count: int):
        #         return _Counter(count=count+1)

        self.__pre_render__()
        return super()._render(sb, indent_level, indent_str, pretty, xhtml)
