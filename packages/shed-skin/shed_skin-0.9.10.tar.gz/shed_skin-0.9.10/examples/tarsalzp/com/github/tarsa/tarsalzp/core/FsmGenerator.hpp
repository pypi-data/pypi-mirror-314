#ifndef __COM_GITHUB_TARSA_TARSALZP_CORE_FSMGENERATOR_HPP
#define __COM_GITHUB_TARSA_TARSALZP_CORE_FSMGENERATOR_HPP

using namespace __shedskin__;
namespace __com__ {
namespace __github__ {
namespace __tarsa__ {
namespace __tarsalzp__ {
namespace __core__ {
namespace __FsmGenerator__ {

extern str *const_0, *const_1;

class FsmGenerator;


extern str *__author__, *__name__;


extern class_ *cl_FsmGenerator;
class FsmGenerator : public pyobj {
public:
    __array__::array<__ss_int> *stateTable;
    __ss_int LimitX;
    __ss_int LimitY;
    __ss_int p;
    list<__ss_int> *freqMask;

    FsmGenerator() {}
    FsmGenerator(int __ss_init) {
        this->__class__ = cl_FsmGenerator;
        __init__();
    }
    void *__init__();
    __ss_int divisor(__ss_int a, __ss_int b);
    __ss_int repeated(__ss_int a, __ss_int b);
    __ss_int opposite(__ss_int a, __ss_int b);
    __ss_int initStates(__ss_int x, __ss_int y, __ss_int h1, __ss_int h0);
};

void __init();

} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace
#endif
