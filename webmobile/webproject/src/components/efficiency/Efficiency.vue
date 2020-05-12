<template>
    <div class="show-box">
          <div class="cir-choose">
              <van-tabs type="card" title-active-color="#1E222B" title-inactive-color="#fff"  v-model="active"  @click="switchCard($event)"> 
                        <van-tab title="运行效率"></van-tab>
                        <!-- <van-tab title="线损情况"></van-tab> -->
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
          <div class="choice-box">
           <div class="show-top">
               <div class="tips">
                   <van-tabs type="card" title-active-color="#1E222B" title-inactive-color="#fff" v-model="choosedate" @click="ChooseDate($event)"> 
                        <van-tab title="日"></van-tab>
                        <van-tab title="月"></van-tab>
                        <van-tab title="年"></van-tab>
                    </van-tabs>
                </div>
           </div>
           <div class="select-workplace" v-if="isrun">
               <van-dropdown-menu>
                    <van-dropdown-item v-model="valuekind" :options="option1" @change="ChooseWorkplace($event)"/>
                </van-dropdown-menu>
           </div>
           </div>
          <div class="piclist">
               <ve-histogram :data="chartData" :settings="chartSettings" width="350px" height="240px"></ve-histogram>
          </div>
          <div class="compare">
              <div class="left-box">
                  <div class="lt">本{{formParameters.resourceTime}}最高负荷率:</div>
                  <div class="num">{{Maxloadrate}}</div>
                  <div class="percent">%</div>
                  <div class="time">时间:</div>
                  <div class="time-now">{{Maxtime}}</div>
              </div>
              <div class="right-box">
                  <div class="lt">本{{formParameters.resourceTime}}最低负荷率:</div>
                  <div class="num">{{Minloadrate}}</div>
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
            valuekind: 0,
            option1: [
                { text: "原提取车间", value: 0 },
                { text: "固体制剂车间", value: 1 },
                { text: "综合制剂车间", value: 2 },
                { text: "GMP车间", value: 3 },
                { text: "中试车间", value: 4 },
                { text: "污水站", value: 5 },
                { text: "锅炉房", value: 6 },
                { text: "前处理车间", value: 7 },
                { text: "提取二车间", value: 8 },
                { text: "综合车间", value: 9 },
                { text: "办公楼＼食堂", value: 10 },
            ],
            formParameters:{
                resourceTime:"日",
                startDate:moment().format("YYYY-MM-DD HH:mm:ss")
            },
            isrun:true,
            choosedate:0,
            tabbar:0,
            AreaName:'原提取车间',
            active: 0,
            value1:'运行效率',
            value2:'有功功率(kwh):',
            value3:'额定功率(kwh):',
            value4:'当前负荷率:',
            value5:'功率等级&nbsp;优',
            num1:'00.00',
            num2:'00.00',
            num3:'00.00',
            Maxloadrate:0,
            Minloadrate:0,
            Maxtime:'2020-05',
            Mintime:'2020-05',
            chartData: {
                columns: ['日期', '负荷率'],
                rows: []
        }
      }
        },
    methods:{
        ChooseWorkplace(e){
          this.AreaName=this.option1[e].text
        },
        ChooseDate(e){
        var dayStartTime = moment(this.formParameters.startDate).format('YYYY-MM-DD') + " 00:00:00"
        var dayEndTime = moment(this.formParameters.startDate).format('YYYY-MM-DD HH:mm:ss')
        var monthStartTime = moment(this.formParameters.startDate).month(moment(this.formParameters.startDate).month()).startOf('month').format('YYYY-MM-DD HH:mm:ss')
        var monthEndTime = moment(this.formParameters.startDate).month(moment(this.formParameters.startDate).month()).endOf('month').format('YYYY-MM-DD HH:mm:ss')
        var yearStartTime = moment(this.formParameters.startDate).year(moment(this.formParameters.startDate).year()).startOf('year').format('YYYY-MM-DD HH:mm:ss')
        var yearEndTime = moment(this.formParameters.startDate).year(moment(this.formParameters.startDate).year()).endOf('year').format('YYYY-MM-DD HH:mm:ss')
        var params={}
        var params2={}
       if(e===0){
          this.formParameters.resourceTime='日'
          params.StartTime = dayStartTime
          params.EndTime = dayEndTime
          params.TimeClass = this.formParameters.resourceTime
          params.CurrentTime = moment(this.formParameters.startDate).format('YYYY-MM-DD HH:mm:ss')
          params.AreaName =  this.AreaName
          params2.StartTime=dayStartTime
          params2.EndTime=dayEndTime
          params2.TimeClass=this.formParameters.resourceTime
       }
       else if(e===1){
          this.formParameters.resourceTime='月'
          params.StartTime = monthStartTime
          params.EndTime = monthEndTime
          params.TimeClass = this.formParameters.resourceTime
          params.CurrentTime = moment(this.formParameters.startDate).format('YYYY-MM-DD HH:mm:ss')
          params.AreaName =  this.AreaName
          params2.StartTime=monthStartTime
          params2.EndTime=monthEndTime
          params2.TimeClass=this.formParameters.resourceTime
       }else{
          this.formParameters.resourceTime='年'
          params.StartTime = yearStartTime
          params.EndTime = yearEndTime
          params.TimeClass = this.formParameters.resourceTime
          params.CurrentTime = moment(this.formParameters.startDate).format('YYYY-MM-DD HH:mm:ss')
          params.AreaName =  this.AreaName
          params2.StartTime=yearStartTime
          params2.EndTime=yearEndTime
          params2.TimeClass=this.formParameters.resourceTime
       }
       if( this.tabbar===0){
       this.$http.get("/api/runefficiency",{params:params}).then(res => {
           this.num1=res.data.activePower
           this.num2=res.data.ratedPower
           this.num3=res.data.loadRate
           var arr=res.data.row
           this.chartData.rows=[]
           var maxrate=arr[0]['负荷率']
           var minrate=arr[0]['负荷率']
           var maxtime=arr[0]['时间']
           var mintime=arr[0]['时间']
           for(var i=0;i<arr.length;i++){
               if(arr[i]['负荷率']!==''){
               this.chartData.rows.push({
               '日期':arr[i]['时间'].slice(-2),
               '负荷率':arr[i]['负荷率']
           })
                if(arr[i]['负荷率']>maxrate){
                    maxrate=arr[i]['负荷率']
                    maxtime=arr[i]['时间']
                }else{
                    maxtime=maxtime
                    maxrate=maxrate
                }
                if(arr[i]['负荷率']<minrate){
                    minrate=arr[i]['负荷率']
                    mintime=arr[i]['时间']
                }else{
                    mintime=mintime
                    minrate=minrate
                }
               }
           }
           this.Maxloadrate=maxrate
           this.Minloadrate=minrate
           this.Maxtime=maxtime
           this.Mintime=mintime
       })}else{
        this.$http.get('/api/steamlossanalysis',{params:params2}).then((res) => {
            this.value5=res.data.PipeDamageRate
            this.num1=res.data.inputSteam
            this.num2=res.data.outputSteam
            this.num3=res.data.PipeDamage
        })
       }
   },
    switchCard(e){
        if(e===0){
          this.tabbar=0
          this.isrun=true
          this.value1='运行效率'
          this.value2='有功功率(kwh):',
          this.value3='额定功率(kwh):',
          this.value4='当前负荷率:'
          this.value5='功率等级&nbsp;优'
          this.num1=this.num2=this.num3=0
      }
    if(e===1){
        this.tabbar=1
        this.tabbar='管损情况'
        this.isrun=false
        this.value1='管损率='
        this.value2='输入汽量(T):'
        this.value3='输出汽量(T):'
        this.value4='管损:'
        this.value5='0'
        this.num1=this.num2=this.num3=0
        this.Maxloadrate=this.Minloadrate=this.Maxtime=this.Mintime=0
        this.chartData.rows=[]
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
            font-size:22px;
            font-family:PingFang SC;
            font-weight:500;
            line-height:45px;
            color:#fff;
            letter-spacing:1px;
            opacity:1;
            height:36px;
            .num1{
                position: absolute;
                left: 0;
            }
            .num2{
                position: absolute;
                left: 95px;
            }
            .num3{
                position: absolute;
                left: 210px;
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
          height: 190px;
          overflow: hidden;
          background-color:rgba(255,255,255,.5);
      }
      .compare{
          position: relative;
          height: 129px;
          width: 100%;
          margin-top: 10px;
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
      .choice-box{
          position: relative;
          margin-top: 10px;
          height: 18px;
      }
      .show-top{
            position: absolute;
            width: 150px;
            height:18px;
            opacity:1;
            border-radius:4px;
            color:#fff;
            font-size: 10px;
            .tips{
                background-color:#1E222B;
                height: 18px;
            }
        }
        .select-workplace{
            position: absolute;
            float: left;
            left: 130px;
            width:120px;
            height:18px;
        }
</style>