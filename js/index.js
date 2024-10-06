import { SceneManager } from "./scenes/SceneManager.js";
import { IrelandScene } from "./scenes/IrelandScene.js";
import { DublinScene } from "./scenes/DublinScene.js";
import { Controls } from "./Controls.js";

window.origin = window.location.href.includes("https://alexnuzum.com/") ? "https://alexnuzum.com/spaceapps-community-mapping/" : window.location.origin;

const canvas = document.getElementById("canvas");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const engine = new BABYLON.Engine(canvas, true); // Generate the BABYLON 3D engine

let sceneManager;

const createScene = function () {
	sceneManager = new SceneManager();
	sceneManager.addScene(new IrelandScene(engine, canvas, { upperRadiusLimit: 2500, lowerRadiusLimit: 60 }))
	sceneManager.addScene(new DublinScene(engine, canvas))
	sceneManager.activateScene(0);

	new Controls().initControls();
}

let currentScene = 0;

document.querySelector("#switch-maps").addEventListener("click", () => {
	currentScene = currentScene === 0 ? 1 : 0;
	canvas.style.animation = 'none';
	void canvas.offsetWidth;
	canvas.style.animation = null;
	canvas.classList.toggle("scene-switcher")
	sceneManager.activateScene(currentScene);
});

window.addEventListener("resize", e => engine.resize)

const scene = createScene(); //Call the createScene function

// Register a render loop to repeatedly render the scene
engine.runRenderLoop(function () {
	if (!sceneManager.getActiveScene()) return;
	sceneManager.getActiveScene().render();
});