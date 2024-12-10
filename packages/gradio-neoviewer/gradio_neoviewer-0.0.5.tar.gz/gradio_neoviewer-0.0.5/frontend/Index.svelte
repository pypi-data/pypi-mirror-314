<svelte:options accessors={true} />

<script lang="ts">
	import type { Gradio, SelectData } from "@gradio/utils";
	import { tick } from 'svelte';
	import File from "./shared/File.svelte";
	import Markdown from "./shared/Markdown.svelte";
	import { FileData } from "@gradio/client";
	import { Block, BlockLabel } from "@gradio/atoms";
	import * as pdfjsLib from "pdfjs-dist";
	pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";

	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value: null | FileData | FileData[];
	export let index_of_file_to_show: number;
	export let libre_office: boolean;
	export let max_size: number;
	export let max_pages: number;

	export let root: string;
	export let height: string | undefined;

	export let loading_status: LoadingStatus;
	export let container = true;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let gradio: Gradio<{
		change: never;
		error: string;
		clear_status: LoadingStatus;
	}>;

	let file: FileData;
	let pending_upload = false;
	let old_file: null | FileData = null;

	let abortController = new AbortController();
	let blinking: HTMLDivElement;
	let viewer: HTMLDivElement;
	let shouldCancelImage = true;
	let shouldCancelMarkdown = true;
	let shouldCancelHtml = true;
	let shouldCancelPdf = true;

	let previous_file_title:string;
	let next_file_title: string;

	if (navigator.language.startsWith('fr')) {
		previous_file_title = "Fichier précédent";
		next_file_title = "Fichier suivant";
	} else {
		previous_file_title = "Previous file";
		next_file_title = "Next file";
	}


	function file_to_show(value: FileData | FileData[], index_of_file_to_show: number) {
		let file: null | FileData;
		if (Array.isArray(value) && value.length > 0) {
			file = value[index_of_file_to_show];
			} else if (value instanceof FileData) {
			file = value;
		}
		return file;
	}

	function addUrl(file: FileData, root: string) {
			if (file) {
				file.url = root + "/gradio_api/file=" + file.path
			}
			return file
		}

	$: if (value && (!Array.isArray(value) || value.length > 0)) {
		// console.log("Value changed");
		if (value && JSON.stringify(file_to_show(value, index_of_file_to_show)) !== JSON.stringify(old_file)) {
			abortController.abort();
			shouldCancelHtml = true;
			shouldCancelImage = true;
			shouldCancelMarkdown = true;
			shouldCancelPdf = true;
			gradio.dispatch("change");
			old_file = file_to_show(value, index_of_file_to_show);
			file = addUrl(file_to_show(value, index_of_file_to_show), root);
			console.log(file.url);
			if (file.size > max_size) {
				console.log("Fichier trop lourd");
				showError('size');
			} else	if (file.path.endsWith('pdf') || libre_office && msFormats.some(ext => file.path.endsWith(ext))) {
				console.log("PDF ou MS");
				showPdf(file);
			} else if (htmlFormats.some(ext => file.path.endsWith(ext))) {
				console.log("HTML");
				if (file.size > max_size/5) {
					console.log("HTML trop lourd");
					showError('size');
				} else {
					showHtml(file);
				}
			} else if (imageFormats.some(ext => file.path.endsWith(ext))) {
				console.log("Image");
				showImage(file);
			} else if (markdownFormats.some(ext => file.path.endsWith(ext)) || codeFormats.some(ext => file.path.endsWith(ext))) {
				console.log("Markdown");
				if (file.size > max_size/5) {
					console.log("Markdown trop lourd");
					showError('size');
				} else {
					showMarkdown(file);
				}
			} else {
				console.log("Autre");
				showError('format');
			}
		}
	} else {
		showEmpty();
		old_file = null;
	}

	const htmlFormats = ['.html', '.svg'];
	const imageFormats = ['.png', '.jpg', '.jpeg'];
	const markdownFormats = ['.md', '.txt', '.csv', '.srt'];
	const msFormats = ['.docx', '.pptx', '.xlsx', '.doc', '.ppt', '.xls'];
	const codeFormats = ['.py', '.js', '.css', '.json', '.yaml', '.yml', '.xml', '.sh', '.bash', '.log', '.ts', '.tsx', '.js', '.jsx', '.cpp'];

	async function showEmpty() {
		abortController.abort();
		abortController = new AbortController();
		await tick();
		blinking.style.display = 'none';
		viewer.innerHTML = '';
	}

	async function showError(error: string) {
		console.log("Show error");
		abortController = new AbortController();
		await tick(); // Attend la fin du rendu
		blinking.style.display = 'none';
		let errorMessage: string;
		if (error == 'format') {
			errorMessage = navigator.language.startsWith('fr')
			? 'Format non pris en charge'
			: 'Unsupported format';
		} else if (error == 'size') {
			errorMessage = navigator.language.startsWith('fr')
			? 'Fichier trop volumineux pour être affiché'
			: 'File too heavy to be displayed';
		}
		viewer.innerHTML = `<div class="error-message">${errorMessage}</div>`;
	}

	async function showPdf(file: FileData) {
		shouldCancelPdf = false;
		console.log("Get doc en cours");
		abortController = new AbortController();
		await tick(); // Attend la fin du rendu
		viewer.innerHTML = '';
		blinking.style.display = 'block';
		const loadingTask = pdfjsLib.getDocument(file.url);
		const pdfDoc = await loadingTask.promise;
		console.log('PDF loaded');

		if (pdfDoc.numPages > max_pages) {
			showError('size');
			return;
		}
		
		const fragment = document.createDocumentFragment(); // Crée un fragment de document

		const renderPage = async (pageNum: number) => {
			if (shouldCancelPdf) {
				console.log('Cancelled');
				return;
			}
			const page = await pdfDoc.getPage(pageNum);
			console.log(`Page ${pageNum} loaded`);
			const scale = 1.5;
			const viewport = page.getViewport({ scale: scale });

			// Création d'un nouveau canevas pour chaque page
			const canvas = document.createElement('canvas');
			canvas.height = viewport.height;
			canvas.width = viewport.width;
			fragment.appendChild(canvas); // Ajoute le canevas au fragment

			const context = canvas.getContext('2d');

			// Rendu de la page
			const renderContext = {
				canvasContext: context,
				viewport: viewport
			};
			page.render(renderContext);
			console.log(`Page ${pageNum} rendered`);
		}

		// Parallélisation du chargement et du rendu des pages
		const renderPromises = [];
		for (let pageNum = 1; pageNum <= pdfDoc.numPages; pageNum++) {
			if (shouldCancelPdf) {
				console.log('Cancelled');
				break;
			}
			renderPromises.push(renderPage(pageNum));
		}
		await Promise.all(renderPromises);
		if (!shouldCancelPdf) {
			viewer.appendChild(fragment); // Ajoute le fragment au conteneur
		} else {
			console.log('append viewer with pdf cancelled');
		}
		shouldCancelPdf = true;
		blinking.style.display = 'none';
	}

	async function showHtml(file: FileData) {
		shouldCancelHtml = false;
		abortController = new AbortController();
		await tick(); // Attend la fin du rendu
		viewer.innerHTML = ''; // Vide le conteneur
		blinking.style.display = 'block';
		try {
			const response = await fetch(file.url, {signal: abortController.signal});
			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}
			const htmlContent = await response.text();

			const iframe = document.createElement('iframe');
			iframe.style.width = '100%';
			iframe.style.height = '100%';
			iframe.srcdoc = htmlContent; // Utilise le contenu HTML comme source de l'iframe

			if (!shouldCancelHtml) {
				viewer.appendChild(iframe);
			} else {
				console.log('append viewer with iframe cancelled');
			}
		} catch (error) {
			console.error('Error fetching HTML content:', error);
		}
		shouldCancelHtml = true;
		blinking.style.display = 'none';
	}

	async function showImage(file: FileData) {
		console.log(viewer.innerHTML)
		shouldCancelImage = false;
		abortController = new AbortController();
		await tick(); // Attend la fin du rendu
		viewer.innerHTML = ''; // Vide le conteneur
		blinking.style.display = 'block';

		try {
			const response = await fetch(file.url, {signal: abortController.signal});
			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}
			const blob = await response.blob();
			const imageUrl = URL.createObjectURL(blob);

			const img = document.createElement('img');
			img.style.width = '100%';
			img.src = imageUrl; // Utilise l'URL de l'image comme source de l'élément img
			
			if (!shouldCancelImage) {
				viewer.appendChild(img);
			} else {
				console.log('append viewer with image cancelled');
			}
		} catch (error) {
			console.error('Error fetching image content:', error);
		}
		shouldCancelImage = true;
		blinking.style.display = 'none';
	}

	async function showMarkdown(file: FileData) {
		shouldCancelMarkdown = false;
		abortController = new AbortController();
		await tick(); // Attend la fin du rendu
		viewer.innerHTML = ''; // Vide le conteneur
		blinking.style.display = 'block';

		try {
			const response = await fetch(file.url, {signal: abortController.signal});
			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}
			let markdownContent = await response.text();

			// Vérifie l'extension du fichier
			const extensionMatch = file.path.match(/\.(\w+)$/);
			if (extensionMatch) {
				const extension = extensionMatch[1];
			console.log(extension);
			if (codeFormats.includes(`.${extension}`)) {
				markdownContent = `\`\`\`${extension}\n${markdownContent}\n\`\`\``;
			}
		}
			// Crée dynamiquement un composant Svelte
			if (!shouldCancelMarkdown) {
				new Markdown({
					target: viewer,
					props: {
						value: markdownContent,
					}
				});
			} else {
				console.log('append viewer with markdown cancelled');
			}
		} catch (error) {
			console.error('Error fetching Markdown content:', error);
		}
		shouldCancelMarkdown = true;
		blinking.style.display = 'none';
}


	async function next_file() {
		await tick(); // Attend la fin du rendu
		blinking.style.display = 'none';
		if (Array.isArray(value) && value.length > 1) {
			index_of_file_to_show = (index_of_file_to_show + 1) % value.length;
		}
 	}

	async function previous_file() {
		await tick(); // Attend la fin du rendu
		blinking.style.display = 'none';
		index_of_file_to_show = (index_of_file_to_show - 1 + value.length) % value.length;
 	}

</script>


<Block {visible} {elem_id} {elem_classes} {container} {scale} {min_width} {height}>
	{#if loading_status}
		<StatusTracker
			autoscroll={gradio.autoscroll}
			i18n={gradio.i18n}
			{...loading_status}
			on:clear_status={() => gradio.dispatch("clear_status", loading_status)}
		/>
	{/if}
    <BlockLabel
        show_label={false}
        Icon={File}
        float={true}
        label={null}
    />
		<div class="viewer-container">
			<div bind:this={blinking} class="viewer-blinker" style="display: none">
				<span>·</span><span>·</span><span>·</span>
			</div>
			<div bind:this={viewer} class="viewer"></div>
			<div class="button-row">
				{#if Array.isArray(value) && value.length > 1}
					<button class="left-arrow" on:click={previous_file} title={previous_file_title}>
						<svg xmlns="http://www.w3.org/2000/svg" width="80%" height="80%" viewBox="0 0 24 24">
							<path d="M15 6L8 12L15 18" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
						</svg>
					</button>
				{/if}
				{#if Array.isArray(value) && value.length > 0}
					<span class="file-name">&nbsp;&nbsp;&nbsp;{value[index_of_file_to_show].orig_name}&nbsp;&nbsp;&nbsp;</span>
				{:else if typeof value === 'string'}
					<span class="file-name">&nbsp;&nbsp;&nbsp;{value.orig_name}&nbsp;&nbsp;&nbsp;</span>
				{/if}
				{#if Array.isArray(value) && value.length > 1}
					<button class="right-arrow" on:click={next_file} title={next_file_title}>
						<svg xmlns="http://www.w3.org/2000/svg" width="80%" height="80%" viewBox="0 0 24 24">
							<path d="M9 6L16 12L9 18" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
						</svg>
					</button>
				{/if}
			</div>
		</div>
	<style>
		:root {
			--neo-blue: rgb(0, 162, 223);
			--neo-white: rgb(255, 255, 255);
			--neo-black: rgb(5, 5, 5);
			--neo-dark-grey: rgb(64, 64, 64);
            --neo-light-grey: rgb(212,212,212);
		}
		.viewer-container {
			position: relative;
			overflow: hidden;
			height: 100%;
			width: 100%;
			display: flex;
			flex-direction: column;
		}
		.viewer {
			display: flex;
			flex-direction: column;
			width: 100%;
			height: 100%;
			overflow: auto;
		}
		.error-message {
			position: absolute;
			top: 50%;
			left: 50%;
			transform: translate(-50%, -50%);
			text-align: center;
		}
		.viewer canvas {
			margin: .1vh 0;
		}
		.button-row {
			display: flex;
			flex-direction: row;
			width: 100%;
			justify-content: center;
			align-items: center;
		}
		.file-name {
			max-width: 90%;
			overflow: hidden;
			text-overflow: ellipsis;
			white-space: nowrap;
		}
		.viewer-blinker {
			position: absolute;
			top: 50%;
			left: 50%;
			transform: translate(-50%, -50%);
			color: var(--neo-blue);
			animation: blinker 1.5s cubic-bezier(.5, 0, 1, 1) infinite alternate;
			font-size: 3em;
		}
		.viewer-blinker span {
			opacity: 0;
			animation-name: blinker;
			animation-duration: 1.5s;
			animation-timing-function: cubic-bezier(.5, 0, 1, 1);
			animation-iteration-count: infinite;
		}
		.viewer-blinker span:nth-child(1) {
			animation-delay: 0s;
		}
		.viewer-blinker span:nth-child(2) {
			animation-delay: .5s; /* Délai pour le deuxième point */
		}
		.viewer-blinker span:nth-child(3) {
			animation-delay: 1s; /* Délai pour le troisième point */
		}
		@keyframes blinker {  
			0%, 100% { opacity: 0; }
			50% { opacity: 1; }
		}
		.left-arrow, .right-arrow {
			width: 18px;
			height: 18px;
			cursor: pointer;
			border-radius: 50px;
			fill: none;
			background-color:var(--button-secondary-background-fill) !important;
			display: flex;
			flex-shrink: 0;
			justify-content: center;
			align-items: center;
			stroke:var(--button-secondary-text-color);
			z-index: var(--layer-1);
		}
	</style>
</Block>
