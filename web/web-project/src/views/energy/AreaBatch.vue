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
        <el-radio-group v-model="formParameters.chartTimeValue" fill="#082F4C" size="small" @change="getCommodityPreview">
          <el-radio-button v-for="(item,index) in chartTimeType" :key="index" :label="item.name"></el-radio-button>
        </el-radio-group>
        <ve-chart :data="chartData" :extend="ChartExtend" :settings="ChartExtendSettings" :legend-visible="false" height="360px"></ve-chart>
      </div>
    </el-col>
    <el-col :span="24" style="margin-top:10px;margin-bottom:2px;">
      <div class="chartHead">
        <div class="chartTile text-size-large text-color-info">本{{ formParameters.resource }}数据表</div>
        <el-select class="collapse-head-select" v-model="commodityValue" placeholder="请选择" @change="getCommodityPreview" size="small">
          <el-option v-for="item in commodityOptions" :key="item.ID" :label="item.BrandName" :value="item.BrandName"></el-option>
        </el-select>
      </div>
    </el-col>
    <el-col :span="24" style="border-radius:4px;padding: 10px;background: #fff;">
      <el-table :data="tableData" border tooltip-effect="dark">
        <el-table-column prop="ID" label="ID"></el-table-column>
        <el-table-column prop="PlanNum" label="计划单号"></el-table-column>
        <el-table-column prop="BatchID" label="批次号"></el-table-column>
        <el-table-column prop="BrandName" label="品名"></el-table-column>
        <el-table-column prop="PlanQuantity" label="计划重量"></el-table-column>
        <el-table-column prop="WaterConsumption" label="水用量"></el-table-column>
        <el-table-column prop="SteamConsumption" label="汽用量"></el-table-column>
        <el-table-column prop="ProductionDate" label="生产日期"></el-table-column>
        <el-table-column prop="StartTime" label="开始时间"></el-table-column>
        <el-table-column prop="EndTime" label="结束时间"></el-table-column>
        <el-table-column prop="CreateDate" label="创建日期"></el-table-column>
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
        chartTimeType:[
          {name:"当前时间"},
          {name:"对比时间"}
        ],
        formParameters:{
          resource:"月",
          contrastingMonth:moment().month(moment().month() - 1).startOf('month').format('YYYY-MM-DD HH:mm'),
          energy:"水",
          chartTimeValue:"当前时间"
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
        commodityValue:"",
        commodityOptions:[],
        tableData:[],
        total:0,
        pagesize:5,
        currentPage:1
      }
    },
    created(){
      this.getBrandName()
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
        var thisStartYear = moment().year(moment().year()).startOf('year').format('YYYY-MM-DD HH:mm')
        var contrastStartYear = moment().year(moment(this.formParameters.contrastingMonth).year()).startOf('year').format('YYYY-MM-DD HH:mm')
        var contrastEndYear = moment().year(moment(this.formParameters.contrastingMonth).year()).endOf('year').format('YYYY-MM-DD HH:mm')
        var params = {}
        var contrastParams = {}
        var chartParams = {}
        var tableParams = {}
        var areaName = ""
        if(this.newAreaName.areaName === "整厂区"){
          areaName = ""
        }else{
          areaName = this.newAreaName.areaName
        }
        //获取当前时间能耗数据 参数
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
        //获取对比时间能耗数据 参数
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
        //获取图表数据 参数
        if(this.formParameters.resource === "月"){
          chartParams.AreaName = areaName
          if(this.formParameters.chartTimeValue === "当前时间"){
            chartParams.StartTime = thisStartMonth
            chartParams.EndTime = todayEndTime
          }else if(this.formParameters.chartTimeValue === "对比时间"){
            chartParams.StartTime = contrastStartMonth
            chartParams.EndTime = contrastEndMonth
          }
          chartParams.EnergyClass = this.formParameters.energy
          chartParams.TimeClass = this.formParameters.resource
        }else if(this.formParameters.resource === "季"){
          chartParams.AreaName = areaName
          if(this.formParameters.chartTimeValue === "当前时间"){
            chartParams.StartTime = thisStartQuarter
            chartParams.EndTime = todayEndTime
          }else if(this.formParameters.chartTimeValue === "对比时间"){
            chartParams.StartTime = contrastStartQuarter
            chartParams.EndTime = contrastEndQuarter
          }
          chartParams.EnergyClass = this.formParameters.energy
          chartParams.TimeClass = this.formParameters.resource
        }else if(this.formParameters.resource === "年"){
          chartParams.AreaName = areaName
          if(this.formParameters.chartTimeValue === "当前时间"){
            chartParams.StartTime = thisStartYear
          chartParams.EndTime = todayEndTime
          }else if(this.formParameters.chartTimeValue === "对比时间"){
            chartParams.StartTime = contrastStartYear
            chartParams.EndTime = contrastEndYear
          }
          chartParams.EnergyClass = this.formParameters.energy
          chartParams.TimeClass = this.formParameters.resource
        }
        //获取表格数据 参数
        if(this.formParameters.resource === "月"){
          tableParams.AreaName = areaName
          tableParams.StartTime = thisStartMonth
          tableParams.EndTime = todayEndTime
          tableParams.BrandName = this.commodityValue
          tableParams.tableName = "BatchMaintain"
          tableParams.limit = this.pagesize
          tableParams.offset = this.currentPage - 1
        }else if(this.formParameters.resource === "季"){
          tableParams.AreaName = areaName
          tableParams.StartTime = thisStartQuarter
          tableParams.EndTime = todayEndTime
          tableParams.BrandName = this.commodityValue
          tableParams.tableName = "BatchMaintain"
          tableParams.limit = this.pagesize
          tableParams.offset = this.currentPage - 1
        }else if(this.formParameters.resource === "年"){
          tableParams.AreaName = areaName
          tableParams.StartTime = thisStartYear
          tableParams.EndTime = todayEndTime
          tableParams.BrandName = this.commodityValue
          tableParams.tableName = "BatchMaintain"
          tableParams.limit = this.pagesize
          tableParams.offset = this.currentPage - 1
        }
        this.axios.all([
          this.axios.get("/api/batchMaintainEnergy",{params: params}),
          this.axios.get("/api/batchMaintainEnergy",{params: contrastParams}),
          this.axios.get("/api/batchMaintainEnergyEcharts",{params: chartParams}),
          this.axios.get("/api/batchMaintainExcelSelect",{params: tableParams}),
        ]).then(this.axios.spread(function(res,contrastRes,chartRes,tableRes){
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
          var data = tableRes.data
          that.tableData = data.rows
          that.total = data.total
        }))
      },
      handleSizeChange(pagesize){ //每页条数切换
        this.pagesize = pagesize
        this.getCommodityPreview()
      },
      handleCurrentChange(currentPage) { // 页码切换
        this.currentPage = currentPage
        this.getCommodityPreview()
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
          that.commodityOptions = data.rows
        },res =>{
          console.log("获取品名时请求错误")
        })
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
