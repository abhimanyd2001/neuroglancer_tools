from __future__ import print_function
import tifffile
import argparse
import numpy as np

import neuroglancer

from numpy import genfromtxt
my_data = genfromtxt('data.csv', delimiter=',')

numofData = my_data.size/3

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


