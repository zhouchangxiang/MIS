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
          data:[],
          limit:5,
          offset:1,
          total:0,
          searchProp:"",
          searchPropList:[
            {label:"用户名",prop:"Name"},
            {label:"工号",prop:"WorkNumber"}
          ],
          tableSelection:true, //是否在第一列添加复选框
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
            {label:"密码",prop:"Password",type:"input",value:""},
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
      }
    }
  }
</script>

<style scoped>

</style>
