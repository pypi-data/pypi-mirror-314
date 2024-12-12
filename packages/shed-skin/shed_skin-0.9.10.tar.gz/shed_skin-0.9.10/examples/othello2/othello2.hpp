#ifndef __OTHELLO2_HPP
#define __OTHELLO2_HPP

using namespace __shedskin__;
namespace __othello2__ {

extern str *const_0, *const_1, *const_10, *const_11, *const_12, *const_13, *const_14, *const_15, *const_16, *const_17, *const_18, *const_19, *const_2, *const_20, *const_21, *const_22, *const_23, *const_24, *const_25, *const_26, *const_27, *const_28, *const_29, *const_3, *const_30, *const_31, *const_32, *const_33, *const_34, *const_35, *const_36, *const_37, *const_38, *const_39, *const_4, *const_40, *const_41, *const_42, *const_43, *const_44, *const_45, *const_46, *const_47, *const_48, *const_49, *const_5, *const_50, *const_51, *const_52, *const_53, *const_54, *const_55, *const_56, *const_57, *const_6, *const_7, *const_8, *const_9;


typedef __ss_int (*lambda0)(void *, void *, void *, void *, void *);
typedef __ss_int (*lambda1)(void *, void *, void *, void *, void *);
typedef __ss_int (*lambda2)(void *, void *, void *, void *, void *);
typedef __ss_int (*lambda3)(void *, void *, void *, void *, void *);
typedef __ss_int (*lambda4)(void *, void *, void *, void *, void *);
typedef __ss_int (*lambda5)(void *, void *, void *, void *, void *);
typedef __ss_int (*lambda6)(void *, void *, void *, void *, void *);
typedef __ss_int (*lambda7)(void *, void *, void *, void *, void *);
typedef __ss_int (*lambda8)(void *, void *, void *, void *, void *);
typedef __ss_int (*lambda9)(void *, void *, void *, void *, void *);

extern str *__name__, *arg, *mode;
extern __ss_int ALPHA_MIN, BETA_MAX, BLACK, CORNER_MASK, NODES, WHITE, WIN_BONUS, __49, i, max_depth;
extern list<__ss_int> *MASKS, *SHIFTS;
extern tuple2<__ss_int, str *> *__46;
extern __iter<tuple2<__ss_int, str *> *> *__47, *__48;
extern list<str *> *__50;


extern __ss_int  default_0;
extern __ss_int  default_1;
__ss_int shift(__ss_int disks, __ss_int direction, __ss_int S, __ss_int M);
__ss_int possible_moves(list<__ss_int> *state, __ss_int color);
void *do_move(list<__ss_int> *state, __ss_int color, __ss_int move);
void *print_board(list<__ss_int> *state);
list<__ss_int> *parse_state(str *board);
str *human_move(__ss_int move);
__ss_int parse_move(str *s);
__ss_int evaluate(list<__ss_int> *state, __ss_int color, __ss_bool is_max_player, __ss_int my_moves, __ss_int opp_moves);
__ss_int minimax_ab(list<__ss_int> *state, __ss_int color, __ss_int depth, __ss_int max_depth, __ss_bool is_max_player, __ss_int alpha, __ss_int beta);
str *empty_board();
void *vs_cpu_cli(__ss_int max_depth);
void *vs_cpu_nboard(__ss_int max_depth);
void *vs_cpu_ugi(__ss_int max_depth);
void *speed_test(__ss_int max_depth);

} // module namespace
#endif
