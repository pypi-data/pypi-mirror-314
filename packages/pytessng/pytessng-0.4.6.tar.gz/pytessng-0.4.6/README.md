This is the tessng with python development package.

##简介

微观交通仿真软件TESS NG路网编辑Python工具包“**pytessng**”主要包括两大功能：**外部数据源导入创建路网**和**多格式路网数据导出**。我们希望通过“pytessng”的推出，为微观交通仿真领域的从业者提供更加便捷、高效的路网编辑工具。

###外部数据数据源导入创建路网

pytessng 专注于提供强大的外部数据源导入创建路网的功能，支持包括 **OpenDrive、Shapefile、OpenStreetMap、Excel** 等多种数据格式，用户可以直接将精准的真实世界的地理交通信息无缝集成到仿真环境中，从而降低路网建模成本，提升路网建模精度。

###多格式路网数据导出

为了满足用户对仿真路网灵活处理的需求，pytessng 提供了多格式路网数据导出的功能，包括 **OpenDrive、Shapefile、GeoJson、Json** 等，用户可以根据实际需要选择合适的格式，方便在其他平台或工具中进行分析处理和可视化。

##使用方法

	from pytessng import TessngObject
	TessngObject(True)

启动代码后，将弹出软件激活弹窗，点击导入激活码，可以选择提供的试用版 key ，点击提交，再次启动代码，即可正常运行。启动代码后，会在启动代码同级目录下生成 WorkSpace 文件夹，其中包含 Cert、SimuResult 等子文件夹。

若是使用试用版 key 且其已到期，将弹出权限提示弹窗显示“没有权限加载插件”，**但只要点击 OK 即可**，只有打断路段和轨迹数据导出功能不可用，其余功能均可正常使用。
