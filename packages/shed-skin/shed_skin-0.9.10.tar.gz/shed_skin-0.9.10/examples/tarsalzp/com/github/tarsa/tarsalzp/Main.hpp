#ifndef __COM_GITHUB_TARSA_TARSALZP_MAIN_HPP
#define __COM_GITHUB_TARSA_TARSALZP_MAIN_HPP

using namespace __shedskin__;

namespace __com__ { /* XXX */
namespace __github__ { /* XXX */
namespace __tarsa__ { /* XXX */
namespace __tarsalzp__ { /* XXX */
namespace __Options__ { /* XXX */
class Options;
}
}
}
}
}
namespace __com__ { /* XXX */
namespace __github__ { /* XXX */
namespace __tarsa__ { /* XXX */
namespace __tarsalzp__ { /* XXX */
namespace __prelude__ { /* XXX */
namespace __Streams__ { /* XXX */
class BufferedInputStream;
class BufferedOutputStreamWrapper;
class OutputStream;
class FileOutputStream;
class DelayedFileOutputStream;
}
}
}
}
}
}
namespace __com__ {
namespace __github__ {
namespace __tarsa__ {
namespace __tarsalzp__ {
namespace __Main__ {

extern str *const_0, *const_1, *const_10, *const_11, *const_12, *const_13, *const_14, *const_15, *const_16, *const_17, *const_18, *const_19, *const_2, *const_20, *const_21, *const_22, *const_23, *const_24, *const_25, *const_26, *const_27, *const_28, *const_29, *const_3, *const_30, *const_31, *const_32, *const_33, *const_34, *const_35, *const_36, *const_37, *const_38, *const_39, *const_4, *const_40, *const_41, *const_42, *const_43, *const_44, *const_45, *const_5, *const_6, *const_7, *const_8, *const_9;

class Main;


extern str *__author__, *__name__;
extern file *__ss_stderr;


extern class_ *cl_Main;
class Main : public pyobj {
public:

    Main() { this->__class__ = cl_Main; }
    void *err(str *string);
    void *printHelp();
    dict<str *, str *> *convertOptions(list<str *> *args);
    void *encode(dict<str *, str *> *optionsMap);
    void *decode(dict<str *, str *> *optionsMap);
    void *showOptions(dict<str *, str *> *optionsMap);
    void *dispatchCommand(list<str *> *args);
    void *run(list<str *> *args);
    void *__ss_main();
};

void __init();

} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace
#endif
