#ifndef __COM_GITHUB_TARSA_TARSALZP_PRELUDE_LONG_HPP
#define __COM_GITHUB_TARSA_TARSALZP_PRELUDE_LONG_HPP

using namespace __shedskin__;
namespace __com__ {
namespace __github__ {
namespace __tarsa__ {
namespace __tarsalzp__ {
namespace __prelude__ {
namespace __Long__ {

extern str *const_0;

class Long;


extern str *__author__, *__name__;


extern class_ *cl_Long;
class Long : public pyobj {
public:
    __ss_int a;
    __ss_int d;
    __ss_int b;
    __ss_int c;

    Long() {}
    Long(__ss_int a, __ss_int b, __ss_int c, __ss_int d) {
        this->__class__ = cl_Long;
        __init__(a, b, c, d);
    }
    void *__init__(__ss_int a, __ss_int b, __ss_int c, __ss_int d);
    void *shl8();
};

void __init();

} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace
#endif
