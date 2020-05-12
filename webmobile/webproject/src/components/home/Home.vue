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
                   <van-tabs type="card" title-active-color="#1E222B"  title-inactive-color="#fff" v-model="choosekind" @click="ChooseKind($event)">
                        <van-tab title="水"></van-tab>
                        <van-tab title="电"></van-tab>
                        <van-tab title="气"></van-tab>
                    </van-tabs>
               </div>
        </div>
        <van-loading size="24px" vertical v-if="loading" color="lightgreen" type="spinner">加载中...</van-loading>
        <div class="show-banner">
                  <div class="sb-name">厂区能耗</div>
                  <div class="sb-number">{{kindnum}}</div>
                  <div class="sb-compare">较上期</div>
                  <div class="sb-l-n" :class="this.todaydaywater-this.yesterdaywater>0?'maxcolor':'mincolor'">{{dayCompare}}</div>
                  <div class="sb-dw">单位</div>
                  <div class="sb-t">{{unit}}</div>
                  <div class="tabbar">
                      <ve-bar :data="chartData" width="150px" height="150px" :legend-visible="false" :extend="areaTimeChartExtend"></ve-bar>
                   </div>
           </div>
           <div class="show-body">
               <div class="sb-l">
                   <div class="scpc">生产批次</div>
                   <div class="scpc-s">{{kind==='电'?0:batchCount}}</div>
                   <div class="znhl">总耗能量</div>
                   <div class="znhl-s">{{kind==='水'?waterCon:(kind==='电'?0:steamCon)}}</div>
                   <div class="dwnh">单位批次能耗</div>
                   <div class="dwnh-s">{{kind==='水'?waterEveryBatch:(kind==='电'?0:steamEveryBatch)}}</div>
                   <div class="dw-kwh">{{unit}}</div>
                   <div class="dw-pc">&nbsp;/&nbsp;批</div>
               </div>
               <div class="sb-r">
                    <van-picker :columns="area" @change="onChange" :default-index="2"/>
               </div>
           </div>
          <div class="show-foot">
               <div class="sf-l">
                   <div class="hf">耗费成本</div>
                   <div class="all-money">{{cost}}<span>元</span></div>
               </div>
                <div class="sf-r">
                   <div class="machine">{{kind}}表在线情况</div>
                   <div class="tj"><span>{{onlineitem.online}}</span>&nbsp;/&nbsp;<span>{{onlineitem.total}}</span></div>
               </div>
        </div>
       </div>
</template>
<script>
var moment=require('moment')
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
                    formatter: '{b}'
                },
                itemStyle: {
                    color:"#fff"
                }
                },
            area:['原提取车间','GMP车间','固体制剂车间','中试车间'],
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
            kindall:['水','电','汽'],
            dateall:['日','月','年'],
            kind:'水',
            date:'日',
            unit:'t',
            cost:0,
            kindnum:0,
            yesterdaywater:0,
            yesterdayelectric:0,
            yesterdaysteam:0,
            todaydaywater:0,
            todaysteam:0,
            todaydayelectric:0,
            AreaName:'GMP车间',
            batchCount:0,
            steamCon:0,
            waterCon:0,
            steamEveryBatch:0,
            waterEveryBatch:0,
            onlineitem:{online:0,total:0},
            myapi:''
        }
    },
    created(){
        this.getInitMessage()
    },
    computed:{
         dayCompare(){
        if(this.kind==='水'){
        if(this.todaydaywater > 0){
          var compare = (this.todaydaywater - this.yesterdaywater) / this.todaydaywater * 100
          if(this.todaydaywater - this.yesterdaywater > 0){
            return "+" + compare.toFixed(2) + "%"
          }else{
            return compare.toFixed(2) + "%"
          }
        }else{
          if(this.yesterdaywater > 0){
            return "-" + 100 + "%"
          }else{
            return 0 + "%"
          }
        }
         }else if(this.kind==='电'){
        if(this.todaydayelectric > 0){
          var compare = (this.todaydayelectric - this.yesterdayelectric) / this.todaydayelectric * 100
          if(this.todaydayelectric - this.yesterdayelectric > 0){
            return "+" + compare.toFixed(2) + "%"
          }else{
            return compare.toFixed(2) + "%"
          }
        }else{
          if(this.yesterdayelectric > 0){
            return "-" + 100 + "%"
          }else{
            return 0 + "%"
          }
        }
         }else{
        if(this.todaysteam > 0){
          var compare = (this.todaysteam - this.yesterdaysteam) / this.todaysteam * 100
          if(this.todaysteam - this.yesterdaysteam > 0){
            return "+" + compare.toFixed(2) + "%"
          }else{
            return compare.toFixed(2) + "%"
          }
        }else{
          if(this.yesterdaysteam > 0){
            return "-" + 100 + "%"
          }else{
            return 0 + "%"
          }
        }
         }
      }
    },
    methods:{
    getInitMessage(){
        this.loading=true
        var nowTime = moment().format('HH:mm').substring(0,4) + "0"
        var todayStartTime = moment().format('YYYY-MM-DD') + " 00:00"
        var todayEndTime = moment().format('YYYY-MM-DD') + " " + nowTime
        var params={}
        var params1={}
        params.StartTime = todayStartTime
        params.EndTime = todayEndTime
        params.Area = 'GMP车间'
        params1.AreaName='GMP车间'
        params1.StartTime=todayStartTime
        params1.EndTime=todayEndTime
        this.$http.all([
            this.$http.get("/api/energywater",{params: params}),
            this.$http.get('/api/batchMaintainEnergy',{params:params1}),
            this.$http.get('/api/areatimeenergycount',{params:{EnergyClass:'水',CompareTime:moment().format('YYYY-MM-DD')}}),
            // this.$http.get('api/energyall',{params:{ModelFlag:"在线检测情况"}})
        ]).then((this.$http.spread((res1,res2,res3)=>{
            this.loading=false
            this.area=[]
            this.chartData.rows=res3.data.rows.slice(0, 4)
            for(var i=0;i<res3.data.rows.length;i++){
                this.area.push(res3.data.rows[i]['区域'])
            }
           this.kindnum=JSON.parse(res1.data).value
           this.unit=JSON.parse(res1.data).unit
           this.cost=JSON.parse(res1.data).cost
           this.batchCount=res2.data.batchCount
           this.waterCon=res2.data.waterCon
           this.steamCon=res2.data.steamCon
           this.steamEveryBatch=res2.data.steamEveryBatch
           this.waterEveryBatch=res2.data.waterEveryBatch
        }
        )))
    },
    onChange(picker, value) {
      this.loading=true
      this.AreaName=value
      var nowTime = moment().format('HH:mm').substring(0,4) + "0"
        var todayStartTime = moment().format('YYYY-MM-DD') + " 00:00"
        var todayEndTime = moment().format('YYYY-MM-DD') + " " + nowTime
        var yesterdayStartTime = moment().subtract(1,'day').format('YYYY-MM-DD') + " 00:00"
        var yesterdayEndTime = moment().subtract(1,'day').format('YYYY-MM-DD') + " " + nowTime
        var monthStartTime = moment().month(moment().month()).startOf('month').format('YYYY-MM-DD HH:mm:ss')
        var yearStartTime = moment().year(moment().year()).startOf('year').format('YYYY-MM-DD HH:mm:ss')
        var monthEndTime = moment().month(moment().month()).endOf('month').format('YYYY-MM-DD HH:mm:ss')
        var params={}
        var yesterdayParams={}
        yesterdayParams.StartTime = yesterdayStartTime
        yesterdayParams.EndTime = yesterdayEndTime
        yesterdayParams.Area = this.AreaName
        if(this.kind==='水'){
            this.myapi='/energywater'
        }else if(this.kind==='电'){
             this.myapi='/energyelectric'
        }else{
             this.myapi='/energysteam'
        }
        if(this.date==='日'){
            params.StartTime=todayStartTime
            params.EndTime = todayEndTime
            params.AreaName = this.AreaName
            yesterdayParams.StartTime = yesterdayStartTime
            yesterdayParams.EndTime = yesterdayEndTime
            yesterdayParams.Area = this.AreaName
        }else if(this.date==='月'){
            params.StartTime=monthStartTime
            params.EndTime = monthEndTime
            params.AreaName = this.AreaName
        }else{
            params.StartTime=yearStartTime
            params.EndTime =moment().format('YYYY-MM-DD HH:mm:ss')
            params.AreaName = this.AreaName
        }
        this.$http.all([
            this.$http.get('api'+this.myapi,{params: params}),
            this.$http.get('/api/batchMaintainEnergy',{params:params}),
            this.$http.get("/api/energywater",{params: yesterdayParams}),
            this.$http.get("/api/energyelectric",{params: yesterdayParams}),
            this.$http.get("/api/energysteam",{params: yesterdayParams}),
            this.$http.get("/api/energywater",{params: params}),
            this.$http.get("/api/energyelectric",{params: params}),
            this.$http.get("/api/energysteam",{params: params}),
        ]).then((this.$http.spread((res1,res2,res3,res4,res5,res6,res7,res8)=>{
          this.loading=false
          this.batchCount=res2.data.batchCount
          this.steamCon=res2.data.steamCon
          this.steamEveryBatch=res2.data.steamEveryBatch
          this.waterCon=res2.data.waterCon
          this.waterEveryBatch=res2.data.waterEveryBatch
          this.kindnum=JSON.parse(res1.data).value
          this.unit=JSON.parse(res1.data).unit
          this.cost=JSON.parse(res1.data).cost
          this.yesterdaywater=JSON.parse(res3.data).value
          this.yesterdayelectric=JSON.parse(res4.data).value
          this.yesterdaysteam=JSON.parse(res5.data).value
          this.todaydaywater=JSON.parse(res6.data).value
          this.todaydayelectric=JSON.parse(res7.data).value
          this.todaysteam=JSON.parse(res8.data).value
        }
        )))
    },
    ChooseKind(e){
     this.kind=this.kindall[e]
     var comparetime = moment().format('YYYY-MM-DD')
     var params={}
     params.EnergyClass=this.kind
     params.CompareTime=comparetime
     this.$http.get('/api/areatimeenergycount',{params:params}).then((res) => {
        this.unit=res.data.unit
        this.chartData.rows=res.data.rows.slice(0, 4)
     })
    },
    ChooseDate(e){
     this.date=this.dateall[e]
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
               font-size: 22px;
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
    .show-foot{
            position: relative;
            height:64px;
            background:@bgca;
            opacity:1;
            border-radius:4px;
            background-color:@bgcc;
            .sf-l{
                position: absolute;
                left:0;
                top:0;
                width: 196px;
                height: 64px;
                border-radius: 4px;
                background-color: @bgct;
                .hf{
                    position: absolute;
                    top:8px;
                    left: 13px;
                    height:11px;
                    font-size:8px;
                    font-weight:400;
                    line-height:11px;
                    color:rgba(255,255,255,1);
                    opacity:1;
                }
                .all-money{
                    position: absolute;
                    left:16px;
                    top:28px;
                    height:23px;
                    font-size: 18px;
                    color:rgba(255,255,255,1);
                    span{
                        font-size: 12px;
                        margin-left: 5px;
                        }
                }

            }
            .sf-r{
                position: absolute;
                right: 0;
                top:0;
                width:141px;
                height: 64px;
                border-radius: 4px;
                background-color:@bgct;
                .machine{
                    position: absolute;
                    top:8px;
                    left: 12px;
                    height:11px;
                    font-size:8px;
                    font-weight:400;
                    line-height:11px;
                    color:rgba(255,255,255,1);
                }
                .tj{
                    position: absolute;
                    left: 13px;
                    top: 28px;
                    font-size: 23px;
                    font-weight: 500;
                    color: #fff;
                    letter-spacing: 5px;
                }
            }
        }
    }
    .maxcolor{
        color:red;
    }
    .mincolor{
        color:green;
    }
</style>