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
var moment=require('moment')
import store from '../../store/index'
export default {
    data(){
        return {
          choosedate:0,
          choosekind:0,
          StartTime:'2020-04-07 12:22:59',
          EndTime:'',
          myapi:'',
          myobj:{},
          kind:''
        }
    },
    methods:{
        ChooseDate(){
            this.$store.commit('Choosedate',this.choosedate)
            let n=this.$store.state.choosedate
            this.EndTime=moment(new Date()).format('YYYY-MM-DD HH:mm:ss')
            let x=this.$store.state.choosekind
            switch(x){
                case 0:
                    this.myapi='/energywater';
                    break;
                case 1:
                    this.myapi='/energyelectric';
                    break;
                case 2:
                    this.myapi='/energysteam';
                    break;
            }
            if(n===0){
                this.StartTime='2020-04-01 00:00:00'
            }else if(n===1){
                this.StartTime='2020-04-07 00:00:00'
            }else{
                this.StartTime='2020-04-09 00:00:00'
            }
            this.$http.all([
                this.$http.get('/api'+this.myapi,{params:{
                StartTime:this.StartTime,
                EndTime:this.EndTime,
                AreaName:this.$store.state.workplace
                }}),
                this.$http.get('/api/batchMaintainEnergy',{params:{
                StartTime:this.StartTime,
                EndTime:this.EndTime,
                AreaName:this.$store.state.workplace
            }})
            ]).then(this.$http.spread((res1,res2)=>{
                this.$store.commit('Sbnumbers',JSON.parse(res1.data))
                this.$store.commit('NumBox',res2.data)
            }))
        },
        ChooseKind(){
            this.$store.commit('Choosekind',this.choosekind)
            let x=this.$store.state.choosedate
            let n=this.$store.state.choosekind
            switch(x){
                case 0:
                    this.StartTime='2020-04-01 00:00:00';
                    break;
                case 1:
                     this.StartTime='2020-04-07 00:00:00';
                    break;
                case 2:
                      this.StartTime='2020-04-09 00:00:00';
                    break;
            }
            if(n===0){
                this.myapi='/energywater',
                this.kind='水'
            }else if(n===1){
                this.myapi='/energyelectric',
                this.kind='电'
            }else{
                this.myapi='/energysteam',
                this.kind='汽'
            }
            this.$http.all([
                this.$http.get('/api'+this.myapi,{params:{
                StartTime:this.StartTime,
                EndTime:this.EndTime,
                AreaName:this.$store.state.workplace
                }}),
            this.$http.get('/api/areatimeenergycount',{params:{
              EnergyClass:this.kind,CompareTime:'2020-04-01'
            }})
            ]).then(this.$http.spread((res1,res2)=>{
                console.log(res2)
                this.$store.commit('Sbnumbers',JSON.parse(res1.data))
                this.$store.commit('CompareBox',res2.data.rows)
            }))
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