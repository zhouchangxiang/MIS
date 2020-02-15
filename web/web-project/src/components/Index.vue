<template>
  <el-container class="body-container">
    <!-- 侧边栏 -->
    <el-aside width="180px" class="left-aside">
      <el-row>
        <el-col :span="24">
          <div class="aside-head">
            <router-link :to="{name:'home'}"><i class="fa fa-home"></i></router-link>
          </div>
          <el-menu class="menu-ul" default-active="0" :collapse="isCollapse">
            <template v-for="(item,index) in subMenulist">
              <el-menu-item v-if="!item.children" :index="item.name" :src="item.url" @click="clickSubMenu"><i :class="item.icon"></i><span slot="title">{{ item.name }}</span></el-menu-item>
              <el-submenu v-if="!item.url" :index="item.name">
                  <template slot="title"><i :class="item.icon"></i><span>{{ item.name }}</span></template>
                  <el-menu-item v-for="(child,childIndex) in item.children" :index="childIndex+''" :src="child.url" @click="clickSubMenu"><span style="margin-left:-10px;">{{child.name}}</span></el-menu-item>
              </el-submenu>
            </template>
          </el-menu>
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
              <el-dropdown trigger="click" @command="handleCommand">
                <span class="el-dropdown-link">
                  <i class="el-icon-user-solid el-icon--left"></i>admin<i class="el-icon-arrow-down el-icon--right"></i>
                </span>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item command="a">个人信息</el-dropdown-item>
                  <el-dropdown-item command="b"><i class="fa fa-power-off"></i></el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </li>
            <li><el-badge :value="12" class="item"><i class="el-icon-s-comment"></i></el-badge></li>
            <li><div>{{ time }}</div></li>
          </ul>
        </div>
        <div class="head-right-menu"><ul><li class="active"><i class="el-icon-menu"></i></li></ul></div>
        <div class="head-right-menu">
          <ul>
            <li v-for="(item,index) in mainMenuList" @click="clickMainMenu(index)" v-bind:class="{active:index==isactive}">{{ item.text }}</li>
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
          <router-view></router-view>
         </transition>
    </el-main>
  </el-container>
</el-container>
</template>

<script>
var moment = require('moment');
export default {
  name: 'Index',
  data () {
    return {
      isCollapse: false, //左侧菜单栏是否缩进了
      sideIcon:'el-icon-arrow-left', //左侧菜单栏缩进点击切换图标
      time:"",  //实时显示当前的时间
      dialogUserVisible:false, //是否弹出个人信息
      isactive:"0", //主菜单选中索引值
      mainMenuList:[ //主菜单导航列表
        {text:"能源管理"},
        {text:"系统管理"}
      ],
      subMenulist:[] //子菜单导航列表
    }
  },
  mounted(){
    let _this = this
    this.timer = setInterval(() =>{
      _this.time = moment(new Date()).format('MM-DD HH:mm:ss');
    },1000);
    this.clickMainMenu(this.isactive)
  },
  methods:{
    clickSubMenu(item){
      console.log(item)
      this.$router.push({
        path:item.$attrs.src,
        query:{
          t:Date.now(),
        }
      })
    },
    handleCommand(command) {
      if(command == "a"){
        this.dialogUserVisible = true
      }else if(command == "b"){
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
              {name:"综合车间",url:"/Areas?areaName='综合车间'"},
              {name:"提取二车间",url:"/Areas?areaName='提取二车间'"},
            ]
          },
          {name: "实时数据", icon: "el-icon-time", url: "/RealTimeData"},
          {name: "数据报表", icon: "el-icon-document", url: "/DataReport"}
        ]
      }else if(index == 1){
        this.subMenulist = [
          {name:"组织架构",icon:"el-icon-s-data",url:"/Organization"}
        ]
      }
    },
    beforeDestroy() {
      if (this.timer) {
        clearInterval(this.timer);
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
    position: absolute;
    width: 100%;
    top: 0;
    text-align: center;
    font-size: 30px;
    padding-top: 30px;
  }
  .aside-head a{
    color: #fff;
  }
  .aside-foot{
    position: absolute;
    width: 100%;
    bottom: 0;
    text-align: center;
    font-size: 18px;
    padding-bottom: 30px;
  }
  .left-aside .el-row .el-col{
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .menu-ul{
    border: none;
  }
  .menu-ul .el-menu-item,.el-submenu__title,.el-submenu__title:hover{
    background: #082F4C;
    color: #fff;
    font-size: 18px;
  }
  .menu-ul .el-menu-item.is-active {
    background-color: #fff;
    color: #082F4C;
  }
  .el-submenu .el-menu-item{
    font-size: 14px;
    min-width: auto;
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
    margin-right: 20px;
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
  .el-dropdown{
    color: #082F4C;
    font-size: 20px;
  }
  .el-dropdown-menu {
    text-align: center;
  }
  .el-badge.item{
    margin-right: 15px;
  }
</style>
