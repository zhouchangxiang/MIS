<template>
    <el-row :gutter="10">
      <el-col :span="24">
        <el-form :inline="true" :model="formParameters">
          <el-form-item label="时间：">
            <el-date-picker type="date" v-model="formParameters.date" :picker-options="pickerOptions" size="mini" format="yyyy-MM-dd" style="width: 130px;" :clearable="false" @change="getChartData(),getAreaTimeEnergy(),getEnergycost()"></el-date-picker>
          </el-form-item>
          <el-form-item style="float: right;">
            <el-radio-group v-model="formParameters.energy" fill="#082F4C" size="small" @change="getDayEnergy(),getChartData(),getAreaTimeEnergy(),getEnergycost()">
              <el-radio-button v-for="(item,index) in energyList" :key="index" :label="item.label"></el-radio-button>
            </el-radio-group>
          </el-form-item>
        </el-form>
      </el-col>
      <el-col :span="24" v-if="$route.query.areaName != '整厂区'">
        <el-col :span="18">
          <div class="energyDataCard">
            <ve-line :data="chartData" :settings="chartSettings" :extend="ChartExtend" v-loading="ChartsLoading" height="300px"></ve-line>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="energyDataCard">
            <div class="realTimeCardTitle">今日能耗<span>{{ todayConUnit }}</span></div>
            <div class="realTimeData itemMarginBottom text-color-primary" v-html="todayHtml">{{ todayCon }}</div>
          </div>
          <div class="energyDataCard">
            <div class="energyDataItem">
              <div class="energyDataItemTitle">
                <el-date-picker type="date" v-model="CompareDate" :picker-options="pickerOptions" size="mini" style="width: 130px;" :clearable="false" @change="getDayEnergy"></el-date-picker>
              </div>
            </div>
            <div class="energyDataItem">
              <div class="energyDataItemTitle">对比日能耗</div>
              <div class="energyDataItemData">{{ CompareAllDateCon }} {{ todayConUnit }}</div>
            </div>
            <div class="energyDataItem">
              <div class="energyDataItemTitle">截止{{ nowTime }}能耗</div>
              <div class="energyDataItemData">{{ CompareDateCon }} {{ todayConUnit }}</div>
            </div>
            <div class="energyDataItem">
              <div class="energyDataItemTitle">对比</div>
              <div class="energyDataItemData">{{ compareRatio }}</div>
            </div>
          </div>
        </el-col>
        <el-col :span="24" v-if="formParameters.energy === '电'">
          <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
            <div class="chartTile">尖峰平谷分析</div>
          </div>
          <div class="platformContainer">
            <el-col :span="12" v-for="(item,index) in electricAnalyze" :key="index" class="itemMarginBottom">
              <p class="text-size-normol itemMarginBottom">{{ item.title }}</p>
              <el-col :span="10">
                <el-progress :text-inside="true" :stroke-width="16" :percentage="item.Ratio" :color="item.color"></el-progress>
              </el-col>
              <el-col :span="14">
                <span class="text-color-info" style="padding-left: 10px;">用量：{{ item.expendEnergy }}{{ item.unit }}</span>
                <span class="text-color-info" style="padding-left: 10px;">成本：{{ item.expendPrice }}元</span>
              </el-col>
            </el-col>
          </div>
        </el-col>
        <el-col :span="24" v-if="formParameters.energy === '水'">
          <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
            <div class="chartTile">水能详细数据</div>
          </div>
          <div class="platformContainer">
            <el-col :span="8">
              <div class="energyDataCard">
                <p class="text-size-normol text-color-info itemMarginBottom">灌溉水</p>
                <p class="text-size-small itemMarginBottom">用量：{{ waterGG }}</p>
                <p class="text-size-small">成本：{{ waterGGCost }}</p>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="energyDataCard">
                <p class="text-size-normol text-color-info itemMarginBottom">饮用水</p>
                <p class="text-size-small itemMarginBottom">用量：{{ waterYY }}</p>
                <p class="text-size-small">成本：{{ waterYYCost }}</p>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="energyDataCard">
                <p class="text-size-normol text-color-info itemMarginBottom">深井水</p>
                <p class="text-size-small itemMarginBottom">用量：{{ waterSJ }}</p>
                <p class="text-size-small">成本：{{ waterSJCost }}</p>
              </div>
            </el-col>
          </div>
        </el-col>
      </el-col>
      <el-col :span="24" v-if="$route.query.areaName === '整厂区'">
        <el-col :span="18">
          <div class="energyDataCard">
            <ve-line :data="chartData" :settings="chartSettings" :extend="ChartExtend" v-loading="ChartsLoading" height="300px"></ve-line>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="energyDataCard">
            <div class="realTimeCardTitle">今日能耗<span>{{ todayConUnit }}</span></div>
            <div class="realTimeData itemMarginBottom text-color-primary" v-html="todayHtml">{{ todayCon }}</div>
          </div>
          <div class="energyDataCard" style="margin-bottom: 0">
            <div class="energyDataItem">
              <div class="energyDataItemTitle">
                <el-date-picker type="date" v-model="CompareDate" :picker-options="pickerOptions" size="mini" style="width: 130px;" :clearable="false" @change="getDayEnergy"></el-date-picker>
              </div>
            </div>
            <div class="energyDataItem">
              <div class="energyDataItemTitle">对比日能耗</div>
              <div class="energyDataItemData">{{ CompareAllDateCon }} {{ todayConUnit }}</div>
            </div>
            <div class="energyDataItem">
              <div class="energyDataItemTitle">截止{{ nowTime }}能耗</div>
              <div class="energyDataItemData">{{ CompareDateCon }} {{ todayConUnit }}</div>
            </div>
            <div class="energyDataItem">
              <div class="energyDataItemTitle">对比</div>
              <div class="energyDataItemData">{{ compareRatio }}</div>
            </div>
          </div>
        </el-col>
        <el-col :span="24">
          <div class="energyDataCard">
            <ul class="colorBar">
              <li><i class="bg-dead"></i><span>停</span></li>
              <li><i class="bg-low"></i><span>低</span></li>
              <li><i class="bg-center"></i><span>中</span></li>
              <li><i class="bg-tall"></i><span>高</span></li>
            </ul>
            <ul class="gradientList itemMarginBottom">
              <li v-for="(item,index) in colorBarOption" :key="index">
                <p class="text-size-small text-color-info">{{ item.AreaName }}</p>
                <el-popover trigger="hover">
                  <div v-for="valueItem in item.valuelist">{{ valueItem.date }}点：{{ valueItem.value }}</div>
                  <div slot="reference" class="gradientColorItem" :style='{background:item.backgroundColor}'></div>
                </el-popover>
              </li>
            </ul>
            <el-row :gutter="1">
              <el-col :span="1"><div class="periodTimeItem">0</div></el-col>
              <el-col :span="1"><div class="periodTimeItem">1</div></el-col>
              <el-col :span="1"><div class="periodTimeItem">2</div></el-col>
              <el-col :span="1"><div class="periodTimeItem">3</div></el-col>
              <el-col :span="1"><div class="periodTimeItem">4</div></el-col>
              <el-col :span="1"><div class="periodTimeItem">5</div></el-col>
              <el-col :span="1"><div class="periodTimeItem">6</div></el-col>
              <el-col :span="1"><div class="periodTimeItem">7</div></el-col>
              <el-col :span="1"><div class="periodTimeItem">8</div></el-col>
              <el-col :span="1"><div class="periodTimeItem">9</div></el-col>
              <el-col :span="1"><div class="periodTimeItem">10</div></el-col>
              <el-col :span="1"><div class="periodTimeItem">11</div></el-col>
              <el-col :span="1"><div class="periodTimeItem">12</div></el-col>
              <el-col :span="1"><div class="periodTimeItem">13</div></el-col>
              <el-col :span="1"><div class="periodTimeItem">14</div></el-col>
              <el-col :span="1"><div class="periodTimeItem">15</div></el-col>
              <el-col :span="1"><div class="periodTimeItem">16</div></el-col>
              <el-col :span="1"><div class="periodTimeItem">17</div></el-col>
              <el-col :span="1"><div class="periodTimeItem">18</div></el-col>
              <el-col :span="1"><div class="periodTimeItem">19</div></el-col>
              <el-col :span="1"><div class="periodTimeItem">20</div></el-col>
              <el-col :span="1"><div class="periodTimeItem">21</div></el-col>
              <el-col :span="1"><div class="periodTimeItem">22</div></el-col>
              <el-col :span="1"><div class="periodTimeItem">23</div></el-col>
            </el-row>
          </div>
        </el-col>
      </el-col>
    </el-row>
</template>

<script>
  var moment = require('moment');
  export default {
    name: "AreaPeriodTime",
    inject:['newAreaName'],
    data(){
      return {
        formParameters:{
          date:moment().format('YYYY-MM-DD'),
          energy:"电"
        },
        energyList:[
          {label:"电"},
          {label:"水"},
          {label:"汽"},
        ],
        nowTime:"",
        todayCon:"",
        todayConUnit:"",
        CompareDate:moment().subtract(1,'day').format('YYYY-MM-DD'),
        CompareDateCon:"",
        CompareAllDateCon:"",
        todayHtml:"",
        pickerOptions:{
          disabledDate(time) {
            return time.getTime() > moment();
          }
        },
        AllArea:false,
        totalDayEnergy:"",
        chartSettings: {
          area:true,
          yAxisName:[]
        },
        ChartsLoading:false,
        ChartExtend: {
          title:{
            text:"能耗趋势"
          },
          grid:{
            left:'0px',
            right:'10px',
            bottom:'0',
            top:'60px'
          },
          series:{
            smooth: false
          }
        },
        chartData:{
          columns:["时间","能耗量"],
          rows:[]
        },
        waterGG:"",
        waterGGCost:"",
        waterYY:"",
        waterYYCost:"",
        waterSJ:"",
        waterSJCost:"",
        electricAnalyze:[],
        colorBarOption:[]
      }
    },
    created(){
      this.getDayEnergy()
      this.getAreaTimeEnergy()
      this.getChartData()
      this.getEnergycost()
    },
    watch:{
      todayCon(newValue){
        if(newValue > 0) {
          var thisYearConStr = newValue.toString().split("")
          var html = ""
          thisYearConStr.forEach(item => {
            if (item === ".") {
              html += `<span style="margin-right: 3px;">${item}</span>`
            } else {
              html += `<span class="numBlock">${item}</span>`
            }
          })
          this.todayHtml = html
        }else{
          this.todayHtml = `<span class="numBlock">0</span>`
        }
      }
    },
    computed:{
      compareRatio(){
        if(this.todayCon > 0){
          var compare = (this.todayCon - this.CompareDateCon) / this.todayCon * 100
          if(this.todayCon - this.CompareDateCon > 0){
            return "+" + compare.toFixed(2) + "%"
          }else{
            return compare.toFixed(2) + "%"
          }
        }else{
          if(this.CompareDateCon > 0){
            return "-" + 100 + "%"
          }else{
            return 0 + "%"
          }
        }
      }
    },
    methods:{
      getDayEnergy(){
        var api = ""
        var that = this
        var areaName = ''
        var nowTime = moment().format('HH:mm').substring(0,4) + "0"
        var todayStartTime = moment().day(moment().day()).startOf('day').format('YYYY-MM-DD HH:mm')
        var todayEndTime = moment().format('YYYY-MM-DD') + " " + nowTime
        var compareDateStartTime = moment(this.CompareDate).day(moment(this.CompareDate).day()).startOf('day').format('YYYY-MM-DD HH:mm')
        var compareDateEndTime = moment(this.CompareDate).format('YYYY-MM-DD') + " " + nowTime
        var compareDateAllEndTime = moment(this.CompareDate).day(moment(this.CompareDate).day()).endOf('day').format('YYYY-MM-DD HH:mm')
        this.nowTime = nowTime
        if(this.formParameters.energy === "电"){
          api = "/api/energyelectric"
        }else if(this.formParameters.energy === "水"){
          api = "/api/energywater"
        }else if(this.formParameters.energy === "汽"){
          api = "/api/energysteam"
        }
        if(this.newAreaName.areaName === "整厂区"){
          areaName = ""
        }else{
          areaName = this.newAreaName.areaName
        }
        this.axios.all([
          this.axios.get(api,{params: {StartTime: todayStartTime,EndTime:todayEndTime,Area:areaName}}),//获取今天能耗
          this.axios.get(api,{params: {StartTime: compareDateStartTime,EndTime:compareDateEndTime,Area:areaName}}),//获取对比天截止当前时间能耗
          this.axios.get(api,{params: {StartTime: compareDateStartTime,EndTime:compareDateAllEndTime,Area:areaName}}),//获取对比整天能耗
        ]).then(this.axios.spread((todayCon,CompareDateCon,CompareAllDateCon) =>{
          that.todayCon = JSON.parse(todayCon.data).value
          that.todayConUnit = JSON.parse(todayCon.data).unit
          that.CompareDateCon = JSON.parse(CompareDateCon.data).value
          that.CompareAllDateCon = JSON.parse(CompareAllDateCon.data).value
        }))
      },
      getChartData(){
        this.ChartsLoading = true
        var selectDate = moment(this.formParameters.date).format("YYYY-MM-DD")
        var areaName = ''
        if(this.newAreaName.areaName === "整厂区"){
          areaName = ""
        }else{
          areaName = this.newAreaName.areaName
        }
        //获取选择天总数据
        var dayStartTime = moment(this.formParameters.date).day(moment(this.formParameters.date).day()).startOf('day').format('YYYY-MM-DD HH:mm:ss'),
          dayEndTime = moment(this.formParameters.date).day(moment(this.formParameters.date).day()).endOf('day').format('YYYY-MM-DD HH:mm:ss')
        if(this.formParameters.energy === "电"){
          this.chartSettings.yAxisName = ["kW·h"]
          this.axios.get("/api/energyelectric",{params:{StartTime: dayStartTime,EndTime:dayEndTime,Area:areaName}}).then(thisDayCon => {
            this.totalDayEnergy = JSON.parse(thisDayCon.data).value
          })
        }else if(this.formParameters.energy === "水"){
          this.chartSettings.yAxisName = ["t"]
          this.axios.get("/api/energywater",{params:{StartTime: dayStartTime,EndTime:dayEndTime,Area:areaName}}).then(thisDayCon => {
            this.totalDayEnergy = JSON.parse(thisDayCon.data).value
          })
        }else if(this.formParameters.energy === "汽"){
          this.chartSettings.yAxisName = ["t"]
          this.axios.get("/api/energysteam",{params:{StartTime: dayStartTime,EndTime:dayEndTime,Area:areaName}}).then(thisDayCon => {
            this.totalDayEnergy = JSON.parse(thisDayCon.data).value
          })
        }
        //获取图表数据
        this.axios.get("/api/trendlookboard",{params: {EnergyClass: this.formParameters.energy,CompareTime:selectDate,AreaName:areaName}}).then(res =>{
          this.ChartsLoading = false
          this.chartData.rows = res.data.rows
          this.ChartExtend.title.text = this.formParameters.energy + "能总耗量：" + this.totalDayEnergy
        })
        //获取水能详细数据
        this.axios.get("/api/watertrendlookboard",{params: {AreaName:areaName,StartTime:dayStartTime,EndTime:dayEndTime}}).then(res =>{
          this.waterGG = res.data.GG + " t"
          this.waterGGCost = res.data.GGcost + " 元"
          this.waterYY = res.data.YY + " t"
          this.waterYYCost = res.data.YYcost + " 元"
          this.waterSJ = res.data.SJ + " t"
          this.waterSJCost = res.data.SJcost + " 元"
        })
      },
      getAreaTimeEnergy(){
        var params = {
          energyType: this.formParameters.energy,
          CompareDate:moment(this.formParameters.date).format('YYYY-MM-DD')
        }
        this.axios.get("/api/areaTimeEnergy",{params:params}).then(res => {
          this.colorBarOption = res.data
        })
      },
      getEnergycost(){  //获取尖峰平谷
        var that = this
        var areaName = ""
        if(this.newAreaName.areaName === "整厂区"){
          areaName = ""
        }else{
          areaName = this.newAreaName.areaName
        }
        var params = {
          StartTime:moment(this.formParameters.date).day(moment(this.formParameters.date).day()).startOf('day').format('YYYY-MM-DD HH:mm'),
          EndTime:moment(this.formParameters.date).day(moment(this.formParameters.date).day()).endOf('day').format('YYYY-MM-DD HH:mm'),
          TimeClass:"日",
          AreaName:areaName
        }
        this.axios.get("/api/electricnergycost",{params:params}).then(res => {
          that.electricAnalyze = res.data.periodTimeTypeItem
        })
      },
    }
  }
</script>

<style scoped>
  .energyDataCard{
    width:100%;
    background:#fff;
    border-radius:4px;
    padding:15px;
    margin-bottom:10px;
    clear: both;
    overflow: hidden;
  }
  .colorBar{float:right;}
  .colorBar li{
    display: inline-block;
    margin-right: 20px;
  }
  .colorBar li i{
    display: inline-block;
    width: 16px;
    height: 16px;
    border-radius: 2px;
    margin-right: 15px;
    vertical-align: middle;
  }
  .colorBar li span{
    display: inline-block;
    color: #082F4C;
    font-size: 16px;
    vertical-align: middle;
  }
  .realTimeCardTitle{
    font-size: 18px;
    color: #082F4C;
  }
  .realTimeCardTitle span{
    float: right;
  }
  .realTimeData{
    margin-top: 20px;
    font-size: 30px;
    color: #082F4C;
  }
  .energyDataItem{
    display: table;
    margin-bottom: 15px;
    font-size: 18px;
  }
  .energyDataItemTitle{
    float: left;
    color: rgba(8,47,76,0.62);
    margin-right: 20px;
  }
  .energyDataItemData{
    float: left;
    color: #082F4C;
  }
  .periodTimeItem {
    text-align: center;
    border: 1px solid rgba(8, 47, 76, 0.58);
    color: rgba(8, 47, 76, 0.58);
  }
</style>
