<template>
    <div>
         <div class="show-top">
               <div class="tips">
                   <van-tabs type="card" title-active-color="#1E222B" title-inactive-color="#fff" v-model="choosedate" @click="ChooseDate"> 
                        <van-tab title="年"></van-tab>
                        <van-tab title="月"></van-tab>
                        <van-tab title="日"></van-tab>
                    </van-tabs>
                </div>
               <div class="tips">
                   <van-tabs type="card" title-active-color="#1E222B"  title-inactive-color="#fff" v-model="choosekind" @click="ChooseKind">
                        <van-tab title="水"></van-tab>
                        <van-tab title="电"></van-tab>
                        <van-tab title="气"></van-tab>
                    </van-tabs>
               </div>
           </div>
    </div>
</template>
<script>
import store from '../../store/index'
export default {
    data(){
        return {
          choosedate:1,
          choosekind:2
        }
    },
    methods:{
        ChooseDate(){
            this.$store.state.choosedate=this.choosedate

        },
        ChooseKind(){
            this.$store.state.choosekind=this.choosekind
       
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