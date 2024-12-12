#ifndef __ML_CAMERA_HPP
#define __ML_CAMERA_HPP

using namespace __shedskin__;

namespace __ml__ { /* XXX */
namespace __raytracer__ { /* XXX */
class RayTracer;
}
}
namespace __ml__ { /* XXX */
namespace __vector3f__ { /* XXX */
class Vector3f;
}
}
namespace __ml__ { /* XXX */
namespace __scene__ { /* XXX */
class Scene;
}
}
namespace __ml__ { /* XXX */
namespace __image__ { /* XXX */
class Image;
}
}
namespace __ml__ {
namespace __camera__ {

extern str *const_0;

class Camera;


extern str *__name__;
extern __re__::re_object *SEARCH;
extern __ss_float pi;


extern class_ *cl_Camera;
class Camera : public pyobj {
public:
    __ml__::__vector3f__::Vector3f *view_position;
    __ml__::__vector3f__::Vector3f *view_direction;
    __ml__::__vector3f__::Vector3f *right;
    __ss_float view_angle;
    __ml__::__vector3f__::Vector3f *up;

    Camera() {}
    Camera(file *in_stream) {
        this->__class__ = cl_Camera;
        __init__(in_stream);
    }
    void *__init__(file *in_stream);
    void *get_frame(__ml__::__scene__::Scene *scene, __ml__::__image__::Image *image);
};

void __init();

} // module namespace
} // module namespace
#endif
