#include "builtin.hpp"
#include "time.hpp"
#include "math.hpp"
#include "re.hpp"
#include "random.hpp"
#include "ml/spatialindex.hpp"
#include "ml/surfacepoint.hpp"
#include "ml/triangle.hpp"
#include "ml/raytracer.hpp"
#include "ml/camera.hpp"
#include "ml/vector3f.hpp"
#include "ml/scene.hpp"
#include "ml/image.hpp"

namespace __ml__ {
namespace __camera__ {

str *const_0;

using __math__::tan;
using __random__::random;
using __ml__::__raytracer__::RayTracer;
using __ml__::__vector3f__::Vector3f;
using __ml__::__vector3f__::Vector3f_str;

str *__name__;
__re__::re_object *SEARCH;
__ss_float pi;



/**
class Camera
*/

class_ *cl_Camera;

void *Camera::__init__(file *in_stream) {
    str *a, *d, *line, *p;
    file *__14;
    __iter<str *> *__15;
    __ss_int __16;
    file::for_in_loop __17;
    tuple<str *> *__18;


    FOR_IN(line,in_stream,14,16,17)
        if (__NOT(line->isspace())) {
            __18 = (__ml__::__camera__::SEARCH->search(line, __ss_int(0), (-__ss_int(1))))->groups(NULL);
            __unpack_check(__18, 3);
            p = __18->__getfast__(0);
            d = __18->__getfast__(1);
            a = __18->__getfast__(2);
            this->view_position = Vector3f_str(p);
            this->view_direction = (Vector3f_str(d))->unitize();
            if ((this->view_direction)->is_zero()) {
                this->view_direction = (new __ml__::__vector3f__::Vector3f(__ss_float(0.0), __ss_float(0.0), __ss_float(1.0)));
            }
            this->view_angle = (___min(2, (__ss_float(__ss_int(0))), ___max(2, (__ss_float(__ss_int(0))), __ss_float(10.0), __float(a)), __ss_float(160.0))*(__ml__::__camera__::pi/__ss_float(180.0)));
            this->right = (((new __ml__::__vector3f__::Vector3f(__ss_float(0.0), __ss_float(1.0), __ss_float(0.0))))->cross(this->view_direction))->unitize();
            if ((this->right)->is_zero()) {
                this->up = (new __ml__::__vector3f__::Vector3f(__ss_float(0.0), __ss_float(0.0), ((___bool((this->view_direction)->y))?(__ss_float(1.0)):((-__ss_float(1.0))))));
                this->right = ((this->up)->cross(this->view_direction))->unitize();
            }
            else {
                this->up = ((this->view_direction)->cross(this->right))->unitize();
            }
            break;
        }
    END_FOR

    return NULL;
}

void *Camera::get_frame(__ml__::__scene__::Scene *scene, __ml__::__image__::Image *image) {
    __ml__::__raytracer__::RayTracer *raytracer;
    __ss_float aspect, x_coefficient, y_coefficient;
    __ss_int __19, __20, __21, __22, x, y;
    __ml__::__vector3f__::Vector3f *offset, *radiance, *sample_direction;

    raytracer = (new __ml__::__raytracer__::RayTracer(scene));
    aspect = (__float(image->height)/__float(image->width));

    FAST_FOR(y,0,image->height,1,19,20)

        FAST_FOR(x,0,image->width,1,21,22)
            x_coefficient = ((((x+random())*__ss_float(2.0))/image->width)-__ss_float(1.0));
            y_coefficient = ((((y+random())*__ss_float(2.0))/image->height)-__ss_float(1.0));
            offset = ((this->right)->__mul__(x_coefficient))->__add__((this->up)->__mul__((y_coefficient*aspect)));
            sample_direction = ((this->view_direction)->__add__((offset)->__mul__(tan((this->view_angle*__ss_float(0.5))))))->unitize();
            radiance = raytracer->get_radiance(this->view_position, sample_direction, NULL);
            image->add_to_pixel(x, y, radiance);
        END_FOR

    END_FOR

    return NULL;
}

void __init() {
    const_0 = new str("(\\(.+\\))\\s*(\\(.+\\))\\s*(\\S+)");

    __name__ = new str("camera");

    pi = __math__::pi;
    SEARCH = __re__::compile(const_0, __ss_int(0));
    cl_Camera = new class_("Camera");
}

} // module namespace
} // module namespace

