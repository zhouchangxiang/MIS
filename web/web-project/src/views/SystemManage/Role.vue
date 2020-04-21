<template>
  <el-row>
    <el-col :span="24">
      <div class="card-head">
        <span style="margin-left: 10px;" class="text-size-normol">角色管理</span>
      </div>
      <div class="platformContainer">
        <tableView :tableData="TableData" @getTableData="getRoleTable" @privileges="privileges"></tableView>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  import tableView from '@/views/SystemManage/CommonTable'
  export default {
    name: "Role",
    components:{tableView},
    data(){
      return {
        TableData:{
          tableName:"Role",
          column:[
            {prop:"RoleName",label:"角色名称"},
            {prop:"RoleCode",label:"角色编码"},
            {prop:"Description",label:"描述"},
            {prop:"ParentNode",label:"所属部门"},
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
          searchProp:"",
          searchPropList:[
            {label:"角色名称",prop:"RoleName"},
            {label:"角色编码",prop:"RoleCode"},
          ],
          searchVal:"",
          handleType:[
            {type:"primary",label:"分配权限",clickEvent:"privileges"},
          ],
        },
      }
    },
    created(){
      this.getRoleTable()
    },
    methods:{
      getRoleTable(){
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
          that.TableData.data = data.rows
          that.TableData.total = data.total
        },res =>{
          console.log("请求错误")
        })
      },
      privileges(){
        console.log("权限分配")
      }
    }
  }
</script>

<style scoped>

</style>
