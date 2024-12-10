<script lang="ts">
	import {
		beforeUpdate,
		afterUpdate,
		createEventDispatcher,
		tick
	} from "svelte";
	import { text_area_resize, resize } from "../shared/utils";
	import { BlockTitle } from "@gradio/atoms";
	import { Upload } from "@gradio/upload";
	import type { FileData, Client } from "@gradio/client";
	import type { SelectData } from "@gradio/utils";

	export let value: { text: string; files: FileData[] } = {
		text: "",
		files: []
	};

	import useRealTime from "./hooks/useRealtime";
	import useAudioRecorder from "./hooks/useAudioRecorder";
    import { 
		play as playAudio, 
		reset as resetAudioPlayer, 
		stop as stopAudioPlayer 
	} from "./hooks/useAudioPlayer";
	import ToolResult from "./hooks/types";

    // Utilise une variable réactive pour gérer l'état
    let isRecording = false;

	export let value_is_output = false;
	export let lines = 1;
	export let placeholder = "Type here...";
	export let disabled = false;
	export let label: string;
	export let interactive: boolean;
	export let loading_message: string;
	export let info: string | undefined = undefined;
	export let show_label = true;
	export let container = true;
	export let max_lines: number;
	export let upload_btn: string | boolean | null = null;
	export let submit_btn: string | boolean | null = null;
	export let stop_btn: string | boolean | null = null;
	export let rtl = false;
	export let autofocus = false;
	export let text_align: "left" | "right" | undefined = undefined;
	export let autoscroll = true;
	export let root: string;
	export let file_types: string[] | null = null;
	export let max_file_size: number | null = null;
	export let upload: Client["upload"];
	export let stream_handler: Client["stream"];
	export let file_count: "single" | "multiple" | "directory" = "multiple";
	export let audio_btn: boolean = false;
	export let stop_audio_btn: boolean = false;

	let upload_component: Upload;
	let hidden_upload: HTMLInputElement;
	let el: HTMLTextAreaElement | HTMLInputElement;
	let can_scroll: boolean;
	let previous_scroll_top = 0;
	let user_has_scrolled_up = false;
	export let dragging = false;
	let uploading = false;
	let oldValue = value.text;
	let saved_message: string;
	let retrieve_saved_message: boolean = false;
	$: dispatch("drag", dragging);
	var onToggleListening = async () => {};
	var onEndingListening = async () => {};
	let already_defined = false;

	$: if (audio_btn && !already_defined) {
		already_defined = audio_btn;
		const { startSession, addUserAudio, inputAudioBufferClear } = useRealTime({
			onWebSocketOpen: () => console.log("WebSocket connection opened"),
			onWebSocketClose: () => console.log("WebSocket connection closed"),
			onWebSocketError: event => console.error("WebSocket error:", event),
			onReceivedError: message => console.error("error", message),
			onReceivedResponseAudioDelta: message => {
				if (typeof isRecording !== 'undefined' && isRecording) {
					playAudio(message.delta);
				} else {
					console.warn("isRecording is not defined or false");
				}
			},
			onReceivedInputAudioBufferSpeechStarted: () => {
				stopAudioPlayer();
			},
			onReceivedExtensionMiddleTierToolResponse: message => {
				try {
					const result: ToolResult = JSON.parse(message.tool_result);
					// Utilise `result` ici si nécessaire
				} catch (e) {
					console.error("Failed to parse tool_result:", e);
				}
			},
		});

		const { start: startAudioRecording, stop: stopAudioRecording } = useAudioRecorder({ onAudioRecorded: addUserAudio });

		onToggleListening = async () => {
			if (!isRecording) {
				console.log("Launching Neo Audio")
				startSession();
				await startAudioRecording();
				resetAudioPlayer();
				isRecording = true;
			}
		};
		onEndingListening = async () => {
			if (isRecording) {
				console.log("Ending Neo audio recording")
				await stopAudioRecording();
				stopAudioPlayer();
				inputAudioBufferClear();
				isRecording = false;
			}
		};
	}

	let full_container: HTMLDivElement;

	$: if (oldValue !== value.text && !uploading && !retrieve_saved_message) {
		// console.log("oldValue", oldValue)
		oldValue = value.text;
		dispatch("change", value);
		// console.log("value.text", value.text)
	}

	$: if (uploading) {
		console.log("uploading")
	}
	$: if (disabled) {
		console.log("disabled")
	}

	$: if (value === null) value = { text: "", files: [] };
	$: value, el && lines !== max_lines && resize(el, lines, max_lines, uploading);
	$: disabled = !interactive || uploading;
	$: if (uploading && !retrieve_saved_message) {
		saved_message = value.text;
		retrieve_saved_message = true;
		value.text = loading_message;
		console.log("value.text uploading", value.text);
	} else if (!uploading && retrieve_saved_message) {
		value.text = saved_message;
		retrieve_saved_message = false;
		console.log("value.text end of uploading", value.text);
	}

	let upload_btn_title:string;
	let submit_btn_title: string;
	let stop_btn_title:string;
	let audio_btn_title:string;
	let stop_audio_btn_title: string;

	if (navigator.language.startsWith('fr')) {
		upload_btn_title = "Ajouter un fichier";
		submit_btn_title = "Poser une question";
		stop_btn_title = "Arrêter";
		audio_btn_title = "Activer l'audio";
		stop_audio_btn_title = "Arrêter l'audio"
	} else {
		upload_btn_title = "Add a file";
		submit_btn_title = "Ask a question";
		stop_btn_title = "Stop";
		audio_btn_title = "Launch audio";
		stop_audio_btn_title = "Stop audio"

	}

	const dispatch = createEventDispatcher<{
		change: typeof value;
		submit: undefined;
		stop: undefined;
		stream: undefined;
		blur: undefined;
		select: SelectData;
		input: undefined;
		focus: undefined;
		drag: boolean;
		upload: FileData[] | FileData;
		clear: undefined;
		load: FileData[] | FileData;
		error: string;
	}>();

	beforeUpdate(() => {
		can_scroll = el && el.offsetHeight + el.scrollTop > el.scrollHeight - 100;
	});

	const scroll = (): void => {
		if (can_scroll && autoscroll && !user_has_scrolled_up) {
			el.scrollTo(0, el.scrollHeight);
		}
	};

	async function handle_change(): Promise<void> {
		dispatch("change", value);
		if (!value_is_output) {
			dispatch("input");
		}
	}

	afterUpdate(() => {
		if (autofocus && el !== null) {
			el.focus();
		}
		if (can_scroll && autoscroll) {
			scroll();
		}
		value_is_output = false;
	});

	function handle_select(event: Event): void {
		const target: HTMLTextAreaElement | HTMLInputElement = event.target as
			| HTMLTextAreaElement
			| HTMLInputElement;
		const text = target.value;
		const index: [number, number] = [
			target.selectionStart as number,
			target.selectionEnd as number
		];
		dispatch("select", { value: text.substring(...index), index: index });
	}

	async function handle_keypress(e: KeyboardEvent): Promise<void> {
		await tick();
		if (e.key === "Enter" && e.shiftKey && lines > 1) {
			e.preventDefault();
			dispatch("submit");
		} else if (
			e.key === "Enter" &&
			!e.shiftKey &&
			lines === 1 &&
			max_lines >= 1
		) {
			e.preventDefault();
			dispatch("submit");
		}
	}

	function handle_scroll(event: Event): void {
		const target = event.target as HTMLElement;
		const current_scroll_top = target.scrollTop;
		if (current_scroll_top < previous_scroll_top) {
			user_has_scrolled_up = true;
		}
		previous_scroll_top = current_scroll_top;

		const max_scroll_top = target.scrollHeight - target.clientHeight;
		const user_has_scrolled_to_bottom = current_scroll_top >= max_scroll_top;
		if (user_has_scrolled_to_bottom) {
			user_has_scrolled_up = false;
		}
	}

	async function handle_upload({
		detail
	}: CustomEvent<FileData | FileData[]>): Promise<void> {
		handle_change();
		if (Array.isArray(detail)) {
			for (let file of detail) {
				value.files.push(file);
			}
			value = value;
		} else {
			value.files.push(detail);
			value = value;
		}
		await tick();
		dispatch("change", value);
		dispatch("upload", detail);
	}

	function handle_upload_click(): void {
		if (hidden_upload) {
			hidden_upload.value = "";
			hidden_upload.click();
		}
	}

	function handle_audio_click(): void {
		onToggleListening();
		dispatch("stream");
	}

	function handle_end_streaming_click(): void {
		onEndingListening();
		dispatch("stream");
	}

	function handle_stop(): void {
		dispatch("stop");
	}

	function handle_submit(): void {
		dispatch("submit");
	}

	function handle_paste(event: ClipboardEvent): void {
		if (!event.clipboardData) return;
		const items = event.clipboardData.items;
		for (let index in items) {
			const item = items[index];
			if (item.type.includes("text/plain")) {
				// avoids retrieving image format of pastes which contain plain/text but also have image data in their clipboardData .
				break;
			}
			if (item.kind === "file" && item.type.includes("image")) {
				const blob = item.getAsFile();
				if (blob) upload_component.load_files([blob]);
			}
		}
	}

	function handle_dragenter(event: DragEvent): void {
		event.preventDefault();
		dragging = true;
	}

	function handle_dragleave(event: DragEvent): void {
		event.preventDefault();
		const rect = full_container.getBoundingClientRect();
		const { clientX, clientY } = event;
		if (
			clientX <= rect.left ||
			clientX >= rect.right ||
			clientY <= rect.top ||
			clientY >= rect.bottom
		) {
			dragging = false;
		}
	}

	function handle_drop(event: DragEvent): void {
		event.preventDefault();
		dragging = false;
		if (event.dataTransfer && event.dataTransfer.files) {
			upload_component.load_files(Array.from(event.dataTransfer.files));
		}
	}
</script>

<div
	class="full-container"
	class:dragging
	bind:this={full_container}
	on:dragenter={handle_dragenter}
	on:dragleave={handle_dragleave}
	on:dragover|preventDefault
	on:drop={handle_drop}
	role="group"
	aria-label="Multimedia input field"
>
	<!-- svelte-ignore a11y-autofocus -->
	<label class:container>
		<BlockTitle {root} {show_label} {info}>{label}</BlockTitle>
		<div class="input-container">
			{#if upload_btn}
				<Upload
					bind:this={upload_component}
					on:load={handle_upload}
					{file_count}
					filetype={file_types}
					{root}
					{max_file_size}
					bind:dragging
					bind:uploading
					show_progress={false}
					disable_click={true}
					bind:hidden_upload
					on:error
					hidden={true}
					{upload}
					{stream_handler}
				></Upload>
				<button
					data-testid="upload-button"
					class="upload-button"
					title={upload_btn_title}
					{disabled}
					on:click={handle_upload_click}>
					{#if upload_btn === true}
						<svg xmlns="http://www.w3.org/2000/svg" width="65%" height="65%" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
							<path d="M12,2L12,22" stroke-width="2"/>
							<path d="M2,12L22,12" stroke-width="2"/>
						</svg>
					{:else}
						{upload_btn}
					{/if}
				</button>
			{/if}
			<textarea
				data-testid="textbox"
				use:text_area_resize={{
					text: value.text,
					lines: lines,
					max_lines: max_lines
				}}
				class="scroll-hide"
				class:no-label={!show_label}
				dir={rtl ? "rtl" : "ltr"}
				bind:value={value.text}
				bind:this={el}
				{placeholder}
				{disabled}
				rows={lines}
				{autofocus}
				on:keypress={handle_keypress}
				on:blur
				on:select={handle_select}
				on:focus
				on:scroll={handle_scroll}
				on:paste={handle_paste}
				style={text_align ? "text-align: " + text_align : ""}
			/>
			{#if audio_btn}
				<button
					class="audio-button"
					class:padded-button={audio_btn !== true}
					title={audio_btn_title}
					{disabled}
					on:click={handle_audio_click}
				>
					{#if audio_btn === true}
						<svg xmlns="http://www.w3.org/2000/svg" width="80%" height="80%" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
							<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"></path>
							<path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
							<line x1="12" x2="12" y1="19" y2="22"></line>
						</svg>
					{:else}
						{audio_btn}
					{/if}
				</button>
			{/if}
			{#if stop_audio_btn}
				<button
					class="stop-audio-button"
					class:padded-button={stop_audio_btn !== true}
					title={stop_audio_btn_title}
					{disabled}
					on:click={handle_end_streaming_click}
				>
					{#if stop_audio_btn === true}
						<svg xmlns="http://www.w3.org/2000/svg" width="80%" height="80%" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
							<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"></path>
							<path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
							<line x1="12" x2="12" y1="19" y2="22"></line>
						</svg>
					{:else}
						{stop_audio_btn}
					{/if}
				</button>
			{/if}
			{#if submit_btn}
				<button
					class="submit-button"
					class:padded-button={submit_btn !== true}
					title={submit_btn_title}
					{disabled}
					on:click={handle_submit}
				>
					{#if submit_btn === true}
						<svg xmlns="http://www.w3.org/2000/svg" width="80%" height="80%" viewBox="0 0 24 24">
							<path d="M12 5V21M12 5L7 10M12 5L17 10" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
						</svg>
					{:else}
						{submit_btn}
					{/if}
				</button>
			{/if}
			{#if stop_btn}
				<button
					class="stop-button"
					class:padded-button={stop_btn !== true}
					title={stop_btn_title}
					on:click={handle_stop}
				>
					{#if stop_btn === true}
						<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
							<rect x="8" y="8" width="8" height="8" rx="1" ry="1"/>
						</svg>
					{:else}
						{stop_btn}
					{/if}
				</button>
			{/if}
		</div>
	</label>
</div>

<style>


	.full-container {
		width: 100%;
		position: relative;
	}

	.full-container.dragging::after {
		content: "";
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		pointer-events: none;
	}

	.input-container {
		display: flex;
		position: relative;
	    /* centrer verticalement les boutons de la multimodale textbox */
		align-items: center;
	}

	textarea {
		flex-grow: 1;
		outline: none !important;
		background: var(--block-background-fill);
		padding: var(--input-padding);
		color: var(--body-text-color);
		font-weight: var(--input-text-weight);
		font-size: var(--input-text-size);
		line-height: var(--line-sm);
		border: none;
		margin-top: 0px;
		margin-bottom: 0px;
		resize: none;
		position: relative;
		z-index: 1;
	}
	textarea.no-label {
		padding-top: 5px;
		padding-bottom: 5px;
	}

	textarea:disabled {
		-webkit-opacity: 1;
		opacity: 1;
		color: var(--input-placeholder-color)
	}

	textarea::placeholder {
		color: var(--input-placeholder-color);
	}

	.upload-button,
	.submit-button,
	.stop-button,
	.stop-audio-button,
	.audio-button {
		border: none;
		text-align: center;
		text-decoration: none;
		font-size: 14px;
		cursor: pointer;
		overflow: hidden;
		border-radius: 50px;
		min-width: 18px;
		height: 18px;
		width: 18px;
		margin: 3px;
		flex-shrink: 0;
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: var(--layer-1);
	}

	.upload-button, .submit-button {
		background-color:var(--button-secondary-background-fill);
		stroke:var(--button-secondary-text-color);
	}

	.upload-button {
		margin-right:0px;
	}

	.submit-button, .stop-button, .stop-audio-button, .audio-button {
		margin-left:0px;
	}
	
	.stop-button svg {
		background-color:var(--button-cancel-background-fill);
		fill:var(--button-cancel-text-color);
		stroke:var(--button-cancel-text-color);
	}
	
	.stop-audio-button {
		background-color:var(--button-cancel-background-fill);
	}
	.stop-audio-button svg {
		stroke:var(--button-cancel-text-color);
	}

	.padded-button {
		padding: 0 10px;
	}

	.upload-button,
	.submit-button,
	.audio-button {
		background: var(--button-secondary-background-fill);
	}

	.upload-button:hover,
	.submit-button:hover,
	.audio-button:hover {
		background: var(--button-secondary-background-fill-hover);
	}

	.upload-button:disabled,
	.submit-button:disabled,
	.audio-button:disabled {
		background: var(--button-secondary-background-fill);
		cursor: initial;
	}
	.upload-button:active,
	.submit-button:active,
	.audio-button:active {
		box-shadow: var(--button-shadow-active);
	}
</style>
