#ifndef __ML_IMAGE_HPP
#define __ML_IMAGE_HPP

using namespace __shedskin__;

namespace __ml__ { /* XXX */
namespace __vector3f__ { /* XXX */
class Vector3f;
}
}
namespace __ml__ {
namespace __image__ {

extern bytes *const_0, *const_1, *const_2, *const_3;

class Image;

typedef __ss_float (*lambda0)(void *, void *, void *, void *, void *);

extern str *__name__;
extern bytes *MINILIGHT_URI, *PPM_ID;
extern __ss_float DISPLAY_LUMINANCE_MAX, GAMMA_ENCODE;
extern __ml__::__vector3f__::Vector3f *RGB_LUMINANCE;


extern class_ *cl_Image;
class Image : public pyobj {
public:
    __ss_int height;
    __ss_int width;
    list<__ss_float> *pixels;

    Image() {}
    Image(file *in_stream) {
        this->__class__ = cl_Image;
        __init__(in_stream);
    }
    void *__init__(file *in_stream);
    __ss_int dim(str *dimension);
    void *add_to_pixel(__ss_int x, __ss_int y, __ml__::__vector3f__::Vector3f *radiance);
    void *get_formatted(file_binary *out, __ss_int iteration);
    __ss_float calculate_tone_mapping(list<__ss_float> *pixels, __ss_float divider);
};

void __init();

} // module namespace
} // module namespace
#endif
