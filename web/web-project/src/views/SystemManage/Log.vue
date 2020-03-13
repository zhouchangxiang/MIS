<template>
  <el-row style="background: #fff;">
    <el-col :span="24" style="padding: 15px;">
      <el-row>
        <el-col :span="24">
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
        </el-col>
      </el-row>
      <el-table :data="tableData" border tooltip-effect="dark">
        <el-table-column prop="IP" label="IP"></el-table-column>
        <el-table-column prop="ComputerName" label="计算机名称"></el-table-column>
        <el-table-column prop="UserName" label="操作用户"></el-table-column>
        <el-table-column prop="OperationDate" label="操作日期"></el-table-column>
        <el-table-column prop="OperationContent" label="操作内容"></el-table-column>
        <el-table-column prop="OperationType" label="类型"></el-table-column>
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
    </el-col>
  </el-row>
</template>

<script>
  export default {
    name: "Log",
    data(){
      return{
        tableData:[],
        total:0,
        pagesize:5,
        currentPage:1,
        region:"",
        regionList:[
          {label:"操作用户",value:"UserName"},
          {label:"操作日期",value:"OperationDate"}
        ],
        searchVal:""
      }
    },
    mounted() {
      this.getTableData()
    },
    methods:{
      getTableData(){
        this.axios.get("/api/CUID",{
          params: {
            tableName: "SysLog",
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
      searchTab(){
        this.axios.get("/api/CUID",{
          params: {
            tableName: "SysLog",
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
      handleSizeChange(pagesize){ //每页条数切换
        this.pagesize = pagesize
        this.getTableData()
      },
      handleCurrentChange(currentPage) { // 页码切换
        this.currentPage = currentPage
        this.getTableData()
      }
    }
  }
</script>

<style scoped>

</style>
