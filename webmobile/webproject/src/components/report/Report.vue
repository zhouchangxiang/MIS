<template>
    <div class="content">
        <DateC :newac="newac"></DateC>
        <div class="show">
        </div>

    </div>
</template>
<script>
import DateC from '../common/Choosedate.vue'
export default {
    
    data(){
        return {
          newac:2
        }
    },
    components:{
        DateC
    },
    methods:{
    }
}
</script>
<style lang="less" scoped>
    .content{
        position:relative;
        width:375px;
        height:526px;
        box-sizing: border-box;
        background-color: #1E222B;
        padding: 0 12px 12px 13px;
        .show{
            width: 100%;
            height: 300px;
            background-color: #ccc;
            margin-top: 20px;
        }
    }
</style>