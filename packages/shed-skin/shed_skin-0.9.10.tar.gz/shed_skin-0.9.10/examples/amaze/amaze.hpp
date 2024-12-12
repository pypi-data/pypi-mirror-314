#ifndef __AMAZE_HPP
#define __AMAZE_HPP

using namespace __shedskin__;

namespace __amaze__ { /* XXX */
class MazeReaderException;
class MazeReader;
class MazeFactory;
class MazeError;
class Maze;
class MazeSolver;
class MazeGame;
class FilebasedMazeGame;
}
namespace __amaze__ {

extern str *const_0, *const_1, *const_10, *const_11, *const_12, *const_13, *const_14, *const_15, *const_16, *const_17, *const_18, *const_19, *const_2, *const_20, *const_21, *const_22, *const_23, *const_24, *const_25, *const_26, *const_27, *const_28, *const_29, *const_3, *const_4, *const_5, *const_6, *const_7, *const_8, *const_9;

class MazeReaderException;
class MazeReader;
class MazeFactory;
class MazeError;
class Maze;
class MazeSolver;
class MazeGame;
class FilebasedMazeGame;


extern str *__name__;
extern __ss_int EXIT, FILE_, PATH, SOCKET, START, STDIN, __93, __94, x;
extern FilebasedMazeGame *game;
extern MazeSolver *solver;


extern class_ *cl_MazeReaderException;
class MazeReaderException : public Exception {
public:
    tuple<str *> *args;

    MazeReaderException() {}
    MazeReaderException(str *arg) {
        this->__class__ = cl_MazeReaderException;
        __init__(arg);
    }
    static void __static__();
};

extern class_ *cl_MazeReader;
class MazeReader : public pyobj {
public:
    list<list<__ss_int> *> *maze_rows;

    MazeReader() {}
    MazeReader(int __ss_init) {
        this->__class__ = cl_MazeReader;
        __init__();
    }
    void *__init__();
    void *readStdin();
    void *readFile();
    list<list<__ss_int> *> *getData();
    list<list<__ss_int> *> *readMaze(__ss_int source);
};

extern class_ *cl_MazeFactory;
class MazeFactory : public pyobj {
public:

    MazeFactory() { this->__class__ = cl_MazeFactory; }
    Maze *makeMaze(__ss_int source);
};

extern class_ *cl_MazeError;
class MazeError : public Exception {
public:
    tuple<str *> *args;

    MazeError() {}
    MazeError(str *arg) {
        this->__class__ = cl_MazeError;
        __init__(arg);
    }
    static void __static__();
};

extern class_ *cl_Maze;
class Maze : public pyobj {
public:
    __ss_int _width;
    __ss_int _height;
    list<list<__ss_int> *> *_rows;

    Maze() {}
    Maze(list<list<__ss_int> *> *rows) {
        this->__class__ = cl_Maze;
        __init__(rows);
    }
    void *__init__(list<list<__ss_int> *> *rows);
    str *__str__();
    void *__validate();
    void *__normalize();
    void *validatePoint(tuple<__ss_int> *pt);
    __ss_int getItem(__ss_int x, __ss_int y);
    void *setItem(__ss_int x, __ss_int y, __ss_int value);
    list<tuple<__ss_int> *> *getNeighBours(tuple<__ss_int> *pt);
    list<tuple<__ss_int> *> *getExitPoints(tuple<__ss_int> *pt);
    __ss_float calcDistance(tuple<__ss_int> *pt1, tuple<__ss_int> *pt2);
};

extern class_ *cl_MazeSolver;
class MazeSolver : public pyobj {
public:
    tuple<__ss_int> *_end;
    tuple<__ss_int> *_start;
    list<tuple<__ss_int> *> *_path;
    __ss_int _steps;
    Maze *maze;
    __ss_int _loops;
    tuple<__ss_int> *_current;
    __ss_bool _tryalternate;
    __ss_bool _trynextbest;
    __ss_int _numretraces;
    __ss_bool _retrace;
    tuple<__ss_int> *_disputed;

    MazeSolver() {}
    MazeSolver(Maze *maze) {
        this->__class__ = cl_MazeSolver;
        __init__(maze);
    }
    void *__init__(Maze *maze);
    void *setStartPoint(tuple<__ss_int> *pt);
    void *setEndPoint(tuple<__ss_int> *pt);
    __ss_bool boundaryCheck();
    void *setCurrentPoint(tuple<__ss_int> *point);
    __ss_bool isSolved();
    tuple<__ss_int> *getNextPoint();
    void *retracePath();
    __ss_bool endlessLoop();
    __ss_bool checkClosedLoop(tuple<__ss_int> *point);
    tuple<__ss_int> *getBestPoint(list<tuple<__ss_int> *> *points);
    list<tuple<__ss_int> *> *sortPoints(list<tuple<__ss_int> *> *points);
    tuple<__ss_int> *getClosestPoint(list<tuple<__ss_int> *> *points);
    tuple<__ss_int> *getAlternatePoint(list<tuple<__ss_int> *> *points, tuple<__ss_int> *point);
    tuple<__ss_int> *getNextClosestPoint(list<tuple<__ss_int> *> *points, tuple<__ss_int> *point);
    tuple<__ss_int> *getNextClosestPointNotInPath(list<tuple<__ss_int> *> *points, tuple<__ss_int> *point);
    void *solve();
    void *printResult();
};

extern class_ *cl_MazeGame;
class MazeGame : public pyobj {
public:
    tuple<__ss_int> *_start;
    tuple<__ss_int> *_end;

    MazeGame() {}
    MazeGame(int __ss_init) {
        this->__class__ = cl_MazeGame;
        __init__();
    }
    virtual Maze *createMaze() { return 0; };
    virtual void *getStartEndPoints(Maze *maze) { return 0; };
    void *__init__();
    MazeSolver *runGame();
};

extern class_ *cl_FilebasedMazeGame;
class FilebasedMazeGame : public MazeGame {
public:

    FilebasedMazeGame() {}
    FilebasedMazeGame(int __ss_init) {
        this->__class__ = cl_FilebasedMazeGame;
        __init__();
    }
    Maze *createMaze();
    void *getStartEndPoints(Maze *maze);
};

extern __ss_int  default_0;
extern __ss_int  default_1;
extern list<list<__ss_int> *> * default_2;
extern str * default_3;
extern str * default_4;

} // module namespace
#endif
