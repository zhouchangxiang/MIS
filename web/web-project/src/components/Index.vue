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
              <el-tooltip class="head-menu-item" effect="dark" content="全屏" placement="bottom">
                <i :class="isFullScreen?'el-icon-aim':'el-icon-full-screen'" @click="getFullCreeen"></i>
              </el-tooltip>
            </li>
            <li>
              <el-tooltip class="head-menu-item" effect="dark" content="基础表管理" placement="bottom">
                <i class="el-icon-c-scale-to-original" @click="$router.push({path:'/config'})"></i>
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
            <div class="mapContent"  v-if="JSON.stringify(steamTagList) != '{}'">
              <div class="mapContentTop">
                <div style="position: relative;height: 100%;">
                  <div v-for="(item,index) in drawerTopAreaOption" class="mapContentItem" :style="{width:item.width, height: item.height,top: item.top,left: item.left}" :key="index" @click="showAreaInfo(item.title,item.img,item.img2)">
                    <div class="mapItemPoint" :style="{marginLeft: item.marginLeft}"></div>
                  </div>
                </div>
              </div>
              <div class="mapContentBottom">
                <div style="position: relative;height: 100%;">
                  <div v-for="(item,index) in drawerBottomAreaOption" class="mapContentItem" :style="{width:item.width, height: item.height,top: item.top,left: item.left}" :key="index">
                    <div class="mapItemPoint" :style="{marginLeft: item.marginLeft}"></div>
                  </div>
                </div>
              </div>
            </div>
            <el-button type="primary" @click="lookWaterMap" style="position: absolute;left: 0;" v-if="JSON.stringify(waterTagList) != '{}'">水表采集图</el-button>
          </div>
        </el-drawer>
        <!-- 水表分布图 -->
        <el-dialog title="水表采集分布" :visible.sync="waterAreaDialog" width="70%" v-if="waterAreaDialog">
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
                  <div class="waterTagData" style="right: 3px;top: 3px;">后走廊灌溉水DN40<p>{{ waterTagList.W_Area_TQR_17_1_9.sumValue }}</p><p>{{ waterTagList.W_Area_TQR_17_1_9.flowValue }}</p></div>
                  <div class="waterTagData" style="bottom: 3px;left:3px;">出料电梯旁饮用水DN100<p>{{ waterTagList.W_Area_TQR_17_2_8.sumValue }}</p><p>{{ waterTagList.W_Area_TQR_17_2_8.flowValue }}</p></div>
                </el-card>
                <el-card shadow="hover" class="useAreaCard" style="height: 140px;">
                  <p>综合车间</p>
                  <div class="waterTagData" style="right: 3px;top: 3px;">带干辅机灌溉水DN40<p>{{ waterTagList.W_Area_ZH_23_1_12.sumValue }}</p><p>{{ waterTagList.W_Area_ZH_23_1_12.flowValue }}</p></div>
                  <div class="waterTagData" style="right: 3px;bottom: 3px;">2楼会议室饮用水DN150<p>{{ waterTagList.W_Area_ZH_23_2_13.sumValue }}</p><p>{{ waterTagList.W_Area_ZH_23_2_13.flowValue }}</p></div>
                </el-card>
              </el-col>
              <el-col :span="4">
                <el-card shadow="hover" style="height: 250px;margin-bottom: 20px;" class="useAreaCard">
                  <p>新综合制剂车间</p>
                  <div class="waterTagData" style="left: 3px;top: 60px;width: 80px;">包材库灌溉水DN50<p>{{ waterTagList.W_Area_XJZ_12_1_3.sumValue }}</p><p>{{ waterTagList.W_Area_XJZ_12_1_3.flowValue }}</p></div>
                  <div class="waterTagData" style="right: 3px;bottom: 3px;">接待室DN100<p>{{ waterTagList.W_Area_XJZ_12_2_5.sumValue }}</p><p>{{ waterTagList.W_Area_XJZ_12_2_5.flowValue }}</p></div>
                </el-card>
              </el-col>
              <el-col :span="8">
                <el-col :span="8">
                  <el-card shadow="hover" class="useAreaCard" style="height: 240px;">
                    <p>化验室/中试车间</p><div class="waterTagData" style="left: 3px;bottom: 3px;">消防DN100<p>{{ waterTagList.W_Area_YF_26_1_15.sumValue }}</p><p>{{ waterTagList.W_Area_YF_26_1_15.flowValue }}</p></div>
                  </el-card>
                </el-col>
                <el-col :span="8">
                  <el-card shadow="hover" class="useAreaCard" style="height: 180px;">
                    <p>原提取</p>
                    <div class="waterTagData" style="left: 3px;top: 40px;">消防DN50<p>{{ waterTagList.W_Area_YTQ_39_1_30.sumValue }}</p><p>{{ waterTagList.W_Area_YTQ_39_1_30.flowValue }}</p></div>
                    <div class="waterTagData" style="left: 3px;bottom: 3px;">灌溉水DN40<p>{{ waterTagList.W_Area_YTQ_39_2_30.sumValue }}</p><p>{{ waterTagList.W_Area_YTQ_39_2_30.flowValue }}</p></div>
                  </el-card>
                </el-col>
                <el-col :span="8">
                  <el-card shadow="hover" class="useAreaCard" style="height: 240px;">
                    <p>前处理车间</p>
                    <div class="waterTagData" style="left: 3px;top: 40px;">洗药室DN25<p>{{ waterTagList.W_Area_QCL_33_1_20.sumValue }}</p><p>{{ waterTagList.W_Area_QCL_33_1_20.flowValue }}</p></div>
                    <div class="waterTagData" style="left: 3px;top: 110px;">饮用水DN25<p>{{ waterTagList.W_Area_QCL_33_2_20.sumValue }}</p><p>{{ waterTagList.W_Area_QCL_33_2_20.flowValue }}</p></div>
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
                  <div class="waterTagData" style="left: 100px;bottom: 10px;">1楼卫生间DN65<p>{{ waterTagList.W_Area_BGL_34_1_22.sumValue }}</p><p>{{ waterTagList.W_Area_BGL_34_1_22.flowValue }}</p></div>
                </el-card>
              </el-col>
            </el-col>
          </el-row>
          <div slot="footer" class="dialog-footer">
            <el-button @click="waterAreaDialog = false">关闭</el-button>
          </div>
        </el-dialog>
        <!-- 汽表分布图 -->
        <el-dialog :title="areaOverallDialogTitle" :visible.sync="areaOverallDialog" :modal="false" width="840px">
          <div v-if="areaOverallDialogSrc2" style="position: relative;display: inline-flex;">
            <el-image style="width: 100%;" :src="areaOverallDialogSrc2"></el-image>
            <div v-if="areaOverallDialogTitle === '提取二车间'">
              <div class="steamTagLabel" style="left:-10px;top: -15px;min-width: 155px;width: 155px;">
                <div class="steamTagTitle">锅炉流量计DN400</div>
                <div class="steamTagValue">
                  <p>{{ steamGlTag.sumValue }}</p>
                  <p>{{ steamGlTag.flowValue }}</p>
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
                  <p>{{ steamGlTag.sumValue }}</p>
                  <p>{{ steamGlTag.flowValue }}</p>
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
                  <p>{{ steamTagList.S_Area_GLF_45_3_502.sumValue }}</p>
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
                  <p>{{ steamGlTag.sumValue }}</p>
                  <p>{{ steamGlTag.flowValue }}</p>
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
                  <p>{{ steamGlTag.sumValue }}</p>
                  <p>{{ steamGlTag.flowValue }}</p>
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
      drawerTopAreaOption:[
        //{title:"污水站",width: "120px",height:"30%",top:"26%",left:"5%",marginLeft:"80px"},
        {title:"锅炉房",width: "220px",height:"20%",top:"26%",left:"15%",marginLeft:"120px",img:require("@/assets/imgs/guolu.jpg")},
        {title:"提取二车间",width: "220px",height:"15%",top:"42%",left:"15%",marginLeft:"100px",img:require("@/assets/imgs/tiquer.jpg"),img2:require("@/assets/imgs/tiquer2.jpg")},
        {title:"综合车间",width: "250px",height:"28%",top:"60%",left:"10%",marginLeft:"100px",img:require("@/assets/imgs/zonghe.jpg")},
        {title:"新建综合制剂车间",width: "100px",height:"45%",top:"18%",left:"34%",marginLeft:"60px",img:require("@/assets/imgs/xinzhiji.jpg")},
        //{title:"中试车间",width: "60px",height:"43%",top:"18%",left:"45%",marginLeft:"35px"},
        //{title:"原提取车间",width: "90px",height:"15%",top:"33%",left:"50%",marginLeft:"30px"},
        //{title:"前处理车间",width: "90px",height:"17%",top:"45%",left:"58%",marginLeft:"40px"},
        //{title:"GMP车间",width: "220px",height:"17%",top:"55%",left:"46%",marginLeft:"80px"},
        {title:"固体制剂车间",width: "280px",height:"28%",top:"74%",left:"48%",marginLeft:"160px",img:require("@/assets/imgs/gutizhiji.jpg")},
      ],
      drawerBottomAreaOption:[
        //{title:"展览室",width: "150px",height:"45%",top:"17%",left:"15%",marginLeft:"70px"},
        //{title:"办公楼＼食堂",width: "360px",height:"48%",top:"10%",left:"25%",marginLeft:"140px"},
      ],
      waterAreaDialog:false,
      areaOverallDialog:false,
      areaOverallDialogTitle:"",
      areaOverallDialogSrc:"",
      areaOverallDialogSrc2:"",
      steamTagList:{},
      waterTagList:{},
      steamGlTag:"",
      websock:null,
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
  },
  destroyed() {
    if(this.websock){
      this.websock.close() //离开路由之后断开websocket连接
    }
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
    showAreaInfo(AreaName,img,img2){
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
    initWebSocket(){ //初始化weosocket
      // this.websock = new WebSocket('ws://' + location.host + '/socket');
      this.websock = new WebSocket('ws://127.0.0.1:5002');
      this.websock.onmessage = this.websocketonmessage;
      this.websock.onopen = this.websocketonopen;
      this.websock.onerror = this.websocketonerror;
      this.websock.onclose = this.websocketclose;
    },
    websocketonopen(){ //连接建立之后执行send方法发送数据
      this.websocketsend("");
    },
    websocketonerror(){//连接建立失败重连
      console.log("websocket连接失败")
    },
    websocketonmessage(e){ //数据接收
      var resdata = JSON.parse(e.data);
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
    height: 100%;
    background: url("../assets/imgs/loginBg.jpg") no-repeat;
    background-size: cover;
    -webkit-background-size: cover;
    -o-background-size: cover;
    background-position: left ;
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
    position: relative;
    height: 60%;
    width: 100%;
  }
  .mapContentTop{
    position: relative;
    padding-left: 340px;
    height:50%;
  }
  .mapContentBottom{
    position: relative;
    height:50%;
  }
  .mapContentItem{
    position: absolute;
    border: none;
    display: flex;
    align-items:center;
    cursor: pointer;
  }
  .mapItemPoint{
    margin-top: 15%;
    margin-left: 50px;
    width: 5px;
    height: 5px;
    background: #fff;
    border-radius: 50%;
    box-shadow: 0 0 5px 5px rgba(227,95,95,1);
    transition: box-shadow 0.6s, transform 0.5s;
  }
  .mapContentItem:hover .mapItemPoint{
    box-shadow: 0 0 10px 10px rgba(251,58,6,1);
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
  .steamTagValue{
    float: right;
  }
  .steamTagValue p{
    background: #333333;
    padding: 0 5px;
    color: #15CC48;
    margin-bottom: 3px;
    white-space: nowrap;
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
  .waterTagData p{
    background: #333333;
    padding: 0 5px;
    color: #15CC48;
    margin-top: 3px;
    white-space: nowrap;
  }
</style>
