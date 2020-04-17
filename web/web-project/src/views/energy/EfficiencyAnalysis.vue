<template>
  <el-row>
    <el-col :span="24">
      <div class="navOptionsItem">
        <ul>
          <li v-for="(item,index) in navOptions" @click="showPage(index)"><a href="javascript:;" :class="{ active:index==navOptionsCurrent }">{{ item.name }}</a></li>
        </ul>
      </div>
      <EfficiencyAnalysisRun v-if="navOptionsCurrent === 0"></EfficiencyAnalysisRun>
      <EfficiencyAnalysisLoss v-if="navOptionsCurrent === 1"></EfficiencyAnalysisLoss>
      <EfficiencyAnalysisPipe v-if="navOptionsCurrent === 2"></EfficiencyAnalysisPipe>
    </el-col>
  </el-row>
</template>

<script>
  import EfficiencyAnalysisRun from '@/views/energy/EfficiencyAnalysisRun'
  import EfficiencyAnalysisLoss from '@/views/energy/EfficiencyAnalysisLoss'
  import EfficiencyAnalysisPipe from '@/views/energy/EfficiencyAnalysisPipe'
  export default {
    name: "EfficiencyAnalysis",
    components:{
      EfficiencyAnalysisRun,EfficiencyAnalysisLoss,EfficiencyAnalysisPipe
    },
    data(){
      return {
        navOptionsCurrent:0,
        navOptions:[
          {name:"运行效率"},
          {name:"线损分析"},
          {name:"管损分析"},
        ]
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
