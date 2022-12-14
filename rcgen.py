#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

holder = re.compile("\$\{([^$]+)\}")
__all__ = ["RCodeGen"]


class _TempDict:
    def __init__(self, owner, dict) -> None:
        self.owner = owner
        self.dict = dict

    def __enter__(self):
        self.owner.dict_list = [self.dict] + self.owner.dict_list

    def __exit__(self, type, value, traceback):
        self.owner.dict_list = self.owner.dict_list[1:]


class _SubHierarc:
    def __init__(self, owner, text, style="default"):
        self.owner = owner
        self.style = style
        self.owner.add(text)

    def __enter__(self):
        if self.style == "block":
            self.owner.add("{")
        self.owner.intend_level += 1

    def __exit__(self, type, value, traceback):
        self.owner.intend_level -= 1
        if self.style == "block":
            self.owner.add("}")


class RCodeGen:
    def __init__(self, filename, indent_chars="\t"):
        self.out = None
        self.dict_list = []
        self.filename = filename
        self.indent_chars = indent_chars
        self.intend_level = 0

    def _format(self, text) -> str:
        while True:
            res = holder.search(text)
            if res is None:
                return text
            else:
                for dict in self.dict_list:
                    if res.group(1) in dict:
                        sub = dict[res.group(1)]
                        break
                    else:
                        raise Exception(
                            "Substitution '%s' not set." % res.groups(1))
                text = text[:res.start()] + str(sub) + text[res.end():]

    def _write(self, text):
        self.out.write(self.indent_chars * self.intend_level + text + '\n')

    def open(self):
        self.out = open(self.filename, 'w')

    def close(self):
        self.out.close()
        self.out = None

    def add(self, text):
        self._write(self._format(text))

    def blank_line(self):
        self._write("")

    def dict(self, **dict):
        self.dict_list = [dict] + self.dict_list

    def temp_dict(self, **dict):
        return _TempDict(self, dict)

    def sub_hierarc(self, text, style):
        return _SubHierarc(self, text, style)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()
