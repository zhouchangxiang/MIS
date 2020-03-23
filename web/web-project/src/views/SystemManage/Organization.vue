<template>
  <div class="chartContainer">
    <input type="checkbox" v-model="landscape" value="1">
    <TreeChart :json="treeData" :class="{landscape: landscape.length}" @click-node="clickNode" />
  </div>
</template>

<script>
  import TreeChart from '@/views/SystemManage/TreeChart'
  export default {
    name: "Organization",
    components: {
      TreeChart
    },
    data(){
      return {
        landscape: [],
        treeData: {
          id: 0,
          name: "云南启辰思维智能科技有限公司",
          children: [
            {id: 2,name: "产品研发部",
              children: [
                {id: 5,name: "研发-前端"},
                {id: 6,name: "研发-后端"},
                {id: 9,name: "UI设计"},
                {id: 10,name: "产品经理"}
              ]
            },
            {id: 3,name: "销售部",
              children: [
                {id: 7,name: "销售一部"},
                {id: 8,name: "销售二部"}
              ]
            },
            {id: 4,name: "财务部"},
            {id: 9,name: "HR人事"}
          ]
        },
      }
    },
    methods: {
      clickNode: function(node){
        // eslint-disable-next-line
        console.log(node)
      }
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
