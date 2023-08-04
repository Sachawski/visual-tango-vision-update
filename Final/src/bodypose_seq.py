#!/usr/bin/python3
# -*- coding: utf-8 -*-
"Module implementing a sequence of BodyPose"
from enum import Enum
from typing import TypeVar,Sequence
from BodyPoseDetection.bodypose import BodyPose

class TypeError(Exception):
    """ Exception over the element we are trying to add in the sequence"""

class SequenceBodyPose:

    def __init__(self):
        self._bp_list = []

    def add(self,bp):
        self._bp_list.append(bp)

    def __len__(self):
        return len(self._bp_list)

    def __getitem__(self,indice_or_slice) :
        if isinstance(indice_or_slice,slice):
            return SequenceBodyPose(*self._bp_list[indice_or_slice])
        return self._bp_list[indice_or_slice]

    def __setitem__(self,indice_or_slice, bp_ou_bps) :
        if isinstance(bp_ou_bps, BodyPose) and isinstance(indice_or_slice, int):
            self._bp_list[indice_or_slice] = bp_ou_bps
        elif isinstance(indice_or_slice, slice):
            if isinstance(bp_ou_bps,SequenceBodyPose):
                self._bp_list[indice_or_slice] = bp_ou_bps._bp_list
            elif isinstance(bp_ou_bps, list) or isinstance(bp_ou_bps, tuple):
                for bp in bp_ou_bps:
                    if not isinstance(bp,BodyPose):
                        raise TypeErreur("Elements must be BodyPose")
                self._bp_list[indice_or_slice] = bp_ou_bps
        else :
            print("Error !")

    def __delitem__(self, indice_or_slice):
        del self._bp_list[indice_or_slice]

    def __iter__(self) -> None:
        for bp in self._bp_list :
            yield bp

    def __add__(self,autre):
        if isinstance(autre,SequenceBodyPose) or isinstance(autre,BodyPose):
            return SequenceBodyPose(*self._bp_list,*autre._bp_list)
        else:
            raise TypeError("Pas le bon type")    

    def __str__(self):
        string = ""
        for values in self._bp_list:
            string += f"{values.array_repr}"
        return string

    def __repr__(self):
        string = "CodeBinaire("
        for value in self._bp_list:
            string += f"{value.array_repr},"
        string = string[:-1] + ")"
        return string
