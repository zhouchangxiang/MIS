<template>
  <el-row>
    <el-col :span="24">
      <div class="platformContainer">
        <tableView :tableData="TableData" @getTableData="getTableData"></tableView>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  import tableView from '@/views/SystemManage/CommonTable'
  export default {
    name: "electricityBalance",
    components:{tableView},
    data(){
      return {
        TableData:{
          tableName:"EarlyWarningPercentMaintain",
          column:[
            {prop:"AreaName",label:"区域"},
            {prop:"EQPName",label:"设备名称"},
            {prop:"Percent",label:"三相电流不平衡百分比"},
            {prop:"Descrption",label:"描述"},
            {prop:"CreateDate",label:"时间"},
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
          searchProp:"",
          searchPropList:[
            {label:"区域",prop:"AreaName"},
            {label:"设备名称",prop:"EQPName"}
          ],
          tableSelection:true, //是否需要选择框
          tableSelectionRadio:false, //是否需要单选
          searchVal:"",
          multipleSelection: [],
          dialogVisible: false,
          dialogTitle:'',
          handleType:[
            {type:"primary",label:"添加"},
            {type:"warning",label:"修改"},
            {type:"danger",label:"删除"},
          ],
          handleForm:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true},
            {label:"区域",prop:"AreaName",type:"input",value:""},
            {label:"设备名称",prop:"EQPName",type:"input",value:""},
            {label:"三相电流不平衡百分比",prop:"Percent",type:"input",value:""},
            {label:"描述",prop:"Descrption",type:"input",value:""}
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
