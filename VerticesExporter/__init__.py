bl_info = {
    "name": "Vertices Exporter",
    "author": "KRR",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Vertex Exporter",
    "description": "Export vertex coordinates of selected mesh.",
    "category": "Object",
}

if "bpy" in locals():
    import imp
    imp.reload(vertices_exporter)
else:
    from .operators import vertices_exporter

import os
import bpy
from bpy.props import StringProperty, FloatProperty, EnumProperty


class OBJECT_PT_VerticesExporterPanel(bpy.types.Panel):
    bl_label = "Vertices Exporter"
    bl_idname = "OBJECT_PT_vertices_exporter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Vertices Exporter"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        scene = context.scene

        col = layout.column(align = False)
        col.prop(scene, "VE_export_directory", text = "Export Directory")
        col.prop(scene, "VE_file_name", text = "File Name")
        col.separator()
        col.prop(scene, "VE_scale", text = "Scale")
        col.prop(scene, "VE_axis_order", text = "Axis Order")
        col.separator()
        col.operator("object.export_verts")


def init_props():
    scene = bpy.types.Scene
    scene.VE_export_directory = StringProperty(
        name = "Export Directory",
        default = os.path.join(os.path.expanduser("~"), "Desktop")
    )
    scene.VE_file_name = StringProperty(
        name = "File Name",
        default = "verts.txt"
    )
    scene.VE_scale = FloatProperty(
        name = "Scale",
        default = 1.0,
        min = 0.0,
        max = 10.0
    )
    scene.VE_axis_order = EnumProperty(
        name = "Axis Order",
        items = [
            ("XYZ", "X Y Z", "Export in X Y Z order"),
            ("XZY", "X Z Y", "Export in X Z Y order"),
            ("YXZ", "Y X Z", "Export in Y X Z order"),
            ("YZX", "Y Z X", "Export in Y Z X order"),
            ("ZXY", "Z X Y", "Export in Z X Y order"),
            ("ZYX", "Z Y X", "Export in Z Y X order"),
        ],
        default = "XYZ"
    )


def clear_props():
    scene = bpy.types.Scene
    del scene.VE_export_directory
    del scene.VE_file_name
    del scene.VE_scale
    del scene.VE_axis_order


classes = [
    OBJECT_PT_VerticesExporterPanel,
    vertices_exporter.OBJECT_OT_ExportVerts
]


def register():
    init_props()
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    clear_props()
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()