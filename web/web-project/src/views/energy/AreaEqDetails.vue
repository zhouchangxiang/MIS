<template>
    <el-row :gutter="10">
      <el-col :span="24">
        <el-form :model="formParameters">
          <el-form-item label="时间：" style="margin-bottom: 0;">
            <el-date-picker type="datetime" v-model="formParameters.startDate" :picker-options="pickerOptions" size="mini" style="width: 180px;" :clearable="false"></el-date-picker> ~
            <el-date-picker type="datetime" v-model="formParameters.endDate" :picker-options="pickerOptions" size="mini" style="width: 180px;" :clearable="false"></el-date-picker>
          </el-form-item>
          <el-form-item label="参数：">
            <el-radio-group v-model="formParameters.eqComponentValue" fill="#082F4C" size="small">
              <el-radio-button v-for="item in eqComponentList" :key="item.id" :label="item.name"></el-radio-button>
            </el-radio-group>
          </el-form-item>
        </el-form>
      </el-col>
      <el-col :span="24" v-if="formParameters.eqComponentValue === '安全/故障'">
        <el-col :span="8">
          <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
            <div class="chartTile">设备</div>
          </div>
          <div class="platformContainer" style="margin-bottom: 10px;">
            <el-table :data="TagDetailTableData" highlight-current-row ref="multipleTable" @selection-change="handleSelectionChange" @row-click="handleRowClick" v-loading="TagEqTableLoading" size="small" height="246px" max-height="246px" style="width: 100%">
              <el-table-column prop="AreaName" label="区域名称"></el-table-column>
              <el-table-column prop="FEFportIP" label="站点地址"></el-table-column>
              <el-table-column prop="EnergyClass" label="分类"></el-table-column>
              <el-table-column prop="IP" label="IP" width="100"></el-table-column>
              <el-table-column prop="COMNum" label="端口"></el-table-column>
            </el-table>
          </div>
        </el-col>
        <el-col :span="16">
          <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
            <div class="chartTile">
              设备信息
            </div>
          </div>
          <div class="platformContainer" style="margin-bottom:10px;" v-if="EnergyClass === '电'">
            <el-col :span="8">
              <div class="faultItemHead">
                <span>功率</span>
                <!--<p>额定功率/kw <span>{{  }}</span></p>-->
              </div>
              <div class="faultItemBody">
                <p style="padding: 29px 0;">有功功率/kwh <span>{{ forEqParameters.ZGL }}</span></p>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="faultItemHead">
                <span>电流</span>
              </div>
              <div class="faultItemBody">
                <p>A项电流 <span>{{ forEqParameters.AI }}</span></p>
                <p>B项电流 <span>{{ forEqParameters.BI }}</span></p>
                <p>C项电流 <span>{{ forEqParameters.CI }}</span></p>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="faultItemHead">
                <span>电压</span>
                <!--<p>额定电压/V <span>{{  }}</span></p>-->
              </div>
              <div class="faultItemBody">
                <p>A项电压 <span>{{ forEqParameters.AU }}</span></p>
                <p>B项电压 <span>{{ forEqParameters.BU }}</span></p>
                <p>C项电压 <span>{{ forEqParameters.CU }}</span></p>
              </div>
            </el-col>
          </div>
          <div class="platformContainer" style="margin-bottom:10px;" v-if="EnergyClass === '水'">
            <el-col :span="12">
              <div class="faultItemHead">
                <span>瞬时量</span>
              </div>
              <div class="faultItemBody">
                <p style="padding: 29px 0;">瞬时量<span>{{ forEqParameters.WaterF }}</span></p>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="faultItemHead">
                <span>累计量</span>
              </div>
              <div class="faultItemBody">
                <p style="padding: 29px 0;">累计量<span>{{ forEqParameters.WaterS }}</span></p>
              </div>
            </el-col>
          </div>
          <div class="platformContainer" style="margin-bottom:10px;" v-if="EnergyClass === '汽' || EnergyClass === '蒸汽总'">
            <el-col :span="6">
              <div class="faultItemHead">
                <span>瞬时量</span>
              </div>
              <div class="faultItemBody">
                <p style="padding: 29px 0;">瞬时量<span>{{ forEqParameters.SteamF }}</span></p>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="faultItemHead">
                <span>累计量</span>
              </div>
              <div class="faultItemBody">
                <p style="padding: 29px 0;">累计量<span>{{ forEqParameters.SteamS }}</span></p>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="faultItemHead">
                <span>体积</span>
              </div>
              <div class="faultItemBody">
                <p style="padding: 29px 0;">体积<span>{{ forEqParameters.SteamV }}</span></p>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="faultItemHead">
                <span>温度</span>
              </div>
              <div class="faultItemBody">
                <p style="padding: 29px 0;">温度<span>{{ forEqParameters.SteamWD }}</span></p>
              </div>
            </el-col>
          </div>
          <div class="faultWarn" v-if="forEqParameters.SituationTime != ''">
            <span>{{ forEqParameters.Situation }}</span>
            <p class="text-color-danger">{{ forEqParameters.SituationTime }}</p>
          </div>
          <div class="faultWarn" v-if="forEqParameters.SituationTime === ''">
            <p class="text-color-success" style="line-height: 50px;">{{ forEqParameters.Situation }}</p>
          </div>
        </el-col>
        <el-col :span="24" style="margin-bottom: 2px;">
          <div class="chartHead text-size-large text-color-info">
            <div class="chartTile">能耗分析</div>
            <ul class="subsectionList" v-if="EnergyClass === '水'">
              <li v-for="(item,index) in subsectionWaterList"><a href="javascript:;" :class="{active:subsectionWaterActive === index}" @click="getSubsectionWater(index)">{{ item.name }}</a></li>
            </ul>
            <ul class="subsectionList" v-if="EnergyClass === '汽'">
              <li v-for="(item,index) in subsectionSteamList"><a href="javascript:;" :class="{active:subsectionSteamActive === index}" @click="getSubsectionSteam(index)">{{ item.name }}</a></li>
            </ul>
          </div>
        </el-col>
        <el-col :span="24" style="margin-bottom: 2px;">
          <div class="energyDataContainer">
            <ve-line :data="faultChartData" :extend="chartExtend" :mark-line="markLine" :settings="chartSettings"></ve-line>
          </div>
        </el-col>
        <el-col :span="24">
          <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
            <div class="chartTile">实时预警 <span class="text-color-info-shallow text-size-mini">所有记录</span></div>
          </div>
          <div class="platformContainer">
            <el-table :data="ralTimeWarningTableData" size="mini" height="246px" max-height="246px" style="width: 100%">
              <el-table-column prop="area" label="区域"></el-table-column>
              <el-table-column prop="name" label="设备"></el-table-column>
              <el-table-column prop="type" label="状态">
                <template slot-scope="scope">
                  <span class="text-size-mini text-color-warning">{{ scope.row.type }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="date" label="时间"></el-table-column>
            </el-table>
          </div>
        </el-col>
      </el-col>
      <el-col :span="24" v-if="formParameters.eqComponentValue == '设备利用率'">
        <el-col :span="24">
          <div class="chartHead text-size-large text-color-info" style="margin-bottom: 2px;">
            <div class="chartTile">设备运行图</div>
            <el-select class="collapse-head-select float-right" v-model="commodityValue" size="small">
              <el-option v-for="item in commodityOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </div>
        </el-col>
        <el-col :span="24" style="margin-bottom: 10px;">
          <div class="platformContainer">
            <el-row type="flex" justify="space-between">
              <el-col :span="4">
                <div class="equirunInfoItem">
                  <label>开机</label>
                  <p><span class="text-size-mini text-color-info-shallow">次数</span><span class="text-size-mini text-color-info-shallow float-right">时间占比</span></p>
                  <p><span>3</span><span class="float-right">72.5%</span></p>
                </div>
              </el-col>
              <el-col :span="4">
                <div class="equirunInfoItem">
                  <label>关机</label>
                  <p><span class="text-size-mini text-color-info-shallow">次数</span><span class="text-size-mini text-color-info-shallow float-right">时间占比</span></p>
                  <p><span>3</span><span class="float-right">7.5%</span></p>
                </div>
              </el-col>
              <el-col :span="4">
                <div class="equirunInfoItem">
                  <label>空载</label>
                  <p><span class="text-size-mini text-color-info-shallow">次数</span><span class="text-size-mini text-color-info-shallow float-right">时间占比</span></p>
                  <p><span>1</span><span class="float-right">7.5%</span></p>
                </div>
              </el-col>
              <el-col :span="4">
                <div class="equirunInfoItem">
                  <label>重载</label>
                  <p><span class="text-size-mini text-color-info-shallow">次数</span><span class="text-size-mini text-color-info-shallow float-right">时间占比</span></p>
                  <p><span>1</span><span class="float-right">2.5%</span></p>
                </div>
              </el-col>
              <el-col :span="4">
                <div class="equirunInfoItem">
                  <label>功率</label>
                  <p><span class="text-size-mini text-color-info-shallow">额定功率</span><span class="text-size-mini text-color-info-shallow float-right">平均功率</span></p>
                  <p><span>45.54</span><span class="float-right">54.4856</span></p>
                </div>
              </el-col>
            </el-row>
            <div class="energyDataContainer">
              <ve-line :data="equiRunChartData" :extend="chartExtend"></ve-line>
            </div>
          </div>
        </el-col>
        <el-col :span="24">
          <div class="chartHead text-size-large text-color-info" style="margin-bottom: 2px;">
            <div class="chartTile">设备利用率分析</div>
          </div>
        </el-col>
      </el-col>
      <el-col :span="24" v-if="formParameters.eqComponentValue == '电能质量'">
        <el-col :span="8">
          <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
            <div class="chartTile">设备</div>
          </div>
          <div class="platformContainer" style="margin-bottom: 10px;">
            <el-table :data="ElectricTagDetailTableData" highlight-current-row ref="ElectricMultipleTable" @selection-change="ElectricHandleSelectionChange" @row-click="ElectricHandleRowClick" v-loading="TagEqTableLoading" size="mini" height="246px" max-height="246px">
              <el-table-column prop="AreaName" label="区域名称"></el-table-column>
              <el-table-column prop="FEFportIP" label="站点地址"></el-table-column>
              <el-table-column prop="EnergyClass" label="分类"></el-table-column>
              <el-table-column prop="IP" label="IP"></el-table-column>
              <el-table-column prop="COMNum" label="端口"></el-table-column>
            </el-table>
          </div>
        </el-col>
        <el-col :span="16" style="margin-bottom: 10px;">
          <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
            <div class="chartTile">
              设备信息
            </div>
          </div>
          <div class="platformContainer">
            <el-col :span="12">
              <div class="faultItemHead">
                <span>最近30天异常次数</span>
              </div>
              <div class="faultItemBody">
                <p style="padding: 44px 0;"><span>{{ thredaycount  }}</span></p>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="faultItemHead">
                <span>最近一次异常数据</span>
                <p>{{ WarningRow }}</p>
              </div>
              <div class="faultItemBody">
                <p style="padding: 22px 0;">故障类型<span>{{ WarningType }}</span></p>
                <p style="padding: 22px 0;">异常时间<span>{{ WarningDate }}</span></p>
              </div>
            </el-col>
          </div>
         </el-col>
        <el-col :span="24" style="margin-bottom: 2px;">
          <div class="chartHead text-size-large text-color-info">
            <div class="chartTile">电能项位</div>
            <ul class="subsectionList">
              <li v-for="(item,index) in ElectricItemList"><a href="javascript:;" :class="{active:ElectricItemActive === index}" @click="getSubsectionElectricItem(index)">{{ item.name }}</a></li>
            </ul>
          </div>
        </el-col>
        <el-col :span="24">
          <div class="energyDataContainer">
            <ve-line :data="threeCurrentImbalanceChartData" :extend="threeCurrentChartExtend" :data-zoom="dataZoom"></ve-line>
          </div>
        </el-col>
      </el-col>
    </el-row>
</template>

<script>
  var moment = require('moment');
  export default {
    name: "AreaEqDetails",
    inject:['newAreaName'],
    data(){
      return {
        formParameters:{
          startDate:moment().day(moment().day()).startOf('day').format('YYYY-MM-DD HH:mm:ss'),
          endDate:moment().format("YYYY-MM-DD HH:mm"),
          eqComponentValue:"安全/故障"
        },
        eqComponentList:[
          {name:"安全/故障",id:1},
          //{name:"设备利用率",id:2},
          {name:"电能质量",id:3},
        ],
        pickerOptions:{
          disabledDate(time) {
            return time.getTime() > Date.now();
          }
        },
        TagEqTableLoading:false,
        multipleSelection:[],
        ElectricMultipleSelection:[],
        TagDetailTableData:[],
        ElectricTagDetailTableData:[],
        forEqParameters:{},
        EnergyClass:"电",
        TagClassValue:"",
        ralTimeWarningTableData:[],
        subsectionWaterList:[
          {name:"累计量"},
          {name:"瞬时量"}
        ],
        subsectionWaterActive:0,
        subsectionSteamList:[
          {name:"累计量"},
          {name:"瞬时量"},
          {name:"体积"},
          {name:"温度"}
        ],
        subsectionSteamActive:0,
        markLine: {
          data: [
            {
              name: '最小值',
              type: 'min'
            },{
              name: '最大值',
              type: 'max'
            },{
              name: '平均值',
              type: 'average'
            }
          ],
          label:{
            position:"insideEndTop",
            formatter:'{b}：{c}'
          },
          lineStyle:{
            color:"#FB8A06"
          }
        },
        chartExtend: {
          grid:{
            left:'0',
            right:'0',
            bottom:'0',
            top:'40px'
          },
          series:{
            smooth: false
          }
        },
        chartSettings: {
          area:true
        },
        faultChartData: {
          columns: ["时间","功率"],
          rows: []
        },
        equiRunChartData:{
          columns: ['时间', '开机', '关机', '空载','重载'],
          rows: [
            { '时间': '00:00', '开机': 647, '关机': 193, '空载': 454 ,'重载':124},
            { '时间': '01:00', '开机': 457, '关机': 320, '空载': 546 ,'重载':544},
            { '时间': '02:00', '开机': 875, '关机': 223, '空载': 454 ,'重载':254},
            { '时间': '03:00', '开机': 955, '关机': 143, '空载': 247 ,'重载':274},
            { '时间': '04:00', '开机': 745, '关机': 342, '空载': 844 ,'重载':457},
            { '时间': '05:00', '开机': 688, '关机': 423, '空载': 648 ,'重载':948}
          ]
        },
        thredaycount:"",
        WarningDate:"",
        WarningType:"",
        WarningRow:"",
        ElectricItemList:[
          {name:"电流"},
          {name:"电压"},
        ],
        ElectricItemActive:0,
        threeCurrentChartExtend:{
          grid:{
            left:'0',
            right:'0',
            bottom:'0',
            top:'40px'
          },
          series:{
            smooth: false
          }
        },
        dataZoom: [
          {
            type: 'slider',
            start: 0,
            end: 20
          }
        ],
        threeCurrentImbalanceChartData:{
          columns: ['时间', 'A项电流', 'B项电流','C项电流'],
          rows: []
        }
      }
    },
    created(){
      this.getEq()
    },
    methods:{
      getSubsectionWater(index){
        this.subsectionWaterActive = index;
        this.getEqData()
      },
      getSubsectionSteam(index){
        this.subsectionSteamActive = index;
        this.getEqData()
      },
      handleSelectionChange(val){
        this.multipleSelection = val;
      },
      ElectricHandleSelectionChange(val){
        this.ElectricMultipleSelection = val;
      },
      getEq(){
        this.TagEqTableLoading = true
        let that = this
        var areaName = ''
        if(this.newAreaName.areaName === "整厂区"){
          areaName = ""
        }else{
          areaName = this.newAreaName.areaName
        }
        var params = {
          tableName:"TagDetail",
          field:"AreaName",
          fieldvalue:areaName,
          limit:100000,
          offset:0
        }
        this.axios.get("/api/CUID",{params:params}).then(res =>{
          that.TagEqTableLoading = false
          var resData = JSON.parse(res.data).rows
          that.TagDetailTableData = resData
          that.TagDetailTableData.forEach(item =>{   //循环电的tag点 插入电能质量table
            if(item.EnergyClass === "电"){
              that.ElectricTagDetailTableData.push(item)
            }
          })
          that.$refs.multipleTable.setCurrentRow(that.TagDetailTableData[0])  //默认获取第一条tag设备 设为选中
          that.handleRowClick(that.TagDetailTableData[0])
          that.EnergyClass = that.TagDetailTableData[0].EnergyClass
          that.TagClassValue = that.TagDetailTableData[0].TagClassValue
        },res =>{
          console.log("获取设备时请求错误")
        })
      },
      getEqData(){
        var that = this
        if(this.EnergyClass === "蒸汽总"){
          this.EnergyClass = "汽"
        }
        var params = {
          TagClassValue:this.TagClassValue,
          EnergyClass:this.EnergyClass,
          StartTime:moment(this.formParameters.startDate).format("YYYY-MM-DD HH:mm:ss"),
          EndTime:moment(this.formParameters.endDate).format("YYYY-MM-DD HH:mm:ss")
        }
        this.axios.get("/api/EquipmentDetail",{params:params}).then(res =>{
          that.forEqParameters = res.data
          if(this.EnergyClass === "电"){
            that.chartSettings.area = false
            that.faultChartData.columns = ["时间","功率"]
          }else if(this.EnergyClass === "水"){
            if(this.subsectionWaterActive === 0){
              that.chartSettings.area = false
              that.faultChartData.columns = ["时间","累计量"]
            }else if(this.subsectionWaterActive === 1){
              that.chartSettings.area = true
              that.faultChartData.columns = ["时间","瞬时量"]
            }
          }else if(this.EnergyClass === "汽"){
            if(this.subsectionSteamActive === 0){
              that.chartSettings.area = false
              that.faultChartData.columns = ["时间","累计量"]
            }else if(this.subsectionSteamActive === 1){
              that.chartSettings.area = true
              that.faultChartData.columns = ["时间","瞬时量"]
            }else if(this.subsectionSteamActive === 2){
              that.chartSettings.area = true
              that.faultChartData.columns = ["时间","体积"]
            }else if(this.subsectionSteamActive === 3){
              that.chartSettings.area = false
              that.faultChartData.columns = ["时间","温度"]
            }
          }
          that.faultChartData.rows = res.data.row
        })
      },
      getSubsectionElectricItem(index){
        this.ElectricItemActive = index;
        this.getEqElectricData()
      },
      getEqElectricData(){
        var that = this
        var params = {
          TagClassValue:this.ElectricMultipleSelection[0].TagClassValue,
          StartTime:moment(this.formParameters.startDate).format("YYYY-MM-DD HH:mm:ss"),
          EndTime:moment(this.formParameters.endDate).format("YYYY-MM-DD HH:mm:ss")
        }
        this.axios.get("/api/powerquality",{params:params}).then(res =>{
          that.thredaycount  = res.data.thredaycount
          that.WarningType  = res.data.WarningType
          that.WarningDate  = res.data.WarningDate
          that.WarningRow  = res.data.row
          if(this.ElectricItemActive === 0){
            that.threeCurrentImbalanceChartData.columns = ['时间', 'A项电流', 'B项电流','C项电流']
            that.threeCurrentImbalanceChartData.rows = res.data.dir_list
          }else if(this.ElectricItemActive === 1){
            that.threeCurrentImbalanceChartData.columns = ['时间', 'A项电压', 'B项电压','C项电压']
            that.threeCurrentImbalanceChartData.rows = res.data.dir_list
          }
        })
      },
      handleRowClick(row){
        this.$refs.multipleTable.clearSelection();
        this.$refs.multipleTable.toggleRowSelection(row)
        this.EnergyClass = this.multipleSelection[0].EnergyClass
        this.TagClassValue = this.multipleSelection[0].TagClassValue
        this.getEqData()
      },
      ElectricHandleRowClick(row){
        this.$refs.ElectricMultipleTable.clearSelection();
        this.$refs.ElectricMultipleTable.toggleRowSelection(row)
        this.getEqElectricData()
      },
    }
  }
</script>

<style scoped>
  .faultItemHead{
    height: 70px;
    background: #EEEEEE;
    border-radius:4px;
    padding: 10px;
    margin-bottom: 10px;
  }
  .faultItemHead p{
    color: #9B9B9B;
    margin-top: 10px;
    font-size: 14px;
  }
  .faultItemHead p span{
    float: right;
    color: #131414;
  }
  .faultItemBody{
    padding: 10px;
    color: #9B9B9B;
    font-size: 14px;
  }
  .faultItemBody p{
    margin-bottom: 10px;
  }
  .faultItemBody p span{
    float: right;
    color: #15CC48;
  }
  .faultWarn{
    border-radius:4px;
    text-align: center;
    height: 50px;
    background: #ffffff;
  }
  .faultWarn span{
    color: #9B9B9B;
    font-size: 12px;
  }
  .overview{
    background: #fff;
    border-radius:4px;
    color: #000;
    font-size: 14px;
    padding: 15px;
    text-align: center;
    clear: both;
    overflow: hidden;
  }
  .overview p{
    margin-bottom: 10px;
  }
  .equirunInfoItem{
    background: #EEEEEE;
    border-radius:4px;
    padding: 10px;
    margin-bottom: 10px;
  }
  .equirunInfoItem p{
    margin-top: 10px;
  }
</style>
