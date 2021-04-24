#version 330 core

in vec2 UV;

out vec4 color;

uniform sampler2D textureSampler;

void main() {
    vec4 fontPixel = texture(textureSampler, UV);
    color = fontPixel;
}

