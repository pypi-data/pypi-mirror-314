# -*- coding: utf-8 -*-
from copy import copy
from pathlib import Path


class Node:
    def __new__(cls, *args, **kwargs):
        # override class attributes with instance attributes
        self = super().__new__(cls)
        for key, value in cls.__dict__.items():  # class attributes
            if isinstance(value, Node):
                setattr(self, key, copy(value))  # instance attributes
        return self

    def __init__(self, path, chroot=False):
        if isinstance(path, str):
            path = Path(path)
        self.path = path
        if chroot:
            self.chroot()

    def __copy__(self):
        return self.__class__(self.path)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.path}')"

    def __str__(self):
        return str(self.path)

    def chroot(self, root=None):
        raise NotImplementedError

    def check(self):
        raise NotImplementedError

    def touch(self):
        raise NotImplementedError


class File(Node):
    def chroot(self, root=None):
        if root is not None:
            self.path = root / self.path
        return self

    def check(self):
        if not self.path.exists():
            raise FileNotFoundError(f'No such file or directory: {self.path}')
        return self

    def touch(self):
        self.path.touch(exist_ok=True)
        return self


class Dir(Node):

    def subs(self):
        values = []
        for key in dir(self):
            value = getattr(self, key)
            if isinstance(value, Node):
                values.append(value)
        return values

    def chroot(self, root=None):
        if root is not None:
            self.path = root / self.path
        for sub in self.subs():
            sub.chroot(self.path)
        return self

    def check(self):
        if not self.path.exists():
            raise FileNotFoundError(f'No such file or directory: {self.path}')
        for sub in self.subs():
            sub.check()
        return self

    def mkdir(self):
        self.path.mkdir(parents=True, exist_ok=True)
        for sub in self.subs():
            if isinstance(sub, Dir):
                sub.mkdir()
        return self

    def touch(self):
        for sub in self.subs():
            sub.touch()
        return self
