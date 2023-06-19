bl_info = {
    "name": "ControlNet Render",
    "description": "",
    "author": "x6ud",
    "version": (1, 0),
    "blender": (3, 5, 0),
    "category": "Render"
}

import bpy
from .properties import ControlNetRenderProperties, ControlNetRenderStateProperties
from .ui import ControlNetRenderPanelImageEditor
from .operators import ControlNetRenderOperator, ControlNetGenerateOperator

classes = [
    ControlNetRenderProperties,
    ControlNetRenderStateProperties,

    ControlNetRenderPanelImageEditor,

    ControlNetRenderOperator,
    ControlNetGenerateOperator,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.controlnet_render_properties = bpy.props.PointerProperty(type=ControlNetRenderProperties)
    bpy.types.WindowManager.controlnet_render_state = bpy.props.PointerProperty(type=ControlNetRenderStateProperties)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
