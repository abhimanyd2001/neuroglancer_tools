from __future__ import print_function
import tifffile
import argparse
import numpy as np

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

viewer = neuroglancer.Viewer()
dimensions = neuroglancer.CoordinateSpace(
    names=['x', 'y', 'z'],
    units='nm',
    scales=[10, 10, 10])
with viewer.txn() as s:
    s.dimensions = dimensions
    s.layers.append(
        name='Neuroglancer Image',
        layer=neuroglancer.LocalVolume(
            data=a,
            dimensions=neuroglancer.CoordinateSpace(
                names=['x', 'y', 'z'],
                units=['nm','nm','nm'],
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


print(viewer)
