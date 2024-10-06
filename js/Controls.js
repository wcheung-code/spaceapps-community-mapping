export class Controls {
	
	#clickingButtons = false;

	constructor() {}

	initControls() {
		console.log('hello');
		document.querySelectorAll("iframe").forEach(iframe => {
			const timer = setInterval(() => {
				// console.log('searching', iframe.contentDocument.querySelector("iframe"));
				const query = iframe.contentDocument?.querySelector(".bk-Row")?.shadowRoot?.querySelector(".bk-Div")?.shadowRoot;
				if (query?.querySelector("iframe")) {
					clearInterval(timer);
					console.log('found');

					// const bk = query?.querySelector(".bk-clearfix");
					// bk.style.width = "100%";
					// bk.style.height = "100%";

					// query?.querySelector("iframe").style.width = "100%";
					// query?.querySelector("iframe").style.height = "100%";

					this.#iframeEvents(query?.querySelector("iframe"));
				}
			});
		});
	}
	
	#iframeEvents(iframe) {

		const zoomIn = setInterval(() => {
			const query = iframe.contentDocument.querySelector(".leaflet-control-zoom-in");
			if(query) {
				query.addEventListener("click", e => {
					console.log('zooming in');
		
					if (this.#clickingButtons) {
						this.#clickingButtons = false;
						return;
					}
					window.dispatchEvent(new CustomEvent("zoom", { bubbles: true, detail: 1 }));
				});

				clearInterval(zoomIn);
			}
		});

		const zoomOut = setInterval(() => {
			console.log('waiting');
			const query = iframe.contentDocument.querySelector(".leaflet-control-zoom-out");
			if (query) {
				query.addEventListener("click", e => {
					if (this.#clickingButtons) {
						this.#clickingButtons = false;
						return;
					}
					window.dispatchEvent(new CustomEvent("zoom", { bubbles: true, detail: -1 }));
				});
				clearInterval(zoomOut);
			}
		});

		window.addEventListener("zoom-by-sliding", e => {
			this.#clickingButtons = true;
			const query = iframe
				.contentDocument
				?.querySelector(".bk-Row")
				?.shadowRoot
				?.querySelector(".bk-Div")
				?.shadowRoot
				?.iframe
				?.contentDocument
				?.querySelector("iframe")
				?.contentDocument;
				
				if(e.detail === 1) {
				console.log("detected zoom out!");
				query?.querySelector(".leaflet-control-zoom-out").click();
			}else {
				console.log("detected zoom in!");
				query?.querySelector(".leaflet-control-zoom-in").click();
			}
		});
	}
}