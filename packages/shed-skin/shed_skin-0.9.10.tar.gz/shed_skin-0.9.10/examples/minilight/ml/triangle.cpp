#include "builtin.hpp"
#include "time.hpp"
#include "re.hpp"
#include "math.hpp"
#include "random.hpp"
#include "ml/triangle.hpp"
#include "ml/vector3f.hpp"

namespace __ml__ {
namespace __triangle__ {

str *const_0;

using __math__::sqrt;
using __random__::random;
using __ml__::__vector3f__::Vector3f_str;

str *__name__;
__re__::re_object *SEARCH;
__ss_float TOLERANCE;
__ml__::__vector3f__::Vector3f *MAX, *ONE, *ZERO;



/**
class Triangle
*/

class_ *cl_Triangle;

void *Triangle::__init__(file *in_stream) {
    str *e, *line, *r, *v0, *v1, *v2;
    __ml__::__vector3f__::Vector3f *edge1, *pa2;
    file *__45;
    __iter<str *> *__46;
    __ss_int __47;
    file::for_in_loop __48;
    tuple<str *> *__49;


    FOR_IN(line,in_stream,45,47,48)
        if (__NOT(line->isspace())) {
            __49 = (__ml__::__triangle__::SEARCH->search(line, __ss_int(0), (-__ss_int(1))))->groups(NULL);
            __unpack_check(__49, 5);
            v0 = __49->__getfast__(0);
            v1 = __49->__getfast__(1);
            v2 = __49->__getfast__(2);
            r = __49->__getfast__(3);
            e = __49->__getfast__(4);
            this->vertexs = (new list<__ml__::__vector3f__::Vector3f *>(3,Vector3f_str(v0),Vector3f_str(v1),Vector3f_str(v2)));
            this->edge0 = (Vector3f_str(v1))->__sub__(Vector3f_str(v0));
            this->edge3 = (Vector3f_str(v2))->__sub__(Vector3f_str(v0));
            this->reflectivity = (Vector3f_str(r))->clamped(__ml__::__triangle__::ZERO, __ml__::__triangle__::ONE);
            this->emitivity = (Vector3f_str(e))->clamped(__ml__::__triangle__::ZERO, __ml__::__triangle__::MAX);
            edge1 = (Vector3f_str(v2))->__sub__(Vector3f_str(v1));
            this->tangent = (this->edge0)->unitize();
            this->normal = ((this->tangent)->cross(edge1))->unitize();
            pa2 = (this->edge0)->cross(edge1);
            this->area = (sqrt(pa2->dot(pa2))*__ss_float(0.5));
            return NULL;
        }
    END_FOR

    throw (new StopIteration());
}

list<__ss_float> *Triangle::get_bound() {
    __ml__::__vector3f__::Vector3f *v2;
    list<__ss_float> *__52, *__54, *bound;
    __ss_int __50, __51, __53, __55, j;
    __ss_float v0, v1;

    v2 = (this->vertexs)->__getfast__(__ss_int(2));
    bound = (new list<__ss_float>(6,v2->x,v2->y,v2->z,v2->x,v2->y,v2->z));

    FAST_FOR(j,0,__ss_int(3),1,50,51)
        v0 = ((this->vertexs)->__getfast__(__ss_int(0)))->__getitem__(j);
        v1 = ((this->vertexs)->__getfast__(__ss_int(1)))->__getitem__(j);
        if ((v0<v1)) {
            if ((v0<bound->__getfast__(j))) {
                bound->__setitem__(j, v0);
            }
            if ((v1>bound->__getfast__((j+__ss_int(3))))) {
                bound->__setitem__((j+__ss_int(3)), v1);
            }
        }
        else {
            if ((v1<bound->__getfast__(j))) {
                bound->__setitem__(j, v1);
            }
            if ((v0>bound->__getfast__((j+__ss_int(3))))) {
                bound->__setitem__((j+__ss_int(3)), v0);
            }
        }
        __52 = bound;
        __53 = j;
        __52->__setitem__(__53, (__52->__getfast__(__53)-((__abs(bound->__getfast__(j))+__ss_float(1.0))*__ml__::__triangle__::TOLERANCE)));
        __54 = bound;
        __55 = (j+__ss_int(3));
        __54->__setitem__(__55, (__54->__getfast__(__55)+((__abs(bound->__getfast__((j+__ss_int(3))))+__ss_float(1.0))*__ml__::__triangle__::TOLERANCE)));
    END_FOR

    return bound;
}

__ss_float Triangle::get_intersection(__ml__::__vector3f__::Vector3f *ray_origin, __ml__::__vector3f__::Vector3f *ray_direction) {
    __ss_float det, e1x, e1y, e1z, e2x, e2y, e2z, inv_det, pvx, pvy, pvz, qvx, qvy, qvz, t, tvx, tvy, tvz, u, v;
    __ml__::__vector3f__::Vector3f *v0;

    e1x = (this->edge0)->x;
    e1y = (this->edge0)->y;
    e1z = (this->edge0)->z;
    e2x = (this->edge3)->x;
    e2y = (this->edge3)->y;
    e2z = (this->edge3)->z;
    pvx = ((ray_direction->y*e2z)-(ray_direction->z*e2y));
    pvy = ((ray_direction->z*e2x)-(ray_direction->x*e2z));
    pvz = ((ray_direction->x*e2y)-(ray_direction->y*e2x));
    det = (((e1x*pvx)+(e1y*pvy))+(e1z*pvz));
    if (((-__ss_float(1e-06))<det)&&(det<__ss_float(1e-06))) {
        return (-__ss_float(1.0));
    }
    inv_det = (__ss_float(1.0)/det);
    v0 = (this->vertexs)->__getfast__(__ss_int(0));
    tvx = (ray_origin->x-v0->x);
    tvy = (ray_origin->y-v0->y);
    tvz = (ray_origin->z-v0->z);
    u = ((((tvx*pvx)+(tvy*pvy))+(tvz*pvz))*inv_det);
    if ((u<__ss_float(0.0))) {
        return (-__ss_float(1.0));
    }
    else if ((u>__ss_float(1.0))) {
        return (-__ss_float(1.0));
    }
    qvx = ((tvy*e1z)-(tvz*e1y));
    qvy = ((tvz*e1x)-(tvx*e1z));
    qvz = ((tvx*e1y)-(tvy*e1x));
    v = ((((ray_direction->x*qvx)+(ray_direction->y*qvy))+(ray_direction->z*qvz))*inv_det);
    if ((v<__ss_float(0.0))) {
        return (-__ss_float(1.0));
    }
    else if (((u+v)>__ss_float(1.0))) {
        return (-__ss_float(1.0));
    }
    t = ((((e2x*qvx)+(e2y*qvy))+(e2z*qvz))*inv_det);
    if ((t<__ss_float(0.0))) {
        return (-__ss_float(1.0));
    }
    return t;
}

__ml__::__vector3f__::Vector3f *Triangle::get_sample_point() {
    __ss_float a, b, r2, sqr1;

    sqr1 = sqrt(random());
    r2 = random();
    a = (__ss_float(1.0)-sqr1);
    b = ((__ss_float(1.0)-r2)*sqr1);
    return (((this->edge0)->__mul__(a))->__add__((this->edge3)->__mul__(b)))->__add__((this->vertexs)->__getfast__(__ss_int(0)));
}

void __init() {
    const_0 = new str("(\\(.+\\))\\s*(\\(.+\\))\\s*(\\(.+\\))\\s*(\\(.+\\))\\s*(\\(.+\\))");

    __name__ = new str("triangle");

    ZERO = __ml__::__vector3f__::ZERO;
    ONE = __ml__::__vector3f__::ONE;
    MAX = __ml__::__vector3f__::MAX;
    SEARCH = __re__::compile(const_0, __ss_int(0));
    TOLERANCE = (__ss_float(1.0)/__ss_float(1024.0));
    cl_Triangle = new class_("Triangle");
}

} // module namespace
} // module namespace

