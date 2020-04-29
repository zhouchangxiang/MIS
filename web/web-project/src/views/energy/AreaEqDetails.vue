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
            <el-table :data="TagDetailTableData" highlight-current-row ref="multipleTable" @selection-change="handleSelectionChange" @row-click="handleRowClick" v-loading="TagEqTableLoading" size="mini" height="246px" max-height="246px" style="width: 100%">
              <el-table-column prop="AreaName" label="区域名称"></el-table-column>
              <el-table-column prop="FEFportIP" label="站点地址"></el-table-column>
              <el-table-column prop="EnergyClass" label="分类"></el-table-column>
              <el-table-column prop="IP" label="IP"></el-table-column>
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
          <div class="platformContainer" style="margin-bottom:10px;" v-if="EnergyClass === '汽'">
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
          <div class="faultWarn">
            <span>2020-02-04 17:56</span>
            <p class="text-color-danger">B项断项</p>
          </div>
        </el-col>
        <el-col :span="24" style="margin-bottom: 2px;">
          <div class="chartHead text-size-large text-color-info">
            <div class="chartTile">参数分析</div>
            <ul class="subsectionList" v-if="EnergyClass === '汽'">
              <li v-for="(item,index) in subsectionList"><a href="javascript:;" :class="{active:subsectionActive === index}" @click="getSubsection(index)">{{ item.name }}</a></li>
            </ul>
          </div>
        </el-col>
        <el-col :span="24">
          <div class="energyDataContainer">
            <ve-line :data="faultChartData" :extend="ChartExtend"></ve-line>
          </div>
          <div class="chartHead text-size-large text-color-info" style="margin-bottom: 2px;">
            <div class="chartTile">数据概览</div>
          </div>
        </el-col>
        <el-col :span="24" style="margin-bottom: 10px;">
          <div class="overview">
            <el-col :span="4"><p class="text-color-caption">最大值</p>{{ overview.maxValue }}</el-col>
            <el-col :span="4"><p class="text-color-caption">发生时间</p>{{ overview.maxTime }}</el-col>
            <el-col :span="4"><p class="text-color-caption">项位</p>{{ overview.maxSite }}</el-col>
            <el-col :span="4"><p class="text-color-caption">最小值</p>{{ overview.maxValue }}</el-col>
            <el-col :span="4"><p class="text-color-caption">发生时间</p>{{ overview.maxTime }}</el-col>
            <el-col :span="4"><p class="text-color-caption">项位</p>{{ overview.maxSite }}</el-col>
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
              <ve-line :data="equiRunChartData" :extend="ChartExtend"></ve-line>
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
                <span>三项电流不平衡度</span>
              </div>
              <div class="faultItemBody">
                <p style="padding: 22px 0;">正常值<span>{{  }}</span></p>
                <p style="padding: 22px 0;">最近30天异常次数<span>{{  }}</span></p>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="faultItemHead">
                <span>最近一次异常数据</span>
              </div>
              <div class="faultItemBody">
                <p style="padding: 22px 0;">三相不平衡度<span>{{  }}</span></p>
                <p style="padding: 22px 0;">异常时间<span>{{  }}</span></p>
              </div>
            </el-col>
          </div>
         </el-col>
        <el-col :span="24">
          <div class="energyDataContainer">
            <ve-line :data="threeCurrentImbalanceChartData" :extend="ChartExtend"></ve-line>
          </div>
        </el-col>
        <el-col :span="24">
          <div class="chartHead text-size-large text-color-info" style="margin-bottom: 2px;">
            <div class="chartTile">实时数据</div>
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
      this.ChartExtend = {
        grid:{
          left:'0',
          right:'0',
          bottom:'0',
          top:'40px'
        },
        series:{
          smooth: false
        }
      }
      return {
        formParameters:{
          startDate:moment().day(moment().day()).startOf('day').format('YYYY-MM-DD HH:mm'),
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
        ralTimeWarningTableData:[],
        subsectionList:[
          {name:"能耗"},
          {name:"体积"},
          {name:"温度"}
        ],
        subsectionActive:1,
        faultChartData: {
          columns: ['时间', '功率'],
          rows: []
        },
        overview:{
          maxValue:"",
          maxTime:"",
          minValue:"",
          minTime:""
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
        threeCurrentImbalanceChartData:{
          columns: ['时间', 'A项', 'B项','C项'],
          rows: [
            { '时间': '00:00', 'A项': 647, 'B项': 193, 'C项': 454 },
            { '时间': '01:00', 'A项': 457, 'B项': 320, 'C项': 546 },
            { '时间': '02:00', 'A项': 875, 'B项': 223, 'C项': 454 },
            { '时间': '03:00', 'A项': 955, 'B项': 143, 'C项': 247 },
            { '时间': '04:00', 'A项': 745, 'B项': 342, 'C项': 844 },
            { '时间': '05:00', 'A项': 688, 'B项': 423, 'C项': 648 }
          ]
        }
      }
    },
    created(){
      this.getEq()
    },
    methods:{
      getSubsection(index){
        this.subsectionActive = index;
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
          that.TagDetailTableData.forEach(item =>{
            if(item.EnergyClass === "电"){
              that.ElectricTagDetailTableData.push(item)
            }
          })
          that.$refs.multipleTable.setCurrentRow(that.TagDetailTableData[0])
          that.handleRowClick(that.TagDetailTableData[0])
        },res =>{
          console.log("获取设备时请求错误")
        })
      },
      getEqData(){
        var that = this
        this.EnergyClass = this.multipleSelection[0].EnergyClass
        var params = {
          TagClassValue:this.multipleSelection[0].TagClassValue,
          EnergyClass:this.multipleSelection[0].EnergyClass,
          StartTime:moment(this.formParameters.startDate).format("YYYY-MM-DD HH:mm"),
          EndTime:moment(this.formParameters.endDate).format("YYYY-MM-DD HH:mm")
        }
        this.axios.get("/api/EquipmentDetail",{params:params}).then(res =>{
          that.forEqParameters = res.data
          if(this.EnergyClass === "电"){
            that.faultChartData.columns = ["时间","功率"]
          }else if(this.EnergyClass === "水"){
            that.faultChartData.columns = ["时间","瞬时量","累计量"]
          }else if(this.EnergyClass === "汽"){
            if(this.subsectionActive === 0){
              that.faultChartData.columns = ["时间","瞬时量","累计量"]
            }else if(this.subsectionActive === 1){
              that.faultChartData.columns = ["时间","体积"]
            }else if(this.subsectionActive === 2){
              that.faultChartData.columns = ["时间","温度"]
            }
          }
          that.faultChartData.rows = res.data.row
        })
      },
      getEqElectricData(){
        var that = this
        var params = {
          TagClassValue:this.ElectricMultipleSelection[0].TagClassValue,
          StartTime:moment(this.formParameters.startDate).format("YYYY-MM-DD HH:mm"),
          EndTime:moment(this.formParameters.endDate).format("YYYY-MM-DD HH:mm")
        }
        // this.axios.get("/api/EquipmentDetail",{params:params}).then(res =>{
        //   that.forEqParameters = res.data
        //   that.faultChartData.rows = res.data.row
        // })
      },
      handleRowClick(row){
        this.$refs.multipleTable.clearSelection();
        this.$refs.multipleTable.toggleRowSelection(row)
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
