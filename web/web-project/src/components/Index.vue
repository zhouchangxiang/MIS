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
            <div style="position: absolute;top: 50px;left: 100px;z-index:1;">
              <div style="display: inline-block;width: 15px;height: 15px;border-radius: 50%;background: #FB8A06;margin-left: 10px;cursor: pointer;" @click="electricAreaDialog = true"></div> 电
              <div style="display: inline-block;width: 15px;height: 15px;border-radius: 50%;background: #228AD5;margin-left: 10px;cursor: pointer;" @click="waterAreaDialog = true"></div> 水
              <div style="display: inline-block;width: 15px;height: 15px;border-radius: 50%;background: #15CC48;margin-left: 10px;cursor: pointer;" @click="steamAreaDialog = true"></div> 汽
            </div>
            <div class="mapContent" v-if="JSON.stringify(steamTagList) != '{}'">
              <div style="position: relative;height: 100%;">
                <div v-for="(item,index) in drawerAreaOption" class="mapContentItem"
                     :style="{top: item.top,left: item.left}" :key="index">
                  <div>
                    <div class="mapItemPoint ElectricPoint" :title="item.title+' 电表'" v-if="item.hasElectric" @click="showAreaElectric(item.title)"></div>
                    <div class="mapItemPoint WaterPoint" :title="item.title+' 水表'" v-if="item.hasWater" @click="showAreaWater(item.title)"></div>
                    <div class="mapItemPoint SteamPoint" :title="item.title+' 汽表'" v-if="item.hasSteam" @click="showAreaSteam(item.title,item.img,item.img2)"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-drawer>
        <!-- 水表全局采集分布图 -->
        <el-dialog title="水表全局采集分布（可鼠标拖动横向滚动进行查看）" :visible.sync="waterAreaDialog" width="75%" top="50px" :fullscreen="waterdialogfullscreen" v-if="waterAreaDialog">
          <el-col :span="24" style="margin-top:-30px;">
            <div style="position: absolute;right: 60px;top: 15px;">
              <span :class="waterdialogfullscreen?'el-icon-aim':'el-icon-full-screen'" class="text-size-big" style="float: right;margin-right: 20px" title="全屏" @click="waterdialogfullscreen?waterdialogfullscreen=false:waterdialogfullscreen=true"></span>
              <span :class="waterImgCollapse?'el-icon-arrow-up':'el-icon-arrow-down'" class="text-size-big" style="float: right;margin-right: 20px" title="折叠" @click="waterImgCollapse?waterImgCollapse=false:waterImgCollapse=true"></span>
            </div>
            <transition name="el-zoom-in-center">
              <div v-show="!waterImgCollapse">
                <div style="width: 100%;text-align: center">
                  <div style="display: inline-block;">
                    <el-image style="width:100px;" :src="printerImg" fit="scale-down"></el-image><p>打印机</p>
                  </div>
                  <div style="display:inline-block;position:relative;top: -50px;width: 100px;height: 1px;background: #a1a1a1;"></div>
                  <div style="display: inline-block;">
                    <el-image style="width:120px;" :src="computerImg" fit="scale-down"></el-image><p>电脑主机</p>
                  </div>
                  <div style="display:inline-block;position:relative;top: -50px;width: 100px;height: 1px;background: #a1a1a1;"></div>
                  <div style="display: inline-block;">
                    <el-image style="width:90px;" :src="UPSImg" fit="scale-down"></el-image><p>UPS电源</p>
                  </div>
                  <div class="TagLine"></div>
                </div>
                <div style="width: 100%;text-align: center">
                  <div style="display: inline-block;">
                    <el-image style="width:120px;" :src="interchangerImg" fit="scale-down"></el-image><p>总交换机</p>
                    <p>水表数量：16</p>
                    <p class="itemMarginBottom">水表总量：{{
                      (waterTagList.W_Area_WSZ_16_2_34.sumValue+
                      waterTagList.W_Area_TQR_17_2_8.sumValue+
                      waterTagList.W_Area_TQR_17_1_9.sumValue+
                      waterTagList.W_Area_ZH_23_2_13.sumValue+
                      waterTagList.W_Area_ZH_23_1_12.sumValue+
                      waterTagList.W_Area_XJZ_12_1_3.sumValue+
                      waterTagList.W_Area_XJZ_12_2_5.sumValue+
                      // waterTagList.W_Area_YF_26_1_15.sumValue+
                      waterTagList.W_Area_YTQ_39_1_30.sumValue+
                      waterTagList.W_Area_YTQ_39_2_30.sumValue+
                      waterTagList.W_Area_QCL_33_1_20.sumValue+
                      waterTagList.W_Area_QCL_33_2_20.sumValue+
                      waterTagList.W_Area_QCL_33_1_20.sumValue+
                      waterTagList.W_Area_QCL_33_2_20.sumValue+
                      waterTagList.W_Area_GT_30_2_18.sumValue+
                      waterTagList.W_Area_GT_30_1_19.sumValue+
                      waterTagList.W_Area_BGL_34_1_22.sumValue).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                </div>
              </div>
            </transition>
            <div style="width: 100%;height:1px;background:#a1a1a1;"></div>
            <el-col :span="24" style="overflow: hidden;position: relative;height: 2000px;">
              <ul class="areaTotalTagUl" @mousedown="move" data-move>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image>
                    <p>污水站</p>
                    <p>水表数量：1</p>
                    <p class="itemMarginBottom">水表总量：{{
                      (waterTagList.W_Area_WSZ_16_2_34.sumValue).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>灌溉水DN40</span><p>{{ waterTagList.W_Area_WSZ_16_2_34.sumValue }}</p><p>{{ waterTagList.W_Area_WSZ_16_2_34.flowValue }}</p></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image>
                    <p>提取一车间</p>
                    <p>水表数量：2</p>
                    <p class="itemMarginBottom">水表总量：{{
                      (waterTagList.W_Area_TQR_17_2_8.sumValue +
                      waterTagList.W_Area_TQR_17_1_9.sumValue).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>后走廊灌溉水DN40</span><p>{{ waterTagList.W_Area_TQR_17_2_8.sumValue }}</p><p>{{ waterTagList.W_Area_TQR_17_2_8.flowValue }}</p></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>出料电梯旁饮用水DN100</span><p>{{ waterTagList.W_Area_TQR_17_1_9.sumValue }}</p><p>{{ waterTagList.W_Area_TQR_17_1_9.flowValue }}</p></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image>
                    <p>提取二车间</p>
                    <p>水表数量：2</p>
                    <p class="itemMarginBottom">水表总量：{{
                      (waterTagList.W_Area_ZH_23_2_13.sumValue +
                      waterTagList.W_Area_ZH_23_1_12.sumValue).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>带干辅机灌溉水DN40</span><p>{{ waterTagList.W_Area_ZH_23_2_13.sumValue }}</p><p>{{ waterTagList.W_Area_ZH_23_2_13.flowValue }}</p></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>2楼会议室饮用水DN150</span><p>{{ waterTagList.W_Area_ZH_23_1_12.sumValue }}</p><p>{{ waterTagList.W_Area_ZH_23_1_12.flowValue }}</p></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image>
                    <p>提取三车间</p>
                    <p>水表数量：2</p>
                    <p class="itemMarginBottom">水表总量：{{
                      (waterTagList.W_Area_YTQ_39_1_30.sumValue+
                      waterTagList.W_Area_YTQ_39_2_30.sumValue).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>消防水DN50</span><p>{{ waterTagList.W_Area_YTQ_39_1_30.sumValue }}</p><p>{{ waterTagList.W_Area_YTQ_39_1_30.flowValue }}</p></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>灌溉水DN40</span><p>{{ waterTagList.W_Area_YTQ_39_2_30.sumValue }}</p><p>{{ waterTagList.W_Area_YTQ_39_2_30.flowValue }}</p></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image>
                    <p>制剂一车间</p>
                    <p>水表数量：2</p>
                    <p class="itemMarginBottom">水表总量：{{
                      (waterTagList.W_Area_GT_30_2_18.sumValue+
                      waterTagList.W_Area_GT_30_1_19.sumValue).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>男卫生间灌溉水DN40</span><p>{{ waterTagList.W_Area_GT_30_2_18.sumValue }}</p><p>{{ waterTagList.W_Area_GT_30_2_18.flowValue }}</p></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>纯化水站饮用水DN100</span><p>{{ waterTagList.W_Area_GT_30_1_19.sumValue }}</p><p>{{ waterTagList.W_Area_GT_30_1_19.flowValue }}</p></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image>
                    <p>制剂二车间</p>
                    <p>水表数量：2</p>
                    <p class="itemMarginBottom">水表总量：{{
                      (waterTagList.W_Area_XJZ_12_1_3.sumValue +
                      waterTagList.W_Area_XJZ_12_2_5.sumValue).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>包材库灌溉水DN50</span><p>{{ waterTagList.W_Area_XJZ_12_1_3.sumValue }}</p><p>{{ waterTagList.W_Area_XJZ_12_1_3.flowValue }}</p></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>接待室饮用水DN100</span><p>{{ waterTagList.W_Area_XJZ_12_2_5.sumValue }}</p><p>{{ waterTagList.W_Area_XJZ_12_2_5.flowValue }}</p></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image>
                    <p>制剂三车间</p>
                    <p>水表数量：2</p>
                    <p class="itemMarginBottom">水表总量：{{
                      (waterTagList.W_Area_QCL_33_1_20.sumValue+
                      waterTagList.W_Area_QCL_33_2_20.sumValue).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>消防水DN50</span><p>{{ waterTagList.W_Area_JK_28_1_16.sumValue }}</p><p>{{ waterTagList.W_Area_JK_28_1_16.flowValue }}</p></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>消防水DN50</span><p>{{ waterTagList.W_Area_JK_28_2_16.sumValue }}</p><p>{{ waterTagList.W_Area_JK_28_2_16.flowValue }}</p></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image>
                    <p>前处理车间</p>
                    <p>水表数量：2</p>
                    <p class="itemMarginBottom">水表总量：{{
                      (waterTagList.W_Area_QCL_33_1_20.sumValue+
                      waterTagList.W_Area_QCL_33_2_20.sumValue).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>洗药室灌溉水DN25</span><p>{{ waterTagList.W_Area_QCL_33_1_20.sumValue }}</p><p>{{ waterTagList.W_Area_QCL_33_1_20.flowValue }}</p></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>饮用水DN25</span><p>{{ waterTagList.W_Area_QCL_33_2_20.sumValue }}</p><p>{{ waterTagList.W_Area_QCL_33_2_20.flowValue }}</p></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image>
                    <p>行政办公楼</p>
                    <p>水表数量：1</p>
                    <p class="itemMarginBottom">水表总量：{{
                      (waterTagList.W_Area_BGL_34_1_22.sumValue).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>1楼卫生间深井水DN65</span><p>{{ waterTagList.W_Area_BGL_34_1_22.sumValue }}</p><p>{{ waterTagList.W_Area_BGL_34_1_22.flowValue }}</p></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image>
                    <p>检验中心</p>
                    <p>水表数量：0</p>
                    <!--<p class="itemMarginBottom">水表总量：{{-->
                      <!--(waterTagList.W_Area_YF_26_1_15.sumValue).toFixed(2)-->
                      <!--}}-->
                    <!--</p>-->
                  </div>
                  <!--<div class="TagLine"></div>-->
                  <!--<div class="electricTagData"><span>消防水DN100</span><p>{{ waterTagList.W_Area_YF_26_1_15.sumValue }}</p><p>{{ waterTagList.W_Area_YF_26_1_15.flowValue }}</p></div>-->
                </li>
              </ul>
            </el-col>
          </el-col>
          <div slot="footer" class="dialog-footer">
            <el-button @click="waterAreaDialog = false">关闭</el-button>
          </div>
        </el-dialog>
        <!-- 电表全局采集分布图 -->
        <el-dialog title="电表全局采集分布（可鼠标拖动横向滚动进行查看）" :visible.sync="electricAreaDialog" width="90%" top="50px" :fullscreen="electricdialogfullscreen" v-if="electricAreaDialog">
          <el-col :span="24" style="margin-top:-30px;">
            <div style="position: absolute;right: 60px;top: 15px;">
              <span :class="electricdialogfullscreen?'el-icon-aim':'el-icon-full-screen'" class="text-size-big" style="float: right;margin-right: 20px" title="全屏" @click="electricdialogfullscreen?electricdialogfullscreen=false:electricdialogfullscreen=true"></span>
              <span :class="electricImgCollapse?'el-icon-arrow-up':'el-icon-arrow-down'" class="text-size-big" style="float: right;margin-right: 20px" title="折叠" @click="electricImgCollapse?electricImgCollapse=false:electricImgCollapse=true"></span>
            </div>
            <transition name="el-zoom-in-center">
              <div v-show="!electricImgCollapse">
                <div style="width: 100%;text-align: center">
                  <div style="display: inline-block;">
                    <el-image style="width:100px;" :src="printerImg" fit="scale-down"></el-image><p>打印机</p>
                  </div>
                  <div style="display:inline-block;position:relative;top: -50px;width: 100px;height: 1px;background: #a1a1a1;"></div>
                  <div style="display: inline-block;">
                    <el-image style="width:120px;" :src="computerImg" fit="scale-down"></el-image><p>电脑主机</p>
                  </div>
                  <div style="display:inline-block;position:relative;top: -50px;width: 100px;height: 1px;background: #a1a1a1;"></div>
                  <div style="display: inline-block;">
                    <el-image style="width:90px;" :src="UPSImg" fit="scale-down"></el-image><p>UPS电源</p>
                  </div>
                  <div class="TagLine"></div>
                </div>
                <div style="width: 100%;text-align: center">
                  <div style="display: inline-block;">
                    <el-image style="width:120px;" :src="interchangerImg" fit="scale-down"></el-image><p>总交换机</p>
                    <p>电表数量：48</p>
                    <p class="itemMarginBottom">总功率：{{
                      (electricTagList.E_Area_WSZ_16_2_35.ZGL +
                      electricTagList.E_Area_GLF_42_1_33_1.ZGL +
                      electricTagList.E_Area_GLF_42_1_33_2.ZGL +
                      electricTagList.E_Area_GLF_42_1_33_3.ZGL +
                      electricTagList.E_Area_TQR_18_2_36_1.ZGL +
                      electricTagList.E_Area_TQR_18_2_36_2.ZGL +
                      electricTagList.E_Area_TQR_18_2_36_3.ZGL +
                      electricTagList.E_Area_TQR_18_2_36_4.ZGL +
                      electricTagList.E_Area_ZH_1.ZGL +
                      electricTagList.E_Area_ZH_2.ZGL +
                      electricTagList.E_Area_ZH_50_1_41_1.ZGL +
                      electricTagList.E_Area_ZH_50_1_41_2.ZGL +
                      electricTagList.E_Area_ZH_50_1_41_3.ZGL +
                      electricTagList.E_Area_ZH_50_1_41_4.ZGL +
                      electricTagList.E_Area_ZH_50_1_41_5.ZGL +
                      electricTagList.E_Area_ZH_50_1_41_6.ZGL +
                      electricTagList.E_Area_XJZ_11_2_7.ZGL +
                      electricTagList.E_Area_XJZ_11_2_7_1.ZGL +
                      electricTagList.E_Area_XJZ_11_2_7_3.ZGL +
                      electricTagList.E_Area_XJZ_11_2_7_4.ZGL +
                      electricTagList.E_Area_XJZ_11_1_6_5.ZGL +
                      electricTagList.E_Area_XJZ_11_1_6_6.ZGL +
                      electricTagList.E_Area_BDS_49_1_39_1.ZGL +
                      electricTagList.E_Area_BDS_49_1_39_2.ZGL +
                      electricTagList.E_Area_BDS_49_1_39_3.ZGL +
                      electricTagList.E_Area_BDS_49_1_39_4.ZGL +
                      electricTagList.E_Area_BDS_49_2_40_5.ZGL +
                      electricTagList.E_Area_BDS_49_2_40_6.ZGL +
                      electricTagList.E_Area_BDS_49_2_40_7.ZGL +
                      electricTagList.E_Area_BDS_49_2_40_8.ZGL +
                      electricTagList.E_Area_BDS_49_2_40_9.ZGL +
                      electricTagList.E_Area_BDS_49_2_40_10.ZGL +
                      electricTagList.E_Area_BDS_49_2_40_11.ZGL +
                      electricTagList.E_Area_BDS_49_2_40_12.ZGL +
                      electricTagList.E_Area_YF_26_1_14.ZGL +
                      electricTagList.E_Area_YF_26_1_14_2.ZGL +
                      electricTagList.E_Area_ZNK_24_1_10_1.ZGL +
                      electricTagList.E_Area_YTQ_38_1_28.ZGL +
                      electricTagList.E_Area_YTQ_38_2_29.ZGL +
                      electricTagList.E_Area_YTQ_38_2_29_3.ZGL +
                      electricTagList.E_Area_YTQ_38_2_29_4.ZGL +
                      electricTagList.E_Area_JK_28_2_17.ZGL +
                      electricTagList.E_Area_JK_28_1_16.ZGL +
                      electricTagList.E_Area_GT_30_2_19.ZGL +
                      electricTagList.E_Area_GT_30_2_19_1.ZGL +
                      electricTagList.E_Area_GT_30_2_19_2.ZGL +
                      electricTagList.E_Area_GT_30_2_19_3.ZGL +
                      electricTagList.E_Area_BGL_36_1_26.ZGL).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                </div>
              </div>
            </transition>
            <div style="width: 100%;height:1px;background:#a1a1a1;"></div>
            <el-col :span="24" style="overflow: hidden;position: relative;height: 2000px;">
              <ul class="areaTotalTagUl" @mousedown="move" data-move>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image>
                    <p>污水站</p>
                    <p>电表数量：1</p>
                    <p class="itemMarginBottom">总功率：{{ (electricTagList.E_Area_WSZ_16_2_35.ZGL).toFixed(2) }}</p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>污水站1</span><p>{{ electricTagList.E_Area_WSZ_16_2_35.ZGL }}</p><span>罗茨风机 电解格栅机 排泥泵 污水泵  配药装置</span></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image><p>锅炉房</p>
                    <p>电表数量：3</p>
                    <p class="itemMarginBottom">总功率：{{
                      (electricTagList.E_Area_GLF_42_1_33_1.ZGL +
                      electricTagList.E_Area_GLF_42_1_33_2.ZGL +
                      electricTagList.E_Area_GLF_42_1_33_3.ZGL).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>锅炉房1号表</span><p>{{ electricTagList.E_Area_GLF_42_1_33_1.ZGL }}</p><span>锅炉</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>锅炉房2号表</span><p>{{ electricTagList.E_Area_GLF_42_1_33_2.ZGL }}</p><span>供暖系统</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>锅炉房3号表</span><p>{{ electricTagList.E_Area_GLF_42_1_33_3.ZGL }}</p><span>脱硫环保系统</span></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image><p>提取一车间</p>
                    <p>电表数量：4</p>
                    <p class="itemMarginBottom">总功率：{{
                      (electricTagList.E_Area_TQR_18_2_36_1.ZGL +
                      electricTagList.E_Area_TQR_18_2_36_2.ZGL +
                      electricTagList.E_Area_TQR_18_2_36_3.ZGL +
                      electricTagList.E_Area_TQR_18_2_36_4.ZGL).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>提取一车间空调室1号表</span><p>{{ electricTagList.E_Area_TQR_18_2_36_1.ZGL }}</p><span>室外冷水机组</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>提取一车间空调室2号表</span><p>{{ electricTagList.E_Area_TQR_18_2_36_2.ZGL }}</p><span>新空调机组</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>提取一车间电控室1号表</span><p>{{ electricTagList.E_Area_TQR_18_2_36_3.ZGL }}</p><span>一楼冷水机组</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>提取一车间电控室2号表</span><p>{{ electricTagList.E_Area_TQR_18_2_36_4.ZGL }}</p><span>流化床制粒机*3</span></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image><p>提取二车间</p>
                    <p>电表数量：8</p>
                    <p class="itemMarginBottom">总功率：{{
                      (electricTagList.E_Area_ZH_1.ZGL +
                      electricTagList.E_Area_ZH_2.ZGL +
                      electricTagList.E_Area_ZH_50_1_41_1.ZGL +
                      electricTagList.E_Area_ZH_50_1_41_2.ZGL +
                      electricTagList.E_Area_ZH_50_1_41_3.ZGL +
                      electricTagList.E_Area_ZH_50_1_41_4.ZGL +
                      electricTagList.E_Area_ZH_50_1_41_5.ZGL +
                      electricTagList.E_Area_ZH_50_1_41_6.ZGL).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>提取二车间</span><p>{{ electricTagList.E_Area_ZH_1.ZGL }}</p><span>MVR1号表</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>提取二车间</span><p>{{ electricTagList.E_Area_ZH_2.ZGL }}</p><span>MVR2号表</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>提取二车间一号表</span><p>{{ electricTagList.E_Area_ZH_50_1_41_1.ZGL }}</p><span>输液泵*10 粉糖机*2</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>提取二车间二号表</span><p>{{ electricTagList.E_Area_ZH_50_1_41_2.ZGL }}</p><span>流化床制粒机*3</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>提取二车间三号表</span><p>{{ electricTagList.E_Area_ZH_50_1_41_3.ZGL }}</p><span>120带干</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>提取二车间4号表</span><p>{{ electricTagList.E_Area_ZH_50_1_41_4.ZGL }}</p><span>真空泵*7  浓缩罐*5  洗衣房 混合机 提取自控系统  办公室</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>提取二车间5号表</span><p>{{ electricTagList.E_Area_ZH_50_1_41_5.ZGL }}</p><span>排风系统  空调</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>提取二车间6号表</span><p>{{ electricTagList.E_Area_ZH_50_1_41_6.ZGL }}</p><span>照明</span></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image><p>提取三车间</p>
                    <p>电表数量：1</p>
                    <p class="itemMarginBottom">总功率：{{
                      (electricTagList.E_Area_YTQ_38_1_28.ZGL).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>提取三车间</span><p>{{ electricTagList.E_Area_YTQ_38_1_28.ZGL }}</p><span>提取三车间电器设备</span></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image><p>制剂一车间</p>
                    <p>电表数量：4</p>
                    <p class="itemMarginBottom">总功率：{{
                      (electricTagList.E_Area_GT_30_2_19.ZGL +
                      electricTagList.E_Area_GT_30_2_19_1.ZGL +
                      electricTagList.E_Area_GT_30_2_19_2.ZGL +
                      electricTagList.E_Area_GT_30_2_19_3.ZGL).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>制剂一车间1号表</span><p>{{ electricTagList.E_Area_GT_30_2_19.ZGL }}</p><span>除尘系统 空调系统 水泵*4</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>制剂一车间2号表</span><p>{{ electricTagList.E_Area_GT_30_2_19_1.ZGL }}</p><span>办公室 保全班 压片机*4  胶囊机*2  混合机*2  包衣机*6  颗粒自动包装线  塑瓶包装线</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>制剂一车间3号表</span><p>{{ electricTagList.E_Area_GT_30_2_19_2.ZGL }}</p><span>冷水机组 除湿机*2 空压机</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>制剂一车间4号表</span><p>{{ electricTagList.E_Area_GT_30_2_19_3.ZGL }}</p><span>照明</span></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image><p>制剂二车间</p>
                    <p>电表数量：6</p>
                    <p class="itemMarginBottom">总功率：{{
                      (electricTagList.E_Area_XJZ_11_2_7.ZGL +
                      electricTagList.E_Area_XJZ_11_2_7_1.ZGL +
                      electricTagList.E_Area_XJZ_11_2_7_3.ZGL +
                      electricTagList.E_Area_XJZ_11_2_7_4.ZGL +
                      electricTagList.E_Area_XJZ_11_1_6_5.ZGL +
                      electricTagList.E_Area_XJZ_11_1_6_6.ZGL).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>制剂二车间二楼配电室</span><p>{{ electricTagList.E_Area_XJZ_11_2_7.ZGL }}</p><span>空压机 纯化水 空调 包衣机*3 除湿机 AK1 AK2 ESTUN</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>制剂二车间二楼配电室</span><p>{{ electricTagList.E_Area_XJZ_11_2_7_1.ZGL }}</p><span>干法制粒*4 配方颗粒包装 AP23 混合机 照明 墙插</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>制剂二车间二楼配电室</span><p>{{ electricTagList.E_Area_XJZ_11_2_7_3.ZGL }}</p><span>电梯 混合机 压片机*2 胶囊机*2 泡罩机*2 粉碎机 清洗机 转料提升机 流化床制粒机 照明</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>制剂二车间二楼配电室</span><p>{{ electricTagList.E_Area_XJZ_11_2_7_4.ZGL }}</p><span>二楼空调</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>制剂二车间一楼配电室1号表</span><p>{{ electricTagList.E_Area_XJZ_11_1_6_5.ZGL }}</p><span>冷水机组1号 洗衣房 照明 排风系统 </span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>制剂二车间一楼配电室2号表</span><p>{{ electricTagList.E_Area_XJZ_11_1_6_6.ZGL }}</p><span>冷水机组2号</span></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image><p>制剂三车间</p>
                    <p>电表数量：2</p>
                    <p class="itemMarginBottom">总功率：{{
                      (electricTagList.E_Area_JK_28_2_17.ZGL +
                      electricTagList.E_Area_JK_28_1_16.ZGL).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>制剂三车间1号表</span><p>{{ electricTagList.E_Area_JK_28_2_17.ZGL }}</p><span>1楼</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>制剂三车间2号表</span><p>{{ electricTagList.E_Area_JK_28_1_16.ZGL }}</p><span>2楼</span></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image><p>变电所</p>
                    <p>电表数量：12</p>
                    <p class="itemMarginBottom">总功率：{{
                      (electricTagList.E_Area_BDS_49_1_39_1.ZGL +
                      electricTagList.E_Area_BDS_49_1_39_2.ZGL +
                      electricTagList.E_Area_BDS_49_1_39_3.ZGL +
                      electricTagList.E_Area_BDS_49_1_39_4.ZGL +
                      electricTagList.E_Area_BDS_49_2_40_5.ZGL +
                      electricTagList.E_Area_BDS_49_2_40_6.ZGL +
                      electricTagList.E_Area_BDS_49_2_40_7.ZGL +
                      electricTagList.E_Area_BDS_49_2_40_8.ZGL +
                      electricTagList.E_Area_BDS_49_2_40_9.ZGL +
                      electricTagList.E_Area_BDS_49_2_40_10.ZGL +
                      electricTagList.E_Area_BDS_49_2_40_11.ZGL +
                      electricTagList.E_Area_BDS_49_2_40_12.ZGL).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>变电所1号表</span><p>{{ electricTagList.E_Area_BDS_49_1_39_1.ZGL }}</p><span>40喷干</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>变电所2号表</span><p>{{ electricTagList.E_Area_BDS_49_1_39_2.ZGL }}</p><span>50喷干</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>变电所3号表</span><p>{{ electricTagList.E_Area_BDS_49_1_39_3.ZGL }}</p><span>循环水泵</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>变电所4号表</span><p>{{ electricTagList.E_Area_BDS_49_1_39_4.ZGL }}</p><span>消防水泵 新大库</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>变电所5号表</span><p>{{ electricTagList.E_Area_BDS_49_2_40_5.ZGL }}</p><span>制剂3车间</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>变电所6号表</span><p>{{ electricTagList.E_Area_BDS_49_2_40_6.ZGL }}</p><span>前处理车间 老700粉碎机 生产部</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>变电所7号表</span><p>{{ electricTagList.E_Area_BDS_49_2_40_7.ZGL }}</p><span>仓储中心</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>变电所8号表</span><p>{{ electricTagList.E_Area_BDS_49_2_40_8.ZGL }}</p><span>提取一车间照明</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>变电所9号表</span><p>{{ electricTagList.E_Area_BDS_49_2_40_9.ZGL }}</p><span>提取一车间空调 40粉碎机</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>变电所10号表</span><p>{{ electricTagList.E_Area_BDS_49_2_40_10.ZGL }}</p><span>60带干 风机 提取一车间办公室</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>变电所11号表</span><p>{{ electricTagList.E_Area_BDS_49_2_40_11.ZGL }}</p><span>提取一车间自控系统</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>变电所12号表</span><p>{{ electricTagList.E_Area_BDS_49_2_40_12.ZGL }}</p><span>超微粉碎 灭菌柜*2</span></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image><p>检验中心</p>
                    <p>电表数量：2</p>
                    <p class="itemMarginBottom">总功率：{{
                      (electricTagList.E_Area_YF_26_1_14.ZGL +
                      electricTagList.E_Area_YF_26_1_14_2.ZGL).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>检验中心配电室1号表</span><p>{{ electricTagList.E_Area_YF_26_1_14.ZGL }}</p><span>检验中心所有电器设备</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>检验中心配电室2号表</span><p>{{ electricTagList.E_Area_YF_26_1_14_2.ZGL }}</p><span>老醇提水泵 大机修</span></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image><p>智能库房</p>
                    <p>电表数量：1</p>
                    <p class="itemMarginBottom">总功率：{{
                      (electricTagList.E_Area_ZNK_24_1_10_1.ZGL).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>智能库房</span><p>{{ electricTagList.E_Area_ZNK_24_1_10_1.ZGL }}</p><span>智能库房所有用电设备</span></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image><p>前处理车间</p>
                    <p>电表数量：3</p>
                    <p class="itemMarginBottom">总功率：{{
                      (electricTagList.E_Area_YTQ_38_2_29.ZGL +
                      electricTagList.E_Area_YTQ_38_2_29_3.ZGL +
                      electricTagList.E_Area_YTQ_38_2_29_4.ZGL).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>前处理车间1号表</span><p>{{ electricTagList.E_Area_YTQ_38_2_29.ZGL }}</p><span>机电车间办公室 新700 机修 备件库</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>前处理车间2号表</span><p>{{ electricTagList.E_Area_YTQ_38_2_29_3.ZGL }}</p><span>洗药机、切药机</span></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>前处理车间3号表</span><p>{{ electricTagList.E_Area_YTQ_38_2_29_4.ZGL }}</p><span>粉碎机</span></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image><p>行政办公楼</p>
                    <p>电表数量：1</p>
                    <p class="itemMarginBottom">总功率：{{
                      (electricTagList.E_Area_BGL_36_1_26.ZGL).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>展馆旁配电柜</span><p>{{ electricTagList.E_Area_BGL_36_1_26.ZGL }}</p></div><span>行政办公楼 食堂 宿舍 展馆 警卫室 冷库 库房</span>
                </li>
              </ul>
            </el-col>
          </el-col>
          <div slot="footer" class="dialog-footer">
            <el-button @click="electricAreaDialog = false">关闭</el-button>
          </div>
        </el-dialog>
        <!-- 汽表全局采集分布图 -->
        <el-dialog title="汽表全局采集分布（可鼠标拖动横向滚动进行查看）" :visible.sync="steamAreaDialog" width="90%" top="50px" :fullscreen="steamdialogfullscreen" v-if="steamAreaDialog">
          <el-col :span="24" style="margin-top:-30px;">
            <div style="position: absolute;right: 60px;top: 15px;">
              <span :class="steamdialogfullscreen?'el-icon-aim':'el-icon-full-screen'" class="text-size-big" style="float: right;margin-right: 20px" title="全屏" @click="steamdialogfullscreen?steamdialogfullscreen=false:steamdialogfullscreen=true"></span>
              <span :class="steamImgCollapse?'el-icon-arrow-up':'el-icon-arrow-down'" class="text-size-big" style="float: right;margin-right: 20px" title="折叠" @click="steamImgCollapse?steamImgCollapse=false:steamImgCollapse=true"></span>
            </div>
            <transition name="el-zoom-in-center">
              <div v-show="!steamImgCollapse">
                <div style="width: 100%;text-align: center">
                  <div style="display: inline-block;">
                    <el-image style="width:100px;" :src="printerImg" fit="scale-down"></el-image><p>打印机</p>
                  </div>
                  <div style="display:inline-block;position:relative;top: -50px;width: 100px;height: 1px;background: #a1a1a1;"></div>
                  <div style="display: inline-block;">
                    <el-image style="width:120px;" :src="computerImg" fit="scale-down"></el-image><p>电脑主机</p>
                  </div>
                  <div style="display:inline-block;position:relative;top: -50px;width: 100px;height: 1px;background: #a1a1a1;"></div>
                  <div style="display: inline-block;">
                    <el-image style="width:90px;" :src="UPSImg" fit="scale-down"></el-image><p>UPS电源</p>
                  </div>
                  <div class="TagLine"></div>
                </div>
                <div style="width: 100%;text-align: center">
                  <div style="display: inline-block;">
                    <el-image style="width:120px;" :src="interchangerImg" fit="scale-down"></el-image><p>总交换机</p>
                    <p>汽表数量：21</p>
                    <p class="itemMarginBottom">锅炉蒸汽总量：{{
                      (steamGlTag.sumValue).toFixed(2) +"t"
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                </div>
              </div>
            </transition>
            <div style="width: 100%;height:1px;background:#a1a1a1;"></div>
            <el-col :span="24" style="overflow: hidden;position: relative;height: 2000px;">
              <ul class="areaTotalTagUl" @mousedown="move" data-move>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image>
                    <p>锅炉房</p>
                    <p>汽表数量：1</p>
                    <p class="itemMarginBottom">蒸汽总量：{{
                      (steamTagList.S_Area_GLF_45_3_502.sumValue).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>供暖DN150</span><p>{{ steamTagList.S_Area_GLF_45_3_502.sumValue }}</p><p>{{ steamTagList.S_Area_GLF_45_3_502.SteamWD }}°C</p></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image>
                    <p>提取一车间</p>
                    <p>汽表数量：6</p>
                    <p class="itemMarginBottom">蒸汽总量：{{
                      (steamTagList.S_Area_TQR_20_1_502.sumValue +
                      steamTagList.S_Area_TQR_19_3_502.sumValue+
                      steamTagList.S_Area_TQR_20_2_502.sumValue+
                      steamTagList.S_Area_TQR_19_1_502.sumValue+
                      steamTagList.S_Area_TQR_19_2_502.sumValue+
                      steamTagList.S_Area_TQR_20_3_502.sumValue).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>一楼灭菌柜DN80</span><p>{{ steamTagList.S_Area_TQR_20_1_502.sumValue }}</p><p>{{ steamTagList.S_Area_TQR_20_1_502.SteamWD }}°C</p></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>单效/双效浓缩DN20</span><p>{{ steamTagList.S_Area_TQR_19_3_502.sumValue }}</p><p>{{ steamTagList.S_Area_TQR_19_3_502.SteamWD }}°C</p></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>喷干两台/CIP DN20</span><p>{{ steamTagList.S_Area_TQR_20_2_502.sumValue }}</p><p>{{ steamTagList.S_Area_TQR_20_2_502.SteamWD }}°C</p></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>提取单号DN150</span><p>{{ steamTagList.S_Area_TQR_19_1_502.sumValue }}</p><p>{{ steamTagList.S_Area_TQR_19_1_502.SteamWD }}°C</p></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>提取双号DN150</span><p>{{ steamTagList.S_Area_TQR_19_2_502.sumValue }}</p><p>{{ steamTagList.S_Area_TQR_19_2_502.SteamWD }}°C</p></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>管式灭菌DN80</span><p>{{ steamTagList.S_Area_TQR_20_3_502.sumValue }}</p><p>{{ steamTagList.S_Area_TQR_20_3_502.SteamWD }}°C</p></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image>
                    <p>提取二车间</p>
                    <p>汽表数量：7</p>
                    <p class="itemMarginBottom">蒸汽总量：{{
                      (steamTagList.S_Area_ZH_21_2_502.sumValue +
                      steamTagList.S_Area_ZH_21_1_502.sumValue+
                      steamTagList.S_Area_ZH_46_1_502.sumValue+
                      steamTagList.S_Area_ZH_46_2_502.sumValue+
                      steamTagList.S_Area_ZH_46_3_502.sumValue+
                      steamTagList.S_Area_ZH_22_1_502.sumValue+
                      steamTagList.S_Area_ZH_21_3_502.sumValue).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>120带干DN32</span><p>{{ steamTagList.S_Area_ZH_21_2_502.sumValue }}</p><p>{{ steamTagList.S_Area_ZH_21_2_502.SteamWD }}°C</p></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>流化床制粒DN50</span><p>{{ steamTagList.S_Area_ZH_21_1_502.sumValue }}</p><p>{{ steamTagList.S_Area_ZH_21_1_502.SteamWD }}°C</p></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>二次浓缩DN100</span><p>{{ steamTagList.S_Area_ZH_46_1_502.sumValue }}</p><p>{{ steamTagList.S_Area_ZH_46_1_502.SteamWD }}°C</p></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>醇提+浓缩DN150</span><p>{{ steamTagList.S_Area_ZH_46_2_502.sumValue }}</p><p>{{ steamTagList.S_Area_ZH_46_2_502.SteamWD }}°C</p></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>双效浓缩/CIP DN200</span><p>{{ steamTagList.S_Area_ZH_46_3_502.sumValue }}</p><p>{{ steamTagList.S_Area_ZH_46_3_502.SteamWD }}°C</p></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>提取双号DN150</span><p>{{ steamTagList.S_Area_ZH_22_1_502.sumValue }}</p><p>{{ steamTagList.S_Area_ZH_22_1_502.SteamWD }}°C</p></div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>提取单号DN150</span><p>{{ steamTagList.S_Area_ZH_21_3_502.sumValue }}</p><p>{{ steamTagList.S_Area_ZH_21_3_502.SteamWD }}°C</p></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image>
                    <p>提取三车间</p>
                    <p>汽表数量：1</p>
                    <p class="itemMarginBottom">蒸汽总量：{{
                      (steamTagList.S_Area_YTQ_40_1_502.sumValue ).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>提取三车间流量计</span><p>{{ steamTagList.S_Area_YTQ_40_1_502.sumValue }}</p><p>{{ steamTagList.S_Area_YTQ_40_1_502.SteamWD }}°C</p></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image>
                    <p>制剂一车间</p>
                    <p>汽表数量：1</p>
                    <p class="itemMarginBottom">蒸汽总量：{{
                      (steamTagList.S_Area_GT_31_1_502.sumValue ).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>制剂一车间</span><p>{{ steamTagList.S_Area_GT_31_1_502.sumValue }}</p><p>{{ steamTagList.S_Area_GT_31_1_502.SteamWD }}°C</p></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image>
                    <p>制剂二车间</p>
                    <p>汽表数量：1</p>
                    <p class="itemMarginBottom">蒸汽总量：{{
                      (steamTagList.S_Area_XJZ_13_1_7_502.sumValue ).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>制剂二车间</span><p>{{ steamTagList.S_Area_XJZ_13_1_7_502.sumValue }}</p><p>{{ steamTagList.S_Area_XJZ_13_1_7_502.SteamWD }}°C</p></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image>
                    <p>制剂三车间</p>
                    <p>汽表数量：1</p>
                    <p class="itemMarginBottom">蒸汽总量：{{
                      (steamTagList.S_Area_JK_27_1_502.sumValue ).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>制剂三车间</span><p>{{ steamTagList.S_Area_JK_27_1_502.sumValue }}</p><p>{{ steamTagList.S_Area_JK_27_1_502.SteamWD }}°C</p></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image>
                    <p>前处理车间</p>
                    <p>汽表数量：1</p>
                    <p class="itemMarginBottom">蒸汽总量：{{
                      (steamTagList.S_Area_YTQ_40_2_502.sumValue ).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>前处理车间流量计</span><p>{{ steamTagList.S_Area_YTQ_40_2_502.sumValue }}</p><p>{{ steamTagList.S_Area_YTQ_40_2_502.SteamWD }}°C</p></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image>
                    <p>行政办公楼</p>
                    <p>汽表数量：1</p>
                    <p class="itemMarginBottom">蒸汽总量：{{
                      (steamTagList.S_Area_BGL_35_1_502.sumValue ).toFixed(2)
                      }}
                    </p>
                  </div>
                  <div class="TagLine"></div>
                  <div class="electricTagData"><span>食堂热水罐</span><p>{{ steamTagList.S_Area_BGL_35_1_502.sumValue }}</p><p>{{ steamTagList.S_Area_BGL_35_1_502.SteamWD }}°C</p></div>
                </li>
                <li>
                  <div class="TagLine"></div>
                  <div class="text-center"><el-image :src="interchangerImg" fit="scale-down"></el-image>
                    <p>检验中心</p>
                    <p>汽表数量：0</p>
                    <p class="itemMarginBottom">蒸汽总量：0</p>
                  </div>
                </li>
              </ul>
            </el-col>
          </el-col>
          <div slot="footer" class="dialog-footer">
            <el-button @click="steamAreaDialog = false">关闭</el-button>
          </div>
        </el-dialog>
        <!-- 水表分布图 -->
        <el-dialog :title="areaOverallDialogTitle" :visible.sync="waterAreaTagDialog" width="40%" v-if="waterAreaTagDialog">
          <el-card shadow="never" v-if="areaOverallDialogTitle === '污水站'">
            <div class="waterTagData" style="position: relative">灌溉水DN40<p class="TagDataVal">{{ waterTagList.W_Area_WSZ_16_2_34.sumValue }}</p><p class="TagDataVal">{{ waterTagList.W_Area_WSZ_16_2_34.flowValue }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '提取一车间'">
            <div class="waterTagData" style="position: relative">后走廊灌溉水DN40<p class="TagDataVal">{{ waterTagList.W_Area_TQR_17_2_8.sumValue }}</p><p class="TagDataVal">{{ waterTagList.W_Area_TQR_17_2_8.flowValue }}</p></div>
            <div class="waterTagData" style="position: relative">出料电梯旁饮用水DN100<p class="TagDataVal">{{ waterTagList.W_Area_TQR_17_1_9.sumValue }}</p><p class="TagDataVal">{{ waterTagList.W_Area_TQR_17_1_9.flowValue }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '提取二车间'">
            <div class="waterTagData" style="position: relative">带干辅机灌溉水DN40<p class="TagDataVal">{{ waterTagList.W_Area_ZH_23_2_13.sumValue }}</p><p class="TagDataVal">{{ waterTagList.W_Area_ZH_23_2_13.flowValue }}</p></div>
            <div class="waterTagData" style="position: relative">2楼会议室饮用水DN150<p class="TagDataVal">{{ waterTagList.W_Area_ZH_23_1_12.sumValue }}</p><p class="TagDataVal">{{ waterTagList.W_Area_ZH_23_1_12.flowValue }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '制剂二车间'">
            <div class="waterTagData" style="position: relative">包材库灌溉水DN50<p class="TagDataVal">{{ waterTagList.W_Area_XJZ_12_1_3.sumValue }}</p><p class="TagDataVal">{{ waterTagList.W_Area_XJZ_12_1_3.flowValue }}</p></div>
            <div class="waterTagData" style="position: relative">接待室饮用水DN100<p class="TagDataVal">{{ waterTagList.W_Area_XJZ_12_2_5.sumValue }}</p><p class="TagDataVal">{{ waterTagList.W_Area_XJZ_12_2_5.flowValue }}</p></div>
          </el-card>
          <!--<el-card shadow="never" v-if="areaOverallDialogTitle === '中试车间'">-->
            <!--<div class="waterTagData" style="position: relative">消防水DN100<p class="TagDataVal">{{ waterTagList.W_Area_YF_26_1_15.sumValue }}</p><p class="TagDataVal">{{ waterTagList.W_Area_YF_26_1_15.flowValue }}</p></div>-->
          <!--</el-card>-->
          <el-card shadow="never" v-if="areaOverallDialogTitle === '提取三车间'">
            <div class="waterTagData" style="position: relative">消防水DN50<p class="TagDataVal">{{ waterTagList.W_Area_YTQ_39_1_30.sumValue }}</p><p class="TagDataVal">{{ waterTagList.W_Area_YTQ_39_1_30.flowValue }}</p></div>
            <div class="waterTagData" style="position: relative">灌溉水DN40<p class="TagDataVal">{{ waterTagList.W_Area_YTQ_39_2_30.sumValue }}</p><p class="TagDataVal">{{ waterTagList.W_Area_YTQ_39_2_30.flowValue }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '前处理车间'">
            <div class="waterTagData" style="position: relative">洗药室灌溉水DN25<p class="TagDataVal">{{ waterTagList.W_Area_QCL_33_1_20.sumValue }}</p><p class="TagDataVal">{{ waterTagList.W_Area_QCL_33_1_20.flowValue }}</p></div>
            <div class="waterTagData" style="position: relative">饮用水DN25<p class="TagDataVal">{{ waterTagList.W_Area_QCL_33_2_20.sumValue }}</p><p class="TagDataVal">{{ waterTagList.W_Area_QCL_33_2_20.flowValue }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '制剂三车间'">
            <div class="waterTagData" style="position: relative">消防水DN50<p class="TagDataVal">{{ waterTagList.W_Area_JK_28_1_16.sumValue }}</p><p class="TagDataVal">{{ waterTagList.W_Area_JK_28_1_16.flowValue }}</p></div>
            <div class="waterTagData" style="position: relative">消防水DN50<p class="TagDataVal">{{ waterTagList.W_Area_JK_28_2_16.sumValue }}</p><p class="TagDataVal">{{ waterTagList.W_Area_JK_28_2_16.flowValue }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '制剂一车间c'">
            <div class="waterTagData" style="position: relative">男卫生间灌溉水DN40<p class="TagDataVal">{{ waterTagList.W_Area_GT_30_2_18.sumValue }}</p><p class="TagDataVal">{{ waterTagList.W_Area_GT_30_2_18.flowValue }}</p></div>
            <div class="waterTagData" style="position: relative">纯化水站饮用水DN100<p class="TagDataVal">{{ waterTagList.W_Area_GT_30_1_19.sumValue }}</p><p class="TagDataVal">{{ waterTagList.W_Area_GT_30_1_19.flowValue }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '行政办公楼'">
            <div class="waterTagData" style="position: relative">1楼卫生间深井水DN65<p class="TagDataVal">{{ waterTagList.W_Area_BGL_34_1_22.sumValue }}</p><p class="TagDataVal">{{ waterTagList.W_Area_BGL_34_1_22.flowValue }}</p></div>
          </el-card>
          <div slot="footer" class="dialog-footer">
            <el-button @click="waterAreaTagDialog = false">关 闭</el-button>
          </div>
        </el-dialog>
        <!-- 电表分布图 -->
        <el-dialog :title="areaOverallDialogTitle" :visible.sync="electricAreaTagDialog" width="40%" v-if="electricAreaTagDialog">
          <el-card shadow="never" v-if="areaOverallDialogTitle === '污水站'">
            <div class="waterTagData">污水站1<p></p><p class="TagDataVal">{{ electricTagList.E_Area_WSZ_16_2_35.ZGL }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '制剂二车间'">
            <div class="waterTagData">综合制剂2楼配电室2<p>空压机、循环水、机器人</p><p class="TagDataVal">{{ electricTagList.E_Area_XJZ_11_2_7.ZGL }}</p></div>
            <div class="waterTagData">综合制剂2楼配电室1<p>干法、颗粒</p><p class="TagDataVal">{{ electricTagList.E_Area_XJZ_11_2_7_1.ZGL }}</p></div>
            <div class="waterTagData">综合制剂2楼配电室3<p>电梯、压片、胶囊、泡罩、粉碎</p><p class="TagDataVal">{{ electricTagList.E_Area_XJZ_11_2_7_3.ZGL }}</p></div>
            <div class="waterTagData">综合制剂2楼空调室4<p>2L空调</p><p class="TagDataVal">{{ electricTagList.E_Area_XJZ_11_2_7_4.ZGL }}</p></div>
            <div class="waterTagData">综合制剂1楼配电室5<p>洗衣机、照明、卷帘门、风机</p><p class="TagDataVal">{{ electricTagList.E_Area_XJZ_11_1_6_5.ZGL }}</p></div>
            <div class="waterTagData">综合制剂1楼冷水室6<p>冷水机组2</p><p class="TagDataVal">{{ electricTagList.E_Area_XJZ_11_1_6_6.ZGL }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '检验中心'">
            <div class="waterTagData">化验室1<p>电器</p><p class="TagDataVal">{{ electricTagList.E_Area_YF_26_1_14.ZGL }}</p></div>
            <div class="waterTagData">化验室2<p>老醇提水泵、车床、台钻、砂轮</p><p class="TagDataVal">{{ electricTagList.E_Area_YF_26_1_14_2.ZGL }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '提取三车间'">
            <div class="waterTagData">老醇提1<p>办公、新700粉碎机、机修、设备库房</p><p class="TagDataVal">{{ electricTagList.E_Area_YTQ_38_1_28.ZGL }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '前处理车间'">
            <div class="waterTagData">原提取1<p>办公、新700粉碎机、机修、设备库房</p><p class="TagDataVal">{{ electricTagList.E_Area_YTQ_38_2_29.ZGL }}</p></div>
            <div class="waterTagData">原提取2<p>洗药机、切药机</p><p class="TagDataVal">{{ electricTagList.E_Area_YTQ_38_2_29_3.ZGL }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '制剂三车间'">
            <div class="waterTagData">健康科技车间一楼1<p></p><p class="TagDataVal">{{ electricTagList.E_Area_JK_28_2_17.ZGL }}</p></div>
            <div class="waterTagData">健康科技车间一楼2<p></p><p class="TagDataVal">{{ electricTagList.E_Area_JK_28_1_16.ZGL }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '制剂一车间'">
            <div class="waterTagData">固体制剂4<p>除尘系统、空调系统</p><p class="TagDataVal">{{ electricTagList.E_Area_GT_30_2_19.ZGL }}</p></div>
            <div class="waterTagData">固体制剂1<p>机修办公室、压片、胶囊、混合、挂衣、颗粒、瓶线</p><p class="TagDataVal">{{ electricTagList.E_Area_GT_30_2_19_1.ZGL }}</p></div>
            <div class="waterTagData">固体制剂2<p>风冷冷水机、除湿机、空压机</p><p class="TagDataVal">{{ electricTagList.E_Area_GT_30_2_19_2.ZGL }}</p></div>
            <div class="waterTagData">固体制剂3<p>照明</p><p class="TagDataVal">{{ electricTagList.E_Area_GT_30_2_19_3.ZGL }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '行政办公楼'">
            <div class="waterTagData">展馆旁1<p></p><p class="TagDataVal">{{ electricTagList.E_Area_BGL_36_1_26.ZGL }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '提取一车间'">
            <div class="waterTagData">提取二2楼空调室二1<p>冷水机组</p><p class="TagDataVal">{{ electricTagList.E_Area_TQR_18_2_36_1.ZGL }}</p></div>
            <div class="waterTagData">提取二2楼空调室二2<p>空调机组</p><p class="TagDataVal">{{ electricTagList.E_Area_TQR_18_2_36_2.ZGL }}</p></div>
            <div class="waterTagData">提取二2楼电控室1<p>冷水机组</p><p class="TagDataVal">{{ electricTagList.E_Area_TQR_18_2_36_3.ZGL }}</p></div>
            <div class="waterTagData">提取二2楼电控室2<p>制粒</p><p class="TagDataVal">{{ electricTagList.E_Area_TQR_18_2_36_4.ZGL }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '锅炉房'">
            <div class="waterTagData">锅炉房电柜1<p>锅炉</p><p class="TagDataVal">{{ electricTagList.E_Area_GLF_42_1_33_1.ZGL }}</p></div>
            <div class="waterTagData">锅炉房电柜2<p>供暖</p><p class="TagDataVal">{{ electricTagList.E_Area_GLF_42_1_33_2.ZGL }}</p></div>
            <div class="waterTagData">锅炉房旁边屋子3<p>脱硫</p><p class="TagDataVal">{{ electricTagList.E_Area_GLF_42_1_33_3.ZGL }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '智能库房'">
            <div class="waterTagData">智能库1楼1<p></p><p class="TagDataVal">{{ electricTagList.E_Area_ZNK_24_1_10_1.ZGL }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '提取二车间'">
            <div class="waterTagData">综合2楼MVR1<p></p><p class="TagDataVal">{{ electricTagList.E_Area_ZH_1.ZGL }}</p></div>
            <div class="waterTagData">综合2楼MVR2<p></p><p class="TagDataVal">{{ electricTagList.E_Area_ZH_2.ZGL }}</p></div>
            <div class="waterTagData">2楼配电室1<p>总表、制粒、带干、粉糖、输液泵</p><p class="TagDataVal">{{ electricTagList.E_Area_ZH_50_1_41_1.ZGL }}</p></div>
            <div class="waterTagData">2楼配电室2<p>制粒</p><p class="TagDataVal">{{ electricTagList.E_Area_ZH_50_1_41_2.ZGL }}</p></div>
            <div class="waterTagData">2楼配电室3<p>带干</p><p class="TagDataVal">{{ electricTagList.E_Area_ZH_50_1_41_3.ZGL }}</p></div>
            <div class="waterTagData">2楼配电室4<p>浓缩罐、自控系统、电梯、洗衣房、真空泵</p><p class="TagDataVal">{{ electricTagList.E_Area_ZH_50_1_41_4.ZGL }}</p></div>
            <div class="waterTagData">2楼配电室5<p>排风</p><p class="TagDataVal">{{ electricTagList.E_Area_ZH_50_1_41_5.ZGL }}</p></div>
            <div class="waterTagData">2楼配电室6<p>照明</p><p class="TagDataVal">{{ electricTagList.E_Area_ZH_50_1_41_6.ZGL }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '变电所'">
            <div class="waterTagData">变电所1<p>40喷干</p><p class="TagDataVal">{{ electricTagList.E_Area_BDS_49_1_39_1.ZGL }}</p></div>
            <div class="waterTagData">变电所2<p>50喷干</p><p class="TagDataVal">{{ electricTagList.E_Area_BDS_49_1_39_2.ZGL }}</p></div>
            <div class="waterTagData">变电所3<p>新提取循环水泵</p><p class="TagDataVal">{{ electricTagList.E_Area_BDS_49_1_39_3.ZGL }}</p></div>
            <div class="waterTagData">变电所4<p>消防水泵+新大库</p><p class="TagDataVal">{{ electricTagList.E_Area_BDS_49_1_39_4.ZGL }}</p></div>
            <div class="waterTagData">变电所5<p>GMP</p><p class="TagDataVal">{{ electricTagList.E_Area_BDS_49_2_40_5.ZGL }}</p></div>
            <div class="waterTagData">变电所6<p>前处理</p><p class="TagDataVal">{{ electricTagList.E_Area_BDS_49_2_40_6.ZGL }}</p></div>
            <div class="waterTagData">变电所7<p>仓储中心</p><p class="TagDataVal">{{ electricTagList.E_Area_BDS_49_2_40_7.ZGL }}</p></div>
            <div class="waterTagData">变电所8<p>提取二照明</p><p class="TagDataVal">{{ electricTagList.E_Area_BDS_49_2_40_8.ZGL }}</p></div>
            <div class="waterTagData">变电所9<p>40粉碎、提取二空调</p><p class="TagDataVal">{{ electricTagList.E_Area_BDS_49_2_40_9.ZGL }}</p></div>
            <div class="waterTagData">变电所10<p>60带干、风机、制粒、办公</p><p class="TagDataVal">{{ electricTagList.E_Area_BDS_49_2_40_10.ZGL }}</p></div>
            <div class="waterTagData">变电所11<p>提取、自控</p><p class="TagDataVal">{{ electricTagList.E_Area_BDS_49_2_40_11.ZGL }}</p></div>
            <div class="waterTagData">变电所12<p>提取二车间新空调</p><p class="TagDataVal">{{ electricTagList.E_Area_BDS_49_2_40_12.ZGL }}</p></div>
          </el-card>
          <div slot="footer" class="dialog-footer">
            <el-button @click="electricAreaTagDialog = false">关 闭</el-button>
          </div>
        </el-dialog>
        <!-- 汽表分布图 没有图片 -->
        <el-dialog :title="areaOverallDialogTitle" :visible.sync="steamAreaTagDialog" width="40%" v-if="steamAreaTagDialog">
          <el-card shadow="never" v-if="areaOverallDialogTitle === '提取三车间'">
            <div class="waterTagData">蒸汽表<p class="TagDataVal">{{ steamTagList.S_Area_YTQ_40_1_502.sumValue }}</p><p class="TagDataVal">{{ steamTagList.S_Area_YTQ_40_1_502.flowValue }}</p><p class="TagDataVal">{{ steamTagList.S_Area_YTQ_40_1_502.SteamWD }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '前处理车间'">
            <div class="waterTagData">蒸汽表<p class="TagDataVal">{{ steamTagList.S_Area_YTQ_40_2_502.sumValue }}</p><p class="TagDataVal">{{ steamTagList.S_Area_YTQ_40_2_502.flowValue }}</p><p class="TagDataVal">{{ steamTagList.S_Area_YTQ_40_2_502.SteamWD }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '制剂三车间'">
            <div class="waterTagData">蒸汽表<p class="TagDataVal">{{ steamTagList.S_Area_JK_27_1_502.sumValue }}</p><p class="TagDataVal">{{ steamTagList.S_Area_JK_27_1_502.flowValue }}</p><p class="TagDataVal">{{ steamTagList.S_Area_JK_27_1_502.SteamWD }}</p></div>
          </el-card>
          <el-card shadow="never" v-if="areaOverallDialogTitle === '行政办公楼'">
            <div class="waterTagData">蒸汽表<p class="TagDataVal">{{ steamTagList.S_Area_BGL_35_1_502.sumValue }}</p><p class="TagDataVal">{{ steamTagList.S_Area_BGL_35_1_502.flowValue }}</p><p class="TagDataVal">{{ steamTagList.S_Area_BGL_35_1_502.SteamWD }}</p></div>
          </el-card>
          <div slot="footer" class="dialog-footer">
            <el-button @click="steamAreaTagDialog = false">关 闭</el-button>
          </div>
        </el-dialog>
        <!-- 汽表分布图 有图片-->
        <el-dialog :title="areaOverallDialogTitle" :visible.sync="areaOverallDialog" :modal="false" width="840px">
          <div v-if="areaOverallDialogSrc2" style="position: relative;display: inline-flex;">
            <el-image style="width: 100%;" :src="areaOverallDialogSrc2"></el-image>
            <div v-if="areaOverallDialogTitle === '提取一车间'">
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
            <div v-if="areaOverallDialogTitle === '提取一车间'">
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
            <div v-if="areaOverallDialogTitle === '提取二车间'">
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
            <div v-if="areaOverallDialogTitle === '制剂二车间'">
              <div class="steamTagLabel" style="left:20px;top: 300px;">
                <div class="steamTagTitle">新制剂分汽缸DN200</div>
                <div class="steamTagValue">
                  <p>{{ steamTagList.S_Area_XJZ_13_1_7_502.sumValue }}</p>
                  <p>{{ steamTagList.S_Area_XJZ_13_1_7_502.flowValue }}</p>
                  <p>{{ steamTagList.S_Area_XJZ_13_1_7_502.SteamWD }}°C</p>
                </div>
              </div>
            </div>
            <div v-if="areaOverallDialogTitle === '制剂一车间'">
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
        {title:"提取一车间",top:"34%",left:"35%",img:require("@/assets/imgs/tiquer.jpg"),img2:require("@/assets/imgs/tiquer2.jpg"),hasElectric:true,hasWater:true,hasSteam:true},
        {title:"提取二车间",top:"40%",left:"35%",img:require("@/assets/imgs/zonghe.jpg"),hasElectric:true,hasWater:true,hasSteam:true},
        {title:"制剂二车间",top:"32%",left:"47%",img:require("@/assets/imgs/xinzhiji.jpg"),hasElectric:true,hasWater:true,hasSteam:true},
        {title:"变电所",top:"40%",left:"48%",hasElectric:true,hasWater:false,hasSteam:false},
        {title:"检验中心",top:"30%",left:"56%",hasElectric:true,hasWater:true,hasSteam:true},
        {title:"智能库房",top:"27%",left:"52%",hasElectric:true,hasWater:false,hasSteam:false},
        {title:"提取三车间",top:"31%",left:"62%",hasElectric:true,hasWater:true,hasSteam:true},
        {title:"前处理车间",top:"34%",left:"68%",hasElectric:true,hasWater:true,hasSteam:true},
        {title:"制剂三车间",top:"38%",left:"61%",hasElectric:true,hasWater:true,hasSteam:true},
        {title:"制剂一车间",top:"43%",left:"61%",img:require("@/assets/imgs/gutizhiji.jpg"),hasElectric:true,hasWater:true,hasSteam:true},
        {title:"展览室",top:"60%",left:"17%"},
        {title:"行政办公楼",top:"57%",left:"28%",hasElectric:true,hasWater:true,hasSteam:true},
      ],
      interchangerImg:require("@/assets/imgs/interchanger.jpg"),
      computerImg:require("@/assets/imgs/computer.png"),
      printerImg:require("@/assets/imgs/printer.png"),
      UPSImg:require("@/assets/imgs/UPS.jpg"),
      waterAreaDialog:false,
      waterAreaTagDialog:false,
      waterdialogfullscreen:false,
      waterImgCollapse:false,
      electricAreaTagDialog:false,
      electricdialogfullscreen:false,
      electricImgCollapse:false,
      steamAreaTagDialog:false,
      electricAreaDialog:false,
      steamAreaDialog:false,
      steamdialogfullscreen:false,
      steamImgCollapse:false,
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
      positionX:"",
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
    },
    move(e){
      let odiv = e.target; //获取目标元素
      if(odiv.attributes.hasOwnProperty("data-move")){
        //算出鼠标相对元素的位置
        let disX = e.clientX - odiv.offsetLeft;
        document.onmousemove = (e)=>{ //鼠标按下并移动的事件
          //用鼠标的位置减去鼠标相对元素的位置，得到元素的位置
          let left = e.clientX - disX;
          //绑定元素位置到positionX和positionY上面
          this.positionX = top;
          //移动当前元素
          odiv.style.left = left + 'px';
        };
        document.onmouseup = (e) => {
          document.onmousemove = null;
          document.onmouseup = null;
        };
      }
    },
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
    line-height: 64px;
  }
  .steamTagValue{
    display: inline-grid;
    float: right;
  }
  .steamTagValue p{
    background: #333333;
    padding: 0 5px;
    color: #15CC48;
    margin-bottom: 3px;
    white-space: nowrap;
    min-width:70px;
    float: right;
  }
  .useAreaCard{
    position: relative;
    background: #EFF5FB;
    min-height: 120px;
  }
  .waterTagData{
    position: relative;
    width: 150px;
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
    position: absolute;
    overflow: hidden;
    overflow-y: auto;
    white-space: nowrap;
    height:100%;
  }
  .areaTotalTagUl li{
    position: relative;
    width: 150px;
    display: inline-block;
    margin-right: 20px;
    vertical-align: top;
  }
  .areaTotalTagUl li img{
    width: 100%;
  }
  .TagLine{
    width: 1px;
    height: 25px;
    margin: 0 auto;
    background: #a1a1a1;
  }
  .electricTagData{
    background: #c0c7cd;
    padding: 10px;
    color: #000;
    border: 1px solid #e1e1e1;
    white-space:normal;
  }
  .electricTagData p{
    background: #476c39;
    padding: 3px 5px;
    text-align: right;
    margin-bottom: 3px;
    white-space: nowrap;
  }
</style>
