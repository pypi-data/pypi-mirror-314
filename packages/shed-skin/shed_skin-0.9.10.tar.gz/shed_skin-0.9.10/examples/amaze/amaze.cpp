#include "builtin.hpp"
#include "random.hpp"
#include "time.hpp"
#include "math.hpp"
#include "amaze.hpp"

/**
Amaze - A completely object-oriented Pythonic maze generator/solver.
This can generate random mazes and solve them. It should be
able to solve any kind of maze and inform you in case a maze is
unsolveable.
This uses a very simple representation of a mze. A maze is
represented as an mxn matrix with each point value being either
0 or 1. Points with value 0 represent paths and those with
value 1 represent blocks. The problem is to find a path from
point A to point B in the matrix.
The matrix is represented internally as a list of lists.
Have fun :-)
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/496884
*/

namespace __amaze__ {

str *const_0, *const_1, *const_10, *const_11, *const_12, *const_13, *const_14, *const_15, *const_16, *const_17, *const_18, *const_19, *const_2, *const_20, *const_21, *const_22, *const_23, *const_24, *const_25, *const_26, *const_27, *const_28, *const_29, *const_3, *const_4, *const_5, *const_6, *const_7, *const_8, *const_9;


str *__name__;
__ss_int EXIT, FILE_, PATH, SOCKET, START, STDIN, __93, __94, x;
FilebasedMazeGame *game;
MazeSolver *solver;


__ss_int  default_0;
__ss_int  default_1;
list<list<__ss_int> *> * default_2;
str * default_3;
str * default_4;
static inline list<__ss_int> *list_comp_0(str *row);
static inline list<str *> *list_comp_1(list<str *> *lines);
static inline list<__ss_int> *list_comp_2(str *line);
static inline list<__ss_int> *list_comp_3(Maze *self);
static inline list<__ss_int> *list_comp_4(list<__ss_int> *row);
static inline list<__ss_float> *list_comp_5(list<tuple<__ss_int> *> *points, MazeSolver *self);

static inline list<__ss_int> *list_comp_0(str *row) {
    str *__10, *y;
    list<str *> *__5;
    __iter<str *> *__6;
    __ss_int __7;
    list<str *>::for_in_loop __8;
    void *__9;

    list<__ss_int> *__ss_result = new list<__ss_int>();

    __5 = row->split();
    __ss_result->resize(len(__5));
    FOR_IN(y,__5,5,7,8)
        __ss_result->units[__7] = __int(y);
    END_FOR

    return __ss_result;
}

static inline list<str *> *list_comp_1(list<str *> *lines) {
    str *line;
    list<str *> *__11;
    __iter<str *> *__12;
    __ss_int __13;
    list<str *>::for_in_loop __14;

    list<str *> *__ss_result = new list<str *>();

    FOR_IN(line,lines,11,13,14)
        if (___bool(line->strip())) {
            __ss_result->append(line);
        }
    END_FOR

    return __ss_result;
}

static inline list<__ss_int> *list_comp_2(str *line) {
    str *__24, *y;
    list<str *> *__19;
    __iter<str *> *__20;
    __ss_int __21;
    list<str *>::for_in_loop __22;
    void *__23;

    list<__ss_int> *__ss_result = new list<__ss_int>();

    __19 = line->split();
    __ss_result->resize(len(__19));
    FOR_IN(y,__19,19,21,22)
        __ss_result->units[__21] = __int(y);
    END_FOR

    return __ss_result;
}

static inline list<__ss_int> *list_comp_3(Maze *self) {
    list<__ss_int> *row;
    list<list<__ss_int> *> *__33;
    __iter<list<__ss_int> *> *__34;
    __ss_int __35;
    list<list<__ss_int> *>::for_in_loop __36;

    list<__ss_int> *__ss_result = new list<__ss_int>();

    __33 = self->_rows;
    __ss_result->resize(len(__33));
    FOR_IN(row,__33,33,35,36)
        __ss_result->units[__35] = len(row);
    END_FOR

    return __ss_result;
}

static inline list<__ss_int> *list_comp_4(list<__ss_int> *row) {
    __ss_int __41, y;
    list<__ss_int> *__39;
    __iter<__ss_int> *__40;
    list<__ss_int>::for_in_loop __42;

    list<__ss_int> *__ss_result = new list<__ss_int>();

    __ss_result->resize(len(row));
    FOR_IN(y,row,39,41,42)
        __ss_result->units[__41] = ___min(2, __ss_int(0), __int(y), __ss_int(1));
    END_FOR

    return __ss_result;
}

static inline list<__ss_float> *list_comp_5(list<tuple<__ss_int> *> *points, MazeSolver *self) {
    tuple<__ss_int> *point;
    list<tuple<__ss_int> *> *__78;
    __iter<tuple<__ss_int> *> *__79;
    __ss_int __80;
    list<tuple<__ss_int> *>::for_in_loop __81;

    list<__ss_float> *__ss_result = new list<__ss_float>();

    __ss_result->resize(len(points));
    FOR_IN(point,points,78,80,81)
        __ss_result->units[__80] = (self->maze)->calcDistance(point, self->_end);
    END_FOR

    return __ss_result;
}

/**
class MazeReaderException
*/

class_ *cl_MazeReaderException;

void MazeReaderException::__static__() {
}

/**
class MazeReader
*/

class_ *cl_MazeReader;

void *MazeReader::__init__() {
    this->maze_rows = (new list<list<__ss_int> *>());
    return NULL;
}

void *MazeReader::readStdin() {
    str *data, *h1, *row, *w1;
    __ss_int __1, __2, __3, __4, h, w, x;
    list<__ss_int> *rowsplit;
    list<str *> *__0;

    print(const_0);
    print(const_1);
    print();
    data = input(const_2);
    __0 = data->split();
    __unpack_check(__0, 2);
    w1 = __0->__getfast__(0);
    h1 = __0->__getfast__(1);
    __1 = __int(w1);
    __2 = __int(h1);
    w = __1;
    h = __2;

    FAST_FOR(x,0,h,1,3,4)
        row = const_3;

        while (__NOT(___bool(row))) {
            row = input(__mod6(const_4, 1, (x+__ss_int(1))));
        }
        rowsplit = list_comp_0(row);
        if ((len(rowsplit)!=w)) {
            throw ((new MazeReaderException(const_5)));
        }
        (this->maze_rows)->append(rowsplit);
    END_FOR

    return NULL;
}

void *MazeReader::readFile() {
    str *fname, *line;
    file *f;
    list<str *> *__15, *lines;
    __ss_int __17, w;
    list<__ss_int> *row;
    __iter<str *> *__16;
    list<str *>::for_in_loop __18;

    fname = const_6;
    try {
        f = open(fname);
        lines = f->readlines();
        f->close();
        lines = list_comp_1(lines);
        w = len((lines->__getfast__(__ss_int(0)))->split());

        FOR_IN(line,lines,15,17,18)
            row = list_comp_2(line);
            if ((len(row)!=w)) {
                throw ((new MazeReaderException(const_7)));
            }
            else {
                (this->maze_rows)->append(row);
            }
        END_FOR

    } catch (OSError *e) {
        throw ((new MazeReaderException(__str(e))));
    }
    return NULL;
}

list<list<__ss_int> *> *MazeReader::getData() {
    return this->maze_rows;
}

list<list<__ss_int> *> *MazeReader::readMaze(__ss_int source) {
    if ((source==__amaze__::STDIN)) {
        this->readStdin();
    }
    else if ((source==__amaze__::FILE_)) {
        this->readFile();
    }
    return this->getData();
}

/**
class MazeFactory
*/

class_ *cl_MazeFactory;

Maze *MazeFactory::makeMaze(__ss_int source) {
    MazeReader *reader;

    reader = (new MazeReader(1));
    return (new Maze(reader->readMaze(source)));
}

/**
class MazeError
*/

class_ *cl_MazeError;

void MazeError::__static__() {
}

/**
class Maze
*/

class_ *cl_Maze;

void *Maze::__init__(list<list<__ss_int> *> *rows) {
    this->_rows = rows;
    this->__validate();
    this->__normalize();
    return NULL;
}

str *Maze::__str__() {
    str *s, *sitem;
    list<__ss_int> *__29, *row;
    __ss_int __27, __31, item;
    list<list<__ss_int> *> *__25;
    __iter<list<__ss_int> *> *__26;
    list<list<__ss_int> *>::for_in_loop __28;
    __iter<__ss_int> *__30;
    list<__ss_int>::for_in_loop __32;

    s = const_8;

    FOR_IN(row,this->_rows,25,27,28)

        FOR_IN(item,row,29,31,32)
            if ((item==__amaze__::PATH)) {
                sitem = const_9;
            }
            else if ((item==__amaze__::START)) {
                sitem = const_10;
            }
            else if ((item==__amaze__::EXIT)) {
                sitem = const_11;
            }
            else {
                sitem = __str(item);
            }
            s = (const_3)->join((new tuple<str *>(4,s,const_12,sitem,const_13)));
        END_FOR

        s = (const_3)->join((new tuple<str *>(2,s,const_14)));
    END_FOR

    return s;
}

void *Maze::__validate() {
    __ss_int width;
    list<__ss_int> *widths;

    width = len((this->_rows)->__getfast__(__ss_int(0)));
    widths = list_comp_3(this);
    if ((widths->count(width)!=len(widths))) {
        throw ((new MazeError(const_15)));
    }
    this->_height = len(this->_rows);
    this->_width = width;
    return NULL;
}

void *Maze::__normalize() {
    __ss_int __37, __38, x;
    list<__ss_int> *row;
    list<list<__ss_int> *> *__43;


    FAST_FOR(x,0,len(this->_rows),1,37,38)
        row = (this->_rows)->__getfast__(x);
        row = list_comp_4(row);
        this->_rows->__setitem__(x, row);
    END_FOR

    return NULL;
}

void *Maze::validatePoint(tuple<__ss_int> *pt) {
    __ss_int h, w, x, y;
    tuple<__ss_int> *__44;
    __ss_bool __45, __46, __47, __48;

    __44 = pt;
    list<__ss_int > *__44_list = new list<__ss_int >(__44);
    __unpack_check(__44_list, 2);
    x = __44_list->__getitem__(0);
    y = __44_list->__getitem__(1);
    w = this->_width;
    h = this->_height;
    if (((x>(w-__ss_int(1))) or (x<__ss_int(0)))) {
        throw ((new MazeError(const_16)));
    }
    if (((y>(h-__ss_int(1))) or (y<__ss_int(0)))) {
        throw ((new MazeError(const_17)));
    }
    return NULL;
}

__ss_int Maze::getItem(__ss_int x, __ss_int y) {
    __ss_int h, w;
    list<__ss_int> *row;

    this->validatePoint((new tuple<__ss_int>(2,x,y)));
    w = this->_width;
    h = this->_height;
    row = (this->_rows)->__getfast__(((h-y)-__ss_int(1)));
    return row->__getfast__(x);
}

void *Maze::setItem(__ss_int x, __ss_int y, __ss_int value) {
    __ss_int h;
    list<__ss_int> *row;

    h = this->_height;
    this->validatePoint((new tuple<__ss_int>(2,x,y)));
    row = (this->_rows)->__getfast__(((h-y)-__ss_int(1)));
    row->__setitem__(x, value);
    return NULL;
}

list<tuple<__ss_int> *> *Maze::getNeighBours(tuple<__ss_int> *pt) {
    __ss_int __53, h, w, x, xx, y, yy;
    tuple<tuple<__ss_int> *> *__51, *poss_nbors;
    list<tuple<__ss_int> *> *nbors;
    tuple<__ss_int> *__49, *__50;
    __iter<tuple<__ss_int> *> *__52;
    tuple<tuple<__ss_int> *>::for_in_loop __54;
    __ss_bool __55, __56, __57, __58, __59, __60;

    this->validatePoint(pt);
    __49 = pt;
    list<__ss_int > *__49_list = new list<__ss_int >(__49);
    __unpack_check(__49_list, 2);
    x = __49_list->__getitem__(0);
    y = __49_list->__getitem__(1);
    h = this->_height;
    w = this->_width;
    poss_nbors = (new tuple<tuple<__ss_int> *>(8,(new tuple<__ss_int>(2,(x-__ss_int(1)),y)),(new tuple<__ss_int>(2,(x-__ss_int(1)),(y+__ss_int(1)))),(new tuple<__ss_int>(2,x,(y+__ss_int(1)))),(new tuple<__ss_int>(2,(x+__ss_int(1)),(y+__ss_int(1)))),(new tuple<__ss_int>(2,(x+__ss_int(1)),y)),(new tuple<__ss_int>(2,(x+__ss_int(1)),(y-__ss_int(1)))),(new tuple<__ss_int>(2,x,(y-__ss_int(1)))),(new tuple<__ss_int>(2,(x-__ss_int(1)),(y-__ss_int(1))))));
    nbors = (new list<tuple<__ss_int> *>());

    FOR_IN(__50,poss_nbors,51,53,54)
        __50 = __50;
        __unpack_check(__50, 2);
        xx = __50->__getfirst__();
        yy = __50->__getsecond__();
        if ((((xx>=__ss_int(0)) and (xx<=(w-__ss_int(1)))) and ((yy>=__ss_int(0)) and (yy<=(h-__ss_int(1)))))) {
            nbors->append((new tuple<__ss_int>(2,xx,yy)));
        }
    END_FOR

    return nbors;
}

list<tuple<__ss_int> *> *Maze::getExitPoints(tuple<__ss_int> *pt) {
    list<tuple<__ss_int> *> *__62, *exits;
    __ss_int __64, xx, yy;
    tuple<__ss_int> *__61;
    __iter<tuple<__ss_int> *> *__63;
    list<tuple<__ss_int> *>::for_in_loop __65;
    void *__66;
    Maze *__67;

    exits = (new list<tuple<__ss_int> *>());

    FOR_IN(__61,this->getNeighBours(pt),62,64,65)
        __61 = __61;
        __unpack_check(__61, 2);
        xx = __61->__getfirst__();
        yy = __61->__getsecond__();
        if ((this->getItem(xx, yy)==__ss_int(0))) {
            exits->append((new tuple<__ss_int>(2,xx,yy)));
        }
    END_FOR

    return exits;
}

__ss_float Maze::calcDistance(tuple<__ss_int> *pt1, tuple<__ss_int> *pt2) {
    __ss_int x1, x2, y1, y2;
    tuple<__ss_int> *__68, *__69;

    this->validatePoint(pt1);
    this->validatePoint(pt2);
    __68 = pt1;
    __unpack_check(__68, 2);
    x1 = __68->__getfirst__();
    y1 = __68->__getsecond__();
    __69 = pt2;
    __unpack_check(__69, 2);
    x2 = __69->__getfirst__();
    y2 = __69->__getsecond__();
    return __power((__power((x1-x2), __ss_int(2))+__power((y1-y2), __ss_int(2))), __ss_float(0.5));
}

/**
class MazeSolver
*/

class_ *cl_MazeSolver;

void *MazeSolver::__init__(Maze *maze) {
    this->maze = maze;
    this->_start = (new tuple<__ss_int>(2,__ss_int(0),__ss_int(0)));
    this->_end = (new tuple<__ss_int>(2,__ss_int(0),__ss_int(0)));
    this->_current = (new tuple<__ss_int>(2,__ss_int(0),__ss_int(0)));
    this->_steps = __ss_int(0);
    this->_path = (new list<tuple<__ss_int> *>());
    this->_tryalternate = False;
    this->_trynextbest = False;
    this->_disputed = (new tuple<__ss_int>(2,__ss_int(0),__ss_int(0)));
    this->_loops = __ss_int(0);
    this->_retrace = False;
    this->_numretraces = __ss_int(0);
    return NULL;
}

void *MazeSolver::setStartPoint(tuple<__ss_int> *pt) {
    (this->maze)->validatePoint(pt);
    this->_start = pt;
    return NULL;
}

void *MazeSolver::setEndPoint(tuple<__ss_int> *pt) {
    (this->maze)->validatePoint(pt);
    this->_end = pt;
    return NULL;
}

__ss_bool MazeSolver::boundaryCheck() {
    list<tuple<__ss_int> *> *exits1, *exits2;
    __ss_bool __70, __71;

    exits1 = (this->maze)->getExitPoints(this->_start);
    exits2 = (this->maze)->getExitPoints(this->_end);
    if (((len(exits1)==__ss_int(0)) or (len(exits2)==__ss_int(0)))) {
        return False;
    }
    return True;
}

void *MazeSolver::setCurrentPoint(tuple<__ss_int> *point) {
    this->_current = point;
    (this->_path)->append(point);
    return NULL;
}

__ss_bool MazeSolver::isSolved() {
    return ___bool(__eq(this->_current, this->_end));
}

tuple<__ss_int> *MazeSolver::getNextPoint() {
    list<tuple<__ss_int> *> *points;
    tuple<__ss_int> *point, *point2;
    __ss_bool __72, __73;

    points = (this->maze)->getExitPoints(this->_current);
    point = this->getBestPoint(points);

    while (this->checkClosedLoop(point)) {
        if (this->endlessLoop()) {
            print(this->_loops);
            point = NULL;
            break;
        }
        point2 = point;
        if ((__eq(point, this->_start) and (len(this->_path)>__ss_int(2)))) {
            this->_tryalternate = True;
            break;
        }
        else {
            point = this->getNextClosestPointNotInPath(points, point2);
            if (__NOT(___bool(point))) {
                this->retracePath();
                this->_tryalternate = True;
                point = this->_start;
                break;
            }
        }
    }
    return point;
}

void *MazeSolver::retracePath() {
    list<tuple<__ss_int> *> *path2;
    __ss_int idx;

    print(const_18);
    this->_retrace = True;
    path2 = (this->_path)->__slice__(__ss_int(0), __ss_int(0), __ss_int(0), __ss_int(0));
    path2->reverse();
    idx = path2->index(this->_start);
    this->_path = (this->_path)->__iadd__((this->_path)->__slice__(__ss_int(7), (-__ss_int(2)), idx, (-__ss_int(1))));
    this->_numretraces = (this->_numretraces+__ss_int(1));
    return NULL;
}

__ss_bool MazeSolver::endlessLoop() {
    if ((this->_loops>__ss_int(100))) {
        print(const_19);
        return True;
    }
    else if ((this->_numretraces>__ss_int(8))) {
        print(const_20);
        return True;
    }
    return False;
}

__ss_bool MazeSolver::checkClosedLoop(tuple<__ss_int> *point) {
    list<__ss_int> *__74, *l;
    __ss_int __76, x;
    __iter<__ss_int> *__75;
    list<__ss_int>::for_in_loop __77;

    l = (new list<__ss_int>(range(__ss_int(0), (len(this->_path)-__ss_int(1)), __ss_int(2))));
    l->reverse();

    FOR_IN(x,l,74,76,77)
        if (__eq((this->_path)->__getfast__(x), point)) {
            this->_loops = (this->_loops+__ss_int(1));
            return True;
        }
    END_FOR

    return False;
}

tuple<__ss_int> *MazeSolver::getBestPoint(list<tuple<__ss_int> *> *points) {
    tuple<__ss_int> *altpoint, *point, *point2;

    point = this->getClosestPoint(points);
    point2 = point;
    altpoint = point;
    if ((this->_path)->__contains__(point2)) {
        point = this->getNextClosestPointNotInPath(points, point2);
        if (__NOT(___bool(point))) {
            point = point2;
        }
    }
    if (this->_tryalternate) {
        point = this->getAlternatePoint(points, altpoint);
        print(const_21, this->_current, point);
    }
    this->_trynextbest = False;
    this->_tryalternate = False;
    this->_retrace = False;
    return point;
}

list<tuple<__ss_int> *> *MazeSolver::sortPoints(list<tuple<__ss_int> *> *points) {
    list<__ss_float> *__82, *distances, *distances2;
    list<tuple<__ss_int> *> *points2;
    __ss_int __84, count, idx;
    __ss_float dist;
    tuple<__ss_int> *point;
    __iter<__ss_float> *__83;
    list<__ss_float>::for_in_loop __85;

    distances = list_comp_5(points, this);
    distances2 = distances->__slice__(__ss_int(0), __ss_int(0), __ss_int(0), __ss_int(0));
    distances->sort(__ss_int(0), __ss_int(0), __ss_int(0));
    points2 = ((new list<tuple<__ss_int> *>(1,(new tuple<__ss_int>()))))->__mul__(len(points));
    count = __ss_int(0);

    FOR_IN(dist,distances,82,84,85)
        idx = distances2->index(dist);
        point = points->__getfast__(idx);

        while ((points2)->__contains__(point)) {
            idx = distances2->index(dist, (idx+__ss_int(1)));
            point = points->__getfast__(idx);
        }
        points2->__setitem__(count, point);
        count = (count+__ss_int(1));
    END_FOR

    return points2;
}

tuple<__ss_int> *MazeSolver::getClosestPoint(list<tuple<__ss_int> *> *points) {
    list<tuple<__ss_int> *> *points2;
    tuple<__ss_int> *closest;

    points2 = this->sortPoints(points);
    closest = points2->__getfast__(__ss_int(0));
    return closest;
}

tuple<__ss_int> *MazeSolver::getAlternatePoint(list<tuple<__ss_int> *> *points, tuple<__ss_int> *point) {
    list<tuple<__ss_int> *> *points2;

    points2 = points->__slice__(__ss_int(0), __ss_int(0), __ss_int(0), __ss_int(0));
    print(points2, point);
    points2->remove(point);
    if (___bool(points2)) {
        return __random__::choice(points2);
    }
    return NULL;
}

tuple<__ss_int> *MazeSolver::getNextClosestPoint(list<tuple<__ss_int> *> *points, tuple<__ss_int> *point) {
    list<tuple<__ss_int> *> *points2;
    __ss_int idx;

    points2 = this->sortPoints(points);
    idx = points2->index(point);
    try {
        return points2->__getfast__((idx+__ss_int(1)));
    } catch (Exception *) {
        return NULL;
    }
    return 0;
}

tuple<__ss_int> *MazeSolver::getNextClosestPointNotInPath(list<tuple<__ss_int> *> *points, tuple<__ss_int> *point) {
    tuple<__ss_int> *point2;

    point2 = this->getNextClosestPoint(points, point);

    while ((this->_path)->__contains__(point2)) {
        point2 = this->getNextClosestPoint(points, point2);
    }
    return point2;
}

void *MazeSolver::solve() {
    __ss_bool unsolvable;
    tuple<__ss_int> *pt;

    if (__eq(this->_start, this->_end)) {
        print(const_22);
        print((new list<tuple<__ss_int> *>(2,this->_start,this->_end)));
        return NULL;
    }
    if (__NOT(this->boundaryCheck())) {
        print(const_23);
        return NULL;
    }
    this->setCurrentPoint(this->_start);
    unsolvable = False;

    while (__NOT(this->isSolved())) {
        this->_steps = (this->_steps+__ss_int(1));
        pt = this->getNextPoint();
        if (___bool(pt)) {
            this->setCurrentPoint(pt);
        }
        else {
            print(const_24);
            unsolvable = True;
            break;
        }
    }
    if (__NOT(unsolvable)) {
    }
    else {
        print(const_25, this->_path);
    }
    return 0;
}

void *MazeSolver::printResult() {
    /**
    Print the maze showing the path 
    */
    __ss_int __89, x, y;
    tuple<__ss_int> *__86;
    list<tuple<__ss_int> *> *__87;
    __iter<tuple<__ss_int> *> *__88;
    list<tuple<__ss_int> *>::for_in_loop __90;


    FOR_IN(__86,this->_path,87,89,90)
        __86 = __86;
        list<__ss_int > *__86_list = new list<__ss_int >(__86);
        __unpack_check(__86_list, 2);
        x = __86_list->__getitem__(0);
        y = __86_list->__getitem__(1);
        (this->maze)->setItem(x, y, __amaze__::PATH);
    END_FOR

    (this->maze)->setItem(this->_start->__getfirst__(), this->_start->__getsecond__(), __amaze__::START);
    (this->maze)->setItem(this->_end->__getfirst__(), this->_end->__getsecond__(), __amaze__::EXIT);
    print(const_26);
    print(this->maze);
    return NULL;
}

/**
class MazeGame
*/

class_ *cl_MazeGame;

void *MazeGame::__init__() {
    ((FilebasedMazeGame *)this)->_start = (new tuple<__ss_int>(2,__ss_int(0),__ss_int(0)));
    ((FilebasedMazeGame *)this)->_end = (new tuple<__ss_int>(2,__ss_int(0),__ss_int(0)));
    return NULL;
}

MazeSolver *MazeGame::runGame() {
    Maze *maze;
    MazeSolver *solver;

    maze = ((FilebasedMazeGame *)this)->createMaze();
    if (__NOT(___bool(maze))) {
        return NULL;
    }
    ((FilebasedMazeGame *)this)->getStartEndPoints(maze);
    solver = (new MazeSolver(maze));
    solver->setStartPoint(((FilebasedMazeGame *)this)->_start);
    solver->setEndPoint(((FilebasedMazeGame *)this)->_end);
    solver->solve();
    return solver;
}

/**
class FilebasedMazeGame
*/

class_ *cl_FilebasedMazeGame;

Maze *FilebasedMazeGame::createMaze() {
    MazeFactory *f;
    Maze *m;

    f = (new MazeFactory());
    m = f->makeMaze(__amaze__::FILE_);
    return m;
}

void *FilebasedMazeGame::getStartEndPoints(Maze *maze) {
    str *pt1, *pt2, *x, *y;
    list<str *> *__91, *__92;


    while (True) {
        try {
            pt1 = const_27;
            __91 = pt1->split();
            __unpack_check(__91, 2);
            x = __91->__getfast__(0);
            y = __91->__getfast__(1);
            this->_start = (new tuple<__ss_int>(2,__int(x),__int(y)));
            maze->validatePoint(this->_start);
            break;
        } catch (Exception *) {
        }
    }

    while (True) {
        try {
            pt2 = const_28;
            __92 = pt2->split();
            __unpack_check(__92, 2);
            x = __92->__getfast__(0);
            y = __92->__getfast__(1);
            this->_end = (new tuple<__ss_int>(2,__int(x),__int(y)));
            maze->validatePoint(this->_end);
            break;
        } catch (Exception *) {
        }
    }
    return NULL;
}

void __init() {
    const_0 = new str("Enter a maze");
    const_1 = new str("You can enter a maze row by row");
    const_2 = new str("Enter the dimension of the maze as Width X Height: ");
    const_3 = new str("");
    const_4 = new str("Enter row number %d: ");
    const_5 = new str("invalid size of maze row");
    const_6 = new str("testdata/maze.txt");
    const_7 = new str("Invalid maze file - error in maze dimensions");
    const_8 = __char_cache[10];
    const_9 = __char_cache[42];
    const_10 = __char_cache[83];
    const_11 = __char_cache[69];
    const_12 = new str("  ");
    const_13 = new str("   ");
    const_14 = new str("\n\n");
    const_15 = new str("Invalid maze!");
    const_16 = new str("x co-ordinate out of range!");
    const_17 = new str("y co-ordinate out of range!");
    const_18 = new str("Retracing...");
    const_19 = new str("Seems to be hitting an endless loop.");
    const_20 = new str("Seem to be retracing loop.");
    const_21 = new str("Trying alternate...");
    const_22 = new str("Start/end points are the same. Trivial maze.");
    const_23 = new str("Either start/end point are unreachable. Maze cannot be solved.");
    const_24 = new str("Dead-lock - maze unsolvable");
    const_25 = new str("Path till deadlock is");
    const_26 = new str("Maze with solution path");
    const_27 = new str("0 4");
    const_28 = new str("5 4");
    const_29 = new str("__main__");

    __name__ = new str("__main__");

    cl_MazeReaderException = new class_("MazeReaderException");
    MazeReaderException::__static__();
    STDIN = __ss_int(0);
    FILE_ = __ss_int(1);
    SOCKET = __ss_int(2);
    PATH = (-__ss_int(1));
    START = (-__ss_int(2));
    EXIT = (-__ss_int(3));
    default_0 = __amaze__::STDIN;
    cl_MazeReader = new class_("MazeReader");
    default_1 = __amaze__::STDIN;
    cl_MazeFactory = new class_("MazeFactory");
    cl_MazeError = new class_("MazeError");
    MazeError::__static__();
    default_2 = (new list<list<__ss_int> *>(1,(new list<__ss_int>())));
    cl_Maze = new class_("Maze");
    cl_MazeSolver = new class_("MazeSolver");
    cl_MazeGame = new class_("MazeGame");
    cl_FilebasedMazeGame = new class_("FilebasedMazeGame");
    if (__eq(__amaze__::__name__, const_29)) {
        game = (new FilebasedMazeGame(1));

        FAST_FOR(x,0,__ss_int(10000),1,93,94)
            solver = __amaze__::game->runGame();
        END_FOR

        __amaze__::solver->printResult();
    }
}

} // module namespace

int main(int, char **) {
    __shedskin__::__init();
    __math__::__init();
    __time__::__init();
    __random__::__init();
    __shedskin__::__start(__amaze__::__init);
}
