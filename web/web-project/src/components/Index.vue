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
            <li><el-tooltip class="head-menu-item" effect="dark" content="采集点分布图" placement="bottom"><i class="el-icon-office-building" @click="scattergram"></i></el-tooltip></li>
            <li><el-tooltip class="head-menu-item" effect="dark" content="全屏" placement="bottom"><i :class="isFullScreen?'el-icon-aim':'el-icon-full-screen'" @click="getFullCreeen"></i></el-tooltip></li>
            <li style="margin-right: 10px;" v-if="weatherDesc === 'OK'"><el-tooltip class="head-menu-item" effect="dark" :content="weatherType" placement="bottom"><i :class="weatherIcon"></i></el-tooltip></li>
            <li><div>{{ time }}</div></li>
          </ul>
        </div>
        <!--<div class="head-right-menu"><ul><li class="active"><i class="el-icon-menu"></i></li></ul></div>-->
        <div class="head-right-menu">
          <ul>
            <li v-for="(item,index) in mainMenuList" :key="index" @click="clickMainMenu(index)" v-bind:class="{active:index==isactive}">{{ item.text }}</li>
          </ul>
        </div>
        <el-drawer :visible.sync="drawer" :with-header="false" size="91%">
          <div class="drawerContent">
            <div class="drawerMaskBg"></div>
            <i class="close-drawer el-icon-close text-size-large" @click="drawer=false"></i>
            <div class="mapContent">
              <div class="mapContentTop">
                <div style="position: relative;height: 100%;">
                  <el-popover v-for="(item,index) in drawerTopAreaOption" placement="bottom" :title="item.title" width="200" trigger="click" @show="showAreaInfo(item.title)" :key="index">
                    <div slot="reference" class="mapContentItem" :style="{width:item.width, height: item.height,top: item.top,left: item.left}"><div class="mapItemPoint" :style="{marginLeft: item.marginLeft}"></div></div>
                    <el-radio-group v-model="energyType" fill="#082F4C" size="mini">
                      <el-radio-button v-for="(item,index) in energyTypeList" border :key="item.index" :label="item.label" :value="item.value"></el-radio-button>
                    </el-radio-group>
                  </el-popover>
                </div>
              </div>
              <div class="mapContentBottom">
                <div style="position: relative;height: 100%;">
                  <el-popover v-for="(item,index) in drawerBottomAreaOption" placement="bottom" :title="item.title" width="200" trigger="click" @show="showAreaInfo(item.title)" :key="index">
                    <div slot="reference" class="mapContentItem" :style="{width:item.width, height: item.height,top: item.top,left: item.left}"><div class="mapItemPoint" :style="{marginLeft: item.marginLeft}"></div></div>
                    <el-radio-group v-model="energyType" fill="#082F4C" size="mini">
                      <el-radio-button v-for="(item,index) in energyTypeList" border :key="item.index" :label="item.label" :value="item.value"></el-radio-button>
                    </el-radio-group>
                  </el-popover>
                </div>
              </div>
            </div>
          </div>
        </el-drawer>
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
      weatherDesc:"",
      weatherType:"",
      weatherIcon:"",
      areaObj:{
        areaName:""
      },
      drawer: false,
      drawerTopAreaOption:[
        {title:"污水站",width: "120px",height:"33%",top:"23%",left:"3%",marginLeft:"70px"},
        {title:"锅炉房",width: "220px",height:"23%",top:"17%",left:"15%",marginLeft:"140px"},
        {title:"提取二车间",width: "220px",height:"17%",top:"40%",left:"15%",marginLeft:"100px"},
        {title:"综合车间",width: "250px",height:"28%",top:"60%",left:"10%",marginLeft:"100px"},
        {title:"新建综合制剂车间",width: "100px",height:"45%",top:"18%",left:"34%",marginLeft:"30px"},
        {title:"研发中心",width: "60px",height:"43%",top:"18%",left:"44%",marginLeft:"30px"},
        {title:"原提取车间",width: "90px",height:"15%",top:"33%",left:"50%",marginLeft:"30px"},
        {title:"前处理车间",width: "90px",height:"17%",top:"45%",left:"58%",marginLeft:"40px"},
        {title:"好护士健康科技车间",width: "220px",height:"17%",top:"57%",left:"46%",marginLeft:"80px"},
        {title:"固体制剂车间",width: "280px",height:"28%",top:"74%",left:"48%",marginLeft:"60px"},
      ],
      drawerBottomAreaOption:[
        {title:"展览室",width: "150px",height:"45%",top:"17%",left:"15%",marginLeft:"70px"},
        {title:"办公楼",width: "360px",height:"48%",top:"10%",left:"25%",marginLeft:"140px"},
      ],
      energyType:"电表",
      energyTypeList:[
        {label:"电表",value:"电"},
        {label:"水表",value:"水"},
        {label:"汽表",value:"汽"}
      ]
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
    this.getWeather()
  },
  methods:{
    getMenuHeight(){
      this.selfHeight.height = window.innerHeight - 210+'px';
    },
    clickSubMenu(areaName,url){  //点击左菜单跳转
      this.areaObj.areaName = areaName
      this.$router.push({
        path:url,
        query:{
          t:Date.now()
        }
      })
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
        var params = {
          tableName: "AreaTable",
          limit:1000,
          offset:0
        }
        var arr = []
        this.axios.get("/api/CUID",{params:params}).then(res =>{
          var resData = JSON.parse(res.data).rows
          arr.push({
            name:"整厂区",
            url:"/Areas?areaName=整厂区"
          })
          for(var i=0;i < resData.length;i++){
            arr.push({
              name:resData[i].AreaName,
              url:"/Areas?areaName=" + resData[i].AreaName
            })
          }
        },res =>{
          console.log("获取车间时请求错误")
        })
        this.subMenulist = [
          {name: "桓仁厂区", icon: "el-icon-location-outline", children:arr},
          {name: "能效分析", icon: "el-icon-time", url: "/EfficiencyAnalysis"},
          {name: "综合报表", icon: "el-icon-document", url: "/DataReport"},
          {name: "综合维护表", icon: "el-icon-s-operation", url: "/MaintainedBoard"},
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
    beforeDestroy() {  //时间定时器
      if (this.timer) {
        clearInterval(this.timer);
      }
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
          city: "昆明",
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
        }
      })
    },
    scattergram(){
      this.drawer = true
    },
    showAreaInfo(AreaName){
      console.log(AreaName)
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
    opacity: 0.52;
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
</style>
