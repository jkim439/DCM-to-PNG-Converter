__author__ = 'Junghwan Kim'
__copyright__ = 'Copyright 2016-2019 Junghwan Kim. All Rights Reserved.'
__version__ = '1.0.0'

import numpy as np
import os
import pydicom
import scipy.misc


def main():

    # Set input path
    path = '/home/jkim/nas/members/sko/SHARE/2019/0118/SET1/1785964_20190113'

    # Set output path
    path_result = '/home/jkim/nas/members/sko/SHARE/2019/0118/SET1/1785964_20190113/png'

    # Set variables
    result = 0

    # New folder
    if not os.path.exists(path_result):
        os.makedirs(path_result)

    # Recur load input directories
    for paths, dirs, files in sorted(os.walk(path)):
        for name in sorted(files):
            ds = pydicom.dcmread(os.path.join(paths, name))
            ds_array = ds.pixel_array
            intercept = ds.RescaleIntercept
            slope = ds.RescaleSlope
            ds_array = ds_array * slope + intercept
            ds_array = GetLUTValue(ds_array, 100, 50)
            AdjImage = scipy.misc.toimage(ds_array)
            AdjImage.save(os.path.join(path_result + '/' + name[:-4] + '.png'))
            print '[SUCCESS]', path_result + '/' + name[:-4] + '.png'

            # Complete every process
        result += 1

    # Print result
    print '\n----------------------------------------------------------------------------------------------------' \
          '\nResult' \
          '\n----------------------------------------------------------------------------------------------------' \
          '\n', result, 'Folders are processed successfully.'

    return None


def GetLUTValue(data, window, level):
    """Apply the RGB Look-Up Table for the given data and window/level value."""

    lutvalue = np.piecewise(data,
                            [data <= (level - 0.5 - (window - 1) / 2),
                             data > (level - 0.5 + (window - 1) / 2)],
                            [0, 255, lambda data: ((data - (level - 0.5)) / (window - 1) + 0.5) * (255 - 0)])
    # Convert the resultant array to an unsigned 8-bit array to create
    # an 8-bit grayscale LUT since the range is only from 0 to 255
    return np.array(lutvalue, dtype=np.uint8)


if __name__ == '__main__':
    main()
