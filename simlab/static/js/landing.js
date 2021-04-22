const canvas= document.getElementById('landing')
const canvasWidth=800;
const canvasHeight=500;

const context= canvas.getContext('2d');
context.font='24px Georgia'

class Num{
    constructor(){
        this.num= Math.floor(Math.random() * 255);
        this.x= canvasWidth/2;
        this.y= canvasHeight/2;
        this.xdec= -4+Math.random()*9;
        this.ydec= -4+Math.random()*9;
    }

    update(){
        this.x += this.xdec;
        this.y+= this.ydec;
    }

    draw(){
        context.fillStyle= 'white';
        context.fillText(this.num, this.x, this.y, 80);
    }
}
let numarray = [];

for(let i=0; i< 4;++i) numarray.push(new Num());

function animate(){
    console.log(numarray.toLocaleString());
    context.clearRect(0, 0, canvasWidth, canvasHeight);
    for(let i=0; i< 4;++i){
        numarray[i].update();
        numarray[i].draw();
        if(numarray[i].x < 0 || numarray[i].y <0 || numarray[i].x > canvasWidth || numarray[i].y > canvasHeight){
            numarray[i]= new Num();
        }
    }
    requestAnimationFrame(animate);
}
animate();





