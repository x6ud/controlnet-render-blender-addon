import bpy


class ControlNetRenderProperties(bpy.types.PropertyGroup):
    webui_url: bpy.props.StringProperty(name="URL", default="http://127.0.0.1:7860")
    prompt: bpy.props.StringProperty(name="Prompt")
    negative_prompt: bpy.props.StringProperty(name="Negative Prompt")
    width: bpy.props.IntProperty(name="Width", step=8, min=64, max=2048, default=512)
    height: bpy.props.IntProperty(name="Height", step=8, min=64, max=2048, default=512)
    restore_faces: bpy.props.BoolProperty(name="Restore Faces", default=False)
    tiling: bpy.props.BoolProperty(name="Tiling", default=False)
    sampling_method: bpy.props.EnumProperty(
        name="Method",
        items=[("Euler a", "Euler a", "Euler a"), ("Euler", "Euler", "Euler"), ("LMS", "LMS", "LMS"),
               ("Heun", "Heun", "Heun"), ("DPM2", "DPM2", "DPM2"), ("DPM2 a", "DPM2 a", "DPM2 a"),
               ("DPM++ 2S a", "DPM++ 2S a", "DPM++ 2S a"), ("DPM++ 2M", "DPM++ 2M", "DPM++ 2M"),
               ("DPM++ SDE", "DPM++ SDE", "DPM++ SDE"), ("DPM++ 2M SDE", "DPM++ 2M SDE", "DPM++ 2M SDE"),
               ("DPM fast", "DPM fast", "DPM fast"), ("DPM adaptive", "DPM adaptive", "DPM adaptive"),
               ("LMS Karras", "LMS Karras", "LMS Karras"), ("DPM2 Karras", "DPM2 Karras", "DPM2 Karras"),
               ("DPM2 a Karras", "DPM2 a Karras", "DPM2 a Karras"),
               ("DPM++ 2S a Karras", "DPM++ 2S a Karras", "DPM++ 2S a Karras"),
               ("DPM++ 2M Karras", "DPM++ 2M Karras", "DPM++ 2M Karras"),
               ("DPM++ SDE Karras", "DPM++ SDE Karras", "DPM++ SDE Karras"),
               ("DPM++ 2M SDE Karras", "DPM++ 2M SDE Karras", "DPM++ 2M SDE Karras"), ("DDIM", "DDIM", "DDIM"),
               ("PLMS", "PLMS", "PLMS"), ("UniPC", "UniPC", "UniPC")],
        default="Euler a"
    )
    sampling_steps: bpy.props.IntProperty(name="Sampling Steps", min=1, max=150, default=20)
    cfg_scale: bpy.props.FloatProperty(name="CFG Scale", min=1, max=30, default=7)
    seed: bpy.props.IntProperty(name="Seed", default=-1)
    img2img: bpy.props.BoolProperty(name="img2img", default=False)
    denoising_strength: bpy.props.FloatProperty(name="Denoising Strength", min=0, max=1, default=0.75)
    depth: bpy.props.BoolProperty(name="ControlNet Depth", default=False)
    depth_weight: bpy.props.FloatProperty(name="Weight", min=0, max=2, default=1)
    depth_starting: bpy.props.FloatProperty(name="Starting Step", min=0, max=1, default=0)
    depth_ending: bpy.props.FloatProperty(name="Ending Step", min=0, max=1, default=1)
    depth_mode: bpy.props.EnumProperty(
        name="Mode",
        items=[("0", "Balanced", "Balanced"),
               ("1", "My prompt is more important", "My prompt is is more important"),
               ("2", "ControlNet is more important", "ControlNet is more important")
               ],
        default="0"
    )
    normal: bpy.props.BoolProperty(name="ControlNet Normal", default=False)
    normal_weight: bpy.props.FloatProperty(name="Weight", min=0, max=2, default=1)
    normal_starting: bpy.props.FloatProperty(name="Starting Step", min=0, max=1, default=0)
    normal_ending: bpy.props.FloatProperty(name="Ending Step", min=0, max=1, default=1)
    normal_mode: bpy.props.EnumProperty(
        name="Mode",
        items=[("0", "Balanced", "Balanced"),
               ("1", "My prompt is more important", "My prompt is is more important"),
               ("2", "ControlNet is more important", "ControlNet is more important")
               ],
        default="0"
    )
    edge: bpy.props.BoolProperty(name="ControlNet Line", default=False)
    edge_weight: bpy.props.FloatProperty(name="Weight", min=0, max=2, default=1)
    edge_starting: bpy.props.FloatProperty(name="Starting Step", min=0, max=1, default=0)
    edge_ending: bpy.props.FloatProperty(name="Ending Step", min=0, max=1, default=1)
    edge_mode: bpy.props.EnumProperty(
        name="Mode",
        items=[("0", "Balanced", "Balanced"),
               ("1", "My prompt is more important", "My prompt is is more important"),
               ("2", "ControlNet is more important", "ControlNet is more important")
               ],
        default="0"
    )
    edge_model: bpy.props.EnumProperty(
        name="Model",
        items=[("canny", "Canny", "Canny"),
               ("mlsd", "MLSD", "MLSD"),
               ("scribble", "Scribble", "Scribble"),
               ("softedge", "SoftEdge", "SoftEdge"),
               ("lineart", "Lineart", "Lineart")
               ],
        default="scribble"
    )


class ControlNetRenderStateProperties(bpy.types.PropertyGroup):
    generating: bpy.props.BoolProperty(default=False)
