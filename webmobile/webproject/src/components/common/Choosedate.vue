<template>
    <div>
         <div class="show-top">
               <div class="tips">
                   <van-radio-group v-model="radio1" direction="horizontal" @change="myc">
                        <van-radio name="1" shape="square" checked-color="#07c160">年</van-radio>
                        <van-radio name="2" shape="square" checked-color="#07c160">月</van-radio>
                        <van-radio name="3" shape="square" checked-color="#07c160">日</van-radio>
                    </van-radio-group>
                </div>
               <div class="tips">
                    <van-radio-group v-model="radio2" direction="horizontal">
                        <van-radio name="1" shape="square" checked-color="#1989fa">水</van-radio>
                        <van-radio name="2" shape="square" checked-color="#1989fa">电</van-radio>
                        <van-radio name="3" shape="square" checked-color="#1989fa">气</van-radio>
                    </van-radio-group>
               </div>
           </div>
    </div>
</template>
<script>
export default {
    data(){
        return {
          radio1:1,
          radio2:1
        }
    },
    methods:{
        myc(){
            this.$toast(this.radio1)
        }
    }
}
</script>
<style lang="less" scoped>
.show-top{
            height:18px;
            opacity:1;
            border-radius:4px;
            color:#fff;
            font-size: 10px;
            margin-bottom: 21px;
            .tips{
                float: left;
                margin-right: 20px;
                width: 120px;
                background-color:#ccc;
            .van-radio{
                margin-right: 0px;
            }
            }
        }
</style>