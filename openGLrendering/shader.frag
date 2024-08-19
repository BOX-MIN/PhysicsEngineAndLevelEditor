#version 330 core

uniform sampler2D tex1;
uniform sampler2D tex2;
uniform float time;
uniform float amplitude;
uniform float rate;
uniform float warp;
uniform vec2 center;

in vec2 uvs;
out vec4 layered;

vec4 layer(vec4 foreground, vec4 background);

void main() {
    vec4 foreground = vec4(texture(tex2, uvs).rgb, 1);

    //removes black background of the foreground texture
    if (foreground.rgba == vec4(0, 0, 0, 1)) {
        foreground.rbga = vec4(0, 0, 0, 0);
    }

    vec2 sine_x_uvs = vec2(uvs.x + sin(uvs.y * 10 + time * rate) * amplitude, uvs.y);

    vec2 center = vec2(center.x + sin(uvs.y * 10 + time * rate) * amplitude, center.y);
    vec2 off_center = sine_x_uvs - center;
    off_center *= 1.0 + 0.8 * pow(abs(off_center.yx), vec2(warp));
    vec2 CRT_uvs = center + off_center;

    vec4 background = vec4(texture(tex1, CRT_uvs).rgb, 1.0);

    if (CRT_uvs.x > 1.0 ||
        CRT_uvs.x < 0.0 ||
        CRT_uvs.y > 1.0 ||
        CRT_uvs.y < 0.0) {
            background=vec4(0.0, 0.0, 0.0, 1.0);
        }


    layered = layer(foreground, background);
}

vec4 layer(vec4 foreground, vec4 background) {
    return foreground * foreground.a + background * (1.0 - foreground.a);
}