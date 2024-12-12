#include "builtin.hpp"
#include "com/__init__.hpp"

namespace __com__ {

str *const_0;


str *__author__, *__name__;



void __init() {
    const_0 = new str("Piotr Tarsa");

    __name__ = new str("com");

    __author__ = const_0;
}

} // module namespace

