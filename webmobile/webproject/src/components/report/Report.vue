<template>
    <div class="show-box">
           <div class="date-box">
               <div class="tips">
                   <van-tabs type="card" title-active-color="#1E222B" title-inactive-color="#fff" v-model="choosedate"> 
                        <van-tab title="年"></van-tab>
                        <van-tab title="月"></van-tab>
                        <van-tab title="日"></van-tab>
                    </van-tabs>
                </div>
               <div class="tips">
                   <van-tabs type="card" title-active-color="#1E222B"  title-inactive-color="#fff" v-model="choosekind">
                        <van-tab title="水"></van-tab>
                        <van-tab title="电"></van-tab>
                        <van-tab title="气"></van-tab>
                    </van-tabs>
               </div>
           </div>
            <div class="show">
                <span>点击</span>
            </div>

    </div>
</template>
<script>
export default {
    
    data(){
        return {
        newac:2,
        choosedate:1,
        choosekind:0,
        
       }
    },
    methods:{
       
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
        .date-box{
            height:18px;
            opacity:1;
            border-radius:4px;
            color:#fff;
            font-size: 10px;
            .tips{
                float: left;
                margin-right: 20px;
                background-color:#1E222B;
                height: 18px;
            }
        }
        .show{
            width: 100%;
            height: 300px;
            background-color: #ccc;
            margin-top: 20px;
            span{
                display: inline-block;
                width: 50px;
                height: 50px;
                background-color: green;
                font-size: 8px;
            }
        }
    }
</style>