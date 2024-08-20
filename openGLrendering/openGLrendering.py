import moderngl
from array import array
import os.path

ctx = moderngl.create_context()

quad_buffer = ctx.buffer(data=array('f', [
    # position (x, y), uv coordinates (x, y)
    -1.0, 1.0, 0.0, 0.0,  # top left
    1.0, 1.0, 1.0, 0.0,  # top right
    -1.0, -1.0, 0.0, 1.0,  # bottom left
    1.0, -1.0, 1.0, 1.0,  # bottom right
]))

with open(os.path.join('openGLrendering', 'shader.vert')) as file:
    vert_shader = file.read()

with open(os.path.join('openGLrendering', 'shader.frag')) as file:
    frag_shader = file.read()

program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
render_object = ctx.vertex_array(program, [(quad_buffer, '2f 2f', 'vert', 'texcoord')])

def surf_to_texture(surf):
    tex = ctx.texture(surf.get_size(), 4)
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    tex.swizzle = 'BGRA'
    tex.write(surf.get_view('1'))
    return tex
