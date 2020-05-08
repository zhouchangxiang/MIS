<template>
  <el-row :gutter="2">
    <el-col :span="24">
      <el-form :model="formParameters">
        <el-form-item label="能耗：" style="margin-bottom: 0;">
          <el-radio-group v-model="formParameters.energy" fill="#082F4C" size="mini" @change="getEnergyChartsData">
            <el-radio-button v-for="item in energyList" :key="item.name" :label="item.name"></el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="时间：" style="margin-bottom: 0;">
          <el-radio-group v-model="formParameters.resourceTime" fill="#082F4C" size="mini" @change="getEnergyChartsData">
            <el-radio-button v-for="item in radioTimeList" border :key="item.id" :label="item.name"></el-radio-button>
          </el-radio-group>
          <el-date-picker type="datetime" v-model="formParameters.startDate" :picker-options="pickerOptions" size="mini" format="yyyy-MM-dd" style="width: 130px;" :clearable="false" @change="getEnergyChartsData"></el-date-picker>
        </el-form-item>
        <el-form-item label="参数：" v-if="formParameters.energy === '电'" style="margin-bottom: 0;">
          <el-radio-group v-model="formParameters.resourceType" fill="#082F4C" size="mini" @change="getEnergyChartsData">
            <el-radio-button v-for="item in radioTypeList" border :key="item.name" :label="item.name" :disabled="item.disabled"></el-radio-button>
          </el-radio-group>
        </el-form-item>
      </el-form>
    </el-col>
    <el-col :span="24" v-if="formParameters.resourceType === '基本电费' && formParameters.energy === '电'" style="margin-top: 10px;">
      <!--<el-col :span="12" v-for="(item,index) in ElecCalculationTypeItem" :key="index">-->
        <!--<div class="ElecCalculationType">-->
          <!--<p>{{ item.title }}</p>-->
          <!--<el-col :span="12"><p class="text-color-caption">{{ item.typeTitle }}</p>{{ item.typeData }}</el-col>-->
          <!--<el-col :span="12"><p class="text-color-caption">{{ item.electricity }}</p>{{ item.electricityData }}</el-col>-->
        <!--</div>-->
      <!--</el-col>-->
      <el-col :span="24">
        <div class="energyDataContainer">
          <ve-histogram :data="basicElectricityChartData" :settings="basicElectricityChartSettings" :extend="ChartExtend" v-loading="chartsLoading"></ve-histogram>
        </div>
      </el-col>
    </el-col>
    <el-col :span="24" v-if="formParameters.resourceType == '电度电费' && formParameters.energy === '电'" style="margin-top: 10px;">
      <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
        <div class="chartTile">趋势图</div>
        <div class="chartHeadRight">
          总电费：{{ totalPrice + '元' }}
        </div>
      </div>
      <el-col :span="6" v-for="(item,index) in periodTimeTypeItem" :key="index" style="margin-bottom:2px;">
        <div class="periodTimeTypeItem">
          <p>{{ item.title }} <span class="text-color-caption" style="float: right;">电价：{{ item.expendPrice }}元</span></p>
          <el-col :span="8"><p class="text-color-caption">电费/元</p>{{ item.unitPrice }}</el-col>
          <el-col :span="8"><p class="text-color-caption">电费占比</p>{{ item.Ratio + '%' }}</el-col>
          <el-col :span="8"><p class="text-color-caption">用电量/{{ item.unit }}</p>{{ item.expendEnergy }}</el-col>
        </div>
      </el-col>
      <div class="energyDataContainer" style="margin-bottom:2px;">
        <el-radio-group v-model="formParameters.dataType" fill="#082F4C" size="mini" @change="getEnergyChartsData">
          <el-radio-button v-for="item in dataTypeItem" :key="item.name" :label="item.name"></el-radio-button>
        </el-radio-group>
        <ve-histogram :data="electricityPileChartData" :settings="electricityPileChartSettings" :extend="ChartExtend" v-loading="chartsPileLoading" height="370px"></ve-histogram>
      </div>
      <el-col :span="6" v-for="item in periodTimeTypeItem" :key="item.title">
        <div class="periodTimeTypeItem">
          <p class="text-size-normol text-color-info">{{ item.title }}</p>
          <p><el-progress :text-inside="true" :stroke-width="16" :percentage="item.Ratio" :color="item.color"></el-progress></p>
        </div>
      </el-col>
    </el-col>
    <el-col :span="24" v-if="formParameters.resourceType == '力调电费' && formParameters.energy === '电'" style="margin-top: 10px;">
      <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
        <div class="chartTile">力调电费</div>
        <div class="chartHeadRight">
          总电费：163411元
        </div>
      </div>
      <el-col :span="12">
        <div class="ElecCalculationType">
          <p>无功罚款</p>
          <el-col :span="8"><p class="text-color-caption">年累计</p>{{ forceElectricityParameter.yearsTotal }}元</el-col>
          <el-col :span="8"><p class="text-color-caption">最大值 {{ forceElectricityParameter.largestMonth }}</p>{{ forceElectricityParameter.largestPrice }}元</el-col>
          <el-col :span="8"><p class="text-color-caption">每月平均</p>{{ forceElectricityParameter.averageMonthly }}元</el-col>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="ElecCalculationType">
          <p>功率因素</p>
          <el-col :span="8"><p class="text-color-caption">功率因素考核值</p>{{ forceElectricityParameter.powerFactorAssessmentValue }}</el-col>
          <el-col :span="8"><p class="text-color-caption">平均功率因素</p>{{ forceElectricityParameter.averagePowerFactor }}</el-col>
          <el-col :span="8"><p class="text-color-caption">低于考核值次数</p>{{ forceElectricityParameter.belowNumber }}次</el-col>
        </div>
      </el-col>
      <el-col :span="24">
        <div class="energyDataContainer">
          <ve-line :data="ElecCalculationChartData" :settings="ElecCalculationChartSettings" :extend="ChartExtend"></ve-line>
        </div>
      </el-col>
    </el-col>
    <el-col :span="24" v-if="formParameters.energy === '水' || formParameters.energy === '汽'" style="margin-top: 10px;">
      <div class="energyDataContainer">
        <ve-histogram :data="waterAndSteamCostChartData" :settings="waterAndSteamCostChartSettings" :extend="ChartExtend"></ve-histogram>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  var moment = require('moment');
  export default {
    name: "CostCenter",
    inject:['newAreaName'],
    data(){
      return {
        formParameters:{
          resourceTime:"日",
          resourceType:"基本电费",
          startDate:moment().format('YYYY-MM-DD HH:mm:ss'),
          energy:"电",
          dataType:"电费"
        },
        radioTimeList:[
          {name:"日"},
          {name:"月"},
          {name:"年"}
        ],
        radioTypeList:[
          {name:"基本电费"},
          {name:"电度电费"},
          // {name:"力调电费"}
        ],
        dataTypeItem:[
          {name:"电费"},
          {name:"电量"}
        ],
        pickerOptions:{
          disabledDate(time) {
            return time.getTime() > moment();
          }
        },
        energyList:[
          {name:"电"},
          {name:"水"},
          {name:"汽"},
        ],
        // ElecCalculationTypeIndex:0,
        // ElecCalculationTypeItem:[
        //   {title:"按容量计算",typeTitle:"变压器容量",typeData:"",electricity:"成本",electricityData:""},
        //   {title:"按耗量计算",typeTitle:"实际耗量",typeData:"",electricity:"成本",electricityData:""}
        // ],
        chartsLoading:false,
        chartsPileLoading:false,
        ChartExtend: {
          grid:{
            left:'0',
            right:'20px',
            bottom:'0',
            top:'40px'
          },
          series:{
            barMaxWidth : 30,
            smooth: false
          }
        },
        basicElectricityChartSettings: {
          axisSite: { right: ['元'] },
          yAxisName: []
        },
        basicElectricityChartData: {
          columns: ['时间', '耗量','成本'],
          rows: []
        },
        totalPrice:"",
        periodTimeTypeItem:[],
        electricityPileChartSettings: {
          stack: { '时段': ['谷时段','平时段','峰时段','尖时段'] }
        },
        electricityPileChartData:{
          columns: ['时间', '谷时段','平时段','峰时段','尖时段'],
          rows: []
        },
        forceElectricityParameter:{
          yearsTotal:263241.12,
          largestMonth:"12月",
          largestPrice:15451.65,
          averageMonthly:3541.5,
          powerFactorAssessmentValue:0.5,
          averagePowerFactor:0.66,
          belowNumber:30
        },
        ElecCalculationChartSettings: {
          axisSite: { right: ['功率因素'] },
          yAxisName: ['无功罚款', '功率因素']
        },
        ElecCalculationChartData:{
          columns: ['日期', '无功罚款','功率因素'],
          rows: [
            { '日期': '01', '无功罚款': 4393, '功率因素': 43},
            { '日期': '02', '无功罚款': 2393, '功率因素': 93},
            { '日期': '03', '无功罚款': 1593, '功率因素': 87},
            { '日期': '04', '无功罚款': 1693, '功率因素': 21}
          ]
        },
        waterAndSteamCostChartSettings:{
          axisSite: { right: ['元'] },
          yAxisName: []
        },
        waterAndSteamCostChartData:{
          columns: ['时间', '耗量', '成本'],
          rows: [
            { '时间': '01', '耗量': 4393, '成本': 43},
            { '时间': '02', '耗量': 2393, '成本': 93},
            { '时间': '03', '耗量': 1593, '成本': 87},
            { '时间': '04', '耗量': 1693, '成本': 21}
          ]
        }
      }
    },
    mounted(){
      this.getEnergyChartsData()
    },
    methods:{
      getEnergyChartsData(){
        this.chartsLoading = true
        this.chartsPileLoading = true
        var that = this
        var dayStartTime = moment(this.formParameters.startDate).day(moment(this.formParameters.startDate).day()).startOf('day').format('YYYY-MM-DD HH:mm:ss'),
          dayEndTime = moment(this.formParameters.startDate).day(moment(this.formParameters.startDate).day()).endOf('day').format('YYYY-MM-DD HH:mm:ss'),
          monthStartTime = moment(this.formParameters.startDate).month(moment(this.formParameters.startDate).month()).startOf('month').format('YYYY-MM-DD HH:mm:ss'),
          monthEndTime = moment(this.formParameters.startDate).month(moment(this.formParameters.startDate).month()).endOf('month').format('YYYY-MM-DD HH:mm:ss'),
          yearStartTime = moment(this.formParameters.startDate).year(moment(this.formParameters.startDate).year()).startOf('year').format('YYYY-MM-DD HH:mm:ss'),
          yearEndTime = moment(this.formParameters.startDate).year(moment(this.formParameters.startDate).year()).endOf('year').format('YYYY-MM-DD HH:mm:ss')
        var areaName = ""
        if(this.newAreaName.areaName === "整厂区"){
          areaName = ""
        }else{
          areaName = this.newAreaName.areaName
        }
        var params = {}
        params.EnergyClass = this.formParameters.energy
        params.TimeClass = this.formParameters.resourceTime
        params.AreaName = areaName
        if(this.formParameters.resourceTime === "日"){
          params.StartTime = dayStartTime
          params.EndTime = dayEndTime
        }else if(this.formParameters.resourceTime === "月"){
          params.StartTime = monthStartTime
          params.EndTime = monthEndTime
        }else if(this.formParameters.resourceTime === "年"){
          params.StartTime = yearStartTime
          params.EndTime = yearEndTime
        }
        this.axios.get("/api/energycost",{params:params}).then(res => {
          this.chartsLoading = false
          that.basicElectricityChartSettings.yAxisName = [res.data.expendUnit,'成本']
          that.basicElectricityChartData.rows = res.data.rows
          that.waterAndSteamCostChartSettings.yAxisName = [res.data.unit,'成本']
          that.waterAndSteamCostChartData.rows = res.data.rows
        })
        if(this.formParameters.resourceType === "电度电费" && this.formParameters.energy === "电"){
          this.axios.get("/api/electricnergycost",{params:params}).then(res => {
            this.chartsPileLoading = false
            that.periodTimeTypeItem = res.data.periodTimeTypeItem
            that.totalPrice = res.data.totalPrice
            if(that.formParameters.dataType === "电费"){
              that.electricityPileChartData.rows = res.data.rows2
            }else if(that.formParameters.dataType === "电量"){
              that.electricityPileChartData.rows = res.data.rows1
            }
          })
        }
      }
    }
  }
</script>

<style scoped>
  .ElecCalculationType{
    background: #fff;
    border-radius:4px;
    color: #000;
    font-size: 14px;
    padding: 15px;
    text-align: center;
    margin-bottom: 10px;
    clear: both;
    overflow: hidden;
  }
  .ElecCalculationType p{
    margin-bottom: 10px;
  }
  .periodTimeTypeItem{
    background: #fff;
    color: #000;
    font-size: 14px;
    padding: 15px;
    clear: both;
    overflow: hidden;
  }
  .periodTimeTypeItem p{
    margin-bottom: 10px;
    white-space: nowrap;
  }
  .el-progress-bar .el-progress-bar__outer{
    border-radius: 4px;
  }
  .el-progress-bar .el-progress-bar__inner{
    border-radius: 4px;
  }
</style>
