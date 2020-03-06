<template>
  <el-row style="height: 100%;background: #fff;">
    <el-col :span="24" style="height: 100%;padding: 15px;">
      <el-row>
        <el-col :span="24">
          <el-form :inline="true">
            <el-form-item>
              <el-input placeholder="请输入搜索内容" size="small"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="success" icon="el-icon-search" size="small">搜索</el-button>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" size="small" @click="openDialog('add')">添加</el-button>
            </el-form-item>
            <el-form-item>
              <el-button type="warning" size="small" @click="openDialog('edit')">修改</el-button>
            </el-form-item>
            <el-form-item>
              <el-button type="danger" size="small" @click="del">删除</el-button>
            </el-form-item>
          </el-form>
        </el-col>
      </el-row>
      <el-table :data="tableData" border tooltip-effect="dark" @selection-change="handleSelectionChange">
        <el-table-column type="selection"></el-table-column>
        <el-table-column type="expand">
            <template slot-scope="props">
              <el-form label-position="left" class="table-expand">
                <el-form-item label="ID">
                  <span>{{ props.row.id }}</span>
                </el-form-item>
                <el-form-item label="密码">
                  <span>{{ props.row.Password }}</span>
                </el-form-item>
                <el-form-item label="创建用户">
                  <span>{{ props.row.Creater }}</span>
                </el-form-item>
                <el-form-item label="创建时间">
                  <span>{{ props.row.CreateTime }}</span>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>
        <el-table-column prop="Name" label="用户名"></el-table-column>
        <el-table-column prop="WorkNumber" label="工号"></el-table-column>
        <el-table-column prop="StationName" label="所属岗位"></el-table-column>
        <el-table-column prop="OrganizationName" label="所属部门"></el-table-column>
        <el-table-column prop="FactoryName" label="所属厂区"></el-table-column>
      </el-table>
      <!--<el-pagination background layout="prev, pager, next"-->
                     <!--:total="total"-->
                     <!--:current-page="currentPage"-->
                     <!--:page-sizes="[10,20,30]"-->
                     <!--:page-size="pagesize"-->
                     <!--@size-change="handleSizeChange"-->
                     <!--@current-change="handleCurrentChange">-->
      <!--</el-pagination>-->
      <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="40%">
        <el-form :model="UserForm" label-width="80px" :rules="rules" ref="ruleForm">
          <el-form-item label="ID">
            <el-input v-model="UserForm.id" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="用户名" prop="Name">
            <el-input v-model="UserForm.Name"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="Password">
            <el-input v-model="UserForm.Password"></el-input>
          </el-form-item>
          <el-form-item label="工号" prop="WorkNumber">
            <el-input v-model="UserForm.WorkNumber"></el-input>
          </el-form-item>
          <el-form-item label="所属岗位">
            <el-input v-model="UserForm.StationName"></el-input>
          </el-form-item>
          <el-form-item label="所属部门">
            <el-input v-model="UserForm.OrganizationName"></el-input>
          </el-form-item>
          <el-form-item label="所属厂区">
            <el-input v-model="UserForm.FactoryName"></el-input>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="save('ruleForm')">保存</el-button>
        </span>
      </el-dialog>
    </el-col>
  </el-row>
</template>

<script>
  export default {
    name: "Personnel",
    data(){
      return {
        tableData:[],
        // total:3,
        // pagesize:2,
        // currentPage:1
        multipleSelection: [],
        dialogVisible: false,
        UserForm:'',
        dialogTitle:'',
        rules:{
          Name:[
            {required: true, message: '请输入用户名', trigger: 'blur'}
          ],
          Password:[
            {required: true, message: '请输入密码', trigger: 'blur'}
          ],
          WorkNumber:[
            {required: true, message: '请输入工号', trigger: 'blur'}
          ]
        }
      }
    },
    mounted() {
      this.getTableData()
    },
    methods:{
      getTableData(){
        this.axios.get("/api/CUID",{
          params: {
            tableName: "User",
            limit:1000000,
            offset:0
          }
        }).then(res =>{
          var data = JSON.parse(res.data)
          this.tableData = data.rows
        },res =>{
          console.log("请求错误")
        })
      },
      // handleSizeChange(pagesize){ //每页条数切换
      //   this.pagesize = pagesize
      //   this.handleCurrentChange(this.currentPage)
      // },
      // handleCurrentChange(currentPage) { // 页码切换
      //   this.currentPage = currentPage
      // }
      handleSelectionChange(val){
        this.multipleSelection = val;
      },
      openDialog(val){
        this.dialogTitle = val
        if(val == "add"){
          this.dialogVisible = true
          this.UserForm = {
            id:"",
            Name:"",
            Password:"",
            WorkNumber:"",
            StationName:"",
            OrganizationName:"",
            FactoryName:""
          }
        }else if(val == "edit"){
          if(this.multipleSelection.length == 1){
            this.dialogVisible = true
            let data = this.multipleSelection[0]
            this.UserForm = {
              id:data.id,
              Name:data.Name,
              Password:data.Password,
              WorkNumber:data.WorkNumber,
              StationName:data.StationName,
              OrganizationName:data.OrganizationName,
              FactoryName:data.FactoryName
            }
          }else{
            this.$message({
              message: '请选择一条数据进行修改',
              type: 'warning'
            });
          }
        }
      },
      save(formName){
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.UserForm.tableName = "User"
            if(this.dialogTitle == "add"){
              this.axios.post("/api/CUID",this.qs.stringify(this.UserForm)).then(res =>{
                console.log(res)
                this.getTableData()
              },res =>{
                console.log("请求错误")
              })
            }else if(this.dialogTitle == "edit"){
              console.log(this.UserForm)
              this.axios.put("/api/CUID",this.qs.stringify(this.UserForm)).then(res =>{
                console.log(res)
                this.getTableData()
              },res =>{
                console.log("请求错误")
              })
            }
          } else {
            return false;
          }
        });
      },
      del(){
        if(this.multipleSelection.length >= 1){
          this.$confirm('确定删除所选记录？', '提示', {
            confirmButtonText: '删除',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            this.axios.delete("/api/CUID",qs.stringify(this.multipleSelection)).then(res =>{
              console.log(res)
              this.$message({
                type: 'success',
                message: '删除成功!'
              });
                this.getTableData()
              },res =>{
                console.log("请求错误")
              })
          }).catch(() => {
            this.$message({
              type: 'info',
              message: '已取消'
            });
          });
        }else{
          this.$message({
            message: '至少选择一条数据进行删除',
            type: 'warning'
          });
        }
      }
    }
  }
</script>

<style scoped>

</style>
