#include "builtin.hpp"
#include "time.hpp"
#include "math.hpp"
#include "re.hpp"
#include "random.hpp"
#include "sys.hpp"
#include "ml/spatialindex.hpp"
#include "minilight.hpp"
#include "ml/surfacepoint.hpp"
#include "ml/triangle.hpp"
#include "ml/raytracer.hpp"
#include "ml/__init__.hpp"
#include "ml/camera.hpp"
#include "ml/entry.hpp"
#include "ml/vector3f.hpp"
#include "ml/scene.hpp"
#include "ml/image.hpp"

namespace __minilight__ {

str *const_0, *const_1;


str *__name__;



void *__ss_main() {
    __ml__::__entry__::__ss_main(const_0);
    return NULL;
}

void __init() {
    const_0 = new str("cornellbox.txt");
    const_1 = new str("__main__");

    __name__ = new str("__main__");

    if (__eq(__minilight__::__name__, const_1)) {
        __ss_main();
    }
}

} // module namespace

int main(int __ss_argc, char **__ss_argv) {
    __shedskin__::__init();
    __ml__::__init();
    __math__::__init();
    __time__::__init();
    __random__::__init();
    __ml__::__vector3f__::__init();
    __ml__::__surfacepoint__::__init();
    __ml__::__raytracer__::__init();
    __re__::__init();
    __ml__::__camera__::__init();
    __ml__::__image__::__init();
    __ml__::__triangle__::__init();
    __ml__::__spatialindex__::__init();
    __ml__::__scene__::__init();
    __sys__::__init(__ss_argc, __ss_argv);
    __ml__::__entry__::__init();
    __shedskin__::__start(__minilight__::__init);
}
