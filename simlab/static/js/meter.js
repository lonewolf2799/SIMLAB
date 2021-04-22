
class meter{
    constructor(id,colors, rad, x, y, quant, range, positiveTerminal, negativeTerminal, type){
        this.x= x;
        this.y= y;
        this.value= quant;
        this.rad= rad;
        this.canvas= document.getElementById(id) 
        this.canvas.style.width="500px"
        this.canvas.style.height="500px"
        this.ctx= this.canvas.getContext('2d')
        this.colors= colors;
        this.range= range;
        this.step = Math.PI/colors.length;
        this.smstep= this.step/colors.length;
        this.pointerAngle = (Math.PI/this.range)*this.value;
        this.type= type;
        if(type=='amm')this.positiveTerminal= positiveTerminal;
        if(type=='amm')this.negativeTerminal= negativeTerminal;
    
    }
    draw(){
        this.ctx.strokeStyle='black';


        this.ctx.clearRect(this.x-this.rad, this.y-this.rad-10,this.rad*2 ,this.rad+25);


        // drawing the meter outercase
        this.ctx.strokeRect(this.x-this.rad, this.y-this.rad-10, 2*this.rad, this.rad+25);

        
        this.ctx.beginPath();
        this.ctx.ellipse(this.x, this.y, this.rad, this.rad, 0, Math.PI, 2*Math.PI);
        this.ctx.stroke();
        

        // creating the wires
        // positive terminal
        if(this.type=='amm'){
        // creating the terminals
        this.ctx.beginPath();
        this.ctx.ellipse(this.x- 3/5*this.rad, this.y+7, 5, 5, 0, 0, 2*Math.PI);
        this.ctx.fill();

        this.ctx.beginPath();
        this.ctx.ellipse(this.x+ 3/5*this.rad, this.y+7, 5, 5, 0, 0, 2*Math.PI);
        this.ctx.fill();   
        this.ctx.beginPath();
        this.ctx.moveTo(this.x- 3/5*this.rad, this.y+7);
        this.ctx.lineTo(this.x- 3/5*this.rad, this.y+this.positiveTerminal);
        this.ctx.strokeStyle= 'red';
        this.ctx.stroke();

        this.ctx.strokeStyle='black';

        this.ctx.beginPath();
        this.ctx.moveTo(this.x+ 3/5*this.rad, this.y+7);
        this.ctx.lineTo(this.x+ 3/5*this.rad, this.y+this.negativeTerminal);
        this.ctx.stroke();
        }


        for(let i =Math.PI, j=0; i<=2*Math.PI && j<this.colors.length;i+=this.step, j++){
            
            this.pointerAngle = (Math.PI/this.range)*this.value;
                this.ctx.beginPath();

                this.ctx.moveTo(this.x,this.y);

                this.ctx.lineTo(this.x-this.rad*Math.cos(i), this.y-this.rad*Math.sin(i))

                this.ctx.ellipse(this.x,this.y,this.rad,this.rad,0,i,i+this.step);

                this.ctx.lineTo(this.x, this.y)

                this.ctx.fillStyle= this.colors[j];

                this.ctx.fill()

                for(let k=i; k<= i+this.step; k+= this.smstep){
                    if(k==i) this.ctx.lineWidth=2;
                    else this.ctx.lineWidth=1
                    this.ctx.beginPath()
                    this.ctx.moveTo(this.x+(4*this.rad/5)*Math.cos(k), this.y+(4*this.rad/5)*Math.sin(k));
                    this.ctx.lineTo(this.x+this.rad*Math.cos(k), this.y+this.rad*Math.sin(k));
                    this.ctx.stroke();
                }
                }
                this.ctx.beginPath()
                this.ctx.moveTo(this.x+(4*this.rad/5), this.y);
                this.ctx.lineWidth=2;
                this.ctx.lineTo(this.x+this.rad, this.y);
                this.ctx.stroke();

                this.ctx.beginPath()
                this.ctx.moveTo(this.x,this.y);
                this.ctx.lineWidth=3
                
                let pointerTipx= this.x-3/5*this.rad*Math.cos(this.pointerAngle)
                let pointerTipy= this.y-3/5*this.rad*Math.sin(this.pointerAngle)

                this.ctx.lineTo(pointerTipx, pointerTipy)
                this.ctx.stroke();

                this.ctx.beginPath();
                this.ctx.moveTo(pointerTipx, pointerTipy)
                let prad= 2/4*this.rad
                let lx= this.x -prad*Math.cos(this.pointerAngle-Math.PI/8)
                let ly= this.y- prad*Math.sin(this.pointerAngle-Math.PI/8)

                let rx= this.x -prad*Math.cos(this.pointerAngle+Math.PI/8)
                let ry= this.y- prad*Math.sin(this.pointerAngle+Math.PI/8)

                this.ctx.lineTo(lx, ly);
                this.ctx.lineTo(pointerTipx- 1/5*this.rad*Math.cos(this.pointerAngle), pointerTipy- 1/5*this.rad*Math.sin(this.pointerAngle))
                this.ctx.lineTo(rx, ry)
                this.ctx.lineTo(pointerTipx, pointerTipy)
                this.ctx.fillStyle='black'
                this.ctx.fill();
            }

}