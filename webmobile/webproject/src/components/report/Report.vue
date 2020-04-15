<template>
    <div class="show-box">
            <DateC :newac="newac"></DateC>
            <div class="show" @click="getM()">
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
        getM(){
            // this.$http.get('/energyall',{params:{
            //    ModelFlag:"在线检测情况" 
            // }}).then(res=>{
            //     console.log(res)
            //     //接口还在写
            //     // 只传递一个参数
            //     //区分水电气
            //     //返回name、online、total、rate
            // })

            
        }
    }
}
</script>
<style lang="less" scoped>
    .show-box{
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