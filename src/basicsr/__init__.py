import os
import sys
import importlib


# `basicsr` isn't compatible with newer versions of pytorch, but
# we can fix that by replacing the missing module
try:
    import torchvision.transforms.functional_tensor  # pyright: ignore[reportMissingImports]
    torchvision.transforms.functional_tensor.rgb_to_grayscale
except (ImportError, AttributeError):
    import types
    from torchvision.transforms.functional import rgb_to_grayscale

    module = types.ModuleType('torchvision.transforms.functional_tensor')
    setattr(module, 'rgb_to_grayscale', rgb_to_grayscale)

    sys.modules[module.__name__] = module

    del module


# Anything importing `basicsr` in the project directory will import
# THIS one, not the real one. Import and cache the REAL `basicsr`
# package and discard this one.

# XXX: It's likely that the below won't play well when building an
# executable or packaging as a distribution because they share the
# same name, but it depends on the build tool. If it places the
# top-level files in the same directory as `site-packages`, this
# and/or the real `basicsr.__init__` would need to be patched during
# the build to make them both namespace packages, or simply prepend
# the original with the above code and exclude this package entirely.

assert __package__ is not None
del sys.modules[__package__]

importlib.invalidate_caches()

assert __path__ and isinstance(__path__, list)
pkg_path = os.path.split(__path__[0])

basicsr = None

for path_hook in reversed(sys.path_hooks):
    for path in reversed(sys.path):
        if path == pkg_path:
            continue

        finder = path_hook(path)
        spec   = finder.find_spec('basicsr')
        if spec is None:
            continue

        assert spec.loader is not None
        basicsr = spec.loader.load_module('basicsr')
        break

    if basicsr is not None:
        break
else:
    raise ImportError('no module named \'basicsr\'')

