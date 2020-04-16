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
          <el-date-picker type="datetime" v-model="formParameters.startDate" :picker-options="pickerOptions" size="mini" format="yyyy-MM-dd HH:mm" style="width: 160px;" :clearable="false" @change="getEnergyChartsData"></el-date-picker> ~
          <el-date-picker type="datetime" v-model="formParameters.endDate" :picker-options="pickerOptions" size="mini" format="yyyy-MM-dd HH:mm" style="width: 160px;" :clearable="false" @change="getEnergyChartsData"></el-date-picker>
        </el-form-item>
        <el-form-item label="参数：" v-if="formParameters.energy === '电'" style="margin-bottom: 0;">
          <el-radio-group v-model="formParameters.resourceType" fill="#082F4C" size="mini" @change="getEnergyChartsData">
            <el-radio-button v-for="item in radioTypeList" border :key="item.name" :label="item.name" :disabled="item.disabled"></el-radio-button>
          </el-radio-group>
        </el-form-item>
      </el-form>
    </el-col>
    <el-col :span="24" v-if="formParameters.resourceType === '基本电费' && formParameters.energy === '电'" style="margin-top: 10px;">
      <el-col :span="12" v-for="(item,index) in ElecCalculationTypeItem" :key="index">
        <div class="ElecCalculationType">
          <p>{{ item.title }}</p>
          <el-col :span="12"><p class="text-color-caption">{{ item.typeTitle }}</p>{{ item.typeData }}</el-col>
          <el-col :span="12"><p class="text-color-caption">{{ item.electricity }}</p>{{ item.electricityData }}</el-col>
        </div>
      </el-col>
      <el-col :span="24">
        <div class="energyDataContainer">
          <ve-histogram :data="basicElectricityChartData" :settings="basicElectricityChartSettings" :extend="ChartExtend"></ve-histogram>
        </div>
      </el-col>
    </el-col>
    <el-col :span="24" v-if="formParameters.resourceType == '电度电费' && formParameters.energy === '电'" style="margin-top: 10px;">
      <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
        <div class="chartTile">趋势图</div>
        <div class="chartHeadRight">
          总电费：163411元
        </div>
      </div>
      <el-col :span="6" v-for="(item,index) in periodTimeTypeItem" :key="index" style="margin-bottom:2px;">
        <div class="periodTimeTypeItem">
          <p>{{ item.title }} <span class="text-color-caption" style="float: right;">电价：{{ item.expendPrice }}元</span></p>
          <el-col :span="8"><p class="text-color-caption">电费/元</p>{{ item.unitPrice }}</el-col>
          <el-col :span="8"><p class="text-color-caption">电费占比</p>{{ item.Ratio }}</el-col>
          <el-col :span="8"><p class="text-color-caption">用电量/{{ item.unit }}</p>{{ item.expendEnergy }}</el-col>
        </div>
      </el-col>
      <div class="energyDataContainer" style="margin-bottom:10px;">
        <ve-histogram :data="electricityPileChartData" :settings="electricityPileChartSettings" :extend="ChartExtend"></ve-histogram>
      </div>
      <el-col :span="12" v-for="item in electricAnalyzeItem" :key="item.title">
        <div class="electricAnalyze">
          <p style="text-align: center;margin-bottom: 10px;">{{ item.title }}</p>
          <el-row :gutter="20" style="margin-bottom: 10px;">
            <el-col :span="8">
              <p class="text-size-normol">尖时段</p>
              <span class="text-size-mini text-color-info-shallow">共{{ item.sharpTime }}小时</span>
              <p><el-progress :text-inside="true" :stroke-width="16" :percentage="item.sharp" color="#FB3A06"></el-progress></p>
            </el-col>
            <el-col :span="8">
              <p class="text-size-normol">峰时段</p>
              <span class="text-size-mini text-color-info-shallow">共{{ item.peakTime }}小时</span>
              <p><el-progress :text-inside="true" :stroke-width="16" :percentage="item.peak" color="#FB8A06"></el-progress></p>
            </el-col>
            <el-col :span="8">
              <p class="text-color-info-shallow" style="margin-bottom: 15px;">总电费：</p>
              <p>{{ item.total }}元</p>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="8">
              <p class="text-size-normol">平时段</p>
              <span class="text-size-mini text-color-info-shallow">共{{ item.poiseTime }}小时</span>
              <p><el-progress :text-inside="true" :stroke-width="16" :percentage="item.poise" color="#F8E71C"></el-progress></p>
            </el-col>
            <el-col :span="8">
              <p class="text-size-normol">谷时段</p>
              <span class="text-size-mini text-color-info-shallow">共{{ item.ebbTime }}小时</span>
              <p><el-progress :text-inside="true" :stroke-width="16" :percentage="item.ebb" color="#15CC48"></el-progress></p>
            </el-col>
            <el-col :span="8">
              <p class="text-color-info-shallow" style="margin-bottom: 15px;">平均电价：</p>
              <p>{{ item.average }}元</p>
            </el-col>
          </el-row>
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
      this.ChartExtend = {
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
      }
      this.electricityPileChartSettings = {
        stack: { '时段': ['谷时段','平时段','峰时段','尖时段'] }
      }
      return {
        formParameters:{
          resourceTime:"时",
          resourceType:"基本电费",
          startDate:moment().day(moment().day()).startOf('day').format('YYYY-MM-DD HH:mm'),
          endDate:moment().format('YYYY-MM-DD HH:mm'),
          energy:"电"
        },
        radioTimeList:[
          {name:"时"},
          {name:"日"},
          {name:"月"},
          {name:"年"}
        ],
        radioTypeList:[
          {name:"基本电费"},
          {name:"电度电费"},
          // {name:"力调电费"}
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
        ElecCalculationTypeIndex:0,
        ElecCalculationTypeItem:[
          {title:"按容量计算",typeTitle:"变压器容量",typeData:"",electricity:"成本",electricityData:""},
          {title:"按耗量计算",typeTitle:"实际耗量",typeData:"",electricity:"成本",electricityData:""}
        ],
        basicElectricityChartSettings: {
          axisSite: { right: ['元'] },
          yAxisName: []
        },
        basicElectricityChartData: {
          columns: ['时间', '容量', '耗量','成本'],
          rows: []
        },
        periodTimeTypeItem:[],
        electricityPileChartData:{
          columns: ['时间', '谷时段','平时段','峰时段','尖时段'],
          rows: []
        },
        electricAnalyzeItem:[
          {title:"尖峰平谷分析",sharp:100,sharpTime:3,peak:85.7,peakTime:7,poise:33.3,poiseTime:6,ebb:12.5,ebbTime:8,total:553524.5,average:0.54},
          {title:"避峰用谷分析（参考）",sharp:100,sharpTime:3,peak:85.7,peakTime:7,poise:33.3,poiseTime:6,ebb:12.5,ebbTime:8,total:553524.5,average:0.54}
        ],
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
          axisSite: { right: ['成本'] },
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
      selectElecCalculationType(index){
        this.ElecCalculationTypeIndex = index;
      },
      getEnergyChartsData(){
        var that = this
        var areaName = ""
        if(this.newAreaName.areaName === "整厂区"){
          areaName = ""
        }else{
          areaName = this.newAreaName.areaName
        }
        var params = {
          EnergyClass: this.formParameters.energy,
          StartTime:moment(this.formParameters.startDate).format("YYYY-MM-DD HH:mm"),
          EndTime:moment(this.formParameters.endDate).format("YYYY-MM-DD HH:mm"),
          TimeClass:this.formParameters.resourceTime,
          AreaName:areaName
        }
        this.axios.get("/api/energycost",{params:params}).then(res => {
          console.log(res.data)
          that.ElecCalculationTypeItem[0].typeData = res.data.transformerStorage + res.data.transformerUnit
          that.ElecCalculationTypeItem[0].electricityData = res.data.storageCost + "元"
          that.ElecCalculationTypeItem[1].typeData = res.data.expend + res.data.expendUnit
          that.ElecCalculationTypeItem[1].electricityData = res.data.expendCost + "元"
          that.basicElectricityChartSettings.yAxisName = [res.data.expendUnit,'成本']
          that.basicElectricityChartData.rows = res.data.rows
          that.waterAndSteamCostChartSettings.yAxisName = [res.data.unit,'成本']
          that.waterAndSteamCostChartData.rows = res.data.rows
        })
        if(this.formParameters.resourceType === "电度电费" && this.formParameters.energy === "电"){
          this.axios.get("/api/electricnergycost",{params:{
            StartTime:moment(this.formParameters.startDate).format("YYYY-MM-DD HH:mm"),
            EndTime:moment(this.formParameters.endDate).format("YYYY-MM-DD HH:mm"),
            TimeClass:this.formParameters.resourceTime,
            AreaName:areaName
          }}).then(res => {
            console.log(res.data)
            that.periodTimeTypeItem = res.data.periodTimeTypeItem
            that.electricityPileChartData.rows = res.data.rows
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
  .electricAnalyze{
    background: #fff;
    color: #082F4C;
    font-size: 18px;
    padding: 15px;
    clear: both;
    overflow: hidden;
  }
  .el-progress-bar .el-progress-bar__outer{
    border-radius: 4px;
  }
  .el-progress-bar .el-progress-bar__inner{
    border-radius: 4px;
  }
</style>
