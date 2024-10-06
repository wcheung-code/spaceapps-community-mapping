import { Scene } from "./SceneManager.js";
import { Sky } from "../Sky.js";
import { Map } from "../maps/Map.js";
import { Water } from "../Water.js";
import { Visuals } from "../visuals/Visuals.js";

export class DublinScene extends Scene {

	#visuals;

	constructor() {
		super();
		this.#init();
	}

	#init() {
		const sky = new Sky();
		sky.initSky(this.getScene(), { y: 1454 });

		new Map().initMap(this.getScene(), 'assets/heightmap.png', "assets/dublinmap.png", 2056, 1454, 2000, 5);

		new Water().initWater(this.getScene(), sky.getSkybox(), { x: 2048, z: 2048 });

		this.#visuals = new Visuals();

		this.#visuals.initVisuals(this.getScene());
	}

	render() {
		super.render();
		this.#visuals.renderVisuals();
	}
}