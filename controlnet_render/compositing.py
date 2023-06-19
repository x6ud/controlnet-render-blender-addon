import bpy
from .constants import RENDER_OUTPUT_PATH


def ensure_node(tree, node_name, node_type, x, y):
    node = tree.nodes.get(node_name)
    new = False
    if not node:
        node = tree.nodes.new(node_type)
        node.name = node_name
        node.select = False
        node.location.x = x
        node.location.y = y
        new = True
    return node, new


def create_node(tree, node_type, x, y):
    node = tree.nodes.new(node_type)
    node.select = False
    node.location.x = x
    node.location.y = y
    return node


def link_nodes(tree, from_node, from_socket_name, to_node, to_socket_name):
    tree.links.new(from_node.outputs[from_socket_name], to_node.inputs[to_socket_name])


def prepare_vector_scalar_mul_node_group():
    tree = bpy.data.node_groups.get("CN Vector Scalar Mul")
    if tree:
        return
    tree = bpy.data.node_groups.new("CN Vector Scalar Mul", "CompositorNodeTree")
    tree.use_fake_user = True
    tree.inputs.new("NodeSocketVector", "Vector")
    tree.inputs.new("NodeSocketFloat", "Value")
    tree.outputs.new("NodeSocketVector", "Vector")
    input = create_node(tree, "NodeGroupInput", 0, 0)
    sep_xyz = create_node(tree, "CompositorNodeSeparateXYZ", 200, 0)
    link_nodes(tree, input, 0, sep_xyz, 0)
    mul_x = create_node(tree, "CompositorNodeMath", 400, 0)
    mul_x.operation = "MULTIPLY"
    link_nodes(tree, sep_xyz, 0, mul_x, 0)
    link_nodes(tree, input, 1, mul_x, 1)
    mul_y = create_node(tree, "CompositorNodeMath", 400, -160)
    mul_y.operation = "MULTIPLY"
    link_nodes(tree, sep_xyz, 1, mul_y, 0)
    link_nodes(tree, input, 1, mul_y, 1)
    mul_z = create_node(tree, "CompositorNodeMath", 400, -320)
    mul_z.operation = "MULTIPLY"
    link_nodes(tree, sep_xyz, 2, mul_z, 0)
    link_nodes(tree, input, 1, mul_z, 1)
    comb_xyz = create_node(tree, "CompositorNodeCombineXYZ", 600, 0)
    link_nodes(tree, mul_x, 0, comb_xyz, 0)
    link_nodes(tree, mul_y, 0, comb_xyz, 1)
    link_nodes(tree, mul_z, 0, comb_xyz, 2)
    output = create_node(tree, "NodeGroupOutput", 800, 0)
    link_nodes(tree, comb_xyz, 0, output, 0)


def prepare_vector_add_node_group():
    tree = bpy.data.node_groups.get("CN Vector Add")
    if tree:
        return
    tree = bpy.data.node_groups.new("CN Vector Add", "CompositorNodeTree")
    tree.use_fake_user = True
    tree.inputs.new("NodeSocketVector", "Vector")
    tree.inputs.new("NodeSocketVector", "Vector")
    tree.outputs.new("NodeSocketVector", "Vector")
    input = create_node(tree, "NodeGroupInput", 0, 0)
    sep_1 = create_node(tree, "CompositorNodeSeparateXYZ", 200, 0)
    link_nodes(tree, input, 0, sep_1, 0)
    sep_2 = create_node(tree, "CompositorNodeSeparateXYZ", 200, -160)
    link_nodes(tree, input, 1, sep_2, 0)
    add_x = create_node(tree, "CompositorNodeMath", 400, 0)
    add_x.operation = "ADD"
    link_nodes(tree, sep_1, 0, add_x, 0)
    link_nodes(tree, sep_2, 0, add_x, 1)
    add_y = create_node(tree, "CompositorNodeMath", 400, -160)
    add_y.operation = "ADD"
    link_nodes(tree, sep_1, 1, add_y, 0)
    link_nodes(tree, sep_2, 1, add_y, 1)
    add_z = create_node(tree, "CompositorNodeMath", 400, -320)
    add_z.operation = "ADD"
    link_nodes(tree, sep_1, 2, add_z, 0)
    link_nodes(tree, sep_2, 2, add_z, 1)
    comb_xyz = create_node(tree, "CompositorNodeCombineXYZ", 600, 0)
    link_nodes(tree, add_x, 0, comb_xyz, 0)
    link_nodes(tree, add_y, 0, comb_xyz, 1)
    link_nodes(tree, add_z, 0, comb_xyz, 2)
    output = create_node(tree, "NodeGroupOutput", 800, 0)
    link_nodes(tree, comb_xyz, 0, output, 0)


def prepare_vector_cross_node_group():
    tree = bpy.data.node_groups.get("CN Vector Cross")
    if tree:
        return
    tree = bpy.data.node_groups.new("CN Vector Cross", "CompositorNodeTree")
    tree.use_fake_user = True
    tree.inputs.new("NodeSocketVector", "Vector")
    tree.inputs.new("NodeSocketVector", "Vector")
    tree.outputs.new("NodeSocketVector", "Vector")
    input = create_node(tree, "NodeGroupInput", 0, 0)
    a = create_node(tree, "CompositorNodeSeparateXYZ", 200, 0)
    link_nodes(tree, input, 0, a, 0)
    b = create_node(tree, "CompositorNodeSeparateXYZ", 200, -160)
    link_nodes(tree, input, 1, b, 0)
    ay_bz = create_node(tree, "CompositorNodeMath", 400, 0)
    ay_bz.operation = "MULTIPLY"
    link_nodes(tree, a, 1, ay_bz, 0)
    link_nodes(tree, b, 2, ay_bz, 1)
    az_bx = create_node(tree, "CompositorNodeMath", 400, -160)
    az_bx.operation = "MULTIPLY"
    link_nodes(tree, a, 2, az_bx, 0)
    link_nodes(tree, b, 0, az_bx, 1)
    ax_by = create_node(tree, "CompositorNodeMath", 400, -160 * 2)
    ax_by.operation = "MULTIPLY"
    link_nodes(tree, a, 0, ax_by, 0)
    link_nodes(tree, b, 1, ax_by, 1)
    az_by = create_node(tree, "CompositorNodeMath", 400, -160 * 3)
    az_by.operation = "MULTIPLY"
    link_nodes(tree, a, 2, az_by, 0)
    link_nodes(tree, b, 1, az_by, 1)
    ax_bz = create_node(tree, "CompositorNodeMath", 400, -160 * 4)
    ax_bz.operation = "MULTIPLY"
    link_nodes(tree, a, 0, ax_bz, 0)
    link_nodes(tree, b, 2, ax_bz, 1)
    ay_bx = create_node(tree, "CompositorNodeMath", 400, -160 * 5)
    ay_bx.operation = "MULTIPLY"
    link_nodes(tree, a, 1, ay_bx, 0)
    link_nodes(tree, b, 0, ay_bx, 1)
    cx = create_node(tree, "CompositorNodeMath", 600, 0)
    cx.operation = "SUBTRACT"
    link_nodes(tree, ay_bz, 0, cx, 0)
    link_nodes(tree, az_by, 0, cx, 1)
    cy = create_node(tree, "CompositorNodeMath", 600, -160)
    cy.operation = "SUBTRACT"
    link_nodes(tree, az_bx, 0, cy, 0)
    link_nodes(tree, ax_bz, 0, cy, 1)
    cz = create_node(tree, "CompositorNodeMath", 600, -320)
    cz.operation = "SUBTRACT"
    link_nodes(tree, ax_by, 0, cz, 0)
    link_nodes(tree, ay_bx, 0, cz, 1)
    comb_xyz = create_node(tree, "CompositorNodeCombineXYZ", 800, 0)
    link_nodes(tree, cx, 0, comb_xyz, 0)
    link_nodes(tree, cy, 0, comb_xyz, 1)
    link_nodes(tree, cz, 0, comb_xyz, 2)
    output = create_node(tree, "NodeGroupOutput", 1000, 0)
    link_nodes(tree, comb_xyz, 0, output, 0)


def prepare_vector_quat_transform_node_group():
    tree = bpy.data.node_groups.get("CN Vector Quat Transform")
    if tree:
        return
    tree = bpy.data.node_groups.new("CN Vector Quat Transform", "CompositorNodeTree")
    tree.use_fake_user = True
    tree.inputs.new("NodeSocketFloat", "Quat X")
    tree.inputs.new("NodeSocketFloat", "Quat Y")
    tree.inputs.new("NodeSocketFloat", "Quat Z")
    tree.inputs.new("NodeSocketFloat", "Quat W")
    tree.inputs.new("NodeSocketVector", "Vector")
    tree.outputs.new("NodeSocketVector", "Vector")
    input = create_node(tree, "NodeGroupInput", 0, 0)
    qv = create_node(tree, "CompositorNodeCombineXYZ", 200, 0)
    link_nodes(tree, input, "Quat X", qv, 0)
    link_nodes(tree, input, "Quat Y", qv, 1)
    link_nodes(tree, input, "Quat Z", qv, 2)
    uv = create_node(tree, "CompositorNodeGroup", 400, 0)
    uv.node_tree = bpy.data.node_groups["CN Vector Cross"]
    link_nodes(tree, qv, 0, uv, 0)
    link_nodes(tree, input, "Vector", uv, 1)
    uuv = create_node(tree, "CompositorNodeGroup", 600, 0)
    uuv.node_tree = bpy.data.node_groups["CN Vector Cross"]
    link_nodes(tree, qv, 0, uuv, 0)
    link_nodes(tree, uv, 0, uuv, 1)
    w2 = create_node(tree, "CompositorNodeMath", 600, -160)
    w2.operation = "MULTIPLY"
    w2.inputs[1].default_value = 2.0
    link_nodes(tree, input, "Quat W", w2, 0)
    uv2 = create_node(tree, "CompositorNodeGroup", 800, 0)
    uv2.node_tree = bpy.data.node_groups["CN Vector Scalar Mul"]
    link_nodes(tree, uv, 0, uv2, 0)
    link_nodes(tree, w2, 0, uv2, 1)
    uuv2 = create_node(tree, "CompositorNodeGroup", 800, -160)
    uuv2.node_tree = bpy.data.node_groups["CN Vector Scalar Mul"]
    uuv2.inputs[1].default_value = 2.0
    link_nodes(tree, uuv, 0, uuv2, 0)
    uv_uuv = create_node(tree, "CompositorNodeGroup", 1000, 0)
    uv_uuv.node_tree = bpy.data.node_groups["CN Vector Add"]
    link_nodes(tree, uv2, 0, uv_uuv, 0)
    link_nodes(tree, uuv2, 0, uv_uuv, 1)
    uv_uuv_v = create_node(tree, "CompositorNodeGroup", 1000, -160)
    uv_uuv_v.node_tree = bpy.data.node_groups["CN Vector Add"]
    link_nodes(tree, uv_uuv, 0, uv_uuv_v, 0)
    link_nodes(tree, input, "Vector", uv_uuv_v, 1)
    output = create_node(tree, "NodeGroupOutput", 1200, 0)
    link_nodes(tree, uv_uuv_v, 0, output, 0)


def prepare_compositor():
    bpy.context.view_layer.use_pass_z = True
    bpy.context.view_layer.use_pass_normal = True
    # bpy.context.view_layer.use_pass_object_index = True
    bpy.context.scene.use_nodes = True
    # bpy.context.scene.render.engine = "CYCLES"
    # bpy.context.scene.cycles.device = "GPU"

    prepare_vector_scalar_mul_node_group()
    prepare_vector_add_node_group()
    prepare_vector_cross_node_group()
    prepare_vector_quat_transform_node_group()

    tree = bpy.context.scene.node_tree

    # ==================== image ====================
    render_layers, new = ensure_node(tree, "Render Layers", "CompositorNodeRLayers", 0, 260)
    composite, new = ensure_node(tree, "Composite", "CompositorNodeComposite", 320, 460)
    if new:
        link_nodes(tree, render_layers, "Image", composite, "Image")
    image_viewer, new = ensure_node(tree, "CN Image Viewer", "CompositorNodeViewer", 480, 460)
    if new:
        link_nodes(tree, render_layers, "Image", image_viewer, "Image")

    # ==================== depth ====================
    depth_normalize, new = ensure_node(tree, "CN Depth Normalize", "CompositorNodeNormalize", 320, 140)
    if new:
        link_nodes(tree, render_layers, "Depth", depth_normalize, "Value")
    depth_invert, new = ensure_node(tree, "CN Depth Invert", "CompositorNodeInvert", 480, 140)
    if new:
        link_nodes(tree, depth_normalize, "Value", depth_invert, "Color")
    depth_color_ramp, new = ensure_node(tree, "CN Depth Color Ramp", "CompositorNodeValToRGB", 640, 140)
    if new:
        link_nodes(tree, depth_invert, "Color", depth_color_ramp, "Fac")
    depth_viewer, new = ensure_node(tree, "CN Depth Viewer", "CompositorNodeViewer", 900, 140)
    if new:
        link_nodes(tree, depth_color_ramp, "Image", depth_viewer, "Image")

    # ==================== depth edge ====================
    depth_laplace, new = ensure_node(tree, "CN Depth Laplace", "CompositorNodeFilter", 320, -100)
    if new:
        depth_laplace.filter_type = "LAPLACE"
        link_nodes(tree, render_layers, "Depth", depth_laplace, "Image")
    depth_edge_color_ramp, new = ensure_node(tree, "CN Depth Edge Color Ramp", "CompositorNodeValToRGB", 480, -100)
    if new:
        depth_edge_color_ramp.color_ramp.elements[0].position = 0.1
        link_nodes(tree, depth_laplace, "Image", depth_edge_color_ramp, "Fac")

    # ==================== normal edge ====================
    normal_laplace, new = ensure_node(tree, "CN Normal Laplace", "CompositorNodeFilter", 320, -320)
    if new:
        normal_laplace.filter_type = "LAPLACE"
        link_nodes(tree, render_layers, "Normal", normal_laplace, "Image")
    normal_edge_color_ramp, new = ensure_node(tree, "CN Normal Edge Color Ramp", "CompositorNodeValToRGB", 480, -320)
    if new:
        normal_edge_color_ramp.color_ramp.elements[0].position = 0.1
        link_nodes(tree, normal_laplace, "Image", normal_edge_color_ramp, "Fac")

    # ==================== mixed edge ====================
    edge_mix, new = ensure_node(tree, "CN Edge Mix", "CompositorNodeMixRGB", 740, -100)
    if new:
        edge_mix.blend_type = "LIGHTEN"
        link_nodes(tree, depth_edge_color_ramp, "Image", edge_mix, 1)
        link_nodes(tree, normal_edge_color_ramp, "Image", edge_mix, 2)
    edge_viewer, new = ensure_node(tree, "CN Edge Viewer", "CompositorNodeViewer", 900, -100)
    if new:
        link_nodes(tree, edge_mix, "Image", edge_viewer, "Image")

    # ==================== normal ====================
    normal_transform, new = ensure_node(tree, "CN Normal Transform", "CompositorNodeGroup", 320, -560)
    if new:
        normal_transform.node_tree = bpy.data.node_groups["CN Vector Quat Transform"]
        link_nodes(tree, render_layers, "Normal", normal_transform, "Vector")
    normal_sep_xyz, new = ensure_node(tree, "CN Normal Sep XYZ", "CompositorNodeSeparateXYZ", 480, -560)
    if new:
        link_nodes(tree, normal_transform, 0, normal_sep_xyz, 0)
    normal_invert_x, new = ensure_node(tree, "CN Normal Invert X", "CompositorNodeMath", 480, -700)
    if new:
        normal_invert_x.operation = "MULTIPLY"
        normal_invert_x.inputs[1].default_value = -1
        link_nodes(tree, normal_sep_xyz, 0, normal_invert_x, 0)
    normal_comb_color, new = ensure_node(tree, "CN Normal Comb Color", "CompositorNodeCombineColor", 660, -560)
    if new:
        link_nodes(tree, normal_invert_x, 0, normal_comb_color, "Red")
        link_nodes(tree, normal_sep_xyz, 1, normal_comb_color, "Green")
        link_nodes(tree, normal_sep_xyz, 2, normal_comb_color, "Blue")
    normal_switch, new = ensure_node(tree, "CN Normal Switch", "CompositorNodeSwitch", 820, -560)
    if new:
        link_nodes(tree, normal_comb_color, 0, normal_switch, "On")
        link_nodes(tree, render_layers, "Normal", normal_switch, "Off")
    normal_viewer, new = ensure_node(tree, "CN Normal Viewer", "CompositorNodeViewer", 980, -560)
    if new:
        link_nodes(tree, normal_switch, "Image", normal_viewer, "Image")

    # ==================== output ====================
    output_file, new = ensure_node(tree, "CN Output File", "CompositorNodeOutputFile", 1120, 0)
    if new:
        output_file.base_path = RENDER_OUTPUT_PATH

        output_file.file_slots.new("Depth")
        output_file.file_slots.new("Edge")
        output_file.file_slots.new("Normal")

        link_nodes(tree, render_layers, "Image", output_file, "Image")
        link_nodes(tree, depth_color_ramp, "Image", output_file, "Depth")
        link_nodes(tree, edge_mix, "Image", output_file, "Edge")
        link_nodes(tree, normal_switch, "Image", output_file, "Normal")


def setup_normal_camera_transform():
    tree = bpy.context.scene.node_tree
    normal_transform = tree.nodes["CN Normal Transform"]
    quat = bpy.context.scene.camera.rotation_euler.to_quaternion()
    quat.invert()
    normal_transform.inputs["Quat X"].default_value = quat.x
    normal_transform.inputs["Quat Y"].default_value = quat.y
    normal_transform.inputs["Quat Z"].default_value = quat.z
    normal_transform.inputs["Quat W"].default_value = quat.w


def set_normal_transform_enabled(b: bool):
    tree = bpy.context.scene.node_tree
    normal_switch = tree.nodes["CN Normal Switch"]
    normal_switch.check = b


def setup_compositor():
    prepare_compositor()
    setup_normal_camera_transform()
    set_normal_transform_enabled(bpy.context.scene.controlnet_render_properties.normal)
    bpy.context.scene.render.resolution_x = bpy.context.scene.controlnet_render_properties.width
    bpy.context.scene.render.resolution_y = bpy.context.scene.controlnet_render_properties.height
