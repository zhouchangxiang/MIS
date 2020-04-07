<template>
    <div class="show-box">
         <DateC></DateC>
         <ShowNumber></ShowNumber>
       </div>
</template>
<script>
import DateC from '../common/Choosedate.vue'
import ShowNumber from '../common/Shownumber.vue'
export default {
    data(){
        return {
          radio1:1,
          radio2:1
        }
    },
    components:{
      DateC,
      ShowNumber
    },
    methods:{
      myc(){
        this.$toast(this.radio1)
      }
    }
}
</script>
<style lang="less" scoped>
    @bgca:#3D4048FF;
     .show-box{
        position: relative;
        width: 375px;
        box-sizing: border-box;
        padding: 0 12px 12px 13px;

    }
</style>