try:
    from PyQt5.QtDataVisualization import *
except ImportError:
    try:
        from PySide2.QtDataVisualization import QtDataVisualization
        Q3DScene = QtDataVisualization.Q3DScene
        QSurfaceDataItem = QtDataVisualization.QSurfaceDataItem
        QAbstractDataProxy = QtDataVisualization.QAbstractDataProxy
        QScatterDataItem = QtDataVisualization.QScatterDataItem
        QBarDataProxy = QtDataVisualization.QBarDataProxy
        QBarDataItem = QtDataVisualization.QBarDataItem
        QItemModelBarDataProxy = QtDataVisualization.QItemModelBarDataProxy
        QScatterDataProxy = QtDataVisualization.QScatterDataProxy
        QItemModelScatterDataProxy = QtDataVisualization.QItemModelScatterDataProxy
        Q3DTheme = QtDataVisualization.Q3DTheme
        Q3DObject = QtDataVisualization.Q3DObject
        QAbstract3DSeries = QtDataVisualization.QAbstract3DSeries
        Q3DCamera = QtDataVisualization.Q3DCamera
        QBar3DSeries = QtDataVisualization.QBar3DSeries
        QAbstract3DGraph = QtDataVisualization.QAbstract3DGraph
        Q3DLight = QtDataVisualization.Q3DLight
        QScatter3DSeries = QtDataVisualization.QScatter3DSeries
        Q3DBars = QtDataVisualization.Q3DBars
        QSurface3DSeries = QtDataVisualization.QSurface3DSeries
        Q3DScatter = QtDataVisualization.Q3DScatter
        Q3DSurface = QtDataVisualization.Q3DSurface
        QAbstract3DInputHandler = QtDataVisualization.QAbstract3DInputHandler
        QCustom3DItem = QtDataVisualization.QCustom3DItem
        Q3DInputHandler = QtDataVisualization.Q3DInputHandler
        QCustom3DLabel = QtDataVisualization.QCustom3DLabel
        QTouch3DInputHandler = QtDataVisualization.QTouch3DInputHandler
        QCustom3DVolume = QtDataVisualization.QCustom3DVolume
        QAbstract3DAxis = QtDataVisualization.QAbstract3DAxis
        QValue3DAxis = QtDataVisualization.QValue3DAxis
        QCategory3DAxis = QtDataVisualization.QCategory3DAxis
        QValue3DAxisFormatter = QtDataVisualization.QValue3DAxisFormatter
        QLogValue3DAxisFormatter = QtDataVisualization.QLogValue3DAxisFormatter
        QSurfaceDataProxy = QtDataVisualization.QSurfaceDataProxy
        QHeightMapSurfaceDataProxy = QtDataVisualization.QHeightMapSurfaceDataProxy
        QItemModelSurfaceDataProxy = QtDataVisualization.QItemModelSurfaceDataProxy
    except ImportError:
        raise ImportError("Neither PyQt5 nor PySide2 are installed, please install on of them")
