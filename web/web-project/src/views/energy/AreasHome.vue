<template>
  <el-row :gutter="15">
    <el-col :span="24" style="margin-bottom: 15px;">
      <el-col :span="8">
        <div class="platformContainer">
          <el-col :span="6">
            <div class="iconBlock float-left" style="color: #FB8A06;">
              <i class="fa fa-flash fa-2x"></i>
            </div>
          </el-col>
          <el-col :span="18">
            <div class="itemMarginBottom text-size-normol text-color-info-shallow">本日耗电量</div>
            <div class="itemMarginBottom text-size-big text-color-info">{{ todayElectricity }}</div>
            <div class="itemMarginBottom">
              <span class="text-size-mini text-color-info-shallow">今日电费</span>
              <span class="text-size-mini text-color-info-shallow float-right">对比昨日</span>
            </div>
            <div class="itemMarginBottom">
              <span class="text-size-normol text-color-info">523.5元</span>
              <span class="text-size-normol float-right">+9.5%</span>
            </div>
          </el-col>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="platformContainer">
          <el-col :span="6">
            <div class="iconBlock float-left" style="color: #228AD5;">
              <i class="fa fa-tint fa-2x"></i>
            </div>
          </el-col>
          <el-col :span="18">
            <div class="itemMarginBottom text-size-normol text-color-info-shallow">本日耗水量</div>
            <div class="itemMarginBottom text-size-big text-color-info">{{ todayWater }}</div>
            <div class="itemMarginBottom">
              <span class="text-size-mini text-color-info-shallow">今日水费</span>
              <span class="text-size-mini text-color-info-shallow float-right">对比昨日</span>
            </div>
            <div class="itemMarginBottom">
              <span class="text-size-normol text-color-info">523.5元</span>
              <span class="text-size-normol float-right">+9.5%</span>
            </div>
          </el-col>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="platformContainer">
          <el-col :span="6">
            <div class="iconBlock float-left" style="color: #15CC48;">
              <i class="fa fa-tachometer fa-2x"></i>
            </div>
          </el-col>
          <el-col :span="18">
            <div class="itemMarginBottom text-size-normol text-color-info-shallow">本日耗汽量</div>
            <div class="itemMarginBottom text-size-big text-color-info">{{ todaySteam }}</div>
            <div class="itemMarginBottom">
              <span class="text-size-mini text-color-info-shallow">今日汽费</span>
              <span class="text-size-mini text-color-info-shallow float-right">对比昨日</span>
            </div>
            <div class="itemMarginBottom">
              <span class="text-size-normol text-color-info">523.5元</span>
              <span class="text-size-normol float-right">+9.5%</span>
            </div>
          </el-col>
        </div>
      </el-col>
    </el-col>
    <el-col :span="24">
      <el-col :span="6">
        <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
          <div class="chartTile">生产详情</div>
        </div>
        <div class="platformContainer" style="margin-bottom:2px;">
          <el-table :data="batchTableData" style="width: 100%">
            <el-table-column prop="Name" label="品名"></el-table-column>
            <el-table-column prop="Batch" label="批次"></el-table-column>
          </el-table>
        </div>
        <div class="platformContainer">
          <el-col :span="24">
            <div class="itemMarginBottom">
              <span class="text-size-normol text-color-info-shallow">今日品名数</span>
              <span class="text-size-normol text-color-info-shallow float-right">今日总成本</span>
            </div>
            <div class="itemMarginBottom">
              <span class="text-size-normol text-color-info">2</span>
              <span class="text-size-normol text-color-info float-right">24562.23元</span>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="itemMarginBottom">
              <span class="text-size-normol text-color-info-shallow">今日批次数</span>
            </div>
            <div class="itemMarginBottom">
              <span class="text-size-normol text-color-info">5</span>
            </div>
          </el-col>
          <el-col :span="12">
            <ve-ring :data="ringChartData" :settings="batchChartSettings" :extend="batchChartExtend" width="100%" height="100px"></ve-ring>
          </el-col>
        </div>
      </el-col>
      <el-col :span="13">
        <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
          <div class="chartTile">数据表</div>
          <el-select v-model="EnergyValue" size="mini">
            <el-option v-for="item in EnergyOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
        </div>
        <div class="platformContainer">

        </div>
      </el-col>
      <el-col :span="5">
        <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
          <div class="chartTile">设备情况</div>
        </div>
        <div class="platformContainer">

        </div>
      </el-col>
    </el-col>
  </el-row>
</template>

<script>
  var moment = require('moment');
  export default {
    name: "AreasHome",
    inject:['newAreaName'],
    data(){
      return {
        todayElectricity:"",
        todayWater:"",
        todaySteam:"",
        EnergyOptions: [{
          value: '电',
          label: '电能'
        }, {
          value: '水',
          label: '水能'
        }, {
          value: '汽',
          label: '汽能'
        }],
        EnergyValue:'电',
        batchTableData:[
          {Name:"药品A",Batch:"JUSA2374627"},
          {Name:"药品B",Batch:"JUSA2374627"},
          {Name:"药品C",Batch:"JUSA2374627"},
          {Name:"药品D",Batch:"JUSA2374627"},
        ],
        batchChartSettings: {
          radius: [20,40],
          offsetY:"50px",
          label:{
            show:false
          },
          labelLine:{
            show:false
          }
        },
        batchChartExtend: {
          legend:{
            show:false
          }
        },
        ringChartData: {
          columns: ['日期', '访问用户'],
          rows: [
            { '日期': '药品A', '访问用户': 1393 },
            { '日期': '药品B', '访问用户': 3530 },
            { '日期': '药品C', '访问用户': 2923 },
            { '日期': '药品D', '访问用户': 1723 }
          ]
        }
      }
    },
    created(){
      this.getEnergyPreview()
    },
    methods:{
      getEnergyPreview(){
        var that = this
        var nowTime = moment().format('HH:mm').substring(0,4) + "0"
        var todayStartTime = moment().format('YYYY-MM-DD') + " 00:00"
        var todayEndTime = moment().format('YYYY-MM-DD') + " " + nowTime
        var params = {}
        if(this.newAreaName.areaName == "整厂区"){
          params.StartTime = todayStartTime
          params.EndTime = todayEndTime
        }else{
          params.StartTime = todayStartTime
          params.EndTime = todayEndTime
          params.Area = this.newAreaName.areaName
        }
        this.axios.all([
          this.axios.get("/api/energyelectric",{params: params}),//获取今天电
          this.axios.get("/api/energywater",{params: params}),//获取今天水
          this.axios.get("/api/energysteam",{params: params}),//获取今天汽
        ]).then(this.axios.spread(function(todayElectricity,todayWater,todaySteam){
          var todayElectricityData = JSON.parse(todayElectricity.data)
          var todayWaterData = JSON.parse(todayWater.data)
          var todaySteamData = JSON.parse(todaySteam.data)
          that.todayElectricity = todayElectricityData.value +" "+ todayElectricityData.unit
          that.todayWater = todayWaterData.value +" "+ todayWaterData.unit
          that.todaySteam = todaySteamData.value +" "+ todaySteamData.unit
        }))
      }
    }
  }
</script>

<style scoped>
  .iconBlock{
    width: 60px;
    height: 60px;
    line-height: 60px;
    background: #082F4C;
    text-align: center;
  }
  .iconBlock i{
    border-radius: 4px;
    vertical-align: middle;
  }
</style>
