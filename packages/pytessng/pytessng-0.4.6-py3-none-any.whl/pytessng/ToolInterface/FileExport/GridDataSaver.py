import json
from collections import defaultdict
from shapely.geometry import Polygon, box
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class GridDataSaver:
    def __init__(self, netiface):  # netiface参数是为了与其他类保存统一，实际不需要
        self.length: float = -1
        self.zone_data: dict = dict()

    # 导出数据
    def export(self, length: float, data: dict, file_path: str):
        # 填充数据
        self.length = length
        self.zone_data = data

        # 更新画布大小
        self._update_size()

        # 获取网格
        grid_data = self._get_location_mapping()

        # 保存数据
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(grid_data, file, indent=4, ensure_ascii=False)

    # 更新画布大小
    def _update_size(self):
        xs, ys = [], []
        for interName, value in pgd.progress(self.zone_data.items(), "(1/3)"):
            for size in ["small", "big"]:
                if value[size]:
                    for x, y in value[size]:
                        xs.append(x)
                        ys.append(y)

        left = min(xs) - 10
        right = max(xs) + 10
        bottom = min(ys) - 10
        top = max(ys) + 10

        n_left = self._get_location_number(left)
        n_right = self._get_location_number(right)
        n_bottom = self._get_location_number(bottom)
        n_top = self._get_location_number(top)

        self.cells = []
        for x in range(n_left, n_right):
            for y in range(n_bottom, n_top):
                self.cells.append([x, y])

    # 找序号
    def _get_location_number(self, x):
        return int(x // self.length)

    # 转换成映射字典
    def _get_location_mapping(self,):
        boxs = {}
        for interName, value in pgd.progress(self.zone_data.items(), "(2/3)"):
            for size in ["small", "big"]:
                if value[size]:
                    name = (interName, size)
                    boxs[name] = Polygon(value[size])
        location_mapping = defaultdict(list)  # dict
        for name, polygon in pgd.progress(boxs.items(), "(3/3)"):
            overlapping_cells = self._overlapping_grid_cells(polygon)
            for cell in overlapping_cells:
                location_mapping[str(cell)].append(name)
        return dict(location_mapping)

    # 找重合的格子
    def _overlapping_grid_cells(self, polygon):
        overlapping_cells = []
        for x, y in self.cells:
            cell_box = box(x * self.length, y * self.length, (x+1) * self.length, (y+1) * self.length)
            intersection_area = polygon.intersection(cell_box).area
            if intersection_area > 0:
                overlapping_cells.append((x, y))
        return overlapping_cells
