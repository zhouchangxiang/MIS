<template>
    <div class="show-box">
           <div class="date-box">
               <div class="tips">
                   <van-tabs type="card" title-active-color="#1E222B"  title-inactive-color="#fff" v-model="choosekind" @click="ChooseKind($event)">
                        <van-tab title="水"></van-tab>
                        <van-tab title="电"></van-tab>
                        <van-tab title="气"></van-tab>
                    </van-tabs>
               </div>
           </div>
           <div class="contain-body">
                <div class="left-box">
                    <van-sidebar v-model="activeKey" @change="onChange">
                        <van-sidebar-item title="原提取车间"  />
                        <van-sidebar-item title="固体制剂车间" />
                        <van-sidebar-item title="新建综合制剂车间" />
                        <van-sidebar-item title="GMP车间" />
                        <van-sidebar-item title="中试车间" />
                        <van-sidebar-item title="污水站" />
                        <van-sidebar-item title="锅炉房" />
                        <van-sidebar-item title="前处理车间" />
                        <van-sidebar-item title="提取二车间" />
                        <van-sidebar-item title="综合车间" />
                        <van-sidebar-item title="办公楼＼食堂" />
                    </van-sidebar>
                </div>
                <div class="bigbox" v-if="this.currentkind==='水'">
                <div class="list-banner" v-if="this.currentArea==='污水站'">
                    <div class="body">
                        <div class='today-water'>灌溉水DN40</div>
                        <div class='today-num1'>{{waterTagList.W_Area_WSZ_16_2_34.sumValue}}</div>
                        <div class='today-consume-rank'>{{ waterTagList.W_Area_WSZ_16_2_34.flowValue }}</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='锅炉房'">
                    <div class="body">
                        <div class='today-water'>锅炉房</div>
                        <div class='today-num1'>无详细数据</div>
                    </div>
                </div>
                 <div class="list-banner" v-if="this.currentArea==='提取二车间'">
                    <div class="body">
                        <div class='today-water'>后走廊灌溉水DN40</div>
                        <div class='today-num1'>{{waterTagList.W_Area_TQR_17_2_8.sumValue}}</div>
                        <div class='today-consume-rank'>{{ waterTagList.W_Area_TQR_17_2_8.flowValue}}</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='提取二车间'">
                    <div class="body">
                        <div class='today-water'>出料电梯旁饮用水DN100</div>
                        <div class='today-num1'>{{waterTagList.W_Area_TQR_17_1_9.sumValue}}</div>
                        <div class='today-consume-rank'>{{ waterTagList.W_Area_TQR_17_1_9.flowValue}}</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='综合车间'">
                    <div class="body">
                        <div class='today-water'>带干辅机灌溉水DN40</div>
                        <div class='today-num1'>{{waterTagList.W_Area_ZH_23_2_13.sumValue}}</div>
                        <div class='today-consume-rank'>{{waterTagList.W_Area_ZH_23_2_13.flowValue}}</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='综合车间'">
                    <div class="body">
                        <div class='today-water'>2楼会议室饮用水DN150</div>
                        <div class='today-num1'>{{waterTagList.W_Area_ZH_23_1_12.sumValue}}</div>
                        <div class='today-consume-rank'>{{waterTagList.W_Area_ZH_23_1_12.flowValue}}</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='新建综合制剂车间'">
                    <div class="body">
                        <div class='today-water'>包材库灌溉水DN50</div>
                        <div class='today-num1'>{{waterTagList.W_Area_XJZ_12_1_3.sumValue}}</div>
                        <div class='today-consume-rank'>{{waterTagList.W_Area_XJZ_12_1_3.flowValue}}</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='新建综合制剂车间'">
                    <div class="body">
                        <div class='today-water'>接待室饮用水DN100</div>
                        <div class='today-num1'>{{waterTagList.W_Area_XJZ_12_2_5.sumValue}}</div>
                        <div class='today-consume-rank'>{{waterTagList.W_Area_XJZ_12_2_5.flowValue}}</div>
                    </div>
                </div>
                 <div class="list-banner" v-if="this.currentArea==='中试车间'">
                    <div class="body">
                        <div class='today-water'>消防水DN100</div>
                        <div class='today-num1'>{{waterTagList.W_Area_YF_26_1_15.sumValue}}</div>
                        <div class='today-consume-rank'>{{waterTagList.W_Area_YF_26_1_15.flowValue}}</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='原提取车间'">
                    <div class="body">
                        <div class='today-water'>消防水DN50</div>
                        <div class='today-num1'>{{waterTagList.W_Area_YTQ_39_1_30.sumValue}}</div>
                        <div class='today-consume-rank'>{{waterTagList.W_Area_YTQ_39_1_30.flowValue}}</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='原提取车间'">
                    <div class="body">
                        <div class='today-water'>灌溉水DN40</div>
                        <div class='today-num1'>{{waterTagList.W_Area_YTQ_39_2_30.sumValue}}</div>
                        <div class='today-consume-rank'>{{waterTagList.W_Area_YTQ_39_2_30.flowValue}}</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='前处理车间'">
                    <div class="body">
                        <div class='today-water'>洗药室灌溉水DN25</div>
                        <div class='today-num1'>{{waterTagList.W_Area_QCL_33_1_20.sumValue}}</div>
                        <div class='today-consume-rank'>{{waterTagList.W_Area_QCL_33_1_20.flowValue}}</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='GMP车间'">
                    <div class="body">
                        <div class='today-water'>消防水DN50</div>
                        <div class='today-num1'>{{waterTagList.W_Area_JK_28_1_16.sumValue}}</div>
                        <div class='today-consume-rank'>{{waterTagList.W_Area_JK_28_1_16.flowValue}}</div>
                    </div>
                </div>
                 <div class="list-banner" v-if="this.currentArea==='GMP车间'">
                    <div class="body">
                        <div class='today-water'>消防水DN50</div>
                        <div class='today-num1'>{{waterTagList.W_Area_JK_28_2_16.sumValue}}</div>
                        <div class='today-consume-rank'>{{waterTagList.W_Area_JK_28_2_16.flowValue}}</div>
                    </div>
                </div>
                 <div class="list-banner" v-if="this.currentArea==='固体制剂车间'">
                    <div class="body">
                        <div class='today-water'>男卫生间灌溉水DN40</div>
                        <div class='today-num1'>{{waterTagList.W_Area_GT_30_2_18.sumValue}}</div>
                        <div class='today-consume-rank'>{{waterTagList.W_Area_GT_30_2_18.flowValue}}</div>
                    </div>
                </div>
                 <div class="list-banner" v-if="this.currentArea==='固体制剂车间'">
                    <div class="body">
                        <div class='today-water'>纯化水站饮用水DN100</div>
                        <div class='today-num1'>{{waterTagList.W_Area_GT_30_1_19.sumValue}}</div>
                        <div class='today-consume-rank'>{{waterTagList.W_Area_GT_30_1_19.flowValue}}</div>
                    </div>
                </div>
                 <div class="list-banner" v-if="this.currentArea==='办公楼＼食堂'">
                    <div class="body">
                        <div class='today-water'>1楼卫生间深井水DN65</div>
                        <div class='today-num1'>{{waterTagList.W_Area_BGL_34_1_22.sumValue}}</div>
                        <div class='today-consume-rank'>{{waterTagList.W_Area_BGL_34_1_22.flowValue}}</div>
                    </div>
                </div>
            </div>
            <div class="bigbox" v-if="this.currentkind==='电'">
                <div class="list-banner" v-if="this.currentArea==='污水站'">
                    <div class="body">
                        <div class='today-water'>电表</div>
                        <div class='today-num1'>{{electricTagList.E_Area_WSZ_16_2_35.ZGL}}</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='锅炉房'">
                    <div class="body">
                        <div class='today-water'>电表</div>
                        <div class='today-num1'>暂无数据</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='新建综合制剂车间'">
                    <div class="body">
                        <div class='today-water'>电表（2楼配电室）</div>
                        <div class='today-num1'>{{electricTagList.E_Area_XJZ_11_2_7.ZGL}}</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='中试车间'">
                    <div class="body">
                        <div class='today-water'>电表（化验室</div>
                        <div class='today-num1'>{{electricTagList.E_Area_YF_26_1_14.ZGL}}</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='原提取车间'">
                    <div class="body">
                        <div class='today-water'>电表（老醇提）</div>
                        <div class='today-num1'>{{electricTagList.E_Area_YTQ_38_1_28.ZGL}}</div>
                    </div>
                </div>
                 <div class="list-banner" v-if="this.currentArea==='前处理车间'">
                    <div class="body">
                        <div class='today-water'>电表（前处理）</div>
                        <div class='today-num1'>{{electricTagList.E_Area_YTQ_38_2_29.ZGL}}</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='GMP车间'">
                    <div class="body">
                        <div class='today-water'>电表（一楼）</div>
                        <div class='today-num1'>{{electricTagList.E_Area_JK_28_2_17.ZGL}}</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='固体制剂车间'">
                    <div class="body">
                        <div class='today-water'>电表</div>
                        <div class='today-num1'>{{electricTagList.E_Area_GT_30_1_19.ZGL}}</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='办公楼＼食堂'">
                    <div class="body">
                        <div class='today-water'>电表</div>
                        <div class='today-num1'>{{electricTagList.E_Area_BGL_36_1_26.ZGL}}</div>
                    </div>
                </div>
             </div>
        <div class="bigbox" v-if="this.currentkind==='汽'">
                <div class="list-banner" v-if="this.currentArea==='中试车间'">
                    <div class="body">
                        <div class='today-water'>蒸汽表</div>
                        <div class='today-num1'>{{steamTagList.S_Area_YF_25_1_502.sumValue}}</div>
                        <div class='today-consume-rank'>{{steamTagList.S_Area_YF_25_1_502.flowValue}}</div>
                        <div class='today-consume-rank2'>{{steamTagList.S_Area_YF_25_1_502.SteamWD}}°C</div>
                    </div>
                </div>
                 <div class="list-banner" v-if="this.currentArea==='锅炉房'">
                    <div class="body">
                        <div class='today-water'>锅炉总流量计DN400</div>
                        <div class='today-num1'>{{steamGlTag.sumValue}}</div>
                        <div class='today-consume-rank'>{{steamGlTag.flowValue}}</div>
                        <div class='today-consume-rank2'>{{steamGlTag.SteamWD}}°C</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='原提取车间'">
                    <div class="body">
                        <div class='today-water'>蒸汽表</div>
                        <div class='today-num1'>{{steamTagList.S_Area_YTQ_40_1_502.sumValue}}</div>
                        <div class='today-consume-rank'>{{steamTagList.S_Area_YTQ_40_1_502.flowValue}}</div>
                        <div class='today-consume-rank2'>{{steamTagList.S_Area_YTQ_40_1_502.SteamWD}}°C</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='前处理车间'">
                    <div class="body">
                        <div class='today-water'>蒸汽表</div>
                        <div class='today-num1'>{{steamTagList.S_Area_YTQ_40_2_502.sumValue}}</div>
                        <div class='today-consume-rank'>{{steamTagList.S_Area_YTQ_40_2_502.flowValue}}</div>
                        <div class='today-consume-rank2'>{{steamTagList.S_Area_YTQ_40_2_502.SteamWD}}°C</div>
                    </div>
                </div>
                 <div class="list-banner" v-if="this.currentArea==='GMP车间'">
                    <div class="body">
                        <div class='today-water'>蒸汽表</div>
                        <div class='today-num1'>{{steamTagList.S_Area_JK_27_1_502.sumValue}}</div>
                        <div class='today-consume-rank'>{{steamTagList.S_Area_JK_27_1_502.flowValue}}</div>
                        <div class='today-consume-rank2'>{{steamTagList.S_Area_JK_27_1_502.SteamWD}}°C</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='提取二车间'">
                    <div class="body">
                        <div class='today-water'>锅炉流量计DN400</div>
                        <div class='today-num1'>{{steamGlTag.sumValue}}</div>
                        <div class='today-consume-rank'>{{steamGlTag.flowValue}}</div>
                        <div class='today-consume-rank2'>{{steamGlTag.SteamWD}}°C</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='固体制剂车间'">
                    <div class="body">
                        <div class='today-water'>固体分汽缸流量计DN100</div>
                        <div class='today-num1'>{{steamTagList.S_Area_GT_31_1_502.sumValue}}</div>
                        <div class='today-consume-rank'>{{steamTagList.S_Area_GT_31_1_502.flowValue}}</div>
                        <div class='today-consume-rank2'>{{steamTagList.S_Area_GT_31_1_502.SteamWD}}°C</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='新建综合制剂车间'">
                    <div class="body">
                        <div class='today-water'>新制剂分汽缸DN200</div>
                        <div class='today-num1'>{{steamTagList.S_Area_XJZ_13_1_7_502.sumValue}}</div>
                        <div class='today-consume-rank'>{{steamTagList.S_Area_XJZ_13_1_7_502.flowValue}}</div>
                        <div class='today-consume-rank2'>{{steamTagList.S_Area_XJZ_13_1_7_502.SteamWD}}°C</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='综合车间'">
                    <div class="body">
                        <div class='today-water'>120带干DN32</div>
                        <div class='today-num1'>{{steamTagList.S_Area_ZH_21_2_502.sumValue}}</div>
                        <div class='today-consume-rank'>{{steamTagList.S_Area_ZH_21_2_502.flowValue}}</div>
                        <div class='today-consume-rank2'>{{steamTagList.S_Area_ZH_21_2_502.SteamWD}}°C</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='综合车间'">
                    <div class="body">
                        <div class='today-water'>流化床制粒DN50</div>
                        <div class='today-num1'>{{steamTagList.S_Area_ZH_21_1_502.sumValue}}</div>
                        <div class='today-consume-rank'>{{ steamTagList.S_Area_ZH_21_1_502.flowValue}}</div>
                        <div class='today-consume-rank2'>{{steamTagList.S_Area_ZH_21_1_502.SteamWD}}°C</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='综合车间'">
                    <div class="body">
                        <div class='today-water'>锅炉流量计DN400</div>
                        <div class='today-num1'>{{steamGlTag.sumValue}}</div>
                        <div class='today-consume-rank'>{{ steamGlTag.flowValue}}</div>
                        <div class='today-consume-rank2'>{{steamGlTag.SteamWD}}°C</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='综合车间'">
                    <div class="body">
                        <div class='today-water'>二次浓缩DN100</div>
                        <div class='today-num1'>{{steamTagList.S_Area_ZH_46_1_502.sumValue}}</div>
                        <div class='today-consume-rank'>{{ steamTagList.S_Area_ZH_46_1_502.flowValue}}</div>
                        <div class='today-consume-rank2'>{{steamTagList.S_Area_ZH_46_1_502.SteamWD}}°C</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='综合车间'">
                    <div class="body">
                        <div class='today-water'>醇提+浓缩DN150</div>
                        <div class='today-num1'>{{steamTagList.S_Area_ZH_46_2_502.sumValue}}</div>
                        <div class='today-consume-rank'>{{ steamTagList.S_Area_ZH_46_2_502.flowValue}}</div>
                        <div class='today-consume-rank2'>{{steamTagList.S_Area_ZH_46_2_502.SteamWD}}°C</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='综合车间'">
                    <div class="body">
                        <div class='today-water'>双效浓缩/CIP DN200</div>
                        <div class='today-num1'>{{steamTagList.S_Area_ZH_46_3_502.sumValue}}</div>
                        <div class='today-consume-rank'>{{ steamTagList.S_Area_ZH_46_3_502.flowValue}}</div>
                        <div class='today-consume-rank2'>{{steamTagList.S_Area_ZH_46_3_502.SteamWD}}°C</div>
                    </div>
                </div>
                 <div class="list-banner" v-if="this.currentArea==='综合车间'">
                    <div class="body">
                        <div class='today-water'>提取双号DN150</div>
                        <div class='today-num1'>{{steamTagList.S_Area_ZH_22_1_502.sumValue}}</div>
                        <div class='today-consume-rank'>{{steamTagList.S_Area_ZH_22_1_502.flowValue}}</div>
                        <div class='today-consume-rank2'>{{steamTagList.S_Area_ZH_22_1_502.SteamWD}}°C</div>
                    </div>
                </div>
                 <div class="list-banner" v-if="this.currentArea==='综合车间'">
                    <div class="body">
                        <div class='today-water'>提取单号DN150</div>
                        <div class='today-num1'>{{steamTagList.S_Area_ZH_21_3_502.sumValue}}</div>
                        <div class='today-consume-rank'>{{ steamTagList.S_Area_ZH_21_3_502.flowValue}}</div>
                        <div class='today-consume-rank2'>{{steamTagList.S_Area_ZH_22_3_502.SteamWD}}°C</div>
                    </div>
                </div>
                <div class="list-banner" v-if="this.currentArea==='办公楼＼食堂'">
                    <div class="body">
                        <div class='today-water'>蒸汽表</div>
                        <div class='today-num1'>{{steamTagList.S_Area_BGL_35_1_502.sumValue}}</div>
                        <div class='today-consume-rank'>{{steamTagList.S_Area_BGL_35_1_502.flowValue}}</div>
                        <div class='today-consume-rank2'>{{steamTagList.S_Area_BGL_35_1_502.SteamWD}}°C</div>
                    </div>
                </div>
           </div>
        </div> 
    </div>
</template>
<script>
var moment=require('moment')
export default {
    data () {
        return {
        myArea:'',
        activeKey: 0,
        CompareDate:Date.now() - 3600 * 1000 * 24,
        choosekind:0,
        kind:['水','电','汽'],
        currentkind:'水',
        Allarea:["原提取车间","固体制剂车间","新建综合制剂车间","GMP车间","中试车间","污水站","锅炉房","前处理车间","提取二车间","综合车间","办公楼＼食堂"],
        currentArea:'原提取车间',
        flag:false,
        websoc:null,
        waterTagList:{},
        electricTagList:{},
        steamTagList:{},
        steamGlTag:{}
      }
    },
    created(){
        this.initOperation();
    },
     destroyed(){
      if(this.websoc){
      this.websoc.close()
      }
    },
    methods:{
        ChooseKind(e){
           this.currentkind=this.kind[e]
            if(this.websoc){
            this.websoc.close()
            }
        },
        initOperation(){
           this.initWebSocket()
           this.getGlSteamLabel()
        },
      onChange(index){
        this.currentArea=this.Allarea[index]
         if(this.websoc){
            this.websoc.close()
            }
           this.initWebSocket()
    },
    getGlSteamLabel(){
      this.$http.get("/api/steamtotal").then(res =>{
        this.steamGlTag = res.data.S_AllArea_Value
      })
    },
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
         this.webscsend()
        },
        webscom(evt){
          var resdata = JSON.parse(evt.data); //获取到实时返回的数据
          this.electricTagList = resdata[0].electric
          this.steamTagList = resdata[0].steam
          this.waterTagList = resdata[0].water
        },
        webscoer(){
            console.log('连接websocket失败')
        },
        webscoclos(e){
            console.log('关闭websocket连接')
        }
    }
}
</script>
<style lang="less" scoped>
    .show-box{
        position:relative;
        width:375px;
        height:850px;
        box-sizing: border-box;
        background-color: #eee;
        padding: 0 12px 12px 13px;
        .date-box{
            height:18px;
            opacity:1;
            border-radius:4px;
            color:#000;
            font-size: 10px;
            .tips{
                float: left;
                margin-right: 20px;
                background-color:#1E222B;
                height: 18px;
            }
        }
        .show{
            position: relative;
            width: 20%;
            background-color: #eee;
            margin-top: 15px;
            .roundpic{
            position: relative;
            height: 170px;
            }
            .listpic{
            position: relative;
            top:10px;
            width: 100%;
            height: 150px;
            overflow: hidden;
            margin-top: 17px;
            border-radius: 4px;
            background-color:#ccc;
            }
        }
        .left-box{
            position: relative;
            float: left;
            width: 100px;
            margin-top:20px;
            width: 100px;
            height: 800px;
            border-radius: 4px;
            background: #eee;
        }
        .bigbox{
            float: left;
            position: relative;
            margin-top:20px;
            margin-left: 20px;
            width: 230px;
            height: 850px;
            border-radius: 4px;
            background: #eee; 
        }
        .list-banner{
            position: relative;
            width: 230px;
            height: 150px;
            border-radius: 4px;
            background: #ccc;
            .body{
                position: relative;
                .today-water{
                position: absolute;
                top:10px;
                left:10px;
                height:11px;
                font-size:12px;
                font-family:PingFang SC;
                font-weight:400;
                line-height:11px;
                color:#000;
                opacity:1;
                }
                .today-consume-rank,.today-consume-rank2{
                position: absolute;
                top:65px;
                left:10px;
                width: 80%;
                height: 18px;
                background-color: #333;
                font-size:10px;
                font-family:PingFang SC;
                font-weight:400;
                line-height:18px;
                color:green;
                opacity:1;
                }
                .today-num1{
                    .today-consume-rank();
                    top:35px;
                }
                .today-consume-rank2{
                    top:95px;
                }
            }

        }
    }
</style>