<template>
  <el-container class="body-container">
    <!-- 侧边栏 -->
    <el-aside width="180px" class="left-aside">
      <el-row>
        <el-col :span="24">
          <div class="aside-head">
            <router-link :to="{name:'home'}"><i class="fa fa-home"></i></router-link>
          </div>
          <div :style="selfHeight" class="aside-menu">
            <el-menu class="menu-ul" default-active="" :collapse="isCollapse">
              <template v-for="(item,index) in subMenulist">
                <el-menu-item v-if="!item.children" :index="item.name" :src="item.url" @click="clickSubMenu(item.name,item.url)"><i :class="item.icon"></i><span slot="title">{{ item.name }}</span></el-menu-item>
                <el-submenu v-if="!item.url" :index="item.name">
                    <template slot="title"><i :class="item.icon"></i><span>{{ item.name }}</span></template>
                    <el-menu-item v-for="(child,childIndex) in item.children" :key="childIndex" :index="childIndex+''" :src="child.url" @click="clickSubMenu(child.name,child.url)"><span style="margin-left:10px;">{{child.name}}</span></el-menu-item>
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
              <el-tooltip class="head-menu-item" effect="dark" content="消息提醒" placement="bottom">
                <el-badge :value="12"><i class="el-icon-s-comment"></i></el-badge>
              </el-tooltip>
            </li>
            <li><el-tooltip class="head-menu-item" effect="dark" content="全屏" placement="bottom"><span :class="isFullScreen?'el-icon-aim':'el-icon-full-screen'" @click="getFullCreeen"></span></el-tooltip></li>
            <li><div>{{ time }}</div></li>
          </ul>
        </div>
        <div class="head-right-menu"><ul><li class="active"><i class="el-icon-menu"></i></li></ul></div>
        <div class="head-right-menu">
          <ul>
            <li v-for="(item,index) in mainMenuList" :key="index" @click="clickMainMenu(index)" v-bind:class="{active:index==isactive}">{{ item.text }}</li>
          </ul>
        </div>
        <!-- 个人信息 -->
        <el-dialog title="个人信息" :visible.sync="dialogUserVisible">
          <el-form></el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogUserVisible = false">取 消</el-button>
            <el-button type="primary" @click="dialogUserVisible = false">确 定</el-button>
          </div>
        </el-dialog>
      </el-header>
      <!-- 页面主体 -->
      <el-main>
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
import {mapState} from 'vuex'
export default {
  name: 'Index',
  data () {
    return {
      selfHeight:{ //自适应高度
        height:''
      },
      isCollapse: false, //左侧菜单栏是否缩进了
      sideIcon:'el-icon-arrow-left', //左侧菜单栏缩进点击切换图标
      time:"",  //实时显示当前的时间
      dialogUserVisible:false, //是否弹出个人信息
      isactive:"0", //主菜单选中索引值
      mainMenuList:[ //主菜单导航列表
        {text:"能源管理"},
        {text:"系统管理"}
      ],
      subMenulist:[], //子菜单导航列表
      isFullScreen:false, //是否全屏
      areaObj:{
        areaName:""
      }
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
      _this.time = moment(new Date()).format('MM-DD HH:mm:ss');
    },1000);
    this.clickMainMenu(this.isactive)
  },
  created(){
    window.addEventListener('resize', this.getMenuHeight);
    this.getMenuHeight()
    if(sessionStorage.getItem("LoginStatus")) {
      this.$store.commit('setUser',sessionStorage.getItem('WorkNumber'))
      var params = {
        tableName: "User",
        ID:sessionStorage.getItem('UserId'),
        LastLoginTime:moment(new Date()).format('YYYY-MM-DD HH:mm:ss')
      }
      this.axios.put("/api/CUID",this.qs.stringify(params)).then(res =>{
      },res =>{
        console.log("修改登录时间时请求错误")
      })
    }else{
      this.$router.push("/login");
    }
  },
  methods:{
    getMenuHeight(){
      this.selfHeight.height = window.innerHeight - 210+'px';
    },
    clickSubMenu(areaName,url){
      this.areaObj.areaName = areaName
      this.$router.push({
        path:url,
        query:{
          t:Date.now()
        }
      })
    },
    handleCommand(command) {
      if(command == "a"){
        this.dialogUserVisible = true
      }else if(command == "b"){
        this.$store.commit('removeUser')
        this.$router.replace("/login")
      }
    },
    iconToggle() {
      this.isCollapse = !this.isCollapse
      if(this.isCollapse){
        this.sideIcon = 'el-icon-arrow-right'
        $(".left-aside").animate({"width":"64px"})
      }else{
        this.sideIcon = 'el-icon-arrow-left'
        $(".left-aside").animate({"width":"180px"})
      }
    },
    clickMainMenu(index){
      this.isactive = index
      if(index == 0) {
        this.subMenulist = [
          {name: "桓仁厂区", icon: "el-icon-location-outline", children:[
              {name:"整厂区",url:"/Areas?areaName=整厂区"},
              {name:"新建综合试剂楼",url:"/Areas?areaName=新建综合试剂楼"},
              {name:"提取二车间",url:"/Areas?areaName=提取二车间"},
              {name:"前处理车间",url:"/Areas?areaName=前处理车间"},
              {name:"研发中心",url:"/Areas?areaName=研发中心"},
              {name:"生物科技楼",url:"/Areas?areaName=生物科技楼"},
              {name:"原提取车间",url:"/Areas?areaName=原提取车间"},
              {name:"锅炉房",url:"/Areas?areaName=锅炉房"},
              {name:"综合办公楼",url:"/Areas?areaName=综合办公楼"},
              {name:"综合车间",url:"/Areas?areaName=综合车间"},
              {name:"污水站",url:"/Areas?areaName=污水站"},
              {name:"固体制剂车间",url:"/Areas?areaName='固体制剂车间"},
              {name:"展览馆",url:"/Areas?areaName=展览馆"},
            ]
          },
          {name: "能效分析", icon: "el-icon-time", url: "/EfficiencyAnalysis"},
          {name: "综合报表", icon: "el-icon-document", url: "/DataReport"}
        ]
      }else if(index == 1){
        this.subMenulist = [
          {name:"组织架构",icon:"el-icon-office-building",url:"/Organization"},
          {name:"厂区管理",icon:"el-icon-location-information",url:"/Factory"},
          {name:"角色管理",icon:"el-icon-s-check",url:"/Role"},
          {name:"人员管理",icon:"el-icon-user",url:"/Personnel"},
          {name:"工厂日历",icon:"el-icon-date",url:"/Calendar"},
          {name:"系统日志",icon:"el-icon-notebook-1",url:"/Log"},
        ]
      }
    },
    beforeDestroy() {
      if (this.timer) {
        clearInterval(this.timer);
      }
    },
    getFullCreeen () {
      if (screenfull.isEnabled) {
        screenfull.toggle()
        if(screenfull.isFullscreen){
          this.isFullScreen = false
        }else{
          this.isFullScreen = true
        }
      }
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
    text-align: center;
    font-size: 30px;
    padding: 30px 0;
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
  }
  .menu-ul::-webkit-scrollbar {
    display: none;  /* 隐藏滚动条 */
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
  .head-right-menu li{
    float: left;
    margin-right: 15px;
    color: #082F4C;
    font-size: 16px;
    text-decoration: none;
    display: block;
    padding: 5px 10px;
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
</style>
