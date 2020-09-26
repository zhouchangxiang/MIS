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
    name: "PowerLoadRateRange",
    components:{tableView},
    data(){
      return {
        TableData:{
          tableName:"RatedPowerMaintain",
          column:[
            {prop:"AreaName",label:"区域"},
            {prop:"RatedPowerValue",label:"额定功率值"},
            {prop:"RatedPowerTime",label:"时间"},
            {prop:"CreateDate",label:"创建日期"},
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
          searchProp:"",
          searchPropList:[
            {label:"时间",prop:"RatedPowerTime"}
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
            {label:"额定功率值",prop:"RatedPowerValue",type:"input",value:""},
            {label:"时间",prop:"RatedPowerTime",type:"input",value:""}
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
