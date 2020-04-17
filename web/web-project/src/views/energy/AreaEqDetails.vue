<template>
    <el-row :gutter="10">
      <el-col :span="24">
        <el-form :model="formParameters">
          <el-form-item label="参数：" style="margin-bottom: 0;">
            <el-radio-group v-model="formParameters.eqComponentValue" fill="#082F4C" size="small">
              <el-radio-button v-for="item in eqComponentList" :key="item.id" :label="item.name"></el-radio-button>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="时间：">
            <el-date-picker type="datetime" v-model="formParameters.startDate" :picker-options="pickerOptions" size="mini" style="width: 180px;" :clearable="false"></el-date-picker> ~
            <el-date-picker type="datetime" v-model="formParameters.endDate" :picker-options="pickerOptions" size="mini" style="width: 180px;" :clearable="false"></el-date-picker>
          </el-form-item>
        </el-form>
      </el-col>
      <el-col :span="24" v-if="formParameters.eqComponentValue === '安全/故障'">
        <el-col :span="8">
          <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
            <div class="chartTile">设备</div>
          </div>
          <div class="platformContainer">
            <el-table :data="TagDetailTableData" highlight-current-row ref="multipleTable" @selection-change="handleSelectionChange" @row-click="handleRowClick" size="mini" height="246px" max-height="246px" style="width: 100%">
              <el-table-column type="selection"></el-table-column>
              <el-table-column prop="AreaName" label="区域名称"></el-table-column>
              <el-table-column prop="FEFportIP" label="站点地址"></el-table-column>
              <el-table-column prop="DeviceNum" label="器件号"></el-table-column>
              <el-table-column prop="EnergyClass" label="分类"></el-table-column>
              <el-table-column prop="TagClassValue" label="Tag点"></el-table-column>
            </el-table>
          </div>
        </el-col>
        <el-col :span="16">
          <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
            <div class="chartTile">
              设备信息
            </div>
            <div class="chartHeadRight">
              <el-button size="mini">档案</el-button>
              <el-button size="mini">历史事件</el-button>
            </div>
          </div>
          <div class="platformContainer" style="margin-bottom:10px;">
            <el-col :span="8">
              <div class="faultItemHead">
                <span>功率</span>
                <p>额定功率/kw <span>53</span></p>
              </div>
              <div class="faultItemBody">
                <p style="padding: 29px 0;">有功功率/kw <span>2.1514</span></p>
              </div>
              <div class="faultWarn">
                <p class="text-color-success" style="line-height: 60px;">未发现异常</p>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="faultItemHead">
                <span>电流</span>
                <p>额定电流/A <span>{{  }}</span></p>
              </div>
              <div class="faultItemBody">
                <p>A项电流 <span>{{  }}</span></p>
                <p>B项电流 <span>0</span></p>
                <p>C项电流 <span>2.1514</span></p>
              </div>
              <div class="faultWarn">
                <span>2020-02-04 17:56</span>
                <p class="text-color-danger">B项断项</p>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="faultItemHead">
                <span>电压</span>
                <p>额定电压/V <span>5</span></p>
              </div>
              <div class="faultItemBody">
                <p>A项电压 <span>2.1514</span></p>
                <p>B项电压 <span>0</span></p>
                <p>C项电压 <span>2.1514</span></p>
              </div>
              <div class="faultWarn">
                <p class="text-color-success" style="line-height: 60px;">未发现异常</p>
              </div>
            </el-col>
          </div>
        </el-col>
        <el-col :span="24" style="margin-bottom: 2px;">
          <div class="chartHead text-size-large text-color-info">
            <div class="chartTile">参数分析</div>
            <ul class="subsectionList">
              <li v-for="item in subsectionList"><a href="javascript:;" :class="{active:subsectionActive == item.id}" @click="getSubsection(item.id)">{{ item.name }}</a></li>
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
        <el-col :span="24" style="margin-bottom: 10px;">
          <div class="platformContainer">
            <el-col :span="8">
              <div class="equirunInfoItem">
                <label>三项电流不平衡度</label>
                <p><span class="text-size-mini text-color-info-shallow">正常值</span><span class="text-size-mini text-color-info-shallow float-right">最近30天一场次数</span></p>
                <p><span><15%</span><span class="float-right">6次</span></p>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="equirunInfoItem">
                <label>最近一次异常数据</label>
                <p><span class="text-size-mini text-color-info-shallow">三相不平衡度</span><span class="text-size-mini text-color-info-shallow float-right">异常时间</span></p>
                <p><span>23.8%</span><span class="float-right">17:00-19:00</span></p>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="equirunInfoItem">
                <label>提示</label>
                <p style="margin-bottom: 10px;"><span class="text-size-mini text-color-info-shallow">三相电流不平衡度连续出现异常，可能是三相线路负载不平衡导致， 需及时调整变压器负载</span></p>
              </div>
            </el-col>
            <div class="energyDataContainer">
              <ve-line :data="threeCurrentImbalanceChartData" :extend="ChartExtend"></ve-line>
            </div>
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
          resourceTime:"班次",
          startDate:moment().day(moment().day()).startOf('day').format('YYYY-MM-DD HH:mm'),
          endDate:moment().format("YYYY-MM-DD HH:mm"),
          eqComponentValue:"安全/故障"
        },
        radioTimeList:[
          {name:"班次",id:1},
          {name:"日",id:2},
          {name:"周",id:3},
          {name:"月",id:4}
        ],
        eqComponentList:[
          {name:"安全/故障",id:1},
          {name:"设备利用率",id:2},
          {name:"电能质量",id:3},
        ],
        pickerOptions:{
          disabledDate(time) {
            return time.getTime() > Date.now();
          }
        },
        multipleSelection:[],
        TagDetailTableData:[],
        ralTimeWarningTableData:[ //实时预警表格数据
          {area:"新建综合制剂楼",name:"汽表2",type:"温度不正常",date:"2020-01-02 12:05"},
          {area:"新建综合制剂楼",name:"汽表4",type:"温度不正常",date:"2020-01-02 12:05"},
          {area:"新建综合制剂楼",name:"电表1",type:"三项电流不平衡",date:"2020-01-02 12:05"},
          {area:"新建综合制剂楼",name:"汽表2",type:"温度不正常",date:"2020-01-02 12:05"}
        ],
        subsectionList:[
          {name:"视在功率",id:1},
          {name:"有功功率",id:2},
          {name:"无功功率",id:3},
          {name:"电流",id:4},
          {name:"电压",id:5},
          {name:"频率",id:6}
        ],
        subsectionActive:1,
        faultChartData: {
          columns: ['时间', '总有功电量', 'A相有功电量', 'B相有功电量','C相有功电量'],
          rows: [
            { '时间': '00:00', '总有功电量': 4647, 'A相有功电量': 193, 'B相有功电量': 454 ,'C相有功电量':124},
            { '时间': '01:00', '总有功电量': 8457, 'A相有功电量': 320, 'B相有功电量': 546 ,'C相有功电量':544},
            { '时间': '02:00', '总有功电量': 4875, 'A相有功电量': 223, 'B相有功电量': 454 ,'C相有功电量':254},
            { '时间': '03:00', '总有功电量': 9755, 'A相有功电量': 143, 'B相有功电量': 247 ,'C相有功电量':274},
            { '时间': '04:00', '总有功电量': 7545, 'A相有功电量': 342, 'B相有功电量': 844 ,'C相有功电量':457},
            { '时间': '05:00', '总有功电量': 6488, 'A相有功电量': 423, 'B相有功电量': 648 ,'C相有功电量':948}
          ]
        },
        overview:{
          maxValue:"222.3V",
          maxTime:"13:00",
          maxSite:"A项电压",
          minValue:"212.6V",
          minTime:"9:00",
          minSite:"B项电压",
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
      //this.getEqData()
    },
    methods:{
      getSubsection(index){
        this.subsectionActive = index;
      },
      handleSelectionChange(val){
        this.multipleSelection = val;
      },
      getEq(){
        let that = this
        var params = {
          tableName:"TagDetail",
          field:"AreaName",
          fieldvalue:this.newAreaName.areaName,
          limit:100000,
          offset:0
        }
        this.axios.get("/api/CUID",{params:params}).then(res =>{
          var resData = JSON.parse(res.data).rows
          that.TagDetailTableData = resData
          that.$refs.multipleTable.setCurrentRow(that.TagDetailTableData[0])
          that.handleRowClick(that.TagDetailTableData[0])
        },res =>{
          console.log("获取设备时请求错误")
        })
      },
      getEqData(){
        var params = {
          TagClassValue:this.multipleSelection[0].TagClassValue,
          EnergyClass:this.multipleSelection[0].EnergyClass,
          StartTime:moment(this.formParameters.startDate).format("YYYY-MM-DD HH:mm"),
          EndTime:moment(this.formParameters.endDate).format("YYYY-MM-DD HH:mm")
        }
        this.axios.get("/api/EquipmentDetail",{params:params}).then(res =>{
          console.log(res.data)
        })
      },
      handleRowClick(row){
        this.$refs.multipleTable.clearSelection();
        this.$refs.multipleTable.toggleRowSelection(row)
        this.getEqData()
      }
    }
  }
</script>

<style scoped>
  .faultItemHead{
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
    border:1px solid #B9B9B9;
    text-align: center;
    height: 60px;
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
