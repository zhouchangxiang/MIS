<template>
    <el-row :gutter="10">
      <el-col :span="24">
        <el-form :inline="true" :model="formParameters">
          <el-form-item label="时间：">
            <el-date-picker type="date" v-model="formParameters.date" :picker-options="pickerOptions" size="mini" format="yyyy-MM-dd" style="width: 130px;" :clearable="false"></el-date-picker>
          </el-form-item>
          <el-form-item style="float: right;">
            <el-radio-group v-model="formParameters.energy" fill="#082F4C" size="small">
              <el-radio-button v-for="item in energyList" :key="item.id" :label="item.name"></el-radio-button>
            </el-radio-group>
          </el-form-item>
        </el-form>
      </el-col>
      <el-col :span="24" v-if="newAreaName.areaName != '整厂区'">
        <el-col :span="18">
          <div class="energyDataCard">
            <ve-line :data="chartData" :settings="chartSettings" :extend="ChartExtend"></ve-line>
          </div>
          <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
            <div class="chartTile">尖峰平谷分析</div>
          </div>
          <div class="platformContainer">
            <el-row :gutter="20" style="margin-bottom: 10px;">
              <el-col :span="9">
                <p class="text-size-normol">尖时段</p>
                <span class="text-size-mini text-color-info-shallow">共{{ electricAnalyze.sharpTime }}小时</span>
                <el-row>
                  <el-col :span="14">
                    <el-progress :text-inside="true" :stroke-width="16" :percentage="electricAnalyze.sharp" color="#FB3A06"></el-progress>
                  </el-col>
                  <el-col :span="10">
                    <p class="text-color-info" style="padding-left: 10px;">耗能：253kwh</p>
                  </el-col>
                </el-row>
              </el-col>
              <el-col :span="9">
                <p class="text-size-normol">峰时段</p>
                <span class="text-size-mini text-color-info-shallow">共{{ electricAnalyze.peakTime }}小时</span>
                <el-row>
                  <el-col :span="14">
                    <el-progress :text-inside="true" :stroke-width="16" :percentage="electricAnalyze.peak" color="#FB8A06"></el-progress>
                  </el-col>
                  <el-col :span="10">
                    <p class="text-color-info" style="padding-left: 10px;">耗能：253kwh</p>
                  </el-col>
                </el-row>
              </el-col>
              <el-col :span="6">
                <p class="text-color-info-shallow" style="margin-bottom: 15px;">总电费：</p>
                <p>{{ electricAnalyze.total }}元</p>
              </el-col>
            </el-row>
            <el-row :gutter="20" style="margin-bottom: 10px;">
              <el-col :span="9">
                <p class="text-size-normol">平时段</p>
                <span class="text-size-mini text-color-info-shallow">共{{ electricAnalyze.poiseTime }}小时</span>
                <el-row>
                  <el-col :span="14">
                    <el-progress :text-inside="true" :stroke-width="16" :percentage="electricAnalyze.poise" color="#F8E71C"></el-progress>
                  </el-col>
                  <el-col :span="10">
                    <p class="text-color-info" style="padding-left: 10px;">耗能：253kwh</p>
                  </el-col>
                </el-row>
              </el-col>
              <el-col :span="9">
                <p class="text-size-normol">谷时段</p>
                <span class="text-size-mini text-color-info-shallow">共{{ electricAnalyze.ebbTime }}小时</span>
                <el-row>
                  <el-col :span="14">
                    <el-progress :text-inside="true" :stroke-width="16" :percentage="electricAnalyze.ebb" color="#15CC48"></el-progress>
                  </el-col>
                  <el-col :span="10">
                    <p class="text-color-info" style="padding-left: 10px;">耗能：253kwh</p>
                  </el-col>
                </el-row>
              </el-col>
              <el-col :span="6">
                <p class="text-color-info-shallow" style="margin-bottom: 15px;">平均电价：</p>
                <p>{{ electricAnalyze.average }}元</p>
              </el-col>
            </el-row>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="energyDataCard">
            <div class="realTimeCardTitle">实时数据 <span>kwh</span></div>
            <div class="realTimeData">22432</div>
            <div style="margin-top: 10px;"><span class="text-color-info-shallow">日累计能耗</span><span class="float-right text-color-info">4543.56kwh</span></div>
          </div>
          <div class="energyDataCard">
            <div class="energyDataItem">
              <div class="energyDataItemTitle">
                <el-date-picker type="date" v-model="contrastDate" :picker-options="pickerOptions" size="mini" format="yyyy-MM-dd" style="width: 130px;" :clearable="false"></el-date-picker>
              </div>
            </div>
            <div class="energyDataItem">
              <div class="energyDataItemTitle">今日能耗</div>
              <div class="energyDataItemData">2342.23 kwh</div>
            </div>
            <div class="energyDataItem">
              <div class="energyDataItemTitle">对比</div>
              <div class="energyDataItemData">+9.5% </div>
            </div>
          </div>
          <div class="energyDataCard">
            <div class="realTimeCardTitle" style="margin-bottom: 10px;">避峰用谷分析（参考）</div>
            <el-col :span="14">
              <p class="text-size-normol">尖时段</p>
              <span class="text-size-mini text-color-info-shallow">共{{ rationalAnalyze.sharpTime }}小时</span>
              <p><el-progress :text-inside="true" :stroke-width="16" :percentage="electricAnalyze.sharp" color="#FB3A06"></el-progress></p>
              <p class="text-size-normol" style="margin-top: 10px;">峰时段</p>
              <span class="text-size-mini text-color-info-shallow">共{{ rationalAnalyze.peakTime }}小时</span>
              <p><el-progress :text-inside="true" :stroke-width="16" :percentage="electricAnalyze.peak" color="#FB8A06"></el-progress></p>
              <p class="text-size-normol" style="margin-top: 10px;">平时段</p>
              <span class="text-size-mini text-color-info-shallow">共{{ rationalAnalyze.poiseTime }}小时</span>
              <p><el-progress :text-inside="true" :stroke-width="16" :percentage="electricAnalyze.poise" color="#F8E71C"></el-progress></p>
              <p class="text-size-normol" style="margin-top: 10px;">谷时段</p>
              <span class="text-size-mini text-color-info-shallow">共{{ rationalAnalyze.ebbTime }}小时</span>
              <p><el-progress :text-inside="true" :stroke-width="16" :percentage="electricAnalyze.ebb" color="#15CC48"></el-progress></p>
            </el-col>
            <el-col :span="10">
              <p class="text-size-normol text-color-info-shallow" style="margin-bottom: 15px;">总电费：</p>
              <p class="text-size-normol text-color-info" style="margin-bottom: 20px;">553545.5 元</p>
              <p class="text-size-normol text-color-info-shallow" style="margin-bottom: 15px;">平均电价：</p>
              <p class="text-size-normol text-color-info" style="margin-bottom: 20px;">0.89 元</p>
              <p class="text-size-normol text-color-info-shallow" style="margin-bottom: 15px;">建议：</p>
              <p class="text-size-mini text-color-danger">设备尽量在峰段（高电价）时刻检修，在平或谷（低电价）生产，可以降低能耗成本</p>
            </el-col>
          </div>
        </el-col>
      </el-col>
      <el-col :span="24" v-if="newAreaName.areaName == '整厂区'">
        <el-col :span="18">
          <div class="energyDataCard">
            <ve-line :data="chartData" :settings="chartSettings" :extend="ChartExtend"></ve-line>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="energyDataCard">
            <div class="realTimeCardTitle">实时数据 <span>kwh</span></div>
            <div class="realTimeData">22432</div>
            <div style="margin-top: 10px;"><span class="text-color-info-shallow">日累计能耗</span><span class="float-right text-color-info">4543.56kwh</span></div>
          </div>
          <div class="energyDataCard">
            <div class="energyDataItem">
              <div class="energyDataItemTitle">
                <el-date-picker type="date" v-model="contrastDate" :picker-options="pickerOptions" size="mini" format="yyyy-MM-dd" style="width: 130px;" :clearable="false"></el-date-picker>
              </div>
            </div>
            <div class="energyDataItem">
              <div class="energyDataItemTitle">今日能耗</div>
              <div class="energyDataItemData">2342.23 kwh</div>
            </div>
            <div class="energyDataItem">
              <div class="energyDataItemTitle">对比</div>
              <div class="energyDataItemData">+9.5% </div>
            </div>
          </div>
        </el-col>
        <el-col :span="24">
          <div class="energyDataCard">
            <ul class="colorBar">
              <li><i class="bg-dead"></i><span>停</span></li>
              <li><i class="bg-low"></i><span>低</span></li>
              <li><i class="bg-center"></i><span>中</span></li>
              <li><i class="bg-tall"></i><span>高</span></li>
            </ul>
            <ul class="gradientList">
              <li v-for="item in colorBarOption">
                <p>{{ item.name }}</p>
                <el-popover trigger="hover">
                  <div>0-4点：{{ item.value0 }}</div>
                  <div>4-8点：{{ item.value4 }}</div>
                  <div>8-12点：{{ item.value8 }}</div>
                  <div>12-16点：{{ item.value12 }}</div>
                  <div>16-20点：{{ item.value16 }}</div>
                  <div>20-24点：{{ item.value20 }}</div>
                  <div slot="reference" class="gradientColorItem" :style='{background:item.backgroundColor}'></div>
                </el-popover>
              </li>
            </ul>
          </div>
        </el-col>
      </el-col>
    </el-row>
</template>

<script>
    export default {
      name: "AreaPeriodTime",
      inject:['newAreaName'],
      data(){
        this.chartSettings = {
          area:true
        }
        this.ChartExtend = {
          title:{
            text:"能耗趋势"
          },
          grid:{
            left:'10px',
            right:'10px',
            bottom:'0',
            top:'50px'
          },
          series:{
            smooth: false
          }
        }
        return {
          formParameters:{
            date:Date.now(),
            energy:"电能"
          },
          energyList:[
            {name:"电能",id:1},
            {name:"水能",id:2},
            {name:"汽能",id:3},
          ],
          pickerOptions:{
            disabledDate(time) {
              return time.getTime() > Date.now();
            }
          },
          AllArea:false,
          chartData:{
            columns:["时间","能耗量"],
            rows:[
              {"时间":"00:00","能耗量":273},
              {"时间":"01:00","能耗量":303},
              {"时间":"02:00","能耗量":333},
              {"时间":"03:00","能耗量":293},
              {"时间":"04:00","能耗量":223},
              {"时间":"05:00","能耗量":313},
              {"时间":"06:00","能耗量":365},
              {"时间":"07:00","能耗量":""},
              {"时间":"08:00","能耗量":""},
              {"时间":"09:00","能耗量":""},
              {"时间":"10:00","能耗量":""},
              {"时间":"11:00","能耗量":""},
              {"时间":"12:00","能耗量":""}
            ]
          },
          electricAnalyze:{
            sharpTime:3,
            sharp:100,
            peakTime:7,
            peak:87.5,
            total:553524.5,
            poiseTime:6,
            poise:33.3,
            ebbTime:8,
            ebb:12.5,
            average:0.89,
          },
          rationalAnalyze:{
            sharpTime:3,
            sharp:100,
            peakTime:7,
            peak:87.5,
            poiseTime:6,
            poise:33.3,
            ebbTime:8,
            ebb:12.5,
            total:553524.5,
            average:0.89
          },
          colorBarOption:[
            {name: "新建综合制剂楼", value0: 2342,value4: 4234,value8: 2232,value12: 235,value16: 2042,value20: 264, backgroundColor: '-webkit-linear-gradient(left,#ECF1F4,#F5E866,#FB8A06,#FB3A06,#F5E866,#FB8A06)'},
            {name: "提取二车间", value0: 2342,value4: 2342,value8: 2342,value12: 2342,value16: 2342,value20: 2342, backgroundColor: '-webkit-linear-gradient(left,#ECF1F4,#F5E866,#FB8A06,#FB3A06,#F5E866,#FB8A06)'},
            {name: "新建综合制剂楼", value0: 2342,value4: 2342,value8: 2342,value12: 2342,value16: 2342,value20: 2342, backgroundColor: '-webkit-linear-gradient(left,#ECF1F4,#F5E866,#FB8A06,#FB3A06,#F5E866,#FB8A06)'},
            {name: "新建综合制剂楼", value0: 2342,value4: 2342,value8: 2342,value12: 2342,value16: 2342,value20: 2342, backgroundColor: '-webkit-linear-gradient(left,#ECF1F4,#F5E866,#FB8A06,#FB3A06,#F5E866,#FB8A06)'}
          ],
          contrastDate:Date.now()
        }
      },
      created(){

      },
      methods:{

      }
    }
</script>

<style scoped>
  .energyDataCard{
    width:100%;
    background:#fff;
    border-radius:4px;
    padding:15px;
    margin-bottom:10px;
    clear: both;
    overflow: hidden;
  }
  .colorBar{float:right;}
  .colorBar li{
    display: inline-block;
    margin-right: 20px;
  }
  .colorBar li i{
    display: inline-block;
    width: 16px;
    height: 16px;
    border-radius: 2px;
    margin-right: 15px;
    vertical-align: middle;
  }
  .colorBar li span{
    display: inline-block;
    color: #082F4C;
    font-size: 16px;
    vertical-align: middle;
  }
  .realTimeCardTitle{
    font-size: 18px;
    color: #082F4C;
  }
  .realTimeCardTitle span{
    float: right;
  }
  .realTimeData{
    margin-top: 20px;
    font-size: 30px;
    color: #082F4C;
  }
  .energyDataItem{
    display: table;
    margin-bottom: 20px;
    font-size: 18px;
  }
  .energyDataItemTitle{
    float: left;
    color: rgba(8,47,76,0.62);
    margin-right: 20px;
  }
  .energyDataItemData{
    float: left;
    color: #082F4C;
  }
</style>
