<template>
  <el-row>
    <el-col :span="24">
      <div class="navOptionsItem">
        <ul>
          <li v-for="(item,index) in navOptions" @click="showPage(index)"><a href="javascript:;" :class="{ active:index==navOptionsCurrent }" v-html="item.name"></a></li>
        </ul>
      </div>
      <AreasHome v-if="navOptionsCurrent == 0"></AreasHome>
      <AreaPeriodTime v-else-if="navOptionsCurrent == 1"></AreaPeriodTime>
      <AreaBasicData v-else-if="navOptionsCurrent == 2"></AreaBasicData>
      <AreaBatch v-else-if="navOptionsCurrent == 3"></AreaBatch>
      <AreaEqDetails v-else-if="navOptionsCurrent == 4"></AreaEqDetails>
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
    inject:['newAreaName'],
    mounted(){
      if(this.$route.query.navOptionsCurrent === undefined){
        this.navOptionsCurrent = 0
      }else{
        this.navOptionsCurrent = this.$route.query.navOptionsCurrent
      }
    },
    data(){
      return {
        navOptionsCurrent:0,
        navOptions:[
          {name:'<i class="fa fa-home fa-1x"></i>'},
          {name:"能耗看板"},
          {name:"能耗明细"},
          {name:"单位批次能耗"},
          {name:"设备详情"},
          {name:"成本中心"},
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
