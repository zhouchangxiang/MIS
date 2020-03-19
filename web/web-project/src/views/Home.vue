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
                    <span class="text-size-normol text-color-warning">{{ unit }}</span></li>
                  <li class="text-size-big text-color-warning">{{ todayCon }}</li>
                  <li><span class="text-size-mini text-color-info-shallow">对比</span>
                    <el-date-picker v-model="CompareDate" align="right" type="date" placeholder="选择日期" :picker-options="pickerOptions" @change="getEnergyPreview" :clearable="false" size="mini" style="width: 130px"></el-date-picker>
                  </li>
                  <li><span class="text-size-small text-color-primary">{{ compareDateCon }}</span>
                    <span class="text-size-mini" :class="todayCon-compareDateCon>0?'text-color-danger':'text-color-success'" style="margin-left: 20px;">{{ comparePer }}</span></li>
                </ul>
              </el-col>
              <el-col :span="9" style="white-space:nowrap;">
                <el-col :span="24">
                  <span class="text-size-large text-color-info">本月耗{{ previewEnergyValue }}量</span>
                  <span class="text-size-mini text-color-info-shallow">（截止{{ nowDate }}）</span>
                  <span class="text-size-normol text-color-warning">{{ unit }}</span>
                </el-col>
                <el-col :span="12">
                  <ul class="card-body-ul">
                    <li></li>
                    <li class="text-size-big text-color-warning">{{ thisMonthCon }}</li>
                    <li style="margin-top: 15px;">
                      <span class="text-size-mini text-color-info-shallow">上月同期</span>
                      <span class="text-size-mini text-color-info">{{ lastMonthCon }}</span>
                    </li>
                    <li>
                      <span class="text-size-mini text-color-info-shallow">上月同期</span>
                      <span class="text-size-mini" :class="thisMonthCon-lastMonthCon>0?'text-color-danger':'text-color-success'">{{ lastMonthCompare }}</span>
                    </li>
                  </ul>
                </el-col>
                <el-col :span="12">
                  <ve-line :data="contrastMonthChartData" :settings="contrastMonthChartSettings" :extend="contrastMonthChartExtend" width="120px" height="100px" :legend-visible="false"></ve-line>
                </el-col>
              </el-col>
              <el-col :span="8" style="white-space:nowrap;">
                <ul class="card-body-ul">
                  <li>
                    <span class="text-size-large text-color-info">年累计耗{{ previewEnergyValue }}量</span>
                    <span class="text-size-normol text-color-warning">{{ unit }}</span>
                  </li>
                  <li class="text-size-big text-color-warning">{{ thisYearCon }}</li>
                  <li style="margin-top: 15px;">
                    <span class="text-size-mini text-color-info-shallow">上年同期</span>
                    <span class="text-size-mini text-color-info">{{ lastYearCon }}</span>
                    <span style="margin-left: 20px;" class="text-size-mini" :class="thisYearCon-lastYearCon>0?'text-color-danger':'text-color-success'">{{ lastYearCompare }}</span>
                  </li>
                </ul>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="24">
                <span class="text-size-small text-color-info">今日对比能耗</span>
                <span class="text-size-small text-color-primary" style="float: right">查看报表<i class="el-icon-d-arrow-right el-icon--right"></i></span>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="24">
                  <ve-line :data="realtimeChartData" :extend="realtimeChartExtend" height="260px" :legend-visible="false"></ve-line>
              </el-col>
            </el-row>
          </div>
        </div>
        <el-row :gutter="15">
          <el-col :span="10">
            <div class="home-card-head">
              <span><i class="el-icon-guide el-icon--left" style="color: #228AD5;"></i>区域时段能耗</span>
              <el-select class="card-head-select" v-model="areaTimeEnergyValue" placeholder="请选择">
                <el-option v-for="(item,index) in areaTimeEnergyOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
              </el-select>
            </div>
            <div class="home-card-body" style="height:280px;">
              <ul class="colorBar">
                <li><i class="bg-dead"></i><span>停</span></li>
                <li><i class="bg-low"></i><span>低</span></li>
                <li><i class="bg-center"></i><span>中</span></li>
                <li><i class="bg-tall"></i><span>高</span></li>
              </ul>
              <ul class="gradientList">
                <li v-for="item in colorBarOption">
                  <p class="text-size-small text-color-info">{{ item.name }}</p>
                  <el-popover trigger="hover">
                    <div>0-4点：{{ item.value0 }}</div>
                    <div>4-8点：{{ item.value4 }}</div>
                    <div>8-12点：{{ item.value8 }}</div>
                    <div>12-16点：{{ item.value12 }}</div>
                    <div>16-20点：{{ item.value16 }}</div>
                    <div>20-24点：{{ item.value20 }}</div>
                    <div slot="reference" class="gradientColorItem" :style='{background:item.backgroundColor}'></div>
                  </el-popover>
                </li>
              </ul>
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
              <el-select class="" v-model="electricLoadRateTime" size="small" style="width: 80px;">
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
                <li v-for="item in onlineEquipmentOption" style="margin-bottom: 5px;">
                  <p class="text-size-normol text-color-info">{{ item.name }}</p>
                  <p class="text-size-mini text-color-info-shallow" style="margin-top: 5px;"><span>上线数/总数</span><span style="float: right;">{{ item.online }}/{{ item.total }}</span></p>
                  <el-progress :text-inside="true" :stroke-width="16" :percentage="item.rate"></el-progress>
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
            <el-table :data="ralTimeWarningTableData" size="mini" height="232px" max-height="232px" style="width: 100%">
              <el-table-column prop="area" label="区域"></el-table-column>
              <el-table-column prop="name" label="设备"></el-table-column>
              <el-table-column prop="type" label="状态">
                <template slot-scope="scope">
                  <span class="text-size-mini text-color-warning">{{ scope.row.type }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="date" label="时间"></el-table-column>
            </el-table>
            <span class="text-size-mini text-color-primary" style="float: right;margin-top: 15px;">更多记录<i class="el-icon-d-arrow-right el-icon--right"></i></span>
          </div>
        </div>
        <div class="home-card">
          <div class="home-card-head">
            <span><i class="el-icon-bell el-icon--left" style="color: #228AD5;"></i>单位批次能耗</span>
          </div>
          <div class="home-card-body" style="height: 300px;">
            <p>
              <span style="font-size: 48px;" class="text-color-primary">54<span class="text-size-mini">批</span></span>
              <el-select class="" v-model="lotsEnergyValue" size="small" style="width: 80px;float: right;">
                <el-option v-for="item in lotsEnergyOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
              </el-select>
            </p>
            <el-table :data="lotsEnergyTableData" size="small" height="160px" max-height="160px" style="width: 100%">
              <el-table-column prop="type" label="类型"></el-table-column>
              <el-table-column prop="total" label="总量">
                <template slot-scope="scope">
                  <span class="text-size-mini text-color-info-shallow">{{ scope.row.total }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="unitNum" label="单位耗量">
                <template slot-scope="scope">
                  <span class="text-size-mini text-color-primary">{{ scope.row.unitNum }}</span>
                </template>
              </el-table-column>
            </el-table>
            <span class="text-size-mini text-color-primary" style="float: right;margin-top: 15px;">查看详情<i class="el-icon-d-arrow-right el-icon--right"></i></span>
          </div>
        </div>
        <div class="home-card-body" style="height: 130px;text-align: center;">
          <p class="text-size-big text-color-primary">系统体检</p>
          <a href="javascript:;" class="systemCheckup" @click="openSystemCheckupDialog">立即体检</a>
          <el-dialog
            title="系统体检"
            :close-on-press-escape="false"
            :close-on-click-modal="false"
            :show-close="false"
            :visible.sync="systemCheckupDialogVisible"
            width="30%"
            center>
            <el-timeline>
              <el-timeline-item
                v-for="(activity, index) in timelineData"
                :key="index"
                :icon="activity.icon"
                size="large"
                :type="activity.type">
                <p>{{activity.content}}</p>
                <p>{{activity.result}}</p>
              </el-timeline-item>
            </el-timeline>
            <span slot="footer" class="dialog-footer">
              <el-button @click="systemCheckupDialogVisible = false">取 消</el-button>
              <el-button type="primary" @click="startSystemCheckup">开 始 体 检</el-button>
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
          columns: ['时间', '上月能耗', '本月能耗'],
          rows:[]
        },
        realtimeChartData:{
          columns: ['时间', '今日能耗', '对比日能耗'],
          rows:[]
        },
        thisYearCon: "", //年能耗量
        lastYearCon: "", //上年同期能耗
        contrastMonthChartSettings: { //本月对比上月能耗图表配置
          area: true,
        },
        contrastMonthChartExtend: {
          yAxis:{
            show:false
          },
          xAxis:{
            show:false
          },
          grid:{
            left: '-40px',
            right: '0',
            bottom: '-20px',
            top:'0'
          },
          series: {
            smooth: false
          }
        },
        realtimeChartExtend: { //今日对比能耗图表配置
          grid:{
            left: '-40px',
            right: '0',
            bottom: '0',
            top:'20px'
          },
          series: {
            smooth: false
          }
        },
        colorBarOption:[
          {name: "新建综合制剂楼", value0: 2342,value4: 4234,value8: 2232,value12: 235,value16: 2042,value20: 264, backgroundColor: '-webkit-linear-gradient(left,#ECF1F4,#F5E866,#FB8A06,#FB3A06,#F5E866,#FB8A06)'},
          {name: "提取二车间", value0: 2342,value4: 2342,value8: 2342,value12: 2342,value16: 2342,value20: 2342, backgroundColor: '-webkit-linear-gradient(left,#ECF1F4,#F5E866,#FB8A06,#FB3A06,#F5E866,#FB8A06)'},
          {name: "新建综合制剂楼", value0: 2342,value4: 2342,value8: 2342,value12: 2342,value16: 2342,value20: 2342, backgroundColor: '-webkit-linear-gradient(left,#ECF1F4,#F5E866,#FB8A06,#FB3A06,#F5E866,#FB8A06)'},
          {name: "新建综合制剂楼", value0: 2342,value4: 2342,value8: 2342,value12: 2342,value16: 2342,value20: 2342, backgroundColor: '-webkit-linear-gradient(left,#ECF1F4,#F5E866,#FB8A06,#FB3A06,#F5E866,#FB8A06)'}
        ],
        electricLoadRateChartData:{
          columns: ['type', 'value'],
          rows: [
            { type: '占比', value: 45 }
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
          value: '选项1',
          label: '本日'
        }, {
          value: '选项2',
          label: '本月'
        }, {
          value: '选项3',
          label: '本年'
        }],
        electricLoadRateTime:'本日', //默认下拉
        onlineEquipmentOption:[ //在线情况采集
          {name:"交换机",online:11,total:12,rate:80},
          {name:"电表",online:6,total:12,rate:70},
          {name:"水表",online:8,total:12,rate:40},
          {name:"汽表",online:15,total:15,rate:100},
        ],
        ralTimeWarningTableData:[ //实时预警表格数据
          {area:"新建综合制剂楼",name:"汽表2",type:"温度不正常",date:"2020-01-02 12:05"},
          {area:"新建综合制剂楼",name:"汽表4",type:"温度不正常",date:"2020-01-02 12:05"},
          {area:"新建综合制剂楼",name:"电表1",type:"三项电流不平衡",date:"2020-01-02 12:05"},
          {area:"新建综合制剂楼",name:"汽表2",type:"温度不正常",date:"2020-01-02 12:05"}
        ],
        lotsEnergyValue:"本日",
        lotsEnergyOptions:[{ //电能负荷率下拉框
          value: '选项1',
          label: '本日'
        }, {
          value: '选项2',
          label: '本月'
        }, {
          value: '选项3',
          label: '本年'
        }],
        lotsEnergyTableData:[
          {type:"电能",total:"16456.24kwh",unitNum:"1246.15kwh/批"},
          {type:"水能",total:"16456.24kwh",unitNum:"1246.15kwh/批"},
          {type:"汽能",total:"16456.24kwh",unitNum:"1246.15kwh/批"}
        ],
        systemCheckupDialogVisible:false, //是否展开系统体检对话框
        timelineData:[],
      }
    },
    created(){
      this.getEnergyPreview()
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
          return 0 + "%"
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
          return 0 + "%"
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
          return 0 + "%"
        }
      }
    },
    methods: {
      getEnergyPreview() {  //获取能耗预览内的数据
        var api = ""
        var that = this
        if(this.previewEnergyValue == "电"){
          api = "/api/energyelectric"
        }else if(this.previewEnergyValue == "水"){
          api = "/api/energywater"
        }else if(this.previewEnergyValue == "汽"){
          api = "/api/energysteam"
        }
        var nowTime = moment().format('HH:mm').substring(0,4) + "0"
        var nowDate = moment().format('MM-DD') + " " + nowTime
        var thisDate = moment().format('DD')
        var thisMonth = moment().format('MM-DD')
        var todayStartTime = moment().format('YYYY-MM-DD') + " 00:00"
        var todayEndTime = moment().format('YYYY-MM-DD') + " " + nowTime
        var compareDateStartTime = moment(this.CompareDate).format('YYYY-MM-DD') + " 00:00"
        var compareDateEndTime = moment(this.CompareDate).format('YYYY-MM-DD') + " " + nowTime
        var thisStartMonth = moment().month(moment().month()).startOf('month').format('YYYY-MM-DD HH:mm')
        var lastStartMonth = moment().month(moment().month() - 1).startOf('month').format('YYYY-MM-DD HH:mm')
        var lastEndMonth = moment().month(moment().month() - 1).endOf('month').format('YYYY-MM-DD').substring(0,7) + "-" + thisDate + " " + nowTime
        var thisStartYear = moment().year(moment().year()).startOf('year').format('YYYY-MM-DD')
        var lastStartYear = moment().year(moment().year() - 1).startOf('year').format('YYYY-MM-DD HH:mm')
        var lastEndYear = moment().year(moment().year() - 1).endOf('year').format('YYYY-MM-DD').substring(0,4) + "-" + thisMonth + " " + nowTime
        this.nowTime = nowTime
        this.nowDate = nowDate
        this.axios.all([
          this.axios.get(api,{params: {StartTime: todayStartTime,EndTime:todayEndTime}}),//获取今天能耗
          this.axios.get(api,{params: {StartTime: compareDateStartTime,EndTime:compareDateEndTime}}),//获取对比天能耗
          this.axios.get(api,{params: {StartTime: thisStartMonth,EndTime:todayEndTime}}),//获取本月能耗
          this.axios.get(api,{params: {StartTime: lastStartMonth,EndTime:lastEndMonth}}),//获取上月能耗
          this.axios.get(api,{params: {StartTime: thisStartYear,EndTime:todayEndTime}}),//获取当年能耗
          this.axios.get(api,{params: {StartTime: lastStartYear,EndTime:lastEndYear}}),//获取上一年能耗
          // this.axios.get('/api/energyall',{
          //   params: {ModelFlag: "能耗预览",CompareDate:moment(this.CompareDate).format('YYYY-MM-DD'),EnergyClass:this.previewEnergyValue}
          // })//获取对比图表
        ]).then(this.axios.spread(function(todayCon,compareDateCon,thisMonthCon,lastMonthCon,thisYearCon,lastYearCon,compareData){
          that.todayCon = JSON.parse(todayCon.data).elctric
          that.unit = JSON.parse(todayCon.data).unit
          that.compareDateCon = JSON.parse(compareDateCon.data).elctric
          that.thisMonthCon = JSON.parse(thisMonthCon.data).elctric
          that.lastMonthCon = JSON.parse(lastMonthCon.data).elctric
          that.thisYearCon = JSON.parse(thisYearCon.data).elctric
          that.lastYearCon = JSON.parse(lastYearCon.data).elctric
          // console.log(JSON.parse(compareData.data))
        }))
      },
      openSystemCheckupDialog(){ //打开系统体检
        this.systemCheckupDialogVisible = true
        this.timelineData = [
          {content:"检查服务端是否正常"},
          {content:"采集设备是否正常"},
          {content:"网络是否正常"},
        ]
      },
      startSystemCheckup(){ //点击开始系统体检
        this.$set(this.timelineData[0],'icon',"el-icon-check")
        this.$set(this.timelineData[0],'type',"success")
        this.$set(this.timelineData[1],'icon',"el-icon-loading")
        this.$set(this.timelineData[1],'type',"primary")
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
  .card-head-select .el-input__inner{
    background-color: #082F4C;
    border:none;
    color:#fff;
  }
  .card-head-select .el-select__caret{
    line-height: 48px;
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
  .gradientList li{
    margin-top: 10px;
  }
  .gradientColorItem{
    width: 100%;
    height: 16px;
    margin-top: 10px;
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
