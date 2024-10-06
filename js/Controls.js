export class Controls {
	
	#clickingButtons = false;

	constructor() {}

	initControls() {
		document.querySelectorAll("iframe").forEach(iframe => {
			this.#iframeEvents(iframe);
		});
	}
	
	#iframeEvents(iframe) {
		iframe.contentDocument.querySelector(".leaflet-control-zoom-in").addEventListener("click", e => {
			if(this.#clickingButtons) {
				this.#clickingButtons = false;
				return;
			}
			window.dispatchEvent(new CustomEvent("zoom", { bubbles: true, detail: 1 }));
		});

		iframe.contentDocument.querySelector(".leaflet-control-zoom-out").addEventListener("click", e => {
			if(this.#clickingButtons) {
				this.#clickingButtons = false;
				return;
			}
			window.dispatchEvent(new CustomEvent("zoom", { bubbles: true, detail: -1 }));
		});

		window.addEventListener("zoom-by-sliding", e => {
			this.#clickingButtons = true;
			if(e.detail === 1) {
				iframe.contentDocument.querySelector(".leaflet-control-zoom-out").click();
			}else {
				iframe.contentDocument.querySelector(".leaflet-control-zoom-in").click();
			}
		});
	}
}