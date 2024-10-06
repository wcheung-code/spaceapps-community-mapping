export class Sky {

	#skybox;
	#light;

	constructor() {}

	initSky(scene, dimensions) {

		this.#light = new BABYLON.SpotLight("spotLight", new BABYLON.Vector3(0, 3000, 0), new BABYLON.Vector3(0, -1, 0), Math.PI / 3, 2, scene);

		this.#skybox = BABYLON.MeshBuilder.CreateSphere("sphere",
			{
				diameterX: dimensions?.xyz ?? dimensions?.x ?? 2000,
				diameterY: dimensions?.xyz ?? dimensions?.y ?? 2000,
				diameterZ: dimensions?.xyz ?? dimensions?.z ?? 2000
			}
		);
		this.#skybox.rotation.x = Math.PI / 2;
		var skyboxMaterial = new BABYLON.StandardMaterial("skyBox", scene);
		skyboxMaterial.backFaceCulling = false;
		skyboxMaterial.reflectionTexture = new BABYLON.CubeTexture(window.origin + "/assets/skybox/TropicalSunnyDay", scene);
		skyboxMaterial.diffuseColor = new BABYLON.Color3(0, 0, 0);
		skyboxMaterial.specularColor = new BABYLON.Color3(0, 0, 0);
		skyboxMaterial.disableLighting = true;
		this.#skybox.material = skyboxMaterial;
	}

	getSkybox() {
		return this.#skybox;
	}

	animateLight() {
		if(!this.#light) return;
	}
}