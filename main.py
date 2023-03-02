import os
import pye57
import numpy as np
from PIL import Image
from os.path import join
from tqdm import tqdm
import optparse

parser = optparse.OptionParser()
parser.add_option('-i', '--input_path', action="store", help="Input path", default='./input', type="string")
parser.add_option('-o', '--output_path', action="store", help="Output path", default='./output', type="string")
options, arguments = parser.parse_args()


def convert_e57(file_path, output_path):
    file_name = os.path.basename(file_path)
    scanner = pye57.E57(file_path)
    data = scanner.read_scan_raw(0)
    header = scanner.get_header(0)

    rows = max(data['rowIndex'])
    cols = max(data['columnIndex'])

    depth_map = np.zeros((rows, cols), dtype=np.float32)
    intensity_map = np.zeros((rows, cols), dtype=np.float32)
    rgb_map = np.zeros((rows, cols, 3), dtype=np.uint8)

    for i in tqdm(range(len(data['rowIndex'])), desc=file_name):
        row_index, col_index = data['rowIndex'][i] - 1, data['columnIndex'][i] - 1
        intensity_map[row_index][col_index] = data['intensity'][i]
        rgb_map[row_index][col_index] = [data['colorRed'][i], data['colorGreen'][i], data['colorBlue'][i]]
        depth_map[row_index][col_index] = np.sqrt(
            data['cartesianX'][i] ** 2 +
            data['cartesianY'][i] ** 2 +
            data['cartesianZ'][i] ** 2
        )

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    depth_map = depth_map / np.max(depth_map) * 65535
    Image.fromarray(depth_map.astype(np.uint16)).save(join(output_path, file_name + '_depth.tiff'))
    intensity_canvas = intensity_map / np.max(intensity_map) * 65535
    Image.fromarray(intensity_canvas.astype(np.uint16)).save(join(output_path, file_name + '_intensity.tiff'))
    Image.fromarray(rgb_map.astype(np.uint8)).save(join(output_path, file_name + '_rgb.tiff'))

    with open(join(output_path, file_name + '.txt'), 'w') as f:
        f.write(f'# x y z m11 m12 m13 m21 m22 m23 m31 m32 m33\n')
        f.write(f'{header.translation[0]} {header.translation[1]} {header.translation[2]}')
        for i in range(3):
            for j in range(3):
                f.write(f' {header.rotation_matrix[i][j]}')
    print('\033[A\033[A')

def main():
    for file in tqdm(os.listdir(options.input_path), desc='Total'):
        if file.endswith('.e57'):
            convert_e57(join(options.input_path, file), options.output_path)
    print('\n\nDone!')


if __name__ == '__main__':
    main()
