<template>
  <el-row :gutter="2">
    <el-col :span="24">
      <el-form :inline="true" :model="formParameters">
        <el-form-item label="时间：">
          <el-radio-group v-model="formParameters.resource" fill="#082F4C" size="mini">
            <el-radio-button v-for="item in radioList" border :key="item.id" :label="item.name"></el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-date-picker type="month" placeholder="选择月份" v-model="formParameters.dateMonth" :picker-options="pickerOptions" size="mini" format="yyyy-MM" style="width: 130px;" :clearable="false"></el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-checkbox v-model="formParameters.checked">对比 </el-checkbox>
          <el-date-picker type="month" placeholder="选择月份" v-model="formParameters.contrastingMonth" :picker-options="pickerOptions" size="mini" format="yyyy-MM" style="width: 130px;" :clearable="false"></el-date-picker>
          <span style="vertical-align: sub;" class="text-color-danger text-size-mini">(选择对比月份起始计算日)</span>
        </el-form-item>
        <el-form-item style="float: right;">
          <el-radio-group v-model="formParameters.energy" fill="#082F4C" size="small">
            <el-radio-button v-for="item in energyList" :key="item.id" :label="item.name"></el-radio-button>
          </el-radio-group>
        </el-form-item>
      </el-form>
    </el-col>
    <el-col :span="24" style="margin-bottom:2px;">
      <div class="chartTile text-size-large text-color-info">趋势图</div>
    </el-col>
    <el-col :span="4">
      <div class="energyDataContainer" style="border-radius: 0 0 0 4px;">
        <ul class="energyDataItem">
          <li class="text-size-normol text-color-info">本月耗电量</li>
          <li class="text-size-large text-color-info">1256.24kwh</li>
          <li class="text-size-mini"><span class="text-color-info-shallow" style="margin-right: 10px;">选择对比</span><span class="text-size-mini text-color-danger">+9.5% <i class="el-icon-top"></i></span></li>
        </ul>
        <ul class="energyDataItem">
          <li class="text-size-normol text-color-info">本月生产批次</li>
          <li class="text-size-large text-color-info">5批</li>
          <li class="text-size-mini"><span class="text-color-info-shallow" style="margin-right: 10px;">选择对比</span><span class="text-size-mini text-color-success">+9.5% <i class="el-icon-top"></i></span></li>
        </ul>
        <ul class="energyDataItem">
          <li class="text-size-normol text-color-info">单位批次能耗</li>
          <li class="text-size-large text-color-info">155.5kwh/批</li>
          <li class="text-size-mini"><span class="text-color-info-shallow" style="margin-right: 10px;">同期对比</span><span class="text-size-mini text-color-success">+9.5% <i class="el-icon-top"></i></span></li>
        </ul>
      </div>
    </el-col>
    <el-col :span="20">
      <div class="energyDataContainer" style="border-radius: 0 0 4px 0;">
        <ve-line :data="chartData" :settings="ChartSettings" :extend="ChartExtend"></ve-line>
      </div>
    </el-col>
    <el-col :span="24" style="margin-top:10px;margin-bottom:2px;">
      <div class="chartTile">
        <span class="text-size-large text-color-info">数据表</span>
        <span class="text-size-mini text-color-danger">（倒序对比）</span>
        <el-select class="collapse-head-select" v-model="commodityValue" placeholder="请选择" @change="getCommodityPreview" size="small">
          <el-option v-for="item in commodityOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
        <el-button type="primary" style="float:right;background-color: #082F4C;border:none;" size="small">导出</el-button>
      </div>
    </el-col>
    <el-col :span="12" style="border-radius:0 0 4px 4px;padding: 10px;background: #fff;">
      <el-table :data="thisDateTableData" size="small" style="width: 100%">
        <el-table-column prop="date" label="时间"></el-table-column>
        <el-table-column prop="commodity" label="品名"></el-table-column>
        <el-table-column prop="batch" label="生产批次号"></el-table-column>
        <el-table-column prop="area" label="区域"></el-table-column>
        <el-table-column prop="energyVal" label="耗电量"></el-table-column>
        <el-table-column prop="totalEnergy" label="总耗电量"></el-table-column>
        <el-table-column prop="unitEnergy" label="单位耗电"></el-table-column>
      </el-table>
    </el-col>
    <el-col :span="12" style="border-radius:0 0 4px 4px;padding: 10px;background: #fff;">
      <el-table :data="thisDateTableData" size="small" style="width: 100%">
        <el-table-column prop="date" label="时间"></el-table-column>
        <el-table-column prop="commodity" label="品名"></el-table-column>
        <el-table-column prop="batch" label="生产批次号"></el-table-column>
        <el-table-column prop="area" label="区域"></el-table-column>
        <el-table-column prop="energyVal" label="耗电量"></el-table-column>
        <el-table-column prop="totalEnergy" label="总耗电量"></el-table-column>
        <el-table-column prop="unitEnergy" label="单位耗电"></el-table-column>
      </el-table>
    </el-col>
  </el-row>
</template>

<script>
    export default {
      name: "AreaShows",
      data(){
        this.ChartSettings = {//趋势图表配置

        }
        this.ChartExtend = {
          grid:{
            left:'0',
            right:'0',
            bottom:'20px',
            top:'40px'
          },
          'series.1.itemStyle.normal.lineStyle': {
            width:2,
            type:'dotted'
          }
        }
        return {
          radioList:[
            {name:"月",id:1},
            {name:"季",id:2},
            {name:"年",id:3},
          ],
          energyList:[
            {name:"电能",id:1},
            {name:"水能",id:2},
            {name:"汽能",id:3},
          ],
          formParameters:{
            resource:"月",
            dateMonth:Date.now(),
            contrastingMonth:Date.now(),
            checked:"",
            energy:"电能"
          },
          pickerOptions:{
            disabledDate(time) {
              return time.getTime() > Date.now();
            }
          },
          chartData: {
            columns: ['日期', '当前月份能耗', '选择同期能耗'],
            rows: [
              { '日期': '1-1', '当前月份能耗': 1393, '选择同期能耗': 1093},
              { '日期': '1-2', '当前月份能耗': 3530, '选择同期能耗': 3230},
              { '日期': '1-3', '当前月份能耗': 2923, '选择同期能耗': 2623},
              { '日期': '1-4', '当前月份能耗': 1723, '选择同期能耗': 1423},
              { '日期': '1-5', '当前月份能耗': 3792, '选择同期能耗': 3492},
              { '日期': '1-6', '当前月份能耗': 4593, '选择同期能耗': 4293}
            ]
          },
          commodityValue:"选项1",
          commodityOptions:[{
            value: '选项1',
            label: '药品1'
          }, {
            value: '选项2',
            label: '药品2'
          }, {
            value: '选项3',
            label: '药品3'
          }],
          thisDateTableData:[ //实时预警表格数据
            {date:"2020-01-02 12:05",commodity:"药品1",batch:"546465456",area:"新建综合制剂楼",energyVal:"4164",totalEnergy:"16424",unitEnergy:"1645"},
            {date:"2020-01-02 12:05",commodity:"药品1",batch:"546465456",area:"新建综合制剂楼",energyVal:"4164",totalEnergy:"16424",unitEnergy:"1645"},
            {date:"2020-01-02 12:05",commodity:"药品1",batch:"546465456",area:"新建综合制剂楼",energyVal:"4164",totalEnergy:"16424",unitEnergy:"1645"},
            {date:"2020-01-02 12:05",commodity:"药品1",batch:"546465456",area:"新建综合制剂楼",energyVal:"4164",totalEnergy:"16424",unitEnergy:"1645"},
            {date:"2020-01-02 12:05",commodity:"药品1",batch:"546465456",area:"新建综合制剂楼",energyVal:"4164",totalEnergy:"16424",unitEnergy:"1645"}
          ]
        }
      },
      created(){
        console.log(this.$route.query.areaName)
      },
      methods: {
        getCommodityPreview() {

        }
      }
    }
</script>

<style>
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
  .chartTile{
    background: #fff;
    padding: 10px 15px;
    border-radius: 4px 4px 0 0;
  }
  .energyDataContainer{
    background: #fff;
    height: 420px;
    padding: 20px 15px;
  }
  .energyDataItem{
    margin-bottom: 45px;
  }
  .energyDataItem:last-child{
    margin-bottom:0;
  }
  .energyDataItem li{
    margin-bottom: 5px;
  }
  .collapse-head-select{
    width: 100px;
  }
  .collapse-head-select .el-input__inner{
    background-color: #fff;
    border:none;
    color:#082F4C;
  }
</style>
