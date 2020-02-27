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
  </el-row>
</template>

<script>
  export default {
    name: "CostCenter",
    data(){
      return {
        formParameters:{
          resourceTime:"月",
          resourceType:"基本电费",
          startDate:Date.now(),
          endDate:Date.now(),
          energy:"电能"
        },
        radioTimeList:[
          {name:"月",id:4},
          {name:"年",id:6}
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
      }
    }
  }
</script>

<style scoped>

</style>
