<template>
  <el-row>
    <el-col :span="24">
      <div style="background: #fff;">
        <el-table :data="tableData">
          <el-table-column prop="name" label="厂区名称"></el-table-column>
          <el-table-column prop="address" label="厂区位置"></el-table-column>
          <el-table-column prop="enterprise" label="所属企业"></el-table-column>
        </el-table>
        <el-pagination background layout="prev, pager, next"
                       :total="total"
                       :current-page="currentPage"
                       :page-sizes="[10,20,30]"
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
      name: "Factory",
      data(){
        return {
          tableData:[
            {name:"好护士桓仁厂区1",address:"辽宁桓仁",enterprise:"好护士药业"},
            {name:"好护士桓仁厂区2",address:"辽宁桓仁",enterprise:"好护士药业"},
            {name:"好护士桓仁厂区3",address:"辽宁桓仁",enterprise:"好护士药业"}
          ],
          total:3,
          pagesize:2,
          currentPage:1
        }
      },
      mounted() {
        this.getData()
      },
      methods:{
        getData(){
          this.axios.get("http://127.0.0.1:5000/CUID").then(res =>{
            console.log(res.data)
          },res =>{
            console.log("请求错误")
          })
        },
        handleSizeChange(pagesize){ //每页条数切换
          this.pagesize = pagesize
          this.handleCurrentChange(this.currentPage)
        },
        handleCurrentChange(currentPage) { // 页码切换
          this.currentPage = currentPage
        }
      }
    }
</script>

<style scoped>

</style>
