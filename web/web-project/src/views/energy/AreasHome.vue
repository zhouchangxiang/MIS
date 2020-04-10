<template>
  <el-row>
    <el-col :span="24" v-if="newAreaName.areaName == '整厂区' || newAreaName.areaName == ''">
      <el-row :gutter="30" style="margin-bottom: 15px;">
        <el-col :span="8">
          <div class="platformContainer">
            <el-col :span="24" style="border-bottom: 1px solid #d8d8d8;padding: 20px 0;">
              <el-col :span="6">
                <div class="iconBlock float-left" style="color: #FB8A06;">
                  <i class="fa fa-flash fa-2x"></i>
                </div>
              </el-col>
              <el-col :span="18">
                <div class="itemMarginBottom text-size-normol text-color-info-shallow">本日耗电量</div>
                <div class="itemMarginBottom text-size-big text-color-info">{{ todayElectricity }} {{ ElectricityUnit }}</div>
                <div class="itemMarginBottom">
                  <span class="text-size-mini text-color-info-shallow">今日电费</span>
                  <span class="text-size-mini text-color-info-shallow float-right">对比昨日</span>
                </div>
                <div class="itemMarginBottom">
                  <span class="text-size-normol text-color-info">523.5元</span>
                  <span class="text-size-normol float-right" :class="todayElectricity-yesterdayElectricityValue>0?'text-color-danger':'text-color-success'">{{ ElectricityCompare }}</span>
                </div>
              </el-col>
            </el-col>
            <el-col :span="24" style="margin-top: 20px;">
              <p class="text-size-small">- 实时数据：{{ electricChartValue }}</p>
              <ve-line :data="electricChartData" :extend="chartExtend" :legend-visible="false" height="300px"></ve-line>
            </el-col>
            <el-col :span="24" style="margin-top: 20px;">
              <p class="text-color-info-shallow">日耗量</p>
              <el-col :span="12">
                <ve-histogram :data="electricHistogram" height="200px" :extend="chartExtend" :legend-visible="false"></ve-histogram>
              </el-col>
              <el-col :span="12">
                <ve-ring :data="electricRing" :settings="ChartSettings" :extend="ChartExtend" width="100%" height="200px"></ve-ring>
              </el-col>
            </el-col>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="platformContainer">
            <el-col :span="24" style="border-bottom: 1px solid #d8d8d8;padding: 20px 0;">
              <el-col :span="6">
                <div class="iconBlock float-left" style="color: #228AD5;">
                  <i class="fa fa-tint fa-2x"></i>
                </div>
              </el-col>
              <el-col :span="18">
                <div class="itemMarginBottom text-size-normol text-color-info-shallow">本日耗水量</div>
                <div class="itemMarginBottom text-size-big text-color-info">{{ todayWater }} {{ WaterUnit }}</div>
                <div class="itemMarginBottom">
                  <span class="text-size-mini text-color-info-shallow">今日水费</span>
                  <span class="text-size-mini text-color-info-shallow float-right">对比昨日</span>
                </div>
                <div class="itemMarginBottom">
                  <span class="text-size-normol text-color-info">523.5元</span>
                  <span class="text-size-normol float-right" :class="todayWater-yesterdayWaterValue>0?'text-color-danger':'text-color-success'">{{ WaterCompare }}</span>
                </div>
              </el-col>
            </el-col>
            <el-col :span="24" style="margin-top: 20px;">
              <p class="text-size-small">- 实时数据：{{ waterChartValue }}</p>
              <ve-line :data="waterChartData" :extend="chartExtend" :legend-visible="false" height="300px"></ve-line>
            </el-col>
            <el-col :span="24" style="margin-top: 20px;">
              <p class="text-color-info-shallow">日耗量</p>
              <el-col :span="12">
                <ve-histogram :data="waterHistogram" height="200px" :extend="chartExtend" :legend-visible="false"></ve-histogram>
              </el-col>
              <el-col :span="12">
                <ve-ring :data="waterRing" :settings="ChartSettings" :extend="ChartExtend" width="100%" height="200px"></ve-ring>
              </el-col>
            </el-col>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="platformContainer">
            <el-col :span="24" style="border-bottom: 1px solid #d8d8d8;padding: 20px 0;">
              <el-col :span="6">
                <div class="iconBlock float-left" style="color: #15CC48;">
                  <i class="fa fa-tachometer fa-2x"></i>
                </div>
              </el-col>
              <el-col :span="18">
                <div class="itemMarginBottom text-size-normol text-color-info-shallow">本日耗汽量</div>
                <div class="itemMarginBottom text-size-big text-color-info">{{ todaySteam }} {{ SteamUnit }}</div>
                <div class="itemMarginBottom">
                  <span class="text-size-mini text-color-info-shallow">今日汽费</span>
                  <span class="text-size-mini text-color-info-shallow float-right">对比昨日</span>
                </div>
                <div class="itemMarginBottom">
                  <span class="text-size-normol text-color-info">523.5元</span>
                  <span class="text-size-normol float-right" :class="todaySteam-yesterdaySteamValue>0?'text-color-danger':'text-color-success'">{{ SteamCompare }}</span>
                </div>
              </el-col>
            </el-col>
            <el-col :span="24" style="margin-top: 20px;">
              <p class="text-size-small">- 实时数据：{{ steamChartValue }}</p>
              <ve-line :data="steamChartData" :extend="chartExtend" :legend-visible="false" height="300px"></ve-line>
            </el-col>
            <el-col :span="24" style="margin-top: 20px;">
              <p class="text-color-info-shallow">日耗量</p>
              <el-col :span="12">
                <ve-histogram :data="steamHistogram" height="200px" :extend="chartExtend" :legend-visible="false"></ve-histogram>
              </el-col>
              <el-col :span="12">
                <ve-ring :data="steamRing" :settings="ChartSettings" :extend="ChartExtend" width="100%" height="200px"></ve-ring>
              </el-col>
            </el-col>
          </div>
        </el-col>
      </el-row>
    </el-col>
    <el-col :span="24" v-if="newAreaName.areaName != '整厂区'">
      <el-row :gutter="15" style="margin-bottom: 15px;">
        <el-col :span="8">
          <div class="platformContainer">
            <el-col :span="6">
              <div class="iconBlock float-left" style="color: #FB8A06;">
                <i class="fa fa-flash fa-2x"></i>
              </div>
            </el-col>
            <el-col :span="18">
              <div class="itemMarginBottom text-size-normol text-color-info-shallow">本日耗电量</div>
              <div class="itemMarginBottom text-size-big text-color-info">{{ todayElectricity }} {{ ElectricityUnit }}</div>
              <div class="itemMarginBottom">
                <span class="text-size-mini text-color-info-shallow">今日电费</span>
                <span class="text-size-mini text-color-info-shallow float-right">对比昨日</span>
              </div>
              <div class="itemMarginBottom">
                <span class="text-size-normol text-color-info">523.5元</span>
                <span class="text-size-normol float-right" :class="todayElectricity-yesterdayElectricityValue>0?'text-color-danger':'text-color-success'">{{ ElectricityCompare }}</span>
              </div>
            </el-col>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="platformContainer">
            <el-col :span="6">
              <div class="iconBlock float-left" style="color: #228AD5;">
                <i class="fa fa-tint fa-2x"></i>
              </div>
            </el-col>
            <el-col :span="18">
              <div class="itemMarginBottom text-size-normol text-color-info-shallow">本日耗水量</div>
              <div class="itemMarginBottom text-size-big text-color-info">{{ todayWater }} {{ WaterUnit }}</div>
              <div class="itemMarginBottom">
                <span class="text-size-mini text-color-info-shallow">今日水费</span>
                <span class="text-size-mini text-color-info-shallow float-right">对比昨日</span>
              </div>
              <div class="itemMarginBottom">
                <span class="text-size-normol text-color-info">523.5元</span>
                <span class="text-size-normol float-right" :class="todayWater-yesterdayWaterValue>0?'text-color-danger':'text-color-success'">{{ WaterCompare }}</span>
              </div>
            </el-col>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="platformContainer">
            <el-col :span="6">
              <div class="iconBlock float-left" style="color: #15CC48;">
                <i class="fa fa-tachometer fa-2x"></i>
              </div>
            </el-col>
            <el-col :span="18">
              <div class="itemMarginBottom text-size-normol text-color-info-shallow">本日耗汽量</div>
              <div class="itemMarginBottom text-size-big text-color-info">{{ todaySteam }} {{ SteamUnit }}</div>
              <div class="itemMarginBottom">
                <span class="text-size-mini text-color-info-shallow">今日汽费</span>
                <span class="text-size-mini text-color-info-shallow float-right">对比昨日</span>
              </div>
              <div class="itemMarginBottom">
                <span class="text-size-normol text-color-info">523.5元</span>
                <span class="text-size-normol float-right" :class="todaySteam-yesterdaySteamValue>0?'text-color-danger':'text-color-success'">{{ SteamCompare }}</span>
              </div>
            </el-col>
          </div>
        </el-col>
      </el-row>
      <el-row :gutter="15">
        <el-col :span="6">
          <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
            <div class="chartTile">生产详情</div>
          </div>
          <div class="platformContainer" style="margin-bottom:2px;">
            <el-table :data="batchTableData" style="width: 100%">
              <el-table-column prop="Name" label="品名"></el-table-column>
              <el-table-column prop="Batch" label="批次"></el-table-column>
            </el-table>
          </div>
          <div class="platformContainer">
            <el-col :span="24">
              <div class="itemMarginBottom">
                <span class="text-size-normol text-color-info-shallow">今日品名数</span>
                <span class="text-size-normol text-color-info-shallow float-right">今日总成本</span>
              </div>
              <div class="itemMarginBottom">
                <span class="text-size-normol text-color-info">2</span>
                <span class="text-size-normol text-color-info float-right">24562.23元</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="itemMarginBottom">
                <span class="text-size-normol text-color-info-shallow">今日批次数</span>
              </div>
              <div class="itemMarginBottom">
                <span class="text-size-normol text-color-info">5</span>
              </div>
            </el-col>
            <el-col :span="12">
              <ve-ring :data="batchRingChartData" :settings="batchChartSettings" :extend="batchChartExtend" width="100%" height="100px"></ve-ring>
            </el-col>
          </div>
        </el-col>
        <el-col :span="13">
          <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
            <div class="chartTile">数据表</div>
          </div>
          <div class="platformContainer">

          </div>
        </el-col>
        <el-col :span="5">
          <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
            <div class="chartTile">设备情况</div>
          </div>
          <div class="platformContainer">
            <ul>
              <li v-for="item in onlineEquipmentOption" style="margin-bottom: 5px;">
                <p class="text-size-normol text-color-info">{{ item.name }}</p>
                <p class="text-size-mini text-color-info-shallow" style="margin-top: 5px;"><span>上线数/总数</span><span style="float: right;">{{ item.online }}/{{ item.total }}</span></p>
                <el-progress :text-inside="true" :stroke-width="16" :percentage="item.rate"></el-progress>
              </li>
            </ul>
          </div>
        </el-col>
      </el-row>
    </el-col>
  </el-row>
</template>

<script>
  var moment = require('moment');
  export default {
    name: "AreasHome",
    inject:['newAreaName'],
    data(){
      return {
        todayElectricity:"",
        todayWater:"",
        todaySteam:"",
        yesterdayElectricityValue:"",
        yesterdayWaterValue:"",
        yesterdaySteamValue:"",
        ElectricityUnit:"",
        WaterUnit:"",
        SteamUnit:"",
        websock:null,
        chartExtend:{
          yAxis:{
            show:false
          },
          grid:{
            left: '-40px',
            right: '0',
            bottom: '20px',
            top:'20px'
          },
          series: {
            barMaxWidth : 30,
            smooth: false,
            symbol: 'none',
            itemStyle:{
              color:"#FB8A06"
            }
          }
        },
        electricChartValue:"",
        electricChartData:{
          columns: ['时间', '功率'],
          rows: [
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
          ]
        },
        electricHistogram:{
          columns: ['时间', '功率'],
          rows: [
            { '时间': "昨日", '功率': "4645"},
            { '时间': "本日", '功率': "3454"},
            { '时间': "月均", '功率': "2547"},
          ]
        },
        electricRing:{
          columns: ['日期', '访问用户'],
          rows: [
            { '日期': '1/1', '访问用户': 1393 },
            { '日期': '1/2', '访问用户': 3530 },
            { '日期': '1/3', '访问用户': 2923 },
            { '日期': '1/4', '访问用户': 1723 },
            { '日期': '1/5', '访问用户': 3792 },
            { '日期': '1/6', '访问用户': 4593 }
          ]
        },
        waterChartValue:"",
        waterChartData:{
          columns: ['时间', '功率'],
          rows: [
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
          ]
        },
        waterHistogram:{
          columns: ['时间', '功率'],
          rows: [
            { '时间': "昨日", '功率': "4645"},
            { '时间': "本日", '功率': "3454"},
            { '时间': "月均", '功率': "2547"},
          ]
        },
        waterRing:{
          columns: ['日期', '访问用户'],
          rows: [
            { '日期': '1/1', '访问用户': 1393 },
            { '日期': '1/2', '访问用户': 3530 },
            { '日期': '1/3', '访问用户': 2923 },
            { '日期': '1/4', '访问用户': 1723 },
            { '日期': '1/5', '访问用户': 3792 },
            { '日期': '1/6', '访问用户': 4593 }
          ]
        },
        steamChartValue:"",
        steamChartData:{
          columns: ['时间', '功率'],
          rows: [
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
            { '时间': "", '功率': ""},
          ]
        },
        steamHistogram:{
          columns: ['时间', '功率'],
          rows: [
            { '时间': "昨日", '功率': "4645"},
            { '时间': "本日", '功率': "3454"},
            { '时间': "月均", '功率': "2547"},
          ]
        },
        steamRing:{
          columns: ['日期', '访问用户'],
          rows: [
            { '日期': '1/1', '访问用户': 1393 },
            { '日期': '1/2', '访问用户': 3530 },
            { '日期': '1/3', '访问用户': 2923 },
            { '日期': '1/4', '访问用户': 1723 },
            { '日期': '1/5', '访问用户': 3792 },
            { '日期': '1/6', '访问用户': 4593 }
          ]
        },
        batchTableData:[
          {Name:"药品A",Batch:"JUSA2374627"},
          {Name:"药品B",Batch:"JUSA2374627"},
          {Name:"药品C",Batch:"JUSA2374627"},
          {Name:"药品D",Batch:"JUSA2374627"},
        ],
        ChartSettings: {
          radius: [30,60],
          offsetY:"120px",
          label:{
            show:false
          },
          labelLine:{
            show:false
          }
        },
        batchChartSettings: {
          radius: [20,40],
          offsetY:"50px",
          label:{
            show:false
          },
          labelLine:{
            show:false
          }
        },
        ChartExtend: {
          legend:{
            show:true
          }
        },
        batchChartExtend: {
          legend:{
            show:false
          }
        },
        batchRingChartData: {
          columns: ['日期', '访问用户'],
          rows: [
            { '日期': '药品A', '访问用户': 1393 },
            { '日期': '药品B', '访问用户': 3530 },
            { '日期': '药品C', '访问用户': 2923 },
            { '日期': '药品D', '访问用户': 1723 }
          ]
        },
        onlineEquipmentOption:[], //在线情况采集
      }
    },
    created(){
      var that = this
      this.getEnergyPreview()
      this.initWebSocket();
      this.getOnLineEq()
    },
    destroyed() {
      this.websock.close() //离开路由之后断开websocket连接
    },
    computed:{
      ElectricityCompare(){
        if(this.todayElectricity > 0){
          var compare = (this.todayElectricity - this.yesterdayElectricityValue) / this.todayElectricity * 100
          if(this.todayElectricity - this.yesterdayElectricityValue > 0){
            return "+" + compare.toFixed(2) + "%"
          }else{
            return compare.toFixed(2) + "%"
          }
        }else{
          if(this.yesterdayElectricityValue > 0){
            return "-" + 100 + "%"
          }else{
            return 0 + "%"
          }
        }
      },
      WaterCompare(){
        if(this.todayWater > 0){
          var compare = (this.todayWater - this.yesterdayWaterValue) / this.todayWater * 100
          if(this.todayWater - this.yesterdayWaterValue > 0){
            return "+" + compare.toFixed(2) + "%"
          }else{
            return compare.toFixed(2) + "%"
          }
        }else{
          if(this.yesterdayWaterValue > 0){
            return "-" + 100 + "%"
          }else{
            return 0 + "%"
          }
        }
      },
      SteamCompare(){
        if(this.todaySteam > 0){
          var compare = (this.todaySteam - this.yesterdaySteamValue) / this.todaySteam * 100
          if(this.todaySteam - this.yesterdaySteamValue > 0){
            return "+" + compare.toFixed(2) + "%"
          }else{
            return compare.toFixed(2) + "%"
          }
        }else{
          if(this.yesterdaySteamValue > 0){
            return "-" + 100 + "%"
          }else{
            return 0 + "%"
          }
        }
      }
    },
    methods:{
      getEnergyPreview(){
        var that = this
        var nowTime = moment().format('HH:mm').substring(0,4) + "0"
        var todayStartTime = moment().format('YYYY-MM-DD') + " 00:00"
        var todayEndTime = moment().format('YYYY-MM-DD') + " " + nowTime
        var yesterdayStartTime = moment().subtract(1,'day').format('YYYY-MM-DD') + " 00:00"
        var yesterdayEndTime = moment().subtract(1,'day').format('YYYY-MM-DD') + " " + nowTime
        var params = {}
        var yesterdayParams ={}
        if(this.newAreaName.areaName == "整厂区"){
          params.StartTime = todayStartTime
          params.EndTime = todayEndTime
          yesterdayParams.StartTime = yesterdayStartTime
          yesterdayParams.EndTime = yesterdayEndTime
        }else{
          params.StartTime = todayStartTime
          params.EndTime = todayEndTime
          params.Area = this.newAreaName.areaName
          yesterdayParams.StartTime = yesterdayStartTime
          yesterdayParams.EndTime = yesterdayEndTime
          yesterdayParams.Area = this.newAreaName.areaName
        }
        this.axios.all([
          this.axios.get("/api/energyelectric",{params: params}),//获取今天电
          this.axios.get("/api/energyelectric",{params: yesterdayParams}),//获取昨天电
          this.axios.get("/api/energywater",{params: params}),//获取今天水
          this.axios.get("/api/energywater",{params: yesterdayParams}),//获取昨天水
          this.axios.get("/api/energysteam",{params: params}),//获取今天汽
          this.axios.get("/api/energysteam",{params: yesterdayParams}),//获取昨天汽
        ]).then(this.axios.spread(function(todayElectricity,yesterdayElectricity,todayWater,yesterdayWater,todaySteam,yesterdaySteam){
          var todayElectricityData = JSON.parse(todayElectricity.data)
          var todayWaterData = JSON.parse(todayWater.data)
          var todaySteamData = JSON.parse(todaySteam.data)
          var yesterdayElectricityValue = JSON.parse(yesterdayElectricity.data).value
          var yesterdayWaterValue = JSON.parse(yesterdayWater.data).value
          var yesterdaySteamValue = JSON.parse(yesterdaySteam.data).value
          that.yesterdayElectricityValue = yesterdayElectricityValue
          that.yesterdayWaterValue = yesterdayWaterValue
          that.yesterdaySteamValue = yesterdaySteamValue
          if(todayElectricityData.value != undefined){
            that.todayElectricity = todayElectricityData.value
            that.ElectricityUnit = todayElectricityData.unit
          }else{
            that.todayElectricity = "无数据"
          }
          if(todayWaterData.value != undefined){
            that.todayWater = todayWaterData.value
            that.WaterUnit = todayWaterData.unit
          }else{
            that.todayWater = "无数据"
          }
          if(todaySteamData.value != undefined){
            that.todaySteam = todaySteamData.value
            that.SteamUnit = todaySteamData.unit
          }else{
            that.todaySteam = "无数据"
          }
        }))
      },
      getOnLineEq(){
        this.axios.get("/api/energyall",{params:{ModelFlag:"在线检测情况"}}).then(res => {
          this.onlineEquipmentOption = JSON.parse(res.data)
        })
      },
      initWebSocket(){ //初始化weosocket
        const wsuri = "ws://127.0.0.1:5002";
        this.websock = new WebSocket(wsuri);
        this.websock.onmessage = this.websocketonmessage;
        this.websock.onopen = this.websocketonopen;
        this.websock.onerror = this.websocketonerror;
        this.websock.onclose = this.websocketclose;
      },
      websocketonopen(){ //连接建立之后执行send方法发送数据
        this.websocketsend();
      },
      websocketonerror(){//连接建立失败重连
        //this.initWebSocket();
        console.log("连接失败")
      },
      websocketonmessage(e){ //数据接收
        const redata = JSON.parse(e.data);
        console.log(redata)
        //电
        this.electricChartData.rows.push({
          "时间": moment(new Date()).format("HH:mm:ss"),
          "功率": redata.E
        })
        this.electricChartData.rows.shift()
        this.electricChartValue = redata.E
        //水
        this.waterChartData.rows.push({
          "时间": moment(new Date()).format("HH:mm:ss"),
          "功率": redata.W
        })
        this.waterChartData.rows.shift()
        this.waterChartValue = redata.W
        //汽
        this.steamChartData.rows.push({
          "时间": moment(new Date()).format("HH:mm:ss"),
          "功率": redata.S
        })
        this.steamChartData.rows.shift()
        this.steamChartValue = redata.S
      },
      websocketsend(Data){//数据发送
        this.websock.send(Data);
      },
      websocketclose(e){  //关闭
        console.log('断开连接');
      },
    }
  }
</script>

<style scoped>
  .iconBlock{
    width: 60px;
    height: 60px;
    line-height: 60px;
    background: #082F4C;
    text-align: center;
  }
  .iconBlock i{
    border-radius: 4px;
    vertical-align: middle;
  }
</style>
