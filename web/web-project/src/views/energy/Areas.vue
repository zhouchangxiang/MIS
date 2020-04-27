<template>
  <el-row>
    <el-col :span="24">
      <div class="navOptionsItem">
        <ul>
          <li v-for="item in navOptions" @click="showPage(item.value)"><a href="javascript:;" :class="{ active:item.value==navOptionsCurrent }" v-html="item.name"></a></li>
        </ul>
      </div>
      <AreasHome v-if="navOptionsCurrent == 1"></AreasHome>
      <AreaPeriodTime v-else-if="navOptionsCurrent == 2"></AreaPeriodTime>
      <AreaBasicData v-else-if="navOptionsCurrent == 3"></AreaBasicData>
      <AreaBatch v-else-if="navOptionsCurrent == 4"></AreaBatch>
      <AreaEqDetails v-else-if="navOptionsCurrent == 5"></AreaEqDetails>
      <CostCenter v-else-if="navOptionsCurrent == 6"></CostCenter>
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
  var moment = require('moment');
  export default {
    name: "Areas",
    components:{
      AreasHome,AreaBatch,AreaPeriodTime,AreaEqDetails,AreaBasicData,CostCenter
    },
    inject:['newAreaName'],
    mounted(){
      this.getNavOptionsCurrent()
    },
    data(){
      return {
        navOptionsCurrent:1,
        navOptions:[
          {name:'<i class="fa fa-home fa-1x"></i>',value:1},
          {name:"能耗看板",value:2},
          {name:"能耗明细",value:3},
          {name:"单位批次能耗",value:4},
          {name:"设备详情",value:5},
          {name:"成本中心",value:6},
        ],
      }
    },
    methods: {
      showPage(index) {
        this.navOptionsCurrent = index
        // this.$router.push({
        //   query:{'areaName':this.newAreaName.areaName,'navOptionsCurrent':index,'t':Date.now()}
        // })
        //this.getNavOptionsCurrent()
      },
      getNavOptionsCurrent(){
        if(this.$route.query.navOptionsCurrent === undefined){
          this.navOptionsCurrent = 1
        }else{
          this.navOptionsCurrent = this.$route.query.navOptionsCurrent
        }
      }
    }
  }
</script>

<style scoped>

</style>
