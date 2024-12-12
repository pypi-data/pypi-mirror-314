#include "builtin.hpp"
#include "random.hpp"
#include "time.hpp"
#include "math.hpp"
#include "copy.hpp"
#include "kmeanspp.hpp"

namespace __kmeanspp__ {

str *const_0, *const_1, *const_10, *const_11, *const_2, *const_3, *const_4, *const_5, *const_6, *const_7, *const_8, *const_9;

using __math__::sin;
using __math__::cos;
using __random__::random;
using __random__::choice;
using __copy__::copy;

str *__name__;
__ss_float FLOAT_MAX, pi;


static inline list<Point *> *list_comp_0(__ss_int npoints);
static inline list<__ss_float> *list_comp_1(list<Point *> *points);
static inline list<Point *> *list_comp_2(__ss_int nclusters);

static inline list<Point *> *list_comp_0(__ss_int npoints) {
    __ss_int _, __3, __4;

    list<Point *> *__ss_result = new list<Point *>();

    FAST_FOR(_,0,npoints,1,3,4)
        __ss_result->append((new Point(__ss_float(0.0), __ss_float(0.0), __ss_int(0))));
    END_FOR

    return __ss_result;
}

static inline list<__ss_float> *list_comp_1(list<Point *> *points) {
    __ss_int _, __15, __16;

    list<__ss_float> *__ss_result = new list<__ss_float>();

    FAST_FOR(_,0,len(points),1,15,16)
        __ss_result->append(__ss_float(0.0));
    END_FOR

    return __ss_result;
}

static inline list<Point *> *list_comp_2(__ss_int nclusters) {
    __ss_int _, __35, __36;

    list<Point *> *__ss_result = new list<Point *>();

    FAST_FOR(_,0,nclusters,1,35,36)
        __ss_result->append((new Point(__ss_float(0.0), __ss_float(0.0), __ss_int(0))));
    END_FOR

    return __ss_result;
}

/**
class Point
*/

class_ *cl_Point;

void *Point::__init__(__ss_float x, __ss_float y, __ss_int group) {
    __ss_float __0, __1;
    __ss_int __2;

    __0 = x;
    __1 = y;
    __2 = group;
    this->x = __0;
    this->y = __1;
    this->group = __2;
    return NULL;
}

Point *Point::__copy__() {
    Point *c = new Point();
    c->group = group;
    c->x = x;
    c->y = y;
    return c;
}

list<str *> *Point::__slots__;

void Point::__static__() {
    __slots__ = (new list<str *>(3,const_0,const_1,const_2));
}

list<Point *> *generate_points(__ss_int npoints, __ss_int radius) {
    list<Point *> *__5, *points;
    Point *p;
    __ss_float ang, r;
    __iter<Point *> *__6;
    __ss_int __7;
    list<Point *>::for_in_loop __8;

    points = list_comp_0(npoints);

    FOR_IN(p,points,5,7,8)
        r = (random()*radius);
        ang = ((random()*__ss_int(2))*__kmeanspp__::pi);
        p->x = (r*cos(ang));
        p->y = (r*sin(ang));
    END_FOR

    return points;
}

__ss_float sqr_distance_2D(Point *a, Point *b) {
    return (__power((a->x-b->x), __ss_int(2))+__power((a->y-b->y), __ss_int(2)));
}

tuple2<__ss_int, __ss_float> *nearest_cluster_center(Point *point, list<Point *> *cluster_centers) {
    /**
    Distance and index of the closest cluster center
    */
    __ss_int __12, i, min_index;
    __ss_float d, min_dist;
    Point *cc;
    tuple2<__ss_int, Point *> *__9;
    __iter<tuple2<__ss_int, Point *> *> *__10, *__11;
    list<Point *> *__13;
    __iter<tuple2<__ss_int, Point *> *>::for_in_loop __14;

    min_index = point->group;
    min_dist = __kmeanspp__::FLOAT_MAX;

    FOR_IN_ENUMERATE(cc,cluster_centers,13,12)
        i = __12;
        d = sqr_distance_2D(cc, point);
        if ((min_dist>d)) {
            min_dist = d;
            min_index = i;
        }
    END_FOR

    return (new tuple2<__ss_int, __ss_float>(2,min_index,min_dist));
}

void *kpp(list<Point *> *points, list<Point *> *cluster_centers) {
    list<__ss_float> *__29, *d;
    __ss_int __17, __18, __22, __28, __33, i, j;
    __ss_float di, sum;
    Point *p;
    tuple2<__ss_int, Point *> *__19;
    __iter<tuple2<__ss_int, Point *> *> *__20, *__21;
    list<Point *> *__23, *__31;
    __iter<tuple2<__ss_int, Point *> *>::for_in_loop __24;
    tuple2<__ss_int, __ss_float> *__25;
    __iter<tuple2<__ss_int, __ss_float> *> *__26, *__27;
    __iter<tuple2<__ss_int, __ss_float> *>::for_in_loop __30;
    __iter<Point *> *__32;
    list<Point *>::for_in_loop __34;

    cluster_centers->__setitem__(__ss_int(0), copy(choice(points)));
    d = list_comp_1(points);

    FAST_FOR(i,__ss_int(1),len(cluster_centers),1,17,18)
        sum = ((__ss_float)(__ss_int(0)));

        FOR_IN_ENUMERATE(p,points,23,22)
            j = __22;
            d->__setitem__(j, nearest_cluster_center(p, cluster_centers->__slice__(__ss_int(2), __ss_int(0), i, __ss_int(0)))->__getsecond__());
            sum = (sum+d->__getfast__(j));
        END_FOR

        sum = (sum*random());

        FOR_IN_ENUMERATE(di,d,29,28)
            j = __28;
            sum = (sum-di);
            if ((sum>((__ss_float)(__ss_int(0))))) {
                continue;
            }
            cluster_centers->__setitem__(i, copy(points->__getfast__(j)));
            break;
        END_FOR

    END_FOR


    FOR_IN(p,points,31,33,34)
        p->group = nearest_cluster_center(p, cluster_centers)->__getfirst__();
    END_FOR

    return NULL;
}

list<Point *> *lloyd(list<Point *> *points, __ss_int nclusters) {
    list<Point *> *__37, *__41, *__45, *__49, *__57, *cluster_centers;
    __ss_int __39, __43, __47, __51, __56, changed, i, lenpts10, min_i;
    Point *cc, *p;
    __iter<Point *> *__38, *__42, *__46, *__50;
    list<Point *>::for_in_loop __40, __44, __48, __52;
    tuple2<__ss_int, Point *> *__53;
    __iter<tuple2<__ss_int, Point *> *> *__54, *__55;
    __iter<tuple2<__ss_int, Point *> *>::for_in_loop __58;

    cluster_centers = list_comp_2(nclusters);
    kpp(points, cluster_centers);
    lenpts10 = (len(points)>>__ss_int(10));
    changed = __ss_int(0);

    while (True) {

        FOR_IN(cc,cluster_centers,37,39,40)
            cc->x = ((__ss_float)(__ss_int(0)));
            cc->y = ((__ss_float)(__ss_int(0)));
            cc->group = __ss_int(0);
        END_FOR


        FOR_IN(p,points,41,43,44)
            cluster_centers->__getfast__(p->group)->group = ((cluster_centers->__getfast__(p->group))->group+__ss_int(1));
            cluster_centers->__getfast__(p->group)->x = ((cluster_centers->__getfast__(p->group))->x+p->x);
            cluster_centers->__getfast__(p->group)->y = ((cluster_centers->__getfast__(p->group))->y+p->y);
        END_FOR


        FOR_IN(cc,cluster_centers,45,47,48)
            cc->x = (cc->x/cc->group);
            cc->y = (cc->y/cc->group);
        END_FOR

        changed = __ss_int(0);

        FOR_IN(p,points,49,51,52)
            min_i = nearest_cluster_center(p, cluster_centers)->__getfirst__();
            if ((min_i!=p->group)) {
                changed = (changed+__ss_int(1));
                p->group = min_i;
            }
        END_FOR

        if ((changed<=lenpts10)) {
            break;
        }
    }

    FOR_IN_ENUMERATE(cc,cluster_centers,57,56)
        i = __56;
        cc->group = i;
    END_FOR

    return cluster_centers;
}

/**
class Color
*/

class_ *cl_Color;

void *Color::__init__(__ss_float r, __ss_float g, __ss_float b) {
    this->r = r;
    this->g = g;
    this->b = b;
    return NULL;
}

void *print_eps(list<Point *> *points, list<Point *> *cluster_centers, __ss_int W, __ss_int H) {
    list<Color *> *colors;
    __ss_int __59, __60, __65, __70, __75, i;
    __ss_float __61, __62, cx, cy, max_x, max_y, min_x, min_y, scale;
    Point *cc, *p;
    list<Point *> *__63, *__71, *__73;
    __iter<Point *> *__64, *__74;
    list<Point *>::for_in_loop __66, __76;
    tuple2<__ss_int, Point *> *__67;
    __iter<tuple2<__ss_int, Point *> *> *__68, *__69;
    __iter<tuple2<__ss_int, Point *> *>::for_in_loop __72;

    colors = (new list<Color *>());

    FAST_FOR(i,0,len(cluster_centers),1,59,60)
        colors->append((new Color((__mods((__ss_int(3)*(i+__ss_int(1))), __ss_int(11))/__ss_float(11.0)), (__mods((__ss_int(7)*i), __ss_int(11))/__ss_float(11.0)), (__mods((__ss_int(9)*i), __ss_int(11))/__ss_float(11.0)))));
    END_FOR

    __61 = (-__kmeanspp__::FLOAT_MAX);
    max_x = __61;
    max_y = __61;
    __62 = __kmeanspp__::FLOAT_MAX;
    min_x = __62;
    min_y = __62;

    FOR_IN(p,points,63,65,66)
        if ((max_x<p->x)) {
            max_x = p->x;
        }
        if ((min_x>p->x)) {
            min_x = p->x;
        }
        if ((max_y<p->y)) {
            max_y = p->y;
        }
        if ((min_y>p->y)) {
            min_y = p->y;
        }
    END_FOR

    scale = ___min(2, (__ss_float(__ss_int(0))), (W/(max_x-min_x)), (H/(max_y-min_y)));
    cx = ((max_x+min_x)/__ss_int(2));
    cy = ((max_y+min_y)/__ss_int(2));
    print(__mod6(const_3, 2, (W+__ss_int(10)), (H+__ss_int(10))));
    print(__add_strs(5, const_4, const_5, const_6, const_7, const_8));

    FOR_IN_ENUMERATE(cc,cluster_centers,71,70)
        i = __70;
        print(__mod6(const_9, 3, (colors->__getfast__(i))->r, (colors->__getfast__(i))->g, (colors->__getfast__(i))->b));

        FOR_IN(p,points,73,75,76)
            if ((p->group!=i)) {
                continue;
            }
        END_FOR

        print(__mod6(const_10, 2, (((cc->x-cx)*scale)+__divs(W, __ss_int(2))), (((cc->y-cy)*scale)+__divs(H, __ss_int(2)))));
    END_FOR

    print(const_11);
    return NULL;
}

void *__ss_main() {
    __ss_int k, npoints;
    list<Point *> *cluster_centers, *points;

    npoints = __ss_int(30000);
    k = __ss_int(7);
    points = generate_points(npoints, __ss_int(10));
    cluster_centers = lloyd(points, k);
    print_eps(points, cluster_centers, __ss_int(400), __ss_int(400));
    return NULL;
}

void __init() {
    const_0 = __char_cache[120];
    const_1 = __char_cache[121];
    const_2 = new str("group");
    const_3 = new str("%%!PS-Adobe-3.0\n%%%%BoundingBox: -5 -5 %d %d");
    const_4 = new str("/l {rlineto} def /m {rmoveto} def\n");
    const_5 = new str("/c { .25 sub exch .25 sub exch .5 0 360 arc fill } def\n");
    const_6 = new str("/s { moveto -2 0 m 2 2 l 2 -2 l -2 -2 l closepath ");
    const_7 = new str("   gsave 1 setgray fill grestore gsave 3 setlinewidth");
    const_8 = new str(" 1 setgray stroke grestore 0 setgray stroke }def");
    const_9 = new str("%g %g %g setrgbcolor");
    const_10 = new str("\n0 setgray %g %g s");
    const_11 = new str("\n%%%%EOF");

    __name__ = new str("__main__");

    pi = __math__::pi;
    FLOAT_MAX = __ss_float(1e+100);
    cl_Point = new class_("Point");
    Point::__static__();
    cl_Color = new class_("Color");
    __ss_main();
}

} // module namespace

int main(int, char **) {
    __shedskin__::__init();
    __math__::__init();
    __time__::__init();
    __random__::__init();
    __copy__::__init();
    __shedskin__::__start(__kmeanspp__::__init);
}
