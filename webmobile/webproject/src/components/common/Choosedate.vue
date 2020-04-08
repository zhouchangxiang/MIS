<template>
    <div>
         <div class="show-top">
               <div class="tips">
                   <van-tabs type="card" title-active-color="#1E222B" title-inactive-color="#fff" @click="mytip" v-model="active"> 
                        <van-tab title="年"></van-tab>
                        <van-tab title="月"></van-tab>
                        <van-tab title="日"></van-tab>
                    </van-tabs>
                </div>
               <div class="tips">
                   <van-tabs type="card" title-active-color="#1E222B"  title-inactive-color="#fff" v-model="active1" @click="mytips">
                        <van-tab title="水"></van-tab>
                        <van-tab title="电"></van-tab>
                        <van-tab title="气"></van-tab>
                    </van-tabs>
               </div>
           </div>
    </div>
</template>
<script>
export default {
    data(){
        return {
          radio1:1,
          radio2:1,
          active:1,
          active1:1
        }
    },
    methods:{
        myc(){
            this.$toast(this.radio1)
        },
        mytip(){
            this.$toast(this.active)
        },
        mytips(){
            this.$toast(this.active1+1)
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
            .tips{
                float: left;
                margin-right: 20px;
                background-color:#1E222B;
                height: 18px;
            }
        }
</style>