#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

holder = re.compile("\$\{([^$]+)\}")
__all__ = ["RCodeGen"]


class RepetitiveCode:
    def __init__(self, owner, dict) -> None:
        self.owner = owner
        self.dict = dict

    def __enter__(self):
        self.owner.dict_list = [self.dict] + self.owner.dict_list

    def __exit__(self, type, value, traceback):
        self.owner.dict_list = self.owner.dict_list[1:]


class RCodeGen:
    def __init__(self, filename, indent_chars="\t"):
        self.out = None
        self.filename = filename
        self.dict_list = []
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

    def __enter__(self):
        self.open()
        return self

    def close(self):
        self.out.close()
        self.out = None

    def __exit__(self, type, value, traceback):
        self.close()

    def add(self, text):
        self._write(self._format(text))

    def blank_line(self):
        self._write("")

    def repetitive_code(self, **dict):
        return RepetitiveCode(self, dict)


class RClangGen(RCodeGen):
    def __init__(self, filename, indent_chars="  "):
        RCodeGen.__init__(self, filename, indent_chars)


class Declaration:
    def __init__(self, owner):
        pass


class Function:
    def __init__(self, owner):
        pass
