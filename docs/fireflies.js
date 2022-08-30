let n_particles = 100;
let speed = 1;
let scale_speed = 1;
let alpha = 0.2;

class firefly {
    constructor() {
        this.x = Math.random() * window.w;
        this.y = Math.random() * window.h;
        this.s = Math.random() * 2;
        this.ang = Math.random() * 2 * Math.PI;
        this.v = speed;
        this.vs = Math.random() / 600 * scale_speed;
    }
    move() {
        this.x += this.v * Math.cos(this.ang);
        this.y += this.v * Math.sin(this.ang);
        this.ang += Math.random() * 20 * Math.PI / 180 - 10 * Math.PI / 180;
        this.s = (1 + Math.sin(this.vs * performance.now())) * 2.5;
    }
    show() {
        window.c.beginPath();
        window.c.arc(this.x, this.y, this.s, 0, 2 * Math.PI);
        window.c.fillStyle = "rgba(255, 255, 255, " + (1 + Math.sin(this.vs * performance.now())) / 2 * alpha + ")";
        window.c.fill();
    }
}

let f = [];

function draw() {
    if (f.length < n_particles * window.w * window.h / 2000000) {
        for (let j = 0; j < 10; j++) {
            f.push(new firefly());
        }
    }
    for (let i = 0; i < f.length; i++) {
        f[i].move();
        f[i].show();
        if (f[i].x < 0 || f[i].x > window.w || f[i].y < 0 || f[i].y > h) {
            f.splice(i, 1);
        }
    }
}

function resize() {
    window.canvas.height = 0;
    window.canvas.width = 0;
    let body = document.body;
    let html = document.documentElement;
    let height = Math.max( body.scrollHeight, body.offsetHeight, 
        html.clientHeight, html.scrollHeight, html.offsetHeight );
    console.log("document height: " + height);
    window.canvas.width = window.w = document.documentElement.clientWidth;
    window.canvas.height = window.h = height;
    loop();
}

function init() {
    window.canvas = document.getElementById("fireflies");
    window.c = canvas.getContext("2d");
    window.w = (canvas.width = window.innerWidth);
    window.h = (canvas.height = window.innerHeight);
    window.c.fillStyle = "rgba(0,0,0,0)";
    window.c.fillRect(0, 0, window.w, window.h);
    
    window.addEventListener("resize", resize);

    loop();
    setInterval(loop, 1000 / 60);
    resize();
}

window.requestAnimFrame = (function () {
    return (
        window.requestAnimationFrame ||
        window.webkitRequestAnimationFrame ||
        window.mozRequestAnimationFrame ||
        window.oRequestAnimationFrame ||
        window.msRequestAnimationFrame ||
        function (callback) {
            window.setTimeout(callback);
        }
    );
});

function loop() {
    window.requestAnimFrame(loop);
    window.c.clearRect(0, 0, window.w, window.h);
    draw();
}

window.onload = init;
