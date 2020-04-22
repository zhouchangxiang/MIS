<template>
  <el-row>
    <el-col :span="24">
      <div class="card-head">
        <span style="margin-left: 10px;" class="text-size-normol">人员管理</span>
      </div>
      <div class="platformContainer">
        <tableView :tableData="TableData" @getTableData="getTableData"></tableView>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  var moment = require('moment');
  import tableView from '@/views/SystemManage/CommonTable'
  export default {
    name: "Personnel",
    components:{tableView},
    data(){
      return {
        TableData:{
          tableName:"User",
          column:[
            {prop:"Name",label:"用户名"},
            {prop:"Password",label:"密码"},
            {prop:"WorkNumber",label:"工号"},
            {prop:"Creater",label:"创建人"},
            {prop:"CreateTime",label:"创建时间"},
            {prop:"LastLoginTime",label:"最近在线时间"},
          ],
          deleteKey:"id",
          data:[],
          limit:5,
          offset:1,
          total:0,
          searchProp:"",
          searchPropList:[
            {label:"用户名",prop:"Name"},
            {label:"工号",prop:"WorkNumber"}
          ],
          tableSelection:true, //是否需要选择框
          tableSelectionRadio:false, //是否需要单选
          searchVal:"",
          multipleSelection: [],
          dialogVisible: false,
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
          },
          handleType:[
            {type:"primary",label:"添加"},
            {type:"warning",label:"修改"},
            {type:"danger",label:"删除"},
          ],
          handleForm:[
            {label:"ID",prop:"id",type:"input",value:"",disabled:true},
            {label:"用户名",prop:"Name",type:"input",value:""},
            {label:"密码",prop:"Password",type:"input",value:"",reg:"/^[0-9]+$/"},
            {label:"工号",prop:"WorkNumber",type:"input",value:"",reg:"/^[0-9]+$/"}
          ],
        },
      }
    },
    mounted() {
      this.getTableData()
    },
    methods:{
      getTableData(){
        var that = this
        var params = {
          tableName: this.TableData.tableName,
          limit:this.TableData.limit,
          offset:this.TableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          var data = JSON.parse(res.data)
          this.TableData.data = data.rows
          this.TableData.total = data.total
        },res =>{
          console.log("请求错误")
        })
      },
      handleSelectionChange(val){  //选择行数
        this.multipleSelection = val;
      },
      openDialog(val){
        this.dialogTitle = val
        if(val === "add"){
          this.dialogVisible = true
          this.UserForm = {
            ID:"",
            Name:"",
            Password:"",
            WorkNumber:"",
            Creater: sessionStorage.getItem('UserName'),
            CreateTime:moment(new Date()).format('YYYY-MM-DD HH:mm:ss')
          }
        }else if(val === "edit"){
          if(this.multipleSelection.length === 1){
            this.dialogVisible = true
            let data = this.multipleSelection[0]
            this.UserForm = {
              ID:data.id,
              Name:data.Name,
              Password:data.Password,
              WorkNumber:data.WorkNumber
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
                delete_data: JSON.stringify(mulId)
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
