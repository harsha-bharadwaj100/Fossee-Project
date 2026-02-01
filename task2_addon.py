bl_info = {
    "name": "FOSSEE Task 2 Addon",
    "author": "GitHub Copilot",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > FOSSEE Task 2",
    "description": "Tools for distributing and merging cubes",
    "category": "Object",
}

import bpy

class FOSSEE_Properties(bpy.types.PropertyGroup):
    """Properties for the FOSSEE addon"""
    number_of_cubes: bpy.props.IntProperty(
        name="Number of Cubes",
        description="Number of cubes to generate",
        default=5,
        min=1
    )

class FOSSEE_OT_DistributeCubes(bpy.types.Operator):
    """Distribute N cubes in a grid"""
    bl_idname = "object.fossee_distribute_cubes"
    bl_label = "Distribute Cubes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print("Distribute Cubes Clicked")
        return {'FINISHED'}

class FOSSEE_OT_DeleteCubes(bpy.types.Operator):
    """Delete generated cubes"""
    bl_idname = "object.fossee_delete_cubes"
    bl_label = "Delete Cubes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print("Delete Cubes Clicked")
        return {'FINISHED'}

class FOSSEE_OT_MergeSelected(bpy.types.Operator):
    """Merge selected meshes if they share a common face"""
    bl_idname = "object.fossee_merge_selected"
    bl_label = "Merge Selected"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print("Merge Selected Clicked")
        return {'FINISHED'}

class FOSSEE_PT_Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "FOSSEE Task 2"
    bl_idname = "VIEW3D_PT_fossee_task2"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
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
