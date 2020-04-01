<template>
    <div class="show-box">
           <div class="show-top">
               <div><span>年</span><span>月</span><span>日</span></div>
               <div><span>水</span><span>电</span><span>气</span></div>
           </div>
           <div class="show-banner">显示模板</div>
           <div class="show-body">生产批次</div>
           <div class="show-foot">耗费成本</div>
       </div>
</template>
<script>
export default {
    data(){
        return {
            currentPage:1
        }
    },
    methods:{

    }
}
</script>
<style lang="less" scoped>
    @bgca:#3D4048FF;
    @bgcc:#1E222BFF;
     .show-box{
        position: relative;
        width: 375px;
        box-sizing: border-box;
        padding: 0 12px 12px 13px;
        background-color: @bgcc;
        .show-top{
            height:18px;
            opacity:1;
            border-radius:4px;
            color:#fff;
            font-size: 10px;
            margin-bottom: 21px;
            div{
                display:inline-block;
                margin-right: 20px;
                span{
                    display: inline-block;
                    width:38px;
                    height:18px;
                    text-align: center;
                    background-color:@bgca;
                    opacity:1;
                    border-radius:4px;
                    font-size:10px;
                    font-family:PingFang SC;
                    font-weight:400;
                    opacity:1;
                    &:hover{
                        background:rgba(255,255,255,1);
                        color:#000;
            }
}
            }
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