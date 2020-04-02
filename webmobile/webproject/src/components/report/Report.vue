<template>
    <div class="content"><ve-histogram :data="chartData" :settings="chartSettings"></ve-histogram></div>
</template>
<script>
export default {
    
    data(){
        this.chartSettings = {
        showLine: ['下单用户']
      }
        return {
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
    }
}
</script>
<style lang="less" scoped>
    .content{
        position:relative;
        width:375px;
        height:526px;
        box-sizing: border-box;
        padding: 0 12px 12px 13px;
    }
</style>