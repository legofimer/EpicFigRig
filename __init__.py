# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

#add-on info

bl_info = {
    "name": "The EpicFigRig - JabLab Version",
    "author": "Jambo, Owenator Productions, Golden Ninja Ben, IX Productions, JabLab, and Citrine's Animations",
    "version": (1, 1, 1),
    "blender": (3, 3, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "An Epic Minifigure Rig",
    "wiki_url": "https://github.com/BlenderBricks/EpicFigRig/tree/jablab-releases",
    "category": "Animation",
}

selected_armature = "FinishedRig"

import os
import bpy, mathutils
from bpy.props import BoolProperty, IntProperty
from bpy.types import PropertyGroup, Panel, Scene
import addon_utils

addon_dirc = os. path .dirname (os .path .realpath (__file__))
#PANELS

class EpicFigRigPanel(bpy.types.Panel):
    
    bl_label = "The EpicFigRig"
    bl_idname = "EPIC_FIGRIG_PT_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EpicFigRig'
    
    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        row = box.row()
        row.operator("wm.url_open", text="User Manual", icon= 'URL', emboss= False).url = "https://docs.google.com/document/d/1wWlGkeNHBnmPA1siEARibdjcdEdBDNlHe-tcdELbq8M/edit?usp=sharing"
        row = layout.row()
        box = layout.box()
        row = box.row()
        row.operator("wm.url_open", text="JabLab Roadmap", icon= 'URL', emboss= False).url = "https://docs.google.com/document/d/1kJMUFe73h4Af69KkrOU4y_3KU6dmt_5DmBlqC_X1Q5E/edit?usp=sharing"
        row = layout.row()
        row.label(text= "Active: Object:")
        #row = layout.row()
        #row.label(text= bpy.context.object.data.name, icon= 'OUTLINER_OB_ARMATURE') #emboss= False)
        
        row = layout.row()
        row.operator('auto.rig')
        row = layout.row()
        row.label(text= "Rig Settings:", icon= 'OPTIONS')
        row = layout.row()
        layout = self.layout
        row = layout.row(align=True)        
        row.operator('main.tab')
        row.operator('advanced.tab')
        row = layout.row()

######MAIN TAB######

class EpicButtons(bpy.types.Panel):
        
    bl_idname = "EPIC_PT_BUTTONS"
    bl_label = "Epic Buttons"
    bl_parent_id = "EPIC_FIGRIG_PT_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EpicFigRig'
    
    @classmethod
    def poll(cls, context):
        #if bpy.context.object.data["RigTabs"] == 0:
        if bpy.context.scene.EpicRigTabs == 0:
            return True
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        
        row = layout.row()
        row.label(text= "Accessory Snapping:", icon= 'SNAP_ON')
        row = layout.row(align=True)
        row.operator('snap_left.add')
        row.operator('snap_right.add')
        row = layout.row(align=True)
        row.operator('snap_head.add')
        #pivot buttons
        layout.label(text="Pivot Foot Switch:", icon= 'ARROW_LEFTRIGHT')
        row = layout.row(align=True)
        row.operator('pivot.left')
        row.operator('pivot.right')
        row = layout.row()
        row.operator('reset.pivot')
        row = layout.row(align=True)
        row.label(text= "Master Bone Control:")
        row = layout.row()
        row.operator('rig.reset')
        row = layout.row()
        row.operator('snap.masterbone') 
       
class RigSettings(bpy.types.Panel):
    
    bl_label = "Rig Settings"
    bl_idname = "RIG_PT_SETTINGS"
    bl_parent_id = "EPIC_FIGRIG_PT_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EpicFigRig'  
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        #if bpy.context.object.data["RigTabs"] == 3:
        if bpy.context.scene.EpicRigTabs == 3:
            return True
    
    def draw(self, context):
        #layout = self.layout
        #wm = context.window_manager
        
        layout = self.layout
        row = layout.row()
        sub = row.row()
        sub.enabled = True
        #layout.use_property_split = True
        #layout.use_property_decorate = True
        
        
        
        #layout.use_property_decorate = True
        
        
        for obj in bpy.context.selected_objects:
               
                
            if obj.type == 'ARMATURE':
                global selected_armature
                selected_armature = obj.name
                check_prop = True
            else:
                check_prop = False
        if check_prop == False:
            row.label(text = "(Select an Armature for Settings)")
            
        if check_prop == True:
            sub = row.row()
            row = layout.row()
            row.prop(context.active_object.data, '["Head Accessory Bone Scale"]', slider=True)
            row = layout.row()
            row.prop(context.active_object.data, '["Head Bone Scale"]', slider=True)
            row = layout.row()
            row.prop(context.active_object.data, '["Head Bone Transform"]', slider=True)
            row = layout.row()
            row.prop(context.active_object.data, '["Torso Bone Scale"]', slider=True)
            row = layout.row()
            row.prop(context.active_object.data, '["Second Master Bone"]', slider=True)
            row = layout.row()
            row.prop(context.active_object.data, '["Locators"]', slider=True)

class SmearSlider(bpy.types.Panel):
    
    bl_label = "Smears"
    bl_idname = "SMEAR_SLIDER"
    bl_parent_id = "EPIC_FIGRIG_PT_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EpicFigRig'  
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        #if bpy.context.object.data["RigTabs"] == 0:
        if bpy.context.scene.EpicRigTabs == 0:
            return True
        
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.active_object.data, '["LLegSmear"]', slider=True)
        row = layout.row() 
        row.prop(context.active_object.data, '["RLegSmear"]', slider=True)
        row = layout.row()
        row.prop(context.active_object.data, '["LArmSmear"]', slider=True)
        row = layout.row()
        row.prop(context.active_object.data, '["RArmSmear"]', slider=True)

class ArmMenu(bpy.types.Panel):
    
    @classmethod
    def poll(cls, context):
        #if bpy.context.object.data["RigTabs"] == 0:
        if bpy.context.scene.EpicRigTabs == 0:
            return True
                        
    bl_label = "Arm Menu"
    bl_idname = "ARM_MENU"
    bl_parent_id = "EPIC_FIGRIG_PT_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EpicFigRig'  
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        #layout = self.layout
        #wm = context.window_manager            
    
        layout = self.layout
        row = layout.row()
        sub = row.row()
        sub.enabled = True
        #layout.use_property_split = True
        #layout.use_property_decorate = True
                
        for obj in bpy.context.selected_objects:
                               
            if obj.type == 'ARMATURE':
                global selected_armature
                selected_armature = obj.name
                check_prop = True
            else:
                check_prop = False
                
        if check_prop == False:
            row.label(text = "(Select an Armature for Settings)")
            
        if check_prop == True:
            """row = layout.row()
            row.prop(context.active_object.data, '["ArmIK"]', slider=True)
            row = layout.row()
            if bpy.data.armatures[bpy.context.object.data.name]["ArmIK"] == 0:
                sub.enabled = False
            else:
                sub.enabled == True
                row = self.layout.row()
                sub = row.row()
                sub.prop(context.active_object.data, '["IK Arm Socket Lock"]', slider=True)"""

            sub = row.row()
            row = layout.row()
            row.prop(context.active_object.data, '["Lepin Hands"]', slider=True)
            row = layout.row()
            layout.label(text="Left Arm:", icon= 'EVENT_L')
           
            row = layout.row()
            row.prop(context.active_object.data, '["LeftArmIK"]', slider=True)
            if bpy.data.armatures[bpy.context.object.data.name]["LeftArmIK"] == 0:
                sub.enabled = True
                row = self.layout.row()
                sub = row.row()
                row = layout.row(align=True)
                row.operator('fk_to.ik_larm')
                row = layout.row()

            else:
                sub.enabled == True
                row = self.layout.row()
                sub = row.row()
                row = layout.row(align=True)
                row.operator('ik_to.fk_larm')
                row = layout.row()
                row.prop(context.active_object.data, '["IK Arm Socket Lock"]', slider=True)
                row = layout.row()
           
            row = layout.row()
            row.prop(context.active_object.data, '["Invert Left Arm"]', slider=True)
            row = layout.row()
            row.prop(context.active_object.data, '["Mirror Left Arm"]', slider=True)
            row = layout.row()
            row.prop(context.active_object.data, '["LArmSmear"]', slider=True)
            layout.label(text="Right Arm:", icon= 'EVENT_R')

            row = layout.row()
            row.prop(context.active_object.data, '["RightArmIK"]', slider=True)
            if bpy.data.armatures[bpy.context.object.data.name]["RightArmIK"] == 0:
                sub.enabled = True
                row = self.layout.row()
                sub = row.row()
                row = layout.row(align=True)
                row.operator('fk_to.ik_rarm')
                row = layout.row()

            else:
                sub.enabled == True
                row = self.layout.row()
                sub = row.row()
                row = layout.row(align=True)
                row.operator('ik_to.fk_rarm')
                row = layout.row()
                row.prop(context.active_object.data, '["IK Arm Socket Lock"]', slider=True)
                row = layout.row()

            row = layout.row()
            row.prop(context.active_object.data, '["Invert Right Arm"]', slider=True)
            row = layout.row()
            row.prop(context.active_object.data, '["Mirror Right Arm"]', slider=True)
            row = layout.row()
            row.prop(context.active_object.data, '["RArmSmear"]', slider=True)


class LegMenu(bpy.types.Panel):
    
    bl_label = "Leg Menu"
    bl_idname = "LEG_MENU"
    bl_parent_id = "EPIC_FIGRIG_PT_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EpicFigRig'  
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        #if bpy.context.object.data["RigTabs"] == 0:
        if bpy.context.scene.EpicRigTabs == 0:
            return True

    def draw(self, context):
        #layout = self.layout
        #wm = context.window_manager
        
        layout = self.layout
        row = layout.row()
        sub = row.row()
        sub.enabled = True
        #layout.use_property_split = True
        #layout.use_property_decorate = True

        
        for obj in bpy.context.selected_objects:
               
                
            if obj.type == 'ARMATURE':
                global selected_armature
                selected_armature = obj.name
                check_prop = True
            else:
                check_prop = False
                
        if check_prop == False:
            row.label(text = "(Select an Armature for Settings)")
            
        if check_prop == True:
            
            layout.label(text="Left Leg:", icon= 'EVENT_L')
            row = layout.row()
            sub = row.row()
            row = layout.row()
            row.prop(context.active_object.data, '["LeftLegIK"]', slider=True)
            if bpy.data.armatures[bpy.context.object.data.name]["LeftLegIK"] == 0:
                sub.enabled = True
                row = self.layout.row()
                sub = row.row()
                row = layout.row(align=True)
                row.operator('fk_to.ik_lleg')
                row = layout.row()

            else:
                sub.enabled == True
                row = self.layout.row()
                sub = row.row()
                row = layout.row(align=True)
                row.operator('ik_to.fk_lleg')
                row = layout.row()
                  
            row = layout.row()
            row.prop(context.active_object.data, '["Invert Left Leg"]', slider=True)
            row = layout.row()
            row.prop(context.active_object.data, '["LLegSmear"]', slider=True)
            row = layout.row()           

            sub = row.row()
            row = layout.row()
            layout.label(text="Right Leg:", icon= 'EVENT_R')
            row = layout.row()
            row.prop(context.active_object.data, '["RightLegIK"]', slider=True)
            if bpy.data.armatures[bpy.context.object.data.name]["RightLegIK"] == 0:
                sub.enabled = True
                row = self.layout.row()
                sub = row.row()
                row = layout.row(align=True)
                row.operator('fk_to.ik_rleg')
                row = layout.row()

            else:
                sub.enabled == True
                row = self.layout.row()
                sub = row.row()
                row = layout.row(align=True)
                row.operator('ik_to.fk_rleg')
                row = layout.row()

            row = layout.row()
            row.prop(context.active_object.data, '["Invert Right Leg"]', slider=True)
            row = layout.row()
            row.prop(context.active_object.data, '["RLegSmear"]', slider=True)
            row = layout.row()

######ADVANCED TAB######

class BoneAdjust(bpy.types.Panel):
    
    bl_label = "Bone Adjustments"
    bl_idname = "BONE_ADJUST"
    bl_parent_id = "EPIC_FIGRIG_PT_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EpicFigRig'  
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        #if bpy.context.object.data["RigTabs"] == 1:
        if bpy.context.scene.EpicRigTabs == 1:
            return True
        
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.active_object.data, '["Head Accessory Bone Scale"]', slider=True)
        row = layout.row()
        row.prop(context.active_object.data, '["Head Bone Scale"]', slider=True)
        row = layout.row()
        row.prop(context.active_object.data, '["Head Bone Transform"]', slider=True)
        row = layout.row()
        row.prop(context.active_object.data, '["Torso Bone Scale"]', slider=True)
        row = layout.row()
        row.prop(context.active_object.data, '["Leg Height"]', slider=True)
        row = layout.row()
        
class BoneVis(bpy.types.Panel):
    
    bl_label = "Bone Visibility"
    bl_idname = "BONE_VISIBILITY"
    bl_parent_id = "EPIC_FIGRIG_PT_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EpicFigRig'  
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        #if bpy.context.object.data["RigTabs"] == 1:
        if bpy.context.scene.EpicRigTabs == 1: 
            return True
        
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.active_object.data, '["Second Master Bone"]', slider=True)
        row = layout.row()
        row.prop(context.active_object.data, '["Locators"]', slider=True)
        
#BUTTONS 

"""#Naming
class Naming(bpy.types.Operator):
    
    bl_label = "Name Minifigure"
    bl_idname = 'name.mini'    
    
    mininame = bpy.props.StringProperty(name = "Minifigure Name:", default= "")
    
    def execute(self, context):
        mname = self.mininame
        
        return {'FINISHED'} 
    
    #Opens naming dialogue window
    def invoke(self, context, event):
        
        return context.window_manager.invoke_props_dialog(self)
"""
#AutoRig
class AutoRig(bpy.types.Operator):
    """Autorig Selected Minifgure - YOU MUST DELETE THE EMPTY!"""
    bl_label = "  Rig Selected Minifigure  "
    bl_idname = 'auto.rig'
    
    #mininame: bpy.props.StringProperty(name = "Minifigure Name:", default= "")
    
    def execute(self, context):        
        
        child = True
        
        #Naming()
        
        #mname = self.mininame
        bpy.context.view_layer.objects.active = bpy.context.selected_objects[1]
        col = bpy.context.active_object.users_collection[0]
        mname = col.name
        
        collections = bpy.context.view_layer.layer_collection.children

        for collection in collections:
            if collection.name == mname:
                bpy.context.view_layer.active_layer_collection = collection
        
        
        def driverCreate(context, object, armatures, path, Bo_nus, path2, expression, x, y, xx, yy):
            obj = bpy.data.objects[object]
            dwive = obj.driver_add("hide_viewport")
            driver = dwive.driver
            
            var = driver.variables.new()
            
            var.type = 'SINGLE_PROP'
            var.name = "hide"

            target = var.targets[0]

            target.id_type = 'ARMATURE'

            b = bpy.data.armatures[armatures]

            target.id = b

            target.data_path = path

            #numba 2
            if Bo_nus == True:
                var = driver.variables.new()
            
                var.type = 'SINGLE_PROP'
                var.name = "hide2"

                target = var.targets[0]

                target.id_type = 'ARMATURE'

                b = bpy.data.armatures[armatures]

                target.id = b

                target.data_path = path2

            driver.expression = expression

            curvyf = obj.animation_data.drivers[0]

            fcrue = curvyf.keyframe_points

            fcrue.add(2)

            fcrue[0].co = (x, y)
            fcrue[0].interpolation = 'CONSTANT'
            fcrue[1].co = (xx, yy)
            fcrue[1].interpolation = 'CONSTANT'

            #next

            obj2 = bpy.data.objects[object]
            dwive2 = obj2.driver_add("hide_render")
            driver2 = dwive2.driver
            
            var2 = driver2.variables.new()
            
            var2.type = 'SINGLE_PROP'
            var2.name = "hide"

            target2 = var2.targets[0]

            target2.id_type = 'ARMATURE'

            b = bpy.data.armatures[armatures]

            target2.id = b

            target2.data_path = path

            #numba 2
            if Bo_nus == True:
                var2 = driver2.variables.new()
            
                var2.type = 'SINGLE_PROP'
                var2.name = "hide2"

                target2 = var2.targets[0]

                target2.id_type = 'ARMATURE'

                b = bpy.data.armatures[armatures]

                target2.id = b

                target2.data_path = path2

            driver2.expression = expression

            curvyf = obj2.animation_data.drivers[0]

            fcrue = curvyf.keyframe_points

            fcrue.add(2)

            fcrue[0].co = (x, y)
            fcrue[0].interpolation = 'CONSTANT'
            fcrue[1].co = (xx, yy)
            fcrue[1].interpolation = 'CONSTANT'
        
        #remove empty
        if bpy.context.selected_objects[0].parent == True:

            empty_name = bpy.context.selected_objects[0].parent.name
            empty = bpy.data.objects[empty_name]
            
            bpy.data.objects.remove(empty)

        def append_rig():
            path = addon_dirc + "/Append.blend/Collection/"
            object_name = "The EpicFigRig"
            bpy.ops.wm.append(filename = object_name, directory = path)

        def append_cape():
            path = addon_dirc + "/Cape_Rig.blend/Collection/"
            object_name = "CapeRig"
            bpy.ops.wm.append(filename = object_name, directory = path)
            #path = addon_dirc + "/Cape_Rig.blend/Object/"
            #bpy.ops.wm.append(filename = currentcape, directory = path)

        leg_l = ["3817", "20926", "24083", "37364p2", "37366"]
        leg_r = ["3816", "20932", "24082", "37364p1", "2532", "37365"]
        head_epic = ["24581", "3626", "28621", "94590", "28650", "28649", "26683", "93248",
        "30480", "30378", "98103", "64804", "92743", "1735", "24601", "24629", "98365", 
        "98384", "93068", "19729", "20613", "41201", "18828", "65431"]
        arm_r = ["16000", "3818", "62691"]
        arm_l = ["16001", "3819", "62691"]
        torso = ["3814"]
        torso_gear = ["95348", "61976", "6132", "93223", "93069", "10052", "10065", "42446", "48724", "92590", "4523", "2524", "12397", "4498", "2526", "30133", "2610", "97895", "38781", "3838", "3840", "2587", "72326",  "11260", "15339", "30091", "15490", "15428", "34685", "24135", "18986", "15423", "98132", "24097", "22402", "28350", "12618", "19723", "4524", "11097", "26966", "93250", "99250", "26073", "4736", "11438", "15406", "18827", "27325", "10183", "6158", "27148", "27151", "27147", "98722", "64802", "23983", "28716", "25376", "30174", "24588", "15086", "13791", "20566", "24217", "88295", "39260", "41637", "34706", "41811", "39796", "41162", "41202", "37822", "65183", "79786"]
        hand_epic = ["3820", "2531", "9532"]
        child_leg = ["37365", "37366" "16709", "37679", "41879"]
        child_leg_single = ["16709", "37679", "41879"]
        dress_brick = ["3678"[:4], "75103", "98376", "19859"]
        regular_dress = ["36036", "95351"]
        head_accessory = ["64798", "64807", "85974", "887990", "87991", "87995", "88283", "88286", "92081", "92083", "93217", "93562", "93563", "18228", "99240", "11908", "99930", "99248",
        "98726", "10301", "10166", "10048", "10048", "10055", "10066", "11256", "12893", "13768", "13251", "13664", "13785", "13750", "13765", "13766", "15443", "15427", "15491", "15500",
        "15485", "17346", "17630", "18858", "21787", "20688", "20877", "20595", "20597", "20596", "21777", "21268", "21269", "21778", "23186", "23187", "24072", "25775", "28798", "25378",
        "25379", "26139", "25972", "27186", "27385", "27160", "28551", "28144", "28149", "27323", "28664", "28432", "28432", "25411", "25412", "25409", "28430", "34316", "25405", "34693", 
        "36060", "36489", "37823", "40938", "3901", "62810", "40239", "3625", "96859", "62711", "6093", "62696", "59363", "95225", "6025", "99245", "92746", "61183", "40240", "98371", "20603", 
        "21788", "21789", "92756", "40233", "24071", "28139", "65425", "35182", "35620", "49362", "92259", "18637", "15675", "18640", "92255", "19196", "65471", "65463", "66912", "3842", "50665", "16599", "30124", "49663",          "36293", "93560", "35458",
        "15851", "3834", "90541", "4505", "26079", "4506", "2338", "3844", "3896", "48493",
        "30273", "89520", "4503", "71015", "2544", "2528", "2543", "23973", "30048", "93554",
        "2545", "40235", "18822", "3629", "30167", "61506", "15424", "13565",  "13788", "13746",
        "6131", "4485", "86035", "11303", "93219", "35660", "11258", "3878", "3624", "41334",
        "3898", "30287", "95678", "36933", "62537", "46303", "3833", "16178", "16175", "98289",
        "99254", "43057", "22380", "85975", "90386", "98381", "30370", "61189", "11217", "15308",
        "30369", "23947", "20904", "20905", "20950", "98119", "21829", "30561", "16497", "57900",
        "52345", "20908", "20954", "21557", "19916", "19917", "87610", "87571", "60768", "92761",
        "6030", "10051", "10056d1", "13767", "10173", "30171", "15530", "17351", "99244", "25971",
        "18831", "66972", "18819", "24076", "25977", "29575", "35697", "20695", "95674", "95319",
        "13789", "30381", "10113", "27161", "18987", "98729", "27326", "10907", "10908", "28631",
        "20917", "17016", "11620", "10909", "15554", "33862", "18936", "19303", "25264", "19026",
        "65589", "19730", "18962", "98130", "96034", "98133", "19857", "24496", "24504", "40925",
        "65072", "93059", "26007", "98128", "25407", "25742", "25743", "25748", "25113", "25114",
        "28679", "30668", "96204", "18984", "90388", "24073", "19861", "90392", "98366", "25978",
        "15404", "98378", "22425", "13792", "13787", "11265", "30172", "27955", "37038", "10164",
        "34704", "54001", "52684", "93557", "65532", "30926", "67145", "66917", "11420"]

        head_clothing_accessories = ["91190", "64647", "30126", "98379", "12886", "33322",
        "25974", "14045", "25634", "13665", "24131", "44553", "41944", "54568", "87696",
        "87695", "11437", "22411", "88964", "39262", "35183"]

        head_clothing_visors = ["2447", "41805", "23318", "89159", "30170", "6119", "30090", 
        "15446", "2594", "22393", "22395", "22400", "22401", "22394", "23851", "28976",]
        
        capes = ["20547","23901","29453","34721","50231","50525","56630","56630","65384","99464"]
        
        #capes_apend = ["20547uv.001.append","23901uv.001.append","29453uv.001.append","34721uv.001.append","50231uv.001.append","50525uv.001.append","56630uv.001.append","56630uv.002.append","65384uv.001.append","99464uv.001.append"] 

        selected_objects = bpy.context.selected_objects
        loc = bpy.context.selected_objects[0]
        
  

        for y in selected_objects:
                if "3814" in y.data.name:
                    loc = y

        child = False 
        for fig in bpy.context.selected_objects:
            
            for num in child_leg:
                #if num in fig.data.name:
                if num[:5] in fig.data.name:
                    child = True

        append_rig()      
        
        all_objects = bpy.data.objects
        rig = all_objects['Rig']
        arma = bpy.data.objects['Rig']
        arma_edit = arma.data.edit_bones

        
        
        rig.location = loc.location

        collections = bpy.data.collections
        h = collections['BoneShapes']
        h.hide_viewport = True

        

        def parent( Bone_name, Dou_ble, Smear_prop):

            fig.select_set(True)
            fig.data = fig.data.copy()
            if Dou_ble == True:
                driverCreate(bpy.context, fig.name, rig.name, '["SmearsTest"]', True, Smear_prop, "hide + hide2", 0, 0, 1, 1)
            else:
                driverCreate(bpy.context, fig.name, rig.name, '["SmearsTest"]', False, Smear_prop, "hide", 0, 0, 1, 1)


            rig.select_set(True)
            bpy.context.view_layer.objects.active = rig
            rig.data.bones.active = rig.data.bones[Bone_name]
            bpy.ops.object.parent_set(type='BONE', keep_transform=True)
            bpy.ops.object.select_all(action='DESELECT')
            
        
        for fig in selected_objects:

            #CHILD_LEG
            for num in child_leg_single:
                if num in fig.data.name:
                    parent("Torso", False, '["LLegSmear"]')
                    bpy.context.object.data.bones["RightFootIK"].hide = True
                    bpy.context.object.data.bones["LeftFootIK"].hide = True
                    bpy.context.object.data.bones["RightLeg"].hide = True
                    bpy.context.object.data.bones["LeftLeg"].hide = True

            #DRESS_BRICK
            for num in dress_brick:
                if num in fig.data.name:
                    parent("Torso", False, '["LLegSmear"]')
                    bpy.context.object.data.bones["RightFootIK"].hide = True
                    bpy.context.object.data.bones["LeftFootIK"].hide = True
                    bpy.context.object.data.bones["RightLeg"].hide = True
                    bpy.context.object.data.bones["LeftLeg"].hide = True

            #REGULAR_DRESS
            for num in regular_dress:
                if num in fig.data.name:
                    parent("Torso", False, '["LLegSmear"]')
                    bpy.context.object.data.bones["RightFootIK"].hide = True
                    bpy.context.object.data.bones["LeftFootIK"].hide = True
                    bpy.context.object.data.bones["RightLeg"].hide = True
                    bpy.context.object.data.bones["LeftLeg"].hide = True

            #LEFT_LEG
            for num in leg_l:
                if num in fig.data.name:
                    parent("LeftLegInvert", True, '["LLegSmear"]')
                    bpy.data.objects["LlegS"].material_slots[0].material = fig.material_slots[0].material



            #RIGHT_LEG
            for num in leg_r:
                if num in fig.data.name:
                    parent("RightLegInvert", True, '["RLegSmear"]')
                    bpy.data.objects["RlegS"].material_slots[0].material = fig.material_slots[0].material

            #IK_HIP
            if "3815" in fig.data.name:
                parent("Torso", False, '["LLegSmear"]')

            #TORSO_GEAR
            for num in torso_gear:
                if num in fig.data.name:
                    parent("Torso Rock", False, '["LLegSmear"]')
                    bpy.context.object.data["Head Bone Transform"] = 1.5
                    bpy.context.object.data["Torso Bone Scale"] = .75

            #TORSO
            for num in torso:
                if num in fig.data.name:
                    parent("Torso Rock", False, '["LLegSmear"]')

            #LEFT_ARM
            for num in arm_l:
                if num in fig.data.name:
                    parent("Left Arm", True, '["LArmSmear"]')
                    bpy.data.objects["LarmS"].material_slots[0].material = fig.material_slots[0].material

            #RIGHT_ARM
            for num in arm_r:
                if num in fig.data.name:
                    parent("Right Arm", True, '["RArmSmear"]')
                    bpy.data.objects["RarmS"].material_slots[0].material = fig.material_slots[0].material
            
            #HEAD
            for num in head_epic:
                if num in fig.data.name:
                    parent("Head", False, '["LLegSmear"]')

            #HEAD_ACCESSORY
            for num in head_accessory:
                if num in fig.data.name:
                    parent("Head Accessory", False, '["LLegSmear"]')
                    bpy.context.object.data["Head Bone Scale"] = .85
                    bpy.context.object.data["Head Accessory Bone Scale"] = 1.0
                    break
            
            #HEAD_CLOTHING.ACCESSORIES
            for num in head_clothing_accessories:
                if num in fig.data.name:
                    parent("Head Accessory", False, '["LLegSmear"]')

            #HEAD_CLOTHING.VISORS
            for num in head_clothing_visors:
                if num in fig.data.name:
                    parent("Head Accessory", False, '["LLegSmear"]')
            
            #CAPE
            for num in capes:
                if num in fig.data.name:
                    currentcape = fig.data.name[:5] + ".append"
                    #renamecape = fig.data.name[:7] + ".001"
                    #fig.data.name = renamecape
                    append_cape()
                    rigcape = bpy.data.objects['CapeRig']
                    rigcape.location = fig.location

                    LFarm = rigcape.pose.bones['LL'].constraints['Transformation']

                    LFarm.target = rig
                    LFarm.subtarget = "Left Arm"

                    LFarm2 = rigcape.pose.bones['LL'].constraints['Transformation.001']

                    LFarm2.target = rig
                    LFarm2.subtarget = "Left Arm Socket Control"

                    
                    RFarm = rigcape.pose.bones['RR'].constraints['Transformation']

                    RFarm.target = rig
                    RFarm.subtarget = "Right Arm"

                    RFarm2 = rigcape.pose.bones['RR'].constraints['Transformation.001']

                    RFarm2.target = rig
                    RFarm2.subtarget = "Right Arm Socket Control"

                    bpy.data.objects[currentcape].material_slots[0].material = fig.material_slots[0].material

                    bpy.ops.object.select_all(action='DESELECT')
                    fig.select_set(True)
                    bpy.context.view_layer.objects.active = fig
                    bpy.ops.object.delete() 
                    fig = rigcape
                    parent("Torso Rock", False, '["LLegSmear"]')
                    
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.context.view_layer.objects.active = None

                    #bpy.data.objects[currentcape].name = "FinishedCape"
                    bpy.context.scene.objects[currentcape].select_set(True)
                    for obj in bpy.context.selected_objects:
                        bpy.context.view_layer.objects.active = obj
                    obj = bpy.context.active_object                    
                    bpy.data.collections['CapeRig'].objects.link(obj)
                    bpy.data.collections['Cape Appends'].objects.unlink(obj)
                    bpy.ops.object.select_all(action='DESELECT')
                                
                    collection = bpy.data.collections.get('Cape Appends')
                    for obj in collection.objects:
                        bpy.data.objects.remove(obj, do_unlink=True)
    
                    bpy.data.collections.remove(collection)
                    
                    r = " Rig"
                    c = " Cape"
                    bpy.data.objects[currentcape].name = mname + c
                    bpy.data.objects['CapeRig'].name = mname + c + r
                    bpy.data.collections['CapeRig'].name = mname + c + r
                    bpy.data.collections['ShapesBones'].hide_viewport = True
                    bpy.data.collections['ShapesBones'].hide_render = True
                    #bpy.data.collections['ShapesBones'].name = 'FinishedShapesBones'
                                            
                            
            """#HAND"""
            for num in hand_epic:
                if num in fig.data.name:
                    
                    shortestDist = 100000
                    bpy.context.view_layer.objects.active = rig
                    bpy.ops.object.posemode_toggle()
                    rig.data.bones.active = rig.data.bones['Left Hand']
                    rig.data.bones.active = rig.data.bones['Right Hand']
                    here = bpy.context.selected_pose_bones
                    bpy.ops.object.posemode_toggle()
                
                    for x in here:
                        hand = x.id_data
                        matrix_final = hand.matrix_world @ x.matrix
                        location = matrix_final.translation.xyz
                        
                        handloc = (location - fig.location).length
                        if handloc < shortestDist:
                            shortestDist = handloc
                            handname = x.name

                    if handname == 'Left Hand':
                        fig.select_set(True)
                        bpy.context.view_layer.objects.active = fig
                        bpy.context.active_object.modifiers.new("Boolean", 'BOOLEAN')
                        bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["RLBool"]
                        fig.select_set(False)

                        obj = bpy.data.objects[fig.name]
                        dwive = obj.modifiers["Boolean"].driver_add("show_viewport")
                        driver = dwive.driver
                        
                        var = driver.variables.new()
                        
                        var.type = 'SINGLE_PROP'
                        var.name = "hide"

                        target = var.targets[0]

                        target.id_type = 'ARMATURE'

                        b = bpy.data.armatures[rig.name]

                        target.id = b

                        target.data_path = '["Lepin Hands"]'

                        driver.expression = "hide"

                        #2

                        obj = bpy.data.objects[fig.name]
                        dwive = obj.modifiers["Boolean"].driver_add("show_render")
                        driver = dwive.driver
                        
                        var = driver.variables.new()
                        
                        var.type = 'SINGLE_PROP'
                        var.name = "hide"

                        target = var.targets[0]

                        target.id_type = 'ARMATURE'

                        b = bpy.data.armatures[rig.name]

                        target.id = b

                        target.data_path = '["Lepin Hands"]'

                        driver.expression = "hide"
                    else:
                        fig.select_set(True)
                        bpy.context.view_layer.objects.active = fig
                        bpy.context.active_object.modifiers.new("Boolean", 'BOOLEAN')
                        bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["RHBool"]
                        
                        obj = bpy.data.objects[fig.name]
                        dwive = obj.modifiers["Boolean"].driver_add("show_viewport")
                        driver = dwive.driver
                        
                        var = driver.variables.new()
                        
                        var.type = 'SINGLE_PROP'
                        var.name = "hide"

                        target = var.targets[0]

                        target.id_type = 'ARMATURE'

                        b = bpy.data.armatures[rig.name]

                        target.id = b

                        target.data_path = '["Lepin Hands"]'

                        driver.expression = "hide"

                        #2

                        obj = bpy.data.objects[fig.name]
                        dwive = obj.modifiers["Boolean"].driver_add("show_render")
                        driver = dwive.driver
                        
                        var = driver.variables.new()
                        
                        var.type = 'SINGLE_PROP'
                        var.name = "hide"

                        target = var.targets[0]

                        target.id_type = 'ARMATURE'

                        b = bpy.data.armatures[rig.name]

                        target.id = b

                        target.data_path = '["Lepin Hands"]'

                        driver.expression = "hide"
                        
                        fig.select_set(False)

                    parent(handname, False, '["LLegSmear"]')

        r = " Rig"
        b = " Bone Shapes"
        bpy.data.armatures["Rig"].name = mname + r
        rig.name = mname + r
        collections["BoneShapes"].name = mname + b
        collections["The EpicFigRig"].name = mname + r

        objectsfsmear = bpy.data.objects
        
        #fix Lepin Hands
        bpy.context.view_layer.objects['RHBool'].hide_viewport = True
        bpy.context.view_layer.objects['RLBool'].hide_viewport = True
        
        objectsfsmear["LlegS"].name = "FinishedLlegS"
        objectsfsmear["RlegS"].name = "FinishedRlegS"
        objectsfsmear["LarmS"].name = "FinishedLarmS"
        objectsfsmear["RarmS"].name = "FinishedRarmS"
        objectsfsmear["RHBool"].name = "FinishedRHBool"
        objectsfsmear["RLBool"].name = "FinishedRLBool"
        
        #Turn Rig into Child
        rig.select_set(True)
        if child == True:
            bpy.context.object.data["Leg Height"] = 2.0

        else:

            bpy.context.object.data["Leg Height"] = 0.0
            
        #create global varibles for iksnap
        global mainfkbone
        mainfkbone = "RightLeg"    
        global snapfkbone
        snapfkbone = "RightLegSnap"
        global mainikbone
        mainikbone = "RightFootIK"
        global snapikbone
        snapikbone = "RightFootIKSnap"
        global toggleikslider
        toggleikslider ="RightLegIK"
        global keyframeikslider
        keyframeikslider ='["RightLegIK"]'

        return {'FINISHED'}
    
    """def invoke(self, context, event):
        
        self.actname = bpy.context.active_object.users_collection
        return context.window_manager.invoke_props_dialog(self)"""


#Master Bone   
class ResetMasterBone(bpy.types.Operator):
    """Reverts Masterbone to Default Values"""
    bl_label = "Reset Master Bone"
    bl_idname = 'rig.reset'
    
    def execute(self, context):
        bpy.context.object.data.name = bpy.context.object.name
        if context.mode == 'POSE':
            
        
            if len(context.selected_objects) == 1:
                
                #names selected_armature and selected_object 
                for obj in bpy.context.selected_objects:
                    
                    if obj.type == 'ARMATURE':
                        global selected_armature
                        selected_armature = obj.name
                        

            master_bone_snap = bpy.data.objects[selected_armature].pose.bones["Master Bone Snap"]
            master_bone = bpy.data.objects[selected_armature].data.bones["MasterBone"]
            cur_frame = bpy.context.scene.frame_current
            context = bpy.context
            cur_frame = bpy.context.scene.frame_current
            context = bpy.context
            
        #insert locrot on pivot bone and master bone frame -1
            bpy.context.scene.frame_set(bpy.context.scene.frame_current -1) 
            bpy.ops.pose.select_all(action='SELECT')
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.data.objects[selected_armature].data.bones["Pivot"].select = True
            bpy.data.objects[selected_armature].data.bones["MasterBone"].select = True
            bpy.data.objects[selected_armature].data.bones["BodyControlBoneIK"].select = True
            bpy.data.objects[selected_armature].data.bones["LeftFootIK"].select = True
            bpy.data.objects[selected_armature].data.bones["RightFootIK"].select = True
            bpy.data.objects[selected_armature].data.bones["Center of Mass"].select = True
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
            
        #reset hip loc and height
            bpy.context.scene.frame_set(bpy.context.scene.frame_current +1)
            bpy.ops.pose.select_all(action='SELECT')
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.data.objects[selected_armature].data.bones["MasterBone"].select = True
            hip_height = bpy.data.objects[selected_armature].pose.bones["BodyControlBoneIK"].location[2]
            hip_rot = bpy.data.objects[selected_armature].pose.bones["BodyControlBoneIK"].rotation_quaternion[1] 
            bpy.data.objects[selected_armature].pose.bones["BodyControlBoneIK"].location[2] = 0
            bpy.data.objects[selected_armature].pose.bones["BodyControlBoneIK"].rotation_quaternion[1] = 0
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
            
        #gets world matrix of the snap bone
            obj = master_bone_snap.id_data
            matrix_final = obj.matrix_world @ master_bone_snap.matrix
            obj2 = master_bone.id_data

        #moves snap empty to snap bone
            obj_empty = bpy.data.objects["Master Bone Snap"]
            obj_empty.matrix_world = matrix_final

        #resets pivot bone locrot
            #bpy.context.scene.frame_set(bpy.context.scene.frame_current +1)
            pivot_rotation = bpy.context.object.pose.bones["Pivot"].rotation_euler[0]
            bpy.data.objects[selected_armature].pose.bones["Pivot"].rotation_euler[0] = 0
            bpy.data.objects[selected_armature].pose.bones["Pivot"].location[0] = 0
            bpy.data.objects[selected_armature].pose.bones["Pivot"].location[1] = 0
            bpy.data.objects[selected_armature].pose.bones["Pivot"].location[2] = 0
            bpy.ops.pose.select_all(action='SELECT')
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.data.objects[selected_armature].data.bones["Pivot"].select = True
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
            
        #reset center of mass rotation
            flip_bone_rotation = bpy.context.object.pose.bones["Center of Mass"].rotation_euler[2]
            bpy.ops.pose.select_all(action='SELECT')
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.data.objects[selected_armature].data.bones["Center of Mass"].select = True
            bpy.context.object.pose.bones["Center of Mass"].rotation_euler[2] = 0
            
        #reset IK Hip Bone 
            ik_distance = bpy.context.object.pose.bones["BodyControlBoneIK"].location[1]
            bpy.ops.pose.select_all(action='SELECT')
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.data.objects[selected_armature].data.bones["BodyControlBoneIK"].select = True
            bpy.context.object.pose.bones["BodyControlBoneIK"].location[1] = 0

        #reset IK Legs   
            bpy.ops.pose.select_all(action='SELECT')
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.data.objects[selected_armature].data.bones["LeftFootIK"].select = True
            bpy.data.objects[selected_armature].data.bones["RightFootIK"].select = True
            bpy.ops.transform.translate(value=(0.0, ik_distance, 0.0), orient_type='LOCAL', orient_matrix=((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1.0, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_target='CLOSEST', snap_point=(0.0, 0.0, 0.0), snap_align=False, snap_normal=(0.0, 0.0, 0.0), gpencil_strokes=False, cursor_transform=False, texture_space=False, remove_on_cancel=False, release_confirm=False, use_accurate=False)

        #moves master bone to snap empty
            snap_empty_xloc = bpy.data.objects["Master Bone Snap"].location[0]
            snap_empty_yloc = bpy.data.objects["Master Bone Snap"].location[1]
            snap_empty_zloc = bpy.data.objects["Master Bone Snap"].location[2]
            snap_empty_xrot = bpy.data.objects["Master Bone Snap"].rotation_euler[0]
            snap_empty_yrot = bpy.data.objects["Master Bone Snap"].rotation_euler[1]
            snap_empty_zrot = bpy.data.objects["Master Bone Snap"].rotation_euler[2]

            bpy.data.objects[selected_armature].pose.bones["MasterBone"].location[0] = snap_empty_xloc
            #bpy.context.object.pose.bones["MasterBone"].location[1] = snap_empty_zloc
            bpy.data.objects[selected_armature].pose.bones["MasterBone"].location[2] = snap_empty_yloc
            bpy.data.objects[selected_armature].pose.bones["MasterBone"].rotation_euler[1] = -snap_empty_zrot #+ 3.14159

        #reset hip height and rot
            bpy.data.objects[selected_armature].pose.bones["BodyControlBoneIK"].location[2] = hip_height
            bpy.data.objects[selected_armature].pose.bones["BodyControlBoneIK"].rotation_quaternion[1] = hip_rot

        #insert locrot
            bpy.ops.pose.select_all(action='SELECT')
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.data.objects[selected_armature].data.bones["BodyControlBoneIK"].select = True
            bpy.data.objects[selected_armature].data.bones["LeftFootIK"].select = True
            bpy.data.objects[selected_armature].data.bones["RightFootIK"].select = True
            bpy.data.objects[selected_armature].data.bones["MasterBone"].select = True
            bpy.data.objects[selected_armature].data.bones["Center of Mass"].select = True
            bpy.data.objects[selected_armature].data.bones["Pivot"].select = True
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
            
            #switch custom property
            bpy.context.scene.frame_set(bpy.context.scene.frame_current -1)
            bpy.data.armatures[selected_armature].keyframe_insert(data_path = '["Pivot Slide"]') #, frame = cur_frame -1)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current +1)
            bpy.data.armatures[selected_armature]["Pivot Slide"] = 0
            bpy.data.armatures[selected_armature].keyframe_insert(data_path = '["Pivot Slide"]') #, frame = cur_frame)
            
            #update the scene
            bpy.context.scene.frame_set(bpy.context.scene.frame_current -1)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current +1)
        else:
            self.report({'ERROR'}, "Make sure you are in Pose Mode")
        

              
        return {'FINISHED'}

class SnapMasterBone(bpy.types.Operator):
    bl_label = "Snap Master Bone"
    bl_idname = 'snap.masterbone'
    
    def execute(self, context): 
        bpy.context.object.data.name = bpy.context.object.name 
        if context.mode == 'POSE':

            name_mark = bpy.context.selected_objects[0]

            if len(context.selected_objects) == 1:
                
                #names selected_armature and selected_object 
                for obj in bpy.context.selected_objects:
                    
                    if obj.type == 'ARMATURE':
                        name_mark = obj
                        global selected_armature
                        selected_armature = obj.name
                        print("UNDER THISSSSSS")
                        print(name_mark)
            master_bone_snap = bpy.data.objects[selected_armature].pose .bones["Master Bone Snap"] #context.active_pose_bone
            master_bone = bpy.data.objects[selected_armature].data.bones["MasterBone"]
            cur_frame = bpy.context.scene.frame_current
            context = bpy.context
            cur_frame = bpy.context.scene.frame_current
            context = bpy.context

        #insert locrot on flip bone and master bone frame -1
            bpy.context.scene.frame_set(bpy.context.scene.frame_current -1) 
            bpy.ops.pose.select_all(action='SELECT')
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.data.objects[selected_armature].data.bones["MasterBone"].select = True
            bpy.data.objects[selected_armature].data.bones["Center of Mass"].select = True
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
            
        #reset hip loc and height
            bpy.context.scene.frame_set(bpy.context.scene.frame_current +1)
            bpy.ops.pose.select_all(action='SELECT')
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.data.objects[selected_armature].data.bones["MasterBone"].select = True
            hip_height = bpy.data.objects[selected_armature].pose.bones["BodyControlBoneIK"].location[2]
            hip_rot = bpy.data.objects[selected_armature].pose.bones["BodyControlBoneIK"].rotation_quaternion[1] 
            bpy.data.objects[selected_armature].pose.bones["BodyControlBoneIK"].location[2] = 0
            bpy.data.objects[selected_armature].pose.bones["BodyControlBoneIK"].rotation_quaternion[1] = 0
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')

        #gets world matrix of the snap bone
            obj = master_bone_snap.id_data
            matrix_final = obj.matrix_world @ master_bone_snap.matrix
            obj2 = master_bone.id_data

        #moves snap empty to snap bone
            obj_empty = bpy.data.objects["Master Bone Snap"]
            obj_empty.matrix_world = matrix_final
            
        #reset center of mass rotation
            bpy.context.scene.frame_set(bpy.context.scene.frame_current +1)
            flip_bone_rotation = bpy.context.object.pose.bones["Center of Mass"].rotation_euler[2]
            bpy.ops.pose.select_all(action='SELECT')
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.data.objects[selected_armature].data.bones["Center of Mass"].select = True
            bpy.context.object.pose.bones["Center of Mass"].rotation_euler[2] = 0
            
        #moves master bone to snap empty
            snap_empty_xloc = bpy.data.objects["Master Bone Snap"].location[0]
            snap_empty_yloc = bpy.data.objects["Master Bone Snap"].location[1]
            snap_empty_zloc = bpy.data.objects["Master Bone Snap"].location[2]
            snap_empty_xrot = bpy.data.objects["Master Bone Snap"].rotation_euler[0]
            snap_empty_yrot = bpy.data.objects["Master Bone Snap"].rotation_euler[1]
            snap_empty_zrot = bpy.data.objects["Master Bone Snap"].rotation_euler[2]

            bpy.data.objects[selected_armature].pose.bones["MasterBone"].location[0] = snap_empty_xloc
            #bpy.context.object.pose.bones["MasterBone"].location[1] = snap_empty_zloc
            bpy.data.objects[selected_armature].pose.bones["MasterBone"].location[2] = snap_empty_yloc
            #py.context.object.pose.bones["MasterBone"].rotation_euler[0] = #snap_empty_xrot
            bpy.data.objects[selected_armature].pose.bones["MasterBone"].rotation_euler[1] = -snap_empty_zrot
            #bpy.context.object.pose.bones["MasterBone"].rotation_euler[2] = snap_empty_zrot
            
        #reset hip height and rot
            bpy.data.objects[selected_armature].pose.bones["BodyControlBoneIK"].location[2] = hip_height
            bpy.data.objects[selected_armature].pose.bones["BodyControlBoneIK"].rotation_quaternion[1] = hip_rot
            
        #insert locrot on flip bone and master bone frame current 
            bpy.ops.pose.select_all(action='SELECT')
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.data.objects[selected_armature].data.bones["MasterBone"].select = True
            bpy.data.objects[selected_armature].data.bones["Center of Mass"].select = True
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
            
            #update scene
            bpy.context.scene.frame_set(bpy.context.scene.frame_current -1)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current +1)

        else:
            self.report({'ERROR'}, "Make sure you are in Pose Mode")
        return {'FINISHED'}  

#Pivot
class SwitchPivottoLeft(bpy.types.Operator):
    """Changes the Pivot Bone to the Left Leg"""
    bl_label = "Left"
    bl_idname = 'pivot.left'
    
    def execute(self, context):
        if context.mode == 'POSE':
            if len(context.selected_objects) == 1:
                
                #names selected_armature and selected_object 
                for obj in bpy.context.selected_objects:
                    
                    if obj.type == 'ARMATURE':
                        global selected_armature
                        selected_armature = obj.name
                        bpy.context.object.data.name = bpy.context.object.name
            

            #insert keyframes on frame -1
            bpy.context.scene.frame_set(bpy.context.scene.frame_current -1)
            #bpy.context.scene.frame_current = bpy.context.scene.frame_current -1
            bpy.ops.pose.select_all(action='SELECT')
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.data.objects[selected_armature].data.bones["Pivot"].select = True
            bpy.data.objects[selected_armature].data.bones["LeftFootIK"].select = True
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
            bpy.data.armatures[selected_armature].keyframe_insert(data_path = '["Pivot Slide"]')
            
            #turn on armature layer 18
            bpy.context.scene.frame_set(bpy.context.scene.frame_current +1)
            bpy.context.object.data.layers[18] = True
            
            #reset IK Foot Loc
            bpy.data.objects[selected_armature].pose.bones["LeftFootIK"].location[0] = 0
            bpy.data.objects[selected_armature].pose.bones["LeftFootIK"].location[1] = 0
            bpy.data.objects[selected_armature].pose.bones["LeftFootIK"].location[2] = 0

            #Move Pivot to Left Foot
            bpy.ops.pose.select_all(action='SELECT')
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.data.objects[selected_armature].data.bones["Pivot lock L"].select = True
            #bpy.context.area.ui_type = 'VIEW_3D'
            bpy.ops.view3d.snap_cursor_to_selected()
            bpy.ops.pose.select_all(action='SELECT')
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.data.objects[selected_armature].data.bones["Pivot"].select = True
            bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)
            #bpy.context.area.ui_type = 'TEXT_EDITOR' 
            
            #switch custom property
            bpy.data.armatures[selected_armature]["Pivot Slide"] = 1
            bpy.data.armatures[selected_armature].keyframe_insert(data_path = '["Pivot Slide"]')
    
            #turn off layer 18
            bpy.context.object.data.layers[18] = False
            
            #insert keyframes
            bpy.ops.pose.select_all(action='SELECT')
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.data.objects[selected_armature].data.bones["Pivot"].select = True
            bpy.data.objects[selected_armature].data.bones["LeftFootIK"].select = True
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
            
            #update scene
            bpy.context.scene.frame_set(bpy.context.scene.frame_current -1)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current +1)
        else:
            self.report({'ERROR'}, "Make sure you are in Pose Mode")
        

        return {'FINISHED'}

class SwitchPivottoRight(bpy.types.Operator):
    """Changes the Pivot Bone to the Right Leg""" 
    bl_label = "Right"
    bl_idname = 'pivot.right'
    
    def execute(self, context):
        if context.mode == 'POSE':

            if len(context.selected_objects) == 1:
                
                #names selected_armature and selected_object 
                for obj in bpy.context.selected_objects:
                    
                    if obj.type == 'ARMATURE':
                        global selected_armature
                        selected_armature = obj.name
                        bpy.context.object.data.name = bpy.context.object.name
                        
        #insert keyframes on frame -1
            bpy.context.scene.frame_set(bpy.context.scene.frame_current -1)
            bpy.ops.pose.select_all(action='SELECT')
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.data.objects[selected_armature].data.bones["Pivot"].select = True
            bpy.data.objects[selected_armature].data.bones["RightFootIK"].select = True
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
            bpy.data.armatures[selected_armature].keyframe_insert(data_path = '["Pivot Slide"]')
            
            #turn on layer 18
            bpy.context.scene.frame_set(bpy.context.scene.frame_current +1) 
            bpy.context.object.data.layers[18] = True
            bpy.data.objects[selected_armature].pose.bones["RightFootIK"].location[0] = 0
            bpy.data.objects[selected_armature].pose.bones["RightFootIK"].location[1] = 0
            bpy.data.objects[selected_armature].pose.bones["RightFootIK"].location[2] = 0

            #Move to Left Foot
            bpy.ops.pose.select_all(action='SELECT')
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.data.objects[selected_armature].data.bones["Pivot lock R"].select = True
            #bpy.context.area.ui_type = 'VIEW_3D'
            bpy.ops.view3d.snap_cursor_to_selected()
            bpy.ops.pose.select_all(action='SELECT')
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.data.objects[selected_armature].data.bones["Pivot"].select = True
            bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)
            #bpy.context.area.ui_type = 'TEXT_EDITOR' 
            
            #switch custom property
            bpy.data.armatures[selected_armature]["Pivot Slide"] = 0
            bpy.data.armatures[selected_armature].keyframe_insert(data_path = '["Pivot Slide"]')
    
            #turn off layer 18
            bpy.context.object.data.layers[18] = False
            
            #insert keyframes
            bpy.ops.pose.select_all(action='SELECT')
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.data.objects[selected_armature].data.bones["Pivot"].select = True
            bpy.data.objects[selected_armature].data.bones["RightFootIK"].select = True
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
            
            #update scene
            bpy.context.scene.frame_set(bpy.context.scene.frame_current -1)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current +1)
        else:
            self.report({'ERROR'}, "Make sure you are in Pose Mode")

        return {'FINISHED'}

class ResetPivot(bpy.types.Operator):
    """Reverts Pivot Bone to Default Values""" 
    bl_label = "Reset Pivot"
    bl_idname = 'reset.pivot'
    
    def execute(self, context):
        if context.mode == 'POSE':

            if len(context.selected_objects) == 1:
                
                #names selected_armature and selected_object 
                for obj in bpy.context.selected_objects:
                    
                    if obj.type == 'ARMATURE':
                        global selected_armature
                        selected_armature = obj.name
                        bpy.context.object.data.name = bpy.context.object.name
                        
            #insert keyframes on frame -1
            bpy.context.scene.frame_set(bpy.context.scene.frame_current -1)
            bpy.ops.pose.select_all(action='SELECT')
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.data.objects[selected_armature].data.bones["Pivot"].select = True
            #bpy.data.objects[selected_armature].data.bones["RightFootIK"].select = True
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
            bpy.data.armatures[selected_armature].keyframe_insert(data_path = '["Pivot Slide"]')
            
            bpy.context.scene.frame_set(bpy.context.scene.frame_current +1)            
            bpy.data.objects[selected_armature].pose.bones["Pivot"].location[0] = 0
            bpy.data.objects[selected_armature].pose.bones["Pivot"].location[1] = 0
            bpy.data.objects[selected_armature].pose.bones["Pivot"].location[2] = 0
            bpy.data.objects[selected_armature].pose.bones["Pivot"].rotation_euler[0] = 0
            bpy.data.objects[selected_armature].pose.bones["RightFootIK"].location[0] = 0
            bpy.data.objects[selected_armature].pose.bones["RightFootIK"].location[1] = 0
            bpy.data.objects[selected_armature].pose.bones["RightFootIK"].location[2] = 0
            bpy.data.objects[selected_armature].data.bones["RightFootIK"].select = True
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
            
            #switch custom property
            bpy.data.armatures[selected_armature]["Pivot Slide"] = 0
            bpy.data.armatures[selected_armature].keyframe_insert(data_path = '["Pivot Slide"]')
            bpy.context.scene.frame_set(bpy.context.scene.frame_current -1)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current +1)
        else:
            self.report({'ERROR'}, "Make sure you are in Pose Mode")
        return {'FINISHED'}

#Snap Bones  
class SnapRight(bpy.types.Operator):
    """Snap Selected Accessory to the Right Hand""" 
    bl_label = "Right Hand"
    bl_idname = 'snap_right.add'
    
    def execute(self, context):
        
        cur_frame = bpy.context.scene.frame_current
        context = bpy.context
        
        
        
        if len(context.selected_objects) == 2:
            
            #names selected_armature and selected_object 
            for obj in bpy.context.selected_objects:
                
                if obj.type == 'ARMATURE':
                    global selected_armature
                    selected_armature = obj.name
                    
                    
                if obj.type == 'MESH':
                    global selected_object
                    selected_object = obj.name
                    
                
            #deselects everything
            bpy.data.objects[selected_armature].data.bones["Right Hand Snap Bone"].select = False
            for obj in bpy.context.selected_objects:
                obj.select_set(False)
            
            #selects adds keyframes to the selected object
            selected_object_keyframe = bpy.data.objects[selected_object].keyframe_insert
            bpy.data.objects[selected_object].select_set(True)
            obj = bpy.context.window.scene.objects[0]       # sets selected object
            bpy.context.view_layer.objects.active = obj     # to active object!!
            selected_object_keyframe(data_path='location', frame = (cur_frame - 1))
            selected_object_keyframe(data_path='rotation_euler', frame = (cur_frame - 1))
            selected_object_keyframe(data_path='scale', frame = (cur_frame - 1))
            
            #adds and sets up Copy Transforms Constraint
            o = bpy.context.selected_objects[0]
            o.constraints.new('COPY_TRANSFORMS')
            
            copy_transform = bpy.data.objects[selected_object].constraints['Copy Transforms']
            target_constraint = bpy.data.objects[selected_armature]
            subtarget_constraint = bpy.data.objects[selected_armature].data.bones['Right Hand Snap Bone']
            
            copy_transform.target = target_constraint
            copy_transform.subtarget = "Right Hand Snap Bone"
            
            #sets up keyframes for influence
            copy_transform.influence = 0
            copy_transform.keyframe_insert(data_path = "influence", frame = cur_frame - 1)
            copy_transform.influence = 1
            copy_transform.keyframe_insert(data_path = "influence", frame = cur_frame)
            
            #sets up keyframes for Loc Rot
            selected_object_keyframe(data_path='location', frame = (cur_frame - 1))
            selected_object_keyframe(data_path='rotation_euler', frame = (cur_frame - 1))
            selected_object_keyframe(data_path='scale', frame = (cur_frame - 1))
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_VisualLocRot')
            copy_transform.influence = 0
            copy_transform.keyframe_insert(data_path = "influence", frame = cur_frame)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current -1)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current +1) 



        else:
            self.report({'ERROR'}, "Select both Armature and Obejct")
            
            
        return {'FINISHED'}
    
class SnapLeft(bpy.types.Operator):
    """Snap Selected Accessory to the Left Hand"""
    bl_label = "Left Hand"
    bl_idname = 'snap_left.add'
    
    def execute(self, context):
        
        cur_frame = bpy.context.scene.frame_current
        context = bpy.context
        
        
        
        if len(context.selected_objects) == 2:
            
            #names selected_armature and selected_object 
            for obj in bpy.context.selected_objects:
                
                if obj.type == 'ARMATURE':
                    global selected_armature
                    selected_armature = obj.name
                    
                    
                if obj.type == 'MESH':
                    global selected_object
                    selected_object = obj.name
                    
                
            #deselects everything
            bpy.data.objects[selected_armature].data.bones["Left Hand Snap Bone"].select = False
            for obj in bpy.context.selected_objects:
                obj.select_set(False)
            
            #selects adds keyframes to the selected object
            selected_object_keyframe = bpy.data.objects[selected_object].keyframe_insert
            bpy.data.objects[selected_object].select_set(True)
            obj = bpy.context.window.scene.objects[0]       # sets selected object
            bpy.context.view_layer.objects.active = obj     # to active object!!
            selected_object_keyframe(data_path='location', frame = (cur_frame - 1))
            selected_object_keyframe(data_path='rotation_euler', frame = (cur_frame - 1))
            selected_object_keyframe(data_path='scale', frame = (cur_frame - 1))
            
            #adds and sets up Copy Transforms Constraint
            o = bpy.context.selected_objects[0]
            o.constraints.new('COPY_TRANSFORMS')
            
            copy_transform = bpy.data.objects[selected_object].constraints['Copy Transforms']
            target_constraint = bpy.data.objects[selected_armature]
            subtarget_constraint = bpy.data.objects[selected_armature].data.bones['Left Hand Snap Bone']
            
            copy_transform.target = target_constraint
            copy_transform.subtarget = "Left Hand Snap Bone"
            
            #sets up keyframes for influence
            copy_transform.influence = 0
            copy_transform.keyframe_insert(data_path = "influence", frame = cur_frame - 1)
            copy_transform.influence = 1
            copy_transform.keyframe_insert(data_path = "influence", frame = cur_frame)
            
            #sets up keyframes for Loc Rot
            selected_object_keyframe(data_path='location', frame = (cur_frame - 1))
            selected_object_keyframe(data_path='rotation_euler', frame = (cur_frame - 1))
            selected_object_keyframe(data_path='scale', frame = (cur_frame - 1))
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_VisualLocRot')
            copy_transform.influence = 0
            copy_transform.keyframe_insert(data_path = "influence", frame = cur_frame)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current -1)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current +1)

        else:
            self.report({'ERROR'}, "Select both Armature and Obejct")
            
            
        return {'FINISHED'}
    
class SnapHead(bpy.types.Operator):
    """Snap Selected Accessory to the Head"""
    bl_label = "Head"
    bl_idname = 'snap_head.add'
    
    def execute(self, context):
        
        cur_frame = bpy.context.scene.frame_current
        context = bpy.context
        
        
        
        if len(context.selected_objects) == 2:
            
            #names selected_armature and selected_object 
            for obj in bpy.context.selected_objects:
                
                if obj.type == 'ARMATURE':
                    global selected_armature
                    selected_armature = obj.name
                    
                    
                if obj.type == 'MESH':
                    global selected_object
                    selected_object = obj.name
                    
                
            #deselects everything
            bpy.data.objects[selected_armature].data.bones["Head Accessory"].select = False
            for obj in bpy.context.selected_objects:
                obj.select_set(False)

            
            #selects adds keyframes to the selected object
            selected_object_keyframe = bpy.data.objects[selected_object].keyframe_insert
            bpy.data.objects[selected_object].select_set(True)
            obj = bpy.context.window.scene.objects[0]       # sets selected object
            bpy.context.view_layer.objects.active = obj     # to active object!!
            selected_object_keyframe(data_path='location', frame = (cur_frame - 1))
            selected_object_keyframe(data_path='rotation_euler', frame = (cur_frame - 1))
            selected_object_keyframe(data_path='scale', frame = (cur_frame - 1))
            
            #adds and sets up Copy Transforms Constraint
            o = bpy.context.selected_objects[0]
            o.constraints.new('COPY_TRANSFORMS')
            
            copy_transform = bpy.data.objects[selected_object].constraints['Copy Transforms']
            target_constraint = bpy.data.objects[selected_armature]
            subtarget_constraint = bpy.data.objects[selected_armature].data.bones['Head Accessory']
            
            copy_transform.target = target_constraint
            copy_transform.subtarget = "Head Accessory"
            
            #sets up keyframes for influence
            copy_transform.influence = 0
            copy_transform.keyframe_insert(data_path = "influence", frame = cur_frame - 1)
            copy_transform.influence = 1
            copy_transform.keyframe_insert(data_path = "influence", frame = cur_frame)
            
            #sets up keyframes for Loc Rot
            selected_object_keyframe(data_path='location', frame = (cur_frame - 1))
            selected_object_keyframe(data_path='rotation_euler', frame = (cur_frame - 1))
            selected_object_keyframe(data_path='scale', frame = (cur_frame - 1))
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_VisualLocRot')
            copy_transform.influence = 0
            copy_transform.keyframe_insert(data_path = "influence", frame = cur_frame)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current -1)
            bpy.context.scene.frame_set(bpy.context.scene.frame_current +1)



        else:
            self.report({'ERROR'}, "Select both Armature and Obejct")
            
            
        return {'FINISHED'}

def iktofk():

    if addon_utils.check("space_view3d_copy_attributes") == (False, False):
        addon_utils.enable("space_view3d_copy_attributes")
        addon_utils.check("space_view3d_copy_attributes")
        
    #sets keyframe on every bone
    bpy.context.object.data["SnapVis"] = 1
    bpy.context.view_layer.objects.active.data.bones[mainfkbone].select = True
    bpy.context.view_layer.objects.active.data.bones[snapfkbone].select = True
    bpy.context.view_layer.objects.active.data.bones[mainikbone].select = True
    bpy.context.view_layer.objects.active.data.bones[snapikbone].select = True
            
    bpy.ops.anim.keyframe_insert_by_name(type="BUILTIN_KSI_LocRot")
    keyframeikslider
           
    bpy.ops.pose.select_all(action='DESELECT')
    
    #Copies rotation data to hidden snap bone from main bone

    bpy.context.view_layer.objects.active.data.bones[snapfkbone].select = True
    bpy.context.object.data.bones.active = bpy.data.objects[selected_armature].pose.bones[mainfkbone].bone
    bpy.context.object.data.bones.active
    bpy.ops.pose.copy_pose_vis_rot()
    bpy.ops.pose.copy_pose_vis_loc()

    bpy.ops.anim.keyframe_insert_by_name(type="BUILTIN_KSI_LocRot")

    #turns on IK contstaint
    bpy.context.object.data[toggleikslider] = 0
    bpy.context.object.data.keyframe_insert(data_path=keyframeikslider)
    bpy.ops.pose.select_all(action='DESELECT')

    #Copies rotation data to main bone from hidden snap bone

    bpy.context.view_layer.objects.active.data.bones[mainfkbone].select = True
    bpy.context.object.data.bones.active = bpy.data.objects[selected_armature].pose.bones[snapfkbone].bone
    bpy.context.object.data.bones.active
    bpy.ops.pose.copy_pose_vis_loc()
    bpy.ops.pose.copy_pose_vis_rot()

    bpy.ops.anim.keyframe_insert_by_name(type="BUILTIN_KSI_LocRot")
    bpy.ops.pose.select_all(action='DESELECT')

    #turns off copy menu if you didn't have it on
    if addon_utils.check("space_view3d_copy_attributes") == (False, True):
        addon_utils.disable("space_view3d_copy_attributes")
        addon_utils.check("space_view3d_copy_attributes")

    bpy.context.object.data["SnapVis"] = 0
    bpy.ops.pose.select_all(action='DESELECT')         

def fktoik():

    if addon_utils.check("space_view3d_copy_attributes") == (False, False):
        addon_utils.enable("space_view3d_copy_attributes")
        addon_utils.check("space_view3d_copy_attributes")
        
    #sets keyframe on every bone
    bpy.context.object.data["SnapVis"] = 1
    bpy.context.view_layer.objects.active.data.bones[mainfkbone].select = True
    bpy.context.view_layer.objects.active.data.bones[snapfkbone].select = True
    bpy.context.view_layer.objects.active.data.bones[mainikbone].select = True
    bpy.context.view_layer.objects.active.data.bones[snapikbone].select = True
            
    bpy.ops.anim.keyframe_insert_by_name(type="BUILTIN_KSI_LocRot")
    keyframeikslider
           
    bpy.ops.pose.select_all(action='DESELECT')
    
    #Copies rotation data to hidden snap bone from main bone

    bpy.context.view_layer.objects.active.data.bones[snapfkbone].select = True
    bpy.context.object.data.bones.active = bpy.data.objects[selected_armature].pose.bones[mainfkbone].bone
    bpy.context.object.data.bones.active
    bpy.ops.pose.copy_pose_vis_rot()
    bpy.ops.pose.copy_pose_vis_loc()

    bpy.ops.anim.keyframe_insert_by_name(type="BUILTIN_KSI_LocRot")

    #turns on IK contstaint
    bpy.context.object.data[toggleikslider] = 1
    bpy.context.object.data.keyframe_insert(data_path=keyframeikslider)
    bpy.ops.pose.select_all(action='DESELECT')

    #Copies rotation data to main bone from hidden snap bone

    bpy.context.view_layer.objects.active.data.bones[mainikbone].select = True
    bpy.context.object.data.bones.active = bpy.data.objects[selected_armature].pose.bones[snapikbone].bone
    bpy.context.object.data.bones.active
    bpy.ops.pose.copy_pose_vis_loc()

    bpy.ops.anim.keyframe_insert_by_name(type="BUILTIN_KSI_LocRot")
    bpy.ops.pose.select_all(action='DESELECT')

    #turns off copy menu if you didn't have it on
    if addon_utils.check("space_view3d_copy_attributes") == (False, True):
        addon_utils.disable("space_view3d_copy_attributes")
        addon_utils.check("space_view3d_copy_attributes")

    bpy.context.object.data["SnapVis"] = 0
    bpy.ops.pose.select_all(action='DESELECT')

class iktofkRleg(bpy.types.Operator):
    """Keyframes the Current Values and changes the Right Leg to FK"""
    bl_label = "Snap IK to FK"
    bl_idname = 'ik_to.fk_rleg'

    import bpy
    import addon_utils

    def execute(self, context):
        if (bpy.context.mode == "POSE"):

            for obj in bpy.context.selected_objects:
                    
                if obj.type == 'ARMATURE':
                    global selected_armature
                    selected_armature = obj.name
    
    
            global mainfkbone
            mainfkbone = "RightLeg"    
            global snapfkbone
            snapfkbone = "RightLegSnap"
            global mainikbone
            mainikbone = "RightFootIK"
            global snapikbone
            snapikbone = "RightFootIKSnap"
            global toggleikslider
            toggleikslider ="RightLegIK"
            global keyframeikslider
            keyframeikslider ='["RightLegIK"]'
    
            iktofk()
            
        else:
            self.report({'ERROR'}, "Must be in Pose Mode")
        
        return {'FINISHED'}
    

class iktofkLleg(bpy.types.Operator):
    """Keyframes the Current Values and changes the Left Leg to FK"""
    bl_label = "Snap IK to FK"
    bl_idname = 'ik_to.fk_lleg'
    
    import bpy
    import addon_utils

    def execute(self, context):
        if (bpy.context.mode == "POSE"):

            for obj in bpy.context.selected_objects:
                    
                if obj.type == 'ARMATURE':
                    global selected_armature
                    selected_armature = obj.name
    
    
            global mainfkbone
            mainfkbone = "LeftLeg"    
            global snapfkbone
            snapfkbone = "LeftLegSnap"
            global mainikbone
            mainikbone = "LeftFootIK"
            global snapikbone
            snapikbone = "LeftFootIKSnap"
            global toggleikslider
            toggleikslider ="LeftLegIK"
            global keyframeikslider
            keyframeikslider ='["LeftLegIK"]'
    
            iktofk()
            
        else:
            self.report({'ERROR'}, "Must be in Pose Mode")
        
        return {'FINISHED'}

class iktofkLarm(bpy.types.Operator):
    """Keyframes the Current Values and changes the Left Arm to FK"""
    bl_label = "Snap IK to FK"
    bl_idname = 'ik_to.fk_larm'
    
    import bpy
    import addon_utils

    def execute(self, context):
        if (bpy.context.mode == "POSE"):

            for obj in bpy.context.selected_objects:
                    
                if obj.type == 'ARMATURE':
                    global selected_armature
                    selected_armature = obj.name
    
    
            global mainfkbone
            mainfkbone = "Left Arm Socket Control"    
            global snapfkbone
            snapfkbone = "Left Arm Snap"
            global mainikbone
            mainikbone = "Left Arm IK"
            global snapikbone
            snapikbone = "Left Arm IK Snap"
            global toggleikslider
            toggleikslider ="LeftArmIK"
            global keyframeikslider
            keyframeikslider ='["LeftArmIK"]'
    
            iktofk()
            
        else:
            self.report({'ERROR'}, "Must be in Pose Mode")
        
        return {'FINISHED'}

class iktofkRarm(bpy.types.Operator):
    """Keyframes the Current Values and changes the Right Arm to FK"""
    bl_label = "Snap IK to FK"
    bl_idname = 'ik_to.fk_rarm'
    
    import bpy
    import addon_utils

    def execute(self, context):
        if (bpy.context.mode == "POSE"):

            for obj in bpy.context.selected_objects:
                    
                if obj.type == 'ARMATURE':
                    global selected_armature
                    selected_armature = obj.name
    
    
            global mainfkbone
            mainfkbone = "Right Arm Socket Control"    
            global snapfkbone
            snapfkbone = "Right Arm Snap"
            global mainikbone
            mainikbone = "Right Arm IK"
            global snapikbone
            snapikbone = "Right Arm IK Snap"
            global toggleikslider
            toggleikslider ="RightArmIK"
            global keyframeikslider
            keyframeikslider ='["RightArmIK"]'
    
            iktofk()
            
        else:
            self.report({'ERROR'}, "Must be in Pose Mode")
        
        return {'FINISHED'}     

class fktoikRleg(bpy.types.Operator):
    """Keyframes the Current Values and changes the Right Leg to IK"""
    bl_label = "Snap FK to IK"
    bl_idname = 'fk_to.ik_rleg'

    import bpy
    import addon_utils

    def execute(self, context):
        if (bpy.context.mode == "POSE"):

            for obj in bpy.context.selected_objects:
                    
                if obj.type == 'ARMATURE':
                    global selected_armature
                    selected_armature = obj.name
    
    
            global mainfkbone
            mainfkbone = "RightLeg"    
            global snapfkbone
            snapfkbone = "RightLegSnap"
            global mainikbone
            mainikbone = "RightFootIK"
            global snapikbone
            snapikbone = "RightFootIKSnap"
            global toggleikslider
            toggleikslider ="RightLegIK"
            global keyframeikslider
            keyframeikslider ='["RightLegIK"]'
    
            fktoik()
            
        else:
            self.report({'ERROR'}, "Must be in Pose Mode")
        
        return {'FINISHED'}
    

class fktoikLleg(bpy.types.Operator):
    """Keyframes the Current Values and changes the Left Leg to IK"""
    bl_label = "Snap FK to IK"
    bl_idname = 'fk_to.ik_lleg'
    
    import bpy
    import addon_utils

    def execute(self, context):
        if (bpy.context.mode == "POSE"):

            for obj in bpy.context.selected_objects:
                    
                if obj.type == 'ARMATURE':
                    global selected_armature
                    selected_armature = obj.name
    
    
            global mainfkbone
            mainfkbone = "LeftLeg"    
            global snapfkbone
            snapfkbone = "LeftLegSnap"
            global mainikbone
            mainikbone = "LeftFootIK"
            global snapikbone
            snapikbone = "LeftFootIKSnap"
            global toggleikslider
            toggleikslider ="LeftLegIK"
            global keyframeikslider
            keyframeikslider ='["LeftLegIK"]'
    
            fktoik()
            
        else:
            self.report({'ERROR'}, "Must be in Pose Mode")
        
        return {'FINISHED'}

class fktoikLarm(bpy.types.Operator):
    """Keyframes the Current Values and changes the Left Arm to IK"""
    bl_label = "Snap FK to IK"
    bl_idname = 'fk_to.ik_larm'
    
    import bpy
    import addon_utils

    def execute(self, context):
        if (bpy.context.mode == "POSE"):

            for obj in bpy.context.selected_objects:
                    
                if obj.type == 'ARMATURE':
                    global selected_armature
                    selected_armature = obj.name
    
    
            global mainfkbone
            mainfkbone = "Left Arm Socket Control"    
            global snapfkbone
            snapfkbone = "Left Arm Snap"
            global mainikbone
            mainikbone = "Left Arm IK"
            global snapikbone
            snapikbone = "Left Arm IK Snap"
            global toggleikslider
            toggleikslider ="LeftArmIK"
            global keyframeikslider
            keyframeikslider ='["LeftArmIK"]'
    
            fktoik()
            
        else:
            self.report({'ERROR'}, "Must be in Pose Mode")
        
        return {'FINISHED'}

class fktoikRarm(bpy.types.Operator):
    """Keyframes the Current Values and changes the Right Arm to IK"""
    bl_label = "Snap FK to IK"
    bl_idname = 'fk_to.ik_rarm'
    
    import bpy
    import addon_utils

    def execute(self, context):
        if (bpy.context.mode == "POSE"):

            for obj in bpy.context.selected_objects:
                    
                if obj.type == 'ARMATURE':
                    global selected_armature
                    selected_armature = obj.name
    
    
            global mainfkbone
            mainfkbone = "Right Arm Socket Control"    
            global snapfkbone
            snapfkbone = "Right Arm Snap"
            global mainikbone
            mainikbone = "Right Arm IK"
            global snapikbone
            snapikbone = "Right Arm IK Snap"
            global toggleikslider
            toggleikslider ="RightArmIK"
            global keyframeikslider
            keyframeikslider ='["RightArmIK"]'
    
            fktoik()
            
        else:
            self.report({'ERROR'}, "Must be in Pose Mode")
        
        return {'FINISHED'}

class MainTab(bpy.types.Operator):
    """Main Rig Settings"""
    bl_label = "Main"
    bl_idname = 'main.tab'
    
    import bpy
    import addon_utils

    def execute(self, context):
        #bpy.context.object.data["RigTabs"] = 0
        bpy.types.Scene.EpicRigTabs = IntProperty(name = "Epic Rig Tabs", default=0)
        
        return {'FINISHED'}

class AdvancedTab(bpy.types.Operator):
    """Advanced Rig Settings - More to Come!"""
    bl_label = "Advanced"
    bl_idname = 'advanced.tab'
    
    import bpy
    import addon_utils

    def execute(self, context):
        #bpy.context.object.data["RigTabs"] = 1
        bpy.types.Scene.EpicRigTabs = IntProperty(name = "Epic Rig Tabs", default=1)
        
        return {'FINISHED'}
    
"""class resetsnapping(bpy.types.Operator):
    
    bl_label = "Reset Snapping"
    bl_idname = 'reset_the.snapping'

    def execute(self, context):
        if (bpy.context.mode == "POSE"):

            for obj in bpy.context.selected_objects:
                    
                if obj.type == 'ARMATURE':
                    global selected_armature
                    selected_armature = obj.name

            bpy.context.object.data["SnapVis"] = 1
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active.data.bones["LeftLegSnap"].select = True
            bpy.context.view_layer.objects.active.data.bones["LeftFootIKSnap"].select = True
            bpy.context.view_layer.objects.active.data.bones["RightLegSnap"].select = True
            bpy.context.view_layer.objects.active.data.bones["RightFootIKSnap"].select = True
            bpy.ops.anim.keyframe_clear_v3d()
            bpy.context.object.data["SnapVis"] = 0
            bpy.ops.pose.select_all(action='DESELECT')

        else:
            self.report({'ERROR'}, "Must be in Pose Mode")
           
        return {'FINISHED'}
"""

#REGISTRATION

def register():

    bpy.utils.register_class(EpicFigRigPanel)

    bpy.utils.register_class(EpicButtons)

    bpy.utils.register_class(RigSettings)

    bpy.utils.register_class(SmearSlider)
    
    bpy.utils.register_class(BoneAdjust)
    
    bpy.utils.register_class(BoneVis)

    bpy.utils.register_class(ResetMasterBone)

    bpy.utils.register_class(SwitchPivottoLeft)

    bpy.utils.register_class(SwitchPivottoRight)

    bpy.utils.register_class(SnapMasterBone)

    bpy.utils.register_class(SnapRight)

    bpy.utils.register_class(SnapLeft)

    bpy.utils.register_class(SnapHead)

    bpy.utils.register_class(ResetPivot)

    bpy.utils.register_class(AutoRig)

    bpy.utils.register_class(iktofkRleg)

    bpy.utils.register_class(iktofkLleg)

    bpy.utils.register_class(iktofkRarm)

    bpy.utils.register_class(iktofkLarm)

    bpy.utils.register_class(fktoikRarm)

    bpy.utils.register_class(fktoikLarm)

    bpy.utils.register_class(fktoikRleg)

    bpy.utils.register_class(fktoikLleg)
    
    bpy.utils.register_class(ArmMenu)
    
    bpy.utils.register_class(LegMenu)
    
    bpy.utils.register_class(MainTab)
    
    bpy.utils.register_class(AdvancedTab)
    
    #bpy.utils.register_class(Naming)
    
    #bpy.utils.register_class(EpicProperties)
    
    #bpy.types.Scene.EpicRigTabs = IntProperty(name = "EpicRigTabs", default=0, min=0, max=3)

    bpy.types.Scene.EpicRigTabs = IntProperty(name = "Epic Rig Tabs", default=0, min=0, max=3)

#    bpy.utils.register_class(resetsnapping)

def unregister():

    bpy.utils.unregister_class(EpicFigRigPanel)

    bpy.utils.unregister_class(EpicButtons)
    
    bpy.utils.unregister_class(RigSettings)

    bpy.utils.unregister_class(SmearSlider)
    
    bpy.utils.unregister_class(BoneAdjust)
    
    bpy.utils.unregister_class(BoneVis)

    bpy.utils.unregister_class(ResetMasterBone)

    bpy.utils.unregister_class(SwitchPivottoLeft)

    bpy.utils.unregister_class(SwitchPivottoRight)

    bpy.utils.unregister_class(SnapMasterBone)

    bpy.utils.unregister_class(SnapRight)

    bpy.utils.unregister_class(SnapLeft)

    bpy.utils.unregister_class(SnapHead)

    bpy.utils.unregister_class(ResetPivot)

    bpy.utils.unregister_class(AutoRig)

    bpy.utils.unregister_class(iktofkRleg)

    bpy.utils.unregister_class(iktofkLleg)

    bpy.utils.unregister_class(iktofkRarm)

    bpy.utils.unregister_class(iktofkLarm)

    bpy.utils.unregister_class(fktoikRarm)

    bpy.utils.unregister_class(fktoikLarm)

    bpy.utils.unregister_class(fktoikRleg)

    bpy.utils.unregister_class(fktoikLleg)
    
    bpy.utils.unregister_class(ArmMenu)
    
    bpy.utils.unregister_class(LegMenu)
    
    bpy.utils.unregister_class(MainTab)
    
    bpy.utils.unregister_class(AdvancedTab)
    
    #bpy.utils.unregister_class(Naming)
    
    #bpy.utils.unregister_class(EpicProperties)
    
    del bpy.types.Scene.EpicRigTabs 
    
#    bpy.utils.unregister_class(resetsnapping)
    
if __name__ == "__main__":
    register()
