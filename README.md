# Differentiate

## Description

A console program which takes an expression and giving you a derivative of this.

## How it works?

This program takes your expression and give you a derivative of given function. You also can choose variable using --var

## Structure

Main module: `Differentiate.py`

Modules: `Parser.py`, `Exceptions.py`, `Constants.py`, `Functions.py`, `Function_Parser.py`

Tests: `test_parser.py`, `test_differentiate.py`

## How to boot

`python Differentiate.py --var x '(x-y)(x+y)'`

Also! ' - is obligation. Without them it can work incorrect (for example, when it starts with minus)
