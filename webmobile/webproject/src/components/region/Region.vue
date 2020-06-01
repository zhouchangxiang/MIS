<template>
    <div class="show-box">
      <van-loading size="24px" vertical v-if="loading" color="lightgreen" type="spinner">加载中...</van-loading>
      <van-sticky>
         <div class="tabbar">
          <van-tabs v-model="active" line-height="0px" line-width="0px" @click="getData()" :swipeable=true :border=false title-active-color="#3fb5b0" title-inactive-color="#000">
            <van-tab :title="item" v-for="(item,index) in list" :key="index"></van-tab>
          </van-tabs>
      </div>
      </van-sticky>
      <div class="date-choose">
        <van-cell title="选择时间段" :value="comparedate" @click="show = true" />
          <van-calendar v-model="show" @confirm="onConfirm" type="range" :min-date="minDate" :max-date="maxDate" color="#07c160"/>
      </div>
      <div class="compare">
        <div class="c1" :class="{switchbgc:bgc1}" @click="switchShow1()">
          <div class="icon electric"></div>
          <div class="dw electric1">kwh</div>
          <div class="number">{{electric}}</div>
        </div>
         <div class="c2" :class="{switchbgc:bgc2}" @click="switchShow2()">
          <div class="icon water"></div>
          <div class="dw water">T</div>
          <div class="number">{{water}}</div>
        </div>
        <div class="c3" :class="{switchbgc:bgc3}" @click="switchShow3()">
          <div class="icon steam"></div>
          <div class="dw">T</div>
          <div class="number">{{steam}}</div>
        </div>
      </div>
      <div class="show-banner"  v-if="this.kind==='电'">
         <div class="header">电能明细</div>
                <div class="body">
                    <div class='today-water'>尖时刻</div>
                    <div class='today-water-max'>用量:</div>
                    <div class='today-water-min'>成本:</div>
                    <div class='today-num2'>{{bovalue}}</div>
                    <div class='today-num3'>{{bocost}}</div>
              </div>
              <div class="body2">
                    <div class='today-water'>峰时刻</div>
                    <div class='today-water-max'>用量:</div>
                    <div class='today-water-min'>成本:</div>
                    <div class='today-num2'>{{fenvalue}}</div>
                    <div class='today-num3'>{{fencost}}</div>
              </div>
              <div class="body3">
                    <div class='today-water'>平时刻</div>
                    <div class='today-water-max'>用量:</div>
                    <div class='today-water-min'>成本:</div>
                    <div class='today-num2'>{{pinvalue}}</div>
                    <div class='today-num3'>{{pincost}}</div>
              </div>
              <div class="body4">
                    <div class='today-water'>谷时刻</div>
                    <div class='today-water-max'>用量:</div>
                    <div class='today-water-min'>成本:</div>
                    <div class='today-num2'>{{guvalue}}</div>
                    <div class='today-num3'>{{gucost}}</div>
              </div>
      </div>
      <div class="show-banner" v-if="this.kind==='水'">
         <div class="header">水能明细</div>
                <div class="body">
                    <div class='today-water'>灌溉水</div>
                    <div class='today-water-max'>水能耗:</div>
                    <div class='today-water-min'>水成本:</div>
                    <div class='today-num2'>{{waterGG}}</div>
                    <div class='today-num3'>{{waterGGcost}}</div>
              </div>
              <div class="body2">
                    <div class='today-water'>饮用水</div>
                    <div class='today-water-max'>水能耗:</div>
                    <div class='today-water-min'>水成本:</div>
                    <div class='today-num2'>{{waterYY}}</div>
                    <div class='today-num3'>{{waterYYcost}}</div>
              </div>
              <div class="body3">
                    <div class='today-water'>深井水</div>
                    <div class='today-water-max'>水能耗:</div>
                    <div class='today-water-min'>水成本:</div>
                    <div class='today-num2'>{{waterSJ}}</div>
                    <div class='today-num3'>{{waterSJcost}}</div>
              </div>
              <div class="body4">
                    <div class='today-water'>综合</div>
                    <div class='today-water-max'>总能耗:</div>
                    <div class='today-water-min'>总成本:</div>
                    <div class='today-num2'>{{water}}t</div>
                    <div class='today-num3'>{{waterCost}}</div>
              </div>
      </div>
       </div>
</template>
<script>
var moment=require('moment')
export default {
    data(){
      this.chartSettings = {
        yAxisType: ['KMB'],
        yAxisName: ['数值']
      }
        return {
           ChartExtend: {
            grid:{
                    left:'0',
                    right:'20px',
                    bottom:'0px',
                    top:'40px'
            },
        },
          comparedate: 'click me!',
          show: false,
          minDate: new Date(2020, 0, 1),
          maxDate: new Date(2020, 11, 31),
          active:0,
          list:["原提取车间","固体制剂车间","新建综合制剂车间","GMP车间","中试车间","污水站","锅炉房","前处理车间","提取二车间","综合车间","办公楼＼食堂"],
          water:0,
          electric:0,
          steam:0,
          todaywater:0,
          todayelectric:0,
          todaysteaowfootm:0,
          yesterdaywater:0,
          yesterdayelectric:0,
          yesterdaysteam:0,
          cost1:[],
          cost:'',
          bgc1:false,
          bgc2:false,
          bgc3:false,
          loading:false,
          websoc:null,
          kind:'电',
          currentchoice:'原提取车间',
          kong:null,
          ElectricEqList:[],
          WaterEqList:[],
          SteamEqList:[],
          watertag:'',
          electrictag:'',
          steamtag:'',
          waterbatch:0,
          steambatch:0,
          ClanderStartTime:'',
          ClanderEndTime:'', 
          waterGG:0,
          waterGGcost:0,
          waterYY:0,
          waterYYcost:0,
          waterSJ:0, 
          waterSJcost:0,
          waterCost:0,
          bovalue:0,
          bocost:0,
          fenvalue:0,
          fencost:0,
          pinvalue:0,
          pincost:0,
          guvalue:0,
          gucost:0,
          electricChartData:{
          columns:['日期', '数值'],
          rows: [
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""}]
        },
        resetChartData: {
          columns: ['日期', '数值'],
          rows: [
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""}]
        },
          waterChartData: {
          columns: ['日期', '数值'],
          rows: [
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""}]
        },
        steamChartData:{
          columns: ['日期', '数值'],
          rows: [
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""}]
        }}
    },
    created(){
      this.getData()
    },
    methods:{
      formatDate(date) {
      var month=`${date.getMonth()+1}`.padStart(2, 0)
      var day=`${date.getDate()}`.padStart(2, 0)
      return `${date.getFullYear()}-${month}-${day}`;
      },
      onConfirm(date) {
      this.show = false
      const [start, end] = date;
      this.comparedate =`${this.formatDate(start)} - ${this.formatDate(end)}`;
      this.ClanderStartTime=`${this.formatDate(start)}`
      this.ClanderEndTime=`${this.formatDate(end)}`
      var nowTime = '23:59'
      var compareDateStartTime = moment(this.ClanderStartTime).day(moment(this.ClanderStartTime).day()).startOf('day').format('YYYY-MM-DD HH:mm')
      var compareDateEndTime = moment(this.ClanderEndTime).format('YYYY-MM-DD') + " " + nowTime
      this.$http.all([
            this.$http.get('/api/energywater',{params:{StartTime:compareDateStartTime,EndTime:compareDateEndTime,AreaName:this.currentchoice}}),
            this.$http.get('/api/energyelectric',{params:{StartTime:compareDateStartTime,EndTime:compareDateEndTime,AreaName:this.currentchoice}}),
            this.$http.get('/api/energysteam',{params:{StartTime:compareDateStartTime,EndTime:compareDateEndTime,AreaName:this.currentchoice}}),
            this.$http.get('/api/watertrendlookboard',{params:{StartTime:compareDateStartTime,EndTime:compareDateEndTime,AreaName:this.currentchoice}}),
            this.$http.get('/api/electricnergycost',{params:{StartTime:compareDateStartTime,EndTime:compareDateEndTime,AreaName:this.currentchoice,TimeClass:'电'}})
            ]).then(this.$http.spread((res1,res2,res3,res4,res5)=>{
             this.water=JSON.parse(res1.data).value
             this.electric=JSON.parse(res2.data).value
             this.steam=JSON.parse(res3.data).value
             var newlist=[]
             newlist.push(JSON.parse(res1.data).cost)
             newlist.push(JSON.parse(res2.data).cost)
             newlist.push(JSON.parse(res3.data).cost)
             this.cost1=newlist
             this.waterGG = res4.data.GG+'t'
             this.waterGGcost=res4.data.GGcost+'元'
             this.waterYY = res4.data.YY+'t'
             this.waterYYcost=res4.data.YYcost+'元'
             this.waterSJ = res4.data.SJ+'t'
             this.waterSJcost=res4.data.GGcost+'元'
             this.waterCost = (res4.data.GGcost + res4.data.YYcost + res4.data.SJcost).toFixed(2)+'元'
             this.bovalue=res5.data.periodTimeTypeItem[0].expendEnergy+'kwh'
             this.bocost=res5.data.periodTimeTypeItem[0].expendPrice+'元'
             this.fenvalue=res5.data.periodTimeTypeItem[1].expendEnergy+'kwh'
             this.fencost=res5.data.periodTimeTypeItem[1].expendPrice+'元'
             this.pinvalue=res5.data.periodTimeTypeItem[2].expendEnergy+'kwh'
             this.pincost=res5.data.periodTimeTypeItem[2].expendPrice+'元'
             this.guvalue=res5.data.periodTimeTypeItem[3].expendEnergy+'kwh'
             this.gucost=res5.data.periodTimeTypeItem[3].expendPrice+'元'
              }))
      },
      switchShow1(){
      this.kind='电'
      this.bgc1=!this.bgc1
      this.bgc2=this.bgc3=false
      this.kong=this.resetChartData
      if(this.bgc1){
        this.$toast('当前显示电数据')
       }
       this.cost=this.cost1[1]
      },
      switchShow2(){
       this.bgc2=!this.bgc2
       this.bgc1=this.bgc3=false
       this.kind='水'
       this.kong=this.resetChartData
       if(this.bgc2){
         this.$toast('当前显示水数据')
       }
       this.cost=this.cost1[0]
      },
      switchShow3(){
       this.bgc1=this.bgc2=false
       this.bgc3=!this.bgc3
       this.kind='汽'
       this.kong=this.SteamEqList=this.resetChartData
       if(this.bgc3){
         this.$toast('当前显示汽数据')
       }
       this.cost=this.cost1[2]
      },
        //点击导航栏获取相关能耗数据
        getData(e){
          var nowTime = moment().format('HH:mm').substring(0,4) + "0"
          var todayStartTime = moment().format('YYYY-MM-DD') + " 00:00"
          var todayEndTime = moment().format('YYYY-MM-DD') + " " + nowTime
          let params1={
            StartTime:todayStartTime,
            EndTime:todayEndTime,
            AreaName:this.list[this.active]
          }
          this.$toast('当前数据展示'+this.currentchoice)
          this.$http.all([
            this.$http.get('/api/energywater',{params:params1}),
            this.$http.get('/api/energyelectric',{params:params1}),
            this.$http.get('/api/energysteam',{params:params1}),
            this.$http.get('/api/watertrendlookboard',{params:params1}),
            this.$http.get('/api/electricnergycost',{params:{StartTime:todayStartTime,EndTime:todayEndTime,AreaName:this.currentchoice,TimeClass:'电'}})
            ]).then(this.$http.spread((res4,res5,res6,res7,res8)=>{
                    this.bgc1=this.bgc2=this.bgc3=false
                    this.water=JSON.parse(res4.data).value
                    this.todaywater=JSON.parse(res4.data).value
                    this.todayelectric=JSON.parse(res5.data).value
                    this.electric=JSON.parse(res5.data).value
                    this.todaysteam=JSON.parse(res6.data).value
                    this.steam=JSON.parse(res6.data).value
                    var newlist=[]
                    newlist.push(JSON.parse(res4.data).cost)
                    newlist.push(JSON.parse(res5.data).cost)
                    newlist.push(JSON.parse(res6.data).cost)
                    this.cost1=newlist
                    this.waterGG = res7.data.GG+'t'
                    this.waterGGcost=res7.data.GGcost+'元'
                    this.waterYY = res7.data.YY+'t'
                    this.waterYYcost=res7.data.YYcost+'元'
                    this.waterSJ = res7.data.SJ+'t'
                    this.waterSJcost=res7.data.GGcost+'元'
                    this.waterCost = (res7.data.GGcost + res7.data.YYcost + res7.data.SJcost).toFixed(2)+'元'
                    this.bovalue=res8.data.periodTimeTypeItem[0].expendEnergy+'kwh'
                    this.bocost=res8.data.periodTimeTypeItem[0].expendPrice+'元'
                    this.fenvalue=res8.data.periodTimeTypeItem[1].expendEnergy+'kwh'
                    this.fencost=res8.data.periodTimeTypeItem[1].expendPrice+'元'
                    this.pinvalue=res8.data.periodTimeTypeItem[2].expendEnergy+'kwh'
                    this.pincost=res8.data.periodTimeTypeItem[2].expendPrice+'元'
                    this.guvalue=res8.data.periodTimeTypeItem[3].expendEnergy+'kwh'
                    this.gucost=res8.data.periodTimeTypeItem[3].expendPrice+'元'
                  }))
              }
    }
}
</script>
<style lang="less" scoped>
    @bgca:#3D4048FF;
    @bgcc:#eee;
    @bgct:#ccc;
     .show-box{
        position: relative;
        width: 375px;
        height:600px;
        box-sizing: border-box;
        padding: 0 12px 12px 13px;
        background: @bgcc;
        .tabbar{
          position: relative;
          padding-top: 10px;
          height: 25px;
          font-size:14px;
          font-family:PingFang SC;
          font-weight:400;
          line-height:25px;
          color:rgba(255,255,255,1);
          opacity:1;
          margin-bottom: 20px;
        }
        .date-choose{
          height: 55px;
          width: 100%;
        }
        .compare{
          width:100%;
          height:150px;
          opacity:1;
          margin-bottom: 17px;
          .icon{
            position: absolute;
            top:23px;
            left:44px;
            width: 17.44px;
            height: 21.15px;
          &.electric{
            background-image: url('../../assets/png/flashlight_1.png');
            width:18px;
            background-size: cover;
          }
          &.water{
            background-image: url('../../assets/png/water.png');
            width:16px;
            background-size: cover;
          }
          &.steam{
            background-image: url('../../assets/png/steam.png');
            background-size: cover;
            width:21px;
          }
          }
          .dw{
            position: absolute;
            left: 51px;
            top: 58px;
            width: 15px;
            height: 11px;
            font-size:8px;
            font-family:PingFang SC;
            font-weight:400;
            line-height:11px;
            color:rgba(20, 20, 20,1);
            opacity:1;
            &.electric1{
              left:42px;
            }
            &.water{
              left:49px;
            }
          }
          .number{
            position: absolute;
            left: 4px;
            top: 85px;
            text-align: center;
            width:97px;
            height:22px;
            overflow: hidden;
            text-overflow: hidden;
            background:#ccc;
            box-shadow:0px 0px 6px rgba(255,255,255,0.16);
            border-radius:4px;
            font-size:16px;
            font-family:PingFang SC;
            font-weight:500;
            color:rgb(20, 20, 20);
            letter-spacing:1px;
            opacity:1;
          }
          .sn{
            position: absolute;
            left: 40px;
            top: 142px;
            width:60px;
            height:17px;
            font-size:12px;
            font-family:PingFang SC;
            font-weight:500;
            line-height:17px;
            opacity:1;
          }
        .maxcolor{
          color:red;
        }
        .mincolor{
          color:green;
        }
          .c1{
            position: relative;
            width:103px;
            height:150px;
            background:#ccc;
            float: left;
            margin-right: 20px;
            border-radius:4px;
          }
          .c2{
            position: relative;
            height:150px;
            width:103px;
            background:#ccc;
            float: left;
            margin-right: 20px;
            border-radius:4px;
          }
          .c3{
            position: relative;
            width: 103px;
            height:150px;
            float: left;
            background:#ccc;
            border-radius:4px;
          }
          .switchbgc{
            background-color: #fff;
            .number{
              background-color:#fff;
            }
          }
        }
        .show-banner{
          position: relative;
          height: 260px;
          width: 100%;
          margin-bottom: 17px;
          background: #ccc;
          border-radius: 4px;
            .header{
              position: relative;
                width: 100%;
                height:20px;
                padding-top: 10px;
                text-align: center;
                font-size:16px;
                font-family:PingFang SC;
                font-weight:500;
                line-height:20px;
                color:#000;
                opacity:1;
            }
            .body,.body2,.body3,.body4{
                position: relative;
                height: 55px;
            }
                .today-water,.today-water-max,.today-water-min{
                position: absolute;
                top:10px;
                left:10px;
                height:11px;
                font-size:12px;
                font-family:PingFang SC;
                font-weight:400;
                line-height:11px;
                color:#222;
                opacity:1;
                }
                .today-water-max{
                    left:120px;
                }
                .today-water-min{
                    left:246px;
                }
                .today-num1,.today-num2,.today-num3{
                    position:absolute;
                    top:30px;
                    left:10px;
                    font-size: 10px;
                    color:#fff;
                }
                .today-num2{
                  left: 120px;
                }
                .today-num3{
                  left: 246px;
                }
        }
     }
</style>