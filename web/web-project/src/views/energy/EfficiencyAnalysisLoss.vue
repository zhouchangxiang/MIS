<template>
  <el-row :gutter="20">
    <el-col :span="24">
      <el-form :inline="true" :model="formParameters">
        <el-form-item label="时间：">
          <el-radio-group v-model="formParameters.resourceTime" fill="#082F4C" size="mini">
            <el-radio-button v-for="item in radioTimeList" border :key="item.id" :label="item.name"></el-radio-button>
          </el-radio-group>
          <el-date-picker type="datetime" v-model="formParameters.startDate" :picker-options="pickerOptions" size="mini" style="width: 180px;" :clearable="false"></el-date-picker>
        </el-form-item>
        <el-form-item style="float: right;">
          <el-radio-group v-model="formParameters.energy" fill="#082F4C" size="small">
            <el-radio-button v-for="item in energyList" :key="item.id" :label="item.name"></el-radio-button>
          </el-radio-group>
        </el-form-item>
      </el-form>
    </el-col>
    <el-col :span="24">
      <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
        <div class="chartTile">趋势图 <span class="text-color-info-shallow text-size-normol">当前视在功率等级 优 额定功率 10kw</span></div>
      </div>
      <div class="platformContainer">
        <el-col :span="6">
          <div class="platformItem">
            <p style="margin-bottom: 10px;">线损率<span class="float-right text-size-mini text-color-info-shallow">选择对比</span></p>
            <p><label class="text-size-big text-color-primary">1.93%</label><span class="float-right">0.15%</span></p>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="platformItem">
            <p style="margin-bottom: 10px;">输入总电量<span class="text-size-mini text-color-info-shallow">kwh</span><span class="float-right text-size-mini text-color-info-shallow">选择对比</span></p>
            <p><label class="text-size-big text-color-primary">16415.1</label><span class="float-right">0.15%</span></p>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="platformItem">
            <p style="margin-bottom: 10px;">输出电量<span class="text-size-mini text-color-info-shallow">kwh</span><span class="float-right text-size-mini text-color-info-shallow">选择对比</span></p>
            <p><label class="text-size-big text-color-primary">6464.35</label><span class="float-right">0.15%</span></p>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="platformItem">
            <p style="margin-bottom: 10px;">线损<span class="text-size-mini text-color-info-shallow">kwh</span><span class="float-right text-size-mini text-color-info-shallow">选择对比</span></p>
            <p><label class="text-size-big text-color-primary">72.3</label><span class="float-right">0.15%</span></p>
          </div>
        </el-col>
      </div>
      <div class="energyDataContainer">
        <ve-histogram :data="lineLossChartData" :extend="ChartExtend" :settings="chartSettings"></ve-histogram>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  export default {
    name: "EfficiencyAnalysisLoss",
    data(){
      this.ChartExtend = {
        grid:{
          left:'0',
          right:'0',
          bottom:'0',
          top:'40px'
        },
        'series.1.itemStyle.normal.lineStyle': {
            width:2,
            type:'dotted'
        },
        series:{
          barMaxWidth : 30,
          smooth: false
        }
      }
      this.chartSettings = {
        showLine: ['选择日']
      }
      return {
        formParameters:{
          resourceTime:"班次",
          startDate:Date.now(),
          energy:"电能"
        },
        radioTimeList:[
          {name:"班次",id:1},
          {name:"日",id:2},
          {name:"周",id:3},
          {name:"月",id:4},
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
        lineLossChartData:{
          columns: ['时间', '今日', '选择日'],
          rows: [
            { '时间': '00:00', '今日': 447, '选择日': 493},
            { '时间': '01:00', '今日': 857, '选择日': 820},
            { '时间': '02:00', '今日': 875, '选择日': 823},
            { '时间': '03:00', '今日': 755, '选择日': 743},
            { '时间': '04:00', '今日': 745, '选择日': 742},
            { '时间': '05:00', '今日': 688, '选择日': 623}
          ]
        }
      }
    }
  }
</script>

<style scoped>
  .platformItem{
   background: #EEEEEE;
   border-radius:4px;
   padding: 15px;
 }
</style>
