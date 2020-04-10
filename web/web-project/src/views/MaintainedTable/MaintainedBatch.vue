<template>
  <el-row>
    <el-col :span="24">
      <div class="navOptionsItem">
        <ul>
          <li v-for="item in navOptions" @click="showPage(item.value)"><a href="javascript:;" :class="{ active:item.value===navOptionsCurrent }" v-html="item.name"></a></li>
        </ul>
      </div>
      <TradeNameTable v-if="navOptionsCurrent === 'TradeNameTable'"></TradeNameTable>
      <Process v-if="navOptionsCurrent === 'Process'"></Process>
      <PlanTask v-if="navOptionsCurrent === 'PlanTask'"></PlanTask>
    </el-col>
  </el-row>
</template>

<script>
  import TradeNameTable from '@/views/MaintainedTable/TradeNameTable'
  import PlanTask from '@/views/MaintainedTable/PlanTask'
  import Process from '@/views/MaintainedTable/Process'
  export default {
    name: "MaintainedBatch",
    components:{
      TradeNameTable,PlanTask,Process
    },
    data(){
      return {
        navOptionsCurrent:"TradeNameTable",
        navOptions:[
          {name:"品名",value:"TradeNameTable"},
          {name:"工序",value:"Process"},
          {name:"计划和任务",value:"PlanTask"},
        ],
      }
    },
    methods: {
      showPage(navOptionsCurrent) {
        this.navOptionsCurrent = navOptionsCurrent
      }
    }
  }
</script>

<style scoped>

</style>
