#ifndef __KMEANSPP_HPP
#define __KMEANSPP_HPP

using namespace __shedskin__;
namespace __kmeanspp__ {

extern str *const_0, *const_1, *const_10, *const_11, *const_2, *const_3, *const_4, *const_5, *const_6, *const_7, *const_8, *const_9;

class Point;
class Color;


extern str *__name__;
extern __ss_float FLOAT_MAX, pi;


extern class_ *cl_Point;
class Point : public pyobj {
public:
    static list<str *> *__slots__;

    __ss_int group;
    __ss_float x;
    __ss_float y;

    Point() {}
    Point(__ss_float x, __ss_float y, __ss_int group) {
        this->__class__ = cl_Point;
        __init__(x, y, group);
    }
    static void __static__();
    void *__init__(__ss_float x, __ss_float y, __ss_int group);
    Point *__copy__();
};

extern class_ *cl_Color;
class Color : public pyobj {
public:
    __ss_float b;
    __ss_float g;
    __ss_float r;

    Color() {}
    Color(__ss_float r, __ss_float g, __ss_float b) {
        this->__class__ = cl_Color;
        __init__(r, g, b);
    }
    void *__init__(__ss_float r, __ss_float g, __ss_float b);
};

list<Point *> *generate_points(__ss_int npoints, __ss_int radius);
__ss_float sqr_distance_2D(Point *a, Point *b);
tuple2<__ss_int, __ss_float> *nearest_cluster_center(Point *point, list<Point *> *cluster_centers);
void *kpp(list<Point *> *points, list<Point *> *cluster_centers);
list<Point *> *lloyd(list<Point *> *points, __ss_int nclusters);
void *print_eps(list<Point *> *points, list<Point *> *cluster_centers, __ss_int W, __ss_int H);
void *__ss_main();

} // module namespace
#endif
