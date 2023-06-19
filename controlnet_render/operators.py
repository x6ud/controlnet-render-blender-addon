import bpy
from .compositing import setup_compositor
from .misc import show_message, header_text_progress, get_current_image_editor, load_rendered_image, image_2_png_base64, \
    event_loop_run_once
from .constants import RENDER_OUTPUT_PATH, IMG_2_IMG_NAME, DEPTH_NAME, NORMAL_NAME, EDGE_NAME, SD_OUTPUT_NAME
import requests
from .http_request import http_request
import asyncio
from asyncio import events
import json
import base64


class ControlNetRenderOperator(bpy.types.Operator):
    bl_idname = "controlnet_render.render"
    bl_label = "Render ControlNet Images"

    def execute(self, context):
        if not bpy.data.is_saved:
            show_message("Please save the file first")
            return {"FINISHED"}

        current_image_name = None
        image_editor = get_current_image_editor()
        if image_editor and image_editor.image:
            current_image_name = image_editor.image.name

        setup_compositor()
        bpy.ops.render.render(use_viewport=True)
        frame = str(bpy.context.scene.frame_current).zfill(4)
        load_rendered_image("Image" + frame, "ControlNet img2img")
        load_rendered_image("Depth" + frame, "ControlNet Depth")
        load_rendered_image("Normal" + frame, "ControlNet Normal")
        load_rendered_image("Edge" + frame, "ControlNet Edge")

        if image_editor and current_image_name:
            image_editor.image = bpy.data.images.get(current_image_name)

        return {"FINISHED"}


class ControlNetGenerateOperator(bpy.types.Operator):
    bl_idname = "controlnet_render.generate"
    bl_label = "Generate"

    def execute(self, context):
        if not bpy.data.is_saved:
            show_message("Please save the file first")
            return {"FINISHED"}

        # ==================== check input images ====================
        input_img2img = bpy.data.images.get(IMG_2_IMG_NAME)
        input_depth = bpy.data.images.get(DEPTH_NAME)
        input_normal = bpy.data.images.get(NORMAL_NAME)
        input_edge = bpy.data.images.get(EDGE_NAME)
        options = context.scene.controlnet_render_properties
        if (options.img2img and not input_img2img
                or options.depth and not input_depth
                or options.normal and not input_normal
                or options.edge and not input_edge):
            show_message("Please render input images first")
            return {"FINISHED"}

        # ==================== build request json ====================
        base_url = options.webui_url
        self._base_url = base_url
        req_url = base_url + ("/sdapi/v1/img2img" if options.img2img else "/sdapi/v1/txt2img")
        req_json = {
            "prompt": options.prompt,
            "negative_prompt": options.negative_prompt,
            "width": options.width,
            "height": options.height,
            "restore_faces": options.restore_faces,
            "tiling": options.tiling,
            "sampler_name": options.sampling_method,
            "steps": options.sampling_steps,
            "cfg_scale": options.cfg_scale,
            "seed": options.seed,
        }

        # ==================== img2img ====================
        if options.img2img:
            req_json["init_images"] = [
                image_2_png_base64(input_img2img)
            ]
            req_json["denoising_strength"] = options.denoising_strength

        # ==================== controlnet args ====================
        controlnet_args = []
        if options.depth or options.normal or options.edge:
            try:
                res = requests.get(base_url + "/controlnet/model_list", timeout=5)
            except BaseException as e:
                show_message(str(e), "Error", "ERROR")
                return {"FINISHED"}
            if res.status_code != 200:
                show_message(f"Network error [{res.status_code}]", "Error", "ERROR")
                print(res.reason)
                return {"FINISHED"}
            model_list = res.json()["model_list"]

            if options.depth:
                model = next((model for model in model_list if "depth" in model), None)
                if not model:
                    show_message("Could not find depth model for ControlNet. Is it installed?", "Error", "ERROR")
                    return {"FINISHED"}
                controlnet_args.append({
                    "input_image": image_2_png_base64(input_depth),
                    "model": model,
                    "module": "none",
                    "weight": options.depth_weight,
                    "guidance_start": options.depth_starting,
                    "guidance_end": options.depth_ending,
                    "control_mode": int(options.depth_mode)
                })

            if options.normal:
                model = next((model for model in model_list if "normal" in model), None)
                if not model:
                    show_message("Could not find normal model for ControlNet. Is it installed?", "Error", "ERROR")
                    return {"FINISHED"}
                controlnet_args.append({
                    "input_image": image_2_png_base64(input_normal),
                    "model": model,
                    "module": "none",
                    "weight": options.normal_weight,
                    "guidance_start": options.normal_starting,
                    "guidance_end": options.normal_ending,
                    "control_mode": int(options.normal_mode)
                })

            if options.edge:
                model_name = options.edge_model
                model = next((model for model in model_list if model_name in model), None)
                if not model:
                    show_message(f"Could not find {model_name} model for ControlNet. Is it installed?",
                                 "Error", "ERROR")
                    return {"FINISHED"}
                controlnet_args.append({
                    "input_image": image_2_png_base64(input_edge),
                    "model": model,
                    "module": "none",
                    "weight": options.edge_weight,
                    "guidance_start": options.edge_starting,
                    "guidance_end": options.edge_ending,
                    "control_mode": int(options.edge_mode)
                })

        if len(controlnet_args):
            req_json["alwayson_scripts"] = {
                "controlnet": {
                    "args": controlnet_args
                }
            }

        # ==================== do http request ====================
        loop = asyncio.get_event_loop()
        loop.set_debug(True)
        events._set_running_loop(loop)
        self._fut = loop.create_task(
            http_request(req_url, method="POST", json=req_json)
        )
        self._timer = context.window_manager.event_timer_add(0.002, window=context.window)
        self._time = self._fut.get_loop().time()
        context.window_manager.modal_handler_add(self)
        context.window_manager.progress_begin(0, 1.0)
        context.window_manager.controlnet_render_state.generating = True

        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        if event.type == "TIMER":
            finished = False
            fut = self._fut
            if fut:
                event_loop_run_once(fut.get_loop())
                if fut.done():
                    # ==================== done ====================
                    finished = True
                    self._handle_response(fut.result())
                elif fut.cancelled():
                    # ==================== cancelled ====================
                    finished = True
                else:
                    # ==================== progressing ====================
                    time = fut.get_loop().time()
                    det_time = time - self._time
                    if det_time > 0.5:
                        self._time = time
                        url = self._base_url + "/sdapi/v1/progress"
                        try:
                            res = requests.get(url, timeout=2)
                            if res.status_code == 200:
                                data = res.json()
                                progress = data["progress"]
                                if progress > 0:
                                    context.window_manager.progress_update(progress)
                                    header_text_progress('Generating...', progress)
                                    img_b64 = data["current_image"]
                                    if img_b64:
                                        self._save_output_image(img_b64, True)
                        except BaseException as err:
                            print(err)
            else:
                finished = True
            if finished:
                context.window_manager.event_timer_remove(self._timer)
                context.window_manager.progress_end()
                context.window_manager.controlnet_render_state.generating = False
                bpy.context.area.header_text_set(None)
                return {"FINISHED"}

        return {"PASS_THROUGH"}

    def _handle_response(self, res):
        data = res["data"].decode("utf-8")
        if res["status"] != 200:
            show_message(data, "Error", "ERROR")
            return
        res = json.loads(data)
        img_b64 = res["images"][0]
        self._save_output_image(img_b64)

    def _save_output_image(self, img_b64, resize=False):
        img_bin = base64.b64decode(img_b64)
        frame = str(bpy.context.scene.frame_current).zfill(4)
        file_name = f"SD_Output{frame}"
        file_path = bpy.path.abspath(f"{RENDER_OUTPUT_PATH}/{file_name}.png")
        with open(file_path, "wb") as file:
            file.write(img_bin)
        load_rendered_image(file_name, SD_OUTPUT_NAME)
        image_editor = get_current_image_editor()
        if resize:
            image = bpy.data.images.get(SD_OUTPUT_NAME)
            image.scale(bpy.context.scene.controlnet_render_properties.width,
                        bpy.context.scene.controlnet_render_properties.height)
        if image_editor:
            image_editor.image = bpy.data.images.get(SD_OUTPUT_NAME)
            bpy.context.region.tag_redraw()
