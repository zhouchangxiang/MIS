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
      <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" :close-on-click-modal="false" width="40%">
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
        total:0,
        pagesize:5,
        currentPage:1,
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
      handleSelectionChange(val){  //选择行数
        this.multipleSelection = val;
      },
      openDialog(val){
        this.dialogTitle = val
        if(val == "add"){
          this.dialogVisible = true
          this.UserForm = {
            ID:"",
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
              ID:data.id,
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
            this.UserForm.Creater = "管理员"
            if(this.dialogTitle == "add"){
              this.axios.post("/api/CUID",this.qs.stringify(this.UserForm)).then(res =>{
                if(res.data == "OK"){
                  this.getTableData()
                }else{
                  this.$message({
                    type: 'info',
                    message: res.data
                  });
                }
                this.dialogVisible = false
              },res =>{
                console.log("请求错误")
              })
            }else if(this.dialogTitle == "edit"){
              this.axios.put("/api/CUID",this.qs.stringify(this.UserForm)).then(res =>{
                if(res.data == "OK"){
                  this.getTableData()
                }else{
                  this.$message({
                    type: 'info',
                    message: res.data
                  });
                }
                this.dialogVisible = false
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
        let mulId = []
        this.multipleSelection.forEach(item=>{
            mulId.push({id:item.id});
        })
        if(this.multipleSelection.length >= 1){
          this.$confirm('确定删除所选记录？', '提示', {
            distinguishCancelAndClose:true,
            type: 'warning'
          }).then(()  => {
            this.axios.delete("/api/CUID",{
              params: {
                tableName: "User",
                Creater: "管理员",
                delete_data: mulId
              }
            }).then(res =>{
              if(res.data == "OK"){
                this.$message({
                  type: 'success',
                  message: '删除成功'
                });
              }
              this.getTableData()
            },res =>{
              console.log("请求错误")
            })
          }).catch(()   => {
            this.$message({
              type: 'info',
              message: '已取消删除'
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
