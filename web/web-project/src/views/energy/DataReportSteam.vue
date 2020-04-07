<template>
  <el-row :gutter="20">
    <el-col :span="24">
      <el-form :model="formParameters">
        <el-form-item label="时间：">
          <el-date-picker type="datetime" v-model="formParameters.startDate" :picker-options="pickerOptions" size="mini" format="yyyy-MM-dd HH:mm:ss" style="width: 180px;" :clearable="false" @change="searchTime"></el-date-picker> ~
          <el-date-picker type="datetime" v-model="formParameters.endDate" :picker-options="pickerOptions" size="mini" format="yyyy-MM-dd HH:mm:ss" style="width: 180px;" :clearable="false" @change="searchTime"></el-date-picker>
          <el-button type="primary" size="mini" style="float: right;" @click="exportExcel">导出水电气数据</el-button>
        </el-form-item>
      </el-form>
    </el-col>
    <el-col :span="24">
      <div class="chartHead text-size-large text-color-info" style="margin-bottom:2px;">
        <div class="chartTile">蒸汽报表</div>
        <el-select v-model="areaValue" size="mini" @change="searchTime">
          <el-option v-for="(item,index) in areaOptions" :key="item.index" :label="item.AreaName" :value="item.value"></el-option>
        </el-select>
        <el-button type="primary" size="mini" style="float: right;margin: 9px 0;">导出</el-button>
      </div>
      <div class="platformContainer">
        <el-table :data="tableData" border tooltip-effect="dark">
          <el-table-column prop="IncremenValue" label="增量值"></el-table-column>
          <el-table-column prop="Unit" label="单位"></el-table-column>
          <el-table-column prop="CollectionDate" label="采集时间"></el-table-column>
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
    name: "DataReportSteam",
    data(){
      return {
        formParameters:{
          startDate:moment().day(moment().day() - 1).format('YYYY-MM-DD') + " 7:00",
          endDate:moment().day(moment().day() - 1).format('YYYY-MM-DD') + " 19:00"
        },
        pickerOptions:{
          disabledDate(time) {
            return time.getTime() > Date.now();
          }
        },
        areaValue:"",
        areaOptions:[],
        tableData:[],
        total:0,
        pagesize:5,
        currentPage:1
      }
    },
    created(){
      this.getArea()
      this.searchTime()
    },
    methods:{
      exportExcel(){
        var startTime = this.formParameters.startDate
        var endTime = this.formParameters.endDate
        this.$confirm('确定导出' +startTime+'至'+endTime+'水电气全部记录？', '提示', {
          type: 'warning'
        }).then(()  => {
          window.location.href = "http://127.0.0.1:5000/exceloutstatistic?StartTime="+startTime+"&EndTime="+endTime
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
          for(var i=0;i < resData.length;i++){
            that.areaOptions.push({
              AreaName:resData[i].AreaName,
              value:resData[i].AreaName
            })
          }
        },res =>{
          console.log("获取车间时请求错误")
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
        this.axios.get("/api/get_steam_energy",{
          params: {
            StartTime:this.formParameters.startDate,
            EndTime:this.formParameters.endDate,
            AreaName:this.areaValue,
            limit:this.pagesize,
            offset:this.currentPage
          }
        }).then(res =>{
          var data = res.data
          console.log(data)
          this.tableData = data.rows
          this.total = data.total_column
        },res =>{
          console.log("请求错误")
        })
      }
    }
  }
</script>

<style scoped>

</style>
