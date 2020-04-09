<template>
  <el-col :span="24" style="background-color:#FFF;padding: 15px;">
    <el-row>
      <el-col :span="24">
        <el-form :inline="true">
          <el-form-item>
            <el-select v-model="region" placeholder="请选择搜索字段" size="small">
              <el-option v-for="(item,index) in regionList" :label="item.label" :value="item.value" :key="index"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            {{ selectedPlanNum }}
            <el-input placeholder="请输入搜索内容" size="small" v-model="searchVal"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="success" icon="el-icon-search" size="small" @click="searchTab">搜索</el-button>
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
      <el-table-column prop="ID" label="ID"></el-table-column>
      <el-table-column prop="PuidName" label="工艺段"></el-table-column>
      <el-table-column prop="PlanNum" label="计划单号"></el-table-column>
      <el-table-column prop="BatchID" label="批次号"></el-table-column>
      <el-table-column prop="BrandName" label="品名"></el-table-column>
      <el-table-column prop="PlanQuantity" label="计划重量"></el-table-column>
      <el-table-column prop="WaterConsumption" label="水用量"></el-table-column>
      <el-table-column prop="SteamConsumption" label="汽用量"></el-table-column>
      <el-table-column prop="ProductionDate" label="生产日期"></el-table-column>
      <el-table-column prop="StartTime" label="开始时间"></el-table-column>
      <el-table-column prop="EndTime" label="结束时间"></el-table-column>
      <el-table-column prop="CreateDate" label="创建日期"></el-table-column>
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
      <el-form :model="submitForm" label-width="80px" :rules="rules" ref="ruleForm">
        <el-form-item label="ID">
          <el-input v-model="submitForm.ID" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="工艺段" prop="PuidName">
          <el-input v-model="submitForm.PuidName"></el-input>
        </el-form-item>
        <el-form-item label="计划单号" prop="PlanNum">
          <el-input v-model="submitForm.PlanNum"></el-input>
        </el-form-item>
        <el-form-item label="批次号" prop="BatchID">
          <el-input v-model="submitForm.BatchID"></el-input>
        </el-form-item>
        <el-form-item label="品名" prop="BrandName">
          <el-input v-model="submitForm.BrandName"></el-input>
        </el-form-item>
        <el-form-item label="计划重量" prop="PlanQuantity">
          <el-input v-model="submitForm.PlanQuantity"></el-input>
        </el-form-item>
        <el-form-item label="水用量" prop="WaterConsumption">
          <el-input v-model="submitForm.WaterConsumption"></el-input>
        </el-form-item>
        <el-form-item label="汽用量" prop="SteamConsumption">
          <el-input v-model="submitForm.SteamConsumption"></el-input>
        </el-form-item>
        <el-form-item label="生产日期" prop="ProductionDate">
          <el-input v-model="submitForm.ProductionDate"></el-input>
        </el-form-item>
        <el-form-item label="开始时间" prop="StartTime">
          <el-input v-model="submitForm.StartTime"></el-input>
        </el-form-item>
        <el-form-item label="结束时间" prop="EndTime">
          <el-input v-model="submitForm.EndTime"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="save('ruleForm')">保存</el-button>
      </span>
    </el-dialog>
  </el-col>
</template>

<script>
  export default {
    name: "Task",
    props:['selectedPlanNum'],
    data(){
      return {
        tableData:[],
        total:0,
        pagesize:5,
        currentPage:1,
        multipleSelection: [],
        dialogVisible: false,
        submitForm:'',
        dialogTitle:'',
        rules:{
          PuidName:[
            {required: true, message: '工艺段', trigger: 'blur'}
          ],
          PlanNum:[
            {required: true, message: '计划单号', trigger: 'blur'}
          ],
          BatchID:[
            {required: true, message: '批次号', trigger: 'blur'}
          ],
          BrandName:[
            {required: true, message: '品名', trigger: 'blur'}
          ],
          PlanQuantity:[
            {required: true, message: '计划重量', trigger: 'blur'}
          ],
          WaterConsumption:[
            {required: true, message: '水用量', trigger: 'blur'}
          ],
          SteamConsumption:[
            {required: true, message: '汽用量', trigger: 'blur'}
          ],
          ProductionDate:[
            {required: true, message: '生产日期', trigger: 'blur'}
          ],
          StartTime:[
            {required: true, message: '开始时间', trigger: 'blur'}
          ],
          EndTime:[
            {required: true, message: '结束时间', trigger: 'blur'}
          ],
        },
        region:"",
        regionList:[
          {label:"工艺段",value:"PuidName"},
          {label:"计划单号",value:"PlanNum"},
          {label:"批次号",value:"BatchID"},
          {label:"品名",value:"BrandName"},
        ],
        searchVal:"",
      }
    },
    created(){

    },
    watch:{
      // selectedPlanNum(newVal,oldVal){
      //   console.log(newVal)
      // }
　　},
    mounted() {
      this.getTableData()
    },
    methods:{
      getTableData(){
        this.axios.get("/api/CUID",{
          params: {
            tableName: "BatchMaintainTask",
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
      searchTab(){
        console.log(this.selectedPlanNum)
        this.axios.get("/api/CUID",{
          params: {
            tableName: "BatchMaintainTask",
            field:this.region,
            fieldvalue:this.searchVal,
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
      openDialog(val){
        this.dialogTitle = val
        if(val == "add"){
          this.dialogVisible = true
          this.submitForm = {
            ID:"",
            PuidName:"",
            PlanNum:"",
            BatchID:"",
            BrandName:"",
            PlanQuantity:"",
            WaterConsumption:"",
            SteamConsumption:"",
            ProductionDate:"",
            StartTime:"",
            EndTime:"",
          }
        }else if(val == "edit"){
          if(this.multipleSelection.length == 1){
            this.dialogVisible = true
            let data = this.multipleSelection[0]
            this.submitForm = {
              ID:data.ID,
              PuidName:data.PuidName,
              PlanNum:data.PlanNum,
              BatchID:data.BatchID,
              BrandName:data.BrandName,
              PlanQuantity:data.PlanQuantity,
              WaterConsumption:data.WaterConsumption,
              SteamConsumption:data.SteamConsumption,
              ProductionDate:data.ProductionDate,
              StartTime:data.StartTime,
              EndTime:data.EndTime,
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
            this.submitForm.tableName = "BatchMaintainTask"
            if(this.dialogTitle == "add"){
              this.axios.post("/api/CUID",this.qs.stringify(this.submitForm)).then(res =>{
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
              this.axios.put("/api/CUID",this.qs.stringify(this.submitForm)).then(res =>{
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
            mulId.push({id:item.ID});
        })
        if(this.multipleSelection.length >= 1){
          this.$confirm('确定删除所选记录？', '提示', {
            distinguishCancelAndClose:true,
            type: 'warning'
          }).then(()  => {
            this.axios.delete("/api/CUID",{
              params: {
                tableName: "BatchMaintainTask",
                delete_data: JSON.stringify(mulId)
              }
            }).then(res =>{
              console.log(res)
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
