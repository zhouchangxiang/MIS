<template>
    <el-row :gutter="10">
      <el-col :span="24">
        <el-form :inline="true" :model="formParameters">
          <el-form-item label="时间：">
            <el-date-picker type="date" v-model="formParameters.date" :picker-options="pickerOptions" size="mini" format="yyyy-MM-dd" style="width: 130px;" :clearable="false" @change="getChartData(),getAreaTimeEnergy()"></el-date-picker>
          </el-form-item>
          <el-form-item style="float: right;">
            <el-radio-group v-model="formParameters.energy" fill="#082F4C" size="small" @change="getChartData(),getAreaTimeEnergy()">
              <el-radio-button v-for="(item,index) in energyList" :key="item.index" :label="item.label"></el-radio-button>
            </el-radio-group>
          </el-form-item>
        </el-form>
      </el-col>
      <el-col :span="24" v-if="newAreaName.areaName != '整厂区'">
        <el-col :span="18">
          <div class="energyDataCard">
            <ve-line :data="chartData" :settings="chartSettings" :extend="ChartExtend"></ve-line>
          </div>
          <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
            <div class="chartTile">尖峰平谷分析</div>
          </div>
          <div class="platformContainer">
            <el-row :gutter="20" style="margin-bottom: 10px;">
              <el-col :span="9">
                <p class="text-size-normol">尖时段</p>
                <span class="text-size-mini text-color-info-shallow">共{{ electricAnalyze.sharpTime }}小时</span>
                <el-row>
                  <el-col :span="14">
                    <el-progress :text-inside="true" :stroke-width="16" :percentage="electricAnalyze.sharp" color="#FB3A06"></el-progress>
                  </el-col>
                  <el-col :span="10">
                    <p class="text-color-info" style="padding-left: 10px;">耗能：253kwh</p>
                  </el-col>
                </el-row>
              </el-col>
              <el-col :span="9">
                <p class="text-size-normol">峰时段</p>
                <span class="text-size-mini text-color-info-shallow">共{{ electricAnalyze.peakTime }}小时</span>
                <el-row>
                  <el-col :span="14">
                    <el-progress :text-inside="true" :stroke-width="16" :percentage="electricAnalyze.peak" color="#FB8A06"></el-progress>
                  </el-col>
                  <el-col :span="10">
                    <p class="text-color-info" style="padding-left: 10px;">耗能：253kwh</p>
                  </el-col>
                </el-row>
              </el-col>
              <el-col :span="6">
                <p class="text-color-info-shallow" style="margin-bottom: 15px;">总电费：</p>
                <p>{{ electricAnalyze.total }}元</p>
              </el-col>
            </el-row>
            <el-row :gutter="20" style="margin-bottom: 10px;">
              <el-col :span="9">
                <p class="text-size-normol">平时段</p>
                <span class="text-size-mini text-color-info-shallow">共{{ electricAnalyze.poiseTime }}小时</span>
                <el-row>
                  <el-col :span="14">
                    <el-progress :text-inside="true" :stroke-width="16" :percentage="electricAnalyze.poise" color="#F8E71C"></el-progress>
                  </el-col>
                  <el-col :span="10">
                    <p class="text-color-info" style="padding-left: 10px;">耗能：253kwh</p>
                  </el-col>
                </el-row>
              </el-col>
              <el-col :span="9">
                <p class="text-size-normol">谷时段</p>
                <span class="text-size-mini text-color-info-shallow">共{{ electricAnalyze.ebbTime }}小时</span>
                <el-row>
                  <el-col :span="14">
                    <el-progress :text-inside="true" :stroke-width="16" :percentage="electricAnalyze.ebb" color="#15CC48"></el-progress>
                  </el-col>
                  <el-col :span="10">
                    <p class="text-color-info" style="padding-left: 10px;">耗能：253kwh</p>
                  </el-col>
                </el-row>
              </el-col>
              <el-col :span="6">
                <p class="text-color-info-shallow" style="margin-bottom: 15px;">平均电价：</p>
                <p>{{ electricAnalyze.average }}元</p>
              </el-col>
            </el-row>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="energyDataCard">
            <div class="realTimeCardTitle">实时数据 <span>kwh</span></div>
            <div class="realTimeData itemMarginBottom">22432</div>
          </div>
          <div class="energyDataCard">
            <div class="energyDataItem">
              <div class="energyDataItemTitle">
                <el-date-picker type="date" v-model="CompareDate" :picker-options="pickerOptions" size="mini" style="width: 130px;" :clearable="false"></el-date-picker>
              </div>
            </div>
            <div class="energyDataItem">
              <div class="energyDataItemTitle">今日能耗</div>
              <div class="energyDataItemData">{{ todayCon }} {{ todayConUnit }}</div>
            </div>
            <div class="energyDataItem">
              <div class="energyDataItemTitle">对比</div>
              <div class="energyDataItemData">{{ compareRatio }}</div>
            </div>
          </div>
          <div class="energyDataCard">
            <div class="realTimeCardTitle" style="margin-bottom: 10px;">避峰用谷分析（参考）</div>
            <el-col :span="14">
              <p class="text-size-normol">尖时段</p>
              <span class="text-size-mini text-color-info-shallow">共{{ rationalAnalyze.sharpTime }}小时</span>
              <p><el-progress :text-inside="true" :stroke-width="16" :percentage="electricAnalyze.sharp" color="#FB3A06"></el-progress></p>
              <p class="text-size-normol" style="margin-top: 10px;">峰时段</p>
              <span class="text-size-mini text-color-info-shallow">共{{ rationalAnalyze.peakTime }}小时</span>
              <p><el-progress :text-inside="true" :stroke-width="16" :percentage="electricAnalyze.peak" color="#FB8A06"></el-progress></p>
              <p class="text-size-normol" style="margin-top: 10px;">平时段</p>
              <span class="text-size-mini text-color-info-shallow">共{{ rationalAnalyze.poiseTime }}小时</span>
              <p><el-progress :text-inside="true" :stroke-width="16" :percentage="electricAnalyze.poise" color="#F8E71C"></el-progress></p>
              <p class="text-size-normol" style="margin-top: 10px;">谷时段</p>
              <span class="text-size-mini text-color-info-shallow">共{{ rationalAnalyze.ebbTime }}小时</span>
              <p><el-progress :text-inside="true" :stroke-width="16" :percentage="electricAnalyze.ebb" color="#15CC48"></el-progress></p>
            </el-col>
            <el-col :span="10">
              <p class="text-size-normol text-color-info-shallow" style="margin-bottom: 15px;">总电费：</p>
              <p class="text-size-normol text-color-info" style="margin-bottom: 20px;">553545.5 元</p>
              <p class="text-size-normol text-color-info-shallow" style="margin-bottom: 15px;">平均电价：</p>
              <p class="text-size-normol text-color-info" style="margin-bottom: 20px;">0.89 元</p>
              <p class="text-size-normol text-color-info-shallow" style="margin-bottom: 15px;">建议：</p>
              <p class="text-size-mini text-color-danger">设备尽量在峰段（高电价）时刻检修，在平或谷（低电价）生产，可以降低能耗成本</p>
            </el-col>
          </div>
        </el-col>
      </el-col>
      <el-col :span="24" v-if="newAreaName.areaName == '整厂区'">
        <el-col :span="18">
          <div class="energyDataCard">
            <ve-line :data="chartData" :settings="chartSettings" :extend="ChartExtend" height="300px"></ve-line>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="energyDataCard">
            <div class="realTimeCardTitle">实时数据 <span>kwh</span></div>
            <div class="realTimeData itemMarginBottom">22432</div>
          </div>
          <div class="energyDataCard" style="margin-bottom: 0">
            <div class="energyDataItem" style="margin-top: 8px">
              <div class="energyDataItemTitle">
                <el-date-picker type="date" v-model="CompareDate" :picker-options="pickerOptions" size="mini" style="width: 130px;" :clearable="false" @change="getDayEnergy"></el-date-picker>
              </div>
            </div>
            <div class="energyDataItem">
              <div class="energyDataItemTitle">今日能耗</div>
              <div class="energyDataItemData">{{ todayCon }} {{ todayConUnit }}</div>
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
              <li v-for="(item,index) in colorBarOption">
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
        todayCon:"",
        todayConUnit:"",
        CompareDate:moment().subtract(1,'day').format('YYYY-MM-DD'),
        CompareDateCon:"",
        pickerOptions:{
          disabledDate(time) {
            return time.getTime() > Date.now();
          }
        },
        AllArea:false,
        chartSettings: {
          area:true
        },
        ChartExtend: {
          title:{
            text:"能耗趋势"
          },
          grid:{
            left:'0px',
            right:'10px',
            bottom:'0',
            top:'50px'
          },
          series:{
            smooth: false
          }
        },
        chartData:{
          columns:["时间","能耗量"],
          rows:[]
        },
        electricAnalyze:{
          sharpTime:3,
          sharp:100,
          peakTime:7,
          peak:87.5,
          total:553524.5,
          poiseTime:6,
          poise:33.3,
          ebbTime:8,
          ebb:12.5,
          average:0.89,
        },
        rationalAnalyze:{
          sharpTime:3,
          sharp:100,
          peakTime:7,
          peak:87.5,
          poiseTime:6,
          poise:33.3,
          ebbTime:8,
          ebb:12.5,
          total:553524.5,
          average:0.89
        },
        colorBarOption:[]
      }
    },
    created(){
      this.getDayEnergy()
      this.getAreaTimeEnergy()
      this.getChartData()
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
        if(this.formParameters.energy == "电"){
          api = "/api/energyelectric"
        }else if(this.formParameters.energy == "水"){
          api = "/api/energywater"
        }else if(this.formParameters.energy == "汽"){
          api = "/api/energysteam"
        }
        var nowTime = moment().format('HH:mm').substring(0,4) + "0"
        var todayStartTime = moment().format('YYYY-MM-DD') + " 00:00"
        var todayEndTime = moment().format('YYYY-MM-DD') + " " + nowTime
        var compareDateStartTime = moment(this.CompareDate).format('YYYY-MM-DD') + " 00:00"
        var compareDateEndTime = moment(this.CompareDate).format('YYYY-MM-DD') + " " + nowTime
        this.axios.all([
          this.axios.get(api,{params: {StartTime: todayStartTime,EndTime:todayEndTime}}),//获取今天能耗
          this.axios.get(api,{params: {StartTime: compareDateStartTime,EndTime:compareDateEndTime}})//获取对比天能耗
        ]).then(this.axios.spread(function(todayCon,CompareDateCon){
          that.todayCon = JSON.parse(todayCon.data).value
          that.todayConUnit = JSON.parse(todayCon.data).unit
          that.CompareDateCon = JSON.parse(CompareDateCon.data).value
        }))
      },
      getChartData(){
        var selectDate = moment(this.formParameters.date).format("YYYY-MM-DD")
        this.axios.get("/api/trendlookboard",{params: {EnergyClass: this.formParameters.energy,CompareTime:selectDate}}).then(res =>{
          this.chartData.rows = res.data.rows
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
    margin-bottom: 20px;
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
