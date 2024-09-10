// PhysicsEngineAndLevelEditor is a 2D physics engine and level editor
// in python, using pygame and pymunk, and rendering through openGL

// Copyright (C) 2024  Emmet Schell

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// any later version.

// this program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

// To contact the author of this program, Email them at
// emmetschell@gmail.com.

#version 330 core

uniform sampler2D tex1;
uniform sampler2D tex2;
uniform float time;
uniform float amplitude;
uniform float rate;
uniform float warp;
uniform vec2 center;
uniform vec2 cam;
uniform vec2 lightoffset;
uniform float aspect_ratio;
uniform int screen_height;
uniform int screen_width;
uniform float light_intensity;
uniform float shadow_fade;
uniform vec3 light_color;

in vec2 uvs;
out vec4 layered;

vec4 layer(vec4 foreground, vec4 background);

void main() {
    vec3 shadowcolor = vec3(-1, -1, -1);
    vec3 lightcolor = vec3(light_color);
    vec4 foreground = vec4(texture(tex2, uvs).rgb, 1);

    //removes black background of the foreground texture
    if (foreground.rgba == vec4(0, 0, 0, 1)) {
        foreground.rbga = vec4(0, 0, 0, 0);
    }

    vec2 sine_x_uvs = vec2(uvs.x + sin(uvs.y * 10 + time * rate) * amplitude, uvs.y);

    vec2 center = vec2(center.x + sin(uvs.y * 10 + time * rate) * amplitude, center.y);
    vec2 off_center = (sine_x_uvs) - center;
    off_center *= 1.0 + 0.8 * pow(abs(off_center.yx), vec2(warp));
    vec2 CRT_uvs = center + off_center;

    //  + sin(uvs.y * 10 + time * rate) * amplitude adding this code made the lights not do the sine thing

    vec2 light_center = vec2((center.x + ((cam.x + lightoffset.x) / screen_width * aspect_ratio)), center.y + (cam.y + lightoffset.y) / screen_height);
    float light_off_center = sqrt( ((CRT_uvs.x * aspect_ratio - light_center.x) * (CRT_uvs.x * aspect_ratio - light_center.x)) + ((CRT_uvs.y - light_center.y) * (CRT_uvs.y - light_center.y)) );
    vec2 light_off_center_vec2 = vec2(light_off_center, light_off_center);
    vec2 light_on_center = (1 / vec2(abs(light_off_center_vec2.x / light_intensity), abs(light_off_center_vec2.y / light_intensity)));
    light_off_center_vec2 = vec2(light_off_center_vec2.x / shadow_fade, light_off_center_vec2.y / shadow_fade);

    float foo = aspect_ratio;

    vec4 background = vec4(mix(
        mix(mix(texture(tex1, CRT_uvs).rgb, shadowcolor.rgb, abs(light_off_center_vec2.x)),
        mix(texture(tex1, CRT_uvs).rgb, shadowcolor.rgb, abs(light_off_center_vec2.y)), 0.5),

        mix(mix(texture(tex1, CRT_uvs).rgb, lightcolor.rgb, abs(light_on_center.x)),
        mix(texture(tex1, CRT_uvs).rgb, lightcolor.rgb, abs(light_on_center.y)), 0.5),

        0.0005)
    , 1.0);

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