"""""" # start delvewheel patch
def _delvewheel_patch_1_9_0():
    import os
    if os.path.isdir(libs_dir := os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'psybee.libs'))):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_9_0()
del _delvewheel_patch_1_9_0
# end delvewheel patch

from .psybee import *

# set gstreamer plugin environment variable to site-packages/psybee/.dylibs/
import os
import sys
import platform

if platform.system() == 'Darwin':
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".dylibs")
    os.environ["GST_PLUGIN_PATH"] = path + ":" + os.environ.get("GST_PLUGIN_PATH", "")

__doc__ = psybee.__doc__
if hasattr(psybee, "__all__"):
    __all__ = psybee.__all__
