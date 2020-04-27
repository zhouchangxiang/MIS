<template>
  <div>
    <el-form :inline="true">
      <el-form-item>
        <el-select v-model="tableData.searchProp" placeholder="请选择搜索字段" size="small">
          <el-option v-for="(item,index) in tableData.searchPropList" :label="item.label" :value="item.prop" :key="index"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-input placeholder="请输入搜索内容" size="small" v-model="tableData.searchVal"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="success" icon="el-icon-search" size="small" @click="searchTab">搜索</el-button>
      </el-form-item>
      <el-form-item v-for="(item,index) in tableData.handleType" :key="index">
        <el-button :type="item.type" size="small" @click="tableClickHandleButton(item.label,item.clickEvent)">{{ item.label }}</el-button>
      </el-form-item>
    </el-form>
    <el-table :data="tableData.data" border ref="multipleTable" @selection-change="handleSelectionChange" @row-click="handleRowClick">
      <el-table-column type="selection" v-if="tableData.tableSelection"></el-table-column>
      <el-table-column v-for="(item,index) in tableData.column" :key="index" :prop="item.prop" :label="item.label"></el-table-column>
    </el-table>
    <div class="paginationClass">
      <el-pagination background  layout="total, sizes, prev, pager, next, jumper"
       :total="tableData.total"
       :current-page="tableData.offset"
       :page-sizes="[5,10,20]"
       :page-size="tableData.limit"
       @size-change="handleSizeChange"
       @current-change="handleCurrentChange">
      </el-pagination>
    </div>
    <el-dialog v-if="tableData.hasOwnProperty('handleForm')" :title="tableData.dialogTitle" :visible.sync="tableData.dialogVisible" :close-on-click-modal="false" width="40%">
      <el-form :model="tableData.submitForm" label-width="110px">
        <el-form-item v-for="(item,index) in tableData.handleForm" :key="index" :label="item.label" :prop="item.prop">
          <el-input v-if="item.type === 'input'" v-model="item.value" :disabled="item.disabled"></el-input>
          <el-select v-if="item.type === 'select'" v-model="item.value" placeholder="请选择">
            <el-option v-for="(i,d) in item.DownData" :key="d" :label="i[item.showDownField]" :value="i[item.showDownField]"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="tableData.dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="save">保存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
  export default {
    name: "CommonTable",
    props:['tableData'],
    data(){
      return {

      }
    },
    created(){

    },
    methods:{
      handleSizeChange(limit){ //每页条数切换
        this.tableData.limit = limit
        this.$emit('getTableData')
      },
      handleCurrentChange(offset) { // 页码切换
        this.tableData.offset = offset
        this.$emit('getTableData')
      },
      handleSelectionChange(val){ //选择行数
        this.tableData.multipleSelection = val;
      },
      handleRowClick(row){
        if(this.tableData.tableSelectionRadio){
          this.$refs.multipleTable.clearSelection();
          this.$refs.multipleTable.toggleRowSelection(row)
        }else{
          this.$refs.multipleTable.toggleRowSelection(row)
        }
      },
      searchTab(){
        this.axios.get("/api/CUID",{
          params: {
            tableName: this.tableData.tableName,
            field:this.tableData.searchProp,
            fieldvalue:this.tableData.searchVal,
            limit:this.tableData.limit,
            offset:this.tableData.offset - 1
          }
        }).then(res =>{
          var data = JSON.parse(res.data)
          this.tableData.data = data.rows
          this.tableData.total = data.total
        },res =>{
          console.log("请求错误")
        })
      },
      tableClickHandleButton(label,event){
        this.tableData.dialogTitle = label
        if(label === "添加"){
          this.determineSubmitType()
          this.tableData.dialogVisible = true
          this.tableData.handleForm.forEach(item =>{
            item.value = ""
          })
        }else if(label === "修改"){
          this.determineSubmitType()
          if(this.tableData.multipleSelection.length == 1){
            this.tableData.dialogVisible = true
            this.tableData.handleForm.forEach(item =>{
              item.value = this.tableData.multipleSelection[0][item.prop]
            })
          }else{
            this.$message({
              type: 'info',
              message: '请单选一条数据 '
            })
          }
        }else if(label === "删除"){
          var params = {tableName:this.tableData.tableName}
          var mulId = []
          if(this.tableData.multipleSelection.length >= 1){
            this.tableData.multipleSelection.forEach(item =>{
              mulId.push({id:item.ID});
            })
            params.delete_data = JSON.stringify(mulId)
            this.$confirm('确定删除所选记录？', '提示', {
              distinguishCancelAndClose:true,
              type: 'warning'
            }).then(()  => {
              this.axios.delete("/api/CUID",{
                params: params
              }).then(res =>{
                if(res.data == "OK"){
                  this.$message({
                    type: 'success',
                    message: '删除成功'
                  });
                }
                this.$emit('getTableData')
              },res =>{
                console.log("请求错误")
              })
            }).catch(() => {
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
        }else{
          this.$emit(event)
        }
      },
      determineSubmitType(){  //判断表单提交的字段类型
        this.tableData.handleForm.forEach(item =>{
          if(item.type === "select"){
            var params = {
              tableName: item.Downtable,
              limit:100000000,
              offset:0
            }
            this.axios.get("/api/CUID",{
              params: params
            }).then(res =>{
              var data = JSON.parse(res.data)
              item.DownData = data.rows
            },res =>{
              console.log("请求错误")
            })
          }
        })
      },
      save(){
        if(this.tableData.dialogTitle === "添加"){
          var params = {tableName:this.tableData.tableName}
          this.tableData.handleForm.forEach(item =>{
            // var numRe = new RegExp(item.reg)
            // if (!numRe.test(item.value)) {
            //   this.$message({
            //      type: 'error',
            //      message: '请输入数字 '
            //   })
            // }
            params[item.prop] = item.value
          })
          this.axios.post("/api/CUID",this.qs.stringify(params)).then(res =>{
            if(res.data == "OK"){
              this.$emit('getTableData')
            }else{
              this.$message({
                type: 'info',
                message: res.data
              });
            }
            this.tableData.dialogVisible = false
          },res =>{
            console.log("请求错误")
          })
        }else if(this.tableData.dialogTitle === "修改"){
          var params = {tableName:this.tableData.tableName}
          this.tableData.handleForm.forEach(item =>{
            params[item.prop] = item.value
          })
          this.axios.put("/api/CUID",this.qs.stringify(params)).then(res =>{
            if(res.data == "OK"){
              this.$emit('getTableData')
            }else{
              this.$message({
                type: 'info',
                message: res.data
              });
            }
            this.tableData.dialogVisible = false
          },res =>{
            console.log("请求错误")
          })
        }
      }
    }
  }
</script>

<style scoped>

</style>
