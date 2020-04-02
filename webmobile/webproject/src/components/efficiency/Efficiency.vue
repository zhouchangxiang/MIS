<template>
    <div class="content">
        <ve-bmap
            :settings="chartSettings"
            :series="chartSeries"
            :tooltip="chartTooltip">
        </ve-bmap>
    </div>
</template>
<script>
export default {
   data () {
      this.chartSettings = {
        key: 'oBvDtR6nzWtVchkY4cLHtnah1VVZQKRK',
        bmap: {
          center: [40.13066322374, 30.240018034923],
          zoom: 10,
          roam: true,
          mapStyle: {}
        }
      }
      this.chartTooltip = { show: true }
      return {
        chartSeries: [
          {
            type: 'scatter',
            coordinateSystem: 'bmap',
            data: [
              [120, 30, 1]
            ]
          }
        ]
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