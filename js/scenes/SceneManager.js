export class SceneManager {
	
	#scenes = [];
	#activeScene;

	constructor() {}

	addScene(scene) {
		this.#scenes.push(scene)
	}

	activateScene(i) {
		this.#activeScene?.deactivate();
		this.#activeScene = this.#scenes[i];
		
		this.#scenes[i].activate();
	}

	getActiveScene() {
		return this.#activeScene;
	}
}

export class Scene {

	#scene;
	#canvas;
	#camera;

	#zoomEvent;
	#currentZoomIndex = 12;

	constructor(engine, canvas, options) {
		this.#scene = new BABYLON.Scene(engine);
		this.#canvas = canvas;
		console.log(options);
		options ??= { upperRadiusLimit: 700, lowerRadiusLimit: 60 };

		this.#camera = new BABYLON.ArcRotateCamera("Camera", -Math.PI / 2, Math.PI / 3, 700, new BABYLON.Vector3(0, 0, 0), this.#scene);
		// Positions the camera overwriting alpha, beta, radius
		// camera.setPosition(new BABYLON.Vector3(0, 500, 0));

		this.#camera.useBouncingBehavior = true;
		this.#camera.upperRadiusLimit = options.upperRadiusLimit;
		this.#camera.lowerRadiusLimit = options.lowerRadiusLimit;
		this.#camera.lowerBetaLimit = 0;
		this.#camera.upperBetaLimit = Math.PI / 2.1;
		this.#camera.radius = options.upperRadiusLimit
		// This attaches the camera to the canvas
		this.#camera.attachControl(this.#canvas, true);

		this.#listenForEvents();
	}

	#listenForEvents() {
		window.addEventListener("zoom", e => {
			const difference = (this.#camera.upperRadiusLimit - this.#camera.lowerRadiusLimit) / 12;
			this.#camera.radius -= e.detail * difference;
		});

		this.#zoomEvent = e => {
			const twelfth = (this.#camera.upperRadiusLimit - this.#camera.lowerRadiusLimit) / 12;
			const divisionIndex = Math.floor(this.#camera.radius/twelfth);
			if(divisionIndex !== this.#currentZoomIndex) {
				const difference = this.#currentZoomIndex < divisionIndex ? 1 : 11;
				this.#currentZoomIndex = divisionIndex;

				window.dispatchEvent(new CustomEvent("zoom-by-sliding", { bubbles: true, detail: difference }));
			}
		}
	}

	activate() {
		this.#scene.attachControl();

		document.body.addEventListener("mousewheel", this.#zoomEvent);
	}

	deactivate() {
		this.#scene.detachControl();
		document.body.removeEventListener("mousewheel", this.#zoomEvent)
	}

	getScene() {
		return this.#scene;
	}

	render() {
		this.#scene.render();
	}
}