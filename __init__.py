# coding=utf-8

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Men of War MDL importer for Blender
# Script Copyright (C) by Björn Martins Paz

# Clear stale bytecode caches so updated .py files are always used
import os as _os, shutil as _shutil
for _cache_dir in (
    _os.path.join(_os.path.dirname(__file__), '__pycache__'),
    _os.path.join(_os.path.dirname(__file__), 'mow', '__pycache__'),
):
    if _os.path.isdir(_cache_dir):
        _shutil.rmtree(_cache_dir, ignore_errors=True)
del _os, _shutil, _cache_dir


bl_info = {
    "name": "Men of War MDL Format",
    "author": "Björn Martins Paz",
    "version": (1, 0, 1),
    "blender": (5, 2, 0),
    "location": "File > Import-Export",
    "description": "Import Men of War MDL",
    "warning": "",
    "support": 'TESTING',
    "category": "Import-Export",
    "doc_url": "https://github.com/anomalyco/io_scene_mdl",
    "tracker_url": "https://github.com/anomalyco/io_scene_mdl/issues",
}

import bpy
from bpy.props import (BoolProperty,
                       FloatProperty,
                       StringProperty,
                       )
from bpy_extras.io_utils import (ImportHelper,
                                  ExportHelper,
                                  path_reference_mode,
                                  axis_conversion,
                                  )


class ImportMDL(bpy.types.Operator, ImportHelper):
    """Load a Men of War MDL File"""
    bl_idname = "import_scene.mdl"
    bl_label = "Import MDL"
    bl_options = {'PRESET', 'UNDO'}

    filename_ext = ".def"
    filter_glob: StringProperty(
            default="*.def",
            options={'HIDDEN'},
            )

    use_animations: BoolProperty(
            name="Animations",
            description="Import animations",
            default=True,
            )

    def execute(self, context):
        from . import import_mdl

        keywords = self.as_keywords()

        # Blender 5.x has a broken from_pydata shim in _bpy_types.py that uses
        # the deprecated polygons.foreach_set('vertices', ...) API. Every C-level
        # mesh operation (bm.to_mesh, update, validate, foreach_set...) fires an
        # RNA notification that calls it, crashing the import.
        #
        # Fix: temporarily replace from_pydata with a no-op for the duration of
        # the import. Our mesh code uses BMesh directly at the C level, so it
        # does not need from_pydata. Restored afterwards so other addons are fine.
        _orig_from_pydata = bpy.types.Mesh.from_pydata

        def _noop_from_pydata(self, vertices, edges, faces, shade_flat=True):
            pass  # silently ignore — mesh data is managed via BMesh

        bpy.types.Mesh.from_pydata = _noop_from_pydata
        try:
            result = import_mdl.load(self, context, **keywords)
        finally:
            bpy.types.Mesh.from_pydata = _orig_from_pydata

        return result

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.prop(self, "use_animations")


class ExportMDL(bpy.types.Operator, ExportHelper):
    """Save a Men of War MDL File"""

    bl_idname = "export_scene.mdl"
    bl_label = 'Export MDL'
    bl_options = {'PRESET'}

    filename_ext = ".mdl; .def"
    filter_glob: StringProperty(
            default="*.mdl;*.def",
            options={'HIDDEN'},
            )

    def execute(self, context):
        self.report({'WARNING'}, "Export functionality not yet implemented")
        return {'CANCELLED'}


def menu_func_import(self, context):
    self.layout.operator(ImportMDL.bl_idname, text="Men of War (.def)")


def menu_func_export(self, context):
    self.layout.operator(ExportMDL.bl_idname, text="Men of War (.def)")


classes = (
    ImportMDL,
    ExportMDL,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()
