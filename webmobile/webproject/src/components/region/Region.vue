<template>
    <div class="show-box">
      <van-loading size="24px" vertical v-if="loading" color="lightgreen" type="spinner">加载中...</van-loading>
         <div class="tabbar">
          <van-tabs  line-height="0px" line-width="0px" v-model="active" @click="getData()" :swipeable=true :border=false title-active-color="#3fb5b0" title-inactive-color="#000">
            <van-tab  title="原提取车间" ></van-tab>
            <van-tab  title="固体制剂车间" ></van-tab>
            <van-tab  title="新建综合制剂车间" ></van-tab>
            <van-tab  title="GMP车间" ></van-tab>
            <van-tab  title="中试车间" ></van-tab>
            <van-tab  title="污水站" ></van-tab>
            <van-tab  title="锅炉房" ></van-tab>
            <van-tab  title="前处理车间" ></van-tab>
            <van-tab  title="提取二车间" ></van-tab>
            <van-tab  title="综合车间" ></van-tab>
            <van-tab  title="办公楼＼食堂" ></van-tab>
          </van-tabs>
      </div>
      <div class="date-choose">
        <van-datetime-picker
          v-model="currentDateStart"
          type="datetime"
          title="选择开始时间"
          :min-date="minDate"
          :max-date="maxDate"
          visible-item-count='1'
          cancel-button-text=' '
          @confirm="chooseStart()"
        />
      </div>
       <div class="date-choose">
        <van-datetime-picker
          v-model="currentDateEnd"
          type="datetime"
          title="选择结束时间"
          :min-date="minDate"
          :max-date="maxDate"
          visible-item-count='1'
          cancel-button-text=' '
          @confirm="chooseEnd()"
        />
      </div>
      <div class="compare">
        <div class="c1" :class="{switchbgc:bgc1}" @click="switchShow1()">
          <div class="icon electric"></div>
          <div class="dw electric1">kwh</div>
          <div class="number">{{electric}}</div>
        </div>
         <div class="c2" :class="{switchbgc:bgc2}" @click="switchShow2()">
          <div class="icon water"></div>
          <div class="dw water">T</div>
          <div class="number">{{water}}</div>
        </div>
        <div class="c3" :class="{switchbgc:bgc3}" @click="switchShow3()">
          <div class="icon steam"></div>
          <div class="dw">T</div>
          <div class="number">{{steam}}</div>
        </div>
      </div>
      <div class="show-banner"  v-if="this.kind==='电'">
         <div class="header">电能明细</div>
                <div class="body">
                    <van-row justify='center'>
                      <van-col span="8">尖时刻</van-col>
                      <van-col span="8">用量</van-col>
                      <van-col span="8">成本</van-col>
                    </van-row>
                    <van-row justify='center'>
                      <van-col span="8"></van-col>
                      <van-col span="8">{{bovalue}}</van-col>
                      <van-col span="8">{{bocost}}</van-col>
                    </van-row>
              </div>
              <div class="body2">
                    <van-row justify='center'>
                     <van-col span="8">峰时刻</van-col>
                      <van-col span="8">用量</van-col>
                      <van-col span="8">成本</van-col>
                    </van-row>
                    <van-row justify='center'>
                      <van-col span="8"></van-col>
                      <van-col span="8">{{fenvalue}}</van-col>
                      <van-col span="8">{{fencost}}</van-col>
                    </van-row>
              </div>
              <div class="body3">
                    <van-row justify='center'>
                     <van-col span="8">平时刻</van-col>
                      <van-col span="8">用量</van-col>
                      <van-col span="8">成本</van-col>
                    </van-row>
                    <van-row justify='center'>
                      <van-col span="8"></van-col>
                      <van-col span="8">{{pinvalue}}</van-col>
                      <van-col span="8">{{pincost}}</van-col>
                    </van-row>
              </div>
              <div class="body4">
                    <van-row justify='center'>
                     <van-col span="8">谷时刻</van-col>
                      <van-col span="8">用量</van-col>
                      <van-col span="8">成本</van-col>
                    </van-row>
                    <van-row justify='center'>
                      <van-col span="8"></van-col>
                      <van-col span="8">{{guvalue}}</van-col>
                      <van-col span="8">{{gucost}}</van-col>
                    </van-row>
              </div>
      </div>
      <div class="show-banner" v-if="this.kind==='水'">
         <div class="header">水能明细</div>
                <div class="body">
                     <van-row justify='center'>
                     <van-col span="8">灌溉水</van-col>
                      <van-col span="8">水能耗</van-col>
                      <van-col span="8">水成本</van-col>
                    </van-row>
                     <van-row justify='center'>
                     <van-col span="8"></van-col>
                      <van-col span="8">{{waterGG}}</van-col>
                      <van-col span="8">{{waterGGcost}}</van-col>
                    </van-row>
              </div>
              <div class="body2">
                     <van-row justify='center'>
                     <van-col span="8">饮用水</van-col>
                      <van-col span="8">水能耗</van-col>
                      <van-col span="8">水成本</van-col>
                    </van-row>
                     <van-row justify='center'>
                     <van-col span="8"></van-col>
                      <van-col span="8">{{waterYY}}</van-col>
                      <van-col span="8">{{waterYYcost}}</van-col>
                    </van-row>
              </div>
              <div class="body3">
                     <van-row justify='center'>
                     <van-col span="8">深井水</van-col>
                      <van-col span="8">水能耗</van-col>
                      <van-col span="8">水成本</van-col>
                    </van-row>
                     <van-row justify='center'>
                     <van-col span="8"></van-col>
                      <van-col span="8">{{waterSJ}}</van-col>
                      <van-col span="8">{{waterSJcost}}</van-col>
                    </van-row>
              </div>
              <div class="body4">
                     <van-row justify='center'>
                     <van-col span="8">总和</van-col>
                      <van-col span="8">总能耗</van-col>
                      <van-col span="8">总成本</van-col>
                    </van-row>
                     <van-row justify='center'>
                     <van-col span="8"></van-col>
                      <van-col span="8">{{water}}t</van-col>
                      <van-col span="8">{{waterCost}}</van-col>
                    </van-row>
              </div>
      </div>
      <div class="show-banner1" v-if="this.kind==='汽'">
        <div class="header">汽能明细</div>
        <div class="body">
                  <van-row justify='center'>
                     <van-col span="8">汽</van-col>
                      <van-col span="8">汽能耗</van-col>
                      <van-col span="8">汽成本</van-col>
                  </van-row>
                  <van-row justify='center'>
                     <van-col span="8"></van-col>
                      <van-col span="8">{{steam}}t</van-col>
                      <van-col span="8">{{steamCost}}元</van-col>
                  </van-row>
        </div>
        <div class="body2">
                    <van-row justify='center'>
                      <van-col span="8"></van-col>
                     <van-col span="8">单位</van-col>
                      <van-col span="8">类型</van-col>
                  </van-row>
                  <van-row justify='center'>
                     <van-col span="8"></van-col>
                      <van-col span="8">{{steamUnit}}</van-col>
                      <van-col span="8">{{kind}}</van-col>
                  </van-row>
        </div>
      </div>
       </div>
</template>
<script>
var moment=require('moment')
export default {
    data(){
        return {
          currentDateStart:new Date(new Date()-24*60*60*1000),
          currentDateEnd:new Date(),
          minDate:new Date(2020, 0, 1),
          maxDate:new Date(2022, 10, 1),
          show: false,
          active:0,
          list:["原提取车间","固体制剂车间","新建综合制剂车间","GMP车间","中试车间","污水站","锅炉房","前处理车间","提取二车间","综合车间","办公楼＼食堂"],
          water:0,
          electric:0,
          steam:0,
          cost:'',
          bgc1:false,
          bgc2:false,
          bgc3:false,
          loading:false,
          kind:'电',
          currentchoice:'原提取车间',
          steamCost:'0',
          steamUnit:'0',
          waterGG:0,
          waterGGcost:0,
          waterYY:0,
          waterYYcost:0,
          waterSJ:0, 
          waterSJcost:0,
          waterCost:0,
          bovalue:0,
          bocost:0,
          fenvalue:0,
          fencost:0,
          pinvalue:0,
          pincost:0,
          guvalue:0,
          gucost:0
        }
    },
    created(){
      this.getData()
    },
    methods:{
      chooseStart(){
        if(new Date(this.currentDateStart).valueOf()>new Date(this.currentDateEnd).valueOf()){
          this.$toast.fail('开始时间大于结束时间')
          this.currentDateStart=new Date(new Date()-24*60*60*1000)
          return;
        }
         this.onConfirm(this.currentDateStart,this.currentDateEnd)
      },
      chooseEnd(){
         if(new Date(this.currentDateStart).valueOf()>new Date(this.currentDateEnd).valueOf()){
          this.$toast.fail('结束时间小于开始时间')
          this.currentDateEnd=new Date()
          return;
        }
         this.onConfirm(this.currentDateStart,this.currentDateEnd)
      },
      onConfirm(Starttime,Endtime) { //时间选择器的点击确定事件
         var compareDateStartTime = moment(Starttime).format('YYYY-MM-DD HH:mm:ss')
         var compareDateEndTime = moment(Endtime).format('YYYY-MM-DD HH:mm:ss')
         this.$http.all([
            this.$http.get('/api/energywater',{params:{StartTime:compareDateStartTime,EndTime:compareDateEndTime,AreaName:this.currentchoice}}),
            this.$http.get('/api/energyelectric',{params:{StartTime:compareDateStartTime,EndTime:compareDateEndTime,AreaName:this.currentchoice}}),
            this.$http.get('/api/energysteam',{params:{StartTime:compareDateStartTime,EndTime:compareDateEndTime,AreaName:this.currentchoice}}),
            this.$http.get('/api/watertrendlookboard',{params:{StartTime:compareDateStartTime,EndTime:compareDateEndTime,AreaName:this.currentchoice}}),
            this.$http.get('/api/electricnergycost',{params:{StartTime:compareDateStartTime,EndTime:compareDateEndTime,AreaName:this.currentchoice,TimeClass:'电'}})
            ]).then(this.$http.spread((res1,res2,res3,res4,res5)=>{
             this.water=JSON.parse(res1.data).value
             this.electric=JSON.parse(res2.data).value
             this.steam=JSON.parse(res3.data).value
             this.steamCost=JSON.parse(res3.data).cost
             this.steamUnit=JSON.parse(res3.data).unit
             this.waterGG = res4.data.GG+'t'
             this.waterGGcost=res4.data.GGcost+'元'
             this.waterYY = res4.data.YY+'t'
             this.waterYYcost=res4.data.YYcost+'元'
             this.waterSJ = res4.data.SJ+'t'
             this.waterSJcost=res4.data.GGcost+'元'
             this.waterCost = (res4.data.GGcost + res4.data.YYcost + res4.data.SJcost).toFixed(2)+'元'
             this.bovalue=res5.data.periodTimeTypeItem[0].expendEnergy+'kwh'
             this.bocost=res5.data.periodTimeTypeItem[0].expendPrice+'元'
             this.fenvalue=res5.data.periodTimeTypeItem[1].expendEnergy+'kwh'
             this.fencost=res5.data.periodTimeTypeItem[1].expendPrice+'元'
             this.pinvalue=res5.data.periodTimeTypeItem[2].expendEnergy+'kwh'
             this.pincost=res5.data.periodTimeTypeItem[2].expendPrice+'元'
             this.guvalue=res5.data.periodTimeTypeItem[3].expendEnergy+'kwh'
             this.gucost=res5.data.periodTimeTypeItem[3].expendPrice+'元'
              }))
      },
      switchShow1(){
      this.kind='电'
      this.bgc1=!this.bgc1
      this.bgc2=this.bgc3=false
      if(this.bgc1){
        this.$toast('当前显示电数据')
       }
      },
      switchShow2(){
       this.bgc2=!this.bgc2
       this.bgc1=this.bgc3=false
       this.kind='水'
       if(this.bgc2){
         this.$toast('当前显示水数据')
       }
      },
      switchShow3(){
       this.bgc1=this.bgc2=false
       this.bgc3=!this.bgc3
       this.kind='汽'
       if(this.bgc3){
         this.$toast('当前显示汽数据')
       }
      },
        //点击导航栏获取相关能耗数据
        getData(){
          this.currentchoice=this.list[this.active]
          var nowTime = moment().format('HH:mm').substring(0,4) + "0"
          var todayStartTime = new Date(moment().format('YYYY-MM-DD') + " 00:00")
          var todayEndTime = new Date(moment().format('YYYY-MM-DD') + " " + nowTime)
          this.currentDateStart= new Date(moment().format('YYYY-MM-DD') + " 00:00"),
          this.currentDateEnd=new Date(),
          this.onConfirm(todayStartTime,todayEndTime)
              }
    }
}
</script>
<style lang="less" scoped>
    @bgca:#3D4048FF;
    @bgcc:#eee;
    @bgct:#ccc;
     .show-box{
        position: relative;
        width: 375px;
        height:800px;
        box-sizing: border-box;
        padding: 0 12px 12px 13px;
        background: @bgcc;
        .tabbar{
          position: relative;
          padding-top: 10px;
          height: 25px;
          font-size:14px;
          font-family:PingFang SC;
          font-weight:400;
          line-height:25px;
          color:rgba(255,255,255,1);
          opacity:1;
          margin-bottom: 20px;
        }
        .date-choose{
          height: 120px;
          width: 100%;
        }
        .compare{
          width:100%;
          height:150px;
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
            top: 58px;
            width: 15px;
            height: 11px;
            font-size:8px;
            font-family:PingFang SC;
            font-weight:400;
            line-height:11px;
            color:rgba(20, 20, 20,1);
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
            top: 85px;
            text-align: center;
            width:97px;
            height:22px;
            overflow: hidden;
            text-overflow: hidden;
            background:#ccc;
            box-shadow:0px 0px 6px rgba(255,255,255,0.16);
            border-radius:4px;
            font-size:16px;
            font-family:PingFang SC;
            font-weight:500;
            color:rgb(20, 20, 20);
            letter-spacing:1px;
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
            height:150px;
            background:#ccc;
            float: left;
            margin-right: 20px;
            border-radius:4px;
          }
          .c2{
            position: relative;
            height:150px;
            width:103px;
            background:#ccc;
            float: left;
            margin-right: 20px;
            border-radius:4px;
          }
          .c3{
            position: relative;
            width: 103px;
            height:150px;
            float: left;
            background:#ccc;
            border-radius:4px;
            .number{
              left:6px;
            }
          }
          .switchbgc{
            background-color: #fff;
            .number{
              background-color:#fff;
            }
          }
        }
        .show-banner{
          position: relative;
          height: 260px;
          width: 100%;
          margin-bottom: 17px;
          background: #ccc;
          border-radius: 4px;
        }
          .show-banner1{
             position: relative;
             height: 160px;
             width: 100%;
             margin-bottom: 17px;
             background: #ccc;
             border-radius: 4px;
          }
            .header{
              position: relative;
                width: 100%;
                height:20px;
                padding-top: 10px;
                padding-bottom: 15px;
                text-align: center;
                font-size:16px;
                font-family:PingFang SC;
                font-weight:500;
                line-height:20px;
                color:#000;
                opacity:1;
            }
            .body,.body2,.body3,.body4{
                position: relative;
                height: 55px;
            }
     }
</style>