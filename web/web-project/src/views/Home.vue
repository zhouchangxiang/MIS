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
                  <li><span class="text-size-large text-color-info">本日耗电量</span><span class="text-size-mini text-color-info-shallow">（截止12：00）</span></li>
                  <li class="text-size-big text-color-warning">1256.25kwh</li>
                  <li><span class="text-size-mini text-color-info-shallow">对比</span>
                    <el-date-picker v-model="CompareDate" align="right" type="date" placeholder="选择日期" :picker-options="pickerOptions" @change="getEnergyPreview" :clearable="false" size="mini" style="width: 130px"></el-date-picker>
                  </li>
                  <li><span class="text-size-small text-color-primary">1256.25kwh</span><span class="text-size-mini text-color-danger" style="margin-left: 20px;">+9.5%<i class="el-icon-top"></i></span></li>
                </ul>
              </el-col>
              <el-col :span="9" style="white-space:nowrap;">
                <ul class="card-body-ul" style="display: inline-block;">
                  <li><span class="text-size-large text-color-info">本月耗电量</span></li>
                  <li class="text-size-big text-color-warning">1256.25kwh</li>
                  <li style="margin-top: 15px;">
                    <span class="text-size-mini text-color-info-shallow">上月同期</span>
                    <span class="text-size-mini text-color-info">4543.56 kwh</span>
                  </li>
                  <li>
                    <span class="text-size-mini text-color-info-shallow">上月同期</span>
                    <span class="text-size-mini text-color-success">+9.5%<i class="el-icon-bottom"></i></span>
                  </li>
                </ul>
                <ve-line :data="contrastMonthChartData" :settings="contrastMonthChartSettings" :extend="contrastMonthChartExtend" width="120px" height="100px" :legend-visible="false" style="display: inline-block;"></ve-line>
              </el-col>
              <el-col :span="8" style="white-space:nowrap;">
                <ul class="card-body-ul">
                  <li>
                    <span class="text-size-large text-color-info">年累计耗电量</span>
                    <span class="text-size-mini text-color-warning">kwh</span>
                  </li>
                  <li class="text-size-big text-color-warning">1256.25kwh</li>
                  <li style="margin-top: 15px;">
                    <span class="text-size-mini text-color-info-shallow">上年同期</span>
                    <span class="text-size-mini text-color-info">4543.56 kwh</span>
                    <span style="margin-left: 20px;" class="text-size-mini text-color-danger">+9.5%<i class="el-icon-top"></i></span>
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
                  <ve-line :data="realtimeChartData" :settings="realtimeChartSettings" :extend="realtimeChartExtend" height="260px" :legend-visible="false"></ve-line>
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
                  <p>{{ item.name }}</p>
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
              <ve-gauge :data="electricLoadRateChartData" :settings="electricLoadRateChartSettings" :extend="electricLoadRateChartExtend" height="220px"></ve-gauge>
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
      this.contrastMonthChartSettings = { //本月对比上月能耗图表配置
        area: true,
      }
      this.contrastMonthChartExtend = {
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
      }
      this.realtimeChartSettings = { //今日对比能耗图表配置

      }
      this.realtimeChartExtend = {
        grid:{
          left: '-40px',
          right: '0',
          bottom: '0',
          top:'20px'
        },
        series: {
          smooth: false
        }
      }
      this.electricLoadRateChartSettings = { //电能负荷率图表配置
        dataType: {
          '占比': 'percent'
        },
        seriesMap: {
          '占比': {
            min: 0,
            max: 1
          }
        }
      }
      this.electricLoadRateChartExtend = {
        grid:{
          left: '0',
          right: '0',
          bottom: '-40px',
          top:'0'
        },
        series: {
          smooth: false
        }
      }
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
        CompareDate:Date.now() - 3600 * 1000 * 24, //默认对比日期
        contrastMonthChartData:{
          columns: ['日期', '上月能耗', '本月能耗'],
          rows: [
            { '日期': '1日', '上月能耗': 1393, '本月能耗': 1093},
            { '日期': '2日', '上月能耗': 3530, '本月能耗': 3230},
            { '日期': '3日', '上月能耗': 2923, '本月能耗': 2623},
            { '日期': '4日', '上月能耗': 1723, '本月能耗': 1423},
            { '日期': '5日', '上月能耗': 3792, '本月能耗': 3492},
            { '日期': '6日', '上月能耗': 4593, '本月能耗': 4293},
            { '日期': '7日', '上月能耗': 4593, '本月能耗': 4293},
            { '日期': '8日', '上月能耗': 4783, '本月能耗': 4453},
          ]
        },
        realtimeChartData:{
          columns: ['日期', '上月能耗', '本月能耗'],
          rows: [
            { '日期': '1日', '上月能耗': 1393, '本月能耗': 1093},
            { '日期': '2日', '上月能耗': 3530, '本月能耗': 3230},
            { '日期': '3日', '上月能耗': 2923, '本月能耗': 2623},
            { '日期': '4日', '上月能耗': 1723, '本月能耗': 1423},
            { '日期': '5日', '上月能耗': 3792, '本月能耗': 3492},
            { '日期': '6日', '上月能耗': 4593, '本月能耗': 4293},
            { '日期': '7日', '上月能耗': 4593, '本月能耗': 4293},
            { '日期': '8日', '上月能耗': 4783, '本月能耗': 4453},
          ]
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
            { type: '占比', value: 0.8 }
          ]
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
      this.getAreaTime()
    },
    mounted(){

    },
    methods: {
      getEnergyPreview() {
        this.axios.get('/api/energyPreview',{
          params: {
              energyType: this.previewEnergyValue,
              compareDate: moment(this.CompareDate).format('YYYY-MM-DD')
          }
        }).then(function (response) {
            console.log(response);
        }).catch(function (error) {
            console.log(error);
        });
      },
      getAreaTime() {
        this.axios.get('/api/areaTimeEnergy',{
          params: {
              energyType: this.areaTimeEnergyValue,
          }
        }).then(function (response) {
            console.log(response);
        }).catch(function (error) {
            console.log(error);
        });
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
