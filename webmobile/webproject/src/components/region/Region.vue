<template>
    <div class="show-box">
      <van-loading size="24px" vertical v-if="loading" color="lightgreen" type="spinner">加载中...</van-loading>
      <div class="tabbar">
      <van-tabs v-model="active" line-height="0px" line-width="0px" @click="getData($event)" :swipeable=true :border=false title-active-color="#fff" title-inactive-color="#76787E">
        <van-tab :title="item" v-for="(item,index) in list" :key="index"></van-tab>
      </van-tabs>
      </div>
      <div class="compare">
        <div class="c1" :class="{switchbgc:this.bgc1}" @click="switchShow1()">
          <div class="icon electric"></div>
          <div class="dw electric1">kwh</div>
          <div class="number">{{this.electric}}</div>
          <div class="comp">较昨日</div>
          <div class="sn">+1.456%</div>
        </div>
         <div class="c2" :class="{switchbgc:this.bgc2}" @click="switchShow2()">
          <div class="icon water"></div>
          <div class="dw water">T</div>
          <div class="number">{{this.water}}</div>
          <div class="comp">较昨日</div>
          <div class="sn">+1.456%</div>
        </div>
        <div class="c3" :class="{switchbgc:this.bgc3}" @click="switchShow3()">
          <div class="icon steam"></div>
          <div class="dw">T</div>
          <div class="number">{{this.steam}}</div>
          <div class="comp">较昨日</div>
          <div class="sn">+1.456%</div>
        </div>
      </div>
        <div class="show-top singledate">
               <div class="tips">
                   <van-tabs type="card" title-active-color="#1E222B" title-inactive-color="#fff" v-model="choosedate" >
                        <van-tab title="日"></van-tab>
                    </van-tabs>
                </div>
        </div>
         <div class="piclist">
           <ve-line :data="electricChartData" :settings="chartSettings" width="350px" height="240px"></ve-line>
         </div>
         <ShowNumber></ShowNumber>
         <div class="bottom-dnh">
           <div class="dnh">电能耗量</div>
           <div class="dnh-number">00000000.00</div>
           <div class="dw">kwh</div>
           <div class="dwpc">单位批次电能耗量</div>
           <div class="dwpc-number">00000000.00</div>
           <div class="pc-dw">kwh/批</div>
         </div>
       </div>
</template>
<script>
import ShowNumber from '../common/Shownumber.vue'
var moment=require('moment')
export default {
    data(){
      this.chartSettings = {
        yAxisType: ['KMB'],
        yAxisName: ['单位']
      }
        return {
          radio1:1,
          radio2:1,
          active:2,
          choosedate:0,
          list:[],
          water:0,
          electric:0,
          steam:0,
          bgc1:false,
          bgc2:false,
          bgc3:false,
          loading:false,
          websoc:null,
          currentchoice:'',
          electricChartData:{
          columns:['日期', '数值'],
          rows: [
            { '日期': '00', '数值': 139 },
            { '日期': '02', '数值': 345 },
            { '日期': '04', '数值': 923 },
            { '日期': '06', '数值': 723 },
            { '日期': '08', '数值': 139 },
            { '日期': '10', '数值': 345 },
            { '日期': '12', '数值': 923 },
            { '日期': '14', '数值': 723 },
            { '日期': '16', '数值': 139 },
            { '日期': '18', '数值': 345 },
            { '日期': '20', '数值': 923 },
            { '日期': '22', '数值': 723 },]
        },
          waterChartData: {
          columns: ['日期', '数值'],
          rows: [
            { '日期': '00', '数值': 139 },
            { '日期': '02', '数值': 345 },
            { '日期': '04', '数值': 923 },
          ]
        },
        steamChartData:{
          columns: ['日期', '数值'],
          rows: [
            { '日期': '00', '数值': 139 },
            { '日期': '02', '数值': 345 },
            { '日期': '04', '数值': 923 },
          ]
        }}
    },
    components:{
      ShowNumber
    },
    created(){
      this.initWebSocket()
    },
    mounted(){
      this.getNavbar()
    },
    destroyed(){
      this.websoc.close()
    },
    methods:{
      switchShow1(){
       this.bgc1=!this.bgc1
       this.bgc2=false
       this.bgc3=false
      },
      switchShow2(){
       this.bgc2=!this.bgc2
       this.bgc1=false
       this.bgc3=false
      },
      switchShow3(){
       this.bgc3=!this.bgc3
       this.bgc1=false
       this.bgc2=false
      },
      //websocket 获取数据方法汇总
       initWebSocket(){
            this.websoc=new WebSocket('ws://127.0.0.1:5002')
            this.websoc.onopen=this.webscop
            this.websoc.onmessage=this.webscom
            this.websoc.onerror=this.webscoer
            this.websoc.onclose=this.webscoclos
        },
        webscsend(data){
            this.websoc.send(data)
        },
        webscop(){
          this.webscsend()  
        },
        webscom(evt){
            var arr=JSON.parse(evt.data)
            for(var i=0;i<arr.length;i++){
              if(arr[i]['AreaName']==this.currentchoice){
              this.electricChartData.rows.push({
                "日期": moment(new Date()).format("ss"),
                "数值": arr[i]['areaEZGL']
              })
              this.electricChartData.rows.shift()
              this.waterChartData.rows.push({
                "日期": moment(new Date()).format("ss"),
                "数值": arr[i]['areaWSum']
              })
              this.waterChartData.rows.shift()
               this.steamChartData.rows.push({
                "日期": moment(new Date()).format("ss"),
                "数值": arr[i]['areaSSum']
              })
              this.steamChartData.rows.shift()
                }
              }
        },
        webscoer(){
            console.log('连接失败。。。')
        },
        webscoclos(){
            console.log('关闭连接。。。')
        },
        getData(e){
          let params={
            StartTime:'2020-04-09 12:22:59',
            EndTime:'2020-04-14 12:22:59',
            AreaName:this.list[e]
          }
          this.currentchoice=this.list[e]
          this.$http.all([
            this.$http.get('/api/energywater',{params}),
            this.$http.get('/api/energyelectric',{params}),
            this.$http.get('/api/energysteam',{params})]).then(this.$http.spread((res1,res2,res3)=>{
                    this.water=JSON.parse(res1.data).value
                    this.electric=JSON.parse(res2.data).value
                    this.steam=JSON.parse(res3.data).value
                  }))
              },
      getNavbar(){
        this.loading=true
        this.$http.get('/api/areatimeenergycount',{params:{
              EnergyClass:'电',CompareTime:'2020-04-14'
            }}).then((res3) => {
              this.loading=false
              this.$store.commit('CompareBox',res3.data.rows)
              let arr=this.$store.state.comparebox
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
          }
          &.water{
            background-image: url('../../assets/png/water.png')
          }
          &.steam{
            background-image: url('../../assets/png/steam.png');
            width:22px;
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
            line-height: 29px;
            background:rgba(126,127,132,1);
            box-shadow:0px 0px 6px rgba(255,255,255,0.16);
            opacity:1;
            border-radius:4px;
            font-size:18px;
            font-family:PingFang SC;
            font-weight:500;
            color:rgba(255,255,255,1);
            letter-spacing:3px;
            opacity:1;
          }
          .comp{
            position: absolute;
            left:41px;
            top:125px;
            width:37px;
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
            left: 32px;
            top: 142px;
            width:42px;
            height:17px;
            font-size:12px;
            font-family:PingFang SC;
            font-weight:500;
            line-height:17px;
            color:rgba(255,80,65,1);
            opacity:1;
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
            width:49px;
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