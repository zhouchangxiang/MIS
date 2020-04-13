<template>
    <div class="show-box">
        <DateC :fz="radio1"></DateC>
        <div class="show-banner">
                  <div class="sb-name" @click="getWater">厂区能耗</div>
                  <div class="sb-number">{{shui}}</div>
                  <div class="sb-compare">较上期</div>
                  <div class="sb-l-n">+1.345%</div>
                  <div class="sb-dw">单位</div>
                  <div class="sb-t">T</div>
                  <div class="tabbar">
                      <ul>
                          <li><div>提取制剂</div><span></span></li>
                          <li>提取二<span></span></li>
                          <li>前处理<span></span></li>
                          <li>研发中心<span></span></li>
                      </ul>
                   </div>
           </div>
           <div class="show-body">
               <div class="sb-l">
                   <div class="scpc">生产批次</div>
                   <div class="scpc-s">0</div>
                   <div class="znhl">总耗能量</div>
                   <div class="znhl-s">000000.00</div>
                   <div class="dwnh">单位批次能耗</div>
                   <div class="dwnh-s">000000.00</div>
                   <div class="dw-kwh">kwh</div>
                   <div class="dw-pc">kwh/批</div>
               </div>
               <div class="sb-r">
                    <van-picker :columns="area" @change="onChange" :default-index="2"/>
               </div>
           </div>
        <ShowNumber></ShowNumber>
       </div>
</template>
<script>
var moment=require('moment')
import ShowNumber from '../common/Shownumber.vue'
import DateC from '../common/Choosedate.vue'
import store from '../../store/index'
import ChoosedateVue from '../common/Choosedate.vue'
var moment=require('moment')
export default {
    data(){
        return {
            radio1:3,
            radio2:3,
            activeKey: 0,
            shui:'',
            area:['新建综合制剂楼','提取二车间','前处理车间','研发中心','生物科技楼','原提取车间','锅炉房']
        }
    },
    components:{
        DateC,
        ShowNumber
    },
    created(){
        this.getWater()
    },
    methods:{
      onChange(picker, value) {
        this.$store.commit("Chooseworkplace",value)
        this.$toast(value);
    },
    getWater(){
        console.log(moment(new Date()).format('YYYY-MM-DD HH:mm:ss'))
        let str=moment(new Date()).format('YYYY-MM-DD HH:mm:ss')

        this.$http.get('/api/energywater',{params:{
            StartTime:'2020-04-07 12:22:59',
            EndTime:str,
            Area:'研发中心'
            }}).then((value) => {
          let a=JSON.parse(value.data)
          console.log(a)
          this.shui=a.value
          console.log(value)
        })
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
               width:56px;
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
               font-size: 32px;
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
               width:42px;
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
            width:25px;
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
                right:15px;
                ul{
                    margin: 0;
                    padding: 0;
                    li{
                        height:36px;
                        text-align: right;
                        font-size:8px;
                        font-weight:400;
                        color: #fff;
                        span{
                            display: block;
                            margin-top: 5px;
                            height: 4px;
                            background-color: #fff;
                        }
                    }
                }
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
                    width:50px;
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
                    right: 8px;
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
        

    }
</style>