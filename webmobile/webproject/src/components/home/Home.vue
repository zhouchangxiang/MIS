<template>
    <div class="show-box">
        <div class="show-top">
               <div class="tips">
                   <van-tabs type="card" title-active-color="#1E222B" title-inactive-color="#fff" v-model="choosedate" @click="ChooseDate"> 
                        <van-tab title="日"></van-tab>
                        <van-tab title="月"></van-tab>
                        <van-tab title="年"></van-tab>
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
        <van-loading size="24px" vertical v-if="loading" color="lightgreen" type="spinner">加载中...</van-loading>
        <div class="show-banner">
                  <div class="sb-name">厂区能耗</div>
                  <div class="sb-number">{{$store.state.sbnumber.value}}</div>
                  <div class="sb-compare">较上期</div>
                  <div class="sb-l-n">+1.345%</div>
                  <div class="sb-dw">单位</div>
                  <div class="sb-t">{{$store.state.sbnumber.unit}}</div>
                  <div class="tabbar">
                      <ve-bar :data="chartData" width="150px" height="150px" :legend-visible="false" :extend="areaTimeChartExtend"></ve-bar>
                   </div>
           </div>
           <div class="show-body">
               <div class="sb-l" v-for="(item,index) in numberbox" :key='index'>
                   <div class="scpc">生产批次</div>
                   <div class="scpc-s">{{item.batchCount}}</div>
                   <div class="znhl">总耗能量</div>
                   <div class="znhl-s">{{choosekind==0?item.waterCon:item.steamCon}}</div>
                   <div class="dwnh">单位批次能耗</div>
                   <div class="dwnh-s">{{choosekind==0?item.waterEveryBatch:item.steamEveryBatch}}</div>
                   <div class="dw-kwh">{{choosekind==0?item.waterUnit:item.steamUnit}}</div>
                   <div class="dw-pc">{{choosekind==0?item.waterUnit:item.steamUnit}}&nbsp;/&nbsp;批</div>
               </div>
               <div class="sb-r">
                    <van-picker :columns="area" @change="onChange" :default-index="2"/>
               </div>
           </div>
           <ShowNumber></ShowNumber>
       </div>
</template>
<script>
var moment=require('moment')
import ShowNumber from '../common/Shownumber.vue'
import store from '../../store/index'
var moment=require('moment')
export default {
    data(){
        return {
            areaTimeChartExtend: {
                yAxis:{
                    show:false,
                    inverse:true
                },
                xAxis:{
                    show:false,
                    inverse:true
                },
                grid:{
                    containLabel: false,
                    left: '0',
                    right: '0',
                    bottom: '0',
                    top:'0'
                },
                series: {
                    barMaxWidth : '6px',
                    smooth: false
                },
                label:{
                    show:true,
                    position:"top",
                    formatter: '{b}: {@score}'
                },
                itemStyle: {
                    color:"#fff"
                }
                },
            myapi:'',
            area:['原提取车间','GMP车间','固体制剂车间','中试车间'],
            StartTime:'2020-04-07 12:22:59',
            numberbox:[],
            loading:false,
            chartData: {
            columns: ['区域', '能耗量'],
            rows: [
                { '区域': '污水站', '能耗量': 100},
                { '区域': '前提取车间', '能耗量': 100},
                { '区域': '二车间', '能耗量': 100},
                { '区域': '综合车间', '能耗量': 100}
            ]
            },
            choosedate:0,
            choosekind:0,
            StartTime:'2020-04-07 12:22:59',
            EndTime:'',
            myapi:'',
            myobj:{},
            kind:''
        }
    },
    components:{
        ShowNumber
    },
    mounted(){
        this.initNum()
    },
    methods:{
    onChange(picker, value) {
        this.loading=true
        this.$store.commit("Chooseworkplace",value)
        this.$toast(value);
        let n=this.$store.state.choosedate
        this.EndTime=moment(new Date()).format('YYYY-MM-DD HH:mm:ss')
        var x=this.choosekind
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
                this.loading=false
                this.$store.commit('Sbnumbers',JSON.parse(res1.data))
                this.$store.commit('NumBox',res2.data)
                this.numberbox=this.$store.state.numberbox 
            }))
    },
    initNum(){
        let str1=moment(new Date()).format('YYYY-MM-DD HH:mm:ss')
        let str2=moment(new Date()).format('YYYY-MM-DD')
        this.loading=true
        this.$http.all([
            this.$http.get('/api/energywater',{params:{
            StartTime:'2020-04-25 12:22:59',
            EndTime:str1,
            AreaName:'前处理车间'
            }}),
            this.$http.get('/api/batchMaintainEnergy',{params:{
            StartTime:'2020-04-07 12:22:59',
            EndTime:str1,
            AreaName:'前处理车间'
        }}),
         this.$http.get('/api/areatimeenergycount',{params:{
              EnergyClass:'电',CompareTime:'2020-04-14'
            }})
        ]).then(this.$http.spread((res1,res2,res3)=>{
            this.loading=false
            this.chartData.rows=res3.data.rows.slice(0, 4)
            let arr=res3.data.rows
            this.area=[]
            for(var i=0;i<arr.length;i++){
               this.area.push(arr[i]['区域'])
            }
            this.$store.commit('Sbnumbers',JSON.parse(res1.data))
            this.$store.commit('NumBox',res2.data)
            this.numberbox=this.$store.state.numberbox

    }))},
    ChooseDate(){
            this.$store.commit('Choosedate',this.choosedate)
            let n=this.$store.state.choosedate
            this.EndTime=moment(new Date()).format('YYYY-MM-DD HH:mm:ss')
            var x=this.choosekind
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
            var x=this.$store.state.choosedate
            var n=this.choosekind
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
                this.$store.commit('Sbnumbers',JSON.parse(res1.data))
                this.chartData.rows=res2.data.rows.slice(0, 4)
            }))
        }
}
}
</script>
<style lang="less" scoped>
    @bgca:#3D4048FF;
    @bgcc:#1E222BFF;
    @bgct:#7E7F84;
    span{
        text-align: center;
    }
     .show-box{
        position: relative;
        width: 375px;
        box-sizing: border-box;
        padding: 0 12px 12px 13px;
        background-color: @bgcc;
        .show-banner{
            position: relative;
            width:350px;
            height:173px;
            overflow: hidden;
            font-family:PingFang SC;
            box-sizing: border-box;
            background:rgba(126,127,132,1);
            box-shadow:0px 0px 6px rgba(255,255,255,0.16);
            opacity:1;
            border-radius:4px;
            margin:21px 0 20px 0;
           .sb-name{
               position: absolute;
               top:14px;
               left: 15px;
               height:20px;
               font-size:14px;
               font-weight:400;
               line-height:20px;
               color:rgba(255,255,255,1);
               opacity:1;
           }
           .sb-number{
               position: absolute;
               left:13px;
               top:58px;
               font-size: 32px;
               word-spacing: 20px;
               height:36px;
               color:rgba(250,192,0,1);
               opacity:1;

           }
           .sb-compare{
               position: absolute;
               left: 15px;
               top: 125px;
               height:11px;
               font-size:8px;
               font-weight:400;
               line-height:11px;
               color:rgba(255,255,255,1);
               opacity:1; 
           }
           .sb-l-n{
               position: absolute;
               left:15px;
               top:142px;
               height:17px;
               font-size:12px;
               font-weight:500;
               line-height:17px;
               color:rgba(255,80,65,1);
               opacity:1;
           }
          .sb-dw{
            position: absolute;
            top:125px;
            left:91px;
            height:11px;
            font-size:8px;
            font-weight:400;
            line-height:11px;
            color:rgba(255,255,255,1);
            opacity:1;
            }
            .sb-t{
                position: absolute;
                left:96px;
                top:142px;
                width:7px;
                height:17px;
                font-size:12px;
                font-weight:500;
                line-height:17px;
                color:rgba(255,255,255,1);
                opacity:1;
            }
            .tabbar{
                position: absolute;
                top:15px;
                right:5px;
                width: 150px;
                height: 150px;
            }
           
        }
        .show-body{
            position: relative;
            height:199px;
            opacity:1;
            border-radius:4px;
            margin-bottom: 13px;
            .sb-l{
                position: absolute;
                top:0;
                left:0;
                width:196px;
                height:199px;
                background:rgba(126,127,132,1);
                box-shadow:0px 0px 6px rgba(255,255,255,0.16);
                opacity:1;
                border-radius:4px;
                .scpc{
                    position: absolute;
                    top:11px;
                    left:15px;
                    width:60px;
                    height:11px;
                    font-size:8px;
                    font-family:PingFang SC;
                    font-weight:400;
                    line-height:11px;
                    color:rgba(255,255,255,1);
                    opacity:1;
                }
                .scpc-s{
                    position: absolute;
                    top:30px;
                    left: 14px;
                    width:17px;
                    height:25px;
                    font-size: 23px;
                    color:rgba(0,250,231,1);
                    opacity:1;
                }
                .znhl{
                    position: absolute;
                    top:74px;
                    left:15px;
                    font-size: 8px;
                    color: rgba(255,255,255,1);
                }
                .znhl-s{
                    position: absolute;
                    top:95px;
                    left: 14px;
                    width:17px;
                    height:25px;
                    font-size: 23px;
                    color:#FAC000;
                    opacity:1;
                }
                .dwnh{
                    position: absolute;
                    top:140px;
                    left: 15px;
                    font-size: 8px;
                    color:rgba(255, 255, 255, 1)
                }
                .dwnh-s{
                    position: absolute;
                    top:161px;
                    left: 14px;
                    height:25px;
                    font-size: 23px;
                    color:#00FAE7;
                    opacity:1;
                }
                .dw-kwh{
                    position: absolute;
                    right: 10px;
                    top:108px;
                    font-size: 8px;
                    font-weight: 500;
                    color: #fff;
                }
                .dw-pc{
                    position: absolute;
                    right: 8px;
                    top:174px;
                    font-size: 8px;
                    font-weight: 500;
                    color: #fff;
                }
            }
            .sb-r{
                position: absolute;
                top:0;
                right:0;
                width:150px;
                height:199px;
                background-color: @bgcc;
                opacity:1;
                border-radius:4px;
                ul{
                    margin: 0;
                    padding: 0;
                    li{
                        height: 35px;
                        line-height: 20px;
                        color: #fff;
                        text-align: right;
                    }
                }
            }
        }
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

    }
</style>