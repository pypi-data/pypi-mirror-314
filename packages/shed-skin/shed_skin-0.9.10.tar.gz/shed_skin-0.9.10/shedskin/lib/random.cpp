/* Copyright 1997-2002 Makoto Matsumoto, Takuji Nishimura, License BSD-3 (See LICENSE) */

#include "random.hpp"

/**
Random variable generators.

    integers
    --------
           uniform within range

    sequences
    ---------
           pick random element
           pick random sample
           generate random permutation

    distributions on the real line:
    ------------------------------
           uniform
           normal (Gaussian)
           lognormal
           negative exponential
           gamma
           beta
           pareto
           Weibull

    distributions on the circle (angles 0 to 2pi)
    ---------------------------------------------
           circular uniform
           von Mises

General notes on the underlying Mersenne Twister core generator:

* The period is 2**19937-1.
* It is one of the most extensively tested generators in existence
* Without a direct way to compute N steps forward, the
  semantics of jumpahead(n) are weakened to simply jump
  to another distant state and rely on the large period
  to avoid overlapping sequences.

Note: The jumpahead method is implemented for WichmannHill, but not yet for
Random (Mersenne Twister).
*/

namespace __random__ {

str *const_0, *const_1, *const_10, *const_11, *const_12, *const_13, *const_14, *const_15, *const_16, *const_17, *const_18, *const_19, *const_2, *const_20, *const_21, *const_22, *const_23, *const_24, *const_25, *const_26, *const_27, *const_28, *const_29, *const_3, *const_30, *const_31, *const_32, *const_33, *const_34, *const_35, *const_36, *const_4, *const_7, *const_8, *const_9;

list<str *> *__all__;
list<int> *mag01;
__ss_float LOG4, NV_MAGICCONST, SG_MAGICCONST;
int BPF, LOWER, M, MATRIX_A, __ss_MAXINT, MAXWIDTH, N, UPPER;
str *__name__;
Random *_inst;

static inline list<__ss_float> *list_comp_0(list<int> *__108) {
    int s, __25;
    list<__ss_float> *result = new list<__ss_float>();
    list<int>::for_in_loop __123;

    result->resize(len(__108));
    FOR_IN(s,__108,108,25,123)
        result->units[(size_t)__25] = __float(s);
    END_FOR

    return result;
}

static inline list<int> *list_comp_1(list<__ss_float> *__108) {
    __ss_float s;
    list<int> *result = new list<int>();
    list<int>::for_in_loop __123;
    int __28;

    result->resize(len(__108));
    FOR_IN(s,__108,108,28,123)
        result->units[(size_t)__28] = __int(s);
    END_FOR

    return result;
}

/**
class Random
*/

class_ *cl_Random;

__ss_float Random::paretovariate(__ss_float alpha) {
    /**
    Pareto distribution.  alpha is the shape parameter.
    */
    __ss_float u;

    u = (1.0-this->random());
    return (1.0/__power(u, (1.0/alpha)));
}

__ss_int Random::randrange(__ss_int stop) {
    return this->randrange(0, stop, 1);
}
__ss_int Random::randrange(__ss_int start, __ss_int stop) {
    return this->randrange(start, stop, 1);
}
__ss_int Random::randrange(__ss_int start, __ss_int stop, __ss_int step) {
    /**
    Choose a random item from range(start, stop[, step]).

            This fixes the problem with randint() which includes the
            endpoint; in Python this is usually not what you want.
            Do not supply the 'int', 'default', and 'maxwidth' arguments.
    */
    __ss_int istart, istep, istop, n, width;

    istart = __int(start);
    if (istart != start) {
        throw (new ValueError(const_0));
    }
    istop = __int(stop);
    if ((istop != stop)) {
        throw (new ValueError(const_1));
    }
    width = (istop-istart);
    if ((step == 1) && (width > 0)) {
        return __int((istart+__int((this->random()*width))));
    }
    if (step==1) {
        throw (new ValueError(const_2));
    }
    istep = __int(step);
    if (istep != step) {
        throw (new ValueError(const_3));
    }
    if (istep > 0) {
        n = (((width+istep)-1)/istep);
    }
    else if (istep < 0) {
        n = (((width+istep)+1)/istep);
    }
    else {
        throw (new ValueError(const_4));
    }
    if (n<=0) {
        throw (new ValueError(const_2));
    }
    return (istart+(istep*__int((this->random()*n))));
}

__ss_float Random::betavariate(__ss_float alpha, __ss_float beta) {
    /**
    Beta distribution.

            Conditions on the parameters are alpha > -1 and beta} > -1.
            Returned values range between 0 and 1.

    */
    __ss_float y;

    y = this->gammavariate(alpha, 1.0);
    if (y==0) {
        return 0.0;
    }
    else {
        return (y/(y+this->gammavariate(beta, 1.0)));
    }
    return 0;
}

__ss_float Random::random() {
    /**
    Generate a random number on [0,1)-real-interval.
    */

    return distr(gen);
}

__ss_float Random::normalvariate(__ss_float mu, __ss_float sigma) {
    /**
    Normal distribution.

            mu is the mean, and sigma is the standard deviation.

    */
    __ss_float u1, u2, z, zz;


    while(1) {
        u1 = this->random();
        u2 = (1.0-this->random());
        z = ((NV_MAGICCONST*(u1-0.5))/u2);
        zz = ((z*z)/4.0);
        if ((zz<=-__math__::log(u2))) {
            break;
        }
    }
    return (mu+(z*sigma));
}

__ss_float Random::weibullvariate(__ss_float alpha, __ss_float beta) {
    /**
    Weibull distribution.

            alpha is the scale parameter and beta is the shape parameter.

    */
    __ss_float u;

    u = (1.0-this->random());
    return (alpha*__power(-__math__::log(u), (1.0/beta)));
}

Random::Random() : gen(7.0), distr(0.0, 1.0) {
    this->__class__ = cl_Random;

    this->mt = ((new list<int>(1, 0)))->__mul__(N);
    this->mti = (N+1);
    this->gauss_next = 0.0;
    this->gauss_switch = 0;
    this->seed((void *)NULL);
    this->VERSION = 2;

}

Random::Random(int a) {
    /**
    Initialize an instance.

            Optional argument a controls seeding, as for Random.seed().
            The seed, a, must be an integer.
    */
    this->__class__ = cl_Random;

    this->mt = ((new list<int>(1, 0)))->__mul__(N);
    this->mti = (N+1);
    this->gauss_next = 0.0;
    this->gauss_switch = 0;
    this->seed(a);
    this->VERSION = 2;
}

int Random::_init_by_array(list<int> *init_key) {
    /**
    Seed the random number generator with a list of numbers.
    */
    list<int> *__14, *__15, *__16, *__19, *__20, *__21, *__22;
    int __12, __13, __17, __18, i, j, k, key_length;

    key_length = len(init_key);
    this->_init_genrand(19650218);
    i = 1;
    j = 0;
    k = ___max(2, 0, N, key_length);

    FAST_FOR(k,k,0,-1,12,13)
        __14 = this->mt;
        __14->__setitem__(i, (((this->mt)->__getfast__(i)^(((this->mt)->__getfast__((i-1))^(((this->mt)->__getfast__((i-1))>>30)&3))*1664525))+init_key->__getfast__(j))+j);
        __15 = this->mt;
        __15->__setitem__(i, __15->__getfast__(i) & -1);
        i += 1;
        j += 1;
        if (i >= N) {
            __16 = this->mt;
            __16->__setitem__(0, (this->mt)->__getfast__((N-1)));
            i = 1;
        }
        if (j >= key_length) {
            j = 0;
        }
    END_FOR


    FAST_FOR(k,(N-1),0,-1,17,18)
        __19 = this->mt;
        __19->__setitem__(i, (((this->mt)->__getfast__(i)^(((this->mt)->__getfast__((i-1))^(((this->mt)->__getfast__((i-1))>>30)&3))*1566083941))-i));
        __20 = this->mt;
        __20->__setitem__(i, __20->__getfast__(i) & -1);
        i += 1;
        if (i >= N) {
            __21 = this->mt;
            __21->__setitem__(0, (this->mt)->__getfast__((N-1)));
            i = 1;
        }
    END_FOR

    __22 = this->mt;
    __22->__setitem__(0, -2147483648);
    return 0;
}

__ss_int Random::randint(__ss_int a, __ss_int b) {
    /**
    Return random integer in range [a, b], including both end points.
    */

    return this->randrange(a, (b+1), 1);
}

__ss_float Random::vonmisesvariate(__ss_float mu, __ss_float kappa) {
    /**
    Circular data distribution.

            mu is the mean angle, expressed in radians between 0 and 2*pi, and
            kappa is the concentration parameter, which must be greater than or
            equal to zero.  If kappa is equal to zero, this distribution reduces
            to a uniform random angle over the range 0 to 2*pi.

    */
    __ss_float d, f, q, r, s, theta, u1, u2, u3, z, TWOPI;
    TWOPI = 2*__math__::pi;

    if (kappa <= 1e-06) {
        return (TWOPI*this->random());
    }
    s = (0.5/kappa);
    r = (s+__math__::sqrt((1.0+(s*s))));

    while (1) {
        u1 = this->random();
        z = __math__::cos((__math__::pi*u1));
        d = (z/(r+z));
        u2 = this->random();
        if (((u2<(1.0-(d*d))) or (u2<=((1.0-d)*__math__::exp(d))))) {
            break;
        }
    }
    q = (1.0/r);
    f = ((q+z)/(1.0+(q*z)));
    u3 = this->random();
    if ((u3>0.5)) {
        theta = __mods((mu+__math__::acos(f)), TWOPI);
    }
    else {
        theta = __mods((mu-__math__::acos(f)), TWOPI);
    }
    return theta;
}

__ss_float Random::gammavariate(__ss_float alpha, __ss_float beta) {
    /**
    Gamma distribution.  Not the gamma function!

            Conditions on the parameters are alpha > 0 and beta > 0.

    */
    __ss_float ainv, b, bbb, ccc, p, r, u, u1, u2, v, x, z;

    if ((alpha <= 0.0) || (beta<=0.0)) {
        throw (new ValueError(const_7));
    }
    if (alpha > 1.0) {
        ainv = __math__::sqrt(((2.0*alpha)-1.0));
        bbb = (alpha-LOG4);
        ccc = (alpha+ainv);

        while(1) {
            u1 = this->random();
            if ((!((1e-07<u1)&&(u1<0.9999999)))) {
                continue;
            }
            u2 = (1.0-this->random());
            v = (__math__::log((u1/(1.0-u1)))/ainv);
            x = (alpha*__math__::exp(v));
            z = ((u1*u1)*u2);
            r = ((bbb+(ccc*v))-x);
            if (((((r+SG_MAGICCONST)-(4.5*z))>=0.0) || (r>=__math__::log(z)))) {
                return (x*beta);
            }
        }
    }
    else if ( alpha == 1.0) {
        u = this->random();

        while(u <= 1e-07) {
            u = this->random();
        }
        return (-__math__::log(u)*beta);
    }
    else {

        while(1) {
            u = this->random();
            b = ((__math__::e+alpha)/__math__::e);
            p = (b*u);
            if ((p<=1.0)) {
                x = __power(p, (1.0/alpha));
            }
            else {
                x = -__math__::log(((b-p)/alpha));
            }
            u1 = this->random();
            if ((!(((p<=1.0) && (u1>__math__::exp(-x))) || ((p>1) && (u1>__power(x, (alpha-1.0))))))) {
                break;
            }
        }
        return (x*beta);
    }
    return 0;
}

__ss_float Random::uniform(__ss_float a, __ss_float b) {
    /**
    Get a random number in the range [a, b).
    */

    return (a+((b-a)*this->random()));
}

static inline __ss_float __triangular(__ss_float low, __ss_float high, __ss_float u, __ss_float c) {
    __ss_float __0, __1;
    if ((u>c)) {
        u = (1.0-u);
        c = (1.0-c);
        __0 = high;
        __1 = low;
        low = __0;
        high = __1;
    }
    return (low+((high-low)*__power((u*c), 0.5)));
}

__ss_float Random::triangular(__ss_float low, __ss_float high, __ss_float mode) {
    /**
    Triangular distribution.

    Continuous distribution bounded by given lower and upper limits,
    and having a given mode value in-between.

    http://en.wikipedia.org/wiki/Triangular_distribution

    */
    return __triangular(low, high, this->random(), ((mode-low)/(high-low)));
}

__ss_float Random::triangular(__ss_float low, __ss_float high, __ss_int mode) {
    return __triangular(low, high, this->random(), (__ss_float)mode);
}

__ss_float Random::triangular(__ss_float low, __ss_float high, void *) {
    return __triangular(low, high, this->random(), 0.5);
}

__ss_float Random::stdgamma(__ss_float alpha, __ss_float, __ss_float, __ss_float) {

    return this->gammavariate(alpha, 1.0);
}

__ss_float Random::expovariate(__ss_float lambd) {
    /**
    Exponential distribution.

            lambd is 1.0 divided by the desired mean.  (The parameter would be
            called "lambda", but that is a reserved word in Python.)  Returned
            values range from 0 to positive infinity.

    */

    /*
    python 2.6 behaviour, changed in 2.7:

    __ss_float u;

    u = this->random();

    while((u<=1e-07)) {
        u = this->random();
    }
    return (-__math__::log(u)/lambd);
    */

    return (-__math__::log(1.0 - this->random())/lambd);
}

__ss_int Random::getrandbits(__ss_int k) {
    /**
    getrandbits(k) -> x.  Generates an int with k random bits.
    */

    if ((k<=0)) {
        throw (const_8);
    }

    return randrange((__ss_int)1<<k);
}

void *Random::setstate(list<__ss_float> *state) {
    /**
    Restore internal state from object returned by getstate().
    */
    int version;

    version = __int(state->__getfast__(0));
    if ((version!=2)) {
        throw ((new ValueError(__mod6(const_10, 2, version, this->VERSION))));
    }
    this->mti = __int(state->__getfast__(1));
    this->gauss_switch = __int(state->__getfast__(2));
    this->mt = list_comp_1(state->__slice__(3, 3, -1, 0));
    this->gauss_next = state->__getfast__(-1);

    return NULL;
}

__ss_float Random::lognormvariate(__ss_float mu, __ss_float sigma) {
    /**
    Log normal distribution.

            If you take the natural logarithm of this distribution, you'll get a
            normal distribution with mean mu and standard deviation sigma.
            mu can have any value, and sigma must be greater than zero.

    */

    return __math__::exp(this->normalvariate(mu, sigma));
}

int Random::_init_genrand(int s) {
    /**
    Seed the random number generator.
    */
    list<int> *__10, *__11, *__7;
    int __8, __9;

    __7 = this->mt;
    __7->__setitem__(0, (s&-1));

    FAST_FOR(this->mti,1,N,1,8,9)
        __10 = this->mt;
        __10->__setitem__(this->mti, ((1812433253*((this->mt)->__getfast__((this->mti-1))^(((this->mt)->__getfast__((this->mti-1))>>30)&3)))+this->mti));
        __11 = this->mt;
        __11->__setitem__(this->mti, __11->__getfast__(this->mti) & -1);
    END_FOR

    this->mti += 1;
    return 0;
}

__ss_float Random::gauss(__ss_float mu, __ss_float sigma) {
    /**
    Gaussian distribution.

            mu is the mean, and sigma is the standard deviation.  This is
            slightly faster than the normalvariate() function.

            Not thread-safe without a lock around calls.

    */
    __ss_float g2rad, x2pi, z;

    if (this->gauss_switch == 1) {
        z = this->gauss_next;
        this->gauss_switch = 0;
    }
    else {
        x2pi = ((this->random()*2)*__math__::pi);
        g2rad = __math__::sqrt((-2.0*__math__::log((1.0-this->random()))));
        z = (__math__::cos(x2pi)*g2rad);
        this->gauss_next = (__math__::sin(x2pi)*g2rad);
        this->gauss_switch = 1;
    }
    return (mu+(z*sigma));
}

list<__ss_float> *Random::getstate() {
    /**
    Return internal state; can be passed to setstate() later.
    */
    list<__ss_float> *x;

    x = list_comp_0(__add((new list<int>(3, this->VERSION, this->mti, this->gauss_switch)), this->mt));
    return __add(x, (new list<__ss_float>(1, this->gauss_next)));
}

__ss_float Random::cunifvariate(__ss_float mean, __ss_float arc) {

    return __math__::fmod((mean+(arc*(this->random()-0.5))), __math__::pi);
}

/**
class WichmannHill
*/

class_ *cl_WichmannHill;

void *WichmannHill::__whseed(int x, int y, int z) {
    /**
    Set the Wichmann-Hill seed from (x, y, z).

            These must be integers in the range [0, 256).
    */
    tuple2<int, int> *__59, *__60, *__61;
    int __62, __63, __64, secs, t, usec;
    __ss_float hophop;

    if ((!(((0<=x)&&(x<256)) && ((0<=y)&&(y<256)) && ((0<=z)&&(z<256))))) {
        throw ((new ValueError(const_11)));
    }
    if ((0==x) && (x==y) && (y==z)) {
        hophop = __time__::time();
        secs = __int(hophop);
        usec = __int((1000000*(hophop-__int(hophop))));
        t = ((__mods(secs, (__ss_MAXINT/1000000))*1000000)|usec);
        __59 = divmod(t, 256);
        t = __59->__getfirst__();
        x = __59->__getsecond__();
        __60 = divmod(t, 256);
        t = __60->__getfirst__();
        y = __60->__getsecond__();
        __61 = divmod(t, 256);
        t = __61->__getfirst__();
        z = __61->__getsecond__();
    }
    if (x==0) {
        x = 1;
    }
    if (y==0) {
        y = 1;
    }
    if (z==0) {
        z = 1;
    }
    __62 = x;
    __63 = y;
    __64 = z;
    this->_seed = (new tuple2<int, int>(3, __62, __63, __64));
    this->gauss_next = 0.0;
    this->gauss_switch = 0;
    return NULL;
}

__ss_float WichmannHill::random() {
    /**
    Get the next random number in the range [0.0, 1.0).
    */
    tuple2<int, int> *__46;
    int __47, __48, __49, x, y, z;

    __46 = this->_seed;
    x = __46->__getfast__(0);
    y = __46->__getfast__(1);
    z = __46->__getfast__(2);
    x = __mods((171*x), 30269);
    y = __mods((172*y), 30307);
    z = __mods((170*z), 30323);
    __47 = x;
    __48 = y;
    __49 = z;
    this->_seed = (new tuple2<int, int>(3, __47, __48, __49));
    return __math__::fmod((((__float(x)/30269.0)+(__float(y)/30307.0))+(__float(z)/30323.0)), 1.0);
}

void *WichmannHill::seed() {
    return this->seed(-1);
}
void *WichmannHill::seed(int a) {
    /**
    Initialize internal state from hashable object.

            If provided, the seed, a, should be a non-negative integer.
            If no argument is provided, current time is used for seeding.

            Distinct values between 0 and 27814431486575L inclusive are guaranteed
            to yield distinct internal states (this guarantee is specific to the
            default Wichmann-Hill generator).
    */
    tuple2<int, int> *__40, *__41, *__42;
    int __43, __44, __45, secs, usec, x, y, z;
    __ss_float hophop;

    if (a==-1) {
        hophop = __time__::time();
        secs = __int(hophop);
        usec = __int((1000000*(hophop-__int(hophop))));
        a = ((__mods(secs, (__ss_MAXINT/1000000))*1000000)|usec);
    }
    __40 = divmod(a, 30268);
    a = __40->__getfirst__();
    x = __40->__getsecond__();
    __41 = divmod(a, 30306);
    a = __41->__getfirst__();
    y = __41->__getsecond__();
    __42 = divmod(a, 30322);
    a = __42->__getfirst__();
    z = __42->__getsecond__();
    __43 = (__int(x)+1);
    __44 = (__int(y)+1);
    __45 = (__int(z)+1);
    this->_seed = (new tuple2<int, int>(3, __43, __44, __45));
    this->gauss_next = 0.0;
    this->gauss_switch = 0;
    return NULL;
}

WichmannHill::WichmannHill() {
    this->__class__ = cl_WichmannHill;

    this->seed(-1);
    this->gauss_next = 0.0;
    this->gauss_switch = 0;
    this->VERSION = 1;
}

WichmannHill::WichmannHill(int a) {
    this->__class__ = cl_WichmannHill;

    this->seed(a);
    this->gauss_next = 0.0;
    this->gauss_switch = 0;
    this->VERSION = 1;
}

void *WichmannHill::whseed() {
    return this->whseed(-1);
}
void *WichmannHill::whseed(int a) {
    /**
    Seed from current time or non-negative integer argument.

            If no argument is provided, current time is used for seeding.

            This is obsolete, provided for compatibility with the seed routine
            used prior to Python 2.1.  Use the .seed() method instead.
    */
    tuple2<int, int> *__65, *__66, *__67;
    int x, y, z;

    if (a==-1) {
        this->__whseed(((int )(0)), ((int )(0)), ((int )(0)));
        return NULL;
    }
    __65 = divmod(a, 256);
    a = __65->__getfirst__();
    x = __65->__getsecond__();
    __66 = divmod(a, 256);
    a = __66->__getfirst__();
    y = __66->__getsecond__();
    __67 = divmod(a, 256);
    a = __67->__getfirst__();
    z = __67->__getsecond__();
    x = __mods((x+a), 256);
    y = __mods((y+a), 256);
    z = __mods((z+a), 256);
    if (x==0) {
        x = 1;
    }
    if (y==0) {
        y = 1;
    }
    if (z==0) {
        z = 1;
    }
    this->__whseed(x, y, z);
    return NULL;
}

void *WichmannHill::setstate(list<__ss_float> *state) {
    /**
    Restore internal state from object returned by getstate().
    */
    __ss_float xf, yf, zf;
    list<__ss_float> *__51;
    int __52, __53, __54, version;

    version = __int(state->__getfast__(0));
    if (version==1) {
        __51 = state->__slice__(3, 1, 4, 0);
        xf = __51->__getfast__(0);
        yf = __51->__getfast__(1);
        zf = __51->__getfast__(2);
        __52 = __int(xf);
        __53 = __int(yf);
        __54 = __int(zf);
        this->_seed = (new tuple2<int, int>(3, __52, __53, __54));
        this->gauss_switch = __int(state->__getfast__(4));
        this->gauss_next = state->__getfast__(5);
    }
    else {
        throw ((new ValueError(__mod6(const_10, 2, version, this->VERSION))));
    }
    return NULL;
}

int WichmannHill::jumpahead(int n) {
    /**
    Act as if n calls to random() were made, but quickly.

            n is an int, greater than or equal to 0.

            Example use:  If you have 2 threads and know that each will
            consume no more than a million random numbers, create two Random
            objects r1 and r2, then do
                r2.setstate(r1.getstate())
                r2.jumpahead(1000000)
            Then r1 and r2 will use guaranteed-disjoint segments of the full
            period.
    */
    tuple2<int, int> *__55;
    int __56, __57, __58, x, y, z;

    if (!(n>=0)) {
        throw ((new ValueError(const_12)));
    }
    __55 = this->_seed;
    x = __55->__getfast__(0);
    y = __55->__getfast__(1);
    z = __55->__getfast__(2);
    x = __mods(__int((x*__power(171, n, 30269))), (__ss_int)30269);
    y = __mods(__int((y*__power(172, n, 30307))), (__ss_int)30307);
    z = __mods(__int((z*__power(170, n, 30323))), (__ss_int)30323);
    __56 = x;
    __57 = y;
    __58 = z;
    this->_seed = (new tuple2<int, int>(3, __56, __57, __58));
    return 0;
}

list<__ss_float> *WichmannHill::getstate() {
    /**
    Return internal state; can be passed to setstate() later.
    */
    tuple2<int, int> *__50;
    int x, y, z;

    __50 = this->_seed;
    x = __50->__getfast__(0);
    y = __50->__getfast__(1);
    z = __50->__getfast__(2);
    return (new list<__ss_float>(6, __float(this->VERSION), __float(x), __float(y), __float(z), __float(this->gauss_switch), this->gauss_next));
}

void __init() {
    const_0 = new str("non-integer arg 1 for randrange()");
    const_1 = new str("non-integer stop for randrange()");
    const_2 = new str("empty range for randrange()");
    const_3 = new str("non-integer step for randrange()");
    const_4 = new str("zero step for randrange()");
    const_7 = new str("gammavariate: alpha and beta must be > 0.0");
    const_8 = new str("number of bits must be greater than zero for getrandbits(k)");
    const_9 = new str("k exceeds size of int for getrandbits(k)");
    const_10 = new str("state with version %s passed to Random.setstate() of version %s");
    const_11 = new str("seeds must be in range(0, 256)");
    const_12 = new str("n must be >= 0");
    const_13 = new str("Random");
    const_14 = new str("seed");
    const_15 = new str("random");
    const_16 = new str("uniform");
    const_17 = new str("randint");
    const_18 = new str("choice");
    const_19 = new str("sample");
    const_20 = new str("randrange");
    const_21 = new str("shuffle");
    const_22 = new str("normalvariate");
    const_23 = new str("lognormvariate");
    const_24 = new str("cunifvariate");
    const_25 = new str("expovariate");
    const_26 = new str("vonmisesvariate");
    const_27 = new str("gammavariate");
    const_28 = new str("stdgamma");
    const_29 = new str("gauss");
    const_30 = new str("betavariate");
    const_31 = new str("paretovariate");
    const_32 = new str("weibullvariate");
    const_33 = new str("getstate");
    const_34 = new str("setstate");
    const_35 = new str("jumpahead");
    const_36 = new str("WichmannHill");

    __name__ = new str("random");

    cl_WichmannHill = new class_("WichmannHill");
    cl_Random = new class_("Random");

    /**
    =========================== Source Notes ==============================
    Translated by Guido van Rossum from C source provided by Adrian Baddeley.
    Adapted by Raymond Hettinger for use with the Mersenne Twister core generator.
    Adapted by Jeff Miller for compatibility with the Shed Skin Python-to-C++
    compiler.

    Mersenne Twister was converted to Python by Jeff Miller
    2007-02-03
    jwmillerusa (at) gmail (dot) com
    http://millerideas.com

    Below are the original comments from the authors' C source file.
    =======================================================================

       A C-program for MT19937, with initialization improved 2002/1/26.
       Coded by Takuji Nishimura and Makoto Matsumoto.

       Before using, initialize the state by using init_genrand(seed)
       or init_by_array(init_key, key_length).

       Copyright (C) 1997 - 2002, Makoto Matsumoto and Takuji Nishimura,
       All rights reserved.

       Redistribution and use in source and binary forms, with or without
       modification, are permitted provided that the following conditions
       are met:

         1. Redistributions of source code must retain the above copyright
            notice, this list of conditions and the following disclaimer.

         2. Redistributions in binary form must reproduce the above copyright
            notice, this list of conditions and the following disclaimer in the
            documentation and/or other materials provided with the distribution.

         3. The names of its contributors may not be used to endorse or promote
            products derived from this software without specific prior written
            permission.

       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
       AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
       IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
       ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
       LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
       CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
       SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
       INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
       CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
       ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
       POSSIBILITY OF SUCH DAMAGE.


       Any feedback is very welcome.
       http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/emt.html
       email: m-mat @ math.sci.hiroshima-u.ac.jp (remove space)
    */
    __all__ = (new list<str *>(24, const_13, const_14, const_15, const_16, const_17, const_18, const_19, const_20, const_21, const_22, const_23, const_24, const_25, const_26, const_27, const_28, const_29, const_30, const_31, const_32, const_33, const_34, const_35, const_36));
    NV_MAGICCONST = ((4*__math__::exp(-0.5))/__math__::sqrt(2.0));
    LOG4 = __math__::log(4.0);
    SG_MAGICCONST = (1.0+__math__::log(4.5));
    BPF = 53;
    MAXWIDTH = (1<<BPF);
    __ss_MAXINT = 2147483647;
    N = 624;
    M = 397;
    MATRIX_A = -1727483681;
    UPPER = -2147483648;
    LOWER = 2147483647;
    mag01 = (new list<int>(2, 0, MATRIX_A));
    _inst = (new Random());
}

__ss_float random() {

    return _inst->random();
}

list<__ss_float> *getstate() {

    return _inst->getstate();
}

void *setstate(list<__ss_float> *state) {

    return _inst->setstate(state);
}

__ss_int randrange(__ss_int stop) {

    return _inst->randrange(0, stop, 1);
}

__ss_int randrange(__ss_int start, __ss_int stop) {

    return _inst->randrange(start, stop, 1);
}

__ss_int randrange(__ss_int start, __ss_int stop, __ss_int step) {

    return _inst->randrange(start, stop, step);
}

__ss_int randint(__ss_int a, __ss_int b) {

    return _inst->randint(a, b);
}

__ss_float uniform(__ss_float a, __ss_float b) {

    return _inst->uniform(a, b);
}

__ss_float normalvariate(__ss_float mu, __ss_float sigma) {

    return _inst->normalvariate(mu, sigma);
}

__ss_float lognormvariate(__ss_float mu, __ss_float sigma) {

    return _inst->lognormvariate(mu, sigma);
}

__ss_float cunifvariate(__ss_float mean, __ss_float arc) {

    return _inst->cunifvariate(mean, arc);
}

__ss_float expovariate(__ss_float lambd) {

    return _inst->expovariate(lambd);
}

__ss_float vonmisesvariate(__ss_float mu, __ss_float kappa) {

    return _inst->vonmisesvariate(mu, kappa);
}

__ss_float gammavariate(__ss_float alpha, __ss_float beta) {

    return _inst->gammavariate(alpha, beta);
}

__ss_float stdgamma(__ss_float alpha, __ss_float ainv, __ss_float bbb, __ss_float ccc) {

    return _inst->stdgamma(alpha, ainv, bbb, ccc);
}

__ss_float gauss(__ss_float mu, __ss_float sigma) {

    return _inst->gauss(mu, sigma);
}

__ss_float betavariate(__ss_float alpha, __ss_float beta) {

    return _inst->betavariate(alpha, beta);
}

__ss_float paretovariate(__ss_float alpha) {

    return _inst->paretovariate(alpha);
}

__ss_float weibullvariate(__ss_float alpha, __ss_float beta) {

    return _inst->weibullvariate(alpha, beta);
}

__ss_int getrandbits(__ss_int k) {

    return _inst->getrandbits(k);
}

__ss_float triangular(__ss_float low, __ss_float high, __ss_float mode) {
    return _inst->triangular(low, high, mode);
}
__ss_float triangular(__ss_float low, __ss_float high, __ss_int mode) {
    return _inst->triangular(low, high, mode);
}
__ss_float triangular(__ss_float low, __ss_float high, void *mode) {
    return _inst->triangular(low, high, mode);
}

} // module namespace

