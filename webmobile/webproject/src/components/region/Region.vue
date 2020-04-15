<template>
    <div class="show-box">
      <div class="tabbar">
      <van-tabs v-model="active" line-height="0px" line-width="0px" @click="mss" :swipeable=true :border=false title-active-color="#fff" title-inactive-color="#76787E">
        <van-tab title="新建制剂"></van-tab>
        <van-tab title="提取二车"></van-tab>
        <van-tab title="前车处理"></van-tab>
        <van-tab title="研发中心"></van-tab>
        <van-tab title="生物科技"></van-tab>
        <van-tab title="原提取"></van-tab>
      </van-tabs>
      </div>
      <div class="compare">
        <div class="c1">
          <div class="icon electric"></div>
          <div class="dw electric">kwh</div>
          <div class="number">13567.3</div>
          <div class="comp">较昨日</div>
          <div class="sn">+1.456%</div>
        </div>
         <div class="c2">
          <div class="icon water"></div>
          <div class="dw water">T</div>
          <div class="number">13567.3</div>
          <div class="comp">较昨日</div>
          <div class="sn">+1.456%</div>
        </div>
        <div class="c3">
          <div class="icon steam"></div>
          <div class="dw">T</div>
          <div class="number">13567.3</div>
          <div class="comp">较昨日</div>
          <div class="sn">+1.456%</div>
        </div>
      </div>
         <DateC></DateC>
         <div class="piclist">zhangsh</div>
         <ShowNumber></ShowNumber>
       </div>
</template>
<script>
import DateC from '../common/Choosedate.vue'
import ShowNumber from '../common/Shownumber.vue'
export default {
    data(){
        return {
          radio1:1,
          radio2:1,
          active:2
        }
    },
    components:{
      DateC,
      ShowNumber
    },
    methods:{
      myc(){
        this.$toast(this.radio1)
      },
      mss(){
        this.$toast(this.active)

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
        height:526px;
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
            &.electric{
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
            &:active{
              background-color: #fff;
            }
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
        }
        .piclist{
          height: 185px;
          background-color: #666;
          margin-top: 2px;
        }
    }
</style>