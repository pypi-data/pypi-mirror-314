#ifndef __COM_GITHUB_TARSA_TARSALZP_CORE_LG2_HPP
#define __COM_GITHUB_TARSA_TARSALZP_CORE_LG2_HPP

using namespace __shedskin__;
namespace __com__ {
namespace __github__ {
namespace __tarsa__ {
namespace __tarsalzp__ {
namespace __core__ {
namespace __Lg2__ {

extern str *const_0;

class Lg2;


extern str *__author__, *__name__;


extern class_ *cl_Lg2;
class Lg2 : public pyobj {
public:
    static list<__ss_int> *lgLut;
    static __ss_int i;
    static __ss_int __4;
    static __ss_int __5;

    Lg2() { this->__class__ = cl_Lg2; }
    static void __static__();
    static __ss_int iLog2(__ss_int value);
    static __ss_int nLog2(__ss_int value);
};

void __init();

} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace
#endif
