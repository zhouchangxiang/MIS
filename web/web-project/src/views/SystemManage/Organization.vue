<template>
  <div style="width: 100%;height: 100%;background-color: #fff">
    <div class="chartContainer">
      <el-checkbox-group v-model="chartSettingsCheckbox" size="small" fill="#082F4C">
        <el-checkbox-button v-for="(item,index) in settingsOptions" :label="item.label" :key="index" :value="item.value" @change="changeCheckbox">{{ item.label }}</el-checkbox-button>
      </el-checkbox-group>
      <ve-tree :data="chartData" :settings="chartSettings"></ve-tree>
    </div>
  </div>
</template>

<script>
  const treeData = {
    name: '好护士药业有限责任公司',
    value: 1,
    children: [
      {
        name: 'a',
        value: 1,
        children: [
          {
            name: 'a-a',
            value: 2
          },
          {
            name: 'a-b',
            value: 2
          }
        ]
      },
      {
        name: 'b',
        value: 1,
        children: [
          {
            name: 'b-a',
            value: 2
          },
          {
            name: 'b-b',
            value: 2
          }
        ]
      },
      {
        name: 'c',
        value: 3,
        children: [
          {
            name: 'c-a',
            value: 4
          },
          {
            name: 'c-b',
            value: 2
          }
        ]
      },
      {
        name: 'd',
        value: 3,
        children: [
          {
            name: 'd-a',
            value: 4
          },
          {
            name: 'd-b',
            value: 2
          }
        ]
      }
    ]
  }
  export default {
    name: "Organization",
    data(){
      return {
        chartSettingsCheckbox:"",
        settingsOptions: [
          {label:'垂直方向',value:"0"},
          {label:'折线形状',value:"1"}
        ],
        chartSettings: {
          seriesMap:{
            tree:{
              orient: 'LR',

            }
          }
        },
        chartData: {
          columns: ['name', 'value'],
          rows: [{
            name: 'tree',
            value: [treeData]
          }]
        }
      }
    },
    methods: {
      changeCheckbox(a,b){
        if(b.target.defaultValue === "垂直方向"){
          if(a){
            this.chartSettings.seriesMap.tree.orient="TB"
          }else{
            this.chartSettings.seriesMap.tree.orient="LR"
          }
        }else if(b.target.defaultValue === "折线形状"){
          console.log(a)
          if(a){
            this.chartSettings.seriesMap.tree.edgeShape="curve"
          }else{
            this.chartSettings.seriesMap.tree.edgeShape= 'polyline'
          }
        }
      }
      // clickNode: function(node){
      //   // eslint-disable-next-line
      //   console.log(node)
      // }
      // renderContent (h, data) {
      //   return data.label
      // },
      // onNodeClick(e, data) {
      //   this.tranLeft = (e.pageX - 240) + 'px'
			// 	this.tranTop = (e.pageY - 60) + 'px'
      //   if(this.selectedId == data.id && this.showBox){
      //     this.showBox = false
      //   }else{
      //     this.showBox = true
      //   }
      //   this.selectedId = data.id
      //   this.selectedLabel = data.label
      // },
      // addNode(){
      //   var treeData = this.treeData
      //   this.showBox = false
      //   this.$prompt('请输入子节点名称', '给'+this.selectedLabel+'添加子节点', {
      //     confirmButtonText: '确定',
      //     cancelButtonText: '取消',
      //   }).then(({ value }) => {
      //     this.$message({
      //       type: 'success',
      //       message: '已成功为' + this.selectedLabel + '添加子节点：' + value
      //     });
      //   }).catch(action => {
      //     console.log(action)
      //     this.$message({
      //       type: 'info',
      //       message: '取消添加'
      //     });
      //   });
      // },
      // editNode(){
      //   this.showBox = false
      //   this.$prompt('请输入子节点名称', '修改'+this.selectedLabel+'的名称', {
      //     confirmButtonText: '确定',
      //     cancelButtonText: '取消',
      //   }).then(({ value }) => {
      //     this.$message({
      //       type: 'success',
      //       message: '已将' + this.selectedLabel + '修改为：' + value
      //     });
      //   }).catch(() => {
      //     this.$message({
      //       type: 'info',
      //       message: '取消修改'
      //     });
      //   });
      // },
      // delNode(){
      //   this.showBox = false
      //   this.$confirm('此操作将永久删除该节点, 是否继续?', '删除'+this.selectedLabel+'节点', {
      //     confirmButtonText: '确定',
      //     cancelButtonText: '取消',
      //     type: 'warning'
      //   }).then(() => {
      //     this.$message({
      //       type: 'success',
      //       message: '删除成功!'
      //     });
      //   }).catch(() => {
      //     this.$message({
      //       type: 'info',
      //       message: '已取消删除'
      //     });
      //   });
      // }
    }
  }
</script>

<style scoped>
  .chartContainer{
    padding: 15px;
    height: 100%;
    clear: both;
    overflow: inherit;
  }
</style>
