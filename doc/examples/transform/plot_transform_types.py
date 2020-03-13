"""
===================================
Types of homographies
===================================

`Homographies <https://en.wikipedia.org/wiki/Homography>`_
are transformations of a Euclidean space that preserve the alignment of points. 
Specific cases of homographies correspond to the conservation of more properties,
such as parallelism (affine transformation), shape (similar transformation) or distances (Euclidean transformation). 

Homographies on a 2D Euclidean space (i.e., for 2D grayscale or multichannel images) are defined by a 3x3 matrix. 
All types of homographies can be defined either by passing the transformation matrix, or by passing the parameters
of simpler transformations (rotation, scaling...) into which some transformations can be decomposed.

The different types of homographies available in scikit-image are
shown here, by increasing order of complexity. While we focus here on the
mathematical properties of transformations, tutorial :ref:`sphx_glr_auto_examples_transform_plot_geometric.py`
explains how to use such transformations for various tasks such as image warping or parameter estimation.
"""
import math
import numpy as np
import matplotlib.pyplot as plt

from skimage import data
from skimage import transform as tf
from skimage import img_as_float

######################################################################
# Euclidean (rigid) transformation
# =================================
#
# A `Euclidean transformation <https://en.wikipedia.org/wiki/Rigid_transformation>`_,
# also called rigid transformation, preserves the Euclidean distance between pairs of
# points. It can be described as a rotation followed by a translation.

tform = tf.EuclideanTransform(
    rotation=np.pi / 12.,
    translation = (100, -20)
    )
print(tform.params)

######################################################################
# Now let's apply this transformation to an image. We use the inverse
# of ``tform``; indeed, ``tform`` is a transformation of *coordinates*,
# therefore we need to use its inverse to rotate and shift the image 
# with the given parameters.
#
# Note that the first dimension corresponds to the horizontal axis,
# positive from left to right, while the second dimension is the vertical
# axis, positive downwards. Also, the rotation is around the origin, that
# is the top-left corner of the image.

img = img_as_float(data.chelsea())
tf_img = tf.warp(img, tform.inverse)
_ = plt.imshow(tf_img)
plt.title('Euclidean transformation')


######################################################################
# For a rotation around the center of the image, one can either 
# compose a translation to change the origin, a rotation, and finally
# the inverse of the first translation, or use the utility function
# :func:`skimage.transform.rotation` (note that its parameter is given
# in degrees, while it is given in radians for the different kinds of
# affine transformations):

plt.figure()
rotated_img = tf.rotate(img, 45)
_ = plt.imshow(rotated_img)
plt.title('Rotation')

######################################################################
# Similarity transformation
# =================================
#
# A `similarity transformation <https://en.wikipedia.org/wiki/Similarity_(geometry)>`_
# preserves the shape of objects. It combines scaling, translation and rotation.

tform = tf.SimilarityTransform(
    scale=0.5,
    rotation=np.pi/12,
    translation=(100, 50))
print(tform.params)
tf_img = tf.warp(img, tform.inverse)
plt.figure()
_ = plt.imshow(tf_img)
plt.title('Similarity transformation')

######################################################################
# Affine transformation
# =================================
#
# An `affine transformation <https://en.wikipedia.org/wiki/Affine_transformation>`_
# preserves lines (hence the alignment of objects), as well as parallelism
# between lines. It can be decomposed into a similarity transform and a
# `shear transformation <https://en.wikipedia.org/wiki/Shear_mapping>`_.

#img = data.checkerboard()
tform = tf.AffineTransform(
        shear=np.pi/6,
        )
print(tform.params)
tf_img = tf.warp(img, tform.inverse)
plt.figure()
_ = plt.imshow(tf_img)
plt.title('Affine transformation')


######################################################################
# Projective transformation (homographies)
# ========================================
#
# A `homography <https://en.wikipedia.org/wiki/Homography>`_, also called
# projective transformation, preserves lines but not necessarily 
# parallelism.

matrix = np.array([[1, -0.5, 100],
                   [0.1, 0.9, 50],
                   [0.0015, 0.0015, 1]])
tform = tf.ProjectiveTransform(matrix=matrix)
tf_img = tf.warp(img, tform.inverse)
plt.figure()
_ = plt.imshow(tf_img)
plt.title('Projective transformation')

plt.show()

# sphinx_gallery_thumbnail_number = 5


######################################################################
# See also
# ========================================
#
# * :ref:`sphx_glr_auto_examples_transform_plot_geometric.py` for composing 
#   transformations or estimating their parameters
# * :ref:`sphx_glr_auto_examples_transform_plot_rescale.py` for simple 
#   rescaling and resizing operations
# * :func:`skimage.transform.rotate` for rotating an image around its center
