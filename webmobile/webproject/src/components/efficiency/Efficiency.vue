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
               <ve-histogram :data="chartData" :settings="chartSettings" width="340px" height="240px"></ve-histogram>
          </div>
          <div class="compare">
              <div class="left-box">
                  <div class="lt">本日最高负荷率:</div>
                  <div class="num">00.00</div>
                  <div class="percent">%</div>
                  <div class="time">时间:</div>
                  <div class="time-now">00:00:00</div>
              </div>
              <div class="right-box">
                  <div class="lt">本日最低负荷率:</div>
                  <div class="num">00.00</div>
                  <div class="percent">%</div>
                  <div class="time">时间:</div>
                  <div class="time-now">00:00:00</div>
              </div>
          </div>
    </div>
           
</template>
<script>
export default {
    data(){
        this.chartSettings = {
         axisSite: { right: ['下单率'] },
         yAxisType: ['KMB', 'percent'],
         yAxisName: ['数值', '比率'],
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
            chartData: {
                columns: ['日期', '有功功率', '额定功率', '负荷率'],
                rows: [
                    { '日期': '1/1', '有功功率': 1393, '额定功率': 1093, '负荷率': 0.9 },
                    { '日期': '1/2', '有功功率': 3530, '额定功率': 3230, '负荷率': 0.26 },
                    { '日期': '1/3', '有功功率': 2923, '额定功率': 2623, '负荷率': 0.76 },
                    { '日期': '1/4', '有功功率': 1723, '额定功率': 1423, '负荷率': 0.49 },
                    { '日期': '1/5', '有功功率': 3792, '额定功率': 3492, '负荷率': 0.323 },
                    { '日期': '1/6', '有功功率': 4593, '额定功率': 4293, '负荷率': 0.78 }
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
      }
      if(e===1){
          this.value1='线损率='
          this.value2='输入电量(kwh):',
          this.value3='输出电量(kwh):',
          this.value4='输入电量(kwh):'
          this.value5='1.83%'  
      }
    if(e===2){
        this.value1='管损率='
        this.value2='输入汽量(T):',
        this.value3='输出汽量(T):',
        this.value4='管损:'
        this.value5='1.83%'
        this.$http.get('/api/steamlossanalysis',{params:{
            StartTime: "2020-04-20 00:00:00",
            EndTime: "2020-04-20 23:59:59",
            TimeClass: "日"
        }}).then((res) => {
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
            width:86px;
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
            width:86px;
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
            width:86px;
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
            width:67px;
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
                  width:88px;
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