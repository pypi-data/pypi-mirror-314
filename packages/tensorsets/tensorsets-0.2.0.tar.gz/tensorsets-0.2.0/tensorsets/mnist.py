from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import logging

import numpy as np
import tensorflow as tf

from tensorsets import common


_URLS = [
    'http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz',
    'http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz',
    'http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz',
    'http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz',
]

_HASHES = [
    'c3557c10f29b266e19b3eeee1553c85e0ef4a8ea',
    'adbf52269f5d842899f287c269e2883e40b4f6e2',
    '65e11ec1fd220343092a5070b58418b5c2644e26',
    'a6d52cc628797e845885543326e9f10abb8a6f89',
]


def mnist(directory, train_shape=(100, 28, 28), test_shape=(10000, 28, 28)):
  if len({np.prod(train_shape[1:]), np.prod(train_shape[1:]), 784}) != 1:
      raise ValueError('Cannot reshape 28 x 28 images to the provided shape.')
  directory = os.path.join(os.path.expanduser(directory), 'mnist')
  downloads = [common.download(directory, url) for url in _URLS]
  filenames = [common.extract(download) for download in downloads]
  for filename, hash_ in zip(filenames, _HASHES):
    common.verify_hash(filename, sha1=hash_)
  train_images, train_labels, test_images, test_labels = filenames
  train = _read_dataset(train_images, train_labels, train_shape[1:])
  train = train.cache().shuffle(100 * train_shape[0])
  train = train.batch(train_shape[0]).prefetch(1)
  test = _read_dataset(test_images, test_labels, test_shape[1:])
  test = test.cache().batch(test_shape[0]).prefetch(1)
  return common.AttrDict(train=train, test=test)


def _read_dataset(images_filename, labels_filename, shape):
  images = tf.data.FixedLengthRecordDataset(
      [images_filename], 28 * 28, header_bytes=16)
  labels = tf.data.FixedLengthRecordDataset(
      [labels_filename], 1, header_bytes=8)
  images = images.map(lambda x: tf.to_float(tf.decode_raw(x, tf.uint8)))
  images = images.map(lambda x: tf.reshape(x, shape) / 255.0)
  labels = labels.map(
      lambda x: tf.cast(tf.decode_raw(x, tf.uint8), tf.int32)[0])
  return tf.data.Dataset.zip((images, labels))


def test_mnist():
  logging.basicConfig(level=logging.INFO, format='%(message)s')
  dataset = mnist('~/dataset', (100, 28, 28), (100, 28, 28))
  train, test = dataset.train, dataset.test
  assert common.testing.count_batches(train) == 600
  assert common.testing.count_batches(test) == 100
  assert common.testing.compute_value_range(
      train.map(lambda image, label: image)) == (0, 1)
  assert common.testing.compute_value_range(
      train.map(lambda image, label: label)) == (0, 9)
  assert common.testing.compute_value_range(
      test.map(lambda image, label: image)) == (0, 1)
  assert common.testing.compute_value_range(
      test.map(lambda image, label: label)) == (0, 9)
  logging.info('Passed.')


if __name__ == '__main__':
  test_mnist()
