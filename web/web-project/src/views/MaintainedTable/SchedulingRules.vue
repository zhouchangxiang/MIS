<template>
  <el-row>
    <el-col :span="24">
      <div class="card-head">
        <span style="margin-left: 10px;" class="text-size-normol">调度维护</span>
      </div>
      <div class="platformContainer" style="margin-bottom: 10px;">
        <tableView :tableData="TableData" @getTableData="getTableData"></tableView>
      </div>
      <div class="platformContainer">
        <tableView :tableData="ShiftsClassTableData" @getTableData="getShiftsClassTableData"></tableView>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  import tableView from '@/views/SystemManage/CommonTable'
  export default {
    name: "SchedulingRules",
    components:{tableView},
    data(){
      return {
        TableData:{
          tableName:"Shifts",
          column:[
            {prop:"ShiftsName",label:"班次名称"},
            {prop:"ShiftsCode",label:"班次编码"},
            {prop:"BeginTime",label:"班次开始时间"},
            {prop:"EndTime",label:"班次结束时间"},
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
          searchProp:"",
          searchPropList:[
            {label:"班次名称",prop:"ShiftsName"}
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
            {label:"班次名称",prop:"ShiftsName",type:"input",value:""},
            {label:"班次编码",prop:"ShiftsCode",type:"input",value:""},
            {label:"班次开始时间",prop:"BeginTime",type:"input",value:""},
            {label:"班次结束时间",prop:"EndTime",type:"input",value:""},
          ],
        },
        ShiftsClassTableData:{
          tableName:"ShiftsClass",
          column:[
            {prop:"ShiftsClassName",label:"班制名称"},
            {prop:"ShiftsClassCode",label:"班制编码"}
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
          searchProp:"",
          searchPropList:[
            {label:"班制名称",prop:"ShiftsClassName"},
            {label:"班制编码",prop:"ShiftsClassCode"},
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
            {label:"班制名称",prop:"ShiftsClassName",type:"input",value:""},
            {label:"班制编码",prop:"ShiftsClassCode",type:"input",value:""}
          ],
        },
      }
    },
     mounted() {
      this.getTableData()
      this.getShiftsClassTableData()
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
      getShiftsClassTableData(){
        var that = this
        var params = {
          tableName: this.ShiftsClassTableData.tableName,
          limit:this.ShiftsClassTableData.limit,
          offset:this.ShiftsClassTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          var data = JSON.parse(res.data)
          this.ShiftsClassTableData.data = data.rows
          this.ShiftsClassTableData.total = data.total
        },res =>{
          console.log("请求错误")
        })
      },
    }
  }
</script>

<style scoped>

</style>
