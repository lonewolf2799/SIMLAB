
import * as THREE from '../node_modules/three/build/three.module.js'
import { OrbitControls } from '../node_modules/three/examples/jsm/controls/OrbitControls.js'

// Canvas
const canvas = document.querySelector('canvas.webgl')

// Scene
const scene = new THREE.Scene()

/**
 * Base
 */
const textureLoader = new THREE.TextureLoader()
const fontLoader= new THREE.FontLoader()
fontLoader.load(
  '../static/fonts/helvetiker_regular.typeface.json',(font)=>{
      const textBufferGeometry = new THREE.TextBufferGeometry(
          'SIMLAB',{
              font,
              size: 0.5, 
              height :0.2,
              curveSegments :12,
              bevelEnabled : true,
              bevelThickness : 0.003,
              bevelSize : 0.002,
              bevelOffSet :0,
              bevelSegments :10
          }
      );
      
     
      textBufferGeometry.center()

      textBufferGeometry.computeBoundingBox()


      const text = new THREE.Mesh(textBufferGeometry,material);
      
      scene.add(text);
  }
)



// textures 
const particleTexture = textureLoader.load('../static/2.png');



//lighting

const ambientLight = new THREE.AmbientLight('#b9d9ff' , 1);

const moonLight = new THREE.DirectionalLight(0xb9d9ff, 0.12);
moonLight.position.set(4, 5, -2)




scene.add(ambientLight)
scene.add(moonLight)


//Material
const material = new THREE.MeshStandardMaterial()
material.roughness = 0.4;
const planematerial = new THREE.MeshStandardMaterial({side : THREE.DoubleSide})
planematerial.roughness = 0.4;

//Objects


const cube =  new THREE.Mesh(new THREE.BoxBufferGeometry(0.5, 0.5, 0.5 ,16, 16, 16), new THREE.MeshBasicMaterial());
// scene.add(cube)


const particlesGeometry = new THREE.BufferGeometry();
let cnt =2000
const positions = new Float32Array(cnt * 3);
const colors = new Float32Array(cnt *3);

for(let i=0; i< cnt*3; ++i){
    positions[i]= 10*(Math.random() - 0.5) ;
    colors[i]= Math.random() ;
}
particlesGeometry.setAttribute(
    'position' , new THREE.BufferAttribute(positions , 3)
)
particlesGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

const particlesMaterial = new THREE.PointsMaterial({
    size: 0.1 , sizeAttenuation : true, alphaMap: particleTexture, transparent: true
})
particlesMaterial.depthWrite = false;
particlesMaterial.blending = THREE.AdditiveBlending;
particlesMaterial.vertexColors = true;

const particles = new THREE.Points(particlesGeometry , particlesMaterial);
scene.add(particles)


const sizes = {
    width: window.innerWidth,
    height: window.innerHeight
}

window.addEventListener('resize', () =>
{
    // Update sizes
    sizes.width = window.innerWidth
    sizes.height = window.innerHeight

    // Update camera
    camera.aspect = sizes.width / sizes.height
    camera.updateProjectionMatrix()

    // Update renderer
    renderer.setSize(sizes.width, sizes.height)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
})

/**
 * Camera
 */
// Base camera
const camera = new THREE.PerspectiveCamera(75, sizes.width / sizes.height, 0.1, 100)
camera.position.z = 3


scene.add(camera)

// Controls
const controls = new OrbitControls(camera, canvas)
controls.enableDamping = true

/**
 * Renderer
 */
const renderer = new THREE.WebGLRenderer({
    canvas: canvas
})
renderer.setSize(sizes.width, sizes.height)
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))


/* * Animate
 */
const clock = new THREE.Clock()

const tick = () =>
{
    const elapsedTime = clock.getElapsedTime()

    for(let i=0; i<cnt ;++i){
        let i3= 3*i;
        let x =particlesGeometry.attributes.position.array[i3]
        particlesGeometry.attributes.position.array[i3+1] =Math.sin(elapsedTime+x);
    }

    particlesGeometry.attributes.position.needsUpdate = true;
    // Update controls
    controls.update()

    // Render
    renderer.render(scene, camera)

    // Call tick again on the next frame
    window.requestAnimationFrame(tick)
}

tick()