import numpy as np
from skimage.feature import canny
from skimage.draw import set_color
from vision.image_functions import threshold
from vision.segmentation.segment import crop_by_saliency, saliency_dragonfly
from vision.tests import get_test_image
from vision.measurements import subspace_shape, procrustes
from skimage.measure import find_contours
import csv
import cv2
import matplotlib.pyplot as plt
from skimage import draw


def read_shape(index):
    path = '/home/james/vision/vision/tests/test_data/wing_area/cropped/{}.csv'.format(index)

    vertices = []
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        for row in reader:
            if len(row) == 2:
                vertices.append(row[:2])
    return np.array(vertices, dtype=np.float)


shapes = [read_shape(i) for i in range(4)]
aligned_shapes = procrustes.generalized_procrustes(shapes)

shape_model = subspace_shape.learn(aligned_shapes, K=5)

mu, phi, sigma2 = shape_model

# for d in range(5):
#     for h_v in np.linspace(-2, 2, 10):
#         h = np.zeros((5, 1))
#         h[d] = h_v
#         s = mu + phi @ h
#         s = s.reshape(-1, 2)
#         plt.plot(s[:, 0], s[:, 1])
#     plt.show()

wings_image = get_test_image('wing_area', 'cropped', '0.png')
cv2.imwrite('wings.png', wings_image)
edges = canny(wings_image[:, :, 1], 2.5)
cv2.imwrite('wing_edge.png', 255 * edges)

inference = subspace_shape.infer(edges, *shape_model)
for iteration in range(200):
    fitted_shape = next(inference)

output_image = np.copy(wings_image)
points = fitted_shape[:, [1, 0]]
perimeter = draw.polygon_perimeter(points[:, 0], points[:, 1])
draw.set_color(output_image, (perimeter[0].astype(np.int), perimeter[1].astype(np.int)), [0, 0, 255])
cv2.imwrite('wings_template.png', output_image)
