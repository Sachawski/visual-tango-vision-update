#!/usr/bin/python3
# -*- coding: utf-8 -*-
"Module implementing the pose of a dancer."
from enum import Enum
from typing import TypeVar,Sequence

class LenError(Exception):
    """ Exception if there is too many points in the bodypose"""


class BodyPose:

    def __init__(self,l) -> None:
        self._landmarks_dict  = {}
        if isinstance(l,list):
            for elem in l:
                self.add(elem)
        elif isinstance(l,dict):
            self._landmarks_dict = l

    def add(self,l):
        self._landmarks_dict[l[0]]=l[1:3]

    def __len__(self):
        return len(self._landmark_dict)

    def __getitem__(self,key) :
        return self._landmark_dict[key]

    def __setitem__(self,key,pts) :
        if key <= 32:
            self._landmark_dict[key] = pts

    def __delitem__(self, key):
        del self._landmark_dict[key]

    def __iter__(self) -> None:
        for bp in self._landmark_dict :
            yield bp

    def __str__(self):
        string = "{"
        for key,value in self._landmarks_dict:
            string += f"{key},{value};"
        string = string[:-1] + "}"
        return string

    def __repr__(self):
        string = "CodeBinaire({"
        for key,value in self._landmarks_dict:
            string += f"{key},{value};"
        string = string[:-1] + "})"
        return string
