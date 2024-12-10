import datetime
import collections
import xml.dom.minidom


class Doc:
    def __init__(self):
        # 只会记录路段，不会记录连接段
        self.link_node_mapping = collections.defaultdict(lambda: {'node': None, 'lanes_node': {}, })
        self.connector_node_mapping = collections.defaultdict(lambda: {'node': None, 'lanes_node': {}, })
        self.doc = xml.dom.minidom.Document()
        self.junction_node_mapping = {}

    def floatToStr(self, number):
        return str(round(number, 5))

    def init_doc(self, proj_string=None):
        # 创建一个根节点Managers对象
        root = self.doc.createElement('OpenDRIVE')
        self.doc.appendChild(root)

        # 创建头节点
        header = self.doc.createElement('header')
        root.appendChild(header)
        header.setAttribute('name', '')
        header.setAttribute('date', str(datetime.datetime.now()))
        if proj_string:
            header.setAttribute('proj_string', proj_string)
            # header.setAttribute('proj', "+proj=tmerc +lat_0=0 +lon_0=114 +k=1 +x_0=500000 +y_0=0 +ellps=GRS80 +units=m +no_defs")

        geoReference = self.doc.createElement('geoReference')
        header.appendChild(geoReference)

        userData = self.doc.createElement('userData')
        header.appendChild(userData)

    def add_junction(self, junctions):
        root = self.doc.getElementsByTagName('OpenDRIVE')[0]
        # 所有的连接都是通过junction(tessng的面域)完成的，所以只需要在此处记录连接关系
        self.predecessor_successor_info = collections.defaultdict(lambda : {"predecessor": None, "successor": None})

        for junction in junctions:
            junction_node = self.doc.createElement('junction')
            root.appendChild(junction_node)
            junction_node.setAttribute('id', str(junction.id))
            self.junction_node_mapping[junction.tess_id] = junction_node

            for connector in junction.ConnectorArea.allConnector():
                for laneConnector in connector.laneConnectors():
                    # 每一个车道连接都隐藏了三对关系
                    # 上游路段的下游关系
                    self.predecessor_successor_info[str(laneConnector.fromLane().link().id())]['successor'] = junction.id
                    # 下游路段的上游关系
                    self.predecessor_successor_info[str(laneConnector.toLane().link().id())]['predecessor'] = junction.id
                    # 当前车道连接(Road)的上下游关系
                    self.predecessor_successor_info[f"{laneConnector.fromLane().id()}_{laneConnector.toLane().id()}"]["predecessor"] = str(laneConnector.fromLane().link().id())
                    self.predecessor_successor_info[f"{laneConnector.fromLane().id()}_{laneConnector.toLane().id()}"]["successor"] = str(laneConnector.toLane().link().id())

    def add_road(self, roads):
        root = self.doc.getElementsByTagName('OpenDRIVE')[0]
        for road in roads:
            road_node = self.doc.createElement('road')
            root.appendChild(road_node)

            # 添加 link 映射
            if road.type == 'link':
                self.link_node_mapping[road.tess_id]['node'] = road_node

            road_node.setAttribute('name', f"Road_{road.tess_id}")
            road_node.setAttribute('id', str(road.id))
            road_node.setAttribute('length', str(road.length))
            road_node.setAttribute('junction', str(-1))  # 默认-1，如果隶属junction，下方会更新

            # link
            link_node = self.doc.createElement('link')
            road_node.appendChild(link_node)
            elementType = 'junction' if road.type == 'link' else 'road'
            if self.predecessor_successor_info[road.tess_id]['predecessor']:
                # 如果上游信息存在，填充
                predecessor_node = self.doc.createElement('predecessor')
                predecessor_node.setAttribute('elementType', elementType)
                predecessor_node.setAttribute('elementId', self.predecessor_successor_info[road.tess_id]['predecessor'])
                predecessor_node.setAttribute('contactPoint', 'end')
                link_node.appendChild(predecessor_node)
            # elementType = 'junction' if road.type == 'link' else 'road'
            if self.predecessor_successor_info[road.tess_id]['successor']:
                # 如果下游信息存在，填充
                successor_node = self.doc.createElement('successor')
                successor_node.setAttribute('elementType', elementType)
                successor_node.setAttribute('elementId', self.predecessor_successor_info[road.tess_id]['successor'])
                successor_node.setAttribute('contactPoint', 'start')
                link_node.appendChild(successor_node)

            # 高程
            elevationProfile_node = self.doc.createElement('elevationProfile')
            road_node.appendChild(elevationProfile_node)

            for elevation in road.elevations:
                elevation_node = self.doc.createElement('elevation')
                elevationProfile_node.appendChild(elevation_node)

                elevation_node.setAttribute('s', self.floatToStr(elevation.s))
                elevation_node.setAttribute('a', self.floatToStr(elevation.a))
                elevation_node.setAttribute('b', self.floatToStr(elevation.b))
                elevation_node.setAttribute('c', self.floatToStr(elevation.c))
                elevation_node.setAttribute('d', self.floatToStr(elevation.d))

            # 超高程
            lateralProfile_node = self.doc.createElement('lateralProfile')
            road_node.appendChild(lateralProfile_node)

            # 参考线
            planView_node = self.doc.createElement('planView')
            road_node.appendChild(planView_node)

            # ==============================================================
            for geometry in road.geometrys:
                geometry_node = self.doc.createElement('geometry')
                planView_node.appendChild(geometry_node)

                # 添加参考线
                geometry_node.setAttribute('s', self.floatToStr(geometry.s))
                geometry_node.setAttribute('x', self.floatToStr(geometry.x))
                geometry_node.setAttribute('y', self.floatToStr(geometry.y))
                geometry_node.setAttribute('hdg', self.floatToStr(geometry.hdg))
                geometry_node.setAttribute('length', self.floatToStr(geometry.length))

                # 添加线条
                if geometry.lineType == 'line':
                    line_node = self.doc.createElement('line')
                elif geometry.lineType == 'paramPoly3':
                    line_node = self.doc.createElement('paramPoly3')
                    line_node.setAttribute('aU', self.floatToStr(0))
                    line_node.setAttribute('bU', self.floatToStr(geometry.bU))
                    line_node.setAttribute('cU', self.floatToStr(geometry.cU))
                    line_node.setAttribute('dU', self.floatToStr(geometry.dU))
                    line_node.setAttribute('aV', self.floatToStr(0))
                    line_node.setAttribute('bV', self.floatToStr(geometry.bV))
                    line_node.setAttribute('cV', self.floatToStr(geometry.cV))
                    line_node.setAttribute('dV', self.floatToStr(geometry.dV))
                    # line_node.setAttribute('aU', self.floatToStr(geometry.aU))
                    # line_node.setAttribute('aV', self.floatToStr(geometry.aV))
                    # line_node.setAttribute('bV', self.floatToStr(geometry.bV))
                    line_node.setAttribute('pRange', "normalized")
                else:
                    print(f"存在不合理的线型: {geometry}")
                    continue
                geometry_node.appendChild(line_node)

            #
            #
            # if road.type == "connector":
            #     geometry_node = self.doc.createElement('geometry')
            #     planView_node.appendChild(geometry_node)
            #
            #     geometry = road.geometrys[0]
            #
            #     # 添加参考线
            #     import numpy as np
            #     hdg = np.arctan(geometry["bV"]/geometry["bU"])
            #     geometry_node.setAttribute('s', self.floatToStr(0))
            #     geometry_node.setAttribute('x', self.floatToStr(geometry["aU"]))
            #     geometry_node.setAttribute('y', self.floatToStr(geometry["aV"]))
            #     geometry_node.setAttribute('hdg', self.floatToStr(hdg))
            #     geometry_node.setAttribute('length', self.floatToStr(geometry["length"]))
            #
            #     # 添加线条
            #     line_node = self.doc.createElement('paramPoly3')
            #     geometry_node.appendChild(line_node)
            #
            #     line_node.setAttribute('aU', self.floatToStr(0))
            #     line_node.setAttribute('bU', self.floatToStr(geometry["bU"]))
            #     line_node.setAttribute('cU', self.floatToStr(geometry["cU"]))
            #     line_node.setAttribute('dU', self.floatToStr(geometry["dU"]))
            #     line_node.setAttribute('aV', self.floatToStr(0))
            #     line_node.setAttribute('bV', self.floatToStr(0))
            #     line_node.setAttribute('cV', self.floatToStr(geometry["cV"]))
            #     line_node.setAttribute('dV', self.floatToStr(geometry["dV"]))
            #     line_node.setAttribute('pRange', "normalized")
            #     print("success")
            #     # ==============================================================
            # else:
            #     for geometry in road.geometrys:
            #         geometry_node = self.doc.createElement('geometry')
            #         planView_node.appendChild(geometry_node)
            #
            #         # 添加参考线
            #         geometry_node.setAttribute('s', self.floatToStr(geometry.s))
            #         geometry_node.setAttribute('x', self.floatToStr(geometry.x))
            #         geometry_node.setAttribute('y', self.floatToStr(geometry.y))
            #         geometry_node.setAttribute('hdg', self.floatToStr(geometry.hdg))
            #         geometry_node.setAttribute('length', self.floatToStr(geometry.length))
            #
            #         # 添加线条
            #         line_node = self.doc.createElement('line')
            #         geometry_node.appendChild(line_node)

            # 车道信息
            lanes_node = self.doc.createElement('lanes')
            road_node.appendChild(lanes_node)
            # 中心车道偏移
            for lane_offset in road.lane_offsets:
                laneOffset_node = self.doc.createElement('laneOffset')
                lanes_node.appendChild(laneOffset_node)

                laneOffset_node.setAttribute('s', self.floatToStr(lane_offset.s))
                laneOffset_node.setAttribute('a', self.floatToStr(lane_offset.a))
                laneOffset_node.setAttribute('b', self.floatToStr(lane_offset.b))
                laneOffset_node.setAttribute('c', self.floatToStr(lane_offset.c))
                laneOffset_node.setAttribute('d', self.floatToStr(lane_offset.d))

            laneSection_node = self.doc.createElement('laneSection')
            lanes_node.appendChild(laneSection_node)

            laneSection_node.setAttribute('s', "0")

            # 添加中心车道,左侧车道，右侧车道
            center_node = self.doc.createElement('center')
            right_node = self.doc.createElement('right')
            left_node = self.doc.createElement('left')
            laneSection_node.appendChild(center_node)
            laneSection_node.appendChild(right_node)
            laneSection_node.appendChild(left_node)

            # 计算并添加所有的车道
            all_lane_node = []
            for lane in road.lanes:
                lane_node = self.doc.createElement('lane')
                eval(f'{lane["direction"]}_node').appendChild(lane_node)
                all_lane_node.append(lane_node)  # 从右向左排序

                # 添加车道信息到映射表
                if road.type == 'link' and lane['lane']:
                    self.link_node_mapping[road.tess_id]['lanes_node'][lane['lane'].number()] = lane_node

                lane_node.setAttribute('id', str(lane['id']))
                lane_node.setAttribute('level', "false")
                lane_node.setAttribute('type', lane['type'])

                link_node = self.doc.createElement('link')
                lane_node.appendChild(link_node)

                # 如果是connector，添加上下游连接关系
                if road.type == 'connector':
                    if "fromLaneId" in lane:
                        predecessor_node = self.doc.createElement('predecessor')
                        predecessor_node.setAttribute('id', str(lane['fromLaneId']))
                        link_node.appendChild(predecessor_node)

                    if 'toLaneId' in lane:
                        successor_node = self.doc.createElement('successor')
                        successor_node.setAttribute('id', str(lane['toLaneId']))
                        link_node.appendChild(successor_node)

                road_mark_node = self.doc.createElement('roadMark')
                lane_node.appendChild(road_mark_node)

                road_mark_node.setAttribute('sOffset', "0")

                # 添加车道宽度信息
                for width in lane['width']:
                    width_node = self.doc.createElement('width')
                    lane_node.appendChild(width_node)

                    width_node.setAttribute('sOffset', self.floatToStr(width.sOffset))
                    width_node.setAttribute('a', self.floatToStr(width.a))
                    width_node.setAttribute('b', self.floatToStr(width.b))
                    width_node.setAttribute('c', self.floatToStr(width.c))
                    width_node.setAttribute('d', self.floatToStr(width.d))

            # 此时所有的基础路段(link)已经建立完成,对于连接段需要同步填充lanelink信息
            if road.type == 'connector':
                # 获取前置/后续连接关系
                from_link = road.fromLink
                to_link = road.toLink
                from_road_node_info = self.link_node_mapping[str(from_link.id())]
                to_road_node_info = self.link_node_mapping[str(to_link.id())]

                junction_node = self.junction_node_mapping[road.junction.tess_id]
                from_road_node = from_road_node_info['node']
                to_road_node = to_road_node_info['node']
                # 添加 junction_id
                road_node.setAttribute('junction', junction_node.getAttribute('id'))

                # 建立来路/去路的连接关系，只需要为来路创建 connection
                for tmp_road_node in filter(None, [from_road_node, to_road_node]):
                    connection_node = self.doc.createElement('connection')
                    junction_node.appendChild(connection_node)
                    contactPoint = 'start' if tmp_road_node == from_road_node else 'end'

                    # 建立基础的 连接node(无连接关系)
                    connection_node.setAttribute('id', str(road.junction.connection_count))
                    road.junction.connection_count += 1
                    connection_node.setAttribute('incomingRoad', tmp_road_node.getAttribute('id'))
                    connection_node.setAttribute('connectingRoad', road_node.getAttribute('id'))
                    connection_node.setAttribute('contactPoint', contactPoint)

                    # 查询连接关系
                    laneConnector = road.laneConnector
                    # 寻找 来路/去路 node
                    incoming_road_node_info = from_road_node_info if contactPoint == 'start' else to_road_node_info
                    incoming_lane_number = laneConnector.fromLane().number() if contactPoint == 'start' else laneConnector.toLane().number()
                    incoming_lane_node = incoming_road_node_info['lanes_node'][incoming_lane_number]  # 来路/去路 node

                    # 连接段上只会有一个右侧的车道 + 中心车道
                    connector_lane_node = right_node.childNodes[0]

                    # 创建 laneLink
                    laneLink_node = self.doc.createElement('laneLink')
                    connection_node.appendChild(laneLink_node)
                    laneLink_node.setAttribute('from', incoming_lane_node.getAttribute('id'))
                    laneLink_node.setAttribute('to', connector_lane_node.getAttribute('id'))
