#include "builtin.hpp"
#include "time.hpp"
#include "math.hpp"
#include "re.hpp"
#include "random.hpp"
#include "sys.hpp"
#include "ml/spatialindex.hpp"
#include "ml/surfacepoint.hpp"
#include "ml/triangle.hpp"
#include "ml/raytracer.hpp"
#include "ml/camera.hpp"
#include "ml/entry.hpp"
#include "ml/vector3f.hpp"
#include "ml/scene.hpp"
#include "ml/image.hpp"

namespace __ml__ {
namespace __entry__ {

str *const_0, *const_1, *const_10, *const_11, *const_12, *const_2, *const_3, *const_4, *const_5, *const_6, *const_7, *const_8, *const_9;

using __ml__::__camera__::Camera;
using __ml__::__image__::Image;
using __ml__::__scene__::Scene;
using __math__::log10;
using __time__::time;

str *BANNER, *HELP, *MODEL_FORMAT_ID, *__name__;
__ss_int SAVE_PERIOD;
list<str *> *argv;
file *__ss_stdout;
__ss_bool __127, __128, __129;



void *save_image(str *image_file_pathname, __ml__::__image__::Image *image, __ss_int frame_no) {
    file_binary *image_file;

    image_file = open_binary(image_file_pathname, const_0);
    image->get_formatted(image_file, (frame_no-__ss_int(1)));
    image_file->close();
    return NULL;
}

void *__ss_main(str *arg) {
    str *image_file_pathname, *line, *model_file_pathname;
    file *__118, *model_file;
    __ss_int __120, __122, __123, frame_no, iterations;
    __ml__::__image__::Image *image;
    __ml__::__camera__::Camera *camera;
    __ml__::__scene__::Scene *scene;
    __ss_float last_time;
    __iter<str *> *__119;
    file::for_in_loop __121;
    __ss_bool __124, __125;

    print(__ml__::__entry__::BANNER);
    model_file_pathname = arg;
    image_file_pathname = (model_file_pathname)->__add__(const_1);
    model_file = open(model_file_pathname, const_2);
    if (__ne((next(model_file))->strip(), __ml__::__entry__::MODEL_FORMAT_ID)) {
        throw (new Exception());
    }

    FOR_IN(line,model_file,118,120,121)
        if (__NOT(line->isspace())) {
            iterations = __int(line);
            break;
        }
    END_FOR

    image = (new __ml__::__image__::Image(model_file));
    camera = (new __ml__::__camera__::Camera(model_file));
    scene = (new __ml__::__scene__::Scene(model_file, camera->view_position));
    model_file->close();
    last_time = (time()-(__ml__::__entry__::SAVE_PERIOD+__ss_int(1)));
    try {

        FAST_FOR(frame_no,__ss_int(1),(iterations+__ss_int(1)),1,122,123)
            camera->get_frame(scene, image);
            if (((((__ss_float)(__ml__::__entry__::SAVE_PERIOD))<(time()-last_time)) or (frame_no==iterations))) {
                last_time = time();
                save_image(image_file_pathname, image, frame_no);
            }
            __ml__::__entry__::__ss_stdout->write(((const_3)->__mul__(((((frame_no>__ss_int(1)))?(__int(log10((frame_no-__ss_int(1))))):((-__ss_int(1))))+__ss_int(12))))->__add__(__mod6(const_4, 1, frame_no)));
            __ml__::__entry__::__ss_stdout->flush();
        END_FOR

        print(const_5);
    } catch (KeyboardInterrupt *) {
        save_image(image_file_pathname, image, frame_no);
        print(const_6);
    }
    return NULL;
}

void __init() {
    const_0 = new str("wb");
    const_1 = new str(".ppm");
    const_2 = __char_cache[114];
    const_3 = __char_cache[8];
    const_4 = new str("iteration: %u");
    const_5 = new str("\nfinished");
    const_6 = new str("\ninterupted");
    const_7 = new str("\n  MiniLight 1.5.2 Python\n  Copyright (c) 2008, Harrison Ainsworth / HXA7241 and Juraj Sukop.\n  http://www.hxa7241.org/minilight/\n");
    const_8 = new str("\n----------------------------------------------------------------------\n  MiniLight 1.5.2 Python\n\n  Copyright (c) 2008, Harrison Ainsworth / HXA7241 and Juraj Sukop.\n  http://www.hxa7241.org/minilight/\n\n  2008-02-17\n----------------------------------------------------------------------\n\nMiniLight is a minimal global illumination renderer.\n\nusage:\n  minilight image_file_pathname\n\nThe model text file format is:\n  #MiniLight\n\n  iterations\n\n  imagewidth imageheight\n\n  viewposition viewdirection viewangle\n\n  skyemission groundreflection\n  vertex0 vertex1 vertex2 reflectivity emitivity\n  vertex0 vertex1 vertex2 reflectivity emitivity\n  ...\n\n-- where iterations and image values are ints, viewangle is a float,\nand all other values are three parenthised floats. The file must end\nwith a newline. Eg.:\n  #MiniLight\n\n  100\n\n  200 150\n\n  (0 0.75 -2) (0 0 1) 45\n\n  (3626 5572 5802) (0.1 0.09 0.07)\n  (0 0 0) (0 1 0) (1 1 0)  (0.7 0.7 0.7) (0 0 0)\n");
    const_9 = new str("#MiniLight");
    const_10 = new str("__main__");
    const_11 = new str("-?");
    const_12 = new str("--help");

    __name__ = new str("entry");

    argv = __sys__::argv;
    __ss_stdout = __sys__::__ss_stdout;
    BANNER = const_7;
    HELP = const_8;
    MODEL_FORMAT_ID = const_9;
    SAVE_PERIOD = __ss_int(180);
    if (__eq(__ml__::__entry__::__name__, const_10)) {
        if (((len(__ml__::__entry__::argv)<__ss_int(2)) or __eq(__ml__::__entry__::argv->__getfast__(__ss_int(1)), const_11) or __eq(__ml__::__entry__::argv->__getfast__(__ss_int(1)), const_12))) {
            print(__ml__::__entry__::HELP);
        }
        else {
            __ss_main(__ml__::__entry__::argv->__getfast__(__ss_int(1)));
        }
    }
}

} // module namespace
} // module namespace

