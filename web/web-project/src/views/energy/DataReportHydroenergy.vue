<template>
  <el-row :gutter="20">
    <el-col :span="24">
      <el-form :model="formParameters">
        <el-form-item label="时间：">
          <el-radio-group v-model="formParameters.resourceTime" fill="#082F4C" size="mini">
            <el-radio-button v-for="item in radioTimeList" border :key="item.id" :label="item.name"></el-radio-button>
          </el-radio-group>
          <el-date-picker type="date" v-model="formParameters.startDate" :picker-options="pickerOptions" size="mini" style="width: 180px;" :clearable="false"></el-date-picker> ~
          <el-date-picker type="date" v-model="formParameters.endDate" :picker-options="pickerOptions" size="mini" style="width: 180px;" :clearable="false"></el-date-picker>
        </el-form-item>
      </el-form>
    </el-col>
    <el-col :span="24">
      <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
        <div class="chartTile">水能报表</div>
        <el-select v-model="areaValue" size="mini">
          <el-option v-for="item in areaOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
        <el-button type="primary" size="mini" style="float: right;margin: 9px 0;">导出</el-button>
      </div>
      <div class="platformContainer">

      </div>
    </el-col>
  </el-row>
</template>

<script>
  export default {
    name: "DataReportSteam",
    data(){
      return {
        formParameters:{
          resourceTime:"班次",
          startDate:Date.now(),
          endDate:Date.now()
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
        areaValue:"桓仁厂区",
        areaOptions:[
          {value: 0,label: '桓仁厂区'},
          {value: 1,label: '新建综合试剂楼'},
          {value: 2,label: '提取二车间'},
          {value: 3,label: '前处理车间'},
          {value: 4,label: '研发中心'},
          {value: 5,label: '生物科技楼'},
          {value: 6,label: '原提取车间'},
          {value: 7,label: '锅炉房'},
          {value: 8,label: '综合办公楼'},
          {value: 9,label: '综合车间'},
          {value: 10,label: '污水站'},
          {value: 11,label: '固体制剂车间'},
          {value: 12,label: '展览馆'},
        ]
      }
    }
  }
</script>

<style scoped>

</style>
