<template>
  <el-container class="body-container">
    <!-- 侧边栏 -->
    <el-aside width="180px" class="left-aside">
      <el-row>
        <el-col :span="24">
          <div class="aside-head">
            <router-link :to="{name:'home'}">
              <el-image style="padding: 0 25px;" :src="require('@/assets/imgs/logo.png')"></el-image>
            </router-link>
          </div>
          <div :style="selfHeight" class="aside-menu">
            <el-menu class="menu-ul" :default-active="defaultActiveUrl" :collapse="isCollapse" :router="true">
              <template v-for="item in subMenulist">
                <el-menu-item v-if="!item.children" :index="item.url"><i :class="item.icon"></i><span slot="title">{{ item.name }}</span></el-menu-item>
                <el-submenu v-if="!item.url" :index="item.name">
                  <template slot="title"><i :class="item.icon"></i><span>{{ item.name }}</span></template>
                  <el-menu-item v-for="(child,childIndex) in item.children" :key="childIndex" :index="child.url" @click="clickSubMenu(child.name)"><span style="margin-left:10px;">{{child.name}}</span></el-menu-item>
                </el-submenu>
              </template>
            </el-menu>
          </div>
          <div class="aside-foot">
            <el-button :icon="sideIcon" size="mini" circle @click="iconToggle"></el-button>
            <div class="version-number">V2.0</div>
          </div>
        </el-col>
      </el-row>
    </el-aside>
    <!-- 右侧部分 -->
    <el-container>
      <!-- 头部 -->
      <el-header>
        <div class="head-left-menu">
          <ul>
            <li>
              <el-dropdown class="head-menu-item" trigger="click" @command="handleCommand">
                <span class="el-dropdown-link">
                  <i class="el-icon-user-solid el-icon--left"></i>{{ this.$store.state.UserName }}<i class="el-icon-arrow-down el-icon--right"></i>
                </span>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item command="a">个人信息</el-dropdown-item>
                  <el-dropdown-item command="b"><i class="fa fa-power-off"></i></el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </li>
            <li>
              <el-tooltip class="head-menu-item" effect="dark" content="采集点分布图" placement="bottom">
                <i class="el-icon-office-building" @click="scattergram"></i>
              </el-tooltip>
            </li>
            <li>
              <el-tooltip class="head-menu-item" effect="dark" content="锅炉房蒸汽总量采集状态" placement="bottom">
                <el-badge>
                  <i class="eq_stuIcon text-size-18 el-icon-bell" @click="getStu_Equ"></i>
                </el-badge>
              </el-tooltip>
            </li>
            <li>
              <el-tooltip class="head-menu-item" effect="dark" content="全屏" placement="bottom">
                <i :class="isFullScreen?'el-icon-aim':'el-icon-full-screen'" @click="getFullCreeen"></i>
              </el-tooltip>
            </li>
            <li style="margin-right: 10px;" v-if="weatherDesc === 'OK'">
              <el-tooltip class="head-menu-item" effect="dark" :content="weatherType" placement="bottom">
                <i :class="weatherIcon"></i>
              </el-tooltip>
            </li>
            <li>
            <div>{{ time }}</div></li>
          </ul>
        </div>
        <div class="head-right-menu">
          <ul>
            <li v-for="(item,index) in mainMenuList" :key="index" @click="clickMainMenu(index)" v-bind:class="{active:index==isactive}">{{ item.text }}</li>
          </ul>
        </div>
        <el-drawer :visible.sync="drawer" :with-header="false" size="91%" @close="closesocket">
          <div class="drawerContent">
            <div class="drawerMaskBg"></div>
            <i class="close-drawer el-icon-close text-size-large" @click="drawer=false"></i>
            <div style="position: absolute;top: 50px;left: 100px;">
              <div style="display: inline-block;width: 15px;height: 15px;border-radius: 50%;background: #FB8A06;margin-left: 10px;"></div> 电
              <div style="display: inline-block;width: 15px;height: 15px;border-radius: 50%;background: #228AD5;margin-left: 10px;"></div> 水
              <div style="display: inline-block;width: 15px;height: 15px;border-radius: 50%;background: #15CC48;margin-left: 10px;"></div> 汽
            </div>
            <div class="mapContent" v-if="JSON.stringify(steamTagList) != '{}'">
              <div style="position: relative;height: 100%;">
                <div v-for="(item,index) in drawerAreaOption" class="mapContentItem"
                     :style="{top: item.top,left: item.left}" :key="index">
                  <div>
                    <div class="mapItemPoint ElectricPoint" v-if="item.hasElectric" @click="showAreaElectric(item.title)"></div>
                    <div class="mapItemPoint WaterPoint" v-if="item.hasWater" @click="showAreaWater(item.title)"></div>
                    <div class="mapItemPoint SteamPoint" v-if="item.hasSteam" @click="showAreaSteam(item.title,item.img,item.img2)"></div>
                  </div>
                </div>
              </div>
            </div>
            <div style="position: absolute;left: 0;">
              <el-button type="primary" @click="lookWaterMap" v-if="JSON.stringify(waterTagList) != '{}'">水表采集图</el-button>
              <!--<el-button type="primary" @click="lookElectricMap" v-if="JSON.stringify(electricTagList) != '{}'">电表采集图</el-button>-->
              <el-button type="primary" @click="lookElectricMap">电表采集图</el-button>
            </div>
          </div>
        </el-drawer>
        <!-- 水表分布图 -->
        <el-dialog title="水表采集分布" :visible.sync="waterAreaDialog" width="75%" v-if="waterAreaDialog">
          <el-row :gutter="20">
            <el-col :span="24" style="margin-bottom: 20px;">
              <el-col :span="4">
                <el-card shadow="hover" class="useAreaCard">
                  <p>污水站</p><div class="waterTagData" style="bottom: 3px;left: 3px;">灌溉水DN40
                  <p>{{ waterTagList.W_Area_WSZ_16_2_34.sumValue }}</p><p>{{ waterTagList.W_Area_WSZ_16_2_34.flowValue }}</p>
                </div>
                </el-card>
              </el-col>
              <el-col :span="8">
                <el-card shadow="hover" class="useAreaCard itemMarginBottom">
                  <p>锅炉房</p><div class="waterTagData">灌溉水DN100</div>
                </el-card>
                <el-card shadow="hover" class="useAreaCard itemMarginBottom">
                  <p>提取二车间</p>
                  <div class="waterTagData" style="right: 3px;top: 3px;">后走廊灌溉水DN40<p>{{ waterTagList.W_Area_TQR_17_2_8.sumValue }}</p><p>{{ waterTagList.W_Area_TQR_17_2_8.flowValue }}</p></div>
                  <div class="waterTagData" style="bottom: 3px;left:3px;">出料电梯旁饮用水DN100<p>{{ waterTagList.W_Area_TQR_17_1_9.sumValue }}</p><p>{{ waterTagList.W_Area_TQR_17_1_9.flowValue }}</p></div>
                </el-card>
                <el-card shadow="hover" class="useAreaCard" style="height: 140px;">
                  <p>综合车间</p>
                  <div class="waterTagData" style="right: 3px;top: 3px;">带干辅机灌溉水DN40<p>{{ waterTagList.W_Area_ZH_23_2_13.sumValue }}</p><p>{{ waterTagList.W_Area_ZH_23_2_13.flowValue }}</p></div>
                  <div class="waterTagData" style="right: 3px;bottom: 3px;">2楼会议室饮用水DN150<p>{{ waterTagList.W_Area_ZH_23_1_12.sumValue }}</p><p>{{ waterTagList.W_Area_ZH_23_1_12.flowValue }}</p></div>
                </el-card>
              </el-col>
              <el-col :span="4">
                <el-card shadow="hover" style="height: 250px;margin-bottom: 20px;" class="useAreaCard">
                  <p>新综合制剂车间</p>
                  <div class="waterTagData" style="left: 3px;top: 60px;width: 80px;">包材库灌溉水DN50<p>{{ waterTagList.W_Area_XJZ_12_1_3.sumValue }}</p><p>{{ waterTagList.W_Area_XJZ_12_1_3.flowValue }}</p></div>
                  <div class="waterTagData" style="right: 3px;bottom: 3px;">接待室饮用水DN100<p>{{ waterTagList.W_Area_XJZ_12_2_5.sumValue }}</p><p>{{ waterTagList.W_Area_XJZ_12_2_5.flowValue }}</p></div>
                </el-card>
              </el-col>
              <el-col :span="8">
                <el-col :span="8">
                  <el-card shadow="hover" class="useAreaCard" style="height: 240px;">
                    <p>化验室/中试车间</p><div class="waterTagData" style="left: 3px;bottom: 3px;">消防水DN100<p>{{ waterTagList.W_Area_YF_26_1_15.sumValue }}</p><p>{{ waterTagList.W_Area_YF_26_1_15.flowValue }}</p></div>
                  </el-card>
                </el-col>
                <el-col :span="8">
                  <el-card shadow="hover" class="useAreaCard" style="height: 180px;">
                    <p>原提取</p>
                    <div class="waterTagData" style="left: 3px;top: 40px;">消防水DN50<p>{{ waterTagList.W_Area_YTQ_39_1_30.sumValue }}</p><p>{{ waterTagList.W_Area_YTQ_39_1_30.flowValue }}</p></div>
                    <div class="waterTagData" style="left: 3px;bottom: 3px;">灌溉水DN40<p>{{ waterTagList.W_Area_YTQ_39_2_30.sumValue }}</p><p>{{ waterTagList.W_Area_YTQ_39_2_30.flowValue }}</p></div>
                  </el-card>
                </el-col>
                <el-col :span="8">
                  <el-card shadow="hover" class="useAreaCard" style="height: 240px;">
                    <p>前处理车间</p>
                    <div class="waterTagData" style="left: 3px;top: 40px;">洗药室灌溉水DN25<p>{{ waterTagList.W_Area_QCL_33_1_20.sumValue }}</p><p>{{ waterTagList.W_Area_QCL_33_1_20.flowValue }}</p></div>
                    <div class="waterTagData" style="left: 3px;top: 120px;">饮用水DN25<p>{{ waterTagList.W_Area_QCL_33_2_20.sumValue }}</p><p>{{ waterTagList.W_Area_QCL_33_2_20.flowValue }}</p></div>
                    <div class="waterTagData" style="right: 3px;bottom: 3px;">生产部 灌消防水</div>
                  </el-card>
                </el-col>
                <el-col :span="24" style="margin-top: 20px;">
                  <el-card shadow="hover" class="useAreaCard" style="height: 140px;">
                    <p>健康科技车间</p>
                    <div class="waterTagData" style="right: 3px;top: 3px;">消防水DN50<p>{{ waterTagList.W_Area_JK_28_1_16.sumValue }}</p><p>{{ waterTagList.W_Area_JK_28_1_16.flowValue }}</p></div>
                    <div class="waterTagData" style="right: 3px;bottom: 3px;">消防水DN50<p>{{ waterTagList.W_Area_JK_28_2_16.sumValue }}</p><p>{{ waterTagList.W_Area_JK_28_2_16.flowValue }}</p></div>
                  </el-card>
                </el-col>
                <el-col :span="24" style="margin-top: 20px;">
                  <el-card shadow="hover" class="useAreaCard" style="height: 140px;">
                    <p>固体制剂车间</p>
                    <div class="waterTagData" style="right: 3px;top: 3px;">男卫生间灌溉水DN40<p>{{ waterTagList.W_Area_GT_30_2_18.sumValue }}</p><p>{{ waterTagList.W_Area_GT_30_2_18.flowValue }}</p></div>
                    <div class="waterTagData" style="right: 3px;bottom: 3px;">纯化水站饮用水DN100<p>{{ waterTagList.W_Area_GT_30_1_19.sumValue }}</p><p>{{ waterTagList.W_Area_GT_30_1_19.flowValue }}</p></div>
                  </el-card>
                </el-col>
              </el-col>
            </el-col>
            <el-col :span="24">
              <el-col :span="8" :offset="5">
                <el-card shadow="hover" class="useAreaCard">
                  <p>办公楼\食堂</p>
                  <div class="waterTagData" style="left: 100px;bottom: 10px;">1楼卫生间深井水DN65<p>{{ waterTagList.W_Area_BGL_34_1_22.sumValue }}</p><p>{{ waterTagList.W_Area_BGL_34_1_22.flowValue }}</p></div>
                </el-card>
              </el-col>
            </el-col>
          </el-row>
          <div slot="footer" class="dialog-footer">
            <el-button @click="waterAreaDialog = false">关闭</el-button>
          </div>
        </el-dialog>
        <!-- 电表采集分布图 -->
        <el-dialog title="电表采集分布" :visible.sync="electricAreaDialog" width="90%" top="0" v-if="electricAreaDialog">
          <el-col :span="24">
            <div></div>
            <ul class="areaTotalTagUl">
              <li>
                <div class="cardformContainer text-center">污水站</div>
                <div class="TagLine"></div>
                <div class="cardformContainer itemMarginBottom-s">
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_WSZ_16_2_35.ZGL }}</p></div>
                  <p>电表</p>
                </div>
              </li>
              <li>
                <div class="cardformContainer text-center">锅炉房</div>
                <div class="TagLine"></div>
                <div class="cardformContainer itemMarginBottom-s">
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_GLF_42_1_33_1.ZGL }}</p></div>
                  <p>锅炉</p>
                </div>
                <div class="cardformContainer itemMarginBottom-s">
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_GLF_42_1_33_2.ZGL }}</p></div>
                  <p>供暖</p>
                </div>
                <div class="cardformContainer itemMarginBottom-s">
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_GLF_42_1_33_3.ZGL }}</p></div>
                  <p>脱硫</p>
                </div>
              </li>
              <li>
                <div class="cardformContainer text-center">提取二车间</div>
                <div class="TagLine"></div>
                <div class="cardformContainer itemMarginBottom-s">
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_TQR_18_2_36_1.ZGL }}</p></div>
                  <p>2L空调室二冷水机组</p>
                </div>
                <div class="cardformContainer itemMarginBottom-s">
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_TQR_18_2_36_2.ZGL }}</p></div>
                  <p>2L空调室二空调机组</p>
                </div>
                <div class="cardformContainer itemMarginBottom-s">
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_TQR_18_2_36_3.ZGL }}</p></div>
                  <p>2L电控室冷水机组</p>
                </div>
                <div class="cardformContainer itemMarginBottom-s">
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_TQR_18_2_36_4.ZGL }}</p></div>
                  <p>2L电控室制粒</p>
                </div>
              </li>
              <li>
                <div class="cardformContainer text-center">综合车间</div>
                <div class="TagLine"></div>
                <div class="cardformContainer itemMarginBottom-s">
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_ZH_1.ZGL }}</p></div>
                  <p>MVR</p>
                </div>
                <div class="cardformContainer itemMarginBottom-s">
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_ZH_2.ZGL }}</p></div>
                  <p>MVR</p>
                </div>
                <div class="cardformContainer itemMarginBottom-s">
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_ZH_50_1_41_1.ZGL }}</p></div>
                  <p>总表、制粒、带干、粉糖、输液泵</p>
                </div>
                <div class="cardformContainer itemMarginBottom-s">
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_ZH_50_1_41_2.ZGL }}</p></div>
                  <p>制粒</p>
                </div>
                <div class="cardformContainer itemMarginBottom-s">
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_ZH_50_1_41_3.ZGL }}</p></div>
                  <p>带干</p>
                </div>
                <div class="cardformContainer itemMarginBottom-s">
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_ZH_50_1_41_4.ZGL }}</p></div>
                  <p>浓缩罐、自控系统、电梯、洗衣房、真空泵</p>
                </div>
                <div class="cardformContainer itemMarginBottom-s">
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_ZH_50_1_41_5.ZGL }}</p></div>
                  <p>排风</p>
                </div>
                <div class="cardformContainer itemMarginBottom-s">
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_ZH_50_1_41_6.ZGL }}</p></div>
                  <p>照明</p>
                </div>
              </li>
              <li>
                <div class="cardformContainer text-center">新建综合制剂车间</div>
                <div class="TagLine"></div>
                <div class="cardformContainer itemMarginBottom-s">
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_XJZ_11_2_7.ZGL }}</p></div>
                  <p>2L空压机、循环水、机器人</p>
                </div>
                <div class="cardformContainer itemMarginBottom-s">
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_XJZ_11_2_7_1.ZGL }}</p></div>
                  <p>2L干法、颗粒</p>
                </div>
                <div class="cardformContainer itemMarginBottom-s">
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_XJZ_11_2_7_3.ZGL }}</p></div>
                  <p>2L电梯、压片、胶囊、泡罩、粉碎</p>
                </div>
                <div class="cardformContainer itemMarginBottom-s">
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_XJZ_11_2_7_4.ZGL }}</p></div>
                  <p>2L空调</p>
                </div>
                <div class="cardformContainer itemMarginBottom-s">
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_XJZ_11_1_6_5.ZGL }}</p></div>
                  <p>1L洗衣机、照明、卷帘门、风机</p>
                </div>
                <div class="cardformContainer itemMarginBottom-s">
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_XJZ_11_1_6_6.ZGL }}</p></div>
                  <p>1L冷水机组2</p>
                </div>
              </li>
              <li>
                <div class="cardformContainer text-center">变电所</div>
                <div class="TagLine"></div>
                <div class="cardformContainer itemMarginBottom-s">
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_BDS_49_1_39_1.ZGL }}</p></div><p>40喷干</p>
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_BDS_49_1_39_2.ZGL }}</p></div><p>50喷干</p>
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_BDS_49_1_39_3.ZGL }}</p></div><p>新提取循环水泵</p>
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_BDS_49_1_39_4.ZGL }}</p></div><p>消防水泵+新大库</p>
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_BDS_49_2_40_5.ZGL }}</p></div><p>GMP</p>
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_BDS_49_2_40_6.ZGL }}</p></div><p>前处理</p>
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_BDS_49_2_40_7.ZGL }}</p></div><p>仓储中心</p>
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_BDS_49_2_40_8.ZGL }}</p></div><p>提取二照明</p>
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_BDS_49_2_40_9.ZGL }}</p></div><p>40粉碎、提取二空调</p>
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_BDS_49_2_40_10.ZGL }}</p></div><p>60带干、风机、制粒、办公</p>
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_BDS_49_2_40_11.ZGL }}</p></div><p>提取、自控</p>
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_BDS_49_2_40_12.ZGL }}</p></div><p>提取二车间新空调</p>
                </div>
              </li>
              <li>
                <div class="cardformContainer text-center">中试车间</div>
                <div class="TagLine"></div>
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_YF_26_1_14.ZGL }}</p></div><p>电器</p>
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_YF_26_1_14_2.ZGL }}</p></div><p>老醇提水泵、车床、台钻、砂轮</p>
              </li>
              <li>
                <div class="cardformContainer text-center">智能库</div>
                <div class="TagLine"></div>
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_ZNK_24_1_10_1.ZGL }}</p></div><p>1L</p>
              </li>
              <li>
                <div class="cardformContainer text-center">原提取车间</div>
                <div class="TagLine"></div>
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_YTQ_38_1_28.ZGL }}</p></div><p>办公、新700粉碎机、机修、设备库房</p>
              </li>
              <li>
                <div class="cardformContainer text-center">前处理车间</div>
                <div class="TagLine"></div>
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_YTQ_38_2_29.ZGL }}</p></div><p>办公、新700粉碎机、机修、设备库房</p>
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_YTQ_38_2_29_3.ZGL }}</p></div><p>洗药机、切药机</p>
              </li>
              <li>
                <div class="cardformContainer text-center">GMP车间</div>
                <div class="TagLine"></div>
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_JK_28_2_17.ZGL }}</p></div><p>1L</p>
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_JK_28_1_16.ZGL }}</p></div><p>2L</p>
              </li>
              <li>
                <div class="cardformContainer text-center">固体制剂车间</div>
                <div class="TagLine"></div>
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_GT_30_2_19.ZGL }}</p></div><p>除尘系统、空调系统</p>
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_GT_30_2_19_1.ZGL }}</p></div><p>机修办公室、压片、胶囊、混合、挂衣、颗粒、瓶线</p>
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_GT_30_2_19_2.ZGL }}</p></div><p>风冷冷水机、除湿机、空压机</p>
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_GT_30_2_19_3.ZGL }}</p></div><p>照明</p>
              </li>
              <li>
                <div class="cardformContainer text-center">办公楼＼食堂</div>
                <div class="TagLine"></div>
                  <div class="electricTagData"><p>{{ electricTagList.E_Area_BGL_36_1_26.ZGL }}</p></div><p>老屋角</p>
              </li>
            </ul>
          </el-col>
          <div slot="footer" class="dialog-footer">
            <el-button @click="electricAreaDialog = false">关闭</el-button>
          </div>
        </el-dialog>
        <!-- 水表分布图 -->
        <el-dialog :title="areaOverallDialogTitle" :visible.sync="waterAreaTagDialog" width="40%" v-if="waterAreaTagDialog">
          <el-card shadow="never" v-if="areaOverallDialogTitle === '污水站'">
            <div class="waterTagData" style="position: relative">灌溉水DN40<p>{{ waterTagList.W_Area_WSZ_16_2_34.sumValue }}</p><p>{{ waterTagList.W_Area_WSZ_16_2_34.flowValue }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '提取二车间'">
            <div class="waterTagData" style="position: relative">后走廊灌溉水DN40<p>{{ waterTagList.W_Area_TQR_17_2_8.sumValue }}</p><p>{{ waterTagList.W_Area_TQR_17_2_8.flowValue }}</p></div>
            <div class="waterTagData" style="position: relative">出料电梯旁饮用水DN100<p>{{ waterTagList.W_Area_TQR_17_1_9.sumValue }}</p><p>{{ waterTagList.W_Area_TQR_17_1_9.flowValue }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '综合车间'">
            <div class="waterTagData" style="position: relative">带干辅机灌溉水DN40<p>{{ waterTagList.W_Area_ZH_23_2_13.sumValue }}</p><p>{{ waterTagList.W_Area_ZH_23_2_13.flowValue }}</p></div>
            <div class="waterTagData" style="position: relative">2楼会议室饮用水DN150<p>{{ waterTagList.W_Area_ZH_23_1_12.sumValue }}</p><p>{{ waterTagList.W_Area_ZH_23_1_12.flowValue }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '新建综合制剂车间'">
            <div class="waterTagData" style="position: relative">包材库灌溉水DN50<p>{{ waterTagList.W_Area_XJZ_12_1_3.sumValue }}</p><p>{{ waterTagList.W_Area_XJZ_12_1_3.flowValue }}</p></div>
            <div class="waterTagData" style="position: relative">接待室饮用水DN100<p>{{ waterTagList.W_Area_XJZ_12_2_5.sumValue }}</p><p>{{ waterTagList.W_Area_XJZ_12_2_5.flowValue }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '中试车间'">
            <div class="waterTagData" style="position: relative">消防水DN100<p>{{ waterTagList.W_Area_YF_26_1_15.sumValue }}</p><p>{{ waterTagList.W_Area_YF_26_1_15.flowValue }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '原提取车间'">
            <div class="waterTagData" style="position: relative">消防水DN50<p>{{ waterTagList.W_Area_YTQ_39_1_30.sumValue }}</p><p>{{ waterTagList.W_Area_YTQ_39_1_30.flowValue }}</p></div>
            <div class="waterTagData" style="position: relative">灌溉水DN40<p>{{ waterTagList.W_Area_YTQ_39_2_30.sumValue }}</p><p>{{ waterTagList.W_Area_YTQ_39_2_30.flowValue }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '前处理车间'">
            <div class="waterTagData" style="position: relative">洗药室灌溉水DN25<p>{{ waterTagList.W_Area_QCL_33_1_20.sumValue }}</p><p>{{ waterTagList.W_Area_QCL_33_1_20.flowValue }}</p></div>
            <div class="waterTagData" style="position: relative">饮用水DN25<p>{{ waterTagList.W_Area_QCL_33_2_20.sumValue }}</p><p>{{ waterTagList.W_Area_QCL_33_2_20.flowValue }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === 'GMP车间'">
            <div class="waterTagData" style="position: relative">消防水DN50<p>{{ waterTagList.W_Area_JK_28_1_16.sumValue }}</p><p>{{ waterTagList.W_Area_JK_28_1_16.flowValue }}</p></div>
            <div class="waterTagData" style="position: relative">消防水DN50<p>{{ waterTagList.W_Area_JK_28_2_16.sumValue }}</p><p>{{ waterTagList.W_Area_JK_28_2_16.flowValue }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '固体制剂车间'">
            <div class="waterTagData" style="position: relative">男卫生间灌溉水DN40<p>{{ waterTagList.W_Area_GT_30_2_18.sumValue }}</p><p>{{ waterTagList.W_Area_GT_30_2_18.flowValue }}</p></div>
            <div class="waterTagData" style="position: relative">纯化水站饮用水DN100<p>{{ waterTagList.W_Area_GT_30_1_19.sumValue }}</p><p>{{ waterTagList.W_Area_GT_30_1_19.flowValue }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '办公楼＼食堂'">
            <div class="waterTagData" style="position: relative">1楼卫生间深井水DN65<p>{{ waterTagList.W_Area_BGL_34_1_22.sumValue }}</p><p>{{ waterTagList.W_Area_BGL_34_1_22.flowValue }}</p></div>
          </el-card>
          <div slot="footer" class="dialog-footer">
            <el-button @click="waterAreaTagDialog = false">关 闭</el-button>
          </div>
        </el-dialog>
        <!-- 电表分布图 -->
        <el-dialog :title="areaOverallDialogTitle" :visible.sync="electricAreaTagDialog" width="40%" v-if="electricAreaTagDialog">
          <el-card shadow="never" v-if="areaOverallDialogTitle === '污水站'">
            <div class="waterTagData" style="position: relative">电表<p></p><p class="TagDataVal">{{ electricTagList.E_Area_WSZ_16_2_35.ZGL }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '新建综合制剂车间'">
            <div class="waterTagData" style="position: relative">2楼配电室<p>空压机、循环水、机器人</p><p class="TagDataVal">{{ electricTagList.E_Area_XJZ_11_2_7.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">2楼配电室<p>干法、颗粒</p><p class="TagDataVal">{{ electricTagList.E_Area_XJZ_11_2_7_1.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">2楼配电室<p>电梯、压片、胶囊、泡罩、粉碎</p><p class="TagDataVal">{{ electricTagList.E_Area_XJZ_11_2_7_3.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">1楼空调室<p>2L空调</p><p class="TagDataVal">{{ electricTagList.E_Area_XJZ_11_2_7_4.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">1楼配电室<p>洗衣机、照明、卷帘门、风机</p><p class="TagDataVal">{{ electricTagList.E_Area_XJZ_11_1_6_5.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">1楼冷水室<p>冷水机组2</p><p class="TagDataVal">{{ electricTagList.E_Area_XJZ_11_1_6_6.ZGL }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '中试车间'">
            <div class="waterTagData" style="position: relative">化验室<p>电器</p><p class="TagDataVal">{{ electricTagList.E_Area_YF_26_1_14.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">化验室<p>老醇提水泵、车床、台钻、砂轮</p><p class="TagDataVal">{{ electricTagList.E_Area_YF_26_1_14_2.ZGL }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '原提取车间'">
            <div class="waterTagData" style="position: relative">老醇提<p>办公、新700粉碎机、机修、设备库房</p><p class="TagDataVal">{{ electricTagList.E_Area_YTQ_38_1_28.ZGL }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '前处理车间'">
            <div class="waterTagData" style="position: relative">前处理1楼<p>办公、新700粉碎机、机修、设备库房</p><p class="TagDataVal">{{ electricTagList.E_Area_YTQ_38_2_29.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">前处理1楼<p>洗药机、切药机</p><p class="TagDataVal">{{ electricTagList.E_Area_YTQ_38_2_29_3.ZGL }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === 'GMP车间'">
            <div class="waterTagData" style="position: relative">电表（1楼）<p></p><p class="TagDataVal">{{ electricTagList.E_Area_JK_28_2_17.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">电表（2楼）<p></p><p class="TagDataVal">{{ electricTagList.E_Area_JK_28_1_16.ZGL }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '固体制剂车间'">
            <div class="waterTagData" style="position: relative">1楼配电室<p>除尘系统、空调系统</p><p class="TagDataVal">{{ electricTagList.E_Area_GT_30_2_19.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">1楼配电室<p>机修办公室、压片、胶囊、混合、挂衣、颗粒、瓶线</p><p class="TagDataVal">{{ electricTagList.E_Area_GT_30_2_19_1.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">1楼配电室<p>风冷冷水机、除湿机、空压机</p><p class="TagDataVal">{{ electricTagList.E_Area_GT_30_2_19_2.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">1楼配电室<p>照明</p><p class="TagDataVal">{{ electricTagList.E_Area_GT_30_2_19_3.ZGL }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '办公楼＼食堂'">
            <div class="waterTagData" style="position: relative">老屋角<p></p><p class="TagDataVal">{{ electricTagList.E_Area_BGL_36_1_26.ZGL }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '提取二车间'">
            <div class="waterTagData" style="position: relative">2L空调室二<p>冷水机组</p><p class="TagDataVal">{{ electricTagList.E_Area_TQR_18_2_36_1.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">2L空调室二<p>空调机组</p><p class="TagDataVal">{{ electricTagList.E_Area_TQR_18_2_36_2.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">2L电控室<p>冷水机组</p><p class="TagDataVal">{{ electricTagList.E_Area_TQR_18_2_36_3.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">2L电控室<p>制粒</p><p class="TagDataVal">{{ electricTagList.E_Area_TQR_18_2_36_4.ZGL }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '锅炉房'">
            <div class="waterTagData" style="position: relative">锅炉房电柜<p>锅炉</p><p>{{ electricTagList.E_Area_GLF_42_1_33_1.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">锅炉房电柜<p>供暖</p><p>{{ electricTagList.E_Area_GLF_42_1_33_2.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">锅炉房旁边屋子<p>脱硫</p><p>{{ electricTagList.E_Area_GLF_42_1_33_3.ZGL }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '智能库'">
            <div class="waterTagData" style="position: relative">智能库1L<p></p><p class="TagDataVal">{{ electricTagList.E_Area_ZNK_24_1_10_1.ZGL }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '综合车间'">
            <div class="waterTagData" style="position: relative">MVR<p></p><p class="TagDataVal">{{ electricTagList.E_Area_ZH_1.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">MVR<p></p><p class="TagDataVal">{{ electricTagList.E_Area_ZH_2.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">2L配电室<p>总表、制粒、带干、粉糖、输液泵</p><p class="TagDataVal">{{ electricTagList.E_Area_ZH_50_1_41_1.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">2L配电室<p>制粒</p><p class="TagDataVal">{{ electricTagList.E_Area_ZH_50_1_41_2.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">2L配电室<p>带干</p><p class="TagDataVal">{{ electricTagList.E_Area_ZH_50_1_41_3.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">2L配电室<p>浓缩罐、自控系统、电梯、洗衣房、真空泵</p><p class="TagDataVal">{{ electricTagList.E_Area_ZH_50_1_41_4.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">2L配电室<p>排风</p><p class="TagDataVal">{{ electricTagList.E_Area_ZH_50_1_41_5.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">2L配电室<p>照明</p><p class="TagDataVal">{{ electricTagList.E_Area_ZH_50_1_41_6.ZGL }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '变电所'">
            <div class="waterTagData" style="position: relative">变电所<p>40喷干</p><p class="TagDataVal">{{ electricTagList.E_Area_BDS_49_1_39_1.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">变电所<p>50喷干</p><p class="TagDataVal">{{ electricTagList.E_Area_BDS_49_1_39_2.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">变电所<p>新提取循环水泵</p><p class="TagDataVal">{{ electricTagList.E_Area_BDS_49_1_39_3.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">变电所<p>消防水泵+新大库</p><p class="TagDataVal">{{ electricTagList.E_Area_BDS_49_1_39_4.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">变电所<p>GMP</p><p class="TagDataVal">{{ electricTagList.E_Area_BDS_49_2_40_5.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">变电所<p>前处理</p><p class="TagDataVal">{{ electricTagList.E_Area_BDS_49_2_40_6.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">变电所<p>仓储中心</p><p class="TagDataVal">{{ electricTagList.E_Area_BDS_49_2_40_7.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">变电所<p>提取二照明</p><p class="TagDataVal">{{ electricTagList.E_Area_BDS_49_2_40_8.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">变电所<p>40粉碎、提取二空调</p><p class="TagDataVal">{{ electricTagList.E_Area_BDS_49_2_40_9.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">变电所<p>60带干、风机、制粒、办公</p><p class="TagDataVal">{{ electricTagList.E_Area_BDS_49_2_40_10.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">变电所<p>提取、自控</p><p class="TagDataVal">{{ electricTagList.E_Area_BDS_49_2_40_11.ZGL }}</p></div>
            <div class="waterTagData" style="position: relative">变电所<p>提取二车间新空调</p><p class="TagDataVal">{{ electricTagList.E_Area_BDS_49_2_40_12.ZGL }}</p></div>
          </el-card>
          <div slot="footer" class="dialog-footer">
            <el-button @click="electricAreaTagDialog = false">关 闭</el-button>
          </div>
        </el-dialog>
        <!-- 汽表分布图 没有图片 -->
        <el-dialog :title="areaOverallDialogTitle" :visible.sync="steamAreaTagDialog" width="40%" v-if="steamAreaTagDialog">
          <el-card shadow="never" v-if="areaOverallDialogTitle === '中试车间'">
            <div class="waterTagData" style="position: relative">蒸汽表<p>{{ steamTagList.S_Area_YF_25_1_502.sumValue }}</p><p>{{ steamTagList.S_Area_YF_25_1_502.flowValue }}</p><p>{{ steamTagList.S_Area_YF_25_1_502.SteamWD }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '原提取车间'">
            <div class="waterTagData" style="position: relative">蒸汽表<p>{{ steamTagList.S_Area_YTQ_40_1_502.sumValue }}</p><p>{{ steamTagList.S_Area_YTQ_40_1_502.flowValue }}</p><p>{{ steamTagList.S_Area_YTQ_40_1_502.SteamWD }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '前处理车间'">
            <div class="waterTagData" style="position: relative">蒸汽表<p>{{ steamTagList.S_Area_YTQ_40_2_502.sumValue }}</p><p>{{ steamTagList.S_Area_YTQ_40_2_502.flowValue }}</p><p>{{ steamTagList.S_Area_YTQ_40_2_502.SteamWD }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === 'GMP车间'">
            <div class="waterTagData" style="position: relative">蒸汽表<p>{{ steamTagList.S_Area_JK_27_1_502.sumValue }}</p><p>{{ steamTagList.S_Area_JK_27_1_502.flowValue }}</p><p>{{ steamTagList.S_Area_JK_27_1_502.SteamWD }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '办公楼＼食堂'">
            <div class="waterTagData" style="position: relative">蒸汽表<p>{{ steamTagList.S_Area_BGL_35_1_502.sumValue }}</p><p>{{ steamTagList.S_Area_BGL_35_1_502.flowValue }}</p><p>{{ steamTagList.S_Area_BGL_35_1_502.SteamWD }}</p></div>
          </el-card>
          <div slot="footer" class="dialog-footer">
            <el-button @click="steamAreaTagDialog = false">关 闭</el-button>
          </div>
        </el-dialog>
        <!-- 汽表分布图 有图片-->
        <el-dialog :title="areaOverallDialogTitle" :visible.sync="areaOverallDialog" :modal="false" width="840px">
          <div v-if="areaOverallDialogSrc2" style="position: relative;display: inline-flex;">
            <el-image style="width: 100%;" :src="areaOverallDialogSrc2"></el-image>
            <div v-if="areaOverallDialogTitle === '提取二车间'">
              <div class="steamTagLabel" style="left:-10px;top: -15px;min-width: 155px;width: 155px;">
                <div class="steamTagTitle">锅炉流量计DN400</div>
                <div class="steamTagValue">
                  <p>{{ steamGlTag.sumValue }}t</p>
                  <p>{{ steamGlTag.flowValue }}t</p>
                  <p>{{ steamGlTag.SteamWD }}°C</p>
                </div>
              </div>
              <div class="steamTagLabel" style="left:210px;top: -54px;min-width: 155px;width: 155px;">
                <div class="steamTagTitle" style="line-height: 45px;">一楼灭菌柜DN80</div>
                <div class="steamTagValue">
                  <p>{{ steamTagList.S_Area_TQR_20_1_502.sumValue }}</p>
                  <p>{{ steamTagList.S_Area_TQR_20_1_502.flowValue }}</p>
                  <p>{{ steamTagList.S_Area_TQR_20_1_502.SteamWD }}°C</p>
                </div>
              </div>
              <div class="steamTagLabel" style="left:152px;top: 82px;min-width: 140px;width: 140px;">
                <div class="steamTagTitle" style="line-height: 22px;">单效/双效浓缩DN20</div>
                <div class="steamTagValue">
                  <p>{{ steamTagList.S_Area_TQR_19_3_502.sumValue }}</p>
                  <p>{{ steamTagList.S_Area_TQR_19_3_502.flowValue }}</p>
                  <p>{{ steamTagList.S_Area_TQR_19_3_502.SteamWD }}°C</p>
                </div>
              </div>
              <div class="steamTagLabel" style="left:700px;top: 95px;;min-width: 95px;width: 95px;">
                <div class="steamTagTitle" style="line-height: 22px;">喷干两台/CIP DN20</div>
                <div class="steamTagValue">
                  <p>{{ steamTagList.S_Area_TQR_20_2_502.sumValue }}</p>
                  <p>{{ steamTagList.S_Area_TQR_20_2_502.flowValue }}</p>
                  <p>{{ steamTagList.S_Area_TQR_20_2_502.SteamWD }}°C</p>
                </div>
              </div>
              <div class="steamTagLabel" style="left:440px;top: 120px;min-width: 140px;width: 140px;">
                <div class="steamTagTitle">提取单号DN150</div>
                <div class="steamTagValue">
                  <p>{{ steamTagList.S_Area_TQR_19_1_502.sumValue }}</p>
                  <p>{{ steamTagList.S_Area_TQR_19_1_502.flowValue }}</p>
                  <p>{{ steamTagList.S_Area_TQR_19_1_502.SteamWD }}°C</p>
                </div>
              </div>
              <div class="steamTagLabel" style="left:373px;top: 320px;">
                <div class="steamTagTitle">提取双号DN150</div>
                <div class="steamTagValue">
                  <p>{{ steamTagList.S_Area_TQR_19_2_502.sumValue }}</p>
                  <p>{{ steamTagList.S_Area_TQR_19_2_502.flowValue }}</p>
                  <p>{{ steamTagList.S_Area_TQR_19_2_502.SteamWD }}°C</p>
                </div>
              </div>
              <div class="steamTagLabel" style="left:-18px;top: 340px;min-width: 85px;width: 85px;">
                <div class="steamTagTitle" style="line-height: 22px;">管式灭菌DN80</div>
                <div class="steamTagValue">
                  <p>{{ steamTagList.S_Area_TQR_20_3_502.sumValue }}</p>
                  <p>{{ steamTagList.S_Area_TQR_20_3_502.flowValue }}</p>
                  <p>{{ steamTagList.S_Area_TQR_20_3_502.SteamWD }}°C</p>
                </div>
              </div>
            </div>
          </div>
          <div style="position: relative;display: inline-flex;">
            <el-image style="width: 100%;" :src="areaOverallDialogSrc"></el-image>
            <div v-if="areaOverallDialogTitle === '锅炉房'">
              <div class="steamTagLabel" style="left:-10px;top: 345px;">
                <div class="steamTagTitle">锅炉总流量计DN400</div>
                <div class="steamTagValue">
                  <p>{{ steamGlTag.sumValue }}t</p>
                  <p>{{ steamGlTag.flowValue }}t</p>
                  <p>{{ steamGlTag.SteamWD }}°C</p>
                </div>
              </div>
              <div class="steamTagLabel" style="left:490px;top: 20px;">
                <div class="steamTagTitle">老醇提/前处理DN100</div>
                <div class="steamTagValue">
                  <p>{{ steamTagList.S_Area_YTQ_40_2_502.sumValue }}</p>
                  <p>{{ steamTagList.S_Area_YTQ_40_2_502.flowValue }}</p>
                  <p>{{ steamTagList.S_Area_YTQ_40_2_502.SteamWD }}°C</p>
                </div>
              </div>
              <div class="steamTagLabel" style="left:495px;top: 100px;">
                <div class="steamTagTitle">GMP/生物科技DN80</div>
                <div class="steamTagValue">
                  <p>{{ steamTagList.S_Area_JK_27_1_502.sumValue }}</p>
                  <p>{{ steamTagList.S_Area_JK_27_1_502.flowValue }}</p>
                  <p>{{ steamTagList.S_Area_JK_27_1_502.SteamWD }}°C</p>
                </div>
              </div>
              <div class="steamTagLabel" style="left:495px;top: 188px;">
                <div class="steamTagTitle">老水提/原提取DN100</div>
                <div class="steamTagValue">
                  <p>{{ steamTagList.S_Area_YTQ_40_1_502.sumValue }}</p>
                  <p>{{ steamTagList.S_Area_YTQ_40_1_502.flowValue }}</p>
                  <p>{{ steamTagList.S_Area_YTQ_40_1_502.SteamWD }}°C</p>
                </div>
              </div>
              <div class="steamTagLabel" style="left:490px;top: 280px;">
                <div class="steamTagTitle">化验室/中试DN100</div>
                <div class="steamTagValue">
                  <p>{{ steamTagList.S_Area_YF_25_1_502.sumValue }}</p>
                  <p>{{ steamTagList.S_Area_YF_25_1_502.flowValue }}</p>
                  <p>{{ steamTagList.S_Area_YF_25_1_502.SteamWD }}°C</p>
                </div>
              </div>
              <div class="steamTagLabel" style="left:512px;top: 370px;">
                <div class="steamTagTitle">供暖DN150</div>
                <div class="steamTagValue">
                  <p>{{ steamTagList.S_Area_GLF_45_3_502.sumValue }}t</p>
                  <p>{{ steamTagList.S_Area_GLF_45_3_502.flowValue }}</p>
                  <p>{{ steamTagList.S_Area_GLF_45_3_502.SteamWD }}°C</p>
                </div>
              </div>
              <div class="steamTagLabel" style="left:500px;top: 450px;">
                <div class="steamTagTitle">食堂DN25</div>
                <div class="steamTagValue">
                  <p>{{ steamTagList.S_Area_BGL_35_1_502.sumValue }}</p>
                  <p>{{ steamTagList.S_Area_BGL_35_1_502.flowValue }}</p>
                  <p>{{ steamTagList.S_Area_BGL_35_1_502.SteamWD }}°C</p>
                </div>
              </div>
            </div>
            <div v-if="areaOverallDialogTitle === '提取二车间'">
              <div class="steamTagLabel" style="left:6px;top: 350px;min-width: 155px;width: 155px;">
                <div class="steamTagTitle">锅炉流量计DN400</div>
                <div class="steamTagValue">
                  <p>{{ steamGlTag.sumValue }}t</p>
                  <p>{{ steamGlTag.flowValue }}t</p>
                  <p>{{ steamGlTag.SteamWD }}°C</p>
                </div>
              </div>
              <div class="steamTagLabel" style="left:408px;top: 461px;min-width: 55px;width: 55px;">
                <div class="steamTagTitle" style="line-height: 22px;padding: 12px 0;">提取停用</div>
              </div>
              <div class="steamTagLabel" style="left:487px;top: 461px;min-width: 55px;width: 55px;">
                <div class="steamTagTitle" style="line-height: 22px;padding: 12px 0;">双效停用</div>
              </div>
            </div>
            <div v-if="areaOverallDialogTitle === '综合车间'">
              <div class="steamTagLabel" style="left:0;top: 50px;min-width: 130px;width: 130px;">
                <div class="steamTagTitle" style="line-height: 22px;">120带干DN32</div>
                <div class="steamTagValue">
                  <p>{{ steamTagList.S_Area_ZH_21_2_502.sumValue }}</p>
                  <p>{{ steamTagList.S_Area_ZH_21_2_502.flowValue }}</p>
                  <p>{{ steamTagList.S_Area_ZH_21_2_502.SteamWD }}°C</p>
                </div>
              </div>
              <div class="steamTagLabel" style="left:0;top: 220px;min-width: 175px;width: 175px;">
                <div class="steamTagTitle" style="line-height: 22px;">流化床制粒DN50</div>
                <div class="steamTagValue">
                  <p>{{ steamTagList.S_Area_ZH_21_1_502.sumValue }}</p>
                  <p>{{ steamTagList.S_Area_ZH_21_1_502.flowValue }}</p>
                  <p>{{ steamTagList.S_Area_ZH_21_1_502.SteamWD }}°C</p>
                </div>
              </div>
              <div class="steamTagLabel" style="left:30px;top: 315px;min-width: 120px;width: 120px;">
                <div class="steamTagTitle" style="line-height: 22px;">锅炉流量计DN400</div>
                <div class="steamTagValue">
                  <p>{{ steamGlTag.sumValue }}t</p>
                  <p>{{ steamGlTag.flowValue }}t</p>
                  <p>{{ steamGlTag.SteamWD }}°C</p>
                </div>
              </div>
              <div class="steamTagLabel" style="left:474px;top: -11px;min-width: 100px;width: 100px;">
                <div class="steamTagTitle" style="line-height: 22px;">二次浓缩DN100</div>
                <div class="steamTagValue">
                  <p>{{ steamTagList.S_Area_ZH_46_1_502.sumValue }}</p>
                  <p>{{ steamTagList.S_Area_ZH_46_1_502.flowValue }}</p>
                  <p>{{ steamTagList.S_Area_ZH_46_1_502.SteamWD }}°C</p>
                </div>
              </div>
              <div class="steamTagLabel" style="left:285px;top: 105px;">
                <div class="steamTagTitle">醇提+浓缩DN150</div>
                <div class="steamTagValue">
                  <p>{{ steamTagList.S_Area_ZH_46_2_502.sumValue }}</p>
                  <p>{{ steamTagList.S_Area_ZH_46_2_502.flowValue }}</p>
                  <p>{{ steamTagList.S_Area_ZH_46_2_502.SteamWD }}°C</p>
                </div>
              </div>
              <div class="steamTagLabel" style="left:362px;top: 176px;min-width: 110px;width: 110px;">
                <div class="steamTagTitle" style="line-height: 22px;">双效浓缩/CIP DN200</div>
                <div class="steamTagValue">
                  <p>{{ steamTagList.S_Area_ZH_46_3_502.sumValue }}</p>
                  <p>{{ steamTagList.S_Area_ZH_46_3_502.flowValue }}</p>
                  <p>{{ steamTagList.S_Area_ZH_46_3_502.SteamWD }}°C</p>
                </div>
              </div>
              <div class="steamTagLabel" style="left:210px;top: 170px;min-width: 110px;width: 110px;">
                <div class="steamTagTitle" style="line-height: 22px;">提取双号DN150</div>
                <div class="steamTagValue">
                  <p>{{ steamTagList.S_Area_ZH_22_1_502.sumValue }}</p>
                  <p>{{ steamTagList.S_Area_ZH_22_1_502.flowValue }}</p>
                  <p>{{ steamTagList.S_Area_ZH_22_1_502.SteamWD }}°C</p>
                </div>
              </div>
              <div class="steamTagLabel" style="left:170px;top: 288px;min-width: 95px;width: 95px;">
                <div class="steamTagTitle" style="line-height: 22px;">提取单号DN150</div>
                <div class="steamTagValue">
                  <p>{{ steamTagList.S_Area_ZH_21_3_502.sumValue }}</p>
                  <p>{{ steamTagList.S_Area_ZH_21_3_502.flowValue }}</p>
                  <p>{{ steamTagList.S_Area_ZH_21_3_502.SteamWD }}°C</p>
                </div>
              </div>
            </div>
            <div v-if="areaOverallDialogTitle === '新建综合制剂车间'">
              <div class="steamTagLabel" style="left:20px;top: 300px;">
                <div class="steamTagTitle">新制剂分汽缸DN200</div>
                <div class="steamTagValue">
                  <p>{{ steamTagList.S_Area_XJZ_13_1_7_502.sumValue }}</p>
                  <p>{{ steamTagList.S_Area_XJZ_13_1_7_502.flowValue }}</p>
                  <p>{{ steamTagList.S_Area_XJZ_13_1_7_502.SteamWD }}°C</p>
                </div>
              </div>
            </div>
            <div v-if="areaOverallDialogTitle === '固体制剂车间'">
              <div class="steamTagLabel" style="left:20px;top: 320px;">
                <div class="steamTagTitle">固体分汽缸流量计DN100</div>
                <div class="steamTagValue">
                  <p>{{ steamTagList.S_Area_GT_31_1_502.sumValue }}</p>
                  <p>{{ steamTagList.S_Area_GT_31_1_502.flowValue }}</p>
                  <p>{{ steamTagList.S_Area_GT_31_1_502.SteamWD }}°C</p>
                </div>
              </div>
            </div>
          </div>
          <div slot="footer" class="dialog-footer">
            <el-button @click="areaOverallDialog = false">关 闭</el-button>
          </div>
        </el-dialog>
        <!-- 个人信息 -->
        <el-dialog title="个人信息" :visible.sync="dialogUserVisible">
          <el-form label-width="110px">
            <el-form-item label="名称：">{{ UserInfo.Name }}</el-form-item>
            <el-form-item label="工号：">{{ UserInfo.WorkNumber }}</el-form-item>
            <el-form-item label="所属厂区：">{{ UserInfo.FactoryName }}</el-form-item>
            <el-form-item label="所属部门：">{{ UserInfo.OrganizationName }}</el-form-item>
            <el-form-item label="创建人：">{{ UserInfo.Creater }}</el-form-item>
            <el-form-item label="创建时间：">{{ UserInfo.CreateTime }}</el-form-item>
            <el-form-item label="最近登录时间：">{{ UserInfo.LastLoginTime }}</el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogUserVisible = false">取 消</el-button>
          </div>
        </el-dialog>
      </el-header>
      <!-- 页面主体 -->
      <el-main style="clear: both;">
        <transition name="move" mode="out-in">
         <!--渲染子页面-->
          <router-view :key="$route.fullPath"></router-view>
       </transition>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
var moment = require('moment');
import screenfull from "screenfull"
export default {
  name: 'Index',
  data () {
    return {
      selfHeight:{ //自适应高度
        height:''
      },
      isCollapse: false, //左侧菜单栏是否缩进了
      sideIcon:'el-icon-arrow-left', //左侧菜单栏缩进点击切换图标
      isClickElseMenu:false,
      AreaArr:[],
      time:"",  //实时显示当前的时间
      dialogUserVisible:false, //是否弹出个人信息
      isactive:"0", //主菜单选中索引值
      defaultActiveUrl:"",
      mainMenuList:[ //主菜单导航列表
        {text:"能源管理"},
        {text:"系统管理"}
      ],
      subMenulist:[], //子菜单导航列表
      energyMenulist:[
        {name: "桓仁厂区", icon: "el-icon-location-outline", children:[]},
        {name: "能效分析", icon: "el-icon-data-analysis", url: "/EfficiencyAnalysis"},
        {name: "综合报表", icon: "el-icon-document", url: "/DataReport"},
        {name: "批次维护表", icon: "el-icon-set-up", url: "/MaintainedBatch"},
        {name: "基础维护表", icon: "el-icon-s-operation", url: "/MaintainedBoard"},
      ],
      systemMenulist:[
        {name:"组织架构",icon:"el-icon-office-building",url:"/Organization"},
        {name:"角色管理",icon:"el-icon-s-check",url:"/Role"},
        {name:"人员管理",icon:"el-icon-user",url:"/Personnel"},
        {name:"工厂日历",icon:"el-icon-date",url:"/Calendar"},
        {name:"调度维护",icon:"el-icon-suitcase",url:"/SchedulingRules"},
        {name:"系统日志",icon:"el-icon-notebook-1",url:"/Log"}
      ],
      isFullScreen:false, //是否全屏
      weatherDesc:"",
      weatherType:"",
      weatherIcon:"",
      areaObj:{
        areaName:""
      },
      UserInfo:{},
      drawer: false,
      drawerAreaOption:[
        {title:"污水站",top:"32%",left:"25%",hasElectric:true,hasWater:true,hasSteam:false},
        {title:"锅炉房",top:"31%",left:"35%",img:require("@/assets/imgs/guolu.jpg"),hasElectric:true,hasWater:false,hasSteam:true},
        {title:"提取二车间",top:"34%",left:"35%",img:require("@/assets/imgs/tiquer.jpg"),img2:require("@/assets/imgs/tiquer2.jpg"),hasElectric:true,hasWater:true,hasSteam:true},
        {title:"综合车间",top:"40%",left:"35%",img:require("@/assets/imgs/zonghe.jpg"),hasElectric:true,hasWater:true,hasSteam:true},
        {title:"新建综合制剂车间",top:"32%",left:"47%",img:require("@/assets/imgs/xinzhiji.jpg"),hasElectric:true,hasWater:true,hasSteam:true},
        {title:"变电所",top:"40%",left:"48%",hasElectric:true,hasWater:false,hasSteam:false},
        {title:"中试车间",top:"30%",left:"56%",hasElectric:true,hasWater:true,hasSteam:true},
        {title:"智能库",top:"27%",left:"52%",hasElectric:true,hasWater:false,hasSteam:false},
        {title:"原提取车间",top:"31%",left:"62%",hasElectric:true,hasWater:true,hasSteam:true},
        {title:"前处理车间",top:"34%",left:"68%",hasElectric:true,hasWater:true,hasSteam:true},
        {title:"GMP车间",top:"38%",left:"61%",hasElectric:true,hasWater:true,hasSteam:true},
        {title:"固体制剂车间",top:"43%",left:"61%",img:require("@/assets/imgs/gutizhiji.jpg"),hasElectric:true,hasWater:true,hasSteam:true},
        {title:"展览室",top:"60%",left:"17%"},
        {title:"办公楼＼食堂",top:"57%",left:"28%",hasElectric:true,hasWater:true,hasSteam:true},
      ],
      waterAreaDialog:false,
      waterAreaTagDialog:false,
      electricAreaTagDialog:false,
      steamAreaTagDialog:false,
      electricAreaDialog:false,
      areaOverallDialog:false,
      areaOverallDialogTitle:"",
      areaOverallDialogSrc:"",
      areaOverallDialogSrc2:"",
      electricTagList:{},
      steamTagList:{},
      waterTagList:{},
      steamGlTag:"",
      websock:null,
      glfEqStuInfo:"", //锅炉房采集状态
    }
  },
  //依赖注入传值
  provide(){
    return{
      newAreaName:this.areaObj
    }
  },
  mounted(){
    let _this = this
    this.timer = setInterval(() =>{
      _this.time = moment(new Date()).format('YYYY-MM-DD HH:mm:ss');
    },1000);
    if(this.$route.meta.title === "系统管理"){  //判断是否是属于系统管理模块，展示系统模块菜单
      this.isactive = 1
    }
    this.clickMainMenu(this.isactive)
    this.defaultActiveUrl = this.$route.path //将菜单激活项设置为当前页面地址
  },
  created(){
    window.addEventListener('resize', this.getMenuHeight);
    this.getMenuHeight()
    this.getAreaSubMenu()
    if(sessionStorage.getItem("LoginStatus")) {
      this.$store.commit('setUser',sessionStorage.getItem('WorkNumber'))
      this.axios.get("/api/CUID",{
        params: {
          tableName: "User",
          field:"WorkNumber",
          fieldvalue:sessionStorage.getItem('WorkNumber'),
          limit:1,
          offset:0
        }
      }).then(res =>{
        var data = JSON.parse(res.data)
        this.UserInfo =  data.rows[0]
      })
    }else{
      this.$router.push("/login");
    }
    this.getWeather()
    this.getStu_Equ()
  },
  destroyed() {
    if(this.websock){
      this.websock.close() //离开路由之后断开websocket连接
    }
  },
  watch:{
    glfEqStuInfo(newval,oldval){
      if(newval === "NO"){
        $(".eq_stuIcon").addClass("blink")
        $(".eq_stuIcon").addClass("text-color-warning").removeClass("text-color-success")
      }else if(newval === "OK"){
        $(".eq_stuIcon").removeClass("blink")
        $(".eq_stuIcon").removeClass("text-color-warning").addClass("text-color-success")
      }
    },
  },
  methods:{
    getMenuHeight(){
      this.selfHeight.height = window.innerHeight - 230+'px';
    },
    clickSubMenu(areaName){  //点击左菜单传区域给子组件
      this.areaObj.areaName = areaName
    },
    handleCommand(command) {  //判断用户下拉点击
      if(command == "a"){
        this.dialogUserVisible = true
      }else if(command == "b"){
        this.$store.commit('removeUser')
        this.$router.replace("/login")
      }
    },
    iconToggle() {  //折叠菜单
      this.isCollapse = !this.isCollapse
      if(this.isCollapse){
        this.sideIcon = 'el-icon-arrow-right'
        $(".left-aside").animate({"width":"64px"})
      }else{
        this.sideIcon = 'el-icon-arrow-left'
        $(".left-aside").animate({"width":"180px"})
      }
    },
    clickMainMenu(index){  //切换模块
      this.isactive = index
      if(index == 0) {
        this.subMenulist = this.energyMenulist
        if(this.isClickElseMenu){
          this.defaultActiveUrl = this.subMenulist[0].children[0].url
        }
      }else if(index == 1){
        this.subMenulist = this.systemMenulist
        this.defaultActiveUrl = this.subMenulist[0].url
      }
    },
    getAreaSubMenu(){ //获取车间加入子菜单
      var params = {
        tableName: "AreaTable",
        limit:1000,
        offset:0
      }
      this.axios.get("/api/CUID",{params:params}).then(res =>{
        var resData = JSON.parse(res.data).rows
        this.AreaArr.push({
          name:"整厂区",
          url:"/Areas?areaName=整厂区"
        })
        for(var i=0;i < resData.length;i++){
          this.AreaArr.push({
            name:resData[i].AreaName,
            url:"/Areas?areaName=" + resData[i].AreaName
          })
        }
        this.energyMenulist[0].children = this.AreaArr
        this.isClickElseMenu = true
      },res =>{
        console.log("获取车间时请求错误")
      })
    },
    getFullCreeen () {  //全屏
      if (screenfull.isEnabled) {
        screenfull.toggle()
        if(screenfull.isFullscreen){
          this.isFullScreen = false
        }else{
          this.isFullScreen = true
        }
      }
    },
    getStu_Equ(){  //获取锅炉房采集状态
      let _this = this
      this.axios.get("/api/selectSteamTotalReminder").then(res =>{
        _this.glfEqStuInfo = res.data
      },res =>{
        console.log("获取锅炉房采集状态时请求错误")
      })
      this.timer = setInterval(() =>{
        this.axios.get("/api/selectSteamTotalReminder").then(res =>{
          _this.glfEqStuInfo = res.data
        },res =>{
          console.log("获取锅炉房采集状态时请求错误")
        })
      },1000*60*10);
    },
    getWeather(){
      this.axios.get("http://wthrcdn.etouch.cn/weather_mini",{
        params: {
          city: "本溪",
        }
      }).then(res =>{
        var weatherType = res.data.data.forecast[0].type
        var wendu = res.data.data.wendu
        this.weatherType = weatherType +"："+ wendu + "°C"
        this.weatherDesc = res.data.desc
        if(weatherType === "晴"){
          this.weatherIcon = "el-icon-sunny"
        }else if(weatherType === "多云"){
          this.weatherIcon = "el-icon-cloudy"
        }else if(weatherType === "阴"){
          this.weatherIcon = "el-icon-cloudy"
        }else if(weatherType === "阵雨"){
          this.weatherIcon = "el-icon-lightning"
        }else if(weatherType === "小雨"){
          this.weatherIcon = "el-icon-light-rain"
        }else if(weatherType === "暴雨"){
          this.weatherIcon = "el-icon-heavy-rain"
        }else if(weatherType === "阵雪"){
          this.weatherIcon = "fa fa-snowflake-o"
        }else if(weatherType === "大雪"){
          this.weatherIcon = "fa fa-snowflake-o"
        }
      })
    },
    scattergram(){
      this.drawer = true
      this.getGlSteamLabel()
      this.initWebSocket()
    },
    showAreaElectric(AreaName){
      this.electricAreaTagDialog = true
      this.areaOverallDialogTitle = AreaName
    },
    showAreaWater(AreaName){
      this.waterAreaTagDialog = true
      this.areaOverallDialogTitle = AreaName
    },
    showAreaSteam(AreaName,img,img2){
      if(img){
        if(img2){
          this.areaOverallDialog = true
          this.areaOverallDialogTitle = AreaName
          this.areaOverallDialogSrc = img
          this.areaOverallDialogSrc2 = img2
        }else{
          this.areaOverallDialog = true
          this.areaOverallDialogTitle = AreaName
          this.areaOverallDialogSrc = img
          this.areaOverallDialogSrc2 = ""
        }
      }else{
        this.steamAreaTagDialog = true
        this.areaOverallDialogTitle = AreaName
      }
    },
    getGlSteamLabel(){
      this.axios.get("/api/steamtotal").then(res =>{
        this.steamGlTag = res.data.S_AllArea_Value
      })
    },
    lookWaterMap(){
      this.waterAreaDialog = true
    },
    lookElectricMap(){
      this.electricAreaDialog = true
    },
    initWebSocket(){ //初始化weosocket
      this.websock = new WebSocket('ws://' + location.host + '/socket');
      // this.websock = new WebSocket('ws://127.0.0.1:5002');
      this.websock.onmessage = this.websocketonmessage;
      this.websock.onopen = this.websocketonopen;
      this.websock.onerror = this.websocketonerror;
      this.websock.onclose = this.websocketclose;
    },
    websocketonopen(){ //连接建立之后执行send方法发送数据
      this.websocketsend();
    },
    websocketonerror(){//连接建立失败重连
      console.log("websocket连接失败")
    },
    websocketonmessage(e){ //数据接收
      var resdata = JSON.parse(e.data);
      this.electricTagList = resdata[0].electric
      this.steamTagList = resdata[0].steam
      this.waterTagList = resdata[0].water
    },
    websocketsend(Data){//数据发送
      this.websock.send(Data);
    },
    websocketclose(e){  //关闭
      console.log("websocket关闭")
    },
    closesocket(){
      this.websock.close()
    }
  }
}
</script>
<style>
  .el-container,.el-aside,.el-aside .el-row,.el-aside .el-row .el-col{
    position: relative;
    height: 100%;
  }
  .el-header{
    overflow: hidden;
  }
  .body-container{
    background: #EEEEEE;
  }
  .left-aside{
    background: #082F4C;
  }
  .aside-head{
    width: 100%;
    padding: 50px 0 30px;
  }
  .aside-head a{
    color: #fff;
  }
  .aside-foot{
    height:110px;
    width: 100%;
    text-align: center;
    font-size: 18px;
    padding-top: 20px;
  }
  .aside-menu{
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .menu-ul{
    border: none;
    clear: both;
    overflow: auto;
    scrollbar-width: none;
    -ms-overflow-style: none;
  }
  .menu-ul::-webkit-scrollbar {
    display: none;
  }
  .el-menu-item .fa {
    margin-right: 5px;
    width: 24px;
    text-align: center;
    font-size: 18px;
    vertical-align: middle;
  }
  .version-number{
    margin-top: 20px;
    color: #737373;
  }
  .head-left-menu,.head-right-menu{
    height: 60px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .head-left-menu{
    float: left;
  }
  .head-left-menu i{
    font-size: 24px;
  }
  .head-right-menu{
    float: right;
  }
  .head-left-menu li{
    display: inline-block;
    margin-right: 30px;
    color: #082F4C;
    font-size: 20px;
  }
  .head-left-menu li i{
    vertical-align: bottom;
  }
  .head-right-menu li{
    float: left;
    margin-right: 15px;
    color: #082F4C;
    font-size: 16px;
    text-decoration: none;
    display: block;
    padding: 8px 15px;
    background-color: #EEEEEE;
    border-radius: 8px;
    cursor: pointer;
  }
  .head-right-menu li.active{
    background-color: #082F4C;
    color: #fff;
  }
  .head-menu-item{
    cursor:pointer;
  }
  .el-dropdown-menu {
    text-align: center;
  }
  .el-badge.item{
    margin-right: 15px;
  }
  .drawerContent{
    position: relative;
    width: 100%;
    min-height: 1000px;
    background: url("../assets/imgs/loginBg.jpg") no-repeat;
    background-size: 100% 100%;
    -webkit-background-size: 100% 100%;
    -o-background-size: 100% 100%;
    display: flex;
    align-items:center;
  }
  .drawerMaskBg{
    position: absolute;
    top: 0;
    width: 100%;
    height: 100%;
    background: #082F4C;
    opacity: 0;
  }
  .close-drawer{
    position: absolute;
    top: 20px;
    right: 20px;
    cursor: pointer;
  }
  .mapContent{
    position: absolute;
    height: 100%;
    width: 100%;
  }
  .mapContentItem{
    position: absolute;
    border: none;
    display: flex;
    align-items:center;
    width: 80px;
    height: 30px;
  }
  .mapItemPoint{
    display: inline-block;
    margin-top: 15%;
    margin-left: 10px;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    transition: box-shadow 0.6s, transform 0.5s;
  }
  .mapContentItem .ElectricPoint{
    background: #FB8A06;
    box-shadow: 0 0 2px 2px #FB8A06;
  }
  .mapContentItem .ElectricPoint:hover{
    box-shadow: 0 0 10px 10px #FB8A06;
	  transition: box-shadow 0.5s;
  }
  .mapContentItem .WaterPoint{
    background: #228AD5;
    box-shadow: 0 0 2px 2px #228AD5;
  }
  .mapContentItem .WaterPoint:hover{
    box-shadow: 0 0 10px 10px #228AD5;
	  transition: box-shadow 0.5s;
  }
  .mapContentItem .SteamPoint{
    background: #15CC48;
    box-shadow: 0 0 2px 2px #15CC48;
  }
  .mapContentItem .SteamPoint:hover{
    box-shadow: 0 0 10px 10px #15CC48;
	  transition: box-shadow 0.5s;
  }
  .steamTagLabel{
    position: absolute;
    padding: 5px 10px 2px;
    background: #fff;
    border: 1px solid #e1e1e1;
    border-radius: 4px;
    min-width: 235px;
  }
  .steamTagTitle{
    float: left;
    padding-right: 15px;
    line-height: 64px;
  }
  .steamTagValue p{
    background: #333333;
    padding: 0 5px;
    color: #15CC48;
    margin-bottom: 3px;
    white-space: nowrap;
    float: right;
  }
  .useAreaCard{
    position: relative;
    background: #EFF5FB;
    min-height: 120px;
  }
  .waterTagData{
    position: absolute;
    display: inline-block;
    padding: 5px;
    font-size: 12px;
    border:1px solid #e1e1e1;
    background: #ffffff;
  }
  .waterTagData .TagDataVal{
    background: #333333;
    padding: 0 5px;
    color: #15CC48;
    margin-top: 3px;
    white-space: nowrap;
  }
  .blink{
    -webkit-animation: twinkling 1s infinite ease-in-out;
  }
  @-webkit-keyframes twinkling{    /*透明度由0到1*/
    0%{
      opacity:1; /*透明度为0*/
    }
    50%{
      opacity:0; /*透明度为1*/
    }
    100%{
      opacity:1; /*透明度为1*/
    }
   }
  .areaTotalTagUl{
    overflow: hidden;
    overflow-x: auto;
    white-space: nowrap;
  }
  .areaTotalTagUl li{
    position: relative;
    width: 150px;
    display: inline-block;
    margin-right: 20px;
    vertical-align: top;
  }
  .areaTotalTagUl li p{
    white-space: nowrap;
  }
  .areaTotalTagUl .TagLine{
    width: 1px;
    height: 30px;
    margin: 0 auto;
    background: #e1e1e1;
  }
  .electricTagData{
    background: #333333;
    padding: 0 5px;
    color: #15CC48;
    margin-bottom: 3px;
    white-space: nowrap;
  }
</style>
