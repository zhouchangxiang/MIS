<template>
  <el-row :gutter="2">
    <el-col :span="24">
      <el-form :model="formParameters">
        <el-form-item label="时间：" style="margin-bottom: 0;">
          <el-radio-group v-model="formParameters.resourceTime" fill="#082F4C" size="mini">
            <el-radio-button v-for="item in radioTimeList" border :key="item.id" :label="item.name"></el-radio-button>
          </el-radio-group>
          <el-date-picker type="month" v-model="formParameters.startDate" :picker-options="pickerOptions" size="mini" format="yyyy-MM" style="width: 150px;" :clearable="false"></el-date-picker> ~
          <el-date-picker type="month" v-model="formParameters.endDate" :picker-options="pickerOptions" size="mini" format="yyyy-MM" style="width: 150px;" :clearable="false"></el-date-picker>
        </el-form-item>
        <el-form-item style="float: right;margin-bottom: 0;">
          <el-radio-group v-model="formParameters.energy" fill="#082F4C" size="small">
            <el-radio-button v-for="item in energyList" :key="item.id" :label="item.name"></el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="参数：" style="margin-bottom: 10px;">
          <el-radio-group v-model="formParameters.resourceType" fill="#082F4C" size="mini">
            <el-radio-button v-for="item in radioTypeList" border :key="item.id" :label="item.name"></el-radio-button>
          </el-radio-group>
        </el-form-item>
      </el-form>
    </el-col>
    <el-col :span="24" v-if="formParameters.resourceType == '基本电费'">
      <el-col :span="12" v-for="item in ElecCalculationTypeItem">
        <div class="ElecCalculationType">
          <p>{{ item.title }}</p>
          <el-col :span="8"><p class="text-color-caption">{{ item.typeTitle }}</p>{{ item.typeData }}</el-col>
          <el-col :span="8"><p class="text-color-caption">{{ item.unit }}</p>{{ item.unitData }}</el-col>
          <el-col :span="8"><p class="text-color-caption">{{ item.electricity }}</p>{{ item.electricityData }}</el-col>
        </div>
      </el-col>
      <el-col :span="24">
        <div class="energyDataContainer">
          <ve-histogram :data="basicElectricityChartData" :settings="basicElectricityChartSettings" :extend="basicElectricityChartExtend"></ve-histogram>
        </div>
      </el-col>
    </el-col>
    <el-col :span="24" v-if="formParameters.resourceType == '电度电费'">
      <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
        <div class="chartTile">趋势图</div>
        <div class="chartHeadRight">
          总电费：163411元
        </div>
      </div>
      <el-col :span="6" v-for="(item,index) in periodTimeTypeItem" style="margin-bottom:2px;">
        <div class="periodTimeTypeItem">
          <p>{{ item.title }} <span class="text-color-caption" style="float: right;">电价：{{ item.electrovalence }}元</span></p>
          <el-col :span="8"><p class="text-color-caption">电费/元</p>{{ item.electricity }}</el-col>
          <el-col :span="8"><p class="text-color-caption">电费占比</p>{{ item.Ratio }}</el-col>
          <el-col :span="8"><p class="text-color-caption">用电量/kwh</p>{{ item.usageAmount }}</el-col>
        </div>
      </el-col>
      <div class="energyDataContainer" style="margin-bottom:10px;">
        <ve-histogram :data="electricityPileChartData" :settings="electricityPileChartSettings" :extend="basicElectricityChartExtend"></ve-histogram>
      </div>
      <el-col :span="12" v-for="item in electricAnalyzeItem">
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
    <el-col :span="24" v-if="formParameters.resourceType == '力调电费'">
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
    </el-col>
  </el-row>
</template>

<script>
  var moment = require('moment');
  export default {
    name: "CostCenter",
    data(){
      this.basicElectricityChartSettings = {
        yAxisName: ['元']
      }
      this.basicElectricityChartExtend = {
        grid:{
          left:'0',
          right:'0',
          bottom:'0',
          top:'40px'
        },
        series:{
          barMaxWidth : 30
        }
      }
      this.electricityPileChartSettings = {
        stack: { '时段': ['谷时段','平时段','峰时段','尖时段'] }
      }
      return {
        formParameters:{
          resourceTime:"月",
          resourceType:"基本电费",
          startDate:moment().startOf('month').subtract('month',1).format('YYYY-MM'),
          endDate:Date.now(),
          energy:"电能"
        },
        radioTimeList:[
          {name:"月",id:1},
          {name:"年",id:2}
        ],
        radioTypeList:[
          {name:"基本电费",id:1},
          {name:"电度电费",id:2},
          {name:"力调电费",id:3},
          {name:"无功补偿",id:4},
          {name:"诺波治理",id:5}
        ],
        pickerOptions:{
          disabledDate(time) {
            return time.getTime() > Date.now();
          }
        },
        energyList:[
          {name:"电能",id:1},
          {name:"水能",id:2},
          {name:"汽能",id:3},
        ],
        ElecCalculationTypeIndex:0,
        ElecCalculationTypeItem:[
          {title:"按容量计算",typeTitle:"变压器容量",typeData:"1000kVA",unit:"单价",unitData:"20元/千伏安.月",electricity:"电费",electricityData:"20000元"},
          {title:"按需量计算",typeTitle:"最大需量",typeData:"536.44kw",unit:"单价",unitData:"20元/千瓦.月",electricity:"电费",electricityData:"20000元"}
        ],
        basicElectricityChartData: {
          columns: ['日期', '容量', '需量'],
          rows: [
            { '日期': '2019-1', '容量': 1393, '需量': 1093 },
            { '日期': '2019-2', '容量': 3530, '需量': 3230 },
            { '日期': '2019-3', '容量': 2923, '需量': 2623 },
            { '日期': '2019-4', '容量': 1723, '需量': 1423 },
            { '日期': '2019-5', '容量': 3792, '需量': 3492 },
            { '日期': '2019-6', '容量': 4593, '需量': 4293 }
          ]
        },
        periodTimeTypeItem:[
          {title:"尖时段",electrovalence:131521,electricity:131541,Ratio:"33.1%",usageAmount:135454},
          {title:"峰时段",electrovalence:131521,electricity:131541,Ratio:"33.1%",usageAmount:135454},
          {title:"平时段",electrovalence:131521,electricity:131541,Ratio:"33.1%",usageAmount:135454},
          {title:"谷时段",electrovalence:131521,electricity:131541,Ratio:"33.1%",usageAmount:135454}
        ],
        electricityPileChartData:{
          columns: ['日期', '谷时段','平时段','峰时段','尖时段'],
          rows: [
            { '日期': '01-01', '尖时段': 4393, '峰时段': 4093 , '平时段': 2345, '谷时段': 235},
            { '日期': '01-02', '尖时段': 5393, '峰时段': 4193 , '平时段': 2945, '谷时段': 635},
            { '日期': '01-03', '尖时段': 3393, '峰时段': 4593 , '平时段': 2345, '谷时段': 235},
            { '日期': '01-04', '尖时段': 5393, '峰时段': 4693 , '平时段': 3345, '谷时段': 935},
            { '日期': '01-05', '尖时段': 6393, '峰时段': 4093 , '平时段': 2745, '谷时段': 235},
            { '日期': '01-06', '尖时段': 5393, '峰时段': 4093 , '平时段': 2345, '谷时段': 235},
            { '日期': '01-07', '尖时段': 7393, '峰时段': 4493 , '平时段': 2345, '谷时段': 735},
            { '日期': '01-08', '尖时段': 3393, '峰时段': 4093 , '平时段': 2345, '谷时段': 235},
            { '日期': '01-09', '尖时段': 5393, '峰时段': 4093 , '平时段': 2345, '谷时段': 235},
            { '日期': '01-09', '尖时段': 5393, '峰时段': 4093 , '平时段': 2345, '谷时段': 235},
            { '日期': '01-09', '尖时段': 5393, '峰时段': 4093 , '平时段': 2345, '谷时段': 235},
            { '日期': '01-09', '尖时段': 5393, '峰时段': 4093 , '平时段': 2345, '谷时段': 235}
          ]
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
        }
      }
    },
    mounted(){

    },
    methods:{
      selectElecCalculationType(index){
        this.ElecCalculationTypeIndex = index;
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
