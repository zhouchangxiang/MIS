<template>
  <el-row :gutter="20">
    <el-col :span="24">
      <el-form :model="formParameters">
        <el-form-item label="时间：" style="margin-bottom: 0;">
          <el-date-picker type="datetime" v-model="formParameters.startDate" :picker-options="pickerOptions" size="mini" style="width: 180px;" :clearable="false"></el-date-picker> ~
          <el-date-picker type="datetime" v-model="formParameters.endDate" :picker-options="pickerOptions" size="mini" style="width: 180px;" :clearable="false"></el-date-picker>
          <el-button type="primary" size="mini" style="float: right;" @click="exportExcel">导出所有数据</el-button>
        </el-form-item>
        <el-form-item label="参数：">
          <el-radio-group v-model="formParameters.electricityType" fill="#082F4C" size="mini">
            <el-radio-button v-for="item in electricityTypeList" border :key="item.id" :label="item.name"></el-radio-button>
          </el-radio-group>
        </el-form-item>
      </el-form>
    </el-col>
    <el-col :span="24">
      <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
        <div class="chartTile">电能报表</div>
        <el-select v-model="areaValue" size="mini">
          <el-option v-for="item in areaOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
        <el-button type="primary" size="mini" style="float: right;margin: 9px 0;">导出</el-button>
      </div>
      <div class="platformContainer">
        <el-form :inline="true">
          <el-form-item>
            <el-select v-model="region" placeholder="请选择搜索字段" size="small">
              <el-option v-for="(item,index) in regionList" :label="item.label" :value="item.value" :key="index"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-input placeholder="请输入搜索内容" size="small" v-model="searchVal"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="success" icon="el-icon-search" size="small" @click="searchTab">搜索</el-button>
          </el-form-item>
        </el-form>
        <el-table :data="tableData" border tooltip-effect="dark">
          <el-table-column type="expand">
            <template slot-scope="props">
              <el-form label-position="left" class="table-expand">
                <el-form-item label="ID">
                  <span>{{ props.row.ID }}</span>
                </el-form-item>
                <el-form-item label="仪表ID">
                  <span>{{ props.row.EquipmnetID }}</span>
                </el-form-item>
                <el-form-item label="价格ID">
                  <span>{{ props.row.PriceID }}</span>
                </el-form-item>
                <el-form-item label="计算增量更新标识">
                  <span>{{ props.row.IncrementFlag }}</span>
                </el-form-item>
                <el-form-item label="两个相邻采集点上一个采集点ID">
                  <span>{{ props.row.PrevID }}</span>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>
          <el-table-column prop="Unit" label="单位"></el-table-column>
          <el-table-column prop="PriceValue" label="价格值"></el-table-column>
          <el-table-column prop="TagClassValue" label="采集点"></el-table-column>
          <el-table-column prop="CollectionDate" label="采集时间"></el-table-column>
          <el-table-column prop="CollectionYear" label="采集年"></el-table-column>
          <el-table-column prop="CollectionMonth" label="采集月"></el-table-column>
          <el-table-column prop="CollectionDay" label="采集天"></el-table-column>
          <el-table-column prop="ZGL" label="总功率"></el-table-column>
          <el-table-column prop="AU" label="A相电压"></el-table-column>
          <el-table-column prop="AI" label="A相电流"></el-table-column>
          <el-table-column prop="BU" label="B相电压"></el-table-column>
          <el-table-column prop="BI" label="B相电流"></el-table-column>
          <el-table-column prop="CU" label="C相电压"></el-table-column>
          <el-table-column prop="CI" label="C相电流"></el-table-column>
          <el-table-column prop="AreaName" label="区域"></el-table-column>
        </el-table>
        <div class="paginationClass">
          <el-pagination background  layout="total, sizes, prev, pager, next, jumper"
                         :total="total"
                         :current-page="currentPage"
                         :page-sizes="[5,10,20]"
                         :page-size="pagesize"
                         @size-change="handleSizeChange"
                         @current-change="handleCurrentChange">
          </el-pagination>
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  var moment = require('moment');
  export default {
    name: "DataReportElectricity",
    data(){
      return {
        formParameters:{
          startDate:Date.now(),
          endDate:Date.now(),
          electricityType:"电量"
        },
        pickerOptions:{
          disabledDate(time) {
            return time.getTime() > Date.now();
          }
        },
        electricityTypeList:[
          {name:"电量",id:1},
          {name:"电流电压频率",id:2},
          {name:"功率",id:3},
        ],
        areaValue:"桓仁厂区",
        areaOptions:[],
        tableData:[],
        total:0,
        pagesize:5,
        currentPage:1,
        region:"",
        regionList:[
          {label:"区域",value:"AreaName"}
        ],
        searchVal:""
      }
    },
    created(){
      this.getTableData()
    },
    methods:{
      exportExcel(){
        var startTime = moment(this.formParameters.startDate).format('YYYY-MM-DD HH:mm:ss')
        var endTime = moment(this.formParameters.endDate).format('YYYY-MM-DD HH:mm:ss')
        this.$confirm('确定导出' +startTime+'至'+endTime+'水电气全部记录？', '提示', {
          type: 'warning'
        }).then(()  => {
          this.axios.get("/api/exceloutstatistic",{
            params: {
              StartTime: startTime,
              EndTime: endTime
            }
          }).then(res =>{
            console.log(res)
            if(res.data == "OK"){
              this.$message({
                type: 'success',
                message: '导出成功'
              });
            }
            this.getTableData()
          },res =>{
            console.log("请求错误")
          })
        }).catch(()   => {
          this.$message({
            type: 'info',
            message: '已取消导出'
          });
        });
      },
      getTableData(){
        this.axios.get("/api/CUID",{
          params: {
            tableName: "ElectricEnergy",
            limit:this.pagesize,
            offset:this.currentPage - 1
          }
        }).then(res =>{
          var data = JSON.parse(res.data)
          this.tableData = data.rows
          this.total = data.total
        },res =>{
          console.log("请求错误")
        })
      },
      handleSizeChange(pagesize){ //每页条数切换
        this.pagesize = pagesize
        this.getTableData()
      },
      handleCurrentChange(currentPage) { // 页码切换
        this.currentPage = currentPage
        this.getTableData()
      },
      searchTab(){
        this.axios.get("/api/CUID",{
          params: {
            tableName: "ElectricEnergy",
            field:this.region,
            fieldvalue:this.searchVal,
            limit:this.pagesize,
            offset:this.currentPage - 1
          }
        }).then(res =>{
          var data = JSON.parse(res.data)
          this.tableData = data.rows
          this.total = data.total
        },res =>{
          console.log("请求错误")
        })
      },
    }
  }
</script>

<style scoped>

</style>
