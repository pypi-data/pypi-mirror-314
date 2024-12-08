from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os

import numpy as np
import tensorflow as tf

from tensorsets import common


_URL = 'http://mattmahoney.net/dc/text8.zip'
_HASH = '3bea1919949baf155f99411df5fada7e'


def text8(directory, shape=(10, 100)):
  if int(0.05 * 1e8) % np.prod(shape):
    message = 'Batch shape must divide data set size of {}.'
    raise ValueError(message.format(int(0.05 * 1e8)))
  directory = os.path.join(os.path.expanduser(directory), 'text8')
  filename = common.download(directory, _URL)
  filename = common.extract(filename, files=('text8',))[0]
  common.verify_hash(filename, md5=_HASH)
  total_bytes = 1e8
  decode = lambda x: tf.reshape(tf.decode_raw(x, tf.uint8), shape[1:])
  convert = lambda x: tf.cast(x, tf.int32)
  train = tf.data.FixedLengthRecordDataset(
      [filename], np.prod(shape[1:]),
      footer_bytes=int(0.1 * total_bytes))
  eval = tf.data.FixedLengthRecordDataset(
      [filename], np.prod(shape[1:]),
      header_bytes=int(0.9 * total_bytes),
      footer_bytes=int(0.05 * total_bytes))
  test = tf.data.FixedLengthRecordDataset(
      [filename], np.prod(shape[1:]),
      header_bytes=int(0.95 * total_bytes))
  train = train.map(decode).cache().shuffle(100 * shape[0])
  train = train.batch(shape[0]).map(convert).prefetch(1)
  eval = eval.map(decode).cache()
  eval = eval.batch(shape[0]).map(convert).prefetch(1)
  test = test.map(decode).cache()
  test = test.batch(shape[0]).map(convert).prefetch(1)
  return common.AttrDict(train=train, eval=eval, test=test)


def test_text8():
  logging.basicConfig(level=logging.INFO, format='%(message)s')
  dataset = text8('~/dataset', (10, 100))
  train, eval, test = dataset.train, dataset.eval, dataset.test
  assert common.testing.count_batches(train) == int(0.9 * 1e8 / 10 / 100)
  assert common.testing.count_batches(eval) == int(0.05 * 1e8 / 10 / 100)
  assert common.testing.count_batches(test) == int(0.05 * 1e8 / 10 / 100)
  assert common.testing.compute_value_range(train) == (32, 122)
  assert common.testing.compute_value_range(eval) == (32, 122)
  assert common.testing.compute_value_range(test) == (32, 122)
  bytes_ = np.stack(common.testing.read_records(eval, 1)).flatten()
  assert ''.join(chr(byte) for byte in bytes_).startswith('e the capital of')
  bytes_ = np.stack(common.testing.read_records(test, 1)).flatten()
  assert ''.join(chr(byte) for byte in bytes_).startswith('be ejected and h')
  logging.info('Passed.')


if __name__ == '__main__':
  test_text8()
