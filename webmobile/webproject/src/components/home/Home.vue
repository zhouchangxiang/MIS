<template>
    <div class="show-box">
           <div class="show-top">年月日</div>
           <div class="show-banner">显示模板</div>
           <div class="show-body">生产批次</div>
           <div class="show-foot">耗费成本</div>
       </div>
</template>
<script>
export default {
    data(){
        return {

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
        background-color: @bgca;
        .show-top{
            width:105px;
            height:18px;
            background:#ccc;
            opacity:1;
            border-radius:4px;
            color:#fff;
            font-size: 10px;
            margin-bottom: 21px;
        }
        .show-banner{
            width:350px;
            height:173px;
            background:rgba(126,127,132,1);
            box-shadow:0px 0px 6px rgba(255,255,255,0.16);
            opacity:1;
            border-radius:4px;
            margin-bottom: 21px;
        }
        .show-body{
            height:199px;
            background:rgba(126,127,132,1);
            box-shadow:0px 0px 6px rgba(255,255,255,0.16);
            opacity:1;
            border-radius:4px;
            background-color: #666;
            margin-bottom: 13px;
        }
        .show-foot{
            height:64px;
            background:@bgca;
            box-shadow:0px 0px 6px rgba(255,255,255,0.16);
            opacity:1;
            border-radius:4px;
            background-color: #ccc;
        }

    }
</style>