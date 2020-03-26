<template>
  <el-row>
    <el-col :span="24">
      <div class="navOptionsItem">
        <ul>
          <li v-for="(item,index) in navOptions" @click="showPage(index)"><a href="javascript:;" :class="{ active:index==navOptionsCurrent }" v-html="item.name"></a></li>
        </ul>
      </div>
      <TradeNameTable v-if="navOptionsCurrent == 0"></TradeNameTable>
      <PlanTask v-if="navOptionsCurrent == 1"></PlanTask>
      <Altitude v-if="navOptionsCurrent == 2"></Altitude>
      <FaultRules v-if="navOptionsCurrent == 3"></FaultRules>
      <SchedulingRules v-if="navOptionsCurrent == 4"></SchedulingRules>
      <Area v-if="navOptionsCurrent == 5"></Area>
      <AreaTimeRange v-if="navOptionsCurrent == 6"></AreaTimeRange>
      <PowerLoadRateRange v-if="navOptionsCurrent == 7"></PowerLoadRateRange>
      <EnergyPrices v-if="navOptionsCurrent == 8"></EnergyPrices>
      <UnitConversion v-if="navOptionsCurrent == 9"></UnitConversion>
      <UnitTable v-if="navOptionsCurrent == 10"></UnitTable>
      <EnergyLimit v-if="navOptionsCurrent == 11"></EnergyLimit>
      <EarlyWarningLimit v-if="navOptionsCurrent == 12"></EarlyWarningLimit>
    </el-col>
  </el-row>
</template>

<script>
  import TradeNameTable from '@/views/MaintainedTable/TradeNameTable'
  import PlanTask from '@/views/MaintainedTable/PlanTask'
  import Altitude from '@/views/MaintainedTable/Altitude'
  import FaultRules from '@/views/MaintainedTable/FaultRules'
  import SchedulingRules from '@/views/MaintainedTable/SchedulingRules'
  import Area from '@/views/MaintainedTable/Area'
  import AreaTimeRange from '@/views/MaintainedTable/AreaTimeRange'
  import PowerLoadRateRange from '@/views/MaintainedTable/PowerLoadRateRange'
  import EnergyPrices from '@/views/MaintainedTable/EnergyPrices'
  import UnitConversion from '@/views/MaintainedTable/UnitConversion'
  import UnitTable from '@/views/MaintainedTable/UnitTable'
  import EnergyLimit from '@/views/MaintainedTable/EnergyLimit'
  import EarlyWarningLimit from '@/views/MaintainedTable/EarlyWarningLimit'
  export default {
    name: "MaintainedBoard",
    components:{
      TradeNameTable,PlanTask,Altitude,FaultRules,SchedulingRules,Area,AreaTimeRange,PowerLoadRateRange,EnergyPrices,UnitConversion,UnitTable,EnergyLimit,EarlyWarningLimit
    },
    data(){
      return {
        navOptionsCurrent:0,
        navOptions:[
          {name:"品名"},
          {name:"计划和任务"},
          {name:"电能尖峰平谷"},
          {name:"故障规则"},
          {name:"调度规则"},
          {name:"区域管理"},
          {name:"区域时段范围"},
          {name:"电能负荷率范围"},
          {name:"能耗价格"},
          {name:"采集数据的单位换算"},
          {name:"单位表"},
          {name:"能耗限度"},
          {name:"温度预警限度"},
        ],
      }
    },
    methods: {
      showPage(index) {
        this.navOptionsCurrent = index
      }
    }
  }
</script>

<style scoped>

</style>
