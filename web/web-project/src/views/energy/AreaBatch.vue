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
          <span style="vertical-align: sub;" class="text-color-info-shallow text-size-mini">(选择需要查询的月份)</span>
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
          <li class="text-size-normol text-color-info">{{ formParameters.resource }}耗{{ formParameters.energy }}量</li>
          <li class="text-size-large text-color-warning">{{ contrastTotal }}{{ Unit }}</li>
        </ul>
        <ul class="energyDataItem">
          <li class="text-size-normol text-color-info">{{ formParameters.resource }}生产批次</li>
          <li class="text-size-large text-color-primary">{{ contrastCount }}批</li>
        </ul>
        <ul class="energyDataItem">
          <li class="text-size-normol text-color-info">{{ formParameters.resource }}单位批次能耗</li>
          <li class="text-size-large text-color-primary">{{ contrastEveryBatch }}{{ Unit }}/批</li>
        </ul>
        <ul class="energyDataItem">
          <li class="text-size-normol text-color-info">{{ formParameters.resource }}生产品名数</li>
          <li class="text-size-large text-color-primary">{{ contrastTypeNum }}种</li>
        </ul>
      </div>
    </el-col>
    <el-col :span="20">
      <div class="energyDataContainer" style="border-radius: 0 0 4px 0;">
        <ve-chart :data="chartData" :extend="ChartExtend" :settings="ChartExtendSettings" v-loading="ChartsLoading" :legend-visible="false"></ve-chart>
      </div>
    </el-col>
    <el-col :span="24" style="margin-top:10px;margin-bottom:2px;">
      <div class="chartHead">
        <div class="chartTile text-size-large text-color-info">选择{{ formParameters.resource }}数据表</div>
        <el-select class="collapse-head-select" v-model="commodityValue" placeholder="请选择" @change="getCommodityPreview" size="small">
          <el-option v-for="item in commodityOptions" :key="item.ID" :label="item.BrandName" :value="item.BrandName"></el-option>
        </el-select>
      </div>
    </el-col>
    <el-col :span="24" style="border-radius:4px;padding: 10px;background: #fff;">
      <el-table :data="tableData" border tooltip-effect="dark" highlight-current-row ref="multipleTable" @selection-change="handleSelectionChange" @row-click="handleRowClick">
        <el-table-column type="selection"></el-table-column>
        <el-table-column prop="AreaName" label="区域"></el-table-column>
        <el-table-column prop="PlanNum" label="计划单号"></el-table-column>
        <el-table-column prop="BatchID" label="批次号"></el-table-column>
        <el-table-column prop="BrandName" label="品名"></el-table-column>
        <el-table-column prop="PlanQuantity" label="计划重量"></el-table-column>
        <el-table-column prop="WaterConsumption" label="水用量"></el-table-column>
        <el-table-column prop="SteamConsumption" label="汽用量"></el-table-column>
        <el-table-column prop="ProductionDate" label="生产日期" width="170"></el-table-column>
        <el-table-column prop="StartTime" label="开始时间" width="170"></el-table-column>
        <el-table-column prop="EndTime" label="结束时间" width="170"></el-table-column>
        <el-table-column prop="CreateDate" label="创建日期" width="170"></el-table-column>
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
        formParameters:{
          resource:"月",
          contrastingMonth:moment().month(moment().month()).startOf('month').format('YYYY-MM-DD HH:mm:ss'),
          energy:"水",
        },
        pickerOptions:{
          disabledDate(time) {
            return time.getTime() > moment();
          }
        },
        contrastTotal:"",
        contrastCount:"",
        contrastEveryBatch:"",
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
        ChartsLoading:false,
        chartData: {
          columns: [],
          rows: []
        },
        commodityValue:"",
        commodityOptions:[],
        tableData:[],
        total:0,
        pagesize:5,
        currentPage:1,
        multipleSelection:[],
      }
    },
    created(){
      this.getBrandName()
      this.getCommodityPreview()
    },
    methods: {
      getCommodityPreview() {
        this.ChartsLoading = true
        var that = this
        var contrastStartMonth = moment(this.formParameters.contrastingMonth).month(moment(this.formParameters.contrastingMonth).month()).startOf('month').format('YYYY-MM-DD HH:mm:ss')
        var contrastEndMonth = moment(this.formParameters.contrastingMonth).month(moment(this.formParameters.contrastingMonth).month()).endOf('month').format('YYYY-MM-DD HH:mm:ss')
        var contrastStartQuarter = moment(this.formParameters.contrastingMonth).quarter(moment(this.formParameters.contrastingMonth).quarter()).startOf('quarter').format('YYYY-MM-DD HH:mm')
        var contrastEndQuarter = moment(this.formParameters.contrastingMonth).quarter(moment(this.formParameters.contrastingMonth).quarter()).endOf('quarter').format('YYYY-MM-DD HH:mm')
        var contrastStartYear = moment(this.formParameters.contrastingMonth).year(moment(this.formParameters.contrastingMonth).year()).startOf('year').format('YYYY-MM-DD HH:mm:ss')
        var contrastEndYear = moment(this.formParameters.contrastingMonth).year(moment(this.formParameters.contrastingMonth).year()).endOf('year').format('YYYY-MM-DD HH:mm:ss')
        var contrastParams = {}
        var chartParams = {}
        var tableParams = {}
        var areaName = ""
        if(this.newAreaName.areaName === "整厂区"){
          areaName = ""
        }else{
          areaName = this.newAreaName.areaName
        }
        //获取选择时间能耗数据 参数
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
        chartParams.AreaName = areaName
        chartParams.EnergyClass = this.formParameters.energy
        chartParams.TimeClass = this.formParameters.resource
        if(this.formParameters.resource === "月"){
          chartParams.StartTime = contrastStartMonth
          chartParams.EndTime = contrastEndMonth
        }else if(this.formParameters.resource === "季"){
          chartParams.StartTime = contrastStartQuarter
          chartParams.EndTime = contrastEndQuarter
        }else if(this.formParameters.resource === "年"){
          chartParams.StartTime = contrastStartYear
          chartParams.EndTime = contrastEndYear
        }
        //获取表格数据 参数
        if(this.formParameters.resource === "月"){
          tableParams.AreaName = areaName
          tableParams.StartTime = contrastStartMonth
          tableParams.EndTime = contrastEndMonth
          tableParams.BrandName = this.commodityValue
          tableParams.tableName = "BatchMaintain"
          tableParams.limit = this.pagesize
          tableParams.offset = this.currentPage - 1
        }else if(this.formParameters.resource === "季"){
          tableParams.AreaName = areaName
          tableParams.StartTime = contrastStartQuarter
          tableParams.EndTime = contrastEndQuarter
          tableParams.BrandName = this.commodityValue
          tableParams.tableName = "BatchMaintain"
          tableParams.limit = this.pagesize
          tableParams.offset = this.currentPage - 1
        }else if(this.formParameters.resource === "年"){
          tableParams.AreaName = areaName
          tableParams.StartTime = contrastStartYear
          tableParams.EndTime = contrastEndYear
          tableParams.BrandName = this.commodityValue
          tableParams.tableName = "BatchMaintain"
          tableParams.limit = this.pagesize
          tableParams.offset = this.currentPage - 1
        }
        this.axios.all([
          this.axios.get("/api/batchMaintainEnergy",{params: contrastParams}),
          this.axios.get("/api/batchMaintainEnergyEcharts",{params: chartParams}),
          this.axios.get("/api/batchMaintainExcelSelect",{params: tableParams}),
        ]).then(this.axios.spread(function(contrastRes,chartRes,tableRes){
          that.ChartsLoading = false
          that.Unit = contrastRes.data.steamUnit
          that.contrastTotal = contrastRes.data.steamCon
          that.contrastCount = contrastRes.data.batchCount
          that.contrastEveryBatch = contrastRes.data.steamEveryBatch
          that.contrastTypeNum = contrastRes.data.typeNum
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
      },
      handleSelectionChange(val){
        this.multipleSelection = val;
      },
      handleRowClick(row){
        this.$refs.multipleTable.clearSelection();
        this.$refs.multipleTable.toggleRowSelection(row)
      },
    }
  }
</script>

<style>
  .energyDataItem{
    margin-bottom: 30px;
  }
  .energyDataItem li{
    margin-bottom: 5px;
  }
</style>
