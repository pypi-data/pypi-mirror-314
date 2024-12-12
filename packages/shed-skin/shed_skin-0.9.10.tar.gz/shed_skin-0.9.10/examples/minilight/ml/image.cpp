#include "builtin.hpp"
#include "math.hpp"
#include "ml/vector3f.hpp"
#include "ml/image.hpp"

namespace __ml__ {
namespace __image__ {

bytes *const_0, *const_1, *const_2, *const_3;

using __math__::log10;
using __ml__::__vector3f__::Vector3f;
using __ml__::__vector3f__::Vector3f_seq;

str *__name__;
bytes *MINILIGHT_URI, *PPM_ID;
__ss_float DISPLAY_LUMINANCE_MAX, GAMMA_ENCODE;
__ml__::__vector3f__::Vector3f *RGB_LUMINANCE;



/**
class Image
*/

class_ *cl_Image;

void *Image::__init__(file *in_stream) {
    str *line;
    file *__23;
    __iter<str *> *__24;
    __ss_int __25, __27, __28;
    file::for_in_loop __26;


    FOR_IN(line,in_stream,23,25,26)
        if (__NOT(line->isspace())) {
            __27 = this->dim((line->split())->__getfast__(__ss_int(0)));
            __28 = this->dim((line->split())->__getfast__(__ss_int(1)));
            this->width = __27;
            this->height = __28;
            this->pixels = ((((new list<__ss_float>(1,__ss_float(0.0))))->__mul__(this->width))->__mul__(this->height))->__mul__(__ss_int(3));
            break;
        }
    END_FOR

    return NULL;
}

__ss_int Image::dim(str *dimension) {
    return ___min(2, __ss_int(0), ___max(2, __ss_int(0), __ss_int(1), __int(dimension)), __ss_int(10000));
}

void *Image::add_to_pixel(__ss_int x, __ss_int y, __ml__::__vector3f__::Vector3f *radiance) {
    __ss_int __34, __36, __38, index;
    __ss_bool __29, __30, __31, __32;
    list<__ss_float> *__33, *__35, *__37;

    if (((x>=__ss_int(0)) and (x<this->width) and (y>=__ss_int(0)) and (y<this->height))) {
        index = ((x+(((this->height-__ss_int(1))-y)*this->width))*__ss_int(3));
        __33 = this->pixels;
        __34 = index;
        __33->__setitem__(__34, (__33->__getfast__(__34)+radiance->x));
        __35 = this->pixels;
        __36 = (index+__ss_int(1));
        __35->__setitem__(__36, (__35->__getfast__(__36)+radiance->y));
        __37 = this->pixels;
        __38 = (index+__ss_int(2));
        __37->__setitem__(__38, (__37->__getfast__(__38)+radiance->z));
    }
    return NULL;
}

void *Image::get_formatted(file_binary *out, __ss_int iteration) {
    __ss_float channel, divider, gammaed, mapped, tonemap_scaling;
    bytes *header, *output;
    list<__ss_float> *__39;
    __iter<__ss_float> *__40;
    __ss_int __41;
    list<__ss_float>::for_in_loop __42;

    divider = (__ss_float(1.0)/((((iteration>__ss_int(0)))?(iteration):(__ss_int(0)))+__ss_int(1)));
    tonemap_scaling = this->calculate_tone_mapping(this->pixels, divider);
    header = __mod6(const_0, 4, __ml__::__image__::PPM_ID, __ml__::__image__::MINILIGHT_URI, this->width, this->height);
    out->write(header);

    FOR_IN(channel,this->pixels,39,41,42)
        mapped = ((channel*divider)*tonemap_scaling);
        gammaed = __power((((mapped>__ss_float(0.0)))?(mapped):(__ss_float(0.0))), __ml__::__image__::GAMMA_ENCODE);
        output = __mod6(const_1, 1, ___min(2, __ss_int(0), __int(((gammaed*__ss_float(255.0))+__ss_float(0.5))), __ss_int(255)));
        out->write(output);
    END_FOR

    return NULL;
}

__ss_float Image::calculate_tone_mapping(list<__ss_float> *pixels, __ss_float divider) {
    __ss_float a, b, log_mean_luminance, sum_of_logs, y;
    __ss_int __43, __44, i;

    sum_of_logs = __ss_float(0.0);

    FAST_FOR(i,0,__floordiv(len(pixels),__ss_int(3)),1,43,44)
        y = ((Vector3f_seq(pixels->__slice__(__ss_int(3), (i*__ss_int(3)), ((i*__ss_int(3))+__ss_int(3)), __ss_int(0))))->dot(__ml__::__image__::RGB_LUMINANCE)*divider);
        sum_of_logs = (sum_of_logs+log10((((y>__ss_float(0.0001)))?(y):(__ss_float(0.0001)))));
    END_FOR

    ASSERT(True, 0);
    log_mean_luminance = __power(__ss_float(10.0), (sum_of_logs/__floordiv(len(pixels),__ss_int(3))));
    a = (__ss_float(1.219)+__power((__ml__::__image__::DISPLAY_LUMINANCE_MAX*__ss_float(0.25)), __ss_float(0.4)));
    b = (__ss_float(1.219)+__power(log_mean_luminance, __ss_float(0.4)));
    return (__power((a/b), __ss_float(2.5))/__ml__::__image__::DISPLAY_LUMINANCE_MAX);
}

void __init() {
    const_0 = new bytes("%s\n# %s\n\n%u %u\n255\n");
    const_1 = new bytes("%c");
    const_2 = new bytes("P6");
    const_3 = new bytes("http://www.hxa7241.org/minilight/");

    __name__ = new str("image");

    PPM_ID = const_2;
    MINILIGHT_URI = const_3;
    DISPLAY_LUMINANCE_MAX = __ss_float(200.0);
    RGB_LUMINANCE = (new __ml__::__vector3f__::Vector3f(__ss_float(0.2126), __ss_float(0.7152), __ss_float(0.0722)));
    GAMMA_ENCODE = __ss_float(0.45);
    cl_Image = new class_("Image");
}

} // module namespace
} // module namespace

