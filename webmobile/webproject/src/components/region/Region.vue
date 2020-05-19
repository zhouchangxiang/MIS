<template>
    <div class="show-box">
      <van-loading size="24px" vertical v-if="loading" color="lightgreen" type="spinner">加载中...</van-loading>
      <div class="tabbar">
      <van-tabs v-model="active" line-height="0px" line-width="0px" @click="getData($event)" :swipeable=true :border=false title-active-color="#fff" title-inactive-color="#76787E">
        <van-tab :title="item" v-for="(item,index) in list" :key="index"></van-tab>
      </van-tabs>
      </div>
      <div class="date-choose">
        <van-cell title="选择对比日期" :value="comparedate" @click="show = true" />
          <van-calendar v-model="show" @confirm="onConfirm" :min-date="minDate" :max-date="maxDate" color="#07c160"/>
      </div>
      <div class="compare">
        <div class="c1" :class="{switchbgc:bgc1}" @click="switchShow1()">
          <div class="icon electric"></div>
          <div class="dw electric1">kwh</div>
          <div class="number">{{electric}}</div>
          <div class="comp" @click="getEq">较{{yester}}日</div>
          <div class="sn" :class="this.todayelectric-this.yesterdayelectric>0?'maxcolor':'mincolor'">{{dayelectricCompare}}</div>
        </div>
         <div class="c2" :class="{switchbgc:bgc2}" @click="switchShow2()">
          <div class="icon water"></div>
          <div class="dw water">T</div>
          <div class="number">{{water}}</div>
          <div class="comp">较{{yester}}日</div>
          <div class="sn" :class="this.todaywater-this.yesterdaywater>0?'maxcolor':'mincolor'">{{daywaterCompare}}</div>
        </div>
        <div class="c3" :class="{switchbgc:bgc3}" @click="switchShow3()">
          <div class="icon steam"></div>
          <div class="dw">T</div>
          <div class="number">{{steam}}</div>
          <div class="comp">较{{yester}}日</div>
          <div class="sn" :class="this.todaysteam-this.yesterdaysteam>0?'maxcolor':'mincolor'">{{daysteamCompare}}</div>
        </div>
      </div>
      <div class="piclist">
           <ve-line :data="kong" :settings="chartSettings" width="350px" height="240px"  :legend-visible="false"></ve-line>
      </div>
         <div class="show-foot">
               <div class="sf-l">
                   <div class="hf">{{kind}}耗费成本</div>
                   <div class="all-money">{{cost}}<span>元</span></div>
               </div>
                <div class="sf-r">
                   <div class="machine">{{kind}}表在线情况</div>
                   <div class="tj"><span>{{onlineitem.online}}</span>&nbsp;/&nbsp;<span>{{onlineitem.total}}</span></div>
               </div>
        </div>
         <div class="bottom-dnh">
           <div class="dnh">{{kind}}能耗量</div>
           <div class="dnh-number">{{kind==='水'?water:(kind==='电'?electric:steam)}}</div>
           <div class="dw">{{kind==='电'?'kwh':'t'}}</div>
           <div class="dwpc">单位批次{{this.kind}}能耗量</div>
           <div class="dwpc-number">{{kind==='水'?waterbatch:(kind==='电'?0:steambatch)}}</div>
           <div class="pc-dw">{{kind==='电'?'kwh':'t'}}/批</div>
         </div>
       </div>
</template>
<script>
var moment=require('moment')
export default {
    data(){
      this.chartSettings = {
        yAxisType: ['KMB'],
        yAxisName: ['数值']
      }
        return {
          comparedate: '2020-04-30',
          show: false,
          minDate: new Date(2020, 0, 1),
          maxDate: new Date(2020, 11, 31),
          active:0,
          list:[],
          water:0,
          electric:0,
          steam:0,
          todaywater:0,
          todayelectric:0,
          todaysteam:0,
          yesterdaywater:0,
          yesterdayelectric:0,
          yesterdaysteam:0,
          cost1:[],
          cost:'',
          bgc1:false,
          bgc2:false,
          bgc3:false,
          loading:false,
          websoc:null,
          kind:'电',
          currentchoice:'GMP车间',
          kong:null,
          yester:'昨',
          ElectricEqList:[],
          WaterEqList:[],
          SteamEqList:[],
          watertag:'',
          electrictag:'',
          steamtag:'',
          waterbatch:0,
          steambatch:0,   
          onlinebiaolist:[{online:12,total:12},{online:2,total:17},{online:12,total:25}],
          onlineitem:{online:0,total:0},
          electricChartData:{
          columns:['日期', '数值'],
          rows: [
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""}]
        },
        resetChartData: {
          columns: ['日期', '数值'],
          rows: [
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""}]
        },
          waterChartData: {
          columns: ['日期', '数值'],
          rows: [
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""}]
        },
        steamChartData:{
          columns: ['日期', '数值'],
          rows: [
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""},
            { '日期': '', '数值': ""}]
        }}
    },
    created(){
      this.initNavbar()
    },
    destroyed(){
      if(this.websoc){
      this.websoc.close()
      }
    },
    computed:{
        dayelectricCompare(){
        if(this.thisYearCon > 0){
          var compare = (this.todayelectric - this.yesterdayelectric) / this.todayelectric * 100
          if(this.todayelectric - this.yesterdayelectric > 0){
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
        },
        daywaterCompare(){
        if(this.todaywater > 0){
          var compare = (this.todaywater - this.yesterdaywater) / this.todaywater * 100
          if(this.todaywater - this.yesterdaywater > 0){
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
        },
        daysteamCompare(){
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
        },
    },
    methods:{
      formatDate(date) {
      var month=`${date.getMonth()+1}`.padStart(2, 0)
      var day=`${date.getDate()}`.padStart(2, 0)
      return `${date.getFullYear()}-${month}-${day}`;
      },
      onConfirm(date) {
      this.show = false;
      this.yester='对比'
      this.comparedate = this.formatDate(date);
      var nowTime = moment().format('HH:mm').substring(0,4) + "0"
      var compareDateStartTime = moment(this.comparedate).day(moment(this.comparedate).day()).startOf('day').format('YYYY-MM-DD HH:mm')
      var compareDateEndTime = moment(this.comparedate).format('YYYY-MM-DD') + " " + nowTime
      this.$http.all([
            this.$http.get('/api/energywater',{params:{StartTime:compareDateStartTime,EndTime:compareDateEndTime,AreaName:this.currentchoice}}),
            this.$http.get('/api/energyelectric',{params:{StartTime:compareDateStartTime,EndTime:compareDateEndTime,AreaName:this.currentchoice}}),
            this.$http.get('/api/energysteam',{params:{StartTime:compareDateStartTime,EndTime:compareDateEndTime,AreaName:this.currentchoice}})
            ]).then(this.$http.spread((res1,res2,res3)=>{
             this.yesterdaywater=JSON.parse(res1.data).value
             this.yesterdayelectric=JSON.parse(res2.data).value
             this.yesterdaysteam=JSON.parse(res3.data).value
              }))
      },
      switchShow1(){
      if(this.websoc){
        this.websoc.close()
        }
      this.kind='电'
      this.bgc1=!this.bgc1
      this.bgc2=this.bgc3=false
      this.onlineitem=this.onlinebiaolist[0]
      this.kong=this.resetChartData
      if(this.bgc1){
        this.$toast('当前显示电数据')
         this.kong=this.electricChartData
       }else{
         this.kong=this.resetChartData
       }
       this.cost=this.cost1[1]
        this.initWebSocket()
      },
      switchShow2(){
        if(this.websoc){
          this.websoc.close()
          }
       this.bgc2=!this.bgc2
       this.bgc1=this.bgc3=false
       this.kind='水'
       this.onlineitem=this.onlinebiaolist[0]
       this.kong=this.resetChartData
       if(this.bgc2){
         this.$toast('当前显示水数据')
         this.kong=this.waterChartData
       }else{
         this.kong=this.resetChartData
       }
       this.cost=this.cost1[0]
       this.initWebSocket()
      },
      switchShow3(){
        if(this.websoc){
          this.websoc.close()
          }
       this.bgc1=this.bgc2=false
       this.bgc3=!this.bgc3
       this.kind='汽'
       this.onlineitem=this.onlinebiaolist[2]
       this.kong=this.SteamEqList=this.resetChartData
       if(this.bgc3){
         this.$toast('当前显示汽数据')
         this.kong=this.steamChartData
       }else{
         this.kong=this.resetChartData
       }
       this.cost=this.cost1[2]
       this.initWebSocket()
      },
      //websocket 获取数据方法汇总
      initWebSocket(){
            this.websoc=new WebSocket('ws://127.0.0.1:5002');
            this.websoc.onopen=this.webscop
            this.websoc.onmessage=this.webscom
            this.websoc.onerror=this.webscoer
            this.websoc.onclose=this.webscoclos
        },
        webscsend(data){
            this.websoc.send(data)
        },
        webscop(){
          if(this.kind==='电'){
            this.webscsend(this.electrictag)
          }else if(this.kind==='水'){
            this.webscsend(this.watertag)
          }else{
            this.webscsend(this.steamtag)
          }
        },
        webscom(evt){
          var arr=JSON.parse(evt.data)[1]
           if(this.kind==='电'){
              this.electricChartData.rows.push({
                "日期": moment(new Date()).format("ss"),
                "数值": arr['areaEZGL']
              })
              this.electricChartData.rows.shift()
           }else if(this.kind==='水'){
             this.waterChartData.rows.push({
               "日期": moment(new Date()).format("ss"),
                "数值": arr['areaWSum']
              })
              this.waterChartData.rows.shift()
           }else{
             this.steamChartData.rows.push({
               "日期": moment(new Date()).format("ss"),
                "数值": arr['areaSSum']
              })
                this.steamChartData.rows.shift()
           }
        },
        webscoer(){
            console.log('连接websocket失败。。。')
        },
        webscoclos(e){
            console.log('关闭websocket连接')
        },
        //点击导航栏获取相关能耗数据
        getData(e){
          var nowTime = moment().format('HH:mm').substring(0,4) + "0"
          var monthStartTime = moment().month(moment().month()).startOf('month').format('YYYY-MM-DD HH:mm:ss')
          var monthEndTime = moment().month(moment().month()).endOf('month').format('YYYY-MM-DD HH:mm:ss')
          var todayStartTime = moment().format('YYYY-MM-DD') + " 00:00"
          var todayEndTime = moment().format('YYYY-MM-DD') + " " + nowTime
          var yesterdayStartTime = moment().subtract(1,'day').format('YYYY-MM-DD') + " 00:00"
          var yesterdayEndTime = moment().subtract(1,'day').format('YYYY-MM-DD') + " " + nowTime
          let params={
            StartTime:monthStartTime,
            EndTime:monthEndTime,
            AreaName:this.list[e]
          }
          let params1={
            StartTime:todayStartTime,
            EndTime:todayEndTime,
            AreaName:this.list[e]
          }
          let params2={
            StartTime:yesterdayStartTime,
            EndTime:yesterdayEndTime,
            AreaName:this.list[e]
          }
          this.currentchoice=this.list[e]
          this.$toast('当前数据展示'+this.currentchoice)
          this.kong=this.resetChartData
          if(this.websoc){
            this.websoc.close()
            }
          this.$http.all([
            this.$http.get('/api/energywater',{params}),
            this.$http.get('/api/energyelectric',{params}),
            this.$http.get('/api/energysteam',{params}),//时间段为月份，获取月的时间段的数据，模拟数据
            this.$http.get('/api/energywater',{params:params1}),
            this.$http.get('/api/energyelectric',{params:params1}),
            this.$http.get('/api/energysteam',{params:params1}),
            this.$http.get('/api/energywater',{params:params2}),
            this.$http.get('/api/energyelectric',{params:params2}),
            this.$http.get('/api/energysteam',{params:params2}),
            this.$http.get('/api/batchMaintainEnergy',{params:params1})
            ]).then(this.$http.spread((res1,res2,res3,res4,res5,res6,res7,res8,res9,res10)=>{
                    this.water=JSON.parse(res1.data).value
                    this.electric=JSON.parse(res2.data).value
                    this.steam=JSON.parse(res3.data).value
                    var newlist=[]
                    newlist.push(JSON.parse(res1.data).cost)
                    newlist.push(JSON.parse(res2.data).cost)
                    newlist.push(JSON.parse(res3.data).cost)
                    this.cost1=newlist
                    this.bgc1=this.bgc2=this.bgc3=false
                    this.kong=this.resetChartData
                    this.getEq()
                    this.todaywater=JSON.parse(res4.data).value
                    this.todayelectric=JSON.parse(res5.data).value
                    this.todaysteam=JSON.parse(res6.data).value
                    this.yesterdaywater=JSON.parse(res7.data).value
                    this.yesterdayelectric=JSON.parse(res8.data).value
                    this.yesterdaysteam=JSON.parse(res9.data).value
                    this.waterbatch=res10.data.waterEveryBatch
                    this.steambatch=res10.data.steamEveryBatch
                  }))
              },
        getEq(){
              this.ElectricEqList = []
              this.WaterEqList = []
              this.SteamEqList = []
              var params = {
                tableName:"TagDetail",
                field:"AreaName",
                fieldvalue:this.currentchoice,
                limit:100000,
                offset:0
              }
              this.$http.get("/api/CUID",{params:params}).then(res =>{
                var rows = JSON.parse(res.data).rows
                rows.forEach(item =>{
                  if(item.EnergyClass === "电"){
                    this.ElectricEqList.push(item)
                    if(this.ElectricEqList!=[]){
                      this.electrictag=this.ElectricEqList[0].TagClassValue
                    }else{
                      this.electrictag=""
                    }
                  }else if(item.EnergyClass === "水"){
                    this.WaterEqList.push(item)
                    if(this.WaterEqList!=[]){
                      this.watertag=this.WaterEqList[0].TagClassValue
                    }else{
                      this.watertag=""
                    }
                  }else if(item.EnergyClass === "汽"){
                    this.SteamEqList.push(item)
                    if(this.SteamEqList!=[]){
                      this.steamtag=this.SteamEqList[0].TagClassValue
                    }else{
                      this.steamtag=""
                    }
                  }
                })
              })},
        //初始化获取navbar数据条
        initNavbar(){
        this.loading=true
        this.$http.get('/api/areatimeenergycount',{params:{
              EnergyClass:'电',CompareTime:'2020-04-14'
            }}).then((res3) => {
              this.loading=false
              let arr=res3.data.rows
              for(var i=0;i<arr.length;i++){
              this.list.push(arr[i]['区域'])
        }
      })
      }
    }
}
</script>
<style lang="less" scoped>
    @bgca:#3D4048FF;
    @bgcc:#1E222BFF;
    @bgct:#7E7F84;
     .show-box{
        position: relative;
        width: 375px;
        height:800px;
        box-sizing: border-box;
        padding: 0 12px 12px 13px;
        background: @bgcc;
        .tabbar{
          position: relative;
          height: 20px;
          font-size:14px;
          font-family:PingFang SC;
          font-weight:400;
          line-height:20px;
          color:rgba(255,255,255,1);
          opacity:1;
          background-color: #ccc;
          margin-bottom: 20px;
        }
        .date-choose{
          height: 55px;
          width: 100%;
        }
        .compare{
          width:100%;
          height:179px;
          opacity:1;
          margin-bottom: 17px;
          .icon{
            position: absolute;
            top:23px;
            left:44px;
            width: 17.44px;
            height: 21.15px;
          &.electric{
            background-image: url('../../assets/png/flashlight_1.png');
            width:18px;
            background-size: cover;
          }
          &.water{
            background-image: url('../../assets/png/water.png');
            width:16px;
            background-size: cover;
          }
          &.steam{
            background-image: url('../../assets/png/steam.png');
            background-size: cover;
            width:21px;
          }
          }
          .dw{
            position: absolute;
            left: 51px;
            top: 53px;
            width: 15px;
            height: 11px;
            font-size:8px;
            font-family:PingFang SC;
            font-weight:400;
            line-height:11px;
            color:rgba(255,255,255,1);
            opacity:1;
            &.electric1{
              left:42px;
            }
            &.water{
              left:49px;
            }
          }
          .number{
            position: absolute;
            left: 4px;
            top: 73px;
            text-align: center;
            width:97px;
            height:29px;
            overflow: hidden;
            text-overflow: hidden;
            background:rgba(126,127,132,1);
            box-shadow:0px 0px 6px rgba(255,255,255,0.16);
            border-radius:4px;
            font-size:18px;
            font-family:PingFang SC;
            font-weight:500;
            color:rgba(255,255,255,1);
            letter-spacing:1px;
            opacity:1;
          }
          .comp{
            position: absolute;
            left:38px;
            top:125px;
            width:50px;
            height:11px;
            font-size:8px;
            font-family:PingFang SC;
            font-weight:400;
            line-height:11px;
            color:rgba(255,255,255,1);
            opacity:1;
          }
          .sn{
            position: absolute;
            left: 40px;
            top: 142px;
            width:60px;
            height:17px;
            font-size:12px;
            font-family:PingFang SC;
            font-weight:500;
            line-height:17px;
            opacity:1;
          }
        .maxcolor{
          color:red;
        }
        .mincolor{
          color:green;
        }
          .c1{
            position: relative;
            width:103px;
            height:179px;
            background:rgba(126,127,132,1);
            float: left;
            margin-right: 20px;
            border-radius:4px;
          }
          .c2{
            position: relative;
            height:179px;
            width:103px;
            background:rgba(126,127,132,1);
            float: left;
            margin-right: 20px;
            border-radius:4px;
          }
          .c3{
            position: relative;
            width: 103px;
            height:179px;
            float: left;
            background:rgba(126,127,132,1);
            border-radius:4px;
          }
          .switchbgc{
            background-color: #FAC000;
            .number{
              background-color:rgba(0,0,0,.1);
            }
            .electric{
              background-image: url('../../assets/png/flashlight_2.png');
              }
          }
        }
        .piclist{
          height: 200px;
          background-color: #666;
          margin: 0 0 20px;
        }
        .bottom-dnh{
          position: relative;
          height: 150px;
          background-color: #1E222B;
          margin: 20px 0 20px;
          .dnh{
            position: absolute;
            top:10px;
            left: 17px;
            height:11px;
            font-size:8px;
            font-family:PingFang SC;
            font-weight:400;
            line-height:11px;
            color:rgba(255,255,255,1);
            opacity:1;
          }
          .dnh-number{
            position: absolute;
            top:30px;
            left: 16px;
            font-size: 24px;
            color:rgba(250,192,0,1);
            opacity:1;
            letter-spacing: 2px;
          }
          .dw{
            position: absolute;
            top:44px;
            left: 204px;
            height:11px;
            font-size:8px;
            font-family:PingFang SC;
            font-weight:500;
            line-height:11px;
            color:rgba(255,255,255,1);
            opacity:1;
          }
        .dwpc{
          position: absolute;
          top:70px;
          left: 17px;
          height:11px;
          font-size:8px;
          font-family:PingFang SC;
          font-weight:400;
          line-height:11px;
          color:rgba(255,255,255,1);
          opacity:1;
        }
        .dwpc-number{
          position: absolute;
          top:90px;
          left: 16px;
          font-size: 24px;
          color:rgba(250,192,0,1);
          opacity:1;
          letter-spacing: 2px;
        }
        .pc-dw{
          position: absolute;
          top:102px;
          left: 204px;
          height:11px;
          font-size:8px;
          font-family:PingFang SC;
          font-weight:500;
          line-height:11px;
          color:rgba(255,255,255,1);
          opacity:1;
        }
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
                    width:75px;
                    height:11px;
                    font-size:8px;
                    font-weight:400;
                    line-height:11px;
                    color:rgba(255,255,255,1);
                    opacity:1;
                }
                .all-money{
                    position: absolute;
                    left:10px;
                    top:28px;
                    height:23px;
                    font-size: 23px;
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
</style>