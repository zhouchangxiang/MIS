<template>
  <div class="home-container">
    <el-row :gutter="15">
      <el-col :span="17">
        <div class="home-card">
          <div class="home-card-head">
            <span><i class="el-icon-time el-icon--left" style="color: #FB3A06;"></i>能耗预览</span>
            <el-select class="card-head-select" v-model="previewEnergyValue" placeholder="请选择" @change="getEnergyPreview">
              <el-option v-for="(item,index) in previewEnergyOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </div>
          <div class="home-card-body" style="height: 462px;">
            <el-row :gutter="10">
              <el-col :span="7" style="white-space:nowrap;">
                <ul class="card-body-ul">
                  <li><span class="text-size-large text-color-info">本日耗{{ previewEnergyValue }}量</span>
                    <span class="text-size-mini text-color-info-shallow">（截止{{ nowTime }}）</span>
                  <li class="text-size-big text-color-warning">{{ todayCon }}{{ unit }}</li>
                  <li><span class="text-size-mini text-color-info-shallow">对比</span>
                    <el-date-picker v-model="CompareDate" align="right" type="date" placeholder="选择日期" :picker-options="pickerOptions" @change="getEnergyPreview" :clearable="false" size="mini" style="width: 130px"></el-date-picker>
                  </li>
                  <li><span class="text-size-small text-color-primary">{{ compareDateCon }}{{ unit }}</span>
                    <span class="text-size-mini" :class="todayCon-compareDateCon>0?'text-color-danger':'text-color-success'" style="margin-left: 20px;">{{ comparePer }}</span></li>
                </ul>
              </el-col>
              <el-col :span="9" style="white-space:nowrap;">
                <el-col :span="24">
                  <span class="text-size-large text-color-info">本月耗{{ previewEnergyValue }}量</span>
                  <span class="text-size-mini text-color-info-shallow">（截止{{ nowDate }}）</span>
                </el-col>
                <el-col :span="12">
                  <ul class="card-body-ul">
                    <li></li>
                    <li class="text-size-big text-color-warning">{{ thisMonthCon }}{{ unit }}</li>
                    <li style="margin-top: 15px;">
                      <span class="text-size-mini text-color-info-shallow">上月同期</span>
                      <span class="text-size-mini text-color-info">{{ lastMonthCon }}{{ unit }}</span>
                    </li>
                    <li>
                      <span class="text-size-mini text-color-info-shallow">同期对比</span>
                      <span class="text-size-mini" :class="thisMonthCon-lastMonthCon>0?'text-color-danger':'text-color-success'">{{ lastMonthCompare }}</span>
                    </li>
                  </ul>
                </el-col>
                <el-col :span="12">
                  <ve-line :data="contrastMonthChartData" :settings="contrastMonthChartSettings" :extend="contrastMonthChartExtend" v-loading="ChartsLoading" width="120px" height="100px" :legend-visible="false"></ve-line>
                </el-col>
              </el-col>
              <el-col :span="8" style="white-space:nowrap;">
                <ul class="card-body-ul">
                  <li>
                    <span class="text-size-large text-color-info">年累计耗{{ previewEnergyValue }}量</span>
                    <span class="text-color-warning text-size-mini">{{ unit }}</span>
                  </li>
                  <li class="text-size-big text-color-primary" v-html="thisYearHtml">{{ thisYearCon }}</li>
                  <li style="margin-top: 15px;">
                    <span class="text-size-mini text-color-info-shallow">上年同期</span>
                    <span class="text-size-mini text-color-info">{{ lastYearCon }}{{ unit }}</span>
                    <span style="margin-left: 20px;" class="text-size-mini" :class="thisYearCon-lastYearCon>0?'text-color-danger':'text-color-success'">{{ lastYearCompare }}</span>
                  </li>
                </ul>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="24">
                <span class="text-size-small text-color-info">今日对比能耗</span>
                <span class="text-size-small text-color-primary" @click="$router.push({ path:'/DataReport'})" style="float: right;cursor: pointer;">查看报表<i class="el-icon-d-arrow-right el-icon--right"></i></span>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="24">
                <ve-line :data="realtimeChartData" :extend="realtimeChartExtend" v-loading="ChartsLoading" height="260px" :legend-visible="true"></ve-line>
              </el-col>
            </el-row>
          </div>
        </div>
        <el-row :gutter="15">
          <el-col :span="10">
            <div class="home-card-head">
              <span><i class="el-icon-place el-icon--left" style="color: #228AD5;"></i>区域时段能耗</span>
              <el-select class="card-head-select" v-model="areaTimeEnergyValue" placeholder="请选择" @change="getAreaTimeEnergy">
                <el-option v-for="(item,index) in areaTimeEnergyOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
              </el-select>
            </div>
            <div class="home-card-body" style="height:280px;">
              <ve-bar :data="areaChartData" :extend="areaTimeChartExtend" v-loading="areaTimeChartsLoading" height="230px" :legend-visible="false"></ve-bar>
              <span class="text-size-small text-color-primary" @click="$router.push({ path:'/Areas?areaName=整厂区&navOptionsCurrent=2'})" style="float: right;cursor: pointer;">查看更多<i class="el-icon-d-arrow-right el-icon--right"></i></span>
            </div>
          </el-col>
          <el-col :span="7">
            <div class="home-card-head">
              <span><i class="el-icon-odometer el-icon--left" style="color: #FB3A06;"></i>电能负荷率</span>
            </div>
            <div class="home-card-body" style="height:280px;text-align: center">
              <ul class="colorBar">
                <li><i class="bg-tall"></i><span>差</span></li>
                <li><i class="bg-center"></i><span>中</span></li>
                <li><i class="bg-fine"></i><span>良</span></li>
                <li><i class="bg-best"></i><span>优</span></li>
              </ul>
              <ve-gauge :data="electricLoadRateChartData" :extend="electricLoadRateChartExtend" height="200px"></ve-gauge>
              <el-select class="" v-model="electricLoadRateTime" size="small" style="width: 80px;" @change="getElectricLoadRateTime">
                <el-option v-for="(item,index) in electricLoadRateTimeOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
              </el-select>
            </div>
          </el-col>
          <el-col :span="7">
            <div class="home-card-head">
              <span><i class="el-icon-s-order el-icon--left" style="color: #15CC48;"></i>在线情况检测</span>
            </div>
            <div class="home-card-body" style="height:280px;">
              <ul>
                <li v-for="item in onlineEquipmentOption" class="itemMarginBottom">
                  <p class="text-size-normol text-color-info" style="margin-bottom: 5px;">{{ item.name }}</p>
                  <p class="text-size-mini text-color-info-shallow" style="margin-bottom: 5px;"><span>上线数/总数</span><span style="float: right;">{{ item.online }}/{{ item.total }}</span></p>
                  <el-progress :text-inside="true" :stroke-width="16" strokeLinecap="square" :color="item.rate == 100?'#15CC48':'#FB8A06'" :percentage="item.rate"></el-progress>
                </li>
              </ul>
            </div>
          </el-col>
        </el-row>
      </el-col>
      <el-col :span="7">
        <div class="home-card">
          <div class="home-card-head">
            <span><i class="el-icon-bell el-icon--left" style="color: #FB3A06;"></i>实时预警</span>
          </div>
          <div class="home-card-body" style="height: 300px;">
            <el-table :data="ralTimeWarningTableData" size="mini" height="232px" max-height="232px" empty-text="暂无异常" style="width: 100%">
              <el-table-column prop="AreaName" label="区域"></el-table-column>
              <el-table-column prop="EQPName" label="设备"></el-table-column>
              <el-table-column prop="WarningType" label="状态">
                <template slot-scope="scope">
                  <span class="text-size-mini text-color-warning">{{ scope.row.WarningType }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="WarningDate" label="时间"></el-table-column>
            </el-table>
            <span class="text-size-mini text-color-primary" @click="$router.push({ path:'/Areas?navOptionsCurrent=5'})" style="float: right;margin-top: 15px;cursor: pointer;">更多记录<i class="el-icon-d-arrow-right el-icon--right"></i></span>
          </div>
        </div>
        <div class="home-card">
          <div class="home-card-head">
            <span><i class="el-icon-bell el-icon--left" style="color: #228AD5;"></i>单位批次能耗</span>
          </div>
          <div class="home-card-body" style="height: 300px;">
            <p>
              <span style="font-size: 48px;" class="text-color-primary">{{ lotsBatchCount }}<span class="text-size-mini">批</span></span>
              <el-select class="" v-model="lotsEnergyValue" size="small" style="width: 80px;float: right;" @change="getBatchEnergy">
                <el-option v-for="item in lotsEnergyOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
              </el-select>
              <el-select class="" v-model="areaNameValue" size="small" style="width: 120px;float: right;margin-right: 10px;" @change="getBatchEnergy">
                <el-option v-for="item in areaOptions" :key="item.ID" :label="item.AreaName" :value="item.AreaName"></el-option>
              </el-select>
            </p>
            <el-table :data="lotsEnergyTableData" size="small" height="160px" max-height="160px" style="width: 100%">
              <el-table-column prop="type" label="类型"></el-table-column>
              <el-table-column prop="total" label="总量">
                <template slot-scope="scope">
                  <span class="text-size-mini text-color-info-shallow">{{ scope.row.Con }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="unitNum" label="单位耗量">
                <template slot-scope="scope">
                  <span class="text-size-mini text-color-primary">{{ scope.row.EveryBatch }}</span>
                </template>
              </el-table-column>
            </el-table>
            <span class="text-size-mini text-color-primary" @click="$router.push({ path:'/Areas?navOptionsCurrent=4'})" style="float: right;margin-top: 15px;cursor: pointer;">查看详情<i class="el-icon-d-arrow-right el-icon--right"></i></span>
          </div>
        </div>
        <div class="home-card-body" style="height: 130px;text-align: center;">
          <p class="text-size-big text-color-primary">系统体检</p>
          <a href="javascript:;" class="systemCheckup" @click="openSystemCheckupDialog">立即体检</a>
          <el-dialog title="系统体检" :close-on-press-escape="false" :close-on-click-modal="false" :show-close="false" :visible.sync="systemCheckupDialogVisible" width="80%" center>
            <el-row :gutter="15">
              <el-col :span="6" v-for="item in systemCheckupList" :key="item.item.name" class="itemMarginBottom">
                <el-card class="box-card" shadow="hover">
                  <el-form>
                    <el-form-item label="执行任务"><span class="text-color-primary text-size-normol">{{ item.item.name }}</span></el-form-item>
                    <el-form-item label="执行成功次数"><span class="text-color-info text-size-normol">{{ item.item.successNumber }}</span></el-form-item>
                    <el-form-item label="执行失败次数"><span class="text-color-info text-size-normol">{{ item.item.errorNumber }}</span></el-form-item>
                    <el-form-item label="总共执行次数"><span class="text-color-info text-size-normol">{{ item.item.totalNumber }}</span></el-form-item>
                    <el-form-item label="开始执行时间"><span class="text-color-info text-size-normol">{{ item.item.startTime }}</span></el-form-item>
                    <el-form-item label="最后刷新时间"><span class="text-color-info text-size-normol">{{ item.item.endTime }}</span></el-form-item>
                    <el-form-item label="执行状态"><p style="display: grid;padding: 0 10px;" :style="item.item.state == '执行成功'?'background:rgb(125, 247, 159)':'background:#FB8A06'">{{ item.item.state }}</p></el-form-item>
                  </el-form>
                </el-card>
              </el-col>
            </el-row>
            <span slot="footer" class="dialog-footer">
              <el-button type="primary" @click="startSystemCheckup">开 始 体 检</el-button>
              <el-button @click="systemCheckupDialogVisible = false">关 闭</el-button>
            </span>
          </el-dialog>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  var moment = require('moment');
  export default {
    name: "Home",
    data(){
      return{
        previewEnergyOptions: [{
          value: '电',
          label: '电能'
        }, {
          value: '水',
          label: '水能'
        }, {
          value: '汽',
          label: '汽能'
        }],
        previewEnergyValue:'电',
        areaTimeEnergyOptions: [{
          value: '电',
          label: '电能'
        }, {
          value: '水',
          label: '水能'
        }, {
          value: '汽',
          label: '汽能'
        }],
        areaTimeEnergyValue:'电',
        pickerOptions: {
          disabledDate(time) {
            return time.getTime() > (Date.now() - 3600 * 1000 * 24);
          },
          shortcuts: [{
            text: '昨天',
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24);
              picker.$emit('pick', date);
            }
          }, {
            text: '一周前',
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit('pick', date);
            }
          }]
        },
        nowTime:"", //当前时间整分
        nowDate:"", //当前日时间整分
        CompareDate:Date.now() - 3600 * 1000 * 24, //默认对比日期
        unit:"", //当前数据单位
        todayCon:"", //本日能耗量
        compareDateCon:"", //选择日期的能耗
        thisMonthCon:"", //本月能耗量
        lastMonthCon:"", //上月同期能耗量
        contrastMonthChartData:{
          columns: ['日期', '上月能耗', '本月能耗'],
          rows:[]
        },
        realtimeChartData:{
          columns: ['时间', '今日能耗', '对比日能耗'],
          rows:[]
        },
        thisYearCon: "", //年能耗量
        thisYearHtml:"",
        lastYearCon: "", //上年同期能耗
        contrastMonthChartSettings: { //本月对比上月能耗图表配置
          area: false,
        },
        ChartsLoading:false,
        contrastMonthChartExtend: {
          yAxis:{
            show:false
          },
          xAxis:{
            show:false
          },
          grid:{
            left: '-20px',
            right: '0',
            bottom: '-10px',
            top:'10px'
          },
          'series.0.itemStyle': {
            color:"#228AD5"
          },
          'series.0.lineStyle':{
            color:"#228AD5",
            width:2
          },
          'series.1.itemStyle': {
            color:"#FB8A06"
          },
          'series.1.lineStyle':{
            color:"#FB8A06",
            width:2,
            type:'dotted'
          },
          series: {
            smooth: false,
            symbolSize: 1
          }
        },
        realtimeChartExtend: { //今日对比能耗图表配置
          yAxis:{
            axisLabel:{
              show:false
            }
          },
          grid:{
            left: '0px',
            right: '0',
            bottom: '0',
            top:'30px'
          },
          'series.0.itemStyle': {
            color:"#228AD5"
          },
          'series.0.lineStyle':{
            color:"#228AD5",
            width:2
          },
          'series.1.itemStyle': {
            color:"#FB8A06"
          },
          'series.1.lineStyle':{
            color:"#FB8A06",
            width:2,
            type:'dotted'
          },
          series: {
            smooth: false,
            symbolSize: 1
          }
        },
        areaTimeChartsLoading:false,
        areaTimeChartExtend: {
          yAxis:{
            show:false,
            inverse:true
          },
          xAxis:{
            show:false
          },
          grid:{
            containLabel: false,
            left: '20px',
            right: '0',
            bottom: '0',
            top:'0'
          },
          series: {
            barMaxWidth : 30,
            smooth: false
          },
          label:{
            show:true,
            position:"insideLeft",
            formatter: '{b}: {@score}'
          },
          itemStyle: {
            color:"#228AD5"
          }
        },
        areaChartData:{
          columns: ['区域', '能耗量'],
          rows:[]
        },
        electricLoadRateChartData:{
          columns: ['type', 'value'],
          rows: [
            { type: '占比', value: 0 }
          ]
        },
        electricLoadRateChartExtend: { //电能负荷率图表配置
          series: {
            min: 0,
            max: 100,
            radius: '90%',
            axisLine:{ //轴线
              lineStyle: {
                width: 10,
                color:[[0.3, '#FB3A06'], [0.5, '#FB8A06'], [0.8, '#228AD5'], [1, '#15CC48']]
              }
            },
            splitLine:{ //分割线
              length: 20,
                lineStyle: {
                  color: 'auto'
                }
            },
            axisTick: { //刻度
              length: 15,
              lineStyle: {
                color: 'auto'
              }
            },
            axisLabel:{  //刻度标签
              color: '#082F4C',
            },
            detail:{ //显示数据
              formatter: '{value}%',
              fontWeight: 'bold',
              color: '#082F4C',
              fontSize:24,
              offsetCenter:["0","75%"]
            }
          }
        },
        electricLoadRateTimeOptions: [{ //电能负荷率下拉框
          value: '日',
          label: '本日'
        }, {
          value: '月',
          label: '本月'
        }, {
          value: '年',
          label: '本年'
        }],
        electricLoadRateTime:'日', //默认下拉
        onlineEquipmentOption:[], //在线情况采集
        ralTimeWarningTableData:[],//实时预警表格数据
        areaNameValue:"提取二车间",
        areaOptions:[],  //批次能耗内区域下拉框
        lotsEnergyValue:"日",
        lotsEnergyOptions:[{ //批次能耗时段下拉框
          value: '日',
          label: '本日'
        }, {
          value: '月',
          label: '本月'
        }, {
          value: '年',
          label: '本年'
        }],
        lotsBatchCount:"",
        lotsEnergyTableData:[
          {type:"水能",Con:"",EveryBatch:""},
          {type:"汽能",Con:"",EveryBatch:""}
        ],
        systemCheckupDialogVisible:false, //是否展开系统体检对话框
        systemCheckupList:[
          {item: {
            name: "采集服务",
            successNumber: "",
            errorNumber: "",
            totalNumber: "",
            startTime: "",
            endTime: "",
            state: ""
          }},
          {item: {
            name: "写入历史数据库服务",
            successNumber: "",
            errorNumber: "",
            totalNumber: "",
            startTime: "",
            endTime: "",
            state: ""
          }},
          {item: {
            name: "写入增量服务",
            successNumber: "",
            errorNumber: "",
            totalNumber: "",
            startTime: "",
            endTime: "",
            state: ""
          }},
          {item: {
            name: "实时数据服务（websocket）",
            successNumber: "",
            errorNumber: "",
            totalNumber: "",
            startTime: "",
            endTime: "",
            state: ""
          }}
        ],
      }
    },
    created(){
      this.getEnergyPreview()
      this.getAreaTimeEnergy()
      this.getElectricLoadRateTime()
      this.getOnLineEq()
      this.getArea()
      this.getBatchEnergy()
    },
    watch:{
      thisYearCon(newValue){
        if(newValue != ""){
          var thisYearConStr = newValue.toString().split("")
          var html = ""
          thisYearConStr.forEach(item =>{
            if(item === "."){
              html += `<span style="margin-right: 3px;">${item}</span>`
            }else{
              html += `<span class="numBlock">${item}</span>`
            }
          })
          this.thisYearHtml = html
        }
      }
    },
    computed:{ //计算属性
      comparePer(){
        if(this.todayCon > 0){
          var compare = (this.todayCon - this.compareDateCon) / this.todayCon * 100
          if(this.todayCon - this.compareDateCon > 0){
            return "+" + compare.toFixed(2) + "%"
          }else{
            return compare.toFixed(2) + "%"
          }
        }else{
          if(this.compareDateCon > 0){
            return "-" + 100 + "%"
          }else{
            return 0 + "%"
          }
        }
      },
      lastMonthCompare(){
        if(this.thisMonthCon > 0){
          var compare = (this.thisMonthCon - this.lastMonthCon) / this.thisMonthCon * 100
          if(this.thisMonthCon - this.lastMonthCon > 0){
            return "+" + compare.toFixed(2) + "%"
          }else{
            return compare.toFixed(2) + "%"
          }
        }else{
          if(this.lastMonthCon > 0){
            return "-" + 100 + "%"
          }else{
            return 0 + "%"
          }
        }
      },
      lastYearCompare(){
        if(this.thisYearCon > 0){
          var compare = (this.thisYearCon - this.lastYearCon) / this.thisYearCon * 100
          if(this.thisYearCon - this.lastYearCon > 0){
            return "+" + compare.toFixed(2) + "%"
          }else{
            return compare.toFixed(2) + "%"
          }
        }else{
          if(this.lastYearCon > 0){
            return "-" + 100 + "%"
          }else{
            return 0 + "%"
          }
        }
      }
    },
    methods: {
      getEnergyPreview() {  //获取能耗预览内的数据
        var api = "",
          that = this,
          nowTime = moment().format('HH:mm').substring(0,4) + "0",
          nowDate = moment().format('MM-DD') + " " + nowTime,
          thisDate = moment().format('DD'),
          todayStartTime = moment().format('YYYY-MM-DD') + " 00:00",
          todayEndTime = moment().format('YYYY-MM-DD') + " " + nowTime,
          compareDateStartTime = moment(this.CompareDate).format('YYYY-MM-DD') + " 00:00",
          compareDateEndTime = moment(this.CompareDate).format('YYYY-MM-DD') + " " + nowTime,
          thisStartMonth = moment().month(moment().month()).startOf('month').format('YYYY-MM-DD HH:mm'),
          lastStartMonth = moment().month(moment().month() - 1).startOf('month').format('YYYY-MM-DD HH:mm'),
          lastEndMonth = moment().month(moment().month() - 1).endOf('month').format('YYYY-MM-DD').substring(0,7) + "-" + thisDate + " " + nowTime,
          thisStartYear = moment().year(moment().year()).startOf('year').format('YYYY-MM-DD HH:mm'),
          lastStartYear = moment().year(moment().year() - 1).startOf('year').format('YYYY-MM-DD HH:mm'),
          lastEndYear = moment().year(moment().year() - 1).endOf('year').format('YYYY-MM-DD HH:mm')
        if(!moment(lastEndMonth)._isValid){  //判断上月结束日期是否合法，否则赋值为上月最后一天的23：59
          lastEndMonth = moment().month(moment().month() - 1).endOf('month').format('YYYY-MM-DD HH:mm');
        }
        this.nowTime = nowTime
        this.nowDate = nowDate
        if(this.previewEnergyValue === "电"){
          api = "/api/energyelectric"
        }else if(this.previewEnergyValue === "水"){
          api = "/api/energywater"
        }else if(this.previewEnergyValue === "汽"){
          api = "/api/energysteam"
        }
        this.ChartsLoading = true
        this.axios.all([
          this.axios.get(api,{params: {StartTime: todayStartTime,EndTime:todayEndTime}}),//获取今天能耗
          this.axios.get(api,{params: {StartTime: compareDateStartTime,EndTime:compareDateEndTime}}),//获取对比天能耗
          this.axios.get(api,{params: {StartTime: thisStartMonth,EndTime:todayEndTime}}),//获取本月能耗
          this.axios.get(api,{params: {StartTime: lastStartMonth,EndTime:lastEndMonth}}),//获取上月能耗
          this.axios.get('/api/energyall',{
            params: {ModelFlag: "能耗预览",CompareDate:moment(this.CompareDate).format('YYYY-MM-DD'),EnergyClass:this.previewEnergyValue}
          })
        ]).then(this.axios.spread((todayCon,compareDateCon,thisMonthCon,lastMonthCon,compareData) =>{
          that.ChartsLoading = false
          that.todayCon = JSON.parse(todayCon.data).value
          that.unit = JSON.parse(todayCon.data).unit
          that.compareDateCon = JSON.parse(compareDateCon.data).value
          that.thisMonthCon = JSON.parse(thisMonthCon.data).value
          that.lastMonthCon = JSON.parse(lastMonthCon.data).value
          that.contrastMonthChartData.rows = JSON.parse(compareData.data).lastMonthRow
          that.realtimeChartData.rows = JSON.parse(compareData.data).compareTodayRow
        }))
        //获取当年能耗
        this.axios.get("/api/souyeselectyear",{params:{StartTime: thisStartYear,EndTime:todayEndTime,EnergyClass:this.previewEnergyValue}}).then(thisYearCon => {
          that.thisYearCon = thisYearCon.data.value
        })
        //获取上一年能耗
        this.axios.get("/api/souyeselectyear",{params:{StartTime: lastStartYear,EndTime:lastEndYear,EnergyClass:this.previewEnergyValue}}).then(lastYearCon => {
          that.lastYearCon = lastYearCon.data.value
        })
      },
      getAreaTimeEnergy(){
        this.areaTimeChartsLoading = true
        var params = {
          EnergyClass: this.areaTimeEnergyValue,
          CompareTime:moment().format("YYYY-MM-DD"),
        }
        this.axios.get("/api/areatimeenergycount",{params:params}).then(res => {
          this.areaTimeChartsLoading = false
          var arr = []
          res.data.rows.forEach((item,index) =>{
            if(index < 4){
              arr.push(item)
            }
          })
          this.areaChartData.rows = arr
          this.areaTimeChartExtend.label.formatter =  '{b}: {@score}' + res.data.unit
        })
      },
      getElectricLoadRateTime(){  //电能负荷率
        var that = this
        var dayStartTime = moment().format('YYYY-MM-DD') + " 00:00:00"
        var dayEndTime = moment().format('YYYY-MM-DD HH:mm:ss')
        var monthStartTime = moment().month(moment().month()).startOf('month').format('YYYY-MM-DD HH:mm:ss')
        var monthEndTime = moment().month(moment().month()).endOf('month').format('YYYY-MM-DD HH:mm:ss')
        var yearStartTime = moment().year(moment().year()).startOf('year').format('YYYY-MM-DD HH:mm:ss')
        var yearEndTime = moment().year(moment().year()).endOf('year').format('YYYY-MM-DD HH:mm:ss')
        var params = {}
        if(this.electricLoadRateTime === "日"){
          params.StartTime = dayStartTime
          params.EndTime = dayEndTime
          params.TimeClass = this.electricLoadRateTime
          params.CurrentTime = moment().format('YYYY-MM-DD HH:mm:ss')
          params.AreaName = ""
        }else if(this.electricLoadRateTime === "月"){
          params.StartTime = monthStartTime
          params.EndTime = monthEndTime
          params.TimeClass = this.electricLoadRateTime
          params.CurrentTime = moment().format('YYYY-MM-DD HH:mm:ss')
          params.AreaName = ""
        }else if(this.electricLoadRateTime === "年"){
          params.StartTime = yearStartTime
          params.EndTime = yearEndTime
          params.TimeClass = this.electricLoadRateTime
          params.CurrentTime = moment().format('YYYY-MM-DD HH:mm:ss')
          params.AreaName = ""
        }
        that.electricLoadRateChartData.rows[0].value = 0
        this.axios.get("/api/runefficiency",{params:params}).then(res => {
          that.electricLoadRateChartData.rows[0].value = res.data.loadRate
        })
      },
      getOnLineEq(){
        this.axios.get("/api/energyall",{params:{ModelFlag:"在线检测情况"}}).then(res => {
          this.onlineEquipmentOption = JSON.parse(res.data)
        })
        this.axios.get("/api/energyall",{params:{ModelFlag:"实时预警"}}).then(res => {
          var resData = JSON.parse(res.data)
          var arr = []
          resData.data.forEach((item,index) =>{
            if (index < 4 ) {
              arr.push(item);
            }
          })
          this.ralTimeWarningTableData = arr
        })
      },
      getArea(){
        let that = this
        var params = {
          tableName: "AreaTable",
          limit:1000,
          offset:0
        }
        this.axios.get("/api/CUID",{params:params}).then(res =>{
          var resData = JSON.parse(res.data).rows
          that.areaOptions = resData
        })
      },
      getBatchEnergy(){
        var that = this,
          nowTime = moment().format('HH:mm').substring(0,4) + "0",
          todayStartTime = moment().format('YYYY-MM-DD') + " 00:00",
          todayEndTime = moment().format('YYYY-MM-DD') + " " + nowTime,
          thisStartMonth = moment().month(moment().month()).startOf('month').format('YYYY-MM-DD HH:mm'),
          thisStartYear = moment().year(moment().year()).startOf('year').format('YYYY-MM-DD'),
          params = {}
        if(this.lotsEnergyValue === "本日"){
          params.AreaName = this.areaNameValue
          params.StartTime = todayStartTime
          params.EndTime = todayEndTime
        }else if(this.lotsEnergyValue === "本月"){
          params.AreaName = this.areaNameValue
          params.StartTime = thisStartMonth
          params.EndTime = todayEndTime
        }else if(this.lotsEnergyValue === "本年"){
          params.AreaName = this.areaNameValue
          params.StartTime = thisStartYear
          params.EndTime = todayEndTime
        }
        this.axios.get("/api/batchMaintainEnergy",{params:params}).then(res =>{
          that.lotsBatchCount = res.data.batchCount
          that.lotsEnergyTableData[0].Con = res.data.waterCon + res.data.waterUnit
          that.lotsEnergyTableData[0].EveryBatch = res.data.waterEveryBatch + res.data.waterUnit + "/批"
          that.lotsEnergyTableData[1].Con = res.data.steamCon + res.data.steamUnit
          that.lotsEnergyTableData[1].EveryBatch = res.data.steamEveryBatch + res.data.steamUnit + "/批"
        })
      },
      openSystemCheckupDialog(){ //打开系统体检
        this.systemCheckupDialogVisible = true

      },
      startSystemCheckup(){ //点击开始系统体检
        this.systemCheckupList = [
          {item: {
            name: "采集服务",
            successNumber: "",
            errorNumber: "",
            totalNumber: "",
            startTime: "",
            endTime: "",
            state: ""
          }},
          {item: {
            name: "写入历史数据库服务",
            successNumber: "",
            errorNumber: "",
            totalNumber: "",
            startTime: "",
            endTime: "",
            state: ""
          }},
          {item: {
            name: "写入增量服务",
            successNumber: "",
            errorNumber: "",
            totalNumber: "",
            startTime: "",
            endTime: "",
            state: ""
          }},
          {item: {
            name: "实时数据服务（websocket）",
            successNumber: "",
            errorNumber: "",
            totalNumber: "",
            startTime: "",
            endTime: "",
            state: ""
          }}
        ]
        this.axios.get("/api/systemcollecting").then(res => {
         this.systemCheckupList[0].item = res.data
        })
        this.axios.get("/api/systemredisdb").then(res => {
         this.systemCheckupList[1].item = res.data
        })
        this.axios.get("/api/systemdbincrment").then(res => {
         this.systemCheckupList[2].item = res.data
        })
        this.axios.get("/api/systemwebsocket").then(res => {
         this.systemCheckupList[3].item = res.data
        })
      }
    }
  }
</script>
<style>
  .home-card{
    width: 100%;
    margin-bottom:10px;
  }
  .home-card-head{
    background: #082F4C;
    color: #fff;
    font-size: 18px;
    height: 48px;
    line-height: 48px;
    padding: 0 10px;
    border-radius:4px;
    margin-bottom: 10px;
  }
  .card-head-select{
    float: right;
    width: 85px;
  }
  .home-card-body{
    background: #fff;
    border-radius:4px;
    padding:10px;
  }
  .card-body-ul li{
    margin-bottom: 10px;
  }
  .text-size-big{
    font-size: 24px;
  }
  .text-size-large{
    font-size: 20px;
  }
  .text-size-normol{
    font-size: 16px;
  }
  .text-size-small{
    font-size: 14px;
  }
  .text-size-mini{
    font-size: 12px;
  }
  .text-color-info{
    color: rgba(8,47,76,1);
  }
  .text-color-info-shallow{
    color: rgba(8,47,76,0.58);
  }
  .text-color-primary{
    color: #228AD5;
  }
  .text-color-warning{
    color: #FB8A06;
  }
  .text-color-success{
    color: #15CC48;
  }
  .text-color-danger{
    color: #FB3A06;
  }
  .colorBar li{
    display: inline-block;
    margin-right: 10px;
    margin-bottom: 5px;
  }
  .colorBar li i{
    display: inline-block;
    width: 14px;
    height: 14px;
    border-radius: 2px;
    margin-right: 5px;
    vertical-align: middle;
  }
  .colorBar li span{
    display: inline-block;
    color: #082F4C;
    font-size: 14px;
    vertical-align: middle;
  }
  .bg-dead{
    background-color: #ECF1F4;
  }
  .bg-low{
    background-color: #F5E866;
  }
  .bg-center{
    background-color: #FB8A06;
  }
  .bg-tall{
    background-color: #FB3A06;
  }
  .bg-fine{
    background-color: #228AD5;
  }
  .bg-best{
    background-color: #15CC48;
  }
  .el-table--mini td, .el-table--mini th{
    padding: 2px 0;
  }
  .systemCheckup{
    display: inline-block;
    padding: 6px 70px;
    background-color: #082F4C;
    border-radius: 4px;
    color: #fff;
    margin-top: 20px;
    text-decoration: none;
    cursor: pointer;
  }
</style>
