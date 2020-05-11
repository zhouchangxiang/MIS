<template>
    <div class="show-box">
           <div class="date-box">
               <div class="tips">
                   <van-tabs type="card" title-active-color="#1E222B" title-inactive-color="#fff" v-model="choosedate" @click="ChooseDate($event)"> 
                        <van-tab title="年"></van-tab>
                        <van-tab title="月"></van-tab>
                        <van-tab title="日"></van-tab>
                    </van-tabs>
                </div>
               <div class="tips">
                   <van-tabs type="card" title-active-color="#1E222B"  title-inactive-color="#fff" v-model="choosekind" @click="ChooseKind($event)">
                        <van-tab title="水"></van-tab>
                        <van-tab title="电"></van-tab>
                        <van-tab title="气"></van-tab>
                    </van-tabs>
               </div>
           </div>
            <div class="show">
                <div class="roundpic">
                   <ve-ring :data="chartData" :settings="chartSettings" :legend-visible="false" :events="chartEvents" :extend="piechartExtend"></ve-ring>
                </div>
                <div class="listpic">
                    <ve-histogram :data="listchartData" width="350px" height="150px" :legend-visible="false"  :extend="ChartExtend">
                </ve-histogram></div>
            </div>
            <div class="list-banner">
                <div class="header">{{currentArea}}</div>
                <div class="body">
                    <div class='today-water'>本{{currentdate}}耗{{currentkind}}量:</div>
                    <div class='today-water-max'>本{{currentdate}}耗{{currentkind}}峰值:</div>
                    <div class='today-water-min'>本{{currentdate}}耗{{currentkind}}谷值:</div>
                    <div class='today-consume-rank'>本日耗排名:</div>
                    <div class='today-time1'>时间:</div>
                    <div class='today-time2'>时间:</div>
                    <div class='today-num1'>00.00</div>
                    <div class='today-num2'>{{highvalue}}</div>
                    <div class='today-num3'>{{lowvalue}}</div>
                    <div class='today-rank-num'>00.00</div>
                    <div class='today-time1-num'>00:00:00</div>
                    <div class='today-time2-num'>00:00:00</div>
                </div>
            </div>
    </div>
</template>
<script>
var moment=require('moment')
export default {
    data () {
        return {
        myArea:'',
        piechartExtend:{
                label:{
                    show:true,
                    position:"Right",
                    formatter:'{b}'
        }},
        chartSettings:{
            dataType: 'KMB',
            radius: [40,70],
            offsetY:"90px",
            label:{
            show:false
           },
            labelLine:{
                show:false
            }
        },
        chartEvents:{
                  click:function(e){
                   localStorage.setItem('myArea',e.data.name)
                  }
              },
        ChartExtend: {
            xAxis:{
                axisLabel:{
                    rotate:45
                }
            },
            grid:{
                    left:'0',
                    right:'0',
                    bottom:'0px',
                    top:'20px'
            },
            series:{
                    barMaxWidth : 15,
                    smooth: false
            }
        },
        choosedate:0,
        choosekind:0,
        date:['年','月','日'],
        kind:['水','电','汽'],
        currentkind:'水',
        currentdate:'年',
        currentArea:'综合车间',
        StartTime:'',
        EndTime:'',
        highvalue:1,
        lowvalue:1,
        flag:false,
        chartData: {
          columns: ['region', 'value'],
          rows: []
        },
        listchartData: {
          columns: ['region', 'value'],
          rows: []
        }
      }
    },
    created(){
        this.initOperation();
    },
    methods:{
        ChooseDate(e){
            this.currentdate=this.date[e]
            if(this.currentdate=='年'){
                this.StartTime='2020-04-14 00:00:00'
            }else if(this.currentdate=='月'){
                this.StartTime='2020-04-20 00:00:00'
            }else{
                this.StartTime='2020-04-23 00:00:00'
            }
            this.EndTime=moment(new Date()).format('YYYY-MM-DD HH:mm:ss')
            this.currentArea=localStorage.getItem('myArea')
            this.$http.get('/api/electricnergycost',{params:{
                StartTime:this.StartTime,
                EndTime:this.EndTime,
                TimeClass:this.currentkind,
                AreaName:this.currentArea
            }}).then((value) => {
                this.highvalue=value.data.periodTimeTypeItem[1].expendEnergy
                this.lowvalue=value.data.periodTimeTypeItem[3].expendEnergy
            })
        },
        ChooseKind(e){
           this.chartData.rows=[]
           this.listchartData.rows=[]
           this.currentkind=this.kind[e]
           var params={EnergyClass:this.currentkind,CompareTime:'2020-04-10'}
           if(!this.flag){
           this.flag=true
           this.$http.get('/api/areatimeenergycount',{params}).then((value) => {
               var arr=value.data.rows
               for(var i=0;i<arr.length;i++){
                   if(arr[i]['能耗量']){
                       this.chartData.rows.push({region:arr[i]['区域'],value:arr[i]['能耗量']})
                       this.listchartData.rows.push({region:arr[i]['区域'],value:arr[i]['能耗量']})
                   }
               }
            this.flag=false
            })}
        },
        initOperation(){
            var params={EnergyClass:'水',CompareTime:'2020-04-10'}
            this.$http.get('/api/areatimeenergycount',{params}).then((value) => {
               var arr=value.data.rows
               for(var i=0;i<arr.length;i++){
                   if(arr[i]['能耗量']){
                       this.chartData.rows.push({region:arr[i]['区域'],value:arr[i]['能耗量']})
                       this.listchartData.rows.push({region:arr[i]['区域'],value:arr[i]['能耗量']})
                   }
               }
           })
        }
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
            position: relative;
            width: 100%;
            background-color: #1E222B;
            margin-top: 15px;
            .roundpic{
            position: relative;
            width: 200px;
            height: 170px;
            left:50%;
            transform: translate(-50%);
            }
            .listpic{
            position: relative;
            top:10px;
            width: 100%;
            height: 150px;
            overflow: hidden;
            margin-top: 17px;
            border-radius: 4px;
            background-color:#ccc;
            }
        }
        .list-banner{
            position: relative;
            margin-top:20px;
            width: 350px;
            height: 120px;
            border-radius: 4px;
            background: #1E222B;
            .header{
                width: 100%;
                height:17px;
                text-align: center;
                font-size:12px;
                font-family:PingFang SC;
                font-weight:400;
                line-height:17px;
                color:rgba(255,255,255,1);
                opacity:1;
            }
            .body{
                position: relative;
                .today-water,.today-water-max,.today-water-min,
                .today-consume-rank,.today-time1,.today-time2{
                position: absolute;
                top:10px;
                left:10px;
                height:11px;
                font-size:8px;
                font-family:PingFang SC;
                font-weight:400;
                line-height:11px;
                color:rgba(255,255,255,1);
                opacity:1;
                }
                .today-water-max{
                    left:120px;
                }
                .today-water-min{
                    left:246px;
                }
                .today-consume-rank{
                    top:60px;
                    left:10px;
                }
                .today-time1{
                    left:120px;
                    top:60px;
                }
                .today-time2{
                    left:246px;
                    top:60px;
                }
                .today-num1,.today-num2,
                .today-num3,.today-rank-num,.today-time1-num,.today-time2-num
                {
                    position:absolute;
                    top:25px;
                    left:10px;
                    font-size: 20px;
                    color:#FAC000;
                }
                .today-num2{
                    left: 120px;
                }
                .today-num3{
                    left: 246px;
                }
                .today-rank-num{
                    left:10px;
                    top:75px;
                }
                .today-time1-num,.today-time2-num{
                    color: #fff;
                    left:120px;
                    top:75px;
                }
                .today-time2-num{
                    left:246px;
                }
            }

        }
    }
</style>