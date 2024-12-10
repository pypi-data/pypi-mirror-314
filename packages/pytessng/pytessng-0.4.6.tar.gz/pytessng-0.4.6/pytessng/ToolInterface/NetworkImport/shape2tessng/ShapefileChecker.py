import os
import shapefile


# 核查shape文件的坐标类型
class ShapefileChecker:
    @staticmethod
    def check_data(folder_path: str, lane_file_name: str, is_use_lon_and_lat: bool) -> (bool, str):
        # 文件路径
        filePath_shp_lane = os.path.join(folder_path, f"{lane_file_name}.shp")

        # 读取文件
        try:
            all_data_shp_lane = shapefile.Reader(filePath_shp_lane, encoding='utf-8').shapes()
        except:
            all_data_shp_lane = shapefile.Reader(filePath_shp_lane, encoding='gbk').shapes()

        # 坐标范围
        x_list, y_list = [], []
        for lane_data_shp in all_data_shp_lane:
            x_list.extend([point[0] for point in lane_data_shp.points])
            y_list.extend([point[1] for point in lane_data_shp.points])

        x_diff = max(x_list) - min(x_list)
        y_diff = max(y_list) - min(y_list)

        # 经纬度坐标
        if is_use_lon_and_lat:
            # 一定不是
            if min(x_list) < -180 or max(x_list) > 180 or min(y_list) < -90 or max(y_list) > 90:
                is_ok = False
                prompt_information = "判断为笛卡尔坐标，请检查！"
            # 大概率不是
            elif x_diff > 2 or y_diff > 2:
                is_ok = False
                prompt_information = "极大概率为笛卡尔坐标，请检查！"
            # 大概率是
            else:
                is_ok = True
                prompt_information = ""
        # 笛卡尔坐标
        else:
            # 很可能不是
            if x_diff < 1 and y_diff < 1:
                is_ok = False
                prompt_information = "极大概率为经纬度坐标，请检查！"
            else:
                is_ok = True
                prompt_information = ""

        return is_ok, prompt_information
