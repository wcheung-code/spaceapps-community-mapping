import { Visual } from "./Visual.js";
export class Visuals {

	#visuals = [];

	constructor() {}

	initVisuals(scene) {
		for(let i = 0; i < 10; i++) {
			console.log('creating visual', i);
			
			if(this.#visuals.find(visual => visual.getId() === i)) return;

			const visual = new Visual(i);
			this.#visuals.push(visual);

			visual.initVisual(new BABYLON.Vector3(this.getRandomInt(-500, 500), 5, this.getRandomInt(-500, 500)), 30 + (i * 10), scene);
		}

		setInterval(() => {
			this.#visuals.forEach(visual => {
				visual.setHeight(this.getRandomInt(1, 50));
			});
		}, 4000);
	}

	renderVisuals() {
		this.#visuals.forEach(visual => visual.animate());
	}

	getRandomInt(min, max) {
		min = Math.ceil(min);
		max = Math.floor(max);
		return Math.floor(Math.random() * (max - min + 1)) + min;
	}
}