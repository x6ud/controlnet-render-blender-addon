import bpy
from .constants import RENDER_OUTPUT_PATH
import base64
import zlib
import struct
import os
import heapq


def show_message(text="", title="Message", icon="INFO"):
    def draw(self, context):
        self.layout.label(text=text)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


def header_text_progress(text, progress):
    try:
        bar_len = 20
        bar = "█" * int(bar_len * progress) + "░" * int(bar_len * (1 - progress))
        bpy.context.area.header_text_set(f'{text} {bar} {int(progress * 100)}%')
    except BaseException as e:
        print(e)


def get_current_image_editor():
    for area in bpy.context.screen.areas:
        for space in area.spaces:
            if space.type == "IMAGE_EDITOR":
                return space
    return None


def load_rendered_image(filename, image_name):
    image = bpy.data.images.get(image_name)
    if image:
        bpy.data.images.remove(image)
    image = bpy.data.images.load(bpy.path.abspath(f"{RENDER_OUTPUT_PATH}/{filename}.png"))
    image.name = image_name
    image.use_fake_user = True


def image_2_png_base64(image):
    if image.filepath and os.path.exists(image.filepath):
        with open(image.filepath, "rb") as file:
            return 'data:image/png;base64,' + base64.b64encode(file.read()).decode()

    # https://blender.stackexchange.com/questions/62072/does-blender-have-a-method-to-a-get-png-formatted-bytearray-for-an-image-via-pyt

    w = image.size[0]
    h = image.size[1]
    buf = bytearray([int(p * 255) for p in image.pixels])

    w4 = w * 4
    raw_data = b''.join(b'\x00' + buf[span:span + w4] for span in range((h - 1) * w4, -1, - w4))

    def png_pack(png_tag, data):
        chunk_head = png_tag + data
        return (struct.pack("!I", len(data)) +
                chunk_head +
                struct.pack("!I", 0xFFFFFFFF & zlib.crc32(chunk_head)))

    png_bytes = b''.join([
        b'\x89PNG\r\n\x1a\n',
        png_pack(b'IHDR', struct.pack("!2I5B", w, h, 8, 6, 0, 0, 0)),
        png_pack(b'IDAT', zlib.compress(raw_data, 9)),
        png_pack(b'IEND', b'')])

    return 'data:image/png;base64,' + base64.b64encode(png_bytes).decode()


_MIN_SCHEDULED_TIMER_HANDLES = 100
_MIN_CANCELLED_TIMER_HANDLES_FRACTION = 0.5
MAXIMUM_SELECT_TIMEOUT = 24 * 3600


def event_loop_run_once(loop):
    # copied and modified from base_events.py

    sched_count = len(loop._scheduled)
    if (sched_count > _MIN_SCHEDULED_TIMER_HANDLES and
            loop._timer_cancelled_count / sched_count > _MIN_CANCELLED_TIMER_HANDLES_FRACTION
    ):
        new_scheduled = []
        for handle in loop._scheduled:
            if handle._cancelled:
                handle._scheduled = False
            else:
                new_scheduled.append(handle)

        heapq.heapify(new_scheduled)
        loop._scheduled = new_scheduled
        loop._timer_cancelled_count = 0
    else:
        while loop._scheduled and loop._scheduled[0]._cancelled:
            loop._timer_cancelled_count -= 1
            handle = heapq.heappop(loop._scheduled)
            handle._scheduled = False

    timeout = 0.01  # this prevent stuck blender editor ui
    if loop._ready or loop._stopping:
        timeout = 0
    elif loop._scheduled:
        when = loop._scheduled[0]._when
        timeout = min(max(0, when - loop.time()), MAXIMUM_SELECT_TIMEOUT)
    loop._process_events(loop._selector.select(timeout))

    end_time = loop.time() + loop._clock_resolution
    while loop._scheduled:
        handle = loop._scheduled[0]
        if handle._when >= end_time:
            break
        handle = heapq.heappop(loop._scheduled)
        handle._scheduled = False
        loop._ready.append(handle)

    ntodo = len(loop._ready)
    for i in range(ntodo):
        handle = loop._ready.popleft()
        if not handle._cancelled:
            handle._run()
