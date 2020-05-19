<template>
    <div class="show-box">
        <div class="show-top">
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
        <div class="tips bannertips">
                <van-tabs type="card" title-active-color="#1E222B"  title-inactive-color="#fff" v-model="banner" @click="Choosebanner($event)">
                        <van-tab title="区域总能耗"></van-tab>
                        <van-tab :title="AreaName"></van-tab>
                </van-tabs>
        </div>
        <van-loading size="24px" vertical v-if="loading" color="lightgreen" type="spinner">加载中...</van-loading>
        <div class="show-banner" v-if="banner===0">
                  <div class="sb-name">厂区{{kind}}总能耗</div>
                  <div class="sb-number">{{kindnum}}</div>
                  <div class="sb-compare">较上期</div>
                  <div class="sb-l-n" :class="todayCon-compareDateCon>0?'maxcolor':'mincolor'"  v-if="this.date==='日'">{{dayCompare}}</div>
                  <div class="sb-l-n" :class="thisMonthCon-lastMonthCon>0?'maxcolor':'mincolor'" v-if="this.date==='月'">{{monthCompare}}</div>
                  <div class="sb-l-n" :class="thisYearCon-lastYearCon>0?'maxcolor':'mincolor'" v-if="this.date==='年'">{{yearCompare}}</div>
                  <div class="sb-dw">单位</div>
                  <div class="sb-t">{{unit}}</div>
                  <div class="tabbar">
                     <ve-line :data="mychartData" width="350px" height="200px" :legend-visible="true"  :extend="lineChartExtend"></ve-line>
                 </div>
           </div>
           <div class="current-Area"  v-if="banner===1">
                  <div class="sb-name">{{AreaName}}--{{kind}}总能耗</div>
                  <div class="sb-number">{{kindnum}}</div>
                  <div class="sb-compare">较上期</div>
                  <div class="sb-l-n" :class="todayCon-compareDateCon>0?'maxcolor':'mincolor'"  v-if="this.date==='日'">{{dayCompare}}</div>
                  <div class="sb-l-n" :class="thisMonthCon-lastMonthCon>0?'maxcolor':'mincolor'" v-if="this.date==='月'">{{monthCompare}}</div>
                  <div class="sb-l-n" :class="thisYearCon-lastYearCon>0?'maxcolor':'mincolor'" v-if="this.date==='年'">{{yearCompare}}</div>
                  <div class="sb-dw">单位</div>
                  <div class="sb-t">{{unit}}</div>
                  <div class="tabbar">
                     <ve-histogram :data="chartData" width="350px" height="200px" :legend-visible="false"  :extend="ChartExtend"></ve-histogram>
                 </div>
                 </div>
           <div class="show-body">
               <div class="sb-l" v-if="this.date==='日'">
                   <div class="scpc">生产批次</div>
                   <div class="scpc-s">{{kind==='电'?0:this.batch1.batchCount}}</div>
                   <div class="znhl">总耗能量</div>
                   <div class="znhl-s">{{kind==='水'?this.batch1.waterCon:(kind==='电'?0:this.batch1.steamCon)}}</div>
                   <div class="dwnh">单位批次能耗</div>
                   <div class="dwnh-s">{{kind==='水'?this.batch1.waterEveryBatch:(kind==='电'?0:this.batch1.steamEveryBatch)}}</div>
                   <div class="dw-kwh">{{unit}}</div>
                   <div class="dw-pc">&nbsp;/&nbsp;批</div>
               </div>
                <div class="sb-l" v-if="this.date==='月'">
                   <div class="scpc">生产批次</div>
                   <div class="scpc-s">{{kind==='电'?0:this.batch2.batchCount}}</div>
                   <div class="znhl">总耗能量</div>
                   <div class="znhl-s">{{kind==='水'?this.batch2.waterCon:(kind==='电'?0:this.batch2.steamCon)}}</div>
                   <div class="dwnh">单位批次能耗</div>
                   <div class="dwnh-s">{{kind==='水'?this.batch2.waterEveryBatch:(kind==='电'?0:this.batch2.steamEveryBatch)}}</div>
                   <div class="dw-kwh">{{unit}}</div>
                   <div class="dw-pc">&nbsp;/&nbsp;批</div>
               </div>
                <div class="sb-l" v-if="this.date==='年'">
                   <div class="scpc">生产批次</div>
                   <div class="scpc-s">{{kind==='电'?0:this.batch3.batchCount}}</div>
                   <div class="znhl">总耗能量</div>
                   <div class="znhl-s">{{kind==='水'?this.batch3.waterCon:(kind==='电'?0:this.batch3.steamCon)}}</div>
                   <div class="dwnh">单位批次能耗</div>
                   <div class="dwnh-s">{{kind==='水'?this.batch3.waterEveryBatch:(kind==='电'?0:this.batch3.steamEveryBatch)}}</div>
                   <div class="dw-kwh">{{unit}}</div>
                   <div class="dw-pc">{{unit}}&nbsp;/&nbsp;批</div>
               </div>
               <div class="sb-r">
                    <van-picker :columns="area" @change="onChange" :default-index="9"/>
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
            lineChartExtend:{
            grid:{
                    left:'0',
                    right:'0',
                    bottom:'0px',
                    top:'30px'
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
            chartData: {
            columns: ['区域', '能耗量'],
            rows: [
                { '区域': '污水站', '能耗量': 100},
                { '区域': '前提取车间', '能耗量': 100},
                { '区域': '二车间', '能耗量': 100},
                { '区域': '综合车间', '能耗量': 100}
            ]
            },
            mychartData: {
                columns: ['日期', '今天数值', '昨天数值'],
                rows: [
                    { '日期': '1/1', '今天数值': 1393, '昨天数值': 1093},
                    { '日期': '1/2', '今天数值': 3530, '昨天数值': 3230},
                    { '日期': '1/3', '今天数值': 2923, '昨天数值': 2623},
                    { '日期': '1/4', '今天数值': 1723, '昨天数值': 1423},
                    { '日期': '1/5', '今天数值': 3792, '昨天数值': 3492},
                    { '日期': '1/6', '今天数值': 4593, '昨天数值': 4293}
                ]
                },
            choosedate:0,
            choosekind:0,
            banner:1,
            kindall:['水','电','汽'],
            dateall:['年','月','日'],
            kind:'水',
            date:'年',
            unit:'t',
            cost:0,
            kindnum:0,
            todaydaywater:0,
            todaydayelectric:0,
            CompareDate:Date.now() - 3600 * 1000 * 24, //默认对比日期
            AreaName:'综合车间',
            batchCount:0,
            steamCon:0,
            waterCon:0,
            steamEveryBatch:0,
            waterEveryBatch:0,
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
            batch1:{batchCount:0,steamCon:'0',steamEveryBatch:'0',waterCon:'0',waterEveryBatch:'0'},
            batch2:{batchCount:0,steamCon:'0',steamEveryBatch:'0',waterCon:'0',waterEveryBatch:'0'},
            batch3:{batchCount:0,steamCon:'0',steamEveryBatch:'0',waterCon:'0',waterEveryBatch:'0'}
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
    getInitMessage(){
        this.loading=true
        var nowTime = moment().format('HH:mm').substring(0,4) + "0"
        var todayStartTime = moment().format('YYYY-MM-DD') + " 00:00"
        var todayEndTime = moment().format('YYYY-MM-DD') + " " + nowTime
        var params={}
        var params1={}
        params.StartTime = todayStartTime
        params.EndTime = todayEndTime
        params.Area = '综合车间'
        params1.AreaName='综合车间'
        params1.StartTime=todayStartTime
        params1.EndTime=todayEndTime
        this.$http.all([
            this.$http.get("/api/energywater",{params: params}),
            this.$http.get('/api/batchMaintainEnergy',{params:params1}),
            this.$http.get('/api/areatimeenergycount',{params:{EnergyClass:'水',CompareTime:moment().format('YYYY-MM-DD')}}),
            // this.$http.get('api/energyall',{params:{ModelFlag:"在线检测情况"}})
            this.$http.get("/api/energyelectric",{params: params}),
            this.$http.get("/api/energysteam",{params: params})
        ]).then((this.$http.spread((res1,res2,res3,res4,res5)=>{
            this.loading=false
            this.water1=this.water2=this.water3=JSON.parse(res1.data)
            this.electric1=this.electric2=this.electric3=JSON.parse(res4.data)
            this.steam1=this.steam2=this.steam3=JSON.parse(res5.data)
            this.area=[]
            this.chartData.rows=res3.data.rows
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
        var params1={}
        var params2={}
        var params3={}
        var myparams={}
         if(this.kind==='水'){
            this.myapi='/energywater'
        }else if(this.kind==='电'){
             this.myapi='/energyelectric'
        }else{
             this.myapi='/energysteam'
        }
        if(this.date==='日'){
            myparams.StartTime=todayStartTime
            myparams.EndTime = todayEndTime
            myparams.AreaName = this.AreaName
        }else if(this.date==='月'){
            myparams.StartTime=monthStartTime
            myparams.EndTime = monthEndTime
            myparams.AreaName = this.AreaName
        }else{
            myparams.StartTime=yearStartTime
            myparams.EndTime =moment().format('YYYY-MM-DD HH:mm:ss')
            myparams.AreaName = this.AreaName
        }
            params1.StartTime=todayStartTime
            params1.EndTime = todayEndTime
            params1.AreaName = this.AreaName
            params2.StartTime=monthStartTime
            params2.EndTime = monthEndTime
            params2.AreaName = this.AreaName
            params3.StartTime=yearStartTime
            params3.EndTime =moment().format('YYYY-MM-DD HH:mm:ss')
            params3.AreaName = this.AreaName
        this.$http.all([
            this.$http.get('api'+this.myapi,{params: myparams}),//当前年月日水电气数据
            this.$http.get('/api/batchMaintainEnergy',{params:myparams}),
            this.$http.get('/api/energywater',{params:params1}),//今天水
            this.$http.get('/api/energywater',{params:params2}),
            this.$http.get('/api/energywater',{params:params3}),
            this.$http.get('/api/energyelectric',{params:params1}),//今天电
            this.$http.get('/api/energyelectric',{params:params2}),
            this.$http.get('/api/energyelectric',{params:params3}),
            this.$http.get('/api/energysteam',{params:params1}),//今天汽
            this.$http.get('/api/energysteam',{params:params2}),
            this.$http.get('/api/energysteam',{params:params3}),
            this.$http.get('/api/batchMaintainEnergy',{params:params1}),//今天批次
            this.$http.get('/api/batchMaintainEnergy',{params:params2}),
            this.$http.get('/api/batchMaintainEnergy',{params:params3}),
        ]).then((this.$http.spread((res1,res2,water1,water2,water3,electric1,electric2,electric3,steam1,steam2,steam3,batch1,batch2,batch3)=>{
          this.loading=false
          this.batchCount=res2.data.batchCount
          this.steamCon=res2.data.steamCon
          this.steamEveryBatch=res2.data.steamEveryBatch
          this.waterCon=res2.data.waterCon
          this.waterEveryBatch=res2.data.waterEveryBatch
          this.kindnum=JSON.parse(res1.data).value
          this.unit=JSON.parse(res1.data).unit
          this.cost=JSON.parse(res1.data).cost
          this.water1=JSON.parse(water1.data)
          this.water2=JSON.parse(water2.data)
          this.water3=JSON.parse(water3.data)
          this.electric1=JSON.parse(electric1.data)
          this.electric2=JSON.parse(electric2.data)
          this.electric3=JSON.parse(electric3.data)
          this.steam1=JSON.parse(steam1.data)
          this.steam2=JSON.parse(steam2.data)
          this.steam3=JSON.parse(steam3.data)
          this.batch1=batch1.data
          this.batch2=batch2.data
          this.batch3=batch3.data
        }
        )))
    },
    ChooseKind(e){
     this.kind=this.kindall[e]
     var comparetime =''
     var thisDate = moment().format('DD')
     var lastMonth = moment().month(moment().month() - 1).endOf('month').format('YYYY-MM-DD').substring(0,7) + "-" + thisDate
     var lastYear = moment().year(moment().year() - 1).format('YYYY-MM-DD')
     if(this.date==='日'){
         comparetime= moment(this.CompareDate).format('YYYY-MM-DD')
         if(this.kind==='水'){
          this.kindnum=this.water1.value
          this.cost=this.water1.cost
         }else if(this.kind==='电'){
          this.kindnum=this.electric1.value
          this.cost=this.electric1.cost
         }else{
          this.kindnum=this.steam1.value
          this.cost=this.steam1.cost
         }
     }else if(this.date==='月'){
         comparetime= lastMonth
          if(this.kind==='水'){
          this.kindnum=this.water2.value
          this.cost=this.water2.cost
         }else if(this.kind==='电'){
          this.kindnum=this.electric2.value
          this.cost=this.electric2.cost
         }else{
          this.kindnum=this.steam2.value
          this.cost=this.steam2.cost
         }
     }else{
         comparetime= lastYear
          if(this.kind==='水'){
          this.kindnum=this.water3.value
          this.cost=this.water3.cost
         }else if(this.kind==='电'){
          this.kindnum=this.electric3.value
          this.cost=this.electric3.cost
         }else{
          this.kindnum=this.steam3.value
          this.cost=this.steam3.cost
         }
     }
     var params={}
     params.EnergyClass=this.kind
     params.CompareTime='2020-04-11'
     this.$http.get('/api/areatimeenergycount',{params:params}).then((res) => {
        this.unit=res.data.unit
        this.chartData.rows=res.data.rows
     })
    },
    ChooseDate(e){
     this.date=this.dateall[e]
      if(this.date==='日'){
         if(this.kind==='水'){
          this.kindnum=this.water1.value
          this.cost=this.water1.cost
         }else if(this.kind==='电'){
          this.kindnum=this.electric1.value
          this.cost=this.electric1.cost
         }else{
          this.kindnum=this.steam1.value
          this.cost=this.steam1.cost
         }
     }else if(this.date==='月'){
          if(this.kind==='水'){
          this.kindnum=this.water2.value
          this.cost=this.water2.cost
         }else if(this.kind==='电'){
          this.kindnum=this.electric2.value
          this.cost=this.electric2.cost
         }else{
          this.kindnum=this.steam2.value
          this.cost=this.steam2.cost
         }
     }else{
          if(this.kind==='水'){
          this.kindnum=this.water3.value
          this.unit=this.water3.unit
          this.cost=this.water3.cost
         }else if(this.kind==='电'){
          this.kindnum=this.electric3.value
          this.unit=this.electric3.unit
          this.cost=this.electric3.cost
         }else{
          this.kindnum=this.steam3.value
          this.unit=this.steam3.unit
          this.cost=this.steam3.cost
         }
     }
     var api=''
     var nowTime = moment().format('HH:mm').substring(0,4) + "0"
     var nowDate = moment().format('MM-DD') + " " + nowTime
     var thisDate = moment().format('DD')
     var todayStartTime = moment().format('YYYY-MM-DD') + " 00:00"
     var todayEndTime = moment().format('YYYY-MM-DD') + " " + nowTime
     var compareDateStartTime = moment(this.CompareDate).format('YYYY-MM-DD') + " 00:00"
     var compareDateEndTime = moment(this.CompareDate).format('YYYY-MM-DD') + " " + nowTime
     var thisStartMonth = moment().month(moment().month()).startOf('month').format('YYYY-MM-DD HH:mm')
     var lastStartMonth = moment().month(moment().month() - 1).startOf('month').format('YYYY-MM-DD HH:mm')
     var lastEndMonth = moment().month(moment().month() - 1).endOf('month').format('YYYY-MM-DD').substring(0,7) + "-" + thisDate + " " + nowTime
     var thisStartYear = moment().year(moment().year()).startOf('year').format('YYYY-MM-DD HH:mm')
     var lastStartYear = moment().year(moment().year() - 1).startOf('year').format('YYYY-MM-DD HH:mm')
     var lastEndYear = moment().year(moment().year() - 1).endOf('year').format('YYYY-MM-DD HH:mm')
        if(!moment(lastEndMonth)._isValid){  //判断上月结束日期是否合法，否则赋值为上月最后一天的23：59
          lastEndMonth = moment().month(moment().month() - 1).endOf('month').format('YYYY-MM-DD HH:mm');
        }
    if(this.kind === "电"){
          api = "/api/energyelectric"
        }else if(this.kind === "水"){
          api = "/api/energywater"
        }else if(this.kind === "汽"){
          api = "/api/energysteam"
        }
         this.$http.all([
          this.$http.get(api,{params: {StartTime: todayStartTime,EndTime:todayEndTime}}),//获取今天能耗
          this.$http.get(api,{params: {StartTime: compareDateStartTime,EndTime:compareDateEndTime}}),//获取对比天能耗
          this.$http.get(api,{params: {StartTime: thisStartMonth,EndTime:todayEndTime}}),//获取本月能耗
          this.$http.get(api,{params: {StartTime: lastStartMonth,EndTime:lastEndMonth}}),//获取上月能耗
          this.$http.get("/api/souyeselectyear",{params:{StartTime: thisStartYear,EndTime:todayEndTime,EnergyClass:this.kind}}),//当年能耗
          this.$http.get("/api/souyeselectyear",{params:{StartTime: lastStartYear,EndTime:lastEndYear,EnergyClass:this.kind}})//上一年能耗
        ]).then(this.$http.spread((todayCon,compareDateCon,thisMonthCon,lastMonthCon,thisYearCon,lastYearCon)=>{
            this.todayCon = JSON.parse(todayCon.data).value
            this.unit = JSON.parse(todayCon.data).unit
            this.compareDateCon = JSON.parse(compareDateCon.data).value
            this.thisMonthCon = JSON.parse(thisMonthCon.data).value
            this.lastMonthCon = JSON.parse(lastMonthCon.data).value
            this.thisYearCon = thisYearCon.data.value
            this.lastYearCon = lastYearCon.data.value
        }))
    },
    Choosebanner(e){
       this.banner=e
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
        height:720px;
        box-sizing: border-box;
        padding: 0 12px 12px 13px;
        background-color: @bgcc;
         .current-Area{
            position: relative;
            width:350px;
            height:290px;
            overflow: hidden;
            font-family:PingFang SC;
            box-sizing: border-box;
            background:rgba(126,127,132,1);
            box-shadow:0px 0px 6px rgba(255,255,255,0.16);
            opacity:1;
            border-radius:4px;
            margin:2px 0 20px 0;
            }
        .show-banner{
           .current-Area()
        }
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
               top:40px;
               font-size: 22px;
               word-spacing: 20px;
               height:36px;
               color:rgba(250,192,0,1);
               opacity:1;

           }
           .sb-compare{
               position: absolute;
               left: 220px;
               top: 18px;
               height:11px;
               font-size:8px;
               font-weight:400;
               line-height:11px;
               color:rgba(255,255,255,1);
               opacity:1; 
           }
           .sb-l-n{
               position: absolute;
               left:220px;
               top:48px;
               height:17px;
               font-size:12px;
               font-weight:500;
               line-height:17px;
               opacity:1;
           }
          .sb-dw{
            position: absolute;
            top:18px;
            left:300px;
            height:11px;
            font-size:8px;
            font-weight:400;
            line-height:11px;
            color:rgba(255,255,255,1);
            opacity:1;
            }
            .sb-t{
                position: absolute;
                left:305px;
                top:48px;
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
                top:90px;
                left:5px;
                width: 350px;
                height: 200px;
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