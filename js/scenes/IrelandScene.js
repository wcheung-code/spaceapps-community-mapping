import { Scene } from "./SceneManager.js";
import { Sky } from "../Sky.js";
import { Map } from "../maps/Map.js";
import { Water } from "../Water.js";
import { Visuals } from "../visuals/Visuals.js";

export class IrelandScene extends Scene {

	#visuals;

	constructor(engine, canvas, options) {
		super(engine, canvas, options);
		this.#init();
	}

	#init() {
		const sky = new Sky();
		sky.initSky(this.getScene(), {xyz: 10000});

		new Map().initMap(this.getScene(), 'assets/ireland-heightmap.png', "assets/ireland-map.png", 1412, 1854, 2000, 10);

		new Water().initWater(this.getScene(), sky.getSkybox());

		this.#visuals = new Visuals();

		// this.#visuals.initVisuals(this.getScene());
	}

	render() {
		super.render();
		this.#visuals.renderVisuals();
	}
}