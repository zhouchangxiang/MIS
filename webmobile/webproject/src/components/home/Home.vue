<template>
    <div class="show-box">
        <div class="show-top">
               <div class="tips">
                   <van-tabs type="card" title-active-color="#1E222B"  title-inactive-color="#fff" v-model="choosekind" @click="ChooseKind($event)">
                        <van-tab title="水"></van-tab>
                        <van-tab title="电"></van-tab>
                        <van-tab title="气"></van-tab>
                    </van-tabs>
               </div>
        </div>
        <van-loading size="24px" vertical v-if="loading" color="rgb(69, 135, 221)" type="spinner">加载中...</van-loading>
        <div class="show-banner">
            <div class="day-tab">
                  <div class="sb-name">厂区{{kind}}日总能耗</div>
                  <div class="sb-number">{{valueall1}}</div>
                  <div class="sb-dw">单位</div>
                  <div class="sb-t">{{unit}}</div>
                  <div class="sb-compare">较昨日</div>
                  <div class="sb-l-n" :class="todayCon-compareDateCon>0?'maxcolor':'mincolor'" >{{dayCompare}}</div>
                  <div class="compare-last">昨日同期</div>
                  <div class="compare-text">{{compareDateCon}}</div>
            </div>
            <div class="month-tab">
                  <div class="sb-name">厂区{{kind}}月总能耗</div>
                  <div class="sb-number">{{valueall2}}</div>
                  <div class="sb-dw">单位</div>
                  <div class="sb-t">{{unit}}</div>
                  <div class="sb-compare">较上月</div>
                  <div class="sb-l-n" :class="thisMonthCon-lastMonthCon>0?'maxcolor':'mincolor'">{{monthCompare}}</div>
                  <div class="compare-last">上月同期</div>
                  <div class="compare-text">{{lastMonthCon}}</div>
            </div>
            <div class="year-tab">
                  <div class="sb-name">厂区{{kind}}年总能耗</div>
                  <div class="sb-number">{{valueall3}}</div>
                  <div class="sb-dw">单位</div>
                  <div class="sb-t">{{unit}}</div>
                  <div class="sb-compare">较去年</div>
                  <div class="sb-l-n" :class="thisYearCon-lastYearCon>0?'maxcolor':'mincolor'">{{yearCompare}}</div>
                  <div class="compare-last">上年同期</div>
                  <div class="compare-text">{{lastYearCon}}</div>
            </div>
                <div class="tabbar1">
                     <ve-line :data="vlchartData1" width="350px" height="200px" :legend-visible="true"  :extend="lineChartExtend" :settings="chartSettings"></ve-line>
                 </div>
                  <div class="tabbar2">
                     <ve-line :data="vlchartData2" width="350px" height="200px" :legend-visible="true"  :extend="lineChartExtend" :settings="chartSettings"></ve-line>
                 </div>
           </div>
          <div class="show-foot">
               <div class="sf-l">
                   <div class="hf">耗费成本</div>
                   <div class="all-money">{{costall}}<span>元</span></div>
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
export default {
    data(){
        this.chartSettings = {
                yAxisType: ['KMB']
            }
        return {
            lineChartExtend:{
            grid:{
                    left:'-1px',
                    right:'16px',
                    bottom:'5px',
                    top:'30px'
            },
             series:{
                    smooth: false
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
            area:['原提取车间','GMP车间','固体制剂车间','中试车间'],
            loading:false,
            vlchartData1: {
                columns: ['时间', '今日能耗', '对比日能耗'],
                rows: [
                    { '时间': '01', '今日能耗': 1393, '对比日能耗': 1093}
                ]
                },
            vlchartData2: {
            columns: ['日期', '本月能耗', '上月能耗'],
            rows: [
                { '日期':'01','本月能耗':234,'上月能耗': 100}
            ]
            },
            choosekind:0,
            kindall:['水','电','汽'],
            kind:'水',
            unit:'t',
            valueall1:0,
            valueall2:0,
            valueall3:0,
            costall:0,
            todaydaywater:0,
            todaydayelectric:0,
            CompareDate:Date.now() - 3600 * 1000 * 24, //默认对比日期
            onlineitem:{online:0,total:0},
            myapi:'',
            todayCon:0,
            compareDateCon:0,
            thisMonthCon:0,
            lastMonthCon:0,
            thisYearCon:0,
            lastYearCon:0,
            water1:{},
            water2:{},
            water3:{},
            electric1:{},
            electric2:{},
            electric3:{},
            steam1:{},
            steam2:{},
            steam3:{},
            waterGG:0,
            waterYY:0,
            waterSJ:0,
            waterGGcost:0,
            waterYYcost:0,
            waterSJcost:0,
            onlineAll:[]
        }
    },
    created(){
        this.getInitMessage()
    },
    computed:{
        dayCompare(){
        if(this.todayCon > 0){
          var compare = (this.todayCon - this.compareDateCon) / this.todayCon * 100
          if(this.todayCon - this.compareDateCon > 0){
            return "+" + compare.toFixed(2) + "%"
          }else{
            return compare.toFixed(2) + "%"
          }
        }else{
          if(this.compareDateCon > 0){
            return "-" + 100 + "%"
          }else{
            return 0 + "%"
          }
        }
         },
        monthCompare(){
         if(this.thisMonthCon > 0){
          var compare = (this.thisMonthCon - this.lastMonthCon) / this.thisMonthCon * 100
          if(this.thisMonthCon - this.lastMonthCon > 0){
            return "+" + compare.toFixed(2) + "%"
          }else{
            return compare.toFixed(2) + "%"
          }
        }else{
          if(this.lastMonthCon > 0){
            return "-" + 100 + "%"
          }else{
            return 0 + "%"
          }
        }
        },
        yearCompare(){
        if(this.thisYearCon > 0){
          var compare = (this.thisYearCon - this.lastYearCon) / this.thisYearCon * 100
          if(this.thisYearCon - this.lastYearCon > 0){
            return "+" + compare.toFixed(2) + "%"
          }else{
            return compare.toFixed(2) + "%"
          }
        }else{
          if(this.lastYearCon > 0){
            return "-" + 100 + "%"
          }else{
            return 0 + "%"
          }
        }
        }
    },
    methods:{
        getallPreview(){
            this.$http.get('/api/energyall',{
            params: {ModelFlag: "能耗预览",CompareDate:moment(this.CompareDate).format('YYYY-MM-DD'),EnergyClass:this.kind}
            }).then((res) => {
               var arr1=JSON.parse(res.data).compareTodayRow
               var arr2=JSON.parse(res.data).lastMonthRow
               this.vlchartData1.rows=[]
               this.vlchartData2.rows=[]
               for(var i=0;i<arr1.length;i++){
                    this.vlchartData1.columns=['时间', '今日能耗', '对比日能耗']
                    this.vlchartData1.rows.push({'时间':arr1[i]['时间'].slice(-2),'今日能耗':arr1[i]['今日能耗'],'对比日能耗':arr1[i]['对比日能耗']})
               }
               for(var i=0;i<arr2.length;i++){
                   this.vlchartData2.columns=['日期', '本月能耗', '上月能耗']
                   this.vlchartData2.rows.push({'日期':arr2[i]['日期'].slice(-2),'本月能耗':arr2[i]['本月能耗'],'上月能耗':arr2[i]['上月能耗']})
               }
            })
        },
        getInitMessage(){
            this.getAllMessage()
            this.getallPreview()
        },
        getAllMessage(e) {
        this.loading=true
        this.AreaName=''
        var nowTime = moment().format('HH:mm').substring(0,4) + "0"
        var nowDate = moment().format('MM-DD') + " " + nowTime
        var thisDate = moment().format('DD')
        var todayStartTime = moment().format('YYYY-MM-DD') + " 00:00"
        var todayEndTime = moment().format('YYYY-MM-DD') + " " + nowTime
        var compareDateStartTime = moment(this.CompareDate).format('YYYY-MM-DD') + " 00:00"
        var compareDateEndTime = moment(this.CompareDate).format('YYYY-MM-DD') + " " + nowTime
        var yesterdayStartTime = moment().subtract(1,'day').format('YYYY-MM-DD') + " 00:00"
        var yesterdayEndTime = moment().subtract(1,'day').format('YYYY-MM-DD') + " " + nowTime
        var monthStartTime = moment().month(moment().month()).startOf('month').format('YYYY-MM-DD HH:mm:ss')
        var monthEndTime = moment().month(moment().month()).endOf('month').format('YYYY-MM-DD HH:mm:ss')
        var lastStartMonth = moment().month(moment().month() - 1).startOf('month').format('YYYY-MM-DD HH:mm')
        var lastEndMonth = moment().month(moment().month() - 1).endOf('month').format('YYYY-MM-DD').substring(0,7) + "-" + thisDate + " " + nowTime
        var yearStartTime = moment().year(moment().year()).startOf('year').format('YYYY-MM-DD HH:mm:ss')
        var lastStartYear = moment().year(moment().year() - 1).startOf('year').format('YYYY-MM-DD HH:mm')
        var lastEndYear = moment().year(moment().year() - 1).endOf('year').format('YYYY-MM-DD HH:mm')
        var params1={StartTime:todayStartTime,EndTime:todayEndTime,AreaName:this.AreaName}
        var params2={StartTime:monthStartTime,EndTime:monthEndTime,AreaName:this.AreaName}
        var params3={StartTime:yearStartTime,EndTime:moment().format('YYYY-MM-DD HH:mm:ss'),AreaName:this.AreaName}
        var api=''
          if(!moment(lastEndMonth)._isValid){  //判断上月结束日期是否合法，否则赋值为上月最后一天的23：59
            lastEndMonth = moment().month(moment().month() - 1).endOf('month').format('YYYY-MM-DD HH:mm');
          }
        this.$http.all([
            this.$http.get('/api/energywater',{params:params1}),//今天水
            this.$http.get('/api/energywater',{params:params2}),
            this.$http.get('/api/energywater',{params:params3}),
            this.$http.get('/api/energyelectric',{params:params1}),//今天电
            this.$http.get('/api/energyelectric',{params:params2}),
            this.$http.get('/api/energyelectric',{params:params3}),
            this.$http.get('/api/energysteam',{params:params1}),//今天汽
            this.$http.get('/api/energysteam',{params:params2}),
            this.$http.get('/api/energysteam',{params:params3}),
            this.$http.get('/api/energywater',{params: {StartTime: compareDateStartTime,EndTime:compareDateEndTime}}),//获取水对比天能耗
            this.$http.get('/api/energyelectric',{params: {StartTime: compareDateStartTime,EndTime:compareDateEndTime}}),//获取电对比天能耗
            this.$http.get('/api/energysteam',{params: {StartTime: compareDateStartTime,EndTime:compareDateEndTime}}),//获取汽对比天能耗
            this.$http.get('/api/energywater',{params: {StartTime: lastStartMonth,EndTime:lastEndMonth}}),//获取水上月能耗
            this.$http.get('/api/energyelectric',{params: {StartTime: lastStartMonth,EndTime:lastEndMonth}}),//获取电上月能耗
            this.$http.get('/api/energysteam',{params: {StartTime: lastStartMonth,EndTime:lastEndMonth}}),//获取汽上月能耗
            this.$http.get("/api/souyeselectyear",{params:{StartTime: lastStartYear,EndTime:lastEndYear,EnergyClass:'水'}}),//上一年水能耗
            this.$http.get("/api/souyeselectyear",{params:{StartTime: lastStartYear,EndTime:lastEndYear,EnergyClass:'电'}}),//上一年电能耗
            this.$http.get("/api/souyeselectyear",{params:{StartTime: lastStartYear,EndTime:lastEndYear,EnergyClass:'汽'}}),//上一年汽能耗
            this.$http.get('api/energyall',{params:{ModelFlag:"在线检测情况"}})
        ]).then((this.$http.spread((water1,water2,water3,electric1,electric2,electric3,steam1,steam2,steam3,dwdc,delc,dste,mwdc,melc,mste,ywdc,yelc,yste,onlin)=>{
         this.onlineAll=(JSON.parse(onlin.data))
          this.water1=JSON.parse(water1.data)
          this.water2=JSON.parse(water2.data)
          this.water3=JSON.parse(water3.data)
          this.electric1=JSON.parse(electric1.data)
          this.electric2=JSON.parse(electric2.data)
          this.electric3=JSON.parse(electric3.data)
          this.steam1=JSON.parse(steam1.data)
          this.steam2=JSON.parse(steam2.data)
          this.steam3=JSON.parse(steam3.data)
          this.dwdc=JSON.parse(dwdc.data).value
          this.delc=JSON.parse(delc.data).value
          this.dste=JSON.parse(dste.data).value
          this.mwdc=JSON.parse(mwdc.data).value
          this.melc=JSON.parse(melc.data).value
          this.mste=JSON.parse(mste.data).value      
          this.ywdc=ywdc.data.value
          this.yelc=yelc.data.value
          this.yste=yste.data.value
          this.loading=false
          this.valueall1=this.water1.value
          this.valueall2=this.water2.value
          this.valueall3=this.water3.value
          this.todayCon=this.water1.value
          this.compareDateCon=this.dwdc
          this.thisMonthCon=this.water2.value
          this.lastMonthCon=this.mwdc
          this.thisYearCon = this.water3.value
          this.lastYearCon = this.ywdc
          this.unit='t'
          this.costall=this.water1.cost //水的的能耗成本
          this.onlineitem=this.onlineAll[1]
        }
        )))
    },
    ChooseKind(e){
     this.kind=this.kindall[e]
     this.getallPreview()
         if(this.kind==='水'){
          this.valueall1=this.water1.value
          this.valueall2=this.water2.value
          this.valueall3=this.water3.value
          this.todayCon=this.water1.value
          this.compareDateCon=this.dwdc
          this.thisMonthCon=this.water2.value
          this.lastMonthCon=this.mwdc
          this.thisYearCon = this.water3.value
          this.lastYearCon = this.ywdc
          this.unit='t'
          this.costall=this.water1.cost  //水的的能耗成本
          this.onlineitem=this.onlineAll[1]
         }else if(this.kind==='电'){
          this.valueall1=this.electric1.value
          this.valueall2=this.electric2.value
          this.valueall3=this.electric3.value
          this.todayCon=this.electric1.value
          this.compareDateCon=this.delc
          this.thisMonthCon=this.electric2.value
          this.lastMonthCon=this.melc
          this.thisYearCon = this.electric3.value
          this.lastYearCon = this.yelc
          this.unit='KWh'
          this.costall=this.electric1.cost
          this.onlineitem=this.onlineAll[0]
         }else{
          this.valueall1=this.steam1.value
          this.valueall2=this.steam2.value
          this.valueall3=this.steam3.value
          this.todayCon=this.steam1.value
          this.compareDateCon=this.dste 
          this.thisMonthCon=this.steam2.value
          this.lastMonthCon=this.mste
          this.thisYearCon = this.steam3.value
          this.lastYearCon = this.yste
          this.unit='t'
          this.costall=this.steam1.cost
          this.onlineitem=this.onlineAll[2]
         }
    }
            }
}
</script>
<style lang="less" scoped>
    @bgca:#3D4048FF;
    @bgcc:#eee;
    @bgct:#eee;
    span{
        text-align: center;
    }
     .show-box{
        position: relative;
        width: 375px;
        height:1200px;
        box-sizing: border-box;
        padding: 0 12px 12px 13px;
        background-color: @bgcc;
        .show-banner{
            position: relative;
            width:350px;
            height:1000px;
            overflow: hidden;
            font-family:PingFang SC;
            box-sizing: border-box;
            background:#eee;
            box-shadow:0px 0px 6px rgba(255,255,255,0.16);
            opacity:1;
            border-radius:4px;
            margin:2px 0 20px 0;
            .day-tab{
                position: relative;
                width: 350px;
                height: 160px;
                background-color: #eee;
                border-bottom: 0.5px solid #000;
            }
            .month-tab{
                .day-tab()
            }
            .year-tab{
                .day-tab()
            }
           .tabbar1{
                position: absolute;
                top:500px;
                left:5px;
                width: 340px;
                height: 220px;
            }
            .tabbar2{
                .tabbar1();
                top:750px;
            }
        }
           .sb-name{
               position: absolute;
               top:14px;
               left: 15px;
               height:20px;
               font-size:14px;
               font-weight:400;
               line-height:20px;
               color:#111;
               opacity:1;
           }
           .sb-number{
               position: absolute;
               left:13px;
               top:40px;
               font-size: 22px;
               word-spacing: 20px;
               height:36px;
               color:#333;
               opacity:1;

           }
           .sb-compare{
               position: absolute;
               left: 200px;
               top: 90px;
               height:11px;
               font-size:8px;
               font-weight:400;
               line-height:11px;
               color:#000;
               opacity:1; 
           }
           .compare-last{
               position: absolute;
               left: 13px;
               top: 90px;
               height:11px;
               font-size:8px;
               font-weight:400;
               line-height:11px;
               color:#000;
               opacity:1; 
           }
           .compare-text{
               position: absolute;
               left: 13px;
               top: 120px;
               height:11px;
               font-size:16px;
               font-weight:400;
               line-height:11px;
               color:#333;
               opacity:1;  
           }
           .sb-l-n{
               position: absolute;
               left:200px;
               top:120px;
               height:17px;
               font-size:12px;
               font-weight:500;
               line-height:17px;
               opacity:1;
           }
          .sb-dw{
            position: absolute;
            top:18px;
            left:200px;
            height:11px;
            font-size:8px;
            font-weight:400;
            line-height:11px;
            color:#000;
            opacity:1;
            }
            .sb-t{
                position: absolute;
                left:205px;
                top:48px;
                width:7px;
                height:17px;
                font-size:12px;
                font-weight:500;
                line-height:17px;
                color:#000;
                opacity:1;
            }
        .show-body{
            position: relative;
            height:80px;
            opacity:1;
            border-radius:4px;
            margin-bottom: 13px;
            .sb-l{
                position: absolute;
                top:0;
                left:0;
                width: 100%;
                height:80px;
                background:#eee;
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
                    color:#000;
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
                    top:9px;
                    left:100px;
                    font-size: 8px;
                    color: #000;
                }
                .znhl-s{
                    position: absolute;
                    top:30px;
                    left: 100px;
                    width:17px;
                    height:25px;
                    font-size: 23px;
                    color:#fff;
                    opacity:1;
                }
                .dwnh{
                    position: absolute;
                    top:9px;
                    left:210px;
                    font-size: 8px;
                    color: #000;
                }
                .dwnh-s{
                    position: absolute;
                    top:30px;
                    left: 240px;
                    width:17px;
                    height:25px;
                    font-size: 23px;
                    color:#00FAE7;
                    opacity:1;
                }
                .dw-kwh{
                    position: absolute;
                    left: 150px;
                    top:9px;
                    font-size: 8px;
                    font-weight: 500;
                    color: #eee;
                }
                .dw-pc{
                    position: absolute;
                    left: 290px;
                    top:9px;
                    font-size: 8px;
                    font-weight: 500;
                    color: #eee;
                }
            }
        }
        .show-top{
            height:18px;
            opacity:1;
            border-radius:4px;
            color:#eee;
            font-size: 10px;
            padding-top:10px;
            .tips{
                float: left;
                margin-right: 10px;
                border-radius: 5px;
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
                background-color: #ccc;
                .hf{
                    position: absolute;
                    top:8px;
                    left: 13px;
                    height:11px;
                    font-size:8px;
                    font-weight:400;
                    line-height:11px;
                    color:#000;
                    opacity:1;
                }
                .all-money{
                    position: absolute;
                    left:16px;
                    top:28px;
                    height:23px;
                    font-size: 18px;
                    color:#000;
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
                background-color:#ccc;
                .machine{
                    position: absolute;
                    top:8px;
                    left: 12px;
                    height:11px;
                    font-size:8px;
                    font-weight:400;
                    line-height:11px;
                    color:#000;
                }
                .tj{
                    position: absolute;
                    left: 13px;
                    top: 28px;
                    font-size: 23px;
                    font-weight: 500;
                    color: #000;
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