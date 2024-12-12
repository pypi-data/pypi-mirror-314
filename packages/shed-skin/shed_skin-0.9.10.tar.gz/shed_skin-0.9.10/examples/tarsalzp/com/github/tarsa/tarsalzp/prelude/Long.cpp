#include "builtin.hpp"
#include "com/github/tarsa/tarsalzp/prelude/Long.hpp"

namespace __com__ {
namespace __github__ {
namespace __tarsa__ {
namespace __tarsalzp__ {
namespace __prelude__ {
namespace __Long__ {

str *const_0;


str *__author__, *__name__;



/**
class Long
*/

class_ *cl_Long;

void *Long::__init__(__ss_int a, __ss_int b, __ss_int c, __ss_int d) {
    this->a = a;
    this->b = b;
    this->c = c;
    this->d = d;
    return NULL;
}

void *Long::shl8() {
    this->a = ((((this->a)&(__ss_int(255)))<<__ss_int(8))+(((this->b)&(__ss_int(65280)))>>__ss_int(8)));
    this->b = ((((this->b)&(__ss_int(255)))<<__ss_int(8))+(((this->c)&(__ss_int(65280)))>>__ss_int(8)));
    this->c = ((((this->c)&(__ss_int(255)))<<__ss_int(8))+(((this->d)&(__ss_int(65280)))>>__ss_int(8)));
    this->d = (((this->d)&(__ss_int(255)))<<__ss_int(8));
    return NULL;
}

void __init() {
    const_0 = new str("Piotr Tarsa");

    __name__ = new str("Long");

    __author__ = const_0;
    cl_Long = new class_("Long");
}

} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace

