<template>
  <el-row :gutter="2">
    <el-col :span="24">
      <el-form :model="formParameters">
        <el-form-item label="时间：" style="margin-bottom: 0;">
          <el-radio-group v-model="formParameters.resourceTime" fill="#082F4C" size="mini">
            <el-radio-button v-for="item in radioTimeList" border :key="item.id" :label="item.name"></el-radio-button>
          </el-radio-group>
          <el-date-picker type="date" v-model="formParameters.date" :picker-options="pickerOptions" size="mini" format="yyyy-MM-dd" style="width: 150px;" :clearable="false"></el-date-picker>
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
    <el-col :span="24" style="margin-bottom:2px;">
      <div class="chartHead text-size-large text-color-info">
        <div class="chartTile">趋势图</div>
        <ul class="subsectionList">
          <li v-for="item in subsectionList"><a href="javascript:;" :class="{active:subsectionActive == item.id}" @click="getSubsection(item.id)">{{ item.name }}</a></li>
        </ul>
        <div class="sortHandle">
          <a href="javascript:;">正向</a> | <a href="javascript:;">反向</a>
        </div>
      </div>
    </el-col>
    <el-col :span="24">
      <div class="energyDataContainer">
        <ve-line :data="chartData" :extend="ChartExtend"></ve-line>
      </div>
    </el-col>
  </el-row>
</template>

<script>
    export default {
      name: "AreaBasicData",
      data(){
        this.ChartExtend = {
          grid:{
            left:'0',
            right:'0',
            bottom:'0',
            top:'40px'
          }
        }
        return {
          formParameters:{
            resourceTime:"实时",
            resourceType:"有功电量",
            date:Date.now(),
            energy:"电能"
          },
          radioTimeList:[
            {name:"实时",id:1},
            {name:"日",id:2},
            {name:"周",id:3},
            {name:"月",id:4},
            {name:"季",id:5},
            {name:"年",id:6},
            {name:"班次",id:7},
            {name:"节日",id:8}
          ],
          radioTypeList:[
            {name:"有功电量",id:1},
            {name:"无功电量",id:2},
            {name:"有功功率",id:3},
            {name:"无功功率",id:4},
            {name:"最大需量",id:5},
            {name:"电流",id:6},
            {name:"电压",id:7}
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
          subsectionList:[
            {name:"小时",id:1},
            {name:"30分钟",id:2},
            {name:"15分钟",id:3},
            {name:"5分钟",id:4},
            {name:"1分钟",id:5}
          ],
          subsectionActive:1,
          chartData: {
            columns: ['时间', '总有功电量', 'A相有功电量', 'B相有功电量','C相有功电量'],
            rows: [
              { '时间': '00:00', '总有功电量': 4647, 'A相有功电量': 193, 'B相有功电量': 454 ,'C相有功电量':124},
              { '时间': '01:00', '总有功电量': 8457, 'A相有功电量': 320, 'B相有功电量': 546 ,'C相有功电量':544},
              { '时间': '02:00', '总有功电量': 4875, 'A相有功电量': 223, 'B相有功电量': 454 ,'C相有功电量':254},
              { '时间': '03:00', '总有功电量': 9755, 'A相有功电量': 143, 'B相有功电量': 247 ,'C相有功电量':274},
              { '时间': '04:00', '总有功电量': 7545, 'A相有功电量': 342, 'B相有功电量': 844 ,'C相有功电量':457},
              { '时间': '05:00', '总有功电量': 6488, 'A相有功电量': 423, 'B相有功电量': 648 ,'C相有功电量':948}
            ]
          }
        }
      },
      methods:{
        getSubsection(index){
          this.subsectionActive = index;
          console.log(index)
        }
      }
    }
</script>

<style scoped>
  .subsectionList{
    float: left;
    height: 46px;
    margin-left: 20px;
  }
  .subsectionList li {
    float: left;
  }
  .subsectionList li a{
    display: block;
    text-decoration: none;
    color: #9B9B9B;
    padding: 0 15px;
    font-size: 14px;
    border-bottom: 2px solid #EEEEEE;
  }
  .subsectionList li a.active{
    color: #228AD5;
    border-bottom: 2px solid #228AD5;
  }
  .sortHandle{
    float: right;
    display: flex;
    color: #9B9B9B;
    font-size: 14px;
  }
  .sortHandle a{
    display: block;
    font-size: 14px;
    color: #9B9B9B;
    text-decoration: none;
    height: 46px;
    line-height: 46px;
    padding: 0 5px;
  }
</style>
