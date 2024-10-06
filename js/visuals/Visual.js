export class Visual {

	#id;

	#bar;

	#targetHeight;
	#originalHeight = 0;
	#actualHeight = 0;

	#position;

	constructor(id) {
		this.#id = id;
	}

	initVisual(position, height, scene) {
		this.#targetHeight = height;
		this.#bar = BABYLON.MeshBuilder.CreateBox("box", { size: 10, height: 5, tileSize: 1 }, scene, true);
		this.#bar.position = position;
		this.#position = new BABYLON.Vector3(position.x, position.y, position.z);
	}

	animate() {
		const direction = this.#targetHeight > this.#actualHeight ? 1 : -1;
		if((this.#bar.scaling.y < this.#targetHeight && direction === 1) || (this.#bar.scaling.y > this.#targetHeight && direction === -1)) {
			this.#actualHeight += direction;
			const scalingFactor = this.#actualHeight / this.#bar.getBoundingInfo().boundingBox.extendSize.y * 2;

			this.#bar.scaling.y = scalingFactor;

			this.#bar.position.y = this.#position.y + (this.#actualHeight * 2);
		}
	}

	setHeight(height) {
		this.#targetHeight = height;
		this.#originalHeight = this.#actualHeight;
		// console.log(this.#targetHeight);
	}

	getId() {
		return this.#id;
	}
}