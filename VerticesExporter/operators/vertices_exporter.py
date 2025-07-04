import os
from mathutils import Vector
import bpy
import bmesh


class OBJECT_OT_ExportVerts(bpy.types.Operator):
    bl_idname = "object.export_verts"
    bl_label = "Export"
    bl_description = "Export vetices"
    bl_options = {"REGISTER", "UNDO"}

    @staticmethod
    def reorder_vector(vec: Vector, order: str) -> Vector:
        axis_map = {
            'X': vec.x,
            'Y': vec.y,
            'Z': vec.z
        }
        return Vector([axis_map[axis] for axis in order])

    def invoke(self, context, event):
        scene = context.scene
        file_path = os.path.join(scene.VE_export_directory, scene.VE_file_name)

        if os.path.exists(file_path):
            return context.window_manager.invoke_confirm(self, event)
        else:
            return self.execute(context)

    def execute(self, context):
        obj = context.object
        if obj is None or obj.type != "MESH":
            self.report({'ERROR'}, "Selected object is not a mesh.")
            return {"CANCELLED"}

        scene = context.scene
        file_path = os.path.join(scene.VE_export_directory, scene.VE_file_name)
        scale = scene.VE_scale
        order = scene.VE_axis_order

        mesh = obj.data
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bm.verts.ensure_lookup_table()
        verts = sorted(bm.verts, key=lambda v: v.index)

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                for v in verts:
                    coord = OBJECT_OT_ExportVerts.reorder_vector((obj.matrix_world @ v.co) * scale, order)
                    f.write(f"{coord.x:.6f} {coord.y:.6f} {coord.z:.6f}\n")
        except Exception as e:
            self.report({"ERROR"}, f"File write failed: {e}")
            return {"CANCELLED"}
        finally:
            bm.free()

        self.report({"INFO"}, f"Exported to {file_path}")
        return {"FINISHED"}
