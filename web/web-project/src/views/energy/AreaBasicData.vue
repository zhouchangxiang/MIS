<template>
  <el-row :gutter="2">
    <el-col :span="24">
      <el-form :inline="true" :model="formParameters">
        <el-form-item label="时间：">
          <el-radio-group v-model="formParameters.resourceTime" fill="#082F4C" size="mini" @change="getChartData">
            <el-radio-button v-for="item in radioTimeList" border :key="item.name" :label="item.name"></el-radio-button>
          </el-radio-group>
          <el-date-picker type="date" v-model="formParameters.date" :picker-options="pickerOptions" size="mini" format="yyyy-MM-dd" style="width: 150px;" :clearable="false" @change="getChartData"></el-date-picker>
        </el-form-item>
        <el-form-item style="float: right;">
          <el-radio-group v-model="formParameters.energy" fill="#082F4C" size="mini" @change="getChartData">
            <el-radio-button v-for="item in energyList" :key="item.id" :label="item.name"></el-radio-button>
          </el-radio-group>
        </el-form-item>
      </el-form>
    </el-col>
    <el-col :span="24" style="margin-bottom:2px;">
      <div class="chartHead text-size-large text-color-info">
        <div class="chartTile">趋势图</div>
        <ul class="subsectionList">
          <li v-for="item in subsectionList"><a href="javascript:;" :class="{active:subsectionActive === item.id}" @click="getSubsection(item.id)">{{ item.name }}</a></li>
        </ul>
      </div>
    </el-col>
    <el-col :span="24">
      <div class="energyDataContainer">
        <ve-line :data="chartData" :extend="ChartExtend"></ve-line>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  var moment = require('moment');
  export default {
    name: "AreaBasicData",
    inject:['newAreaName'],
    data(){
      return {
        formParameters:{
          resourceTime:"实时",
          date:moment().format("YYYY-MM-DD HH:mm"),
          energy:"电"
        },
        radioTimeList:[
          {name:"实时"},
          {name:"日"},
          {name:"周"},
          {name:"月"},
          {name:"季"},
          {name:"年"}
        ],
        pickerOptions:{
          disabledDate(time) {
            return time.getTime() > Date.now();
          }
        },
        energyList:[
          {name:"电"},
          {name:"水"},
          {name:"汽"},
        ],
        subsectionList:[
          {name:"小时",id:1},
          {name:"30分钟",id:2},
          {name:"15分钟",id:3},
          {name:"5分钟",id:4},
          {name:"1分钟",id:5}
        ],
        subsectionActive:1,
        ChartExtend: {
          grid:{
            left:'0',
            right:'0',
            bottom:'0',
            top:'40px'
          },
          series:{
            smooth: false
          }
        },
        chartData: {
          columns: ['时间', '总有功电量', 'A相有功电量', 'B相有功电量','C相有功电量'],
          rows: []
        }
      }
    },
    created(){
      this.getChartData();
    },
    destroyed() {
      this.websock.close() //离开路由之后断开websocket连接
    },
    methods:{
      getSubsection(index){
        this.subsectionActive = index;
      },
      getChartData(){
        if(this.formParameters.resourceTime === "实时"){
          this.initWebSocket()
        }else{
          this.websock.close()
          var that = this
          var nowTime = moment().format('HH:mm').substring(0,4) + "0"
          var dayStartTime = moment(this.formParameters.date).format('YYYY-MM-DD') + " 00:00"
          var dayEndTime = moment(this.formParameters.date).format('YYYY-MM-DD') + " " + nowTime
          var weekStartTime = moment(this.formParameters.date).week(moment(this.formParameters.date).week()).startOf('week').format('YYYY-MM-DD HH:mm')
          var weekEndTime = moment(this.formParameters.date).week(moment(this.formParameters.date).week()).endOf('week').format('YYYY-MM-DD HH:mm')
          var monthStartTime = moment(this.formParameters.date).month(moment(this.formParameters.date).month()).startOf('month').format('YYYY-MM-DD HH:mm')
          var monthEndTime = moment(this.formParameters.date).month(moment(this.formParameters.date).month()).endOf('month').format('YYYY-MM-DD HH:mm')
          var quarterStartTime = moment(this.formParameters.date).quarter(moment(this.formParameters.date).quarter()).startOf('quarter').format('YYYY-MM-DD HH:mm')
          var quarterEndTime = moment(this.formParameters.date).quarter(moment(this.formParameters.date).quarter()).endOf('quarter').format('YYYY-MM-DD HH:mm')
          var yearStartTime = moment(this.formParameters.date).year(moment(this.formParameters.date).year()).startOf('year').format('YYYY-MM-DD HH:mm')
          var yearEndTime = moment(this.formParameters.date).year(moment(this.formParameters.date).year()).endOf('year').format('YYYY-MM-DD HH:mm')
          var params = {}
          var areaName = ""
          if(this.newAreaName.areaName === "整厂区"){
            areaName = ""
          }else{
            areaName = this.newAreaName.areaName
          }
          if(this.formParameters.resourceTime === "日"){
            params.StartTime = dayStartTime
            params.EndTime = dayEndTime
            params.AreaName = areaName
            params.EnergyClass = this.formParameters.energy
          }else if(this.formParameters.resourceTime === "周"){
            params.StartTime = weekStartTime
            params.EndTime = weekEndTime
            params.AreaName = areaName
            params.EnergyClass = this.formParameters.energy
          }else if(this.formParameters.resourceTime === "月"){
            params.StartTime = monthStartTime
            params.EndTime = monthEndTime
            params.AreaName = areaName
            params.EnergyClass = this.formParameters.energy
          }else if(this.formParameters.resourceTime === "季"){
            params.StartTime = quarterStartTime
            params.EndTime = quarterEndTime
            params.AreaName = areaName
            params.EnergyClass = this.formParameters.energy
          }else if(this.formParameters.resourceTime === "年"){
            params.StartTime = yearStartTime
            params.EndTime = yearEndTime
            params.AreaName = areaName
            params.EnergyClass = this.formParameters.energy
          }
          console.log(params)
          this.axios.get("/api/energydetail",{params:params}).then(res => {
            console.log(res.data)
          })
        }
      },
      initWebSocket(){ //初始化weosocket
        const wsuri = "ws://127.0.0.1:5002";
        this.websock = new WebSocket(wsuri);
        this.socketLoading = true
        this.websock.onmessage = this.websocketonmessage;
        this.websock.onopen = this.websocketonopen;
        this.websock.onerror = this.websocketonerror;
        this.websock.onclose = this.websocketclose;
      },
      websocketonopen(){ //连接建立之后执行send方法发送数据
        this.websocketsend();
      },
      websocketonerror(){//连接建立失败
        //this.initWebSocket();
        console.log("连接失败")
      },
      websocketonmessage(e){ //数据接收
        this.socketLoading = false
        const resdata = JSON.parse(e.data);
        console.log(resdata)
        // for(var i=0;i<resdata.length;i++){
        //   if(resdata[i].AreaName === "" || resdata[i].AreaName === "整厂区"){
        //     this.chartData.rows.push({
        //       "时间": moment(new Date()).format("HH:mm:ss"),
        //       "总功率": this.electricChartValue
        //     })
        //   }
        // }
      },
      websocketsend(Data){//数据发送
        this.websock.send(Data);
      },
      websocketclose(e){  //关闭
        console.log('断开连接');
      }
    }
  }
</script>

<style scoped>
  .sortHandle{
    float: right;
    display: flex;
    color: #9B9B9B;
    font-size: 14px;
    margin-right: 15px;
  }
  .sortHandle a{
    display: block;
    font-size: 14px;
    color: #9B9B9B;
    text-decoration: none;
    height: 46px;
    line-height: 46px;
    padding: 0 5px;
  }
</style>
