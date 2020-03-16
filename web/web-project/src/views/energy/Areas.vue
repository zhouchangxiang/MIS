<template>
  <el-row>
    <el-col :span="24">
      <div class="navOptionsItem">
        <ul>
          <li v-for="(item,index) in navOptions" @click="showPage(index)"><a href="javascript:;" :class="{ active:index==navOptionsCurrent }" v-html="item.name"></a></li>
        </ul>
      </div>
      <AreasHome v-if="navOptionsCurrent == 0"></AreasHome>
      <AreaPeriodTime v-if="navOptionsCurrent == 1"></AreaPeriodTime>
      <AreaBatch v-else-if="navOptionsCurrent == 2"></AreaBatch>
      <AreaEqDetails v-else-if="navOptionsCurrent == 3"></AreaEqDetails>
      <AreaBasicData v-else-if="navOptionsCurrent == 4"></AreaBasicData>
      <CostCenter v-else-if="navOptionsCurrent == 5"></CostCenter>
    </el-col>
  </el-row>
</template>

<script>
  import AreasHome from '@/views/energy/AreasHome'
  import AreaBatch from '@/views/energy/AreaBatch'
  import AreaPeriodTime from '@/views/energy/AreaPeriodTime'
  import AreaEqDetails from '@/views/energy/AreaEqDetails'
  import AreaBasicData from '@/views/energy/AreaBasicData'
  import CostCenter from '@/views/energy/CostCenter'
  export default {
    name: "Areas",
    components:{
      AreasHome,AreaBatch,AreaPeriodTime,AreaEqDetails,AreaBasicData,CostCenter
    },
    data(){
      return {
        navOptionsCurrent:0,
        navOptions:[
          {name:'<i class="fa fa-home"></i>'},
          {name:"能耗看板"},
          {name:"单位批次能耗"},
          {name:"设备详情"},
          {name:"基础数据"},
          {name:"成本中心"},
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
