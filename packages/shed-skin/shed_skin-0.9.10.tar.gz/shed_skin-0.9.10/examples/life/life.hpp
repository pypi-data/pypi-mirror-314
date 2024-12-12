#ifndef __LIFE_HPP
#define __LIFE_HPP

using namespace __shedskin__;
namespace __life__ {

extern str *const_0;


typedef __ss_int (*lambda0)();
typedef __ss_int (*lambda1)();
typedef __collections__::defaultdict<tuple<__ss_int> *, __ss_int> *(*lambda2)(__collections__::defaultdict<tuple<__ss_int> *, __ss_int> *);

extern str *__name__;
extern __ss_int columns, count, rows;


__ss_int add(__collections__::defaultdict<tuple<__ss_int> *, __ss_int> *board, tuple<__ss_int> *pos);
__collections__::defaultdict<tuple<__ss_int> *, __ss_int> *snext(__collections__::defaultdict<tuple<__ss_int> *, __ss_int> *board);
__collections__::defaultdict<tuple<__ss_int> *, __ss_int> *process(__collections__::defaultdict<tuple<__ss_int> *, __ss_int> *board);
__iter<__collections__::defaultdict<tuple<__ss_int> *, __ss_int> *> *generator(__ss_int rows, __ss_int columns);
void *bruteforce(__ss_int rows, __ss_int columns);

} // module namespace
#endif
