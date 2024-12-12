#ifndef __ML_ENTRY_HPP
#define __ML_ENTRY_HPP

using namespace __shedskin__;

namespace __ml__ { /* XXX */
namespace __scene__ { /* XXX */
class Scene;
}
}
namespace __ml__ { /* XXX */
namespace __vector3f__ { /* XXX */
class Vector3f;
}
}
namespace __ml__ { /* XXX */
namespace __camera__ { /* XXX */
class Camera;
}
}
namespace __ml__ { /* XXX */
namespace __image__ { /* XXX */
class Image;
}
}
namespace __ml__ {
namespace __entry__ {

extern str *const_0, *const_1, *const_10, *const_11, *const_12, *const_2, *const_3, *const_4, *const_5, *const_6, *const_7, *const_8, *const_9;



extern str *BANNER, *HELP, *MODEL_FORMAT_ID, *__name__;
extern __ss_int SAVE_PERIOD;
extern list<str *> *argv;
extern file *__ss_stdout;
extern __ss_bool __127, __128, __129;


void __init();
void *save_image(str *image_file_pathname, __ml__::__image__::Image *image, __ss_int frame_no);
void *__ss_main(str *arg);

} // module namespace
} // module namespace
#endif
