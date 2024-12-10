import json
import numpy as np

from pytessng.ToolInterface.NetworkExport.BaseTessng2Other import BaseTessng2Other
from .utils import create_curve, calc_boundary, xyz2xzy, chunk
from pytessng.Config import NetworkExportConfig
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class Tessng2Unity(BaseTessng2Other):
    def save_data(self, data: dict, file_path: str) -> None:
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

    def analyze_data(self, proj_string: str = None) -> dict:
        # 属性映射关系
        CONVERT_ATTRIBUTE = NetworkExportConfig.Unity.CONVERT_ATTRIBUTE
        # 线宽
        BORDER_LINE_WIDTH = NetworkExportConfig.Unity.BORDER_LINE_WIDTH

        # ==================== 获取三角形数据 ====================
        polygon_data = {
            "black": [],
            "white": [],
            "yellow": []
        }

        # 绘制路面(黑色)
        for link in pgd.progress(self.netiface.links(), "路段数据读取中（1/5）"):
            left_points = self._qtpoint2list(link.leftBreakPoint3Ds())
            right_points = self._qtpoint2list(link.rightBreakPoint3Ds())
            polygon_data["black"] += create_curve(left_points, right_points)
        for connector in pgd.progress(self.netiface.connectors(), "连接段数据读取中（2/5）"):
            for laneConnector in connector.laneConnectors():
                left_points = self._qtpoint2list(laneConnector.leftBreakPoint3Ds())
                right_points = self._qtpoint2list(laneConnector.rightBreakPoint3Ds())
                # 防止 nan 情况发生(长度为0的情况)
                left_points = [_ for _ in left_points if not np.isnan(_[2])]
                polygon_data["black"] += create_curve(left_points, right_points)

        # 绘制左右边界线(黄色实线，白色实线，白色虚线)
        for link in pgd.progress(self.netiface.links(), "左右边界线计算中（3/5）"):
            lanes = link.lanes()
            for index, lane in enumerate(lanes):
                if index == 0:
                    # 最右侧车道绘制右侧边界(白色实线)
                    base_points = self._qtpoint2list(link.rightBreakPoint3Ds())
                    left_points, right_points = calc_boundary(base_points, BORDER_LINE_WIDTH)
                    polygon_data['white'] += create_curve(left_points, right_points)
                # 所有车道绘制左侧边界
                if index == len(lanes) - 1:
                    # 最左侧车道绘制黄色实线
                    base_points = self._qtpoint2list(link.leftBreakPoint3Ds())
                    left_points, right_points = calc_boundary(base_points, BORDER_LINE_WIDTH)
                    polygon_data['yellow'] += create_curve(left_points, right_points)
                elif lane.actionType() != lanes[index + 1].actionType():
                    # 左侧相邻车道类型不一致，绘制白色实线
                    base_points = self._qtpoint2list(link.leftBreakPoint3Ds())
                    left_points, right_points = calc_boundary(base_points, BORDER_LINE_WIDTH)
                    polygon_data['white'] += create_curve(left_points, right_points)
                else:
                    # 左侧相邻车道类型一致，绘制白色虚线
                    base_points = self._qtpoint2list(link.leftBreakPoint3Ds())
                    left_points, right_points = calc_boundary(base_points, BORDER_LINE_WIDTH)
                    polygon_data['white'] += create_curve(left_points, right_points, split=True)

        # ==================== 存储最终的unity三角形信息 ====================
        triangle_data = {
            CONVERT_ATTRIBUTE[color]: [
                xyz2xzy(point)
                for triangle in triangles
                for point in triangle
            ]
            for color, triangles in pgd.progress(polygon_data.items(), "三角形计算中（4/5）")
        }

        # 转换为 unity数据
        unity_data = {
            'unity': {},
            'count': {},
        }
        for attribute, value in pgd.progress(triangle_data.items(), "三角形计算中（5/5）"):
            # unity 单次接收的三角形数量有限制，不能超过 256 * 256 个
            unity_data["unity"][attribute] = [
                {
                    'pointsArray': info,
                    'drawOrder': [i for i in range(len(info))],
                    'count': int(len(info))
                }
                for info in chunk(value, 60000)
            ]
            unity_data["count"][attribute] = len(unity_data["unity"][attribute])

        return unity_data
