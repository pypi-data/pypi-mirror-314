#include "builtin.hpp"
#include "time.hpp"
#include "sys.hpp"
#include "array.hpp"
#include "com/github/tarsa/tarsalzp/prelude/__init__.hpp"
#include "com/github/tarsa/tarsalzp/Main.hpp"
#include "com/github/tarsa/tarsalzp/prelude/Long.hpp"
#include "com/github/__init__.hpp"
#include "com/github/tarsa/tarsalzp/core/__init__.hpp"
#include "com/github/tarsa/tarsalzp/__init__.hpp"
#include "com/github/tarsa/tarsalzp/core/FsmGenerator.hpp"
#include "com/github/tarsa/tarsalzp/Options.hpp"
#include "com/github/tarsa/tarsalzp/prelude/Streams.hpp"
#include "tarsalzp.hpp"
#include "com/github/tarsa/tarsalzp/core/Common.hpp"
#include "com/github/tarsa/tarsalzp/core/Decoder.hpp"
#include "com/github/tarsa/tarsalzp/core/Encoder.hpp"
#include "com/github/tarsa/__init__.hpp"
#include "com/github/tarsa/tarsalzp/core/Coder.hpp"
#include "com/github/tarsa/tarsalzp/core/Lg2.hpp"
#include "com/__init__.hpp"

namespace __tarsalzp__ {

str *const_0, *const_1;

using __com__::__github__::__tarsa__::__tarsalzp__::__Main__::Main;

str *__author__, *__name__;



void __init() {
    const_0 = new str("Piotr Tarsa");
    const_1 = new str("__main__");

    __name__ = new str("__main__");

    __author__ = const_0;
    if (__eq(__tarsalzp__::__name__, const_1)) {
        ((new __com__::__github__::__tarsa__::__tarsalzp__::__Main__::Main()))->__ss_main();
    }
}

} // module namespace

int main(int __ss_argc, char **__ss_argv) {
    __shedskin__::__init();
    __com__::__init();
    __com__::__github__::__init();
    __com__::__github__::__tarsa__::__init();
    __com__::__github__::__tarsa__::__tarsalzp__::__init();
    __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__init();
    __array__::__init();
    __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::__init();
    __com__::__github__::__tarsa__::__tarsalzp__::__core__::__init();
    __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Long__::__init();
    __com__::__github__::__tarsa__::__tarsalzp__::__Options__::__init();
    __com__::__github__::__tarsa__::__tarsalzp__::__core__::__Lg2__::__init();
    __com__::__github__::__tarsa__::__tarsalzp__::__core__::__FsmGenerator__::__init();
    __com__::__github__::__tarsa__::__tarsalzp__::__core__::__Common__::__init();
    __com__::__github__::__tarsa__::__tarsalzp__::__core__::__Decoder__::__init();
    __com__::__github__::__tarsa__::__tarsalzp__::__core__::__Encoder__::__init();
    __com__::__github__::__tarsa__::__tarsalzp__::__core__::__Coder__::__init();
    __sys__::__init(__ss_argc, __ss_argv);
    __time__::__init();
    __com__::__github__::__tarsa__::__tarsalzp__::__Main__::__init();
    __shedskin__::__start(__tarsalzp__::__init);
}
