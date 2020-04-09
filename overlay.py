from __future__ import print_function
import tifffile
import argparse
import numpy as np
from copy import deepcopy
import math


import neuroglancer

ap = argparse.ArgumentParser()
ap.add_argument(
    '-a',
    '--bind-address',
    help='Bind address for Python web server.  Use 127.0.0.1 (the default) to restrict access '
         'to browers running on the local machine, use 0.0.0.0 to permit access from remote browsers.')
ap.add_argument(
    '--static-content-url', help='Obtain the Neuroglancer client code from the specified URL.')
args = ap.parse_args()
if args.bind_address:
    neuroglancer.set_server_bind_address(args.bind_address)
if args.static_content_url:
    neuroglancer.set_static_content_source(url=args.static_content_url)

im = tifffile.imread("testFile3d.tif")
a = np.array(im)
a = np.moveaxis(a, 0, -1)

# creating the numpy "sphere" array
r0 = 30
r1 = 40
r2 = 20
r3 = 25
r4 = 50
r5 = 35
x0, y0, z0 = 642, 370, 70
x1, y1, z1 = 200, 500, 25
x2, y2, z2 = 650, 550, 64
x3, y3, z3 = 660, 280, 64
x4, y4, z4 = 642, 370, 77



dimensions = (a.shape[0], a.shape[1], a.shape[2])
zeros = np.zeros(dimensions)

sphere0 = deepcopy(zeros)
sphere1 = deepcopy(zeros)
sphere2 = deepcopy(zeros)
sphere3 = deepcopy(zeros)
sphere4 = deepcopy(zeros)

for x in range(x0 - r0, x0 + r0):
    for y in range(y0 - r0, y0 + r0):
        for z in range(z0 - r0, z0 + r0):
            distance0 = math.sqrt(math.pow(x - x0, 2) + math.pow(y - y0, 2) + math.pow(z - z0, 2))
            distance1 = math.sqrt(math.pow(x - x1, 2) + math.pow(y - y1, 2) + math.pow(z - z1, 2))
            distance2 = math.sqrt(math.pow(x - x2, 2) + math.pow(y - y2, 2) + math.pow(z - z2, 2))
            distance3 = math.sqrt(math.pow(x - x3, 2) + math.pow(y - y3, 2) + math.pow(z - z3, 2))
            distance4 = math.sqrt(math.pow(x - x4, 2) + math.pow(y - y4, 2) + math.pow(z - z4, 2))
            if distance0 <= r0 :    sphere0[x,y,z] = 1
            if distance1 <= r1 :    sphere1[x,y,z] = 2
            if distance2 <= r2 :    sphere2[x,y,z] = 3
            if distance3 <= r3 :    sphere3[x,y,z] = 4
            if distance4 <= r4 :    sphere4[x,y,z] = 5

viewer = neuroglancer.Viewer()
dimensions = neuroglancer.CoordinateSpace(
    names=['x', 'y', 'z'],
    units='nm',
    scales=[10, 10, 10]
)
with viewer.txn() as s:
    s.dimensions = dimensions
    s.layers.append(
        name='a',
        layer=neuroglancer.LocalVolume(
            data=a,
            dimensions=neuroglancer.CoordinateSpace(
                names=['x', 'y', 'z'],
                units=['nm', 'nm', 'nm'],
                scales=[10, 10, 10]),
            voxel_offset=(20, 30, 15),
        ),
        shader="""
void main() {
  emitRGB(vec3(toNormalized(getDataValue(0)),
               toNormalized(getDataValue(1)),
               toNormalized(getDataValue(2))));
}
""")
    s.layers.append(
        name = 'First sphere (Q1) overlay',
        layer = neuroglancer.LocalVolume(
            data = sphere0,
            dimensions = dimensions,
        ),
        shader="""
        void main() {
          emitRGB(vec3(toNormalized(getDataValue(0)),
                       toNormalized(getDataValue(1)),
                       toNormalized(getDataValue(2))));
        }
        """)


    s.layers.append(
        name = "Second sphere (200, 500, 25) Overlay",
        layer = neuroglancer.LocalVolume(
            data=sphere1,
            dimensions = dimensions,
        ),
        shader="""
        void main() {
          emitRGB(vec3(toNormalized(getDataValue(0)),
                       toNormalized(getDataValue(1)),
                       toNormalized(getDataValue(2))));
        }
        """)
    s.layers.append(
        name="Third sphere (200, 500, 25) Overlay",
        layer=neuroglancer.LocalVolume(
            data=sphere2,
            dimensions=dimensions,
        ),
        shader="""
            void main() {
              emitRGB(vec3(toNormalized(getDataValue(0)),
                           toNormalized(getDataValue(1)),
                           toNormalized(getDataValue(2))));
            }
            """)

    s.layers.append(
        name="Fourth sphere (200, 500, 25) Overlay",
        layer=neuroglancer.LocalVolume(
            data=sphere3,
            dimensions=dimensions,
        ),
        shader="""
            void main() {
              emitRGB(vec3(toNormalized(getDataValue(0)),
                           toNormalized(getDataValue(1)),
                           toNormalized(getDataValue(2))));
            }
            """)

    s.layers.append(
        name="Fifth sphere (200, 500, 25) Overlay",
        layer=neuroglancer.LocalVolume(
            data=sphere4,
            dimensions=dimensions,
        ),
        shader="""
            void main() {
              emitRGB(vec3(toNormalized(getDataValue(0)),
                           toNormalized(getDataValue(1)),
                           toNormalized(getDataValue(2))));
            }
            """)





def acquire_mouse_action(s):
    print('Getting some mouse action')
    print('  Mouse position: %s' % (s.mouse_voxel_coordinates,))
    coordinates = s.mouse_voxel_coordinates
    with viewer.config_state.txn() as s:
        s.status_messages['Welcome to this example'] = 'You pressed key t'
        s.status_messages['You pressed key t'] = 'The mouse position is'
        s.status_messages['The mouse position is'] = coordinates

viewer.actions.add('mouse-action', acquire_mouse_action)
with viewer.config_state.txn() as s:
    s.input_event_bindings.viewer['keyt'] = 'mouse-action'
    s.status_messages['hello'] = 'Welcome to this example'

def acquire_layer_action(s):
    print('Getting selected layer action')
    print(' Layer selected values: %s' % (s.selected_values,))
    coordinates = s.selected_values
    with viewer.config_state.txn() as s:
        s.status_messages['Welcome to this example'] = 'You pressed key m'
        s.status_messages['You pressed key m'] = 'The selected layer info is'
        s.status_messages['The selected layer info is'] = coordinates

viewer.actions.add('layer-action', acquire_layer_action)
with viewer.config_state.txn() as s:
    s.input_event_bindings.viewer['keym'] = 'layer-action'
    s.status_messages['hello'] = 'Welcome to this example'


print(viewer)


