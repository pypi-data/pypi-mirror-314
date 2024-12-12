#include "builtin.hpp"
#include "array.hpp"
#include "com/github/tarsa/tarsalzp/prelude/__init__.hpp"
#include "com/github/tarsa/tarsalzp/Options.hpp"
#include "com/github/tarsa/tarsalzp/prelude/Long.hpp"
#include "com/github/tarsa/tarsalzp/prelude/Streams.hpp"
#include "com/github/__init__.hpp"
#include "com/github/tarsa/__init__.hpp"
#include "com/github/tarsa/tarsalzp/core/Common.hpp"
#include "com/github/tarsa/tarsalzp/__init__.hpp"
#include "com/github/tarsa/tarsalzp/core/Decoder.hpp"
#include "com/github/tarsa/tarsalzp/core/Encoder.hpp"
#include "com/github/tarsa/tarsalzp/core/Coder.hpp"
#include "com/github/tarsa/tarsalzp/core/FsmGenerator.hpp"
#include "com/github/tarsa/tarsalzp/core/Lg2.hpp"
#include "com/__init__.hpp"

namespace __com__ {
namespace __github__ {
namespace __tarsa__ {
namespace __tarsalzp__ {
namespace __core__ {
namespace __Coder__ {

str *const_0, *const_1, *const_2, *const_3, *const_4;

using __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Long__::Long;
using __com__::__github__::__tarsa__::__tarsalzp__::__Options__::Options;
using __com__::__github__::__tarsa__::__tarsalzp__::__core__::__Decoder__::Decoder;
using __com__::__github__::__tarsa__::__tarsalzp__::__core__::__Encoder__::Encoder;

str *__author__, *__name__;



/**
class Coder
*/

class_ *cl_Coder;

__com__::__github__::__tarsa__::__tarsalzp__::__Options__::Options *Coder::getOptions(__com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream *inputStream) {
    __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Long__::Long *header;
    __ss_int __166, __167, i, inputByte;

    header = (new __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Long__::Long(__ss_int(0), __ss_int(0), __ss_int(0), __ss_int(0)));

    FAST_FOR(i,0,__ss_int(8),1,166,167)
        header->shl8();
        inputByte = inputStream->readByte();
        if ((inputByte==(-__ss_int(1)))) {
            throw ((new OSError(const_0)));
        }
        header->d = ((header->d)|(inputByte));
    END_FOR

    if (((((((___bool((header->a!=(Coder::HeaderValue)->a)))|(___bool((header->b!=(Coder::HeaderValue)->b)))))|(___bool((header->c!=(Coder::HeaderValue)->c)))))|(___bool((header->d!=(Coder::HeaderValue)->d))))) {
        throw ((new OSError(const_1)));
    }
    return Coder::getOptionsHeaderless(inputStream);
}

__com__::__github__::__tarsa__::__tarsalzp__::__Options__::Options *Coder::getOptionsHeaderless(__com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream *inputStream) {
    __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Long__::Long *packedOptions;
    __ss_int __168, __169, i, inputByte;
    __com__::__github__::__tarsa__::__tarsalzp__::__Options__::Options *result;

    packedOptions = (new __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Long__::Long(__ss_int(0), __ss_int(0), __ss_int(0), __ss_int(0)));

    FAST_FOR(i,0,__ss_int(8),1,168,169)
        packedOptions->shl8();
        inputByte = inputStream->readByte();
        if ((inputByte==(-__ss_int(1)))) {
            throw ((new OSError(const_0)));
        }
        packedOptions->d = ((packedOptions->d)|(inputByte));
    END_FOR

    result = Options::fromPacked(packedOptions);
    if ((result==NULL)) {
        throw ((new ValueError(const_2)));
    }
    else {
        return result;
    }
    return 0;
}

void *Coder::checkInterval(__ss_int intervalLength) {
    if ((intervalLength<=__ss_int(0))) {
        throw ((new ValueError(const_3)));
    }
    return NULL;
}

void *Coder::decode(__com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream *inputStream, __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedOutputStreamWrapper *outputStream, __ss_int intervalLength) {
    __com__::__github__::__tarsa__::__tarsalzp__::__Options__::Options *options;

    Coder::checkInterval(intervalLength);
    options = Coder::getOptions(inputStream);
    Coder::decodeRaw(inputStream, outputStream, intervalLength, options);
    return NULL;
}

void *Coder::decodeRaw(__com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream *inputStream, __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedOutputStreamWrapper *outputStream, __ss_int intervalLength, __com__::__github__::__tarsa__::__tarsalzp__::__Options__::Options *options) {
    __com__::__github__::__tarsa__::__tarsalzp__::__core__::__Decoder__::Decoder *decoder;
    __ss_int amountProcessed;

    Coder::checkInterval(intervalLength);
    decoder = (new __com__::__github__::__tarsa__::__tarsalzp__::__core__::__Decoder__::Decoder(inputStream, outputStream, options));
    amountProcessed = __ss_int(0);

    while (__NOT(decoder->decode(intervalLength))) {
        amountProcessed = (amountProcessed+intervalLength);
    }
    return NULL;
}

void *Coder::encode(__com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedInputStream *inputStream, __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Streams__::BufferedOutputStreamWrapper *outputStream, __ss_int intervalLength, __com__::__github__::__tarsa__::__tarsalzp__::__Options__::Options *options) {
    __com__::__github__::__tarsa__::__tarsalzp__::__core__::__Encoder__::Encoder *encoder;
    __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Long__::Long *header, *packedOptions;
    __ss_int __170, __171, __172, __173, i;

    Coder::checkInterval(intervalLength);
    encoder = (new __com__::__github__::__tarsa__::__tarsalzp__::__core__::__Encoder__::Encoder(inputStream, outputStream, options));
    header = (new __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Long__::Long((Coder::HeaderValue)->a, (Coder::HeaderValue)->b, (Coder::HeaderValue)->c, (Coder::HeaderValue)->d));

    FAST_FOR(i,0,__ss_int(8),1,170,171)
        outputStream->writeByte((header->a>>__ss_int(8)));
        header->shl8();
    END_FOR

    packedOptions = options->toPacked();

    FAST_FOR(i,0,__ss_int(8),1,172,173)
        outputStream->writeByte((packedOptions->a>>__ss_int(8)));
        packedOptions->shl8();
    END_FOR

    Coder::doEncode(encoder, intervalLength);
    return NULL;
}

void *Coder::doEncode(__com__::__github__::__tarsa__::__tarsalzp__::__core__::__Encoder__::Encoder *encoder, __ss_int intervalLength) {
    __ss_int amountProcessed;

    amountProcessed = __ss_int(0);

    while (__NOT(encoder->encode(intervalLength))) {
        amountProcessed = (amountProcessed+intervalLength);
    }
    encoder->flush();
    return NULL;
}

__com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Long__::Long *Coder::HeaderValue;

void Coder::__static__() {
    HeaderValue = (new __com__::__github__::__tarsa__::__tarsalzp__::__prelude__::__Long__::Long(__ss_int(8331), __ss_int(48031), __ss_int(23314), __ss_int(39102)));
}

void __init() {
    const_0 = new str("Unexpected end of file.");
    const_1 = new str("Wrong file header. Probably not a compressed file.");
    const_2 = new str("Invalid compression options.");
    const_3 = new str("Interval length has to be positive.");
    const_4 = new str("Piotr Tarsa");

    __name__ = new str("Coder");

    __author__ = const_4;
    cl_Coder = new class_("Coder");
    Coder::__static__();
}

} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace
} // module namespace

