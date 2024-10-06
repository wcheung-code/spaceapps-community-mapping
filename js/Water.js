export class Water {
	
	constructor() {}

	initWater(scene, skybox, dimensions) {

		var water = new BABYLON.WaterMaterial("water", scene, new BABYLON.Vector2(10000, 10000));
		water.backFaceCulling = true;
		water.bumpTexture = new BABYLON.Texture(window.origin + "/assets/water.png", scene);
		water.windForce = -1;
		water.waveHeight = 0.1;
		water.bumpHeight = 0.1;
		water.windDirection = new BABYLON.Vector2(1, 1);
		water.waterColor = new BABYLON.Color3(0, 0, 221 / 255);
		water.colorBlendFactor = 0.0;

		const waterMesh = BABYLON.MeshBuilder.CreateGround("plane", {
			height: dimensions?.x ?? 10000,
			width: dimensions?.z ?? 10000,
			subdivisions: 64
		}, scene, false); //scene is optional and defaults to the current scene

		waterMesh.position.y = 1;

		waterMesh.material = water;

		water.addToRenderList(skybox);
	}
}