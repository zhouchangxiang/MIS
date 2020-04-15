<template>
  <el-row>
    <el-col :span="24" v-if="newAreaName.areaName === '整厂区' || newAreaName.areaName === ''">
      <el-row :gutter="30">
        <el-col :span="8">
          <div class="platformContainer" style="clear: none;overflow: initial;display: inline-block">
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
                  <span class="text-size-normol text-color-info">{{ electricityCost }}</span>
                  <span class="text-size-normol float-right" :class="todayElectricity-yesterdayElectricityValue>0?'text-color-danger':'text-color-success'">{{ ElectricityCompare }}</span>
                </div>
              </el-col>
            </el-col>
            <el-col :span="24" style="margin-top: 15px;">
              <p class="text-size-small">- 总功率：{{ electricChartValue }}</p>
              <ve-line :data="electricChartData" :extend="chartExtend" :legend-visible="false" height="300px" v-loading="socketLoading"></ve-line>
            </el-col>
            <el-col :span="24" style="margin-top: 15px;">
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
          <div class="platformContainer" style="clear: none;overflow: initial;display: inline-block">
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
                  <span class="text-size-normol text-color-info">{{ waterCost }}</span>
                  <span class="text-size-normol float-right" :class="todayWater-yesterdayWaterValue>0?'text-color-danger':'text-color-success'">{{ WaterCompare }}</span>
                </div>
              </el-col>
            </el-col>
            <el-col :span="24" style="margin-top: 15px;">
              <p class="text-size-small">- 累计流量：{{ waterChartValue }}</p>
              <ve-line :data="waterChartData" :extend="chartExtend" :legend-visible="false" height="300px" v-loading="socketLoading"></ve-line>
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
          <div class="platformContainer" style="clear: none;overflow: initial;display: inline-block">
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
                  <span class="text-size-normol text-color-info">{{ steamCost }}</span>
                  <span class="text-size-normol float-right" :class="todaySteam-yesterdaySteamValue>0?'text-color-danger':'text-color-success'">{{ SteamCompare }}</span>
                </div>
              </el-col>
            </el-col>
            <el-col :span="24" style="margin-top: 20px;">
              <p class="text-size-small">- 累计流量：{{ steamChartValue }}</p>
              <ve-line :data="steamChartData" :extend="chartExtend" :legend-visible="false" height="300px" v-loading="socketLoading"></ve-line>
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
    <el-col :span="24" v-else>
      <el-row :gutter="30" style="margin-bottom: 15px;">
        <el-col :span="8">
          <div class="platformContainer">
            <el-col :span="24" style="padding: 20px 0;">
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
                <span class="text-size-normol text-color-info">{{ electricityCost }}</span>
                <span class="text-size-normol float-right" :class="todayElectricity-yesterdayElectricityValue>0?'text-color-danger':'text-color-success'">{{ ElectricityCompare }}</span>
              </div>
            </el-col>
            </el-col>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="platformContainer">
            <el-col :span="24" style="padding: 20px 0;">
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
                <span class="text-size-normol text-color-info">{{ waterCost }}</span>
                <span class="text-size-normol float-right" :class="todayWater-yesterdayWaterValue>0?'text-color-danger':'text-color-success'">{{ WaterCompare }}</span>
              </div>
            </el-col>
            </el-col>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="platformContainer">
            <el-col :span="24" style="padding: 20px 0;">
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
                <span class="text-size-normol text-color-info">{{ steamCost }}</span>
                <span class="text-size-normol float-right" :class="todaySteam-yesterdaySteamValue>0?'text-color-danger':'text-color-success'">{{ SteamCompare }}</span>
              </div>
            </el-col>
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
            <div class="chartTile">本日批次能耗</div>
          </div>
          <div class="platformContainer">
            <el-table :data="tableData" border tooltip-effect="dark" height="400px">
              <el-table-column prop="AreaName" label="区域"></el-table-column>
              <el-table-column prop="PlanNum" label="计划单号"></el-table-column>
              <el-table-column prop="BatchID" label="批次号"></el-table-column>
              <el-table-column prop="BrandName" label="品名"></el-table-column>
              <el-table-column prop="PlanQuantity" label="计划重量"></el-table-column>
              <el-table-column prop="WaterConsumption" label="水用量"></el-table-column>
              <el-table-column prop="SteamConsumption" label="汽用量"></el-table-column>
              <el-table-column prop="ProductionDate" label="生产日期"></el-table-column>
            </el-table>
            <div class="paginationClass">
              <el-pagination background  layout="total, sizes, prev, pager, next, jumper"
                             :total="total"
                             :current-page="currentPage"
                             :page-sizes="[5,10,20]"
                             :page-size="pagesize"
                             @size-change="handleSizeChange"
                             @current-change="handleCurrentChange">
              </el-pagination>
            </div>
          </div>
        </el-col>
        <el-col :span="5">
          <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
            <div class="chartTile">设备情况</div>
          </div>
          <div class="platformContainer" style="height: 490px;">
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
        electricityCost:"",
        waterCost:"",
        steamCost:"",
        websock:null,
        socketLoading:false,
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
          columns: ['时间', '总功率'],
          rows: [
            { '时间': "", '总功率': ""},
            { '时间': "", '总功率': ""},
            { '时间': "", '总功率': ""},
            { '时间': "", '总功率': ""},
            { '时间': "", '总功率': ""},
            { '时间': "", '总功率': ""},
            { '时间': "", '总功率': ""},
            { '时间': "", '总功率': ""},
            { '时间': "", '总功率': ""},
            { '时间': "", '总功率': ""},
            { '时间': "", '总功率': ""},
            { '时间': "", '总功率': ""},
            { '时间': "", '总功率': ""},
            { '时间': "", '总功率': ""},
            { '时间': "", '总功率': ""},
            { '时间': "", '总功率': ""},
            { '时间': "", '总功率': ""},
            { '时间': "", '总功率': ""},
            { '时间': "", '总功率': ""},
            { '时间': "", '总功率': ""},
          ]
        },
        electricHistogram:{
          columns: ['时间', '总功率'],
          rows: []
        },
        electricRing:{
          columns: ['区域', '能耗量'],
          rows: []
        },
        waterChartValue:"",
        waterChartData:{
          columns: ['时间', '累计流量'],
          rows: [
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
          ]
        },
        waterHistogram:{
          columns: ['时间', '累计流量'],
          rows: []
        },
        waterRing:{
          columns: ['区域', '能耗量'],
          rows: []
        },
        steamChartValue:"",
        steamChartData:{
          columns: ['时间', '累计流量'],
          rows: [
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
            { '时间': "", '累计流量': ""},
          ]
        },
        steamHistogram:{
          columns: ['时间', '累计流量'],
          rows: []
        },
        steamRing:{
          columns: ['区域', '能耗量'],
          rows: []
        },
        batchTableData:[
          {Name:"药品A",Batch:"JUSA2374627"},
          {Name:"药品B",Batch:"JUSA2374627"},
          {Name:"药品C",Batch:"JUSA2374627"},
          {Name:"药品D",Batch:"JUSA2374627"},
        ],
        ChartSettings: {
          radius: [30,60],
          offsetY:"100px",
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
            show:false
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
        tableData:[],
        total:0,
        pagesize:5,
        currentPage:1,
        onlineEquipmentOption:[], //在线情况采集
      }
    },
    created(){
      this.getEnergyPreview()
      this.initWebSocket()
      this.getBatchTable()
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
        var thisStartMonth = moment().month(moment().month()).startOf('month').format('YYYY-MM-DD HH:mm')
        var thisMonthDay = moment().format('DD')
        var params = {}
        var yesterdayParams ={}
        var thisMonthParams ={}
        if(this.newAreaName.areaName === "整厂区"){
          params.StartTime = todayStartTime
          params.EndTime = todayEndTime
          yesterdayParams.StartTime = yesterdayStartTime
          yesterdayParams.EndTime = yesterdayEndTime
          thisMonthParams.StartTime = thisStartMonth
          thisMonthParams.EndTime = todayEndTime
        }else{
          params.StartTime = todayStartTime
          params.EndTime = todayEndTime
          params.Area = this.newAreaName.areaName
          yesterdayParams.StartTime = yesterdayStartTime
          yesterdayParams.EndTime = yesterdayEndTime
          yesterdayParams.Area = this.newAreaName.areaName
          thisMonthParams.StartTime = thisStartMonth
          thisMonthParams.EndTime = todayEndTime
          thisMonthParams.Area = this.newAreaName.areaName
        }
        this.axios.all([
          this.axios.get("/api/energyelectric",{params: params}),//获取今天电
          this.axios.get("/api/energyelectric",{params: yesterdayParams}),//获取昨天电
          this.axios.get("/api/energywater",{params: params}),//获取今天水
          this.axios.get("/api/energywater",{params: yesterdayParams}),//获取昨天水
          this.axios.get("/api/energysteam",{params: params}),//获取今天汽
          this.axios.get("/api/energysteam",{params: yesterdayParams}),//获取昨天汽
          this.axios.get("/api/energyelectric",{params: thisMonthParams}),//获取本月电
          this.axios.get("/api/energywater",{params: thisMonthParams}),//获取本月水
          this.axios.get("/api/energysteam",{params: thisMonthParams}),//获取本月汽
          this.axios.get("/api/todayAreaRingCharts"),//获取环形图
        ]).then(this.axios.spread(function(todayElectricity,yesterdayElectricity,todayWater,yesterdayWater,todaySteam,yesterdaySteam,monthElectricity,monthWater,monthSteam,todayAreaData){
          var todayElectricityData = JSON.parse(todayElectricity.data)
          var todayWaterData = JSON.parse(todayWater.data)
          var todaySteamData = JSON.parse(todaySteam.data)
          var yesterdayElectricityValue = JSON.parse(yesterdayElectricity.data).value
          var yesterdayWaterValue = JSON.parse(yesterdayWater.data).value
          var yesterdaySteamValue = JSON.parse(yesterdaySteam.data).value
          var thisMonthElectricityValue = JSON.parse(monthElectricity.data).value
          var thisMonthWaterValue = JSON.parse(monthWater.data).value
          var thisMonthSteamValue = JSON.parse(monthSteam.data).value
          that.yesterdayElectricityValue = yesterdayElectricityValue
          that.yesterdayWaterValue = yesterdayWaterValue
          that.yesterdaySteamValue = yesterdaySteamValue
          //电
          that.todayElectricity = todayElectricityData.value
          that.ElectricityUnit = todayElectricityData.unit
          that.electricityCost = todayElectricityData.cost + "元"
          that.electricHistogram.rows = [
            { '时间': "昨日", '总功率': that.yesterdayElectricityValue},
            { '时间': "本日", '总功率': that.todayElectricity},
            { '时间': "月均", '总功率': (thisMonthElectricityValue / thisMonthDay).toFixed(2)}
          ]
          //水
          that.todayWater = todayWaterData.value
          that.WaterUnit = todayWaterData.unit
          that.waterCost = todayWaterData.cost + "元"
          that.waterHistogram.rows = [
            { '时间': "昨日", '累计流量': that.yesterdayElectricityValue},
            { '时间': "本日", '累计流量': that.todayElectricity},
            { '时间': "月均", '累计流量': (thisMonthWaterValue / thisMonthDay).toFixed(2)}
          ]
          //汽
          that.todaySteam = todaySteamData.value
          that.SteamUnit = todaySteamData.unit
          that.steamCost = todaySteamData.cost + "元"
          that.steamHistogram.rows = [
            { '时间': "昨日", '累计流量': that.yesterdayElectricityValue},
            { '时间': "本日", '累计流量': that.todayElectricity},
            { '时间': "月均", '累计流量': (thisMonthSteamValue / thisMonthDay).toFixed(2)}
          ]
          that.electricRing.rows = todayAreaData.data.erow
          that.waterRing.rows = todayAreaData.data.wrow
          that.steamRing.rows = todayAreaData.data.srow
        }))
      },
      getBatchTable(){
        var that = this
        var nowTime = moment().format('HH:mm').substring(0,4) + "0"
        var todayStartTime = moment().format('YYYY-MM-DD') + " 00:00"
        var todayEndTime = moment().format('YYYY-MM-DD') + " " + nowTime
        var params = {
          AreaName:this.newAreaName.areaName,
          StartTime:todayStartTime,
          EndTime:todayEndTime,
          BrandName:"",
          tableName:"BatchMaintain",
          limit:this.pagesize,
          offset:this.currentPage - 1
        }
        this.axios.get("/api/batchMaintainExcelSelect",{params:params}).then(res => {
          var data = res.data
          that.tableData = data.rows
          that.total = data.total
        })
      },
      handleSizeChange(pagesize){ //每页条数切换
        this.pagesize = pagesize
        this.getBatchTable()
      },
      handleCurrentChange(currentPage) { // 页码切换
        this.currentPage = currentPage
        this.getBatchTable()
      },
      getOnLineEq(){
        this.axios.get("/api/energyall",{params:{ModelFlag:"在线检测情况"}}).then(res => {
          this.onlineEquipmentOption = JSON.parse(res.data)
        })
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
      websocketonerror(){//连接建立失败重连
        //this.initWebSocket();
        console.log("连接失败")
      },
      websocketonmessage(e){ //数据接收
        this.socketLoading = false
        const resdata = JSON.parse(e.data);
        console.log(resdata)
        console.log(this.newAreaName.areaName)
        for(var i=0;i<resdata.length;i++){
          if(resdata[i].AreaName === "" || resdata[i].AreaName === "整厂区"){
            this.electricChartValue = resdata[i].areaEZGL
            this.waterChartValue = resdata[i].areaWSum
            this.steamChartValue = resdata[i].areaSSum
            //电
            this.electricChartData.rows.push({
              "时间": moment(new Date()).format("HH:mm:ss"),
              "总功率": this.electricChartValue
            })
            this.electricChartData.rows.shift()
            //水
            this.waterChartData.rows.push({
              "时间": moment(new Date()).format("HH:mm:ss"),
              "累计流量": this.waterChartValue
            })
            this.waterChartData.rows.shift()
            //汽
            this.steamChartData.rows.push({
              '时间': moment(new Date()).format("HH:mm:ss"),
              '累计流量': this.steamChartValue
            })
            this.steamChartData.rows.shift()
          }
        }
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
