export class Map {

	#map;

	constructor() {}

	initMap(scene, heightmap, texture, width, height, subdivisions, maxHeight) {

		this.#map = BABYLON.MeshBuilder.CreateGroundFromHeightMap("gdhm", window.origin + "/" + heightmap, {
			width: width,
			height: height,
			subdivisions: subdivisions,
			maxHeight: maxHeight
		}, scene); //scene is optional and defaults to the current scene
		this.#map.position = new BABYLON.Vector3(0, 0, 20);//0.1
		const groundMaterial = new BABYLON.StandardMaterial("ground");
		groundMaterial.diffuseTexture = new BABYLON.Texture(texture);
		groundMaterial.specularColor = new BABYLON.Color3(0, 0, 0);
		this.#map.material = groundMaterial;
	}

	getMap() {
		return this.#map;
	}
}