import bpy
from .constants import IMG_2_IMG_NAME


class ControlNetRenderPanelImageEditor(bpy.types.Panel):
    bl_label = "ControlNet"
    bl_idname = "CONTROL_NET_RENDER_PT_IMAGE_EDITOR"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"
    bl_category = "ControlNet"

    @classmethod
    def poll(cls, context):
        return bpy.context.scene is not None

    def draw(self, context):
        options = context.scene.controlnet_render_properties
        layout = self.layout
        layout.prop(options, "webui_url")
        layout.prop(options, "width")
        layout.prop(options, "height")
        layout.prop(options, "sampling_method")
        layout.prop(options, "sampling_steps")
        layout.prop(options, "restore_faces")
        layout.prop(options, "tiling")
        layout.prop(options, "cfg_scale")
        layout.prop(options, "seed")
        layout.prop(options, "img2img")
        if options.img2img:
            layout.prop(options, "denoising_strength")
        layout.prop(options, "depth")
        if options.depth:
            layout.prop(options, "depth_weight")
            layout.prop(options, "depth_starting")
            layout.prop(options, "depth_ending")
            layout.prop(options, "depth_mode")
        layout.prop(options, "normal")
        if options.normal:
            layout.prop(options, "normal_weight")
            layout.prop(options, "normal_starting")
            layout.prop(options, "normal_ending")
            layout.prop(options, "normal_mode")
        layout.prop(options, "edge")
        if options.edge:
            layout.prop(options, "edge_model")
            layout.prop(options, "edge_weight")
            layout.prop(options, "edge_starting")
            layout.prop(options, "edge_ending")
            layout.prop(options, "edge_mode")
        layout.separator()
        layout.operator("controlnet_render.render", text="Render Input Images", icon="RENDERLAYERS")
        layout.separator()
        layout.prop(options, "prompt")
        layout.prop(options, "negative_prompt")
        if context.window_manager.controlnet_render_state.generating:
            row = layout.row()
            row.alignment = "CENTER"
            row.label(text="Generating...")
        else:
            layout.operator("controlnet_render.generate", text="Generate", icon="LIGHT")
