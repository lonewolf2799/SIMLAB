let intervalColors= ['#66cc66', '#93b75f', '#E7E658' , '#579575', '#cc6666']

let canvas= createCanvas(1000, 700);
canvas.id='pid'

let parent= document.getElementById('diodeCanvasParent')
parent.appendChild(canvas);


canvas.style.position='absolute'
canvas.style.left=0;
let ctx= canvas.getContext('2d');

let cktImage= new Image();
cktImage.src= '/static/images/diodefrw.png'
cktImage.onload = function(){
    ctx.drawImage(cktImage, 100, 100);
}

/////////////////////////parameters

let r= document.getElementById('R');
let v= document.getElementById('V');
let vdio= document.getElementById('vd');
let vmax= 7;
let rmin =100;
let currmax= vmax/rmin;
let pointer= vmax/r.value *1000;
let rd=3e-1;
let R= r.value;
let V= v.value;

let aR= new meter( 'pid' ,intervalColors, 30, 300,100, pointer ,currmax, 30, 30,'amm')
let vD= new meter('pid', intervalColors,30, 575,250 ,pointer,1.0 , 30 ,30 )

r.addEventListener('change', ()=>{
    R= r.value;
});
v.addEventListener('change', ()=>{
    V= v.value;
})
let vt= 26e-3;
let vdo=7e-1;

let ir= document.getElementById('amps');
let vf= 6e-1;
let isat=1e-14;


////////////////////////////////meters



function check(){
    if(parseInt(v.value) >7) v.value = '5';
    if(parseInt(r.value) > 2e3) r.value ='2000';
    let id= ((parseFloat(v.value) - vf) / (parseInt(r)+ parseInt(rd))) *1e3;
    let id1= parseFloat(v.value)/parseFloat(R);
    let id1_s= Math.log(id1/isat);
    let vd= vt*id1_s;
    if(v.value<vdo){
        aR.value= 0;
        vD.value= parseFloat(v.value);
        ir.innerHTML ="0 mA";
        vdio.innerHTML = V ? `${V} volts` : "0 volts";
    }else{
        aR.value= id1;
        vD.value =vd;
        ir.innerHTML= aR.value.toPrecision(4)+' mA';
        vdio.innerHTML = `${vd.toPrecision(4)} V`;
    }
    aR.draw();
    vD.draw();
}

setInterval(check, 15);


let tAdder= document.getElementById('add');
let table= document.getElementById('VI_table')
let tableBody= table.getElementsByTagName('tbody')[0];
let currRow= 0;

let data=[]
let label=[]

let nctx= document.getElementById('graph').getContext('2d');

var chart = new Chart(nctx, {
    // The type of chart we want to create
    type: 'line',
    // The data for our dataset
    data: {
        labels: label,
        datasets: [{
            label: 'Current',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 0, 0)',
            data: data,
            fill:false,
        }],
    },

    // Configuration options go here
    options: {
        scales: {
            xAxes: [{
                ticks: {
                    // Include a dollar sign in the ticks
                    callback: function(value, index, values) {
                        return value.toFixed(4)
                    }
                }
            }],
            yAxes: [{
                ticks: {
                    // Include a dollar sign in the ticks
                    callback: function(value, index, values) {
                        return value.toFixed(4);
                    }
                }
            }]
        }
    }
});


tAdder.addEventListener('click', ()=>{
    let row=tableBody.insertRow(currRow);
    let c1= row.insertCell(0);
    let c2= row.insertCell(1);
    let c3= row.insertCell(2);

    c1.innerHTML= currRow++;
    c2.innerHTML= vdio.innerHTML;
    c3.innerHTML= ir.innerHTML;
    data.push(parseFloat(ir.innerHTML));
    label.push(parseFloat(vdio.innerHTML));
})


let clearAll= document.getElementById('clearAll');
clearAll.addEventListener('click',()=>{
    tableBody.innerHTML="";
    currRow=0;
    if(data.length> 0 && label.length>0){
        data.splice(0, data.length);
        label.splice(0, label.length);
        chart.data.datasets[0].data= data;
        chart.data.label= label;
        chart.update();
    }
})




let plot= document.getElementById('plot');
plot.addEventListener('click', ()=>{
    data.sort();
    label.sort();
    chart.data.datasets[0].data= data;
    chart.data.label= label;
    chart.update();
});