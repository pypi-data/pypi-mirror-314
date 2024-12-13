
#ifndef METATENSOR_TORCH_EXPORT_H
#define METATENSOR_TORCH_EXPORT_H

#ifdef METATENSOR_TORCH_STATIC_DEFINE
#  define METATENSOR_TORCH_EXPORT
#  define METATENSOR_TORCH_NO_EXPORT
#else
#  ifndef METATENSOR_TORCH_EXPORT
#    ifdef metatensor_torch_EXPORTS
        /* We are building this library */
#      define METATENSOR_TORCH_EXPORT __attribute__((visibility("default")))
#    else
        /* We are using this library */
#      define METATENSOR_TORCH_EXPORT __attribute__((visibility("default")))
#    endif
#  endif

#  ifndef METATENSOR_TORCH_NO_EXPORT
#    define METATENSOR_TORCH_NO_EXPORT __attribute__((visibility("hidden")))
#  endif
#endif

#ifndef METATENSOR_TORCH_DEPRECATED
#  define METATENSOR_TORCH_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef METATENSOR_TORCH_DEPRECATED_EXPORT
#  define METATENSOR_TORCH_DEPRECATED_EXPORT METATENSOR_TORCH_EXPORT METATENSOR_TORCH_DEPRECATED
#endif

#ifndef METATENSOR_TORCH_DEPRECATED_NO_EXPORT
#  define METATENSOR_TORCH_DEPRECATED_NO_EXPORT METATENSOR_TORCH_NO_EXPORT METATENSOR_TORCH_DEPRECATED
#endif

/* NOLINTNEXTLINE(readability-avoid-unconditional-preprocessor-if) */
#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef METATENSOR_TORCH_NO_DEPRECATED
#    define METATENSOR_TORCH_NO_DEPRECATED
#  endif
#endif

#endif /* METATENSOR_TORCH_EXPORT_H */
