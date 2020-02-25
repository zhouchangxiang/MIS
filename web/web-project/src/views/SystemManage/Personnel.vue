<template>
    <el-row>
    <el-col :span="24">
      <div style="background: #fff;">
        <el-table :data="tableData">
          <el-table-column prop="name" label="名字"></el-table-column>
          <el-table-column prop="accountNum" label="账号/工号"></el-table-column>
          <el-table-column prop="post" label="所属岗位"></el-table-column>
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
      name: "Personnel",
      data(){
        return {
          tableData:[
            {name:"周昌象",accountNum:"122343",post:"系统管理员"},
            {name:"闵子文",accountNum:"322344",post:"生产部负责人"},
            {name:"吴旭",accountNum:"252324",post:"生产部维修工"}
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
