<template>
  <el-row :gutter="20">
    <el-col :span="24">
      <el-form :inline="true" :model="formParameters">
        <el-form-item label="时间：">
          <el-radio-group v-model="formParameters.resourceTime" fill="#082F4C" size="mini" @change="getPipeData">
            <el-radio-button v-for="(item,index) in radioTimeList" border :key="index" :label="item.name"></el-radio-button>
          </el-radio-group>
          <el-date-picker type="datetime" v-model="formParameters.startDate" :picker-options="pickerOptions" size="mini" style="width: 180px;" :clearable="false" @change="getPipeData"></el-date-picker>
        </el-form-item>
      </el-form>
    </el-col>
    <el-col :span="24">
      <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
        <div class="chartTile">运行效率</div>
        <el-select v-model="areaValue" size="mini" @change="searchTime">
          <el-option v-for="(item,index) in areaOptions" :key="index" :label="item.AreaName" :value="item.value"></el-option>
        </el-select>
      </div>
      <div class="platformContainer">
        <el-col :span="8">
          <div class="platformItem">
            <p style="margin-bottom: 10px;">负荷率<span class="float-right text-size-mini text-color-info-shallow"></span></p>
            <p><label class="text-size-big text-color-primary">{{ loadRate }}</label><span class="float-right"></span></p>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="platformItem">
            <p style="margin-bottom: 10px;">额定功率<span class="float-right text-size-mini text-color-info-shallow"></span></p>
            <p><label class="text-size-big text-color-primary">{{ ratedPower }}</label><span class="float-right"></span></p>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="platformItem">
            <p style="margin-bottom: 10px;">有功功率<span class="float-right text-size-mini text-color-info-shallow"></span></p>
            <p><label class="text-size-big text-color-primary">{{ activePower }}</label><span class="float-right"></span></p>
          </div>
        </el-col>
      </div>
      <div class="energyDataContainer">
        <ve-histogram :data="runEfficiencyChartData" :extend="ChartExtend" v-loading="chartsLoading"></ve-histogram>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  var moment = require('moment');
  export default {
    name: "EfficiencyAnalysisRun",
    data(){
      return {
        formParameters:{
          resourceTime:"日",
          startDate:moment().format("YYYY-MM-DD HH:mm:ss")
        },
        radioTimeList:[
          {name:"日"},
          {name:"月"},
          {name:"年"},
        ],
        pickerOptions:{
          disabledDate(time) {
            return time.getTime() > Date.now();
          }
        },
        loadRate:"",
        ratedPower:"",
        activePower:"",
        areaValue:"",
        areaOptions:[],
        ChartExtend: {
          grid:{
            left:'0',
            right:'0',
            bottom:'0',
            top:'40px'
          },
          series:{
            barMaxWidth : 30,
            smooth: false
          }
        },
        runEfficiencyChartData:{
          columns: ['时间', '负荷率'],
          rows: []
        },
        chartsLoading:false
      }
    },
    created(){
      this.getPipeData()
    },
    methods:{
      getPipeData(){
        this.chartsLoading = true
        var that = this
        var dayStartTime = moment(this.formParameters.startDate).format('YYYY-MM-DD') + " 00:00:00"
        var dayEndTime = moment(this.formParameters.startDate).format('YYYY-MM-DD HH:mm:ss')
        var monthStartTime = moment(this.formParameters.startDate).month(moment(this.formParameters.startDate).month()).startOf('month').format('YYYY-MM-DD HH:mm:ss')
        var monthEndTime = moment(this.formParameters.startDate).month(moment(this.formParameters.startDate).month()).endOf('month').format('YYYY-MM-DD HH:mm:ss')
        var yearStartTime = moment(this.formParameters.startDate).year(moment(this.formParameters.startDate).year()).startOf('year').format('YYYY-MM-DD HH:mm:ss')
        var yearEndTime = moment(this.formParameters.startDate).year(moment(this.formParameters.startDate).year()).endOf('year').format('YYYY-MM-DD HH:mm:ss')
        var params = {}
        if(this.formParameters.resourceTime === "日"){
          params.StartTime = dayStartTime
          params.EndTime = dayEndTime
          params.TimeClass = this.formParameters.resourceTime
          params.CurrentTime = moment(this.formParameters.startDate).format('YYYY-MM-DD HH:mm:ss')
          params.AreaName = this.areaValue
        }else if(this.formParameters.resourceTime === "月"){
          params.StartTime = monthStartTime
          params.EndTime = monthEndTime
          params.TimeClass = this.formParameters.resourceTime
          params.CurrentTime = moment(this.formParameters.startDate).format('YYYY-MM-DD HH:mm:ss')
          params.AreaName = this.areaValue
        }else if(this.formParameters.resourceTime === "年"){
          params.StartTime = yearStartTime
          params.EndTime = yearEndTime
          params.TimeClass = this.formParameters.resourceTime
          params.CurrentTime = moment(this.formParameters.startDate).format('YYYY-MM-DD HH:mm:ss')
          params.AreaName = this.areaValue
        }
        this.axios.get("/api/runefficiency",{params:params}).then(res => {
          that.chartsLoading = false
          that.loadRate = res.data.loadRate + "%"
          that.ratedPower = res.data.ratedPower + res.data.unit
          that.activePower = res.data.activePower + res.data.unit
          that.runEfficiencyChartData.rows = res.data.row
        })
      },
      getArea(){
        var params = {
          tableName: "AreaTable",
          limit:1000,
          offset:0
        }
        var that = this
        this.axios.get("/api/CUID",{params:params}).then(res =>{
          var resData = JSON.parse(res.data).rows
          that.areaOptions.push({
            AreaName:"整厂区",value:""
          })
          resData.forEach(item =>{
            that.areaOptions.push({
              AreaName:item.AreaName,
              value:item.AreaName
            })
          })
        })
      },
    }
  }
</script>

<style scoped>
 .platformItem{
    background: #EEEEEE;
    border-radius:4px;
    padding: 15px;
    overflow: hidden;
    clear: both;
  }
</style>
