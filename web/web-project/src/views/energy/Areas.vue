<template>
  <el-row>
    <el-col :span="24">
      <div class="navOptionsItem">
        <ul>
          <li v-for="(item,index) in navOptions" @click="showPage(index)"><a href="javascript:;" :class="{ active:index==navOptionsCurrent }">{{ item.name }}</a></li>
        </ul>
      </div>
      <AreaPeriodTime v-if="navOptionsCurrent == 0"></AreaPeriodTime>
      <AreaBatch v-else-if="navOptionsCurrent == 1"></AreaBatch>
      <AreaEqDetails v-else-if="navOptionsCurrent == 2"></AreaEqDetails>
    </el-col>
  </el-row>
</template>

<script>
  import AreaBatch from '@/views/energy/AreaBatch'
  import AreaPeriodTime from '@/views/energy/AreaPeriodTime'
  import AreaEqDetails from '@/views/energy/AreaEqDetails'
  export default {
    name: "Areas",
    components:{
      AreaBatch,AreaPeriodTime,AreaEqDetails
    },
    data(){
      return {
        navOptionsCurrent:0,
        navOptions:[
          {name:"时段能耗"},
          {name:"单位批次能耗"},
          {name:"设备详情"}
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
  .navOptionsItem{
    width:100%;
    background:#082F4C;
    clear: both;
    overflow: hidden;
    border-radius:4px;
    margin-bottom: 20px;
  }
  .navOptionsItem ul li{
    float:left;
    margin:10px;
  }
  .navOptionsItem ul li a{
    display: block;
    color:#fff;
    font-size:18px;
    background:#082F4C;
    text-decoration: none;
    padding:5px 20px;
    border-radius:4px;
  }
  .navOptionsItem ul li a.active{
    color:#082F4C;
    background:#fff;
  }
</style>
