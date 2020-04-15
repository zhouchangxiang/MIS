const mutations={
    Choosedate:(state,choosedate)=>{
        state.choosedate=choosedate
    },
    Choosekind:(state,choosekind)=>{
        state.choosekind=choosekind
    },  
    Chooseworkplace:(state,workplace)=>{
    state.workplace=workplace
    },
    Sbnumbers:(state,value)=>{
        state.sbnumber=value
    },
    NumBox:(state,value)=>{
        state.numberbox=[]
        state.numberbox.push(value)
    }
}
export default mutations