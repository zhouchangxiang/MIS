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
            <el-input placeholder="请输入搜索内容" size="small" v-model="searchVal"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="success" icon="el-icon-search" size="small" @click="searchTab">搜索</el-button>
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
      <el-table-column prop="ID" label="ID"></el-table-column>
      <el-table-column prop="PriceName" label="价格名称"></el-table-column>
      <el-table-column prop="PriceValue" label="价格值"></el-table-column>
      <el-table-column prop="PriceType" label="价格类型"></el-table-column>
      <el-table-column prop="StartTime" label="开始时间"></el-table-column>
      <el-table-column prop="EndTime" label="结束时间"></el-table-column>
      <el-table-column prop="IsEnabled" label="是否启用"></el-table-column>
      <el-table-column prop="Description" label="描述"></el-table-column>
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
        <el-form-item label="价格名称" prop="PriceName">
          <el-input v-model="submitForm.PriceName"></el-input>
        </el-form-item>
        <el-form-item label="价格值" prop="PriceValue">
          <el-input v-model="submitForm.PriceValue"></el-input>
        </el-form-item>
        <el-form-item label="价格类型" prop="PriceType">
          <el-input v-model="submitForm.PriceType"></el-input>
        </el-form-item>
        <el-form-item label="是否启用" prop="IsEnabled">
          <el-input v-model="submitForm.IsEnabled"></el-input>
        </el-form-item>
        <el-form-item label="开始时间" prop="StartTime">
          <el-input v-model="submitForm.StartTime"></el-input>
        </el-form-item>
        <el-form-item label="结束时间" prop="EndTime">
          <el-input v-model="submitForm.EndTime"></el-input>
        </el-form-item>
        <el-form-item label="描述" prop="Description">
          <el-input v-model="submitForm.Description"></el-input>
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
    name: "ElectricPrice",
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
          PriceName:[
            {required: true, message: '价格名称', trigger: 'blur'}
          ],
          PriceValue:[
            {required: true, message: '价格值', trigger: 'blur'}
          ],
          PriceType:[
            {required: true, message: '价格类型', trigger: 'blur'}
          ]
        },
        region:"",
        regionList:[
          {label:"价格名称",value:"PriceName"},
          {label:"价格类型",value:"PriceType"},
        ],
        searchVal:""
      }
    },
    mounted() {
      this.getTableData()
    },
    methods:{
      getTableData(){
        this.axios.get("/api/CUID",{
          params: {
            tableName: "ElectricPrice",
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
        this.axios.get("/api/CUID",{
          params: {
            tableName: "ElectricPrice",
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
            PriceName:"",
            PriceValue:"",
            PriceType:"",
            IsEnabled:"",
            StartTime:"",
            EndTime:"",
            Description:"",
          }
        }else if(val == "edit"){
          if(this.multipleSelection.length == 1){
            this.dialogVisible = true
            let data = this.multipleSelection[0]
            this.submitForm = {
              ID:data.ID,
              PriceName:data.PriceName,
              PriceValue:data.PriceValue,
              PriceType:data.PriceType,
              IsEnabled:data.IsEnabled,
              StartTime:data.StartTime,
              EndTime:data.EndTime,
              Description:data.Description,
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
            this.submitForm.tableName = "ElectricPrice"
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
                tableName: "ElectricPrice",
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
