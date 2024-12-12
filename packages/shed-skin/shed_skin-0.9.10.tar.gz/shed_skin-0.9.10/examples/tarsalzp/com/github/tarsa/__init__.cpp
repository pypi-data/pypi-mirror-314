#include "builtin.hpp"
#include "com/github/tarsa/__init__.hpp"

namespace __com__ {
namespace __github__ {
namespace __tarsa__ {

str *const_0;


str *__author__, *__name__;



void __init() {
    const_0 = new str("Piotr Tarsa");

    __name__ = new str("tarsa");

    __author__ = const_0;
}

} // module namespace
} // module namespace
} // module namespace

