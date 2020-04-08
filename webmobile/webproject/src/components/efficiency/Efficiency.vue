<template>
    <div class="show-box">
          <div class="cir-choose">
              <van-tabs type="card" title-active-color="#1E222B" title-inactive-color="#fff"  v-model="active"  @click="mhy"> 
                        <van-tab title="运行效率"></van-tab>
                        <van-tab title="线损情况"></van-tab>
                        <van-tab title="管损情况"></van-tab>
              </van-tabs>
          </div>
          <div class="show-banner">
              <div class="tips">线损率=</div>
              <div class="input-elc1">输入电量(kw)：</div>
              <div class="output-elc">输出电量(kw):</div>
              <div class="input-elc2">输出电量(kw):</div>
              <div class="ou">1.38%</div>
              <div class="shownumber">
                  <span class="num1">00.00</span>
                  <span class="num2">00.00</span>
                  <span class="num3">00.00</span>
                  <span class="fh1"></span>
                  <span class="fh2">/</span>
                  <span class="fh3">%</span>
                  </div>
          </div>
          <div class="piclist">数图标区域</div>
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
        return {
            radio1:3,
            radio2:3,
            active: 0
        }
    },
    methods:{
        myc(){
            this.$toast(this.radio1)
    },
    mhy(){
        this.$toast(this.active)
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
        height:526px;
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
          margin-top: 20px;
          background:rgba(126,127,132,1);
          box-shadow:0px 0px 6px rgba(255,255,255,0.16);
          opacity:1;
          border-radius:4px;
        .tips{
            position: absolute;
            top: 14px;
            left: 15px;
            width:55px;
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
            left:300px;
            width:28px;
            height:14px;
            font-size:10px;
            font-family:PingFang SC;
            font-weight:400;
            line-height:14px;
            color:rgba(0,250,231,1);
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
          margin-top: 30px;
          height: 131px;
          background-color: #ccc;
      }
      .compare{
          position: relative;
          height: 129px;
          width: 100%;
          margin-top: 30px;
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