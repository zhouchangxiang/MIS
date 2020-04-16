<template>
    <div class="show-box">
            <DateC :newac="newac"></DateC>
            <div class="show" @click="getM()">
                 <ve-line :data="chartData" :settings="chartSettings"></ve-line>
            </div>

    </div>
</template>
<script>
import DateC from '../common/Choosedate.vue'
export default {
    
    data(){
        this.chartSettings = {
        metrics: ['访问用户', '下单用户'],
        dimension: ['日期']
      }
        return {
        newac:2,
        chartData: {
          columns: ['日期', '访问用户', '下单用户', '下单率'],
          rows: [
            { '日期': '1/1', '访问用户': 1393, '下单用户': 1093, '下单率': 0.32 },
            { '日期': '1/2', '访问用户': 3530, '下单用户': 3230, '下单率': 0.26 },
            { '日期': '1/3', '访问用户': 2923, '下单用户': 2623, '下单率': 0.76 },
            { '日期': '1/4', '访问用户': 1723, '下单用户': 1423, '下单率': 0.49 },
            { '日期': '1/5', '访问用户': 3792, '下单用户': 3492, '下单率': 0.323 },
            { '日期': '1/6', '访问用户': 4593, '下单用户': 4293, '下单率': 0.78 }
          ]
        }
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