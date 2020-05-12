<template>
  <el-row :gutter="20">
    <el-col :span="24">
      <el-form :model="formParameters">
        <el-form-item label="时间：">
          <el-date-picker type="datetime" v-model="formParameters.startDate" :picker-options="pickerOptions" size="mini" format="yyyy-MM-dd HH:mm:ss"  style="width: 180px;" :clearable="false"></el-date-picker> ~
          <el-date-picker type="datetime" v-model="formParameters.endDate" :picker-options="pickerOptions" size="mini" format="yyyy-MM-dd HH:mm:ss" style="width: 180px;" :clearable="false" @blur="searchTime"></el-date-picker>
          <span class="text-size-mini text-color-info-shallow">（选择结束时间后刷新数据）</span>
          <el-button type="primary" size="mini" style="float: right;" @click="exportAllExcel">导出统计数据</el-button>
        </el-form-item>
      </el-form>
    </el-col>
    <el-col :span="24">
      <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
        <div class="chartTile">电能报表</div>
        <el-select v-model="areaValue" size="mini" @change="searchTime">
          <el-option v-for="(item,index) in areaOptions" :key="index" :label="item.AreaName" :value="item.value"></el-option>
        </el-select>
        <el-button type="primary" size="mini" style="float: right;margin: 9px 0;" @click="exportExcel">导出详细数据</el-button>
      </div>
      <div class="platformContainer">
        <el-table :data="tableData" border tooltip-effect="dark" v-loading="loading">
          <el-table-column prop="AreaName" label="区域"></el-table-column>
          <el-table-column prop="ZGL" label="总功率"></el-table-column>
          <el-table-column prop="AU" label="A相电压"></el-table-column>
          <el-table-column prop="AI" label="A相电流"></el-table-column>
          <el-table-column prop="BU" label="B相电压"></el-table-column>
          <el-table-column prop="BI" label="B相电流"></el-table-column>
          <el-table-column prop="CU" label="C相电压"></el-table-column>
          <el-table-column prop="CI" label="C相电流"></el-table-column>
          <el-table-column prop="Unit" label="单位"></el-table-column>
          <el-table-column prop="CollectionDate" label="采集时间" width="170"></el-table-column>
          <el-table-column prop="TagClassValue" label="采集点"></el-table-column>
        </el-table>
        <div class="paginationClass">
          <el-pagination background  layout="total, sizes, prev, pager, next, jumper"
                         :total="total"
                         :current-page="currentPage"
                         :page-sizes="[10,20,30]"
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
          startDate:moment().day(moment().day() - 1).format('YYYY-MM-DD') + " 07:00",
          endDate:moment().day(moment().day() - 1).format('YYYY-MM-DD') + " 19:00"
        },
        pickerOptions:{
          disabledDate(time) {
            return time.getTime() > moment();
          }
        },
        areaValue:"",
        areaOptions:[],
        tableData:[],
        total:0,
        pagesize:10,
        currentPage:1,
        loading:false
      }
    },
    created(){
      this.getArea()
      this.searchTime()
    },
    methods:{
      exportAllExcel(){
        var startTime = moment(this.formParameters.startDate).format("YYYY-MM-DD HH:mm:ss")
        var endTime = moment(this.formParameters.endDate).format("YYYY-MM-DD HH:mm:ss")
        this.$confirm('确定导出' +startTime+'至'+endTime+'电能统计记录？', '提示', {
          type: 'warning'
        }).then(()  => {
          window.location.href = "/api/exceloutstatistic?StartTime="+startTime+"&EndTime="+endTime+"&EnergyClass=电"
        });
      },
      exportExcel(){
        var startTime = moment(this.formParameters.startDate).format("YYYY-MM-DD HH:mm:ss")
        var endTime = moment(this.formParameters.endDate).format("YYYY-MM-DD HH:mm:ss")
        var areaValue = this.areaValue
        this.$confirm('确定导出' +startTime+'至'+endTime+" "+areaValue+'的电能详细记录？', '提示', {
          type: 'warning'
        }).then(()  => {
          window.location.href = "/api/excelout?StartTime="+startTime+"&EndTime="+endTime+"&Area="+areaValue+"&EnergyClass=电"
        });
      },
      getArea(){
        var params = {
          tableName: "AreaTable",
          limit:1000,
          offset:0
        }
        var that = this
        this.axios.get("/api/CUID",{params:params}).then(res =>{
          var resData = JSON.parse(res.data).rows
          that.areaOptions.push({
            AreaName:"整厂区",value:""
          })
          resData.forEach(item =>{
            that.areaOptions.push({
              AreaName:item.AreaName,
              value:item.AreaName
            })
          })
        })
      },
      handleSizeChange(pagesize){ //每页条数切换
        this.pagesize = pagesize
        this.searchTime()
      },
      handleCurrentChange(currentPage) { // 页码切换
        this.currentPage = currentPage
        this.searchTime()
      },
      searchTime(){
        this.loading = true
        this.axios.get("/api/electric_report",{
          params: {
            start_time:moment(this.formParameters.startDate).format("YYYY-MM-DD HH:mm:ss"),
            end_time:moment(this.formParameters.endDate).format("YYYY-MM-DD HH:mm:ss"),
            area_name:this.areaValue,
            limit:this.pagesize,
            offset:this.currentPage
          }
        }).then(res =>{
          var data = res.data
          this.tableData = data.rows
          this.total = data.total_column
          this.loading = false
        })
      }
    }
  }
</script>

<style scoped>

</style>
