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
        //     //接口还在写
        //     // 只传递一个参数
        //     //区分水电气
        //     //返回name、online、total、rate
        }
    },
    components:{
        DateC
    },
    methods:{
        getM(){
            this.$http.get('/api/areatimeenergycount',{params:{
              EnergyClass:"水",CompareTime:"2020-04-03"
            }}).then(res=>{
                console.log(res)
            },
                this.$http.get('/api/energywater',{params:{
                StartTime:'2020-04-03 00:00:00',
                EndTime:'2020-04-03 23:59:00',
                AreaName:'提取二车间'
            }}).then(res=>{
                console.log('------------------------------------')
                console.log(res.data)
            })

            
            )}
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