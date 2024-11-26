bl_info = {
    "name": "Bone Renamer",
    "blender": (4, 0, 0),
    "category": "Armature",
    "version": (1, 0),
    "author": "Boonsak Watanavisit",
    "description": "Rename bones in selected armature",
}

import bpy
import json
from bpy.props import StringProperty, CollectionProperty, BoolProperty, PointerProperty
from bpy_extras.io_utils import ImportHelper, ExportHelper

class BoneMappingItem(bpy.types.PropertyGroup):
    old_name: StringProperty(name="Old Name")
    new_name: StringProperty(name="New Name")
    selected: BoolProperty(name="Select", default=True)

class LoadBoneMappings(bpy.types.Operator, ImportHelper):
    bl_idname = "bone_renamer.load_mappings"
    bl_label = "Load Bone Mappings"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".json"

    filter_glob: StringProperty(
        default="*.json",
        options={'HIDDEN'}
    )

    def execute(self, context):
        context.scene.bone_mappings.clear()
        bone_mappings = load_bone_mappings(self.filepath)
        for mapping in bone_mappings:
            item = context.scene.bone_mappings.add()
            item.old_name = mapping["old_name"]
            item.new_name = mapping["new_name"]
        return {'FINISHED'}

class SaveBoneMappings(bpy.types.Operator, ExportHelper):
    bl_idname = "bone_renamer.save_mappings"
    bl_label = "Save Bone Mappings"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".json"

    filter_glob: StringProperty(
        default="*.json",
        options={'HIDDEN'}
    )

    def execute(self, context):
        bone_mappings = []
        for item in context.scene.bone_mappings:
            bone_mappings.append({"old_name": item.old_name, "new_name": item.new_name})
        save_bone_mappings(self.filepath, bone_mappings)
        return {'FINISHED'}

class AddBoneMapping(bpy.types.Operator):
    bl_idname = "bone_renamer.add_mapping"
    bl_label = "Add Bone Mapping"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        item = context.scene.bone_mappings.add()
        item.old_name = ""
        item.new_name = ""
        return {'FINISHED'}

class RemoveBoneMapping(bpy.types.Operator):
    bl_idname = "bone_renamer.remove_mapping"
    bl_label = "Remove Bone Mapping"
    bl_options = {'REGISTER', 'UNDO'}

    index: bpy.props.IntProperty()

    def execute(self, context):
        context.scene.bone_mappings.remove(self.index)
        return {'FINISHED'}

class SwapBoneMappings(bpy.types.Operator):
    bl_idname = "bone_renamer.swap_mappings"
    bl_label = "Swap Bone Mappings"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for item in context.scene.bone_mappings:
            item.old_name, item.new_name = item.new_name, item.old_name
        return {'FINISHED'}

class MoveBoneMapping(bpy.types.Operator):
    bl_idname = "bone_renamer.move_mapping"
    bl_label = "Move Bone Mapping"
    bl_options = {'REGISTER', 'UNDO'}

    index: bpy.props.IntProperty()
    direction: bpy.props.EnumProperty(items=[('UP', 'Up', ''), ('DOWN', 'Down', '')])

    def execute(self, context):
        if self.direction == 'UP':
            new_index = max(0, self.index - 1)
        elif self.direction == 'DOWN':
            new_index = min(len(context.scene.bone_mappings) - 1, self.index + 1)

        context.scene.bone_mappings.move(self.index, new_index)
        return {'FINISHED'}

class ClearBoneMappings(bpy.types.Operator):
    bl_idname = "bone_renamer.clear_mappings"
    bl_label = "Clear Bone Mappings"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.bone_mappings.clear()
        return {'FINISHED'}

class LoadArmatureBones(bpy.types.Operator):
    bl_idname = "bone_renamer.load_armature_bones"
    bl_label = "Load Armature Bones"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armature = context.scene.target_armature

        if armature is None:
            self.report({'ERROR'}, "Please select an armature.")
            return {'CANCELLED'}

        if armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Selected object is not an armature.")
            return {'CANCELLED'}

        context.scene.bone_mappings.clear()
        for bone in armature.data.bones:
            item = context.scene.bone_mappings.add()
            item.old_name = bone.name
            item.new_name = bone.name
        return {'FINISHED'}

class RenameBones(bpy.types.Operator):
    bl_idname = "bone_renamer.rename_bones"
    bl_label = "Rename Bones"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armature = context.scene.target_armature

        if armature is None:
            self.report({'ERROR'}, "Please select an armature.")
            return {'CANCELLED'}

        if armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Selected object is not an armature.")
            return {'CANCELLED'}

        for item in context.scene.bone_mappings:
            if item.selected and item.old_name in armature.data.bones:
                armature.data.bones[item.old_name].name = item.new_name
                print(f"Renamed bone '{item.old_name}' to '{item.new_name}'")
            elif item.old_name not in armature.data.bones:
                print(f"Bone '{item.old_name}' not found in the armature.")
        return {'FINISHED'}

class BoneRenamerPanel(bpy.types.Panel):
    bl_label = "Bone Renamer"
    bl_idname = "VIEW3D_PT_bone_renamer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "target_armature", text="Target Armature")

        box = layout.box()
        for index, item in enumerate(context.scene.bone_mappings):
            row = box.row()
            row.prop(item, "selected", text="")
            row.prop(item, "old_name", text="")
            row.prop(item, "new_name", text="")
            move_up_op = row.operator("bone_renamer.move_mapping", text="", icon='TRIA_UP')
            move_up_op.index = index
            move_up_op.direction = 'UP'
            move_down_op = row.operator("bone_renamer.move_mapping", text="", icon='TRIA_DOWN')
            move_down_op.index = index
            move_down_op.direction = 'DOWN'
            remove_op = row.operator("bone_renamer.remove_mapping", text="", icon='X')
            remove_op.index = index

        row = layout.row()
        row.operator("bone_renamer.add_mapping", text="Add Bone Mapping")
        row.operator("bone_renamer.load_mappings", text="Load JSON File")
        row.operator("bone_renamer.save_mappings", text="Save JSON File")
        row.operator("bone_renamer.clear_mappings", text="Clear List")
        row.operator("bone_renamer.load_armature_bones", text="Load Armature Bones")

        row = layout.row()
        row.operator("bone_renamer.swap_mappings", text="Swap Bone Mappings")

        row = layout.row()
        rename_op = row.operator("bone_renamer.rename_bones", text="Rename Bones", icon='FILE_TICK')
        if not context.scene.bone_mappings:
            rename_op.enabled = False

def load_bone_mappings(json_file_path):
    """Load bone mappings from a JSON file."""
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        return data.get("bone_mappings", [])

def save_bone_mappings(json_file_path, bone_mappings):
    """Save bone mappings to a JSON file."""
    with open(json_file_path, 'w') as file:
        json.dump({"bone_mappings": bone_mappings}, file, indent=4)

classes = (
    BoneMappingItem,
    LoadBoneMappings,
    SaveBoneMappings,
    AddBoneMapping,
    RemoveBoneMapping,
    SwapBoneMappings,
    MoveBoneMapping,
    ClearBoneMappings,
    LoadArmatureBones,
    RenameBones,
    BoneRenamerPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.bone_mappings = CollectionProperty(type=BoneMappingItem)
    bpy.types.Scene.target_armature = PointerProperty(type=bpy.types.Object, name="Target Armature")

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.bone_mappings
    del bpy.types.Scene.target_armature

if __name__ == "__main__":
    register()