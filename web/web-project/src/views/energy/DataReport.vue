<template>
  <el-row>
    <el-col :span="24">
      <div class="navOptionsItem">
        <ul>
          <li v-for="(item,index) in navOptions" @click="showPage(index)"><a href="javascript:;" :class="{ active:index==navOptionsCurrent }">{{ item.name }}</a></li>
        </ul>
      </div>
      <DataReportElectricity v-if="navOptionsCurrent == 0"></DataReportElectricity>
      <DataReportHydroenergy v-if="navOptionsCurrent == 1"></DataReportHydroenergy>
      <DataReportSteam v-if="navOptionsCurrent == 2"></DataReportSteam>
    </el-col>
  </el-row>
</template>

<script>
  import DataReportElectricity from '@/views/energy/DataReportElectricity'
  import DataReportHydroenergy from '@/views/energy/DataReportHydroenergy'
  import DataReportSteam from '@/views/energy/DataReportSteam'
  export default {
    name: "DataReport",
    components:{
      DataReportElectricity,DataReportHydroenergy,DataReportSteam
    },
    data(){
      return {
        navOptionsCurrent:0,
        navOptions:[
          {name:"电能报表"},
          {name:"水能报表"},
          {name:"汽能报表"}
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
