<template>
  <el-row>
    <el-col :span="24">
      <div class="card-head">
        <span style="margin-left: 10px;" class="text-size-normol">角色管理</span>
      </div>
      <div class="platformContainer">
        <tableView :tableData="TableData" @getTableData="getRoleTable" @privileges="privileges"></tableView>
      </div>
      <el-dialog title="提示" :visible.sync="dialogVisible" width="60%">
        <el-transfer :titles="['全部权限', '当前权限']" v-model="transferValue" :data="transferData"></el-transfer>
        <span slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
        </span>
      </el-dialog>
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
        dialogVisible:false,
        transferValue:[],
        transferData:[]
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
        this.dialogVisible = true
        var that = this
        var params = {
          tableName: "Menu",
          limit:100000000,
          offset:0
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          var data = JSON.parse(res.data)
          console.log(data)
        },res =>{
          console.log("请求错误")
        })
      }
    }
  }
</script>

<style scoped>

</style>
