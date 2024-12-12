/*
 * eos - A 3D Morphable Model fitting library written in modern C++11/14.
 *
 * File: include/eos/render/detail/utils.hpp
 *
 * Copyright 2014-2017, 2023 Patrik Huber
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#pragma once

#ifndef EOS_RENDER_DETAIL_UTILS_HPP
#define EOS_RENDER_DETAIL_UTILS_HPP

#include "eos/core/Rect.hpp"
#include "eos/render/detail/Vertex.hpp"

#include "Eigen/Core"

#include <algorithm>
#include <cmath>

/**
 * Implementations of internal functions, not part of the
 * API we expose and not meant to be used by a user.
 */
namespace eos {
namespace render {
namespace detail {

/**
 * Calculates the enclosing bounding box of 3 vertices (a triangle). If the
 * triangle is partly outside the screen, it will be clipped appropriately.
 *
 * Todo: If it is fully outside the screen, check what happens, but it works.
 *
 * @param[in] v0 First vertex.
 * @param[in] v1 Second vertex.
 * @param[in] v2 Third vertex.
 * @param[in] viewport_width Screen width.
 * @param[in] viewport_height Screen height.
 * @return A bounding box rectangle.
 */
template <typename T>
core::Rect<int> calculate_clipped_bounding_box(const Eigen::Vector2<T>& v0, const Eigen::Vector2<T>& v1,
                                               const Eigen::Vector2<T>& v2, int viewport_width,
                                               int viewport_height)
{
    /* Old, producing artifacts:
    t.minX = max(min(t.v0.position[0], min(t.v1.position[0], t.v2.position[0])), 0.0f);
    t.maxX = min(max(t.v0.position[0], max(t.v1.position[0], t.v2.position[0])), (float)(viewportWidth - 1));
    t.minY = max(min(t.v0.position[1], min(t.v1.position[1], t.v2.position[1])), 0.0f);
    t.maxY = min(max(t.v0.position[1], max(t.v1.position[1], t.v2.position[1])), (float)(viewportHeight -
    1));*/

    using std::ceil;
    using std::floor;
    using std::max;
    using std::min;
    // Readded this comment after merge: What about rounding, or rather the conversion from double to int?
    const int minX = max(min(floor(v0[0]), min(floor(v1[0]), floor(v2[0]))), T(0));
    const int maxX = min(max(ceil(v0[0]), max(ceil(v1[0]), ceil(v2[0]))), static_cast<T>(viewport_width - 1));
    const int minY = max(min(floor(v0[1]), min(floor(v1[1]), floor(v2[1]))), T(0));
    const int maxY = min(max(ceil(v0[1]), max(ceil(v1[1]), ceil(v2[1]))), static_cast<T>(viewport_height - 1));
    return core::Rect<int>{minX, minY, maxX - minX, maxY - minY};
};

/**
 * Computes whether the triangle formed out of the given three vertices is
 * counter-clockwise in screen space. Assumes the origin of the screen is on
 * the top-left, and the y-axis goes down (as in OpenCV images).
 *
 * @param[in] v0 First vertex.
 * @param[in] v1 Second vertex.
 * @param[in] v2 Third vertex.
 * @return Whether the vertices are CCW in screen space.
 */
template <typename T>
bool are_vertices_ccw_in_screen_space(const Eigen::Vector2<T>& v0, const Eigen::Vector2<T>& v1,
                                      const Eigen::Vector2<T>& v2)
{
    const auto dx01 = v1[0] - v0[0]; // Note: Could replace with .x() and .y()
    const auto dy01 = v1[1] - v0[1];
    const auto dx02 = v2[0] - v0[0];
    const auto dy02 = v2[1] - v0[1];

    return (dx01 * dy02 - dy01 * dx02 < T(0)); // Original: (dx01*dy02 - dy01*dx02 > 0.0f). But: OpenCV has origin top-left, y goes down
};

template <typename T>
double implicit_line(float x, float y, const Eigen::Vector4<T>& v1, const Eigen::Vector4<T>& v2)
{
    return ((double)v1[1] - (double)v2[1]) * (double)x + ((double)v2[0] - (double)v1[0]) * (double)y +
           (double)v1[0] * (double)v2[1] - (double)v2[0] * (double)v1[1];
};

inline std::vector<Vertex<float>> clip_polygon_to_plane_in_4d(const std::vector<Vertex<float>>& vertices,
                                                              const Eigen::Vector4<float>& plane_normal)
{
    std::vector<Vertex<float>> clipped_vertices;

    // We can have 2 cases:
    //  * 1 vertex visible: we make 1 new triangle out of the visible vertex plus the 2 intersection points
    //    with the near-plane
    //  * 2 vertices visible: we have a quad, so we have to make 2 new triangles out of it.

    // See here for more info?
    // http://math.stackexchange.com/questions/400268/equation-for-a-line-through-a-plane-in-homogeneous-coordinates

    for (unsigned int i = 0; i < vertices.size(); i++)
    {
        const int a = i;                         // the current vertex
        const int b = (i + 1) % vertices.size(); // the following vertex (wraps around 0)

        const float fa = vertices[a].position.dot(plane_normal); // Note: Shouldn't they be unit length?
        const float fb = vertices[b].position.dot(plane_normal); // < 0 means on visible side, > 0 means on invisible side?

        if ((fa < 0 && fb > 0) || (fa > 0 && fb < 0)) // one vertex is on the visible side of the plane, one
                                                      // on the invisible? so we need to split?
        {
            const auto direction = vertices[b].position - vertices[a].position;
            const float t = -(plane_normal.dot(vertices[a].position)) /
                            plane_normal.dot(direction); // the parametric value on the line, where the line
                                                         // to draw intersects the plane?

            // generate a new vertex at the line-plane intersection point
            const auto position = vertices[a].position + t * direction;
            const auto color = vertices[a].color + t * (vertices[b].color - vertices[a].color);
            const auto texcoords =
                vertices[a].texcoords +
                t * (vertices[b].texcoords -
                     vertices[a].texcoords); // We could omit that if we don't render with texture.

            if (fa < 0) // we keep the original vertex plus the new one
            {
                clipped_vertices.push_back(vertices[a]);
                clipped_vertices.push_back(Vertex<float>{position, color, texcoords});
            } else if (fb < 0) // we use only the new vertex
            {
                clipped_vertices.push_back(Vertex<float>{position, color, texcoords});
            }
        } else if (fa < 0 && fb < 0) // both are visible (on the "good" side of the plane), no splitting
                                     // required, use the current vertex
        {
            clipped_vertices.push_back(vertices[a]);
        }
        // else, both vertices are not visible, nothing to add and draw
    }

    return clipped_vertices;
};

/**
 * @brief Todo.
 *
 * Takes in clip coords? and outputs NDC.
 * divides by w and outputs [x_ndc, y_ndc, z_ndc, 1/w_clip].
 * The w-component is set to 1/w_clip (which is what OpenGL passes to the FragmentShader).
 *
 * @param[in] vertex X.
 * @ return X.
 */
template <typename T>
Eigen::Vector4<T> divide_by_w(const Eigen::Vector4<T>& vertex)
{
    const auto one_over_w = 1.0 / vertex.w();
    // divide by w: (if ortho, w will just be 1)
    Eigen::Vector4<T> v_ndc = vertex / vertex.w();
    // Set the w coord to 1/w (i.e. 1/w_clip). This is what OpenGL passes to the FragmentShader.
    v_ndc.w() = one_over_w;
    return v_ndc;
};

} /* namespace detail */
} /* namespace render */
} /* namespace eos */

#endif /* EOS_RENDER_DETAIL_UTILS_HPP */
