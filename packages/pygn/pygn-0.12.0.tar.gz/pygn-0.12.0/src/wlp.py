# -*- coding: utf-8 -*-
from __future__ import absolute_import
import wlp_parser


def mkdict(infile):
    dict = {}

    tree = wlp_parser.parser.parse(
        wlp_parser.lexer.lex(infile.read()))

    for subtree in tree:
        current_key = subtree[0].getstr().strip('<>')
        if current_key not in dict:
            dict[current_key] = {}

        for key, value in subtree[1]:
            key = key.getstr()
            value = value.getstr().strip("'\"")
            dict[current_key][key] = value

    return dict
