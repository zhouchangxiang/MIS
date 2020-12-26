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
    name: "TagDetail",
    components:{tableView},
    data(){
      return {
        TableData:{
          tableName:"TagDetail",
          column:[
            {prop:"EnergyClass",label:"类型"},
            {prop:"AreaName",label:"区域名称"},
            {prop:"FEFportIP",label:"采集点名称"},
            {prop:"IsExport",label:"是否导出"},
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
          searchProp:"",
          searchPropList:[
            {label:"区域名称",prop:"AreaName"},
            {label:"区域编码",prop:"AreaCode"}
          ],
          tableSelection:true, //是否需要选择框
          tableSelectionRadio:false, //是否需要单选
          searchVal:"",
          multipleSelection: [],
          dialogVisible: false,
          dialogTitle:'',
          handleType:[
            {type:"warning",label:"修改"},
          ],
          handleForm:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true},
            {label:"是否导出",prop:"IsExport",type:"select",value:"",Downtable:"ISFlag",showDownField:"Description"},
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
