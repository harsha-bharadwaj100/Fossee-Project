bl_info = {
    "name": "FOSSEE Task 2 Addon",
    "author": "Harsha Bharadwaj",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > FOSSEE Task 2",
    "description": "Tools for distributing and merging cubes",
    "category": "Object",
}

import bpy
import math


class FOSSEE_Properties(bpy.types.PropertyGroup):
    """Properties for the FOSSEE addon"""

    number_of_cubes: bpy.props.IntProperty(
        name="Number of Cubes",
        description="Number of cubes to generate",
        default=5,
        min=1,
    )  # type: ignore


class FOSSEE_OT_DistributeCubes(bpy.types.Operator):
    """Distribute N cubes in a grid"""

    bl_idname = "object.fossee_distribute_cubes"
    bl_label = "Distribute Cubes"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.fossee_props
        n = props.number_of_cubes

        # 1. Validation
        if n > 20:
            self.report({"ERROR"}, "The number is out of range (>20)")
            return {"CANCELLED"}

        # 2. Collection Management
        col_name = "Generated Cubes"
        if col_name in bpy.data.collections:
            collection = bpy.data.collections[col_name]
        else:
            collection = bpy.data.collections.new(col_name)
            context.scene.collection.children.link(collection)

        # 3. Grid Logic
        cols = int(math.ceil(math.sqrt(n)))
        spacing = 1.5

        for i in range(n):
            x = (i % cols) * spacing
            y = (i // cols) * spacing

            # Create cube
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0))
            cube = context.active_object

            # Link to collection
            if collection.name not in cube.users_collection:
                collection.objects.link(cube)

            # Unlink from other collections to clean up
            for col in cube.users_collection:
                if col != collection:
                    col.objects.unlink(cube)

        self.report({"INFO"}, f"Created {n} cubes in '{col_name}'")
        return {"FINISHED"}


class FOSSEE_OT_DeleteCubes(bpy.types.Operator):
    """Delete generated cubes"""

    bl_idname = "object.fossee_delete_cubes"
    bl_label = "Delete Cubes"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        col_name = "Generated Cubes"

        if col_name in bpy.data.collections:
            collection = bpy.data.collections[col_name]

            # List objects strictly to avoid modifying while iterating
            objects_to_delete = [obj for obj in collection.objects]

            for obj in objects_to_delete:
                bpy.data.objects.remove(obj, do_unlink=True)

            bpy.data.collections.remove(collection)
            self.report({"INFO"}, "Deleted cubes and collection")
        else:
            self.report({"INFO"}, "No generated cubes found")

        # Force update
        if context.view_layer:
            context.view_layer.update()

        return {"FINISHED"}


class FOSSEE_OT_MergeSelected(bpy.types.Operator):
    """Merge selected meshes if they share a common face"""

    bl_idname = "object.fossee_merge_selected"
    bl_label = "Merge Selected"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        selected_objects = [
            obj for obj in context.selected_objects if obj.type == "MESH"
        ]

        if len(selected_objects) < 2:
            self.report({"ERROR"}, "Select at least 2 mesh objects")
            return {"CANCELLED"}

        # Store the active object or set one if needed
        if context.active_object not in selected_objects:
            context.view_layer.objects.active = selected_objects[0]

        # 2. Join Objects
        try:
            bpy.ops.object.join()
        except Exception as e:
            self.report({"ERROR"}, f"Join failed: {str(e)}")
            return {"CANCELLED"}

        # 3. Clean Geometry
        # Switch to Edit Mode
        bpy.ops.object.mode_set(mode="EDIT")

        # Select all vertices
        bpy.ops.mesh.select_all(action="SELECT")

        # Merge vertices (Remove Doubles)
        # This merges vertices that are effectively in the same spot,
        # which is the prerequisite for faces to be considered "interior"
        bpy.ops.mesh.remove_doubles(threshold=0.0001)

        # Remove Interior Faces
        # Deselect everything first
        bpy.ops.mesh.select_all(action="DESELECT")

        # Select interior faces (faces shared by >2 manifold edges post-merge)
        bpy.ops.mesh.select_interior_faces()

        # Delete the selected faces
        bpy.ops.mesh.delete(type="FACE")

        # Return to Object Mode
        bpy.ops.object.mode_set(mode="OBJECT")

        self.report(
            {"INFO"}, f"Merged {len(selected_objects)} objects and cleaned geometry"
        )
        return {"FINISHED"}


class FOSSEE_PT_Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""

    bl_label = "FOSSEE Task 2"
    bl_idname = "VIEW3D_PT_fossee_task2"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FOSSEE Task 2"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.fossee_props

        # Input
        layout.prop(props, "number_of_cubes")

        # Buttons
        layout.separator()
        layout.operator("object.fossee_distribute_cubes")
        layout.operator("object.fossee_delete_cubes")

        layout.separator()
        layout.operator("object.fossee_merge_selected")


classes = (
    FOSSEE_Properties,
    FOSSEE_OT_DistributeCubes,
    FOSSEE_OT_DeleteCubes,
    FOSSEE_OT_MergeSelected,
    FOSSEE_PT_Panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.fossee_props = bpy.props.PointerProperty(type=FOSSEE_Properties)


def unregister():
    if hasattr(bpy.types.Scene, "fossee_props"):
        del bpy.types.Scene.fossee_props

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
