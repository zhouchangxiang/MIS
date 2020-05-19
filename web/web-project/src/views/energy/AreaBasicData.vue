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
        <el-select v-model="areaName" size="mini" @change="getEq" v-if="newAreaName.areaName === '整厂区' || $route.query.areaName === '整厂区' && formParameters.resourceTime === '实时'">
          <el-option v-for="(item,index) in areaList" :key="index" :label="item.label" :value="item.value"></el-option>
        </el-select>
        <el-select v-model="ElectricEqActive" size="mini" @change="getChartData" v-if="formParameters.energy ==='电'">
          <el-option v-for="(item,index) in ElectricEqList" :key="index" :label="item.FEFportIP" :value="item.TagClassValue"></el-option>
        </el-select>
        <el-select v-model="WaterEqActive" size="mini" @change="getChartData" v-if="formParameters.energy ==='水'">
          <el-option v-for="(item,index) in WaterEqList" :key="index" :label="item.FEFportIP" :value="item.TagClassValue"></el-option>
        </el-select>
        <el-select v-model="SteamEqActive" size="mini" @change="getChartData" v-if="formParameters.energy ==='汽'">
          <el-option v-for="(item,index) in SteamEqList" :key="index" :label="item.FEFportIP" :value="item.TagClassValue"></el-option>
        </el-select>
        <div class="chartHeadRight">
          <span class="text-size-small text-color-primary" @click="$router.push({ path:'/DataReport'})" style="float: right;cursor: pointer;">查看报表</span>
        </div>
      </div>
    </el-col>
    <el-col :span="24">
      <div class="energyDataContainer">
        <ve-chart :data="chartData" :extend="ChartExtend" :settings="chartSettings" :data-zoom="dataZoom" v-loading="chartsLoading"></ve-chart>
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
        ElectricEqList:[],
        ElectricEqActive:"",
        WaterEqList:[],
        WaterEqActive:"",
        SteamEqList:[],
        SteamEqActive:"",
        dataZoom: [],
        ChartExtend: {
          grid:{
            left:'10px',
            right:'10px',
            bottom:'40px',
            top:'40px'
          },
          series:{
            barMaxWidth : 50,
            smooth: false,
            label:{
              show: true,
              position: "top"
            }
          }
        },
        chartSettings: {
          type:"",
          yAxisName:[]
        },
        chartData: {
          columns: [],
          rows: []
        },
        chartsLoading:false,
        source:null,
        areaList:[],
        areaName:"",
      }
    },
    created(){
      this.getArea()
    },
    destroyed() {
      if(this.websock){
        this.websock.close() //离开路由之后断开websocket连接
      }
    },
    methods:{
      getArea(){
        var params = {
          tableName: "AreaTable",
          limit:1000,
          offset:0
        }
        this.axios.get("/api/CUID",{params:params}).then(res =>{
          var resData = JSON.parse(res.data).rows
          resData.forEach(item =>{
            this.areaList.push({
              label:item.AreaName,
              value:item.AreaName
            })
          })
          this.areaName = resData[0].AreaName
          this.getEq()
        })
      },
      getEq(){
        this.ElectricEqList = []
        this.WaterEqList = []
        this.SteamEqList = []
        let that = this
        if(this.$route.query.areaName != "整厂区"){
          this.areaName = this.$route.query.areaName
        }
        var params = {
          tableName:"TagDetail",
          field:"AreaName",
          fieldvalue:this.areaName,
          limit:100000,
          offset:0
        }
        this.axios.get("/api/CUID",{params:params}).then(res =>{
          var rows = JSON.parse(res.data).rows
          rows.forEach(item =>{
            if(item.EnergyClass === "电"){
              that.ElectricEqList.push(item)
              if(that.ElectricEqList[0].TagClassValue){
                that.ElectricEqActive = that.ElectricEqList[0].TagClassValue
                that.getChartData()
              }else{
                that.ElectricEqActive = ""
              }
            }else if(item.EnergyClass === "水"){
              that.WaterEqList.push(item)
              if(that.WaterEqList[0].TagClassValue){
                that.WaterEqActive = that.WaterEqList[0].TagClassValue
                that.getChartData()
              }else{
                that.WaterEqActive = ""
              }
            }else if(item.EnergyClass === "汽"){
              that.SteamEqList.push(item)
              if(that.SteamEqList[0].TagClassValue){
                that.SteamEqActive = that.SteamEqList[0].TagClassValue
                that.getChartData()
              }else{
                that.SteamEqActive = ""
              }
            }
          })
        })
      },
      cancel(){
        this.source.cancel('关闭axios请求')
      },
      getChartData(){
        if(this.formParameters.resourceTime === "实时"){
          this.chartsLoading = true
          this.dataZoom = []
          this.chartSettings.type = "line"
          this.ChartExtend.series.label.show = false
          if(this.websock){
            this.websock.close()
          }
          if(this.source){
            this.cancel()
          }
          if(this.formParameters.energy === "电"){
            this.chartSettings.yAxisName = ["kW·h"]
            this.chartData = {
              columns: ["时间","总功率"],
              rows: [
                { '时间': moment().subtract(40, 's').format("HH:mm:ss"), '总功率': null},
                { '时间': moment().subtract(38, 's').format("HH:mm:ss"), '总功率': null},
                { '时间': moment().subtract(36, 's').format("HH:mm:ss"), '总功率': null},
                { '时间': moment().subtract(34, 's').format("HH:mm:ss"), '总功率': null},
                { '时间': moment().subtract(32, 's').format("HH:mm:ss"), '总功率': null},
                { '时间': moment().subtract(30, 's').format("HH:mm:ss"), '总功率': null},
                { '时间': moment().subtract(28, 's').format("HH:mm:ss"), '总功率': null},
                { '时间': moment().subtract(26, 's').format("HH:mm:ss"), '总功率': null},
                { '时间': moment().subtract(24, 's').format("HH:mm:ss"), '总功率': null},
                { '时间': moment().subtract(22, 's').format("HH:mm:ss"), '总功率': null},
                { '时间': moment().subtract(20, 's').format("HH:mm:ss"), '总功率': null},
                { '时间': moment().subtract(18, 's').format("HH:mm:ss"), '总功率': null},
                { '时间': moment().subtract(16, 's').format("HH:mm:ss"), '总功率': null},
                { '时间': moment().subtract(14, 's').format("HH:mm:ss"), '总功率': null},
                { '时间': moment().subtract(12, 's').format("HH:mm:ss"), '总功率': null},
                { '时间': moment().subtract(10, 's').format("HH:mm:ss"), '总功率': null},
                { '时间': moment().subtract(8, 's').format("HH:mm:ss"), '总功率': null},
                { '时间': moment().subtract(6, 's').format("HH:mm:ss"), '总功率': null},
                { '时间': moment().subtract(4, 's').format("HH:mm:ss"), '总功率': null},
                { '时间': moment().subtract(2, 's').format("HH:mm:ss"), '总功率': null}
              ]
            }
            if(this.ElectricEqList){
              this.initWebSocket()
            }
          }else if(this.formParameters.energy === "水"){
            this.chartSettings.yAxisName = ["t"]
            this.chartData = {
              columns: ['时间', '累计流量'],
              rows: [
                { '时间': moment().subtract(40, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(38, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(36, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(34, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(32, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(30, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(28, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(26, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(24, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(22, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(20, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(18, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(16, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(14, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(12, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(10, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(8, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(6, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(4, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(2, 's').format("HH:mm:ss"), '累计流量': null}
              ]
            }
            if(this.WaterEqList){
              this.initWebSocket()
            }
          }else if(this.formParameters.energy === "汽"){
            this.chartSettings.yAxisName = ["t"]
            this.chartData = {
              columns: ['时间', '累计流量'],
              rows: [
                { '时间': moment().subtract(40, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(38, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(36, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(34, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(32, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(30, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(28, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(26, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(24, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(22, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(20, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(18, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(16, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(14, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(12, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(10, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(8, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(6, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(4, 's').format("HH:mm:ss"), '累计流量': null},
                { '时间': moment().subtract(2, 's').format("HH:mm:ss"), '累计流量': null}
              ]
            }
            if(this.SteamEqList){
              this.initWebSocket()
            }
          }
        }else{
          if(this.source){
            this.cancel()
          }
          this.source = this.axios.CancelToken.source(); // 初始化source对象
          if(this.websock){
            this.websock.close()
          }
          this.chartsLoading = true
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
          var TagClassValue = ""
          if(this.newAreaName.areaName === "整厂区" || this.newAreaName.areaName === ""){
            areaName = ""
            this.ChartExtend.series.label.show = true
            TagClassValue = ""
            if(this.formParameters.energy === "电"){
              this.chartSettings.yAxisName = ["kW·h"]
            }else if(this.formParameters.energy === "水"){
              this.chartSettings.yAxisName = ["t"]
            }else if(this.formParameters.energy === "汽"){
              this.chartSettings.yAxisName = ["t"]
            }
          }else{
            areaName = this.newAreaName.areaName
            this.ChartExtend.series.label.show = false
            if(this.formParameters.energy === "电"){
              this.chartSettings.yAxisName = ["kW·h"]
              TagClassValue = this.ElectricEqActive
            }else if(this.formParameters.energy === "水"){
              this.chartSettings.yAxisName = ["t"]
              TagClassValue = this.WaterEqActive
            }else if(this.formParameters.energy === "汽"){
              this.chartSettings.yAxisName = ["t"]
              TagClassValue = this.SteamEqActive
            }
          }
          if(this.formParameters.resourceTime === "日"){
            params.StartTime = dayStartTime
            params.EndTime = dayEndTime
            params.TagClassValue = TagClassValue
            params.EnergyClass = this.formParameters.energy
            params.AreaName = areaName
          }else if(this.formParameters.resourceTime === "周"){
            params.StartTime = weekStartTime
            params.EndTime = weekEndTime
            params.TagClassValue = TagClassValue
            params.EnergyClass = this.formParameters.energy
            params.AreaName = areaName
          }else if(this.formParameters.resourceTime === "月"){
            params.StartTime = monthStartTime
            params.EndTime = monthEndTime
            params.TagClassValue = TagClassValue
            params.EnergyClass = this.formParameters.energy
            params.AreaName = areaName
          }else if(this.formParameters.resourceTime === "季"){
            params.StartTime = quarterStartTime
            params.EndTime = quarterEndTime
            params.TagClassValue = TagClassValue
            params.EnergyClass = this.formParameters.energy
            params.AreaName = areaName
          }else if(this.formParameters.resourceTime === "年"){
            params.StartTime = yearStartTime
            params.EndTime = yearEndTime
            params.TagClassValue = TagClassValue
            params.EnergyClass = this.formParameters.energy
            params.AreaName = areaName
          }
          this.axios.get("/api/energydetail",{params:params,cancelToken: this.source.token}).then(res => {
            this.chartsLoading = false
            if(areaName === ""){
              that.dataZoom = []
              that.chartSettings.type = "histogram"
              that.chartData = {
                columns: ['车间', '能耗量'],
                rows: res.data.row
              }
            }else{
              that.dataZoom = [{type: 'slider',start: 0,end: 20}]
              that.chartSettings.type = "line"
              that.chartData = {
                columns: ['时间', '能耗量'],
                rows: res.data.row
              }
            }
          })
        }
      },
      initWebSocket(){ //初始化weosocket
        // this.websock = new WebSocket('ws://' + location.host + '/socket');
        this.websock = new WebSocket('ws://127.0.0.1:5002');
        this.chartsLoading = true
        this.websock.onmessage = this.websocketonmessage;
        this.websock.onopen = this.websocketonopen;
        this.websock.onerror = this.websocketonerror;
        this.websock.onclose = this.websocketclose;
      },
      websocketonopen(){ //连接建立之后执行send方法发送数据
        this.websocketsend();
      },
      websocketonerror(){//连接建立失败
        console.log("websocket连接失败")
      },
      websocketonmessage(e){ //数据接收
        this.chartsLoading = false
        var resdata = JSON.parse(e.data);
        if(this.formParameters.energy === "电"){
          for(var key in resdata[0].electric){
            if(key === this.ElectricEqActive){
              this.chartData.rows.push({
                "时间": moment().format("HH:mm:ss"),
                "总功率": resdata[0].electric[key].ZGL
              })
              this.chartData.rows.shift()
            }
          }

        }else if(this.formParameters.energy === "水"){
          for(var key in resdata[0].water){
            if(key === this.WaterEqActive){
              this.chartData.rows.push({
                "时间": moment().format("HH:mm:ss"),
                "累计流量": resdata[0].water[key].sumValue
              })
              this.chartData.rows.shift()
            }
          }
        }else if(this.formParameters.energy === "汽"){
          for(var key in resdata[0].steam){
            if(key === this.SteamEqActive){
              this.chartData.rows.push({
                "时间": moment().format("HH:mm:ss"),
                "累计流量": resdata[0].steam[key].sumValue
              })
              this.chartData.rows.shift()
            }
          }
          this.chartData.rows.shift()
        }
      },
      websocketsend(Data){//数据发送
        this.websock.send(Data);
      },
      websocketclose(e){  //关闭
        console.log("websocket关闭")
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
