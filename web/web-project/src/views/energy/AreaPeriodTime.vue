<template>
    <el-row :gutter="10">
      <el-col :span="24">
        <el-form :inline="true" :model="formParameters">
          <el-form-item label="时间：">
            <el-date-picker type="date" v-model="formParameters.date" :picker-options="pickerOptions" size="mini" format="yyyy-MM-dd" style="width: 130px;" :clearable="false"></el-date-picker>
          </el-form-item>
          <el-form-item style="float: right;">
            <el-radio-group v-model="formParameters.energy" fill="#082F4C" size="small">
              <el-radio-button v-for="item in energyList" :key="item.id" :label="item.name"></el-radio-button>
            </el-radio-group>
          </el-form-item>
        </el-form>
      </el-col>
      <el-col :span="16">
        <div class="energyDataCard">
          <ve-line :data="chartData" :settings="chartSettings" :extend="ChartExtend"></ve-line>
        </div>
        <div class="energyDataCard">
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
      <el-col :span="8">
        <div class="energyDataCard">
          <div class="realTimeCardTitle">实时数据 <span>kwh</span></div>
          <div class="realTimeData">22432</div>
        </div>
        <div class="energyDataCard">
          <div class="energyDataItem">
            <div class="energyDataItemTitle">今日能耗</div>
            <div class="energyDataItemData">2342.23 kwh</div>
          </div>
          <div class="energyDataItem">
            <div class="energyDataItemTitle">对比日期</div>
            <el-date-picker type="date" v-model="contrastDate" :picker-options="pickerOptions" size="mini" format="yyyy-MM-dd" style="width: 130px;" :clearable="false"></el-date-picker>
          </div>
          <div class="energyDataItem">
            <div class="energyDataItemTitle">选择同期</div>
            <div class="energyDataItemData">2342.23 kwh</div>
          </div>
          <div class="energyDataItem">
            <div class="energyDataItemTitle">同期对比</div>
            <div class="energyDataItemData">+9.5% <i class="el-icon-top"></i></div>
          </div>
        </div>
        <div class="energyDataCard">
          <div class="realTimeCardTitle">能耗占比排名</div>

        </div>
      </el-col>
    </el-row>
</template>

<script>
    export default {
      name: "AreaPeriodTime",
      data(){
        this.chartSettings = {
          area:true
        }
        this.ChartExtend = {
          title:{
            text:"能耗趋势"
          },
          grid:{
            left:'10px',
            right:'10px',
            bottom:'20px',
            top:'50px'
          }
        }
        return {
          formParameters:{
            date:Date.now(),
            energy:"电能"
          },
          energyList:[
            {name:"电能",id:1},
            {name:"水能",id:2},
            {name:"汽能",id:3},
          ],
          pickerOptions:{
            disabledDate(time) {
              return time.getTime() > Date.now();
            }
          },
          chartData:{
            columns:["时间","能耗量"],
            rows:[
              {"时间":"00:00","能耗量":273},
              {"时间":"01:00","能耗量":563},
              {"时间":"02:00","能耗量":733},
              {"时间":"03:00","能耗量":223},
            ]
          },
          colorBarOption:[
            {name: "新建综合制剂楼", value0: 2342,value4: 4234,value8: 2232,value12: 235,value16: 2042,value20: 264, backgroundColor: '-webkit-linear-gradient(left,#ECF1F4,#F5E866,#FB8A06,#FB3A06,#F5E866,#FB8A06)'},
            {name: "提取二车间", value0: 2342,value4: 2342,value8: 2342,value12: 2342,value16: 2342,value20: 2342, backgroundColor: '-webkit-linear-gradient(left,#ECF1F4,#F5E866,#FB8A06,#FB3A06,#F5E866,#FB8A06)'},
            {name: "新建综合制剂楼", value0: 2342,value4: 2342,value8: 2342,value12: 2342,value16: 2342,value20: 2342, backgroundColor: '-webkit-linear-gradient(left,#ECF1F4,#F5E866,#FB8A06,#FB3A06,#F5E866,#FB8A06)'},
            {name: "新建综合制剂楼", value0: 2342,value4: 2342,value8: 2342,value12: 2342,value16: 2342,value20: 2342, backgroundColor: '-webkit-linear-gradient(left,#ECF1F4,#F5E866,#FB8A06,#FB3A06,#F5E866,#FB8A06)'}
          ],
          contrastDate:Date.now()
        }
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
  .realTimeCardTitle{
    font-size: 21px;
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
    display: inline-block;
    margin-bottom: 20px;
    font-size: 22px;
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
</style>
