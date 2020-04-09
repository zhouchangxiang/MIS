<template>
  <el-row :gutter="2">
    <el-col :span="24">
      <el-form :inline="true" :model="formParameters">
        <el-form-item label="时间：">
          <el-radio-group v-model="formParameters.resource" fill="#082F4C" size="mini" @change="getCommodityPreview">
            <el-radio-button v-for="(item,index) in radioList" border :key="index" :label="item.name" :value="item.value"></el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-date-picker type="month" placeholder="选择月份" v-model="formParameters.contrastingMonth" :picker-options="pickerOptions" size="mini" format="yyyy-MM" style="width: 130px;" :clearable="false" @change="getCommodityPreview"></el-date-picker>
          <span style="vertical-align: sub;" class="text-color-info-shallow text-size-mini">(对比时间)</span>
        </el-form-item>
        <el-form-item style="float: right;">
          <el-radio-group v-model="formParameters.energy" fill="#082F4C" size="small" @change="getCommodityPreview">
            <el-radio-button v-for="item in energyList" :key="item.id" :label="item.name"></el-radio-button>
          </el-radio-group>
        </el-form-item>
      </el-form>
    </el-col>
    <el-col :span="24" style="margin-bottom:2px;">
      <div class="chartHead text-size-large text-color-info"><div class="chartTile">趋势图</div></div>
    </el-col>
    <el-col :span="4">
      <div class="energyDataContainer" style="border-radius: 0 0 0 4px;">
        <ul class="energyDataItem">
          <li class="text-size-normol text-color-info">本{{ formParameters.resource }}耗{{ formParameters.energy }}量</li>
          <li class="text-size-large text-color-warning">{{ Total }}{{ Unit }}</li>
          <li class="text-size-mini">
            <span class="text-color-info-shallow" style="margin-right: 10px;">选择对比</span>
            <span class="text-size-mini" :class="Total-contrastTotal>0?'text-color-danger':'text-color-success'">{{ contrastRatioTotal }}</span>
          </li>
        </ul>
        <ul class="energyDataItem">
          <li class="text-size-normol text-color-info">本{{ formParameters.resource }}生产批次</li>
          <li class="text-size-large text-color-primary">{{ Count }}批</li>
          <li class="text-size-mini">
            <span class="text-color-info-shallow" style="margin-right: 10px;">选择对比</span>
            <span class="text-size-mini" :class="Count-contrastCount>0?'text-color-danger':'text-color-success'">{{ contrastRatioCount }}</span>
          </li>
        </ul>
        <ul class="energyDataItem">
          <li class="text-size-normol text-color-info">本{{ formParameters.resource }}单位批次能耗</li>
          <li class="text-size-large text-color-primary">{{ EveryBatch }}{{ Unit }}/批</li>
          <li class="text-size-mini">
            <span class="text-color-info-shallow" style="margin-right: 10px;">选择对比</span>
            <span class="text-size-mini" :class="EveryBatch-contrastEveryBatch>0?'text-color-danger':'text-color-success'">{{ contrastRatioEveryBatch }}</span>
          </li>
        </ul>
        <ul class="energyDataItem">
          <li class="text-size-normol text-color-info">本{{ formParameters.resource }}生产品名数</li>
          <li class="text-size-large text-color-primary">{{ TypeNum }}种</li>
          <li class="text-size-mini">
            <span class="text-color-info-shallow" style="margin-right: 10px;">选择对比</span>
            <span class="text-size-mini" :class="TypeNum-contrastTypeNum>0?'text-color-danger':'text-color-success'">{{ contrastRatioTypeNum }}</span>
          </li>
        </ul>
      </div>
    </el-col>
    <el-col :span="20">
      <div class="energyDataContainer" style="border-radius: 0 0 4px 0;">
        <ve-chart :data="chartData" :extend="ChartExtend" :settings="ChartExtendSettings" :legend-visible="false"></ve-chart>
      </div>
    </el-col>
    <el-col :span="24" style="margin-top:10px;margin-bottom:2px;">
      <div class="chartHead">
        <div class="chartTile text-size-large text-color-info">数据表<span class="text-size-mini text-color-danger">（倒序对比）</span></div>
        <el-select class="collapse-head-select" v-model="commodityValue" placeholder="请选择" @change="getCommodityPreview" size="small">
          <el-option v-for="item in commodityOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
        <el-button type="primary" style="background-color: #082F4C;border:none;" size="small">导出</el-button>
      </div>
    </el-col>
    <el-col :span="12" style="border-radius:0 0 4px 4px;padding: 10px;background: #fff;">
      <el-table :data="thisDateTableData" size="small" style="width: 100%">
        <el-table-column prop="date" label="时间"></el-table-column>
        <el-table-column prop="commodity" label="品名"></el-table-column>
        <el-table-column prop="batch" label="生产批次号"></el-table-column>
        <el-table-column prop="area" label="区域"></el-table-column>
        <el-table-column prop="energyVal" label="耗电量"></el-table-column>
        <el-table-column prop="totalEnergy" label="总耗电量"></el-table-column>
        <el-table-column prop="unitEnergy" label="单位耗电"></el-table-column>
      </el-table>
    </el-col>
    <el-col :span="12" style="border-radius:0 0 4px 4px;padding: 10px;background: #fff;">
      <el-table :data="thisDateTableData" size="small" style="width: 100%">
        <el-table-column prop="date" label="时间"></el-table-column>
        <el-table-column prop="commodity" label="品名"></el-table-column>
        <el-table-column prop="batch" label="生产批次号"></el-table-column>
        <el-table-column prop="area" label="区域"></el-table-column>
        <el-table-column prop="energyVal" label="耗电量"></el-table-column>
        <el-table-column prop="totalEnergy" label="总耗电量"></el-table-column>
        <el-table-column prop="unitEnergy" label="单位耗电"></el-table-column>
      </el-table>
    </el-col>
  </el-row>
</template>

<script>
  var moment = require('moment');
  export default {
    name: "AreaShows",
    inject:['newAreaName'],
    data(){
      return {
        radioList:[
          {name:"月"},
          {name:"季"},
          {name:"年"},
        ],
        energyList:[
          {name:"水",value:"水"},
          {name:"汽",value:"汽"},
        ],
        formParameters:{
          resource:"月",
          contrastingMonth:moment().month(moment().month() - 1).startOf('month').format('YYYY-MM-DD HH:mm'),
          energy:"水"
        },
        pickerOptions:{
          disabledDate(time) {
            return time.getTime() > Date.now();
          }
        },
        Total:"",
        contrastTotal:"",
        Count:"",
        contrastCount:"",
        EveryBatch:"",
        contrastEveryBatch:"",
        TypeNum:"",
        contrastTypeNum:"",
        Unit:"",
        ChartExtendSettings:{
          type:"",
        },
        ChartExtend: {
          grid:{
            left:'0',
            right:'0',
            bottom:'0',
            top:'40px'
          },
          series:{
            barMaxWidth : 50,
            smooth: false
          }
        },
        chartData: {
          columns: [],
          rows: []
        },
        commodityValue:"选项1",
        commodityOptions:[{
          value: '选项1',
          label: '药品1'
        }, {
          value: '选项2',
          label: '药品2'
        }, {
          value: '选项3',
          label: '药品3'
        }],
        thisDateTableData:[ //实时预警表格数据
          {date:"2020-01-02 12:05",commodity:"药品1",batch:"546465456",area:"新建综合制剂楼",energyVal:"4164",totalEnergy:"16424",unitEnergy:"1645"},
          {date:"2020-01-02 12:05",commodity:"药品1",batch:"546465456",area:"新建综合制剂楼",energyVal:"4164",totalEnergy:"16424",unitEnergy:"1645"},
          {date:"2020-01-02 12:05",commodity:"药品1",batch:"546465456",area:"新建综合制剂楼",energyVal:"4164",totalEnergy:"16424",unitEnergy:"1645"},
          {date:"2020-01-02 12:05",commodity:"药品1",batch:"546465456",area:"新建综合制剂楼",energyVal:"4164",totalEnergy:"16424",unitEnergy:"1645"},
          {date:"2020-01-02 12:05",commodity:"药品1",batch:"546465456",area:"新建综合制剂楼",energyVal:"4164",totalEnergy:"16424",unitEnergy:"1645"}
        ]
      }
    },
    created(){
      this.getCommodityPreview()
    },
    computed:{
      contrastRatioTotal(){
        if(this.Total > 0){
          var compare = (this.Total - this.contrastTotal) / this.Total * 100
          if(this.Total - this.contrastTotal > 0){
            return "+" + compare.toFixed(2) + "%"
          }else{
            return compare.toFixed(2) + "%"
          }
        }else{
          if(this.contrastTotal > 0){
            return "-" + 100 + "%"
          }else{
            return 0 + "%"
          }
        }
      },
      contrastRatioCount(){
        if(this.Count > 0){
          var compare = (this.Count - this.contrastCount) / this.Count * 100
          if(this.Count - this.contrastCount > 0){
            return "+" + compare.toFixed(2) + "%"
          }else{
            return compare.toFixed(2) + "%"
          }
        }else{
          if(this.contrastCount > 0){
            return "-" + 100 + "%"
          }else{
            return 0 + "%"
          }
        }
      },
      contrastRatioEveryBatch(){
        if(this.EveryBatch > 0){
          var compare = (this.EveryBatch - this.contrastEveryBatch) / this.EveryBatch * 100
          if(this.EveryBatch - this.contrastEveryBatch > 0){
            return "+" + compare.toFixed(2) + "%"
          }else{
            return compare.toFixed(2) + "%"
          }
        }else{
          if(this.contrastEveryBatch > 0){
            return "-" + 100 + "%"
          }else{
            return 0 + "%"
          }
        }
      },
      contrastRatioTypeNum(){
        if(this.TypeNum > 0){
          var compare = (this.TypeNum - this.contrastTypeNum) / this.TypeNum * 100
          if(this.TypeNum - this.contrastTypeNum > 0){
            return "+" + compare.toFixed(2) + "%"
          }else{
            return compare.toFixed(2) + "%"
          }
        }else{
          if(this.contrastTypeNum > 0){
            return "-" + 100 + "%"
          }else{
            return 0 + "%"
          }
        }
      }
    },
    methods: {
      getCommodityPreview() {
        var that = this
        var nowTime = moment().format('HH:mm').substring(0,4) + "0"
        var nowDate = moment().format('MM-DD') + " " + nowTime
        var todayEndTime = moment().format('YYYY-MM-DD') + " " + nowTime
        var thisStartMonth = moment().month(moment().month()).startOf('month').format('YYYY-MM-DD HH:mm')
        var contrastStartMonth = moment().month(moment(this.formParameters.contrastingMonth).month()).startOf('month').format('YYYY-MM-DD HH:mm')
        var contrastEndMonth = moment().month(moment(this.formParameters.contrastingMonth).month()).endOf('month').format('YYYY-MM-DD HH:mm')
        var thisStartQuarter = moment().quarter(moment().quarter()).startOf('quarter').format('YYYY-MM-DD HH:mm')
        var contrastStartQuarter = moment().quarter(moment(this.formParameters.contrastingMonth).quarter()).startOf('quarter').format('YYYY-MM-DD HH:mm')
        var contrastEndQuarter = moment().quarter(moment(this.formParameters.contrastingMonth).quarter()).endOf('quarter').format('YYYY-MM-DD HH:mm')
        var thisStartYear = moment().year(moment().year()).startOf('year').format('YYYY-MM-DD')
        var contrastStartYear = moment().year(moment(this.formParameters.contrastingMonth).year()).startOf('year').format('YYYY-MM-DD')
        var contrastEndYear = moment().year(moment(this.formParameters.contrastingMonth).year()).endOf('year').format('YYYY-MM-DD')
        var params = {}
        var contrastParams = {}
        var chartParams = {}
        var areaName = ""
        if(this.newAreaName.areaName === "整厂区"){
          areaName = ""
        }else{
          areaName = this.newAreaName.areaName
        }
        if(this.formParameters.resource === "月"){
          params.AreaName = areaName
          params.StartTime = thisStartMonth
          params.EndTime = todayEndTime
        }else if(this.formParameters.resource === "季"){
          params.AreaName = areaName
          params.StartTime = thisStartQuarter
          params.EndTime = todayEndTime
        }else if(this.formParameters.resource === "年"){
          params.AreaName = areaName
          params.StartTime = thisStartYear
          params.EndTime = todayEndTime
        }
        if(this.formParameters.resource === "月"){
          contrastParams.AreaName = areaName
          contrastParams.StartTime = contrastStartMonth
          contrastParams.EndTime = contrastEndMonth
        }else if(this.formParameters.resource === "季"){
          contrastParams.AreaName = areaName
          contrastParams.StartTime = contrastStartQuarter
          contrastParams.EndTime = contrastEndQuarter
        }else if(this.formParameters.resource === "年"){
          contrastParams.AreaName = areaName
          contrastParams.StartTime = contrastStartYear
          contrastParams.EndTime = contrastEndYear
        }
        if(this.formParameters.resource === "月"){
          chartParams.AreaName = areaName
          chartParams.StartTime = thisStartMonth
          chartParams.EndTime = todayEndTime
          chartParams.EnergyClass = this.formParameters.energy
          chartParams.TimeClass = this.formParameters.resource
        }else if(this.formParameters.resource === "季"){
          chartParams.AreaName = areaName
          chartParams.StartTime = thisStartQuarter
          chartParams.EndTime = todayEndTime
          chartParams.EnergyClass = this.formParameters.energy
          chartParams.TimeClass = this.formParameters.resource
        }else if(this.formParameters.resource === "年"){
          chartParams.AreaName = areaName
          chartParams.StartTime = thisStartYear
          chartParams.EndTime = todayEndTime
          chartParams.EnergyClass = this.formParameters.energy
          chartParams.TimeClass = this.formParameters.resource
        }
        this.axios.all([
          this.axios.get("/api/batchMaintainEnergy",{params: params}),
          this.axios.get("/api/batchMaintainEnergy",{params: contrastParams}),
          this.axios.get("/api/batchMaintainEnergyEcharts",{params: chartParams}),
        ]).then(this.axios.spread(function(res,contrastRes,chartRes){
          if(that.formParameters.energy === "水"){
            that.Unit = res.data.waterUnit
            that.Total = res.data.waterCon
            that.Count = res.data.batchCount
            that.EveryBatch = res.data.waterEveryBatch
            that.TypeNum = res.data.typeNum
          }else if(that.formParameters.energy === "汽"){
            that.Unit = res.data.steamUnit
            that.contrastTotal = res.data.steamCon
            that.contrastCount = res.data.batchCount
            that.contrastEveryBatch = res.data.steamEveryBatch
            that.contrastTypeNum = res.data.typeNum
          }
          if(that.formParameters.resource === "月") {
            that.chartData.rows = chartRes.data.row
            that.chartData.columns = ['批次', '批次能耗量']
            that.ChartExtendSettings.type = "line"
          }else if(that.formParameters.resource === "季"){
            that.chartData.rows = chartRes.data.row
            that.chartData.columns = ['批次', '批次能耗量']
            that.ChartExtendSettings.type = "line"
          }else if(that.formParameters.resource === "年"){
            that.chartData.rows = chartRes.data.row
            that.chartData.columns = ['日期', '批次能耗量']
            that.ChartExtendSettings.type = "histogram"
          }
        }))
      }
    }
  }
</script>

<style>
  .energyDataItem{
    margin-bottom: 30px;
  }
  .energyDataItem:last-child{
    margin-bottom:0;
  }
  .energyDataItem li{
    margin-bottom: 5px;
  }
</style>
