<template>
  <el-row>
    <el-col :span="24" v-if="newAreaName.areaName === '整厂区' || newAreaName.areaName === '' && $route.query.areaName === '整厂区'">
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
                  <span class="text-size-mini text-color-info-shallow float-right">对比昨日能耗</span>
                </div>
                <div class="itemMarginBottom">
                  <span class="text-size-normol text-color-info">{{ electricityCost }}</span>
                  <span class="text-size-normol float-right" :class="todayElectricity-yesterdayElectricityValue>0?'text-color-danger':'text-color-success'">{{ ElectricityCompare }}</span>
                </div>
              </el-col>
            </el-col>
            <el-col :span="24" style="margin-top: 15px;">
              <p class="text-color-info-shallow">日耗量</p>
              <ve-histogram :data="electricHistogram" height="200px" :extend="chartExtend" :legend-visible="false"></ve-histogram>
            </el-col>
            <el-col :span="24" style="margin-top: 15px;">
              <p class="text-color-info-shallow">车间耗量占比</p>
              <ve-ring :data="electricRing" :settings="ChartSettings" :extend="ChartExtend" width="100%" height="300px"></ve-ring>
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
                  <span class="text-size-mini text-color-info-shallow float-right">对比昨日能耗</span>
                </div>
                <div class="itemMarginBottom">
                  <span class="text-size-normol text-color-info">{{ waterCost }}</span>
                  <span class="text-size-normol float-right" :class="todayWater-yesterdayWaterValue>0?'text-color-danger':'text-color-success'">{{ WaterCompare }}</span>
                </div>
              </el-col>
            </el-col>
            <el-col :span="24" style="margin-top: 20px;">
              <p class="text-color-info-shallow">日耗量</p>
              <ve-histogram :data="waterHistogram" height="200px" :extend="chartExtend" :legend-visible="false"></ve-histogram>
            </el-col>
            <el-col :span="24" style="margin-top: 15px;">
              <p class="text-color-info-shallow">车间耗量占比</p>
              <ve-ring :data="waterRing" :settings="ChartSettings" :extend="ChartExtend" width="100%" height="300px"></ve-ring>
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
                  <span class="text-size-mini text-color-info-shallow float-right">对比昨日能耗</span>
                </div>
                <div class="itemMarginBottom">
                  <span class="text-size-normol text-color-info">{{ steamCost }}</span>
                  <span class="text-size-normol float-right" :class="todaySteam-yesterdaySteamValue>0?'text-color-danger':'text-color-success'">{{ SteamCompare }}</span>
                </div>
              </el-col>
            </el-col>
            <el-col :span="24" style="margin-top: 20px;">
              <p class="text-color-info-shallow">日耗量</p>
              <ve-histogram :data="steamHistogram" height="200px" :extend="chartExtend" :legend-visible="false"></ve-histogram>
            </el-col>
            <el-col :span="24" style="margin-top: 15px;">
              <p class="text-color-info-shallow">车间耗量占比</p>
              <ve-ring :data="steamRing" :settings="ChartSettings" :extend="ChartExtend" width="100%" height="300px"></ve-ring>
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
                <span class="text-size-mini text-color-info-shallow float-right">对比昨日能耗</span>
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
                <span class="text-size-mini text-color-info-shallow float-right">对比昨日能耗</span>
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
                  <span class="text-size-mini text-color-info-shallow float-right">对比昨日能耗</span>
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
          <div class="platformContainer" style="margin-bottom:3px;">
            <el-table :data="commodityTable" height="305px">
              <el-table-column prop="BrandName" label="品名"></el-table-column>
            </el-table>
          </div>
          <div class="platformContainer">
            <el-col :span="24">
              <div class="itemMarginBottom">
                <span class="text-size-normol text-color-info-shallow">今日品名数</span>
              </div>
              <div class="itemMarginBottom">
                <span class="text-size-normol text-color-info">{{ todayBrandTypeNum }}</span>
              </div>
            </el-col>
            <el-col :span="24">
              <div class="itemMarginBottom">
                <span class="text-size-normol text-color-info-shallow">今日批次数</span>
              </div>
              <div class="itemMarginBottom">
                <span class="text-size-normol text-color-info">{{ todayBatchCount }}</span>
              </div>
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
              <li v-for="item in onlineEquipmentOption" class="itemMarginBottom">
                <p class="text-size-normol text-color-info" style="margin-bottom: 5px;">{{ item.name }}</p>
                <p class="text-size-mini text-color-info-shallow" style="margin-bottom: 5px;"><span>上线数/总数</span><span style="float: right;">{{ item.online }}/{{ item.total }}</span></p>
                <el-progress :text-inside="true" :stroke-width="16" :color="item.rate == 100?'#15CC48':'#FB8A06'" :percentage="item.rate"></el-progress>
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
        electricHistogram:{
          columns: ['时间', '总功率'],
          rows: []
        },
        electricRing:{
          columns: ['区域', '能耗量'],
          rows: []
        },
        waterHistogram:{
          columns: ['时间', '累计流量'],
          rows: []
        },
        waterRing:{
          columns: ['区域', '能耗量'],
          rows: []
        },
        steamHistogram:{
          columns: ['时间', '累计流量'],
          rows: []
        },
        steamRing:{
          columns: ['区域', '能耗量'],
          rows: []
        },
        commodityTable:[],
        ChartSettings: {
          radius: [40,60],
          offsetY:"160px",
          label:{
            show:true,
            position:'outside'
          },
          labelLine:{
            show:true,
            length:16,
            length2:10,
          }
        },
        ChartExtend: {
          legend:{
            show:false
          },
        },
        tableData:[],
        total:0,
        pagesize:5,
        currentPage:1,
        todayBrandTypeNum:"",
        todayBatchCount:"",
        onlineEquipmentOption:[], //在线情况采集
      }
    },
    created(){
      this.getEnergyPreview()
      this.getBrandName()
      this.getBrandData()
      this.getBatchTable()
      this.getOnLineEq()
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
        let that = this,
          nowTime = moment().format('HH:mm').substring(0,4) + "0",
          todayStartTime = moment().format('YYYY-MM-DD') + " 00:00",
          todayEndTime = moment().format('YYYY-MM-DD') + " " + nowTime,
          yesterdayStartTime = moment().subtract(1,'day').format('YYYY-MM-DD') + " 00:00",
          yesterdayEndTime = moment().subtract(1,'day').format('YYYY-MM-DD') + " " + nowTime,
          thisStartMonth = moment().month(moment().month()).startOf('month').format('YYYY-MM-DD HH:mm'),
          thisMonthDay = moment().format('DD'),
          params = {},
          yesterdayParams ={},
          thisMonthParams ={}
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
        ]).then(this.axios.spread((todayElectricity,yesterdayElectricity,todayWater,yesterdayWater,todaySteam,yesterdaySteam,monthElectricity,monthWater,monthSteam,todayAreaData) =>{
          var todayElectricityData = JSON.parse(todayElectricity.data),
            todayWaterData = JSON.parse(todayWater.data),
            todaySteamData = JSON.parse(todaySteam.data),
            yesterdayElectricityValue = JSON.parse(yesterdayElectricity.data).value,
            yesterdayWaterValue = JSON.parse(yesterdayWater.data).value,
            yesterdaySteamValue = JSON.parse(yesterdaySteam.data).value,
            thisMonthElectricityValue = JSON.parse(monthElectricity.data).value,
            thisMonthWaterValue = JSON.parse(monthWater.data).value,
            thisMonthSteamValue = JSON.parse(monthSteam.data).value
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
            { '时间': "昨日", '累计流量': that.yesterdayWaterValue},
            { '时间': "本日", '累计流量': that.todayWater},
            { '时间': "月均", '累计流量': (thisMonthWaterValue / thisMonthDay).toFixed(2)}
          ]
          //汽
          that.todaySteam = todaySteamData.value
          that.SteamUnit = todaySteamData.unit
          that.steamCost = todaySteamData.cost + "元"
          that.steamHistogram.rows = [
            { '时间': "昨日", '累计流量': that.yesterdaySteamValue},
            { '时间': "本日", '累计流量': that.todaySteam},
            { '时间': "月均", '累计流量': (thisMonthSteamValue / thisMonthDay).toFixed(2)}
          ]
          that.electricRing.rows = todayAreaData.data.erow
          that.waterRing.rows = todayAreaData.data.wrow
          that.steamRing.rows = todayAreaData.data.srow
        }))
      },
      getBrandName(){
        var that = this
        this.axios.get("/api/CUID",{
          params: {
            tableName: "BrandMaintain",
            limit:100000000,
            offset:0
          }
        }).then(res =>{
          var data = JSON.parse(res.data)
          that.commodityTable = data.rows
        })
      },
      getBatchTable(){
        var that = this,
          nowTime = moment().format('HH:mm').substring(0,4) + "0",
          todayStartTime = moment().format('YYYY-MM-DD') + " 00:00",
          todayEndTime = moment().format('YYYY-MM-DD') + " " + nowTime,
          params = {
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
      getBrandData(){
        var that = this,
          nowTime = moment().format('HH:mm').substring(0,4) + "0",
          todayStartTime = moment().format('YYYY-MM-DD') + " 00:00",
          todayEndTime = moment().format('YYYY-MM-DD') + " " + nowTime,
          areaName = "",
          params = {
            AreaName:areaName,
            StartTime:todayStartTime,
            EndTime:todayEndTime
          }
        if(this.newAreaName.areaName === "整厂区"){
          areaName = ""
        }else{
          areaName = this.newAreaName.areaName
        }
        this.axios.get("/api/batchMaintainEnergy",{params:params}).then(res => {
          that.todayBrandTypeNum = res.data.typeNum
          that.todayBatchCount = res.data.batchCount
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
