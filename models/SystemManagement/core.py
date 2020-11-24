# /******************************************************************************************
# ************* STK make model usage:
# ************* version: print python3.6.3  version
# ************* make: make Python file
# ************* STK makemodel.py 1.0.0
# ************* @author Xujin
# ************* @date 2019-08-09 15:58:36
# ************* @Model 
# ******************************************************************************************/

# 引入必要的类库
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, Column, ForeignKey, Table, DateTime, Integer, String
from sqlalchemy import Column, DateTime, Float, Integer, String, Unicode, BigInteger
from sqlalchemy.dialects.mssql.base import BIT
from dbset.database.db_operate import GLOBAL_DATABASE_CONNECT_STRING
from datetime import datetime
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

# 引入mssql数据库引擎
import pymssql

# 创建对象的基类
engine = create_engine(GLOBAL_DATABASE_CONNECT_STRING, deprecate_large_types=True,
                       max_overflow=0,  # 超过连接池大小外最多创建的连接
                       pool_size=100,  # 连接池大小
                       pool_timeout=50,  # 池中没有线程最多等待的时间，否则报错
                       pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
                       # echo = True   #输出SQL
                       )
SessionFactory = sessionmaker(bind=engine)
session = SessionFactory()
Base = declarative_base(engine)

# Role_Menu_START:
# 菜单与角色关联表
Role_Menu = Table(
    "role_menu",
    Base.metadata,
    Column("Role_ID", Integer, ForeignKey("Role.ID"), nullable=False, primary_key=True),
    Column("Menu_ID", Integer, ForeignKey("Menu.ID"), nullable=False, primary_key=True)
)

# Role_Menu_END:


# DepartmentManager_START:
class DepartmentManager(Base):
    '''部门'''
    __tablename__ = "DepartmentManager"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 部门名称:
    DepartName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 部门编码:
    DepartCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 所属厂区:
    DepartLoad = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# DepartmentManager_END:

# MenuType_START:
class MenuType(Base):
    __tablename__ = "MenuType"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 类型名称:
    TypeName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 类型编码:
    TypeCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# MenuType_END:

# Role_START:
class Role(Base):
    '''角色'''
    __tablename__ = "Role"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 角色编码:
    RoleCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # RoleName:
    RoleName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # Description:
    Description = Column(Unicode(50), primary_key=False, autoincrement=False, nullable=True)

    # 所属部门:
    ParentNode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 查询权限
    menus = relationship("Menu", secondary=Role_Menu)


# Role_END:

# Menu_START:
# 模块菜单表
class Menu(Base):
    __tablename__ = 'Menu'
    # 模块ID
    ID = Column(Integer, primary_key=True, autoincrement=True)

    # 模块名称
    ModuleName = Column(Unicode(32), nullable=False)

    # 模块编码
    ModuleCode = Column(String(100),nullable=False)

    # 模块路由
    Url = Column(String(100), nullable=True)

    # 描述
    Description = Column(Unicode(1024), nullable=True)

    # 创建时间
    CreateDate = Column(DateTime, default=datetime.now, nullable=True)

    # 创建人
    Creator = Column(Unicode(50), nullable=True)

    # 父节点
    ParentNode = Column(Integer, nullable=True)

    # 查询角色
    roles = relationship("Role", secondary=Role_Menu)

# Menu_END:

# SpareStock_START:
class SpareStock(Base):
    __tablename__ = "SpareStock"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 备件编码:
    SpareCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 备件名称:
    SpareName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 备件状态:
    SpareStatus = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 备件型号:
    SpareModel = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 生产厂家:
    SpareFactory = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 备件类型:
    SpareType = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 备件功率:
    SparePower = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 描述:
    Description = Column(Unicode(120), primary_key=False, autoincrement=False, nullable=True)

    # 备件使用状况:
    StockUseStatus = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 生产日期:
    ProductionDate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 录入时间:
    CreateDate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 录入人:
    InStockPeople = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 审核人:
    CheckedPeople = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 审核时间:
    CheckedDate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 入库时间:
    InStockDate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# SpareStock_END:


# SpareTypeStore_START:
class SpareTypeStore(Base):
    __tablename__ = "SpareTypeStore"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 备件类型编码:
    SpareTypeCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 备件类型名称:
    SpareTypeName = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 父节点:
    ParentNode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# SpareTypeStore_END:


# EquipmentReportingRecord_START:
class EquipmentReportingRecord(Base):
    __tablename__ = "EquipmentReportingRecord"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 设备维修计划单号:
    FailureNumber = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 工序:
    PUIDName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 故障时间:
    FailureDate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 早晚班:
    Shift = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 设备名称:
    EQPName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 故障描述:
    FailureReportingDesc = Column(Unicode(120), primary_key=False, autoincrement=False, nullable=True)

    # 原因分析:
    AnalysisFailure = Column(Unicode(120), primary_key=False, autoincrement=False, nullable=True)

    # 解决措施:
    Precautions = Column(Unicode(100), primary_key=False, autoincrement=False, nullable=True)

    # 不影响生产:
    UnAffectingProduction = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 影响生产:
    AffectingProduction = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 维修人:
    Repairman = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 备件更换情况:
    ReplacementOfSpareParts = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# EquipmentReportingRecord_END:


# EquipmentMaintenanceStore_START:
class EquipmentMaintenanceStore(Base):
    __tablename__ = "EquipmentMaintenanceStore"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 设备型号:
    EquipmentType = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 设备名称:
    EquipentName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 设备编号:
    EquipmentNumber = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 操作内容:
    Content = Column(Unicode(120), primary_key=False, autoincrement=False, nullable=True)

    # 保养责任人:
    PersonLiable = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 督导人:
    SuperVisor = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 操作时间:
    OperationDate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# EquipmentMaintenanceStore_END:


# plantCalendarScheduling_START:
class plantCalendarScheduling(Base):
    '''日历'''
    __tablename__ = "plantCalendarScheduling"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 颜色:
    color = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 标题:
    title = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 时间:
    start = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 结束:
    end = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# plantCalendarScheduling_END:


# Enterprise_START:
class Enterprise(Base):
    __tablename__ = "Enterprise"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 上级企业:
    ParentNode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 企业类型:
    Type = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 描述:
    Desc = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 父节点名称:
    ParentNodeName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 企业代码:
    EnterpriseNo = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 企业名称:
    EnterpriseName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 企业编码:
    EnterpriseCode = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)


# Enterprise_END:


# Factory_START:
class Factory(Base):
    __tablename__ = "Factory"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 所属企业:
    EnterpriseName = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 厂名:
    FactoryName = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 所在地区:
    Region = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)


# Factory_END:


# Station_START:
class Station(Base):
    '''岗位'''
    __tablename__ = "Station"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 地址:
    Address = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 电话:
    Phone = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 岗位负责人:
    PersonCharge = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 岗位职责:
    Responsibility = Column(Unicode(100), primary_key=False, autoincrement=False, nullable=True)

    # 所属部门:
    DepartName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 岗位类型:
    StationType = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 岗位名称:
    StationName = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 岗位编码:
    StationCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# Station_END:

# DeviceList_START:
class DeviceList(Base):
    '''器件'''
    __tablename__ = "DeviceList"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 器件名称:
    DeviceName = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 器件编码:
    DeviceCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 器件类型:
    DeviceType = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 规格型号:
    SpecificationType = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 品牌:
    Brand = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 单位:
    Unit = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 备注:
    Description = Column(Unicode(100), primary_key=False, autoincrement=False, nullable=True)


# DeviceList_END:


# CollectionPoint_START:
class CollectionPoint(Base):
    __tablename__ = "CollectionPoint"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 采集点名称:
    CollectionPointName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 采集点编码:
    CollectionPointCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 采集位置:
    CollectionPosition = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 厂区:
    FactoryName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 车间:
    Workshop = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 位置描述:
    PositionDescription = Column(Unicode(100), primary_key=False, autoincrement=False, nullable=True)


# CollectionPoint_END:


# RedisKey_START:
class RedisKey(Base):
    __tablename__ = "RedisKey"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 对应的键值:
    KEY = Column(Unicode(52), primary_key=False, autoincrement=False, nullable=True)

    # 描述:
    Description = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)


# RedisKey_END:


# AreaMaintain_START:
class AreaMaintain(Base):
    '''厂区'''
    __tablename__ = "AreaMaintain"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 区域编码:
    AreaCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 区域名称:
    AreaName = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 所属厂区:
    FactoryName = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)


# AreaMaintain_END:


# LimitTable_START:
class LimitTable(Base):
    __tablename__ = "LimitTable"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 名称:
    LimitName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 编码:
    LimitCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 限值:
    LimitValue = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# LimitTable_END:


# Unit_START:
class Unit(Base):
    __tablename__ = "Unit"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 单位名称:
    UnitName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 单位值:
    UnitValue = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# Unit_END:


# BrandAreaTable_START:
class BrandAreaTable(Base):
    __tablename__ = "BrandAreaTable"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 区域:
    AreaName = Column(Unicode(52), primary_key=False, autoincrement=False, nullable=True)

    # 品名:
    BrandName = Column(Unicode(52), primary_key=False, autoincrement=False, nullable=True)


# BrandAreaTable_END:


# BatchMaintain_START:
class BatchMaintain(Base):
    '''
    计划表
    '''
    __tablename__ = "BatchMaintain"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 计划单号:
    PlanNum = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 批次号:
    BatchID = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 品名:
    BrandName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 计划重量:
    PlanQuantity = Column(Unicode(52), primary_key=False, autoincrement=False, nullable=True)

    # 水用量:
    WaterConsumption = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 汽用量:
    SteamConsumption = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 创建日期:
    CreateDate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 生产日期:
    ProductionDate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 开始时间:
    StartTime = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 结束时间:
    EndTime = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 生产车间:
    AreaName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# BatchMaintain_END:


# WorkShop_START:
class WorkShop(Base):
    '''车间'''
    __tablename__ = "WorkShop"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 车间名称:
    WorkShopName = Column(Unicode(52), primary_key=False, autoincrement=False, nullable=True)

    # 车间编码:
    WorkShopCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 所属厂区:
    FactoryName = Column(Unicode(52), primary_key=False, autoincrement=False, nullable=True)

    # 描述:
    Desc = Column(Unicode(100), primary_key=False, autoincrement=False, nullable=True)


# WorkShop_END:


# Equipment_START:
class Equipment(Base):
    __tablename__ = "Equipment"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 设备编码:
    EQPCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 设备名称:
    EQPName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 设备状态:
    Equipment_State = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 成本归属:
    CostAttach = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 基本参数:
    Equipment_Model = Column(Unicode(100), primary_key=False, autoincrement=False, nullable=True)

    # 采购日期:
    Procurement_Date = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 工艺段:
    PUID = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 备注说明:
    Desc = Column(Unicode(100), primary_key=False, autoincrement=False, nullable=True)

    # 操作时间:
    OperationDate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 区域:
    AreaName = Column(Unicode(52), primary_key=False, autoincrement=False, nullable=True)


# Equipment_END:


# Instrumentation_START:
class Instrumentation(Base):
    __tablename__ = "Instrumentation"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 仪表编码:
    InstrumentationCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 仪表名称:
    InstrumentationName = Column(Unicode(52), primary_key=False, autoincrement=False, nullable=True)

    # 检定周期:
    VerificationCycle = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 检定次数:
    NumberVerification = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 提醒时间:
    ReminderTime = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 状态:
    Status = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 录入时间:
    CreateTime = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 处理人:
    Handler = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 处理状态:
    HandleStatus = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 审核人:
    Reviewer = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 审核状态:
    ReviewStatus = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 更新时间:
    UpdateTime = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# Instrumentation_END:


# AreaTable_START:
class AreaTable(Base):
    __tablename__ = "AreaTable"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 区域名称:
    AreaName = Column(Unicode(52), primary_key=False, autoincrement=False, nullable=True)

    # 区域编码:
    AreaCode = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 所属车间:
    WorkShopName = Column(Unicode(52), primary_key=False, autoincrement=False, nullable=True)

    # 描述:
    Desc = Column(Unicode(100), primary_key=False, autoincrement=False, nullable=True)


# AreaTable_END:


# TagClassType_START:
class TagClassType(Base):
    __tablename__ = "TagClassType"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # Tag类型名称:
    TagClassName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # Tag对应值:
    TagClassValue = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 设备ID:
    EquipmnetID = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 设备名称:
    EQPName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 所属区域:
    AreaName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# TagClassType_END:


# TagDetail_START:
class TagDetail(Base):
    __tablename__ = "TagDetail"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 区域名称:
    AreaName = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 器件号:
    DeviceNum = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # IP地址:
    IP = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 端口:
    Port = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 虚拟分配COM号:
    COMNum = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 采集点名称:
    FEFportIP = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 位置:
    Area = Column(Unicode(65), primary_key=False, autoincrement=False, nullable=True)

    # 备注:
    Description = Column(Unicode(150), primary_key=False, autoincrement=False, nullable=True)

    # 水电汽分类:
    EnergyClass = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # Tag点:
    TagClassValue = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 厂商
    Type = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 用电设备
    Equipment = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 是否导出
    IsExport = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)
    # 电量约束
    ConstrainValue = Column(Unicode(32), nullable=True)


# TagDetail_END:


# ElectricEnergy_START:
class ElectricEnergy(Base):
    """电能"""
    __tablename__ = "ElectricEnergy"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 单位:
    Unit = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 仪表ID:
    EquipmnetID = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 价格ID:
    PriceID = Column(Float(53), primary_key=False, autoincrement=False, nullable=True)

    # 采集点:
    TagClassValue = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 采集时间:
    CollectionDate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 采集年:
    CollectionYear = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 采集月:
    CollectionMonth = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 采集天:
    CollectionDay = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 总功率:
    ZGL = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # A相电压:
    AU = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # A相电流:
    AI = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # B相电压:
    BU = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # B相电流:
    BI = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # C相电压:
    CU = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # C相电压:
    CI = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 计算增量更新标识:
    IncrementFlag = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 两个相邻采集点上一个采集点ID:
    PrevID = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 区域:
    AreaName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# ElectricEnergy_END:


# SteamEnergy_START:
class SteamEnergy(Base):
    """蒸汽能量"""
    __tablename__ = "SteamEnergy"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 瞬时流量单位:
    FlowUnit = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 仪表ID:
    EquipmnetID = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 价格ID:
    PriceID = Column(Float(53), primary_key=False, autoincrement=False, nullable=True)

    # 采集点:
    TagClassValue = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 采集时间:
    CollectionDate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 采集年:
    CollectionYear = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 采集月:
    CollectionMonth = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 采集天:
    CollectionDay = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 温度:
    WD = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 蒸汽瞬时值（单位：kg/h）:
    FlowValue = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 蒸汽重量累计值（单位：kg）:
    SumValue = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 累计量体积单位:
    SumUnit = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 体积（单位：m3:
    Volume = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 计算增量更新标识:
    IncrementFlag = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 两个相邻采集点上一个采集点ID:
    PrevID = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 区域:
    AreaName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 增量库体积插入标识
    insertVolumeFlag = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# SteamEnergy_END:


# WaterEnergy_START:
class WaterEnergy(Base):
    """水能"""
    __tablename__ = "WaterEnergy"

    # ID:
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 水瞬时流量单位:
    FlowWUnit = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 仪表ID:
    EquipmnetID = Column(Integer, primary_key=False, autoincrement=False, nullable=True)

    # 价格ID:
    PriceID = Column(Float(53), primary_key=False, autoincrement=False, nullable=True)

    # 采集点:
    TagClassValue = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 采集时间:
    CollectionDate = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 采集年:
    CollectionYear = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 采集月:
    CollectionMonth = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 采集天:
    CollectionDay = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 瞬时流量:
    WaterFlow = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 累计流量:
    WaterSum = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 水累计量体积单位:
    SumWUnit = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 计算增量更新标识:
    IncrementFlag = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 两个相邻采集点上一个采集点ID:
    PrevID = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)

    # 区域:
    AreaName = Column(Unicode(32), primary_key=False, autoincrement=False, nullable=True)


# WaterEnergy_END:

# 生成表单的执行语句_START
Base.metadata.create_all(engine)

# 生成表单的执行语句_END
