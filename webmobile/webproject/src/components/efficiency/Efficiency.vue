<template>
    <div class="show-box">
          <div class="cir-choose">
              <van-tabs type="card" title-active-color="#1E222B" title-inactive-color="#fff"  v-model="active"  @click="switchCard($event)"> 
                        <van-tab title="运行效率"></van-tab>
                        <van-tab title="线损情况"></van-tab>
                        <van-tab title="管损情况"></van-tab>
              </van-tabs>
          </div>
          <div class="show-banner">
              <div class="tips">{{value1}}</div>
              <div class="input-elc1">{{value2}}</div>
              <div class="output-elc">{{value3}}</div>
              <div class="input-elc2">{{value4}}</div>
              <div class="ou" v-html="value5"></div>
              <div class="shownumber">
                  <span class="num1">{{num1}}</span>
                  <span class="num2">{{num2}}</span>
                  <span class="num3">{{num3}}</span>
                  </div>
          </div>
          <div class="piclist">
               <ve-histogram :data="chartData" :settings="chartSettings" width="350px" height="240px"></ve-histogram>
          </div>
          <div class="compare">
              <div class="left-box">
                  <div class="lt">本日最高负荷率:</div>
                  <div class="num">{{maxloadrate}}</div>
                  <div class="percent">%</div>
                  <div class="time">时间:</div>
                  <div class="time-now">{{Maxtime}}</div>
              </div>
              <div class="right-box">
                  <div class="lt">本日最低负荷率:</div>
                  <div class="num">{{minloadrate}}</div>
                  <div class="percent">%</div>
                  <div class="time">时间:</div>
                  <div class="time-now">{{Mintime}}</div>
              </div>
          </div>
    </div>
           
</template>
<script>
var moment=require('moment')
export default {
    data(){
        this.chartSettings = {
         yAxisType: ['KMB'],
         yAxisName: ['数值'],
      }
        return {
            active: 0,
            value1:'运行效率',
            value2:'有功功率(kwh):',
            value3:'额定功率(kwh):',
            value4:'当前负荷率:',
            value5:'功率等级&nbsp;优',
            num1:'00.00',
            num2:'00.00',
            num3:'00.00',
            maxloadrate:0.8,
            minloadrate:0.3,
            Maxtime:'2020-03-16',
            Mintime:'2020-03-16',
            chartData: {
                columns: ['日期', '负荷率'],
                rows: [
                    { '日期': '01', '负荷率':0.1},
                    { '日期': '02', '负荷率': 0.2},
                    { '日期': '03', '负荷率': 0.7},
                    { '日期': '01', '负荷率':0.7},
                    { '日期': '02', '负荷率': 0.5},
                    { '日期': '03', '负荷率': 0.3},
                    { '日期': '01', '负荷率':0.2},
                    { '日期': '02', '负荷率': 0.2},
                    { '日期': '03', '负荷率': 0.9}
                ]
        }
      }
        },
    methods:{
    switchCard(e){
      if(e===0){
          this.value1='运行效率'
          this.value2='有功功率(kwh):',
          this.value3='额定功率(kwh):',
          this.value4='当前负荷率:'
          this.value5='功率等级&nbsp;优'
          this.$http.get('/api/runefficiency',{params:{
              StartTime:'2020-04-24 09:00:00',
              EndTime:'2020-04-24 21:23:00',
              TimeClass:'日'
          }}).then((res) => {
               this.num1=res.data.activePower
               this.num2=res.data.ratedPower
               this.num3=res.data.loadRate
               var arr=res.data.row
               this.chartData.rows=[]
               var max=arr[0]['负荷率']
               var min=arr[0]['负荷率']
               var maxtime=arr[0]['时间']
               var mintime=arr[0]['时间']
               for(var i=0;i<arr.length;i++){
                if(arr[i]['负荷率']>max){
                    max=arr[i]['负荷率']
                    maxtime=arr[i]['时间']
                }
                if(arr[i]['负荷率']<min){
                    min=arr[i]['负荷率']
                    mintime=arr[i]['时间']
                }
                this.chartData.rows.push({
                "日期": arr[i]['时间'].slice(-2),
                "负荷率": arr[i]['负荷率']
              })
               }
                this.maxloadrate=max
                this.minloadrate=min
                this.Maxtime=maxtime
                this.Mintime=mintime
          })
      }
      if(e===1){
          this.value1='线损率='
          this.value2='输入电量(kwh):'
          this.value3='输出电量(kwh):'
          this.value4='输入电量(kwh):'
          this.value5='1.83%'  
      }
    if(e===2){
        this.value1='管损率='
        this.value2='输入汽量(T):'
        this.value3='输出汽量(T):'
        this.value4='管损:'
        this.value5='1.83%'
        this.$http.get('/api/steamlossanalysis',{params:{
            StartTime: "2020-04-20 00:00:00",
            EndTime: "2020-04-20 23:59:59",
            TimeClass: "日"
        }}).then((res) => {
            console.log(res)
            this.value5=res.data.PipeDamageRate
            this.num1=res.data.inputSteam
            this.num2=res.data.outputSteam
            this.num3=res.data.PipeDamage
        })
    }
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
        height:576px;
        box-sizing: border-box;
        padding: 0 12px 12px 13px;
        background-color: @bgcc;
      .cir-choose{
          position: relative;
          left: 78px;
          width:193px;
          height:22px;
          background:rgba(61,64,72,1);
          opacity:1;
          border-radius:4px
            }
        }
      .show-banner{
          position: relative;
          width:350px;
          height:130px;
          margin-top: 10px;
          background:rgba(126,127,132,1);
          box-shadow:0px 0px 6px rgba(255,255,255,0.16);
          opacity:1;
          border-radius:4px;
        .tips{
            position: absolute;
            top: 14px;
            left: 15px;
            width:70px;
            height:20px;
            font-size:14px;
            font-family:PingFang SC;
            font-weight:400;
            line-height:20px;
            color:rgba(255,255,255,1);
            opacity:1;
        }
        .input-elc1{
            position: absolute;
            left: 15px;
            top:60px;
            height:11px;
            font-size:8px;
            font-family:PingFang SC;
            font-weight:400;
            line-height:11px;
            color:rgba(255,255,255,1);
            opacity:1;
        }
        .output-elc{
            position: absolute;
            left: 125px;
            top:60px;
            height:11px;
            font-size:8px;
            font-family:PingFang SC;
            font-weight:400;
            line-height:11px;
            color:rgba(255,255,255,1);
            opacity:1;
        }
        .input-elc2{
            position: absolute;
            left: 235px;
            top:60px;
            height:11px;
            font-size:8px;
            font-family:PingFang SC;
            font-weight:400;
            line-height:11px;
            color:rgba(255,255,255,1);
            opacity:1;
        }
        .ou{
            position: absolute;
            top:14px;
            left:267px;
            height:14px;
            font-size:10px;
            font-family:PingFang SC;
            font-weight:400;
            line-height:14px;
            color: #fff;
            opacity:1;
        }
        .shownumber{
            position: absolute;
            left: 13px;
            top:75px;
            font-size:30px;
            font-family:PingFang SC;
            font-weight:500;
            line-height:45px;
            color:#fff;
            letter-spacing:2px;
            opacity:1;
            height:36px;
            .num1{
                position: absolute;
                left: 0;
            }
            .num2{
                position: absolute;
                left: 120px;
            }
            .num3{
                position: absolute;
                left: 231px;
                color:rgba(250,192,0,1); 
            }
            .fh1{
                position: absolute;
                left: 101px;
                top:12px;
                width:7px;
                height:17px;
                border-bottom: 1px solid #fff;
                font-size:12px;
                font-family:PingFang SC;
                font-weight:500;
                line-height:17px;
                color:#fff;
                opacity:1;
            }
            .fh2{
                position: absolute;
                left: 217px;
                top:16px;
                width:7px;
                height:17px;
                font-size:12px;
                font-family:PingFang SC;
                font-weight:500;
                line-height:17px;
                color:#fff;
                opacity:1; 
            }
            .fh3{
                position: absolute;
                left: 319px;
                top:16px;
                width:12px;
                height:17px;
                font-size:14px;
                font-family:PingFang SC;
                font-weight:500;
                line-height:17px;
                color:#fff;
                opacity:1; 
            }
        }
      }
      .piclist{
          margin-top: 15px;
          height: 190px;
          overflow: hidden;
          background-color:rgba(255,255,255,.5);
      }
      .compare{
          position: relative;
          height: 129px;
          width: 100%;
          margin-top: 15px;
           .lt{
                  position: absolute;
                  top:14px;
                  left:13px;
                  height:11px;
                  font-size:8px;
                  font-family:PingFang SC;
                  font-weight:400;
                  line-height:11px;
                  color:rgba(255,255,255,1);
                  opacity:1;
              }
              .num{
                  position: absolute;
                  left:9px;
                  top:34px;
                  height:36px;
                  font-size: 30px;
                  color:rgba(250,192,0,1);   
              }
              .percent{
                  position: absolute;
                  top:49px;
                  left:103px;
                  width:12px;
                  height:17px;
                  font-size:12px;
                  font-family:PingFang SC;
                  font-weight:500;
                  line-height:17px;
                  color:rgba(255,255,255,1);
                  opacity:1;
              }
              .time{
                  position: absolute;
                  left:14px;
                  top:79px;
                  width:29px;
                  height:11px;
                  font-size:8px;
                  font-family:PingFang SC;
                  font-weight:400;
                  line-height:11px;
                  color:rgba(255,255,255,1);
                  opacity:1;
              }
              .time-now{
                  position: absolute;
                  left:11px;
                  top:98px;
                  font-size: 20px;
                  color:#fff;
              }
          .left-box{
              position: absolute;;
              left: 0;
              width:165px;
              height:129px;
              background:rgba(126,127,132,1);
              box-shadow:0px 0px 6px rgba(255,255,255,0.16);
              opacity:1;
              border-radius:4px;
          }
          .right-box{
              position: absolute;
              left:185px!important;
              top:0;
              width:165px;
              height:129px;
              background:rgba(126,127,132,1);
              box-shadow:0px 0px 6px rgba(255,255,255,0.16);
              opacity:1;
              border-radius:4px;

          }
      }
</style>